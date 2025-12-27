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

    # 3. Run Soufflé (Iterative Label Propagation)
    lpa_step_file = "src/lpa_step.dl"
    
    # Initialize labels: Each node is its own label
    node_file = os.path.join(FACTS_DIR, "node.facts")
    label_file = os.path.join(FACTS_DIR, "label.facts")
    
    nodes = []
    if os.path.exists(node_file):
        with open(node_file, 'r') as f:
            nodes = [line.strip() for line in f if line.strip()]
            
    current_labels = {n: n for n in nodes}
    
    def write_labels(labels_map, filepath):
        with open(filepath, 'w', newline='\n') as f:
            for n, l in labels_map.items():
                f.write(f"{n},{l}\n")

    # Read Max Iter
    MAX_ITER = 20
    config_file = os.path.join(FACTS_DIR, "config_max_iter.facts")
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                MAX_ITER = int(f.read().strip())
        except: pass

    # Iteration Loop
    converged = False
    debug_log = []
    
    def log(msg):
        print(msg)
        debug_log.append(msg)

    # DEBUG: Check if files exist and are not empty
    abs_facts_dir = os.path.abspath(FACTS_DIR)
    abs_output_dir = os.path.abspath(OUTPUT_DIR)
    edge_fact_path = os.path.join(abs_facts_dir, "edge.facts")
    
    if os.path.exists(edge_fact_path):
        size = os.path.getsize(edge_fact_path)
        log(f"Debug: edge.facts size is {size} bytes at {edge_fact_path}")
        # Read first few lines to verify format
        with open(edge_fact_path, 'r') as f:
            first_lines = [f.readline().strip() for _ in range(3)]
            log(f"Debug: First 3 lines of edge.facts: {first_lines}")
        if size == 0:
            log("CRITICAL: edge.facts is empty!")
    else:
        log(f"CRITICAL: edge.facts not found at {edge_fact_path}")

    log(f"Starting Analysis. Nodes: {len(nodes)}, Initial Labels: {len(current_labels)}")

    for i in range(MAX_ITER):
        # Write current labels to FACTS_DIR/label.facts
        write_labels(current_labels, label_file)

        # Run one step
        abs_lpa_file = os.path.abspath(lpa_step_file)
        
        # Use ABSOLUTE paths for -F and -D to avoid ambiguity
        cmd = ["souffle", "-F", abs_facts_dir, "-D", abs_output_dir, abs_lpa_file]
        
        log(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, check=True, text=True)
            if result.stdout:
                log(f"Souffle stdout: {result.stdout[:200]}")
            if result.stderr:
                log(f"Souffle stderr: {result.stderr[:200]}")
        except subprocess.CalledProcessError as e:
             err_msg = f"Souffle Execution Failed at Iteration {i}. Stderr: {e.stderr}"
             log(err_msg)
             log(f"Souffle stdout: {e.stdout}")
             break

        # Read new labels
        output_label_file = os.path.join(abs_output_dir, "label_new.csv") 
        
        new_labels = {}
        if os.path.exists(output_label_file):
            log(f"Debug: label_new.csv exists, size={os.path.getsize(output_label_file)}")
            with open(output_label_file, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if len(row) >= 2:
                        new_labels[row[0]] = row[1]
        else:
            log(f"Debug: label_new.csv NOT FOUND at {output_label_file}")
        
        log(f"Iteration {i}: Computed {len(new_labels)} labels.")

        if not new_labels:
            log(f"Warning: No new labels generated in iteration {i}. Keeping previous labels.")
            break

        if new_labels == current_labels:
            converged = True
            log(f"Converged at iteration {i}")
            break
        
        current_labels = new_labels

    # Write final community file
    community_file = os.path.join(abs_output_dir, "community.facts")
    write_labels(current_labels, community_file)
    log(f"Written final community file with {len(current_labels)} entries.")
    
    # ALSO copy to facts dir for modularity.dl to read (it uses -F input dir)
    import shutil
    community_facts_input = os.path.join(abs_facts_dir, "community.facts")
    shutil.copy(community_file, community_facts_input)
    log(f"Copied community.facts to {community_facts_input} for modularity input.")

    # ---------------------------------------------------------
    # 3b. Run Post-Processing Datalog (Statistics & Modularity)
    # ---------------------------------------------------------
    
    # Run Modularity logic (Datalog)
    log("Running Modularity Calculation in Datalog...")
    try:
        result = subprocess.run(["souffle", "-F", abs_facts_dir, "-D", abs_output_dir, os.path.abspath("src/modularity.dl")], 
                              capture_output=True, check=True, text=True)
        if result.stderr:
            log(f"Modularity stderr: {result.stderr[:200]}")
    except subprocess.CalledProcessError as e:
        log(f"Modularity Datalog failed: {e}")
        log(f"Modularity stderr: {e.stderr}")

    # Run Statistics logic (Datalog)
    log("Running Statistics Calculation in Datalog...")
    try:
        result = subprocess.run(["souffle", "-F", abs_facts_dir, "-D", abs_output_dir, os.path.abspath("src/statistics.dl")], 
                              capture_output=True, check=True, text=True)
        if result.stderr:
            log(f"Statistics stderr: {result.stderr[:200]}")
        # Check if output was created
        deg_file = os.path.join(abs_output_dir, "node_degree.csv")
        if os.path.exists(deg_file):
            log(f"Debug: node_degree.csv created, size={os.path.getsize(deg_file)}")
            with open(deg_file, 'r') as f:
                first_line = f.readline().strip()
                log(f"Debug: First line of node_degree.csv: {first_line}")
        else:
            log("Debug: node_degree.csv NOT created!")
    except subprocess.CalledProcessError as e:
        log(f"Statistics Datalog failed: {e}")
        log(f"Statistics stderr: {e.stderr}")

    # 4. Parse Outputs for Frontend
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
    if os.path.exists(community_file):
        with open(community_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row:
                    node_groups[row[0]] = row[1]
    
    log(f"Loaded {len(node_groups)} groups from community file.")

    # Read Stats (Degrees)
    node_degrees = {}
    degree_file = os.path.join(abs_output_dir, "node_degree.csv")
    if os.path.exists(degree_file):
         with open(degree_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row: node_degrees[row[0]] = row[1]

    # Build Node List
    nodes = []
    # Statistics for Comm Count
    comm_map = {} 
    
    for n in nodes_set:
        group = node_groups.get(n, "0")
        degree = node_degrees.get(n, "0")
        
        # Add degree to label for visibility
        label_text = f"{n} (d={degree})"
        
        nodes.append({"id": n, "label": label_text, "group": group, "value": int(degree)})
        
        if group not in comm_map: comm_map[group] = []
        comm_map[group].append(n)
        
    # Read Modularity from Datalog Output
    modularity = 0.0
    modularity_file = os.path.join(abs_output_dir, "modularity.csv")
    if os.path.exists(modularity_file):
        try:
            with open(modularity_file, 'r') as f:
                val = f.read().strip()
                modularity = float(val) if val else 0.0
        except: pass

    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "modularity": round(modularity, 4),
        "community_count": len(comm_map),
        "debug_log": debug_log
    })

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
