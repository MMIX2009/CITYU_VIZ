import streamlit as st
import random

def generate_sorted_list(size):
    return sorted(random.sample(range(1, 101), size))

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        yield arr, left, mid, right
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

st.set_page_config(layout="wide")
st.title("Binary Search Visualization")

# Sidebar for user input
st.sidebar.header("Settings")
size = st.sidebar.slider("Select list size", min_value=10, max_value=50, value=20)
target = st.sidebar.number_input("Enter target number", min_value=1, max_value=100, value=50)
highlight_color = st.sidebar.color_picker("Choose highlight color", "#00FF00")
text_color = st.sidebar.color_picker("Choose text color for highlighted boxes", "#000000")
show_initial_mid = st.sidebar.checkbox("Show initial middle element", value=True)

# Generate sorted list
if 'numbers' not in st.session_state or st.sidebar.button("Generate New List"):
    st.session_state.numbers = generate_sorted_list(size)

# Function to display list with highlighted section
def display_list(arr, left, mid, right, step_num=None, show_mid=True):
    max_cols = 25  # Maximum number of columns before wrapping
    num_cols = min(len(arr), max_cols)
    
    grid_html = f"""
    <style>
        .number-grid {{
            display: grid;
            grid-template-columns: repeat({num_cols}, 1fr);
            gap: 5px;
        }}
        .number-box {{
            border: 1px solid black;
            padding: 5px;
            text-align: center;
            font-size: 0.8em;
        }}
        .highlighted {{
            background-color: {highlight_color};
            color: {text_color};
        }}
        .mid {{
            border: 2px solid red;
        }}
    </style>
    <div class="number-grid">
    """
    
    for i, num in enumerate(arr):
        class_name = "number-box"
        if left <= i <= right:
            class_name += " highlighted"
        if show_mid and i == mid:
            class_name += " mid"
        grid_html += f'<div class="{class_name}">{num}</div>'
    
    grid_html += "</div>"
    
    st.markdown(grid_html, unsafe_allow_html=True)
    
    if step_num is not None:
        st.write(f"Step {step_num}: Searching between index {left} and {right}. Middle index: {mid}")
    st.write("")  # Add some space between steps

# Display original list
st.subheader("Original Sorted List")
initial_mid = len(st.session_state.numbers) // 2 if show_initial_mid else -1
display_list(st.session_state.numbers, 0, initial_mid, len(st.session_state.numbers)-1, show_mid=show_initial_mid)

# Binary search visualization
if st.button("Start Binary Search"):
    search_steps = list(binary_search(st.session_state.numbers, target))
    
    st.subheader(f"Binary Search Steps (Searching for {target})")
    for i, (arr, left, mid, right) in enumerate(search_steps):
        display_list(arr, left, mid, right, i+1)
    
    if search_steps:
        last_step = search_steps[-1]
        if st.session_state.numbers[last_step[2]] == target:
            st.write(f"Target {target} found at index {last_step[2]}")
        else:
            st.write(f"Target {target} not found in the list")
    else:
        st.write(f"Target {target} not found in the list")
    
    st.write(f"Search completed in {len(search_steps)} steps.")

# Display final result
st.subheader("Final Result")
result = binary_search(st.session_state.numbers, target)
final_result = next(result)
if st.session_state.numbers[final_result[2]] == target:
    st.write(f"Target {target} found at index {final_result[2]}")
else:
    st.write(f"Target {target} not found in the list")