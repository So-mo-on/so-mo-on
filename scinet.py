"""
scinet.py — SciNet Backend
===========================
Two network types:
  1. Co-authorship network
  2. Paper similarity network (TF-IDF)

Both include fields of study statistics.
"""

import re
import math
import requests
import numpy as np
import pandas as pd
import networkx as nx
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


# ── Helpers ───────────────────────────────────────────────────────────

def normalize_author_name(name: str) -> str:
    if re.match(r"^[A-Z]\.\s?[A-Z][a-z]+$", name):
        return name.strip()
    parts = name.strip().split()
    if not parts:
        return name
    first   = parts[0]
    initial = (first[0].upper() + ".") if len(first) > 1 else (first + ".")
    return f"{initial} {parts[-1].capitalize()}"


def _scale_pos(pos):
    """Scale spring layout positions to canvas coords (80–720 x, 60–540 y)."""
    xs = [v[0] for v in pos.values()]
    ys = [v[1] for v in pos.values()]
    xr = (max(xs) - min(xs)) or 1
    yr = (max(ys) - min(ys)) or 1
    return {
        n: (80  + (x - min(xs)) / xr * 640,
            60  + (y - min(ys)) / yr * 480)
        for n, (x, y) in pos.items()
    }


def _graph_to_canvas(G, pos, label_fn, color="#ccdaa6"):
    degrees   = dict(G.degree())
    max_deg   = max(degrees.values()) if degrees else 1
    min_deg   = min(degrees.values()) if degrees else 0
    deg_range = (max_deg - min_deg) or 1

    nodes_out = []
    for nid in G.nodes():
        x, y = pos[nid]
        deg  = degrees[nid]
        size = 8 + ((deg - min_deg) / deg_range) * 20
        nodes_out.append({
            "id":     str(nid),
            "label":  label_fn(nid),
            "x":      round(x, 1),
            "y":      round(y, 1),
            "size":   round(size, 1),
            "color":  color,
            "degree": deg,
        })

    max_w = max((d.get("weight", 1) for _, _, d in G.edges(data=True)), default=1)
    edges_out = []
    for src, tgt, edata in G.edges(data=True):
        w = edata.get("weight", 1)
        edges_out.append({
            "src": str(src), "tgt": str(tgt),
            "weight": round(w / max_w, 3),
            "x0": round(pos[src][0], 1), "y0": round(pos[src][1], 1),
            "x1": round(pos[tgt][0], 1), "y1": round(pos[tgt][1], 1),
        })

    return nodes_out, edges_out


def _fields_stats(df) -> dict:
    """Count fields of study across all papers."""
    all_fields = []
    for fields in df.get("Fields", []):
        if isinstance(fields, list):
            all_fields.extend([f for f in fields if f])
    return dict(Counter(all_fields).most_common(10))


# ── 1. Co-authorship ──────────────────────────────────────────────────

def search_papers(query: str, n: int, api_key: str) -> pd.DataFrame:
    resp = requests.get(BASE_URL, timeout=15,
        headers={"x-api-key": api_key},
        params={"query": query, "limit": n,
                "fields": "title,authors,citationCount,url,year,fieldsOfStudy"})
    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text}")

    records = []
    for p in resp.json().get("data", []):
        records.append({
            "Title":    p.get("title") or "Unknown",
            "Authors":  [normalize_author_name(a.get("name", ""))
                         for a in p.get("authors", [])],
            "Year":     p.get("year") or "?",
            "Citations": p.get("citationCount") or 0,
            "URL":       p.get("url") or "#",
            "Fields":   p.get("fieldsOfStudy") or [],
        })
    df = pd.DataFrame(records)
    df = df.fillna("?")
    return df


def build_coauthorship_network(query: str, n: int, api_key: str) -> dict:
    df = search_papers(query, n, api_key)
    if df.empty:
        return {"error": "No papers found for this query."}

    unique_authors = np.unique(np.concatenate(df["Authors"].values))
    auth_idx       = {a: i for i, a in enumerate(unique_authors)}
    n_auth         = len(unique_authors)
    mat            = np.zeros((n_auth, n_auth), dtype=int)

    for authors in df["Authors"]:
        idxs = [auth_idx[a] for a in authors]
        mat[np.ix_(idxs, idxs)] += 1
    np.fill_diagonal(mat, 0)

    G          = nx.from_numpy_array(mat)
    components = list(nx.connected_components(G))
    if not components:
        return {"error": "No connected authors found."}

    giant   = G.subgraph(max(components, key=len)).copy()
    mapping = {i: unique_authors[i] for i in giant.nodes()}
    giant   = nx.relabel_nodes(giant, mapping)
    pos     = _scale_pos(nx.spring_layout(giant, seed=42))

    nodes_out, edges_out = _graph_to_canvas(giant, pos,
                                            label_fn=str, color="#ccdaa6")

    degrees     = dict(giant.degree())
    top_authors = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "found":          True,
        "network_type":   "coauthorship",
        "query":          query,
        "paper_count":    len(df),
        "node_count":     giant.number_of_nodes(),
        "edge_count":     giant.number_of_edges(),
        "nodes":          nodes_out,
        "edges":          edges_out,
        "top_authors":    [{"name": a, "collaborations": d} for a, d in top_authors],
        "fields_of_study": _fields_stats(df),
        "papers":         df[["Title", "Authors", "Year", "Citations", "URL"]].to_dict("records"),
    }


# ── 2. Paper similarity ───────────────────────────────────────────────

def search_papers_with_abstracts(query: str, n: int, api_key: str) -> pd.DataFrame:
    resp = requests.get(BASE_URL, timeout=15,
        headers={"x-api-key": api_key},
        params={"query": query, "limit": n,
                "fields": "title,authors,citationCount,url,year,abstract,fieldsOfStudy"})
    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text}")

    records = []
    for p in resp.json().get("data", []):
        records.append({
            "Title":    p.get("title") or "Unknown",
            "Authors":  [normalize_author_name(a.get("name", ""))
                         for a in p.get("authors", [])],
            "Year":     p.get("year") or "?",
            "Citations": p.get("citationCount") or 0,
            "URL":       p.get("url") or "#",
            "Abstract":  p.get("abstract") or "",
            "Fields":   p.get("fieldsOfStudy") or [],
        })
    df = pd.DataFrame(records)
    df = df.fillna("?")
    return df


def build_paper_similarity_network(query: str, n: int, api_key: str,
                                   threshold: float = 0.1) -> dict:
    df = search_papers_with_abstracts(query, n, api_key)
    if df.empty:
        return {"error": "No papers found for this query."}

    abstracts  = df["Abstract"].replace("?", "").tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf      = vectorizer.fit_transform(abstracts)
    sim_matrix = cosine_similarity(tfidf)

    G = nx.Graph()
    for i, row in df.iterrows():
        G.add_node(i, title=row["Title"], url=row["URL"])
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            if sim_matrix[i, j] > threshold:
                G.add_edge(i, j, weight=float(sim_matrix[i, j]))

    components = list(nx.connected_components(G))
    if not components:
        return {"error": "No similar papers found. Try a broader query."}

    giant   = G.subgraph(max(components, key=len)).copy()
    idx_map = {i: i for i in giant.nodes()}
    mapping = {i: df.loc[i, "Title"] for i in giant.nodes()}
    title_to_idx = {df.loc[i, "Title"]: i for i in giant.nodes()}
    giant   = nx.relabel_nodes(giant, mapping)
    pos     = _scale_pos(nx.spring_layout(giant, seed=42))

    def short_label(title):
        return title[:28] + "…" if len(title) > 28 else title

    nodes_out, edges_out = _graph_to_canvas(giant, pos,
                                            label_fn=short_label, color="#98b4c8")

    for nd in nodes_out:
        orig_idx = title_to_idx.get(nd["id"])
        if orig_idx is not None:
            nd["url"]        = df.loc[orig_idx, "URL"]
            nd["full_title"] = df.loc[orig_idx, "Title"]

    return {
        "found":           True,
        "network_type":    "similarity",
        "query":           query,
        "paper_count":     len(df),
        "node_count":      giant.number_of_nodes(),
        "edge_count":      giant.number_of_edges(),
        "nodes":           nodes_out,
        "edges":           edges_out,
        "fields_of_study": _fields_stats(df),
        "papers":          df[["Title", "Authors", "Year", "Citations", "URL"]].to_dict("records"),
    }


# ── Entry point ───────────────────────────────────────────────────────

def run(query: str, network_type: str, n: int, api_key: str) -> dict:
    if not query.strip():
        return {"error": "Please enter a search query."}
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return {"error": "API key not configured. Add SEMANTIC_SCHOLAR_API_KEY to data.py."}
    try:
        if network_type == "coauthorship":
            return build_coauthorship_network(query, n, api_key)
        else:
            return build_paper_similarity_network(query, n, api_key)
    except Exception as e:
        return {"error": str(e)}