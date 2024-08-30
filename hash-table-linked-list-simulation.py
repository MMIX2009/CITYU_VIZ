import streamlit as st
import random
import string
from graphviz import Digraph

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return sum(ord(char) for char in key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while current.next:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            if current.key == key:
                current.value = value
            else:
                current.next = Node(key, value)

    def get(self, key):
        index = self.hash_function(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        index = self.hash_function(key)
        if self.table[index] is None:
            return

        if self.table[index].key == key:
            self.table[index] = self.table[index].next
            return

        current = self.table[index]
        while current.next:
            if current.next.key == key:
                current.next = current.next.next
                return
            current = current.next

def visualize_hash_table(hash_table, highlight_index=None, highlight_key=None):
    dot = Digraph(comment='Hash Table with Linked Lists')
    dot.attr(rankdir='LR')
    
    # Create a node for the hash table
    dot.node('hash_table', 'Hash Table', shape='record', label='{{0|1|2|3|4|5|6|7|8|9}}')
    
    # Create nodes for each bucket and its linked list
    for i in range(hash_table.size):
        bucket_name = f'bucket_{i}'
        if hash_table.table[i] is None:
            dot.node(bucket_name, 'None')
        else:
            current = hash_table.table[i]
            prev_node = None
            while current:
                node_name = f'{bucket_name}_{current.key}'
                node_color = 'lightblue' if i == highlight_index and current.key == highlight_key else 'white'
                dot.node(node_name, f'{current.key}: {current.value}', style='filled', fillcolor=node_color)
                if prev_node:
                    dot.edge(prev_node, node_name)
                else:
                    dot.edge(bucket_name, node_name)
                prev_node = node_name
                current = current.next
        
        # Connect hash table to bucket
        dot.edge(f'hash_table:{i}', bucket_name)
    
    return dot

def generate_random_key_value():
    key = ''.join(random.choices(string.ascii_lowercase, k=3))
    value = random.randint(1, 100)
    return key, value

def main():
    st.title("Hash Table with Linked Lists Simulation")

    # Sidebar for hash table size
    table_size = st.sidebar.slider("Hash Table Size", min_value=5, max_value=15, value=10)

    # Initialize or update hash table
    if 'hash_table' not in st.session_state or st.session_state.hash_table.size != table_size:
        st.session_state.hash_table = HashTable(table_size)

    # Operations
    operation = st.radio("Select Operation", ["Insert", "Get", "Delete"])

    if operation == "Insert":
        key, value = generate_random_key_value()
        key = st.text_input("Enter key (or use generated)", value=key)
        value = st.number_input("Enter value (or use generated)", value=value)
        if st.button("Insert"):
            st.session_state.hash_table.insert(key, value)
            st.success(f"Inserted key '{key}' with value '{value}'")
            highlight_index = st.session_state.hash_table.hash_function(key)
            dot = visualize_hash_table(st.session_state.hash_table, highlight_index, key)
            st.graphviz_chart(dot)

    elif operation == "Get":
        key = st.text_input("Enter key to retrieve")
        if st.button("Get"):
            value = st.session_state.hash_table.get(key)
            if value is not None:
                st.success(f"Value for key '{key}': {value}")
                highlight_index = st.session_state.hash_table.hash_function(key)
                dot = visualize_hash_table(st.session_state.hash_table, highlight_index, key)
                st.graphviz_chart(dot)
            else:
                st.error(f"Key '{key}' not found")
                dot = visualize_hash_table(st.session_state.hash_table)
                st.graphviz_chart(dot)

    elif operation == "Delete":
        key = st.text_input("Enter key to delete")
        if st.button("Delete"):
            highlight_index = st.session_state.hash_table.hash_function(key)
            st.session_state.hash_table.delete(key)
            st.success(f"Deleted key '{key}'")
            dot = visualize_hash_table(st.session_state.hash_table, highlight_index)
            st.graphviz_chart(dot)

    # Visualize current state
    if st.button("Visualize Current State"):
        dot = visualize_hash_table(st.session_state.hash_table)
        st.graphviz_chart(dot)

if __name__ == "__main__":
    main()
