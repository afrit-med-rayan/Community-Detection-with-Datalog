import networkx as nx
import matplotlib.pyplot as plt
import csv
import os

def plot_communities(edge_file, community_file, output_path="output/communities.png"):
    """Visualize detected communities"""
    print(f"Visualizing results...")
    
    if not os.path.exists(community_file):
        print(f"❌ Error: Community file not found at {community_file}")
        return

    # Load graph
    G = nx.Graph()
    with open(edge_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                if row[0].startswith('#') or row[0] == "source": continue
                G.add_edge(row[0].strip(), row[1].strip())
    
    # Load communities
    node_colors = {}
    communities = {}
    with open(community_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if not row: continue
            node, comm = row[0], row[1]
            node_colors[node] = comm
            if comm not in communities:
                communities[comm] = []
            communities[comm].append(node)
    
    if not communities:
        print("⚠ No communities found to visualize.")
        return

    # Assign colors
    # Use tab20 for good distinction, fallback to set3
    colors = plt.cm.tab20(range(len(communities)))
    color_map = []
    
    # We need to map community IDs to an index 0..N
    comm_to_idx = {comm: i for i, comm in enumerate(communities.keys())}
    
    for node in G.nodes():
        if node in node_colors:
            comm_idx = comm_to_idx[node_colors[node]]
            # Cyclic color usage if > 20 communities
            color_map.append(colors[comm_idx % 20])
        else:
            color_map.append((0.8, 0.8, 0.8, 1.0)) # Grey for unassigned

    # Plot
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, seed=42, k=0.3) # k=0.3 spreads nodes out
    
    nx.draw_networkx_nodes(G, pos, 
                          node_color=color_map,
                          node_size=300, 
                          alpha=0.9, 
                          edgecolors='white')
                          
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    
    plt.title(f"Detected Communities (LPA)\n{min(len(communities), G.number_of_nodes())} Clusters Found")
    plt.axis('off')
    plt.tight_layout()
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plt.savefig(output_path, dpi=300)
    print(f"✓ Saved visualization to {output_path}")
    plt.close()
