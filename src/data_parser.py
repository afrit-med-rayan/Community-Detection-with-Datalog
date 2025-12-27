import csv
import os

def csv_to_facts(input_csv, output_dir):
    """Convert edge list CSV to Datalog facts"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    nodes = set()
    edges = []
    
    print(f"Reading from {input_csv}...")
    with open(input_csv, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                # Assuming headerless or skipping simple checks for now
                if row[0].startswith('#') or row[0] == "source": continue 
                
                source, target = row[0].strip(), row[1].strip()
                nodes.add(source)
                nodes.add(target)
                edges.append((source, target))
    
    # Write node.facts
    node_file = os.path.join(output_dir, "node.facts")
    with open(node_file, 'w', newline='\n') as f:
        for node in sorted(list(nodes)):
            f.write(f"{node}\n")
    
    # Write edge.facts (comma-separated now)
    edge_file = os.path.join(output_dir, "edge.facts")
    with open(edge_file, 'w', newline='\n') as f:
        for source, target in edges:
            f.write(f"{source},{target}\n")
    
    # Write config (max iterations)
    config_file = os.path.join(output_dir, "config_max_iter.facts")
    with open(config_file, 'w', newline='\n') as f:
        f.write("20\n")  # Max 20 iterations
    
    print(f"✓ Generated facts for {len(nodes)} nodes, {len(edges)} edges in '{output_dir}/'")
