import streamlit as st
import random

def generate_random_list(size):
    return [random.randint(1, 100) for _ in range(size)]

def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr.copy(), (i, min_idx)
        elif all(arr[k] <= arr[k+1] for k in range(len(arr)-1)):
            break

st.set_page_config(layout="wide")
st.title("Selection Sort Visualization")

# Sidebar for user input
st.sidebar.header("Settings")
size = st.sidebar.slider("Select list size", min_value=2, max_value=50, value=32)
highlight_color = st.sidebar.color_picker("Choose highlight color", "#FFFF00")
text_color = st.sidebar.color_picker("Choose text color for highlighted boxes", "#000000")

# Generate random list
if 'numbers' not in st.session_state or st.sidebar.button("Generate New List"):
    st.session_state.numbers = generate_random_list(size)

# Function to display list in a grid
def display_list(arr, step_num=None, swapped_indices=None):
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
        .swapped {{
            background-color: {highlight_color};
            color: {text_color};
        }}
    </style>
    <div class="number-grid">
    """
    
    for i, num in enumerate(arr):
        class_name = "number-box swapped" if swapped_indices and i in swapped_indices else "number-box"
        grid_html += f'<div class="{class_name}">{num}</div>'
    
    grid_html += "</div>"
    
    st.markdown(grid_html, unsafe_allow_html=True)
    
    if step_num is not None:
        st.write(f"Step {step_num}")
    st.write("")  # Add some space between steps

# Display original list
st.subheader("Original List")
display_list(st.session_state.numbers)

# Sorting visualization
if st.button("Start Sorting"):
    sorting_steps = list(selection_sort(st.session_state.numbers.copy()))
    
    st.subheader("Sorting Steps")
    for i, (step, swapped) in enumerate(sorting_steps):
        display_list(step, i+1, swapped)
    
    if not sorting_steps:
        st.write("The list was already sorted!")
    else:
        st.write(f"Sorting completed in {len(sorting_steps)} steps.")
    
# Display final sorted list
st.subheader("Final Sorted List")
display_list(sorted(st.session_state.numbers))