"""
app.py — Flask Portfolio
Run with: python app.py
Then open http://127.0.0.1:8080
"""

from flask import Flask, render_template, request, jsonify
import data
import analytics

app = Flask(__name__)
# ── Home / CV page ───────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template(
        "index.html",
        name=data.NAME,
        tagline=data.TAGLINE,
        about=data.ABOUT,
        skills=data.SKILLS,
        experiences=data.WORK_EXPERIENCES,
        projects=data.PROJECTS,
        presentations=data.PRESENTATIONS,
        contact=data.CONTACT,
    )
# ── Writing / Papers page ────────────────────────────────────────────
@app.route("/writing")
def writing():
    return render_template(
        "writing.html",
        name=data.NAME,
        papers=data.PAPERS,
        writing_intro=data.WRITING_INTRO,
    )
# ── Analytics Tool page ──────────────────────────────────────────────
@app.route("/analytics")
def analytics_page():
    return render_template(
        "analytics.html",
        name=data.NAME,
        tool_title=data.ANALYTICS_TOOL_TITLE,
        tool_description=data.ANALYTICS_TOOL_DESCRIPTION,
        tool_instructions=data.ANALYTICS_TOOL_INSTRUCTIONS,
        node_count=analytics.G.number_of_nodes(),
        edge_count=analytics.G.number_of_edges(),
    )
# ── Run analytics (called by the search form via fetch) ──────────────
@app.route("/run-analytics", methods=["POST"])
def run_analytics():
    try:
        user_input = request.json.get("data", "")
        result = analytics.run(user_input)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


import scinet

@app.route("/scinet")
def scinet_page():
    return render_template("scinet.html", name=data.NAME)

@app.route("/run-scinet", methods=["POST"])
def run_scinet():
    try:
        body         = request.json
        query        = body.get("query", "")
        network_type = body.get("network_type", "coauthorship")
        n            = int(body.get("n", 20))
        result       = scinet.run(query, network_type, n, data.SEMANTIC_SCHOLAR_API_KEY)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ── Autocomplete endpoint — returns all node labels ──────────────────
@app.route("/autocomplete")
def autocomplete():
    labels = analytics.get_all_labels()
    return jsonify(labels)
if __name__ == "__main__":
    app.run(debug=True, port=8080)