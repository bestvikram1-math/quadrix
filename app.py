import streamlit as st
import time

st.set_page_config(page_title="Quadrix", layout="centered")

# -----------------------------------
# STYLE
# -----------------------------------

st.markdown("""
<style>

input {
    text-align: center;
    font-size: 24px !important;
    font-weight: bold !important;
}

.cell-label {
    text-align: center;
    font-size: 12px;
    color: gray;
}

.block-cell {
    background-color: black;
    height: 70px;
    border-radius: 8px;
}

.highlight-cell {
    background-color: #90EE90;
    height: 10px;
    border-radius: 5px;
    margin-bottom: 5px;
}

.unlocked-cell {
    background-color: #d8f5d0;
    height: 10px;
    border-radius: 5px;
    margin-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("🧠 Quadrix")
st.subheader("Think Before You Calculate")

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "unlocked_cells" not in st.session_state:

    st.session_state.unlocked_cells = [
        "0-0",   # A1
        "2-2",   # C3
        "4-4"    # E5
    ]

if "highlighted_cells" not in st.session_state:

    st.session_state.highlighted_cells = []

if "solved_cells" not in st.session_state:

    st.session_state.solved_cells = []

if "start_time" not in st.session_state:

    st.session_state.start_time = time.time()

if "bonus_message" not in st.session_state:

    st.session_state.bonus_message = ""

unlocked_cells = st.session_state.unlocked_cells

# -----------------------------------
# HELPER FUNCTION
# -----------------------------------

def cell_name(cell_key):

    row, col = cell_key.split("-")

    rows = ["A", "B", "C", "D", "E"]

    return f"{rows[int(row)]}{int(col)+1}"

# -----------------------------------
# GRID STRUCTURE
# -----------------------------------

grid = [
    ["", "", "■", "", ""],
    ["", "■", "", "■", ""],
    ["", "", "", "", ""],
    ["", "■", "", "■", ""],
    ["", "", "■", "", ""]
]

rows = ["A", "B", "C", "D", "E"]

# -----------------------------------
# ANSWERS
# -----------------------------------

answers = {
    "0-0": "1",
    "1-2": "0",
    "2-0": "0",
    "2-2": "-6",
    "3-4": "non-real",
    "4-4": "-1"
}

# -----------------------------------
# HINTS
# -----------------------------------

hints = {
    "0-0": "Hint: What happens if a+b+c=0 ?",
    "1-2": "Hint: Calculate b²−4ac",
    "2-0": "Hint: Equal roots imply something about discriminant",
    "2-2": "Hint: Product of roots = c/a",
    "3-4": "Hint: What happens when D < 0 ?",
    "4-4": "Hint: What if a-b+c=0 ?"
}

# -----------------------------------
# UNLOCK MAP
# -----------------------------------

unlock_map = {
    "0-0": ["1-2"],
    "1-2": ["2-0"],
    "2-2": ["3-4"]
}

# -----------------------------------
# CLUES DATABASE
# -----------------------------------

clues = {

    "0-0": "If a+b+c=0, one root is ?",

    "1-2": "Discriminant of x²−2x+1 ?",

    "2-0": "If roots are equal, discriminant is ?",

    "2-2": "Roots are 2 and -3. Product of roots?",

    "3-4": "If D < 0, roots are real or non-real?",

    "4-4": "If a-b+c=0, one root is ?"
}

# -----------------------------------
# BONUS MESSAGE
# -----------------------------------

if st.session_state.bonus_message != "":

    st.success(st.session_state.bonus_message)

# -----------------------------------
# DISPLAY GRID
# -----------------------------------

st.write("## Quadratic Intelligence Grid")

user_inputs = {}

for i in range(5):

    cols = st.columns(5)

    for j in range(5):

        cell = f"{i}-{j}"

        cell_label = f"{rows[i]}{j+1}"

        if grid[i][j] == "■":

            cols[j].markdown(
                """
                <div class="block-cell"></div>
                """,
                unsafe_allow_html=True
            )

        else:

            cols[j].markdown(
                f"<div class='cell-label'>{cell_label}</div>",
                unsafe_allow_html=True
            )

            # Newly unlocked cells
            if cell in st.session_state.highlighted_cells:

                cols[j].markdown(
                    """
                    <div class="highlight-cell"></div>
                    """,
                    unsafe_allow_html=True
                )

            # Previously unlocked cells
            elif cell in unlocked_cells:

                cols[j].markdown(
                    """
                    <div class="unlocked-cell"></div>
                    """,
                    unsafe_allow_html=True
                )

            disabled_state = cell not in unlocked_cells

            value = cols[j].text_input(
                label=cell_label,
                value="",
                key=cell,
                disabled=disabled_state,
                label_visibility="collapsed"
            )

            user_inputs[cell] = value

# -----------------------------------
# AUTO VALIDATION
# -----------------------------------

for key, correct_answer in answers.items():

    if key in user_inputs:

        entered_value = user_inputs[key]

        # Correct answer
        if entered_value == correct_answer:

            if key not in st.session_state.solved_cells:

                st.session_state.solved_cells.append(key)

                # Insight bonus
                solve_time = time.time() - st.session_state.start_time

                if solve_time < 5:

                    st.session_state.bonus_message = (
                        "⚡ Insight Bonus +20 | Fast Pattern Recognition!"
                    )

                # Unlock connected cells
                if key in unlock_map:

                    for new_cell in unlock_map[key]:

                        if new_cell not in unlocked_cells:

                            unlocked_cells.append(new_cell)

                            st.session_state.highlighted_cells.append(new_cell)

                            st.rerun()

        # Wrong answer feedback
        elif entered_value != "":

            st.warning(
                f"{cell_name(key)}: {hints[key]}"
            )

# -----------------------------------
# DISPLAY ACTIVE CLUES
# -----------------------------------

st.write("---")

st.write("# Active Clues")

for cell in unlocked_cells:

    if cell in clues:

        st.markdown(
            f"""
### {cell_name(cell)}

{clues[cell]}
"""
        )