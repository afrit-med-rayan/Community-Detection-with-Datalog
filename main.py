import subprocess
import sys
import os
import argparse
from parser import csv_to_facts
from visualizer import plot_communities

# Configuration
FACTS_DIR = "facts"
OUTPUT_DIR = "output"
DATALOG_FILE = "cc_algorithm.dl"

def check_souffle():
    """Check if souffle is installed."""
    try:
        subprocess.run(["souffle", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def run_community_detection(input_file):
    print("=== Community Detection Pipeline ===")
    
    # Ensure directories exist
    os.makedirs(FACTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Step 1: Parse input
    print("\n[1/4] Parsing input file...")
    try:
        csv_to_facts(input_file, FACTS_DIR)
    except Exception as e:
        print(f"❌ Error parsing input: {e}")
        sys.exit(1)
    
    # Step 2 & 3: Run Datalog (Souffle interprets by default, simpler dev cycle)
    print("\n[2/4] Executing Datalog Engine (Soufflé)...")
    
    if not check_souffle():
        print("❌ 'souffle' executable not found in PATH.")
        print("Please install Soufflé: https://souffle-lang.github.io/install")
        # For demonstration purposes in a non-souffle env, we might warn but here we exit.
        sys.exit(1)

    cmd = [
        "souffle", 
        "-F", FACTS_DIR,      # Input facts directory
        "-D", OUTPUT_DIR,     # Output directory
        DATALOG_FILE          # Datalog source file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Datalog execution failed:\n{result.stderr}")
            sys.exit(1)
        else:
            print("✓ Datalog analysis complete.")
    except Exception as e:
        print(f"❌ Error running subprocess: {e}")
        sys.exit(1)
    
    # Step 4: Visualize
    print("\n[3/4] Visualizing results...")
    community_output = os.path.join(OUTPUT_DIR, "community.csv")
    plot_output = os.path.join(OUTPUT_DIR, "communities.png")
    
    try:
        plot_communities(input_file, community_output, plot_output)
    except Exception as e:
        print(f"⚠ Visualization failed: {e}")
    
    # Calculate Modularity in Python
    print("\n[4/4] Calculating Modularity...")
    try:
        import networkx as nx
        import csv
        
        # Load Graph
        G = nx.Graph()
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    if row[0].startswith('#') or row[0] == "source": continue
                    G.add_edge(row[0].strip(), row[1].strip())
        
        # Load Communities
        communities = {}
        with open(community_output, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if row:
                    node, comm = row[0], row[1]
                    if comm not in communities:
                        communities[comm] = []
                    communities[comm].append(node)
        
        comm_list = list(communities.values())
        if comm_list:
            mod_score = nx.community.modularity(G, comm_list)
            print(f"✓ Modularity Score: {mod_score:.4f}")
            
            # Save to file for report
            with open(os.path.join(OUTPUT_DIR, "modularity_score.txt"), "w") as f:
                f.write(str(mod_score))
        else:
            print("⚠ No communities found.")
            
    except Exception as e:
        print(f"⚠ Modularity calculation failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Datalog Community Detection")
    parser.add_argument("input", nargs="?", default="data/karate.csv", help="Path to input CSV edge list")
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ Input file '{args.input}' not found.")
        print("Creating sample data...")
        # Create a sample file if it doesn't exist just to be helpful
        os.makedirs("data", exist_ok=True)
        import networkx as nx
        G = nx.karate_club_graph()
        with open("data/karate.csv", "w") as f:
             for u, v in G.edges():
                 f.write(f"{u},{v}\n")
        print("✓ Created 'data/karate.csv' using NetworkX built-in data.")
        args.input = "data/karate.csv"
    
    run_community_detection(args.input)
