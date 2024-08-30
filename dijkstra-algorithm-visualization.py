import streamlit as st
import random
from graphviz import Digraph
import io
from queue import PriorityQueue

class Node:
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.current = False
        self.distance = float('inf')
        self.previous = None

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, name):
        self.nodes[name] = Node(name)

    def add_edge(self, start, end, weight):
        if start not in self.edges:
            self.edges[start] = {}
        self.edges[start][end] = weight

    def get_graphviz(self, bg_color, box_color, default_color, visited_color, current_color, path_color, zoom_level, path=None):
        dot = Digraph(comment='Dijkstra\'s Algorithm Visualization')
        dot.attr(engine='neato')
        
        width, height = 22 * zoom_level, 17 * zoom_level
        size = f"{width},{height}"
        dot.attr(rankdir='LR', bgcolor=bg_color, size=size, dpi="60")
        
        with dot.subgraph(name='cluster_bg') as c:
            c.attr(style='filled,rounded', color=box_color, fillcolor=box_color, penwidth='2')
            c.attr(label='', fontcolor="#00000000")

        node_size = max(0.3, 0.8 / zoom_level)
        dot.attr('node', shape='circle', style='filled', fontcolor='black', fontname='Arial', 
                 fontsize=str(max(10, int(20 / zoom_level))), width=str(node_size), height=str(node_size), fixedsize='true')
        
        edge_len = max(1.0, 2.0 * zoom_level)
        dot.attr('edge', fontname='Arial', fontsize=str(max(8, int(16 / zoom_level))), len=str(edge_len))

        for name, node in self.nodes.items():
            if path and name in path:
                dot.node(name, name, fillcolor=path_color)
            elif node.visited:
                dot.node(name, name, fillcolor=visited_color)
            elif node.current:
                dot.node(name, name, fillcolor=current_color, penwidth='3')
            else:
                dot.node(name, name, fillcolor=default_color)

        for start, ends in self.edges.items():
            for end, weight in ends.items():
                if path and start in path and end in path and path.index(end) == path.index(start) + 1:
                    dot.edge(start, end, label=str(weight), color=path_color, penwidth='3')
                else:
                    dot.edge(start, end, label=str(weight), color='#A9A9A9', penwidth='2')

        return dot

    def get_mermaid(self, path=None):
        mermaid_code = ["graph LR"]
        for start, ends in self.edges.items():
            for end, weight in ends.items():
                if path and start in path and end in path and path.index(end) == path.index(start) + 1:
                    mermaid_code.append(f"    {start}-->{end}")
                    mermaid_code.append(f"    style {start} fill:#ff0000")
                    mermaid_code.append(f"    style {end} fill:#ff0000")
                else:
                    mermaid_code.append(f"    {start}--{weight}-->{end}")
        return "\n".join(mermaid_code)

    def dijkstra(self, start, end):
        for node in self.nodes.values():
            node.distance = float('inf')
            node.previous = None
            node.visited = False
            node.current = False

        self.nodes[start].distance = 0
        pq = PriorityQueue()
        pq.put((0, start))

        while not pq.empty():
            current_distance, current_node = pq.get()
            
            if current_node == end:
                break

            if current_distance > self.nodes[current_node].distance:
                continue

            self.nodes[current_node].visited = True

            if current_node in self.edges:
                for neighbor, weight in self.edges[current_node].items():
                    distance = current_distance + weight
                    if distance < self.nodes[neighbor].distance:
                        self.nodes[neighbor].distance = distance
                        self.nodes[neighbor].previous = current_node
                        pq.put((distance, neighbor))

        path = []
        current = end
        while current:
            path.append(current)
            current = self.nodes[current].previous
        path.reverse()

        return path if path[0] == start else []

def create_random_graph(num_nodes, max_weight):
    graph = Graph()
    nodes = [chr(65 + i) for i in range(num_nodes)]
    for node in nodes:
        graph.add_node(node)
    
    for i in range(num_nodes - 1):
        graph.add_edge(nodes[i], nodes[i+1], random.randint(1, max_weight))
    
    for _ in range(num_nodes):
        start = random.choice(nodes)
        end = random.choice(nodes)
        if start != end and end not in graph.edges.get(start, {}):
            graph.add_edge(start, end, random.randint(1, max_weight))
    
    return graph

def main():
    st.title("Interactive Dijkstra's Algorithm Visualization")

    st.sidebar.header("Graph Settings")
    num_nodes = st.sidebar.slider("Number of Nodes", 3, 10, 6)
    max_weight = st.sidebar.slider("Maximum Edge Weight", 1, 10, 5)
    zoom_level = st.sidebar.slider("Zoom Level", 0.5, 3.0, 1.0, 0.1)

    st.sidebar.header("Color Settings")
    bg_color = st.sidebar.color_picker("Background Color", "#FFFFFF")
    box_color = st.sidebar.color_picker("Box Color", "#E0E0E0")
    default_color = st.sidebar.color_picker("Unvisited Node Color", "#e6f3ff")
    visited_color = st.sidebar.color_picker("Visited Node Color", "#b3d9ff")
    current_color = st.sidebar.color_picker("Current Node Color", "#80bfff")
    path_color = st.sidebar.color_picker("Shortest Path Color", "#FF6347")

    if 'graph' not in st.session_state:
        st.session_state.graph = create_random_graph(num_nodes, max_weight)

    if st.sidebar.button("Generate New Graph"):
        st.session_state.graph = create_random_graph(num_nodes, max_weight)

    graph = st.session_state.graph
    nodes = list(graph.nodes.keys())

    st.sidebar.header("Dijkstra's Algorithm")
    start_node = st.sidebar.selectbox("Start Node", nodes)
    end_node = st.sidebar.selectbox("End Node", nodes)

    if st.sidebar.button("Find Shortest Path"):
        path = graph.dijkstra(start_node, end_node)
        st.session_state.path = path
        if path:
            st.sidebar.success(f"Shortest path: {' -> '.join(path)}")
        else:
            st.sidebar.error("No path found!")
    else:
        st.session_state.path = []

    dot = graph.get_graphviz(bg_color, box_color, default_color, visited_color, current_color, path_color, zoom_level, st.session_state.path)

    png_data = dot.pipe(format='png')
    st.image(png_data, caption="Dijkstra's Algorithm Graph", use_column_width=True)

    st.download_button(
        label="Download Graph as PNG",
        data=png_data,
        file_name="dijkstra_graph.png",
        mime="image/png"
    )

    tab1, tab2 = st.tabs(["Graphviz DOT", "Mermaid"])

    with tab1:
        st.subheader("Graphviz DOT Code")
        st.code(dot.source)

    with tab2:
        st.subheader("Mermaid Graph")
        mermaid_code = graph.get_mermaid(st.session_state.path)
        st.code(mermaid_code, language="mermaid")

if __name__ == "__main__":
    main()
