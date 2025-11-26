import gradio as gr

# -------------------------------
# Helper Function: Check if sorted
# -------------------------------
def is_sorted(arr):
    # Returns True only if every element is ≤ the next element
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


# ---------------------------------------------------------
# Visualization Helper: Create HTML boxes for each element
# ---------------------------------------------------------
def visualize_array(arr, left, right, mid):
    """
    Returns an HTML string that visually displays the array.
    - Mid index → orange box
    - Active search range (left to right) → light blue
    - Everything else → grey (excluded)
    """
    html_parts = []

    for i, val in enumerate(arr):

        # Highlight the mid element (currently being checked)
        if i == mid:
            html_parts.append(
                f'<span style="display:inline-block; width:40px; height:40px; line-height:40px; '
                f'text-align:center; background-color:#FFA500; color:white; margin:2px; '
                f'border-radius:4px; font-weight:bold;">{val}</span>'
            )

        # Highlight active search range (left ≤ i ≤ high)
        elif left <= i <= right:
            html_parts.append(
                f'<span style="display:inline-block; width:40px; height:40px; line-height:40px; '
                f'text-align:center; background-color:#ADD8E6; color:black; margin:2px; '
                f'border-radius:4px;">{val}</span>'
            )

        # Grey for excluded values
        else:
            html_parts.append(
                f'<span style="display:inline-block; width:40px; height:40px; line-height:40px; '
                f'text-align:center; background-color:#E0E0E0; color:#888; margin:2px; '
                f'border-radius:4px;">{val}</span>'
            )

    return "".join(html_parts)


# --------------------------------------------------
# Binary Search Logic + Step-by-Step Visualization
# --------------------------------------------------
def binary_search_visualizer(array_str: str, target_str: str):

    # --------------------
    # Validation checks
    # --------------------
    if not array_str.strip():
        return "Error: Please enter a list of numbers.", "", "", ""

    if not target_str.strip():
        return "Error: Please enter a target value.", "", "", ""

    # Convert input strings to integers
    try:
        target = int(target_str)
        arr = [int(x.strip()) for x in array_str.split(",")]
    except ValueError:
        return "Error: All inputs must be integers.", "", "", ""

    if len(arr) == 0:
        return "Error: Array cannot be empty.", "", "", ""

    # Binary Search requires a sorted list
    if not is_sorted(arr):
        return "Error: The input list must be sorted in ascending order.", "", "", ""

    # --------------------------
    # Binary Search Setup
    # --------------------------
    left = 0
    right = len(arr) - 1
    steps_html = []          # Store visualization for each step
    found = False
    found_index = -1
    comparisons = 0          # Count how many comparisons were made
    step_num = 1

    # --------------------------
    # Binary Search Loop
    # --------------------------
    while left <= right:

        mid = (left + right) // 2
        comparisons += 1  # Every check of arr[mid] counts as a comparison

        # Build HTML for current step visualization
        viz_html = visualize_array(arr, left, right, mid)

        # Describe what is happening at this step
        step_html = f"""
        <div style="margin-bottom:20px; padding:10px; border-left:3px solid #4CAF50;">
            <strong>Step {step_num}:</strong> Checking index {mid} → value {arr[mid]}<br>
            Target = {target} → {
                "Found!" if arr[mid] == target
                else "Too small → search right" if arr[mid] < target
                else "Too large → search left"
            }
            <div style="margin-top:10px;">{viz_html}</div>
        </div>
        """

        steps_html.append(step_html)

        # --------------------------
        # Binary Search Decisions
        # --------------------------
        if arr[mid] == target:
            found = True
            found_index = mid
            break

        elif arr[mid] < target:
            left = mid + 1  # Move right

        else:
            right = mid - 1  # Move left

        step_num += 1

    # --------------------------
    # Final Result Message
    # --------------------------
    if found:
        result_msg = f"✅ Target {target} found at index {found_index}."
    else:
        result_msg = f"❌ Target {target} not found in the list."

    # Final visual display (highlight the found element)
    final_viz = (
        visualize_array(arr, -1, -1, found_index) if found
        else visualize_array(arr, 0, -1, -1)
    )

    final_display = f'<div style="text-align:center; margin-top:10px;">{final_viz}</div>'
    comparisons_msg = str(comparisons)  # Display comparison count

    # Return final output for Gradio
    return result_msg, final_display, "".join(steps_html), comparisons_msg


# --------------------------
# Gradio Interface
# --------------------------
with gr.Blocks(title="Binary Search Visualizer") as demo:

    # Title + instructions
    gr.Markdown("# 🔍 Binary Search Visualizer")
    gr.Markdown(
        "Enter a **sorted list of integers** and a **target** to see binary search performed step-by-step."
    )

    # Inputs
    with gr.Row():
        array_input = gr.Textbox(
            label="Sorted List (comma-separated)",
            value="1,3,5,7,9,11,13,15",
            placeholder="e.g., 1,2,3,4,5"
        )
        target_input = gr.Textbox(
            label="Target Value",
            value="7",
            placeholder="e.g., 3"
        )

    run_btn = gr.Button("🔍 Run Binary Search")

    # Outputs
    result_output = gr.Textbox(label="Result", interactive=False)
    comparisons_output = gr.Textbox(label="Number of Comparisons", interactive=False)
    final_array_display = gr.HTML(label="Final Array State")
    steps_display = gr.HTML(label="Step-by-Step Visualization")

    # Button behavior
    run_btn.click(
        fn=binary_search_visualizer,
        inputs=[array_input, target_input],
        outputs=[result_output, final_array_display, steps_display, comparisons_output]
    )

    # Color Legend
    gr.Markdown("""
    ### 🎨 Color Legend
    - <span style="display:inline-block; width:20px; height:20px; background-color:#FFA500;"></span> **Current middle element**
    - <span style="display:inline-block; width:20px; height:20px; background-color:#ADD8E6;"></span> **Active search range**
    - <span style="display:inline-block; width:20px; height:20px; background-color:#E0E0E0;"></span> **Excluded elements**

    💡 **Each check of the middle element counts as one comparison.**
    """)

# Run app
if __name__ == "__main__":
    demo.launch()

