---
name: identify-baselines
description: Complete general-purpose workflow to analyze research papers for any literature survey, extract baselines, verify publication venues and core representations via web search, and generate high-resolution interactive timeline visualizations.
---

# Identify Baselines and Generate Timeline Skill

This skill codifies the complete pipeline for analyzing a collection of research papers in **any domain** to extract their core baselines, verify their publication metadata, and visualize their progression over time. 

When invoked to analyze baselines or generate a timeline for a new literature survey, follow these steps sequentially:

## 1. Extract and Structure Baselines
- Read through the provided research papers (or their abstracts/introductions) to identify what previous works they compare against (baselines).
- Create or update a `baselines.md` artifact with a structured table mapping each baseline to the papers that cite/use it.

## 2. Verify Metadata via Web Search
- **Do not rely solely on internal knowledge or arXiv pre-print dates.**
- For every paper in the dataset, perform extensive concurrent web searches using the `search_web` tool.
- **Verify Core Methodology/Representation**: Determine the exact core methodology or representation used by the paper (relevant to the specific domain you are surveying). Pay close attention to explicit user definitions.
- **Verify Conference/Journal Venue**: Identify the true, final publication venue for each paper (e.g., top-tier conferences or journals in the target domain). If a paper is currently listed as an `arXiv` preprint or under review, rigorously search to confirm whether it has since been accepted. Ensure a 1-to-1 accurate matching.

## 3. Update the Dataset
- Update the tracking CSV file (e.g., `paper_details.csv`) with the newly verified data.
- Ensure the CSV contains necessary columns: `Paper,Month,Year,Conference,Conference_Year,Representation` (or domain equivalent).
- Inject the 100% verified venue and methodology values directly into this file, replacing any inferred or outdated data.

## 4. Generate the Visualization Script
- Write or update a python script to generate the timeline graphs using `plotly` and `networkx`. 
- **CRITICAL:** You must use the optimized plotting layout logic below to prevent text overlap, generate interactive HTML hover-tooltips, and draw precise citation edges. 

### Core Plotting & Layout Logic (Python Boilerplate)
Use the following proven code logic to construct the timeline. It includes CSV parsing, baseline network generation, interactive hover text, deterministic beeswarm jitter, and force-directed collision resolution.

```python
import re
import csv
import networkx as nx
from datetime import datetime, timedelta
import plotly.graph_objects as go
from collections import defaultdict

BASELINES_FILE = "notes/baselines.md"
DATES_FILE = "notes/paper_details.csv"

# 1. Load Dates, Conferences, and Representations
paper_dates, paper_conferences, paper_representations = {}, {}, {}
try:
    with open(DATES_FILE, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                date_obj = datetime(year=int(row["Year"]), month=int(row["Month"]), day=1)
                paper_dates[row["Paper"].strip()] = date_obj
                paper_conferences[row["Paper"].strip()] = row.get("Conference", "arXiv").strip()
                paper_representations[row["Paper"].strip()] = row.get("Representation", "Unknown").strip()
            except: pass
except FileNotFoundError: pass

def get_date(p): return paper_dates.get(p.strip(), datetime(2024, 1, 1))

# 2. Build the Citation Network
G = nx.DiGraph()
with open(BASELINES_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("|") and not line.startswith("| :---") and not line.startswith("| Baseline"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                baseline_match = re.search(r'\*\*(.*?)\*\*', parts[1])
                baseline = baseline_match.group(1).strip() if baseline_match else parts[1].strip()
                papers = [p.strip() for p in parts[2].split(",")]
                if baseline and papers and papers[0] != "":
                    G.add_node(baseline)
                    for paper in papers:
                        G.add_node(paper)
                        G.add_edge(paper, baseline)

# 3. Organic Beeswarm Layout
node_x, node_y, ideal_y = {}, {}, {}
# Map your domain's specific categories to Y-axis integers
rep_ideal_y = {"CategoryA": 25, "CategoryB": 12, "CategoryC": 0, "Other": -25, "Unknown": 0}

for node in G.nodes():
    node_x[node] = get_date(node)
    targets = list(G.successors(node))
    if targets:
        ideal_y[node] = sum(rep_ideal_y.get(paper_representations.get(t, "Unknown"), 0) for t in targets) / len(targets)
    else:
        ideal_y[node] = rep_ideal_y.get(paper_representations.get(node, "Unknown"), 0)

month_groups = defaultdict(list)
for node in G.nodes(): month_groups[(get_date(node).year, get_date(node).month)].append(node)

y_spacing = 8.5
for (year, month), nodes in month_groups.items():
    nodes.sort(key=lambda n: ideal_y[n], reverse=True)
    if nodes:
        center_y = sum(ideal_y[n] for n in nodes) / len(nodes)
        N = len(nodes)
        for i, node in enumerate(nodes):
            node_y[node] = center_y + ((N - 1) / 2.0 - i) * y_spacing
            day_offset = (hash(node) % 28) + 1  # Beeswarm Jitter
            node_x[node] = datetime(year, month, 1) + timedelta(days=day_offset)

# 4. Force-Directed Collision Resolution
for iteration in range(300):
    moved = False
    nodes_list = list(G.nodes())
    for i in range(len(nodes_list)):
        for j in range(i + 1, len(nodes_list)):
            n1, n2 = nodes_list[i], nodes_list[j]
            required_dx = (len(n1) + len(n2)) * 2.25 + 25 
            if abs((node_x[n1] - node_x[n2]).days) < required_dx:
                dy = abs(node_y[n1] - node_y[n2])
                if dy < 6.0:
                    push = (6.0 - dy) / 2.0 + 0.1
                    if node_y[n1] >= node_y[n2]: node_y[n1] += push; node_y[n2] -= push
                    else: node_y[n1] -= push; node_y[n2] += push
                    moved = True
    if not moved: break

# 5. Build Plotly Graph with Edges and Interactive Hover
fig = go.Figure()

for edge in G.edges():
    fig.add_annotation(
        x=node_x[edge[1]], y=node_y[edge[1]], ax=node_x[edge[0]], ay=node_y[edge[0]],
        axref="x", ayref="y", xref="x", yref="y",
        showarrow=True, arrowhead=2, arrowsize=1.0, arrowwidth=1.5,
        arrowcolor="rgba(120, 130, 150, 0.35)", standoff=14, startstandoff=14, opacity=0.7
    )

x_vals, y_vals, texts, hover_texts, sizes = [], [], [], [], []
for node in G.nodes():
    x_vals.append(node_x[node])
    y_vals.append(node_y[node])
    texts.append(node)
    sizes.append(20 + (G.in_degree(node) * 3.5))
    
    hover_texts.append(f"<b style='font-size: 16px;'>{node}</b><br>"
                       f"<span style='color: gray;'>Published:</span> {get_date(node).strftime('%b %Y')}<br>"
                       f"<span style='color: gray;'>Venue:</span> {paper_conferences.get(node, 'Unknown')}<br>"
                       f"<span style='color: gray;'>Method:</span> {paper_representations.get(node, 'Unknown')}<br>"
                       f"<span style='color: gray;'>Used By:</span> {G.in_degree(node)} papers")

fig.add_trace(go.Scatter(
    x=x_vals, y=y_vals, mode='markers+text',
    marker=dict(size=sizes, color='#1f77b4', line=dict(width=1.5, color='rgba(255,255,255,0.9)')),
    text=texts, hoverinfo='text', hovertext=hover_texts, textposition="top center",
    textfont=dict(size=16, color='#222222', family="Arial"), showlegend=False
))

fig.update_layout(
    title=dict(text="Literature Timeline", x=0.5, font=dict(size=32)),
    xaxis=dict(title='Publication Timeline', type='date', showgrid=True),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='#fdfdfd', paper_bgcolor='#ffffff',
    width=2400, height=1800, margin=dict(l=40, r=40, t=100, b=60)
)

fig.write_html("interactive_baseline_graph.html")
fig.write_image("baseline_graph.png", scale=3)
```

## 5. Execute and Present
- Run the python script to generate both the static `.png` and the interactive `.html` timeline graphs.
- Instruct the user to open the `.html` file in their browser so they can hover over nodes to instantly see the paper's representation, publication date, venue, and citation count.
- Present the visual masterpieces, highlighting the chronological progression of the literature.
