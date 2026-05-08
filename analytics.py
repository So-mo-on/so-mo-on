import os
import math
import pandas as pd
import networkx as nx

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
NODES_CSV = os.path.join(BASE_DIR, "static", "nodes.csv")
EDGES_CSV = os.path.join(BASE_DIR, "static", "edges.csv")

# Load CSVs and build graph once at startup
nodes_df = pd.read_csv(NODES_CSV)
edges_df = pd.read_csv(EDGES_CSV)

G = nx.Graph()  # undirected — simpler to visualize

for _, row in nodes_df.iterrows():
    G.add_node(str(row["Id"]), label=str(row["Label"]))

# ADD THESE TWO LINES:
print("columns:", nodes_df.columns.tolist())
print("first node:", list(G.nodes(data=True))[0])

for _, row in edges_df.iterrows():
    src = str(int(row["Source"]) - 1)
    tgt = str(int(row["Target"]) - 1)
    G.add_edge(src, tgt, weight=float(row.get("Weight", 1.0)))
# label → id lookup (case insensitive)
LABEL_TO_ID = {
    data["label"].lower(): nid
    for nid, data in G.nodes(data=True)
}

print(f"Graph ready: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
print("Sample node data:", list(G.nodes(data=True))[:2])

def run(query: str) -> dict:
    query = query.strip().lower()
    if not query:
        return {"error": "Please type a node name."}

    # Find node — exact match first, then partial
    node_id = LABEL_TO_ID.get(query)
    if node_id is None:
        for label, nid in LABEL_TO_ID.items():
            if query in label:
                node_id = nid
                break

    if node_id is None:
        return {"error": f"No node found for '{query}'."}

    # Get 1st and 2nd neighbours
    first  = set(G.neighbors(node_id))
    second = set()
    for n in first:
        second.update(G.neighbors(n))
    second -= first
    second.discard(node_id)

    # All nodes to show
    all_nodes = {node_id} | first | second

    # Simple circular layout: center → 1st ring → 2nd ring
    positions = {}
    positions[node_id] = (400, 300)

    first = list(first)
    for i, nid in enumerate(first):
        angle = 2 * math.pi * i / len(first)
        positions[nid] = (400 + 160 * math.cos(angle), 300 + 160 * math.sin(angle))

    second = list(second)
    for i, nid in enumerate(second):
        angle = 2 * math.pi * i / max(len(second), 1)
        positions[nid] = (400 + 290 * math.cos(angle), 300 + 290 * math.sin(angle))

    # Build node list for the browser
    nodes_out = []
    for nid in all_nodes:
        x, y = positions[nid]
        if nid == node_id:
            color, size = "#d69799", 16
        elif nid in set(first):
            color, size = "#ccdaa6", 10
        else:
            color, size = "#98b4c8", 7
        nodes_out.append({
            "id": nid,
            "label": G.nodes[nid]["label"],
            "x": round(x, 1), "y": round(y, 1),
            "color": color, "size": size,
        })

    # Build edge list — only edges within our visible nodes
    edges_out = []
    for a, b in G.edges():
        if a in all_nodes and b in all_nodes:
            ax, ay = positions[a]
            bx, by = positions[b]
            edges_out.append({"src": a, "tgt": b, "x0": ax, "y0": ay, "x1": bx, "y1": by, "weight": round(G[a][b].get("weight", 1.0), 3)})

    return {
        "node_label": G.nodes[node_id]["label"],
        "nodes": nodes_out,
        "edges": edges_out,
    }


def get_all_labels():
    return sorted([data["label"] for _, data in G.nodes(data=True)])