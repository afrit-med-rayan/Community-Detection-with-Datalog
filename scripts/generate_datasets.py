"""
Generate additional datasets for community detection testing.
Downloads/generates: Dolphin, Les Miserables, and Football networks.
"""

import networkx as nx
import os

def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def generate_dolphin_network(data_dir):
    """Generate Dolphin social network (62 nodes, 159 edges)."""
    print("Generating Dolphin network...")
    try:
        # NetworkX has this built-in
        G = nx.read_gml(nx.utils.misc.get_data_path('dolphins.gml'))
        
        output_file = os.path.join(data_dir, "dolphin.csv")
        with open(output_file, 'w') as f:
            for u, v in G.edges():
                f.write(f"{u},{v}\n")
        
        print(f"✓ Generated {output_file}: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return True
    except Exception as e:
        print(f"⚠ Could not generate from NetworkX: {e}")
        return False

def generate_lesmis_network(data_dir):
    """Generate Les Miserables character network (77 nodes, 254 edges)."""
    print("Generating Les Miserables network...")
    try:
        # NetworkX has this built-in
        G = nx.les_miserables_graph()
        
        output_file = os.path.join(data_dir, "lesmis.csv")
        with open(output_file, 'w') as f:
            for u, v in G.edges():
                f.write(f"{u},{v}\n")
        
        print(f"✓ Generated {output_file}: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return True
    except Exception as e:
        print(f"⚠ Could not generate from NetworkX: {e}")
        return False

def generate_football_network(data_dir):
    """Generate NCAA Football network (115 nodes, 613 edges)."""
    print("Generating Football network...")
    try:
        # NetworkX has this built-in
        G = nx.read_gml(nx.utils.misc.get_data_path('football.gml'))
        
        output_file = os.path.join(data_dir, "football.csv")
        with open(output_file, 'w') as f:
            for u, v in G.edges():
                f.write(f"{u},{v}\n")
        
        print(f"✓ Generated {output_file}: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return True
    except Exception as e:
        print(f"⚠ Could not generate from NetworkX: {e}")
        return False

def main():
    print("=== Dataset Generation ===\n")
    
    data_dir = ensure_data_dir()
    
    # Generate all datasets
    results = {
        "Dolphin": generate_dolphin_network(data_dir),
        "Les Miserables": generate_lesmis_network(data_dir),
        "Football": generate_football_network(data_dir)
    }
    
    print("\n=== Summary ===")
    for name, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {name}")
    
    total = sum(results.values())
    print(f"\n{total}/{len(results)} datasets generated successfully.")

if __name__ == "__main__":
    main()
