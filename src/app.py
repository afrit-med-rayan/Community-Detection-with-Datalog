import os
import csv
import subprocess
import networkx as nx
from flask import Flask, render_template, jsonify, request
from data_parser import csv_to_facts

app = Flask(__name__)

# Configuration
DATA_DIR = "data"
FACTS_DIR = "facts"
OUTPUT_DIR = "output"
DATALOG_FILE = "src/cc_algorithm.dl"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FACTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_analysis():
    # 1. Determine Input File
    input_file = os.path.join(DATA_DIR, "karate.csv")
    
    # Optional: Check if user uploaded a file? 
    # For now, let's keep it simple: Use the karate file or regenerate it.
    if not os.path.exists(input_file):
        G = nx.karate_club_graph()
        with open(input_file, "w") as f:
             for u, v in G.edges():
                 f.write(f"{u},{v}\n")

    # 2. Parse Data to Facts
    try:
        csv_to_facts(input_file, FACTS_DIR)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 3. Run Soufflé
    cmd = ["souffle", "-F", FACTS_DIR, "-D", OUTPUT_DIR, DATALOG_FILE]
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
         return jsonify({"error": "Souffle Execution Failed", "details": e.stderr.decode()}), 500

    # 4. Parse Outputs for Frontend
    # We need: Nodes (id, group), Edges (from, to)
    
    # Read Edges (Structure)
    edges = []
    nodes_set = set()
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                if row[0].startswith('#'): continue
                u, v = row[0].strip(), row[1].strip()
                edges.append({"from": u, "to": v})
                nodes_set.add(u)
                nodes_set.add(v)

    # Read Communities (Groups)
    node_groups = {}
    community_file = os.path.join(OUTPUT_DIR, "community.csv")
    with open(community_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row:
                node_groups[row[0]] = row[1]

    # Build Node List
    nodes = []
    # Calculate Modularity on the fly
    G_nx = nx.Graph()
    G_nx.add_edges_from([(e['from'], e['to']) for e in edges])
    
    # Group for Modularity calc
    comm_map = {} # comm_id -> [nodes]
    
    for n in nodes_set:
        group = node_groups.get(n, "0")
        nodes.append({"id": n, "label": n, "group": group})
        
        if group not in comm_map: comm_map[group] = []
        comm_map[group].append(n)
        
    # Calc Metric
    try:
        modularity = nx.community.modularity(G_nx, list(comm_map.values()))
    except:
        modularity = 0.0

    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "modularity": round(modularity, 4),
        "community_count": len(comm_map)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
