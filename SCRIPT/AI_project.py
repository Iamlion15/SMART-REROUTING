import pandas as pd
import networkx as nx
import numpy as np
from fuzzywuzzy import process  # Install fuzzywuzzy using pip if not already installed
import os


# Load and preprocess the graph
def load_and_prepare_graph(file_path):
    roads_df = pd.read_csv(file_path, encoding="latin1")

    # Normalize LENGTHKM and AADT
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    roads_df[['LENGTHKM', 'AADT']] = scaler.fit_transform(roads_df[['LENGTHKM', 'AADT']])

    # Convert conditions and surfaces to numerical values
    condition_weights = {'Good': 1, 'Fair': 2, 'Poor': 3, 'Very Poor': 4}
    surface_weights = {'Paved': 1, 'Gravel': 2, 'Earth': 3}
    roads_df['CONDITION_WEIGHT'] = roads_df['CONDITION'].map(condition_weights).fillna(3)
    roads_df['SURFACE_WEIGHT'] = roads_df['SURFTYPE'].map(surface_weights).fillna(3)

    # Create the graph
    G = nx.DiGraph()
    for _, row in roads_df.iterrows():
        weight = (
            row['LENGTHKM'] * 0.4 +
            row['AADT'] * 0.3 +
            row['CONDITION_WEIGHT'] * 0.2 +
            row['SURFACE_WEIGHT'] * 0.1
        )
        G.add_edge(row['STARTDESC'], row['ENDDESC'], weight=weight, condition=row['CONDITION_WEIGHT'])
    return G

# Standardize input for exact matching
def standardize_input(input_str):
    return input_str.strip().upper()

# Find all paths and calculate the optimal path
def find_optimal_path(start_node, end_node):
    graph=load_and_prepare_graph("./SCRIPT/Angola_Roads.csv")
    # Standardize inputs
    start_node = standardize_input(start_node)
    end_node = standardize_input(end_node)

    # Match start and end nodes
    all_nodes = list(graph.nodes)
    start_match = process.extractOne(start_node, all_nodes)
    end_match = process.extractOne(end_node, all_nodes)

    # Verify matches
    if start_match is None or start_match[1] < 80:  # Adjust threshold if necessary
        print(f"Start node '{start_node}' not found. Closest match: {start_match}")
        print("Available nodes in the graph:", all_nodes)
        return None
    if end_match is None or end_match[1] < 80:
        print(f"End node '{end_node}' not found. Closest match: {end_match}")
        print("Available nodes in the graph:", all_nodes)
        return None

    # Use matched nodes
    start_node = start_match[0]
    end_node = end_match[0]
    paths=[]

    print(f"Matched Start Node: {start_node}")
    print(f"Matched End Node: {end_node}")

    # Get all paths between start and end nodes
    all_paths = list(nx.all_simple_paths(graph, source=start_node, target=end_node))
    print(f"Paths from {start_node} to {end_node}:")

    if not all_paths:
        print(f"No paths found between {start_node} and {end_node}.")
        # Check if the nodes are isolated
        if not nx.has_path(graph, start_node, end_node):
            print("The graph shows no connectivity between these nodes.")
        return None

    for path in all_paths:
        paths.append(path)
        print(path)

    # Evaluate each path and select the optimal path
    path_scores = []
    for path in all_paths:
        path_weight = sum(graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        path_scores.append((path, path_weight))

    # Find the optimal path (lowest weight)
    optimal_path, optimal_score = min(path_scores, key=lambda x: x[1])
    print(f"Optimal Path: {optimal_path}, Optimal Score: {optimal_score}")

    return optimal_path, optimal_score,paths

# Main script
if __name__ == "__main__":
    dataset_path = "./SCRIPT/Angola_Roads.csv"  # Update with your dataset path

    # Load graph and preprocess
    road_graph = load_and_prepare_graph(dataset_path)

    # Input start and end nodes
    start_node = input("Enter the start location: ")
    end_node = input("Enter the end location: ")

    # Find optimal path
    result = find_optimal_path(road_graph, start_node, end_node)

    if result:
        optimal_path, optimal_score = result
        print(f"Optimal Path: {optimal_path}")
        print(f"Optimal Score: {optimal_score}")
    else:
        print("No optimal path could be found.")