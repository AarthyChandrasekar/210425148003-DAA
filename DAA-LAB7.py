import streamlit as st
import pandas as pd


# ==========================================
# Check if Queen Can Be Placed
# ==========================================
def is_safe(board, row, col):

    for prev_row in range(row):

        placed = board[prev_row]

        # Same column
        if placed == col:
            return False

        # Same diagonal
        if abs(prev_row - row) == abs(placed - col):
            return False

    return True


# ==========================================
# Solve N-Queens
# ==========================================
def solve_n_queens(n):

    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):

        if row == n:

            solutions.append(board[:])
            return

        for col in range(n):

            if is_safe(board, row, col):

                board[row] = col

                backtrack(row + 1)

                # Undo the move
                board[row] = -1

                backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


# ==========================================
# Display Chess Board
# ==========================================
def display_board(solution, n):

    board_data = []

    for row in range(n):

        row_data = []

        for col in range(n):

            if solution[row] == col:
                row_data.append("♛")
            else:
                row_data.append("·")

        board_data.append(row_data)

    df = pd.DataFrame(
        board_data,
        index=[f"Row {i + 1}" for i in range(n)],
        columns=[f"Col {i + 1}" for i in range(n)]
    )

    st.table(df)


# ==========================================
# Streamlit Configuration
# ==========================================
st.set_page_config(
    page_title="N-Queens Problem",
    page_icon="♛",
    layout="wide"
)


# ==========================================
# Main Page
# ==========================================
st.title("♛ N-Queens Problem")

st.write(
    """
    The **N-Queens Problem** places N queens on an N × N
    chessboard such that no two queens attack each other.

    This application solves the problem using **Backtracking**.
    """
)


# ==========================================
# Input
# ==========================================
st.sidebar.header("Configuration")

n = st.sidebar.number_input(
    "Select N",
    min_value=1,
    max_value=10,
    value=4,
    step=1
)


solve_button = st.sidebar.button("Solve N-Queens")


# ==========================================
# Solve
# ==========================================
if solve_button:

    with st.spinner("Finding solutions..."):

        solutions, backtracks = solve_n_queens(n)

    st.session_state["solutions"] = solutions
    st.session_state["backtracks"] = backtracks
    st.session_state["n"] = n


# ==========================================
# Display Results
# ==========================================
if "solutions" in st.session_state:

    solutions = st.session_state["solutions"]
    backtracks = st.session_state["backtracks"]
    n = st.session_state["n"]

    # ======================================
    # Statistics
    # ======================================

    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Board Size",
            f"{n} × {n}"
        )

    with col2:

        st.metric(
            "Number of Solutions",
            len(solutions)
        )

    with col3:

        st.metric(
            "Backtracks",
            backtracks
        )


    # ======================================
    # No Solution
    # ======================================

    if len(solutions) == 0:

        st.error(
            f"No solution exists for {n}-Queens."
        )


    else:

        # ==================================
        # Solution Selection
        # ==================================

        st.subheader("♛ View Solution")

        solution_number = st.selectbox(
            "Select Solution",
            range(1, len(solutions) + 1)
        )

        selected_solution = solutions[
            solution_number - 1
        ]

        st.write(
            f"**Solution {solution_number}:** "
            f"{selected_solution}"
        )

        display_board(
            selected_solution,
            n
        )


        # ==================================
        # All Solutions
        # ==================================

        if n <= 6:

            st.divider()

            st.subheader(
                f"All {len(solutions)} Solutions"
            )

            for i, solution in enumerate(
                solutions, 1
            ):

                st.write(
                    f"### Solution {i}: {solution}"
                )

                display_board(
                    solution,
                    n
                )

        else:

            st.info(
                "For N > 6, use the solution selector "
                "above to view individual solutions. "
                "Displaying every solution may require "
                "a large amount of screen space."
            )


# ==========================================
# Algorithm Explanation
# ==========================================

st.divider()

st.subheader("📚 Algorithm Information")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        **Backtracking Steps:**

        1. Start from the first row.
        2. Try placing a queen in each column.
        3. Check whether the position is safe.
        4. If safe, move to the next row.
        5. If no position works, go back.
        6. Remove the previous queen.
        7. Try another position.
        """
    )

with col2:

    st.markdown(
        """
        **Safety Conditions:**

        A queen cannot share:

        - The same column
        - The same diagonal
        - The same row

        Since we place exactly one queen per row,
        the row condition is automatically satisfied.
        """
    )
