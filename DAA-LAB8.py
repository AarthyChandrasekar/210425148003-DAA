import streamlit as st
import pandas as pd
from itertools import permutations
import math

INF = float("inf")


# ==========================================
# TSP Brute Force
# ==========================================
def tsp_brute_force(cost, n):
    cities = list(range(1, n))

    best_cost = INF
    best_path = None

    for perm in permutations(cities):

        path = [0] + list(perm) + [0]

        total_cost = 0

        for i in range(n):
            total_cost += cost[path[i]][path[i + 1]]

        if total_cost < best_cost:
            best_cost = total_cost
            best_path = path

    return best_path, best_cost


# ==========================================
# Streamlit Configuration
# ==========================================
st.set_page_config(
    page_title="Travelling Salesman Problem",
    page_icon="🚗",
    layout="wide"
)


# ==========================================
# Title
# ==========================================
st.title("🚗 Travelling Salesman Problem (TSP)")

st.write(
    """
    Find the **minimum-cost tour** that visits every city
    exactly once and returns to the starting city.

    This application uses the **Brute Force approach**.
    """
)


# ==========================================
# Number of Cities
# ==========================================
st.sidebar.header("TSP Configuration")

n = st.sidebar.number_input(
    "Number of Cities",
    min_value=2,
    max_value=9,
    value=5,
    step=1
)


# ==========================================
# City Names
# ==========================================
default_cities = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

cities = default_cities[:n]


# ==========================================
# Default Cost Matrix
# ==========================================
default_matrix = [
    [None, 10, 8, 9, 7],
    [10, None, 10, 5, 6],
    [8, 10, None, 8, 9],
    [9, 5, 8, None, 6],
    [7, 6, 9, 6, None]
]


st.subheader("Enter Cost Matrix")

st.write(
    """
    Enter the travel cost between cities.
    Leave the diagonal as `0` because a city does not
    travel to itself.
    """
)


# ==========================================
# Create Input Matrix
# ==========================================
matrix = []

for i in range(n):

    cols = st.columns(n)

    row = []

    for j in range(n):

        if i == j:

            value = cols[j].number_input(
                f"{cities[i]} → {cities[j]}",
                value=0,
                min_value=0,
                key=f"matrix_{i}_{j}",
                disabled=True
            )

        else:

            if n == 5:
                default_value = default_matrix[i][j]
            else:
                default_value = 10

            value = cols[j].number_input(
                f"{cities[i]} → {cities[j]}",
                value=default_value,
                min_value=0,
                key=f"matrix_{i}_{j}"
            )

        row.append(value)

    matrix.append(row)


# ==========================================
# Calculate TSP
# ==========================================
if st.button("🚀 Find Optimal Tour"):

    cost = []

    for i in range(n):

        row = []

        for j in range(n):

            if i == j:
                row.append(INF)
            else:
                row.append(matrix[i][j])

        cost.append(row)


    # ======================================
    # Run Brute Force
    # ======================================

    with st.spinner("Searching for the optimal tour..."):

        best_path, best_cost = tsp_brute_force(
            cost,
            n
        )


    # ======================================
    # Display Cost Matrix
    # ======================================

    st.subheader("📊 Cost Matrix")

    display_matrix = []

    for i in range(n):

        row = []

        for j in range(n):

            if i == j:
                row.append("INF")
            else:
                row.append(matrix[i][j])

        display_matrix.append(row)


    df_matrix = pd.DataFrame(
        display_matrix,
        index=cities,
        columns=cities
    )

    st.dataframe(
        df_matrix,
        use_container_width=True
    )


    # ======================================
    # Results
    # ======================================

    st.subheader("🏆 Optimal Solution")

    col1, col2 = st.columns(2)

    with col1:

        tour = " → ".join(
            cities[i]
            for i in best_path
        )

        st.success("Optimal Tour")

        st.code(tour)


    with col2:

        st.info("Minimum Cost")

        st.metric(
            "Total Cost",
            best_cost
        )


    # ======================================
    # Path Verification
    # ======================================

    st.subheader("🔍 Path Verification")

    verification = []

    for i in range(n):

        u = best_path[i]
        v = best_path[i + 1]

        verification.append({
            "From": cities[u],
            "To": cities[v],
            "Cost": matrix[u][v]
        })


    verification_df = pd.DataFrame(
        verification
    )

    st.dataframe(
        verification_df,
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # Cost Calculation
    # ======================================

    calculation = " + ".join(
        str(matrix[best_path[i]][best_path[i + 1]])
        for i in range(n)
    )

    st.write(
        f"**Total Cost:** {calculation} = **{best_cost}**"
    )


    # ======================================
    # Algorithm Information
    # ======================================

    st.divider()

    st.subheader("📚 Algorithm Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Technique\n\nBrute Force")

    with col2:
        st.info("Time Complexity\n\nO((n − 1)!)")

    with col3:
        st.info("Space Complexity\n\nO(n)")


    st.warning(
        """
        Brute force checks every possible ordering of the cities.
        Therefore, the execution time increases very quickly as
        the number of cities increases.
        """
    )
