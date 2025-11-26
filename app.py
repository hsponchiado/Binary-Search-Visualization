import gradio as gr

# -------------------------------
# Helper Function: Check if sorted
# -------------------------------
def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


# ---------------------------------------------------------
# Visualization Helper: Create HTML boxes for each element
# ---------------------------------------------------------
def visualize_array(arr, left, right, mid):
    """
    Returns an HTML string that visually displays the array.
    This function builds HTML <span> boxes with inline CSS.

    - Orange box = middle index
    - Blue box   = active search range (low..right)
    - Grey box   = excluded elements
    """

    html_parts = []

    for i, val in enumerate(arr):

        # ---------------------------------------------
        # HTML BOX FOR MIDDLE ELEMENT
        # <span> creates a small box with inline CSS.
        # - display:inline-block → makes it behave like a box
        # - width/height → sets size
        # - background-color:#FFA500 → orange color
        # - line-height:40px → vertically centers text
        # - font-weight:bold → makes number bold
        # ---------------------------------------------
        if i == mid:
            html_parts.append(
                f'<span style="display:inline-block; width:40px; height:40px; line-height:40px; '
                f'text-align:center; background-color:#FFA500; color:white; margin:2px; '
                f'border-radius:4px; font-weight:bold;">{val}</span>'
            )

        # -----------------------------------------------------
        # HTML BOX FOR ACTIVE SEARCH RANGE (left → right)
        # - Light blue color (#ADD8E6)
        # - Same styling as above but without bold or orange
        # -----------------------------------------------------
        elif left<= i <= right:
            html_parts.append(
                f'<span style="display:inline-block; width:40px; height:40px; line-height:40px; '
                f'text-align:center; background-color:#ADD8E6; color:black; margin:2px; '
                f'border-radius:4px;">{val}</span>'
            )

        # -------------------------------------------------------
        # HTML BOX FOR EXCLUDED ELEMENTS
        # - Grey color (#E0E0E0)
        # - Slightly faded text (#888)
        # -------------------------------------------------------
        else:
            html_parts.append(
                f'<span style="display:inline-block; width:40px; height:40px; line-height:40px; '
                f'text-align:center; background-color:#E0E0E0; color:#888; margin:2px; '
                f'border-radius:4px;">{val}</span>'
            )

    # Join all HTML <span> boxes together into one string
    return "".join(html_parts)


# --------------------------------------------------
# Binary Search Logic + Step by Step Visualization
# --------------------------------------------------
def binary_search_visualizer(array_str: str, target_str: str):

    # Input validation
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

    if not is_sorted(arr):
        return "Error: The input list must be sorted in ascending order.", "", "", ""

    # Binary search setup
    left= 0
    right = len(arr) - 1
    steps_html = []     # Stores HTML for each visualization frame
    found = False
    found_index = -1
    comparisons = 0
    step_num = 1

    # Binary search loop
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1

        # HTML visual representation of current step
        viz_html = visualize_array(arr, low, right, mid)

        # ----------------------------------------------------------------------------
        # This block creates a styled HTML <div> containing:
        # - Step number
        # - Explanation text
        # - The array visualization HTML
        #
        # <div> is used because:
        # - Makes each step look like a separate card
        #
        # border-left:3px solid #4CAF50 → Green line that is simply used for decoration
        # ----------------------------------------------------------------------------
        step_html = f"""
        <div style="margin-bottom:20px; padding:10px; border-left:3px solid #4CAF50;">
            <strong>Step {step_num}:</strong> Checking index {mid} → value {arr[mid]}<br>
            Target = {target} → { "Found!" if arr[mid] == target else "Too small → search right" if arr[mid] < target else "Too large → search left" }
            
            <!-- Insert the HTML boxes created for this step -->
            <div style="margin-top:10px;">{viz_html}</div>
        </div>
        """

        steps_html.append(step_html)

        # Binary search logic
        if arr[mid] == target:
            found = True
            found_index = mid
            break
        elif arr[mid] < target:
            left= mid + 1
        else:
            right = mid - 1

        step_num += 1

    # Final result message
    result_msg = (
        f"✅ Target {target} found at index {found_index}."
        if found else
        f"❌ Target {target} not found in the list."
    )

    # --------------------------------------------------------------
    # FINAL VISUALIZATION
    # Using same HTML <span> boxes but rightlighting the final target
    # --------------------------------------------------------------
    final_viz = (
        visualize_array(arr, -1, -1, found_index) if found
        else visualize_array(arr, 0, -1, -1)
    )

    # --------------------------------------------------------------
    # HTML wrapper <div> to center the final visualization
    # --------------------------------------------------------------
    final_display = f'<div style="text-align:center; margin-top:10px;">{final_viz}</div>'

    return result_msg, final_display, "".join(steps_html), str(comparisons)


# --------------------------
# Gradio Interface
# --------------------------
with gr.Blocks(title="Binary Search Visualizer") as demo:

    gr.Markdown("# 🔍 Binary Search Visualizer")
    gr.Markdown("Enter a sorted **list of integers, separated by commas**, and see binary search visualized!")

    with gr.Row():
        array_input = gr.Textbox(label="Sorted List (comma-separated)", placeholder="e.g., 1,3,5,7,9,11,13,15")
        target_input = gr.Textbox(label="Target Value", placeholder="e.g., 7")

    run_btn = gr.Button("🔍 Run Binary Search")

    result_output = gr.Textbox(label="Result", interactive=False)
    comparisons_output = gr.Textbox(label="Number of Comparisons", interactive=False)
    final_array_display = gr.HTML(label="Final Array State")       
    steps_display = gr.HTML(label="Step-by-Step Visualization")  

    run_btn.click(
        fn=binary_search_visualizer,
        inputs=[array_input, target_input],
        outputs=[result_output, final_array_display, steps_display, comparisons_output]
    )

    # Color legend (HTML elements explaining colors)
    gr.Markdown("""
    ### 🎨 Color Legend
    - <span style="display:inline-block; width:20px; height:20px; background-color:#FFA500;"></span> Middle element  
    - <span style="display:inline-block; width:20px; height:20px; background-color:#ADD8E6;"></span> Active search range  
    - <span style="display:inline-block; width:20px; height:20px; background-color:#E0E0E0;"></span> Excluded  
    """)

if __name__ == "__main__":
    demo.launch()
