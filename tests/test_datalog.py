import os
import csv
import subprocess
import shutil
import pytest

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
FACTS_DIR = os.path.join(BASE_DIR, "db")
OUTPUT_DIR = os.path.join(BASE_DIR, "out")

@pytest.fixture(scope="module")
def setup_env():
    # Setup test directories
    if os.path.exists(FACTS_DIR): shutil.rmtree(FACTS_DIR)
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
    os.makedirs(FACTS_DIR)
    os.makedirs(OUTPUT_DIR)
    yield
    # Cleanup
    # shutil.rmtree(FACTS_DIR)
    # shutil.rmtree(OUTPUT_DIR)

def create_small_graph():
    # Triangle Graph: 1-2, 2-3, 3-1
    edges = [("1", "2"), ("2", "3"), ("3", "1"), ("1", "4")] # Node 4 is a leaf
    with open(os.path.join(FACTS_DIR, "edge.facts"), "w") as f:
        for u, v in edges:
            f.write(f"{u}\t{v}\n")
    return edges

def test_statistics_logic(setup_env):
    create_small_graph()
    
    # Run statistics.dl
    cmd = ["souffle", "-F", FACTS_DIR, "-D", OUTPUT_DIR, os.path.join(PROJECT_DIR, "src", "statistics.dl")]
    subprocess.run(cmd, check=True)
    
    # Check Degrees
    # 1: connected to 2,3,4 -> degree 3
    # 2: connected to 1,3 -> degree 2
    # 3: connected to 1,2 -> degree 2
    # 4: connected to 1 -> degree 1
    degrees = {}
    with open(os.path.join(OUTPUT_DIR, "stats_degree.csv"), "r") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
             degrees[row[0]] = int(row[1])
             
    assert degrees["1"] == 3
    assert degrees["4"] == 1
    
    # Check Triangles
    # Only one triangle (1-2-3)
    with open(os.path.join(OUTPUT_DIR, "stats_triangles.csv"), "r") as f:
        val = int(f.read().strip())
        assert val == 1

def test_modularity_logic(setup_env):
    create_small_graph()
    
    # Mock Community Structure
    # Comm A: {1, 2, 3} (The triangle)
    # Comm B: {4} (The leaf)
    with open(os.path.join(FACTS_DIR, "community.csv"), "w") as f:
        f.write("1\tA\n")
        f.write("2\tA\n")
        f.write("3\tA\n")
        f.write("4\tB\n")
        
    # Run modularity.dl
    cmd = ["souffle", "-F", FACTS_DIR, "-D", OUTPUT_DIR, os.path.join(PROJECT_DIR, "src", "modularity.dl")]
    subprocess.run(cmd, check=True)
    
    # Check Result
    # Edges (M) = 4
    # Comm A: Internal Edges = 3 (1-2, 2-3, 3-1), Degree Sum = 3+2+2 = 7
    # Comm B: Internal Edges = 0, Degree Sum = 1
    # Q = [3/4 - (7/8)^2] + [0/4 - (1/8)^2] 
    #   = [0.75 - 0.7656] + [0 - 0.0156]
    #   = -0.0156 - 0.0156 = -0.03 approx
    
    with open(os.path.join(OUTPUT_DIR, "stats_modularity.csv"), "r") as f:
        val = float(f.read().strip())
        assert -0.1 < val < 0.1 # Just checking it runs and produces a number in range
