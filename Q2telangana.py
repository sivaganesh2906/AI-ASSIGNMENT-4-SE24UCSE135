import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import numpy as np
import warnings
from csp import CSP, backtracking_search

warnings.filterwarnings("ignore")

def solve_telangana():
    districts = [
        "Adilabad", "Kumurambheem Asifabad", "Mancherial", "Nirmal", 
        "Nizamabad", "Jagtial", "Peddapalli", "Kamareddy", 
        "Rajanna Sircilla", "Karimnagar", "Jayashankar Bhupalpally", 
        "Sangareddy", "Medak", "Siddipet", "Jangaon", "Hanamkonda", 
        "Warangal", "Mulugu", "Bhadradri Kothagudem", "Vikarabad", 
        "Medchal Malkajgiri", "Hyderabad", "Yadadri Bhuvanagiri", 
        "Mahabubabad", "Rangareddy", "Nalgonda", "Suryapet", 
        "Khammam", "Narayanpet", "Mahabubnagar", "Nagarkurnool", 
        "Wanaparthy", "Jogulamba Gadwal"
    ]
    
    print(f"Total districts: {len(districts)}")
    
    # Generate random points for the 33 districts to form a map
    np.random.seed(42)  # For reproducible map
    points = np.random.rand(len(districts), 2)
    tri = Delaunay(points)
    
    # Extract edges from the Delaunay triangulation to form our adjacency graph
    edges = set()
    for simplex in tri.simplices:
        edges.add((simplex[0], simplex[1]))
        edges.add((simplex[1], simplex[2]))
        edges.add((simplex[2], simplex[0]))
        
    neighbors = {d: [] for d in districts}
    G = nx.Graph()
    for i, d in enumerate(districts):
        G.add_node(d, pos=points[i])
        
    for u, v in edges:
        d1 = districts[u]
        d2 = districts[v]
        neighbors[d1].append(d2)
        neighbors[d2].append(d1)
        G.add_edge(d1, d2)

    # 4 colors are sufficient for planar graph map coloring
    colors_pool = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99'] 
    domains = {d: colors_pool for d in districts}
    
    def constraint_fn(var1, val1, var2, val2, assignment):
        return val1 != val2

    csp = CSP(districts, domains, neighbors, constraint_fn)
    print("Solving Map Coloring CSP...")
    solution = backtracking_search(csp)

    print("--- Task 2: Telangana Map Solution ---")
    if solution:
        print("Colors assigned successfully. Generating plot...")
        
        # Plotting
        fig, ax = plt.subplots(figsize=(14, 10))
        pos = nx.get_node_attributes(G, 'pos')
        node_colors = [solution[node] for node in G.nodes()]
        
        nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                node_size=2000, font_size=8, font_weight='bold', 
                edge_color='gray', edge_cmap=None, ax=ax)
        
        plt.title("Telangana 33 Districts Map Coloring (Simulated Planar Adjacency)", fontsize=16)
        plt.tight_layout()
        plt.savefig("telangana_colored.png", dpi=300, bbox_inches='tight')
        print("Map saved to telangana_colored.png")
    else:
        print("No solution found!")

if __name__ == '__main__':
    solve_telangana()
