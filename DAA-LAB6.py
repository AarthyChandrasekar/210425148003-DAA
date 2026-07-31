import streamlit as st
import pandas as pd


# ==========================================
# Matrix Chain Multiplication using DP
# ==========================================
def matrix_chain_order(dims):
    """
    Matrix Chain Multiplication using Dynamic Programming.

    dims = [p0, p1, p2, ..., pn]

    Matrix Ai has dimension:
    dims[i-1] x dims[i]

    Time Complexity: O(n^3)
    Space Complexity: O(n^2)
    """

    n = len(dims) - 1

    # m[i][j] = minimum multiplication cost
    m = [[0] * (n + 1) for _ in range(n + 1)]

    # s[i][j] = optimal splitting position
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # Chain length
    for length in range(2, n + 1):

        for i in range(1, n - length + 2):

            j = i + length - 1

            m[i][j] = float("inf")

            for k in range(i, j):

                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:

                    m[i][j] = cost
                    s[i][j] = k

    return m, s


# ==========================================
# Optimal Parenthesization
# ==========================================
def print_optimal_parens(s, i, j):

    if i == j:
        return f"A{i}"

    k = s[i][j]

    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)

    return f"({left} × {right})"


# ==========================================
# Create DP Table
# ==========================================
def create_dp_table(m, n):

    data = []

    for i in range(1, n + 1):

        row = []

        for j in range(1, n + 1):

            if j < i:
                row.append("---")
            else:
                row.append(m[i][j])

        data.append(row)

    columns = [f"A{j}" for j in range(1, n + 1)]
    index = [f"A{i}" for i in range(1, n + 1)]

    return pd.DataFrame(
        data,
        index=index,
        columns=columns
    )


# ==========================================
# Streamlit Page
# ==========================================
st.set_page_config(
    page_title="Matrix Chain Multiplication",
    page_icon="🔢",
    layout="wide"
)

st.title("🔢 Matrix Chain Multiplication")

st.write(
    """
    **Matrix Chain Multiplication using Dynamic Programming**

    Find the minimum number of scalar multiplications required
    to multiply a sequence of matrices.
    """
)


# ==========================================
# Input
# ==========================================
st.subheader("Enter Matrix Dimensions")

st.write(
    """
    Enter dimensions separated by commas.

    Example:
    `10,30,5,60,10`
    """
)

dims_input = st.text_input(
    "Dimensions",
    value="10,30,5,60,10"
)


# ==========================================
# Calculate
# ==========================================
if st.button("Calculate"):

    try:

        dims = [
            int(x.strip())
            for x in dims_input.split(",")
        ]

        # Validation
        if len(dims) < 2:

            st.error(
                "Enter at least 2 dimensions."
            )

        elif any(x <= 0 for x in dims):

            st.error(
                "All dimensions must be positive."
            )

        else:

            n = len(dims) - 1

            # Run DP
            m, s = matrix_chain_order(dims)

            # ==================================
            # Matrix Dimensions
            # ==================================
            st.subheader("Matrix Dimensions")

            matrix_data = []

            for i in range(n):

                matrix_data.append({
                    "Matrix": f"A{i + 1}",
                    "Rows": dims[i],
                    "Columns": dims[i + 1],
                    "Dimension":
                        f"{dims[i]} × {dims[i + 1]}"
                })

            st.dataframe(
                pd.DataFrame(matrix_data),
                use_container_width=True,
                hide_index=True
            )


            # ==================================
            # Results
            # ==================================
            st.subheader("Results")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Minimum Scalar Multiplications",
                    f"{m[1][n]:,}"
                )

            with col2:

                optimal = print_optimal_parens(
                    s, 1, n
                )

                st.write("**Optimal Parenthesization**")

                st.code(optimal)


            # ==================================
            # DP Cost Table
            # ==================================
            st.subheader("DP Cost Table")

            st.write(
                """
                `m[i][j]` represents the minimum number
                of scalar multiplications needed to
                multiply matrices Ai through Aj.
                """
            )

            dp_table = create_dp_table(m, n)

            st.dataframe(
                dp_table,
                use_container_width=True
            )


            # ==================================
            # Split Table
            # ==================================
            st.subheader("Optimal Split Table")

            split_data = []

            for i in range(1, n + 1):

                row = []

                for j in range(1, n + 1):

                    if j <= i:

                        row.append("---")

                    else:

                        row.append(
                            f"k = {s[i][j]}"
                        )

                split_data.append(row)

            split_table = pd.DataFrame(
                split_data,
                index=[
                    f"A{i}"
                    for i in range(1, n + 1)
                ],
                columns=[
                    f"A{j}"
                    for j in range(1, n + 1)
                ]
            )

            st.dataframe(
                split_table,
                use_container_width=True
            )


# ==========================================
# Explanation
# ==========================================
st.divider()

st.subheader("📚 Algorithm Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Time Complexity: O(n³)")

with col2:
    st.info("Space Complexity: O(n²)")

with col3:
    st.info("Technique: Dynamic Programming")
