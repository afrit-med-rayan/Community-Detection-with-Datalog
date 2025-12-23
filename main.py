import subprocess
import sys
import os
import argparse
from parser import csv_to_facts
from visualizer import plot_communities

# Configuration
FACTS_DIR = "facts"
OUTPUT_DIR = "output"
DATALOG_FILE = "lpa_algorithm.dl"

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
    
    # Show modularity
    modularity_file = os.path.join(OUTPUT_DIR, "modularity_score.csv")
    if os.path.exists(modularity_file):
        with open(modularity_file, 'r') as f:
            content = f.read().strip()
            print(f"\n[4/4] ✓ Modularity Score: {content}")
    else:
        print("\n⚠ No modularity score generated.")

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
