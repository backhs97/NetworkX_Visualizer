#import lib.
import networkx as nx
import matplotlib.pyplot as plt
import random
import os


#read graph from external file
def read_graph_from_file(filename):
    graph = nx.Graph()

    with open(filename, 'r') as file:
        for line in file:
            nodes = line.strip().split()
            if nodes:
                source = nodes[0]
                for target in nodes[1:]:
                    graph.add_edge(source, target)
    return graph


#function to import a graph from a file
def import_graph():
    input_file = input("Enter the filename (ex. graph.txt) to import the graph from: ")
    if not os.path.isfile(input_file):
        print("Invalid input file. File does not exist.")
        return None
    return read_graph_from_file(input_file)


#save graph to external file
def save_graph_to_file(graph, filename):
    with open(filename, 'w') as file:
        for node in graph.nodes():
            neighbors = " ".join(map(str, graph.neighbors(node)))
            file.write(f"{node} {neighbors}\n")


#function to create a labeled Erdos-Renyi random graph
def create_labeled_erdos_renyi_graph(num_nodes, probability):
    graph = nx.Graph()
    for i in range(num_nodes):
        node_label = input(f"Enter label for node {i + 1}: ") #let the user input the each node label
        graph.add_node(node_label)
    for node1 in graph.nodes():
        for node2 in graph.nodes():
            if node1 != node2 and random.random() < probability:
                graph.add_edge(node1, node2)
    return graph


#show graph
def visualize_graph(graph, shortest_path=None):
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_size=500, font_size=10, font_color='black')

    if shortest_path:
        edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw(graph, pos, edgelist=edges, edge_color='r', width=2)

    plt.show()


#user inputs information of the graph (main)
def main():
    graph = None
    while True:
        print("\nMenu:")
        print("1. Create random graph")
        print("2. Visualize graph")
        print("3. Compute shortest path")
        print("4. Save graph to file")
        print("5. Import graph form file")
        print("6. Exit")
        choice = input("Enter your choice: ")
        #random graph
        if choice == '1':
            try:
                num_nodes = int(input("Enter the number of nodes: "))
                if num_nodes <= 0:
                    raise ValueError("Number of nodes must be a positive integer.")
            except ValueError:
                print("Error: Invalid number of nodes.")
                continue

            try:
                probability = float(input("Enter the probability (0-1): "))
                if probability < 0 or probability > 1:
                    raise ValueError("Probability must be between 0 and 1.")
            except ValueError:
                print("Error: Invalid probability.")
                continue

            graph = create_labeled_erdos_renyi_graph(num_nodes, probability)
            nodes = list(graph.nodes())
            print("Nodes in the graph:", nodes)
        #show graph
        elif choice == '2':
            if graph is not None:  #check if graph is created
                visualize_graph(graph)
            else:
                print("No graph created yet. Please create a graph first.")
        #user inputs two specified nodes for the shortest path
        elif choice == '3':
            if graph is not None:
                source = input("Enter start node: ")
                target = input("Enter target node: ")
                try:
                    shortest_path = nx.shortest_path(graph, source=source, target=target)
                    print("Shortest path:", shortest_path)
                    visualize_graph(graph, shortest_path)
                except nx.NodeNotFound:
                    print("Error: Either start or target node is not in the graph.")
            else:
                print("No graph created yet. Please create a graph first.")
        #save the modified graph to a file
        elif choice == '4':
            if graph is not None:
                output_file = input("Enter the filename to save the graph: ")
                save_graph_to_file(graph, output_file)
                print("Graph saved to", output_file)
            else:
                print("No graph created yet. Please create a graph first.")
        #import graph file
        elif choice == '5':
            imported_graph = import_graph()
            if imported_graph is not None:
                graph = imported_graph
                print("Graph imported successfully.")
        #quit program
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
