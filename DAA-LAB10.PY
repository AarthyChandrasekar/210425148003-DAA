import streamlit as st
import pandas as pd
import random
import time
import sys

sys.setrecursionlimit(20000)


# ==========================================
# Partition
# ==========================================
def partition(arr, low, high, counter):

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):

        counter[0] += 1

        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = (
        arr[high],
        arr[i + 1]
    )

    return i + 1


# ==========================================
# Deterministic QuickSort
# ==========================================
def deterministic_quicksort(
    arr,
    low,
    high,
    counter
):

    if low < high:

        pi = partition(
            arr,
            low,
            high,
            counter
        )

        deterministic_quicksort(
            arr,
            low,
            pi - 1,
            counter
        )

        deterministic_quicksort(
            arr,
            pi + 1,
            high,
            counter
        )


# ==========================================
# Randomized QuickSort
# ==========================================
def randomized_quicksort(
    arr,
    low,
    high,
    counter
):

    if low < high:

        # Select random pivot
        rand_idx = random.randint(
            low,
            high
        )

        arr[rand_idx], arr[high] = (
            arr[high],
            arr[rand_idx]
        )

        pi = partition(
            arr,
            low,
            high,
            counter
        )

        randomized_quicksort(
            arr,
            low,
            pi - 1,
            counter
        )

        randomized_quicksort(
            arr,
            pi + 1,
            high,
            counter
        )


# ==========================================
# Run Test
# ==========================================
def run_test(sort_fn, arr):

    a = arr[:]

    counter = [0]

    start = time.perf_counter()

    sort_fn(
        a,
        0,
        len(a) - 1,
        counter
    )

    elapsed = (
        time.perf_counter() - start
    ) * 1000

    return counter[0], elapsed


# ==========================================
# Generate Test Cases
# ==========================================
def generate_test_cases(n):

    test_cases = {

        "Random":
            [
                random.randint(1, 100000)
                for _ in range(n)
            ],

        "Sorted":
            list(range(n)),

        "Reverse":
            list(range(n, 0, -1)),

        "Nearly Sorted":
            list(range(n))
    }

    # Slightly shuffle Nearly Sorted
    ns = test_cases["Nearly Sorted"]

    for _ in range(max(1, n // 20)):

        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

        ns[i], ns[j] = (
            ns[j],
            ns[i]
        )

    return test_cases


# ==========================================
# Streamlit Configuration
# ==========================================
st.set_page_config(
    page_title="QuickSort Comparison",
    page_icon="⚡",
    layout="wide"
)


# ==========================================
# Title
# ==========================================
st.title(
    "⚡ Deterministic vs Randomized QuickSort"
)

st.write(
    """
    Compare **Deterministic QuickSort (DQS)** and
    **Randomized QuickSort (RQS)** using different
    types of input data.
    """
)


# ==========================================
# Sidebar
# ==========================================
st.sidebar.header("Test Configuration")

n = st.sidebar.number_input(
    "Array Size",
    min_value=10,
    max_value=10000,
    value=5000,
    step=100
)

run_button = st.sidebar.button(
    "🚀 Run Comparison"
)


# ==========================================
# Information
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
        **Deterministic QuickSort**

        Uses the last element as pivot.
        """
    )

with col2:
    st.info(
        """
        **Randomized QuickSort**

        Selects a random pivot.
        """
    )

with col3:
    st.info(
        """
        **Comparison Metric**

        Number of element comparisons.
        """
    )


# ==========================================
# Run Comparison
# ==========================================
if run_button:

    with st.spinner(
        "Running QuickSort comparison..."
    ):

        test_cases = generate_test_cases(n)

        results = []

        for case, arr in test_cases.items():

            # Deterministic QuickSort
            d_comps, d_time = run_test(
                deterministic_quicksort,
                arr
            )

            # Randomized QuickSort
            r_comps, r_time = run_test(
                randomized_quicksort,
                arr
            )

            results.append({

                "Input Type": case,

                "DQS Comparisons":
                    d_comps,

                "DQS Time (ms)":
                    round(d_time, 2),

                "RQS Comparisons":
                    r_comps,

                "RQS Time (ms)":
                    round(r_time, 2)
            })


        df = pd.DataFrame(results)


        # ======================================
        # Results Table
        # ======================================

        st.subheader(
            f"📊 Results for N = {n}"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


        # ======================================
        # Comparison Count Chart
        # ======================================

        st.subheader(
            "🔢 Comparison Count"
        )

        comparison_df = df.set_index(
            "Input Type"
        )[
            [
                "DQS Comparisons",
                "RQS Comparisons"
            ]
        ]

        st.bar_chart(
            comparison_df
        )


        # ======================================
        # Execution Time Chart
        # ======================================

        st.subheader(
            "⏱️ Execution Time"
        )

        time_df = df.set_index(
            "Input Type"
        )[
            [
                "DQS Time (ms)",
                "RQS Time (ms)"
            ]
        ]

        st.bar_chart(
            time_df
        )


        # ======================================
        # Best Results
        # ======================================

        st.subheader(
            "🏆 Comparison Summary"
        )

        col1, col2 = st.columns(2)

        with col1:

            d_total = df[
                "DQS Comparisons"
            ].sum()

            st.metric(
                "Total DQS Comparisons",
                f"{d_total:,}"
            )

        with col2:

            r_total = df[
                "RQS Comparisons"
            ].sum()

            st.metric(
                "Total RQS Comparisons",
                f"{r_total:,}"
            )


        # ======================================
        # Explanation
        # ======================================

        st.divider()

        st.subheader(
            "📚 Algorithm Analysis"
        )

        st.markdown(
            """
            ### Deterministic QuickSort

            The pivot is always selected using a fixed rule
            in this implementation: **the last element**.

            - Average Time: **O(n log n)**
            - Worst Time: **O(n²)**
            - Random input usually performs well.
            - Sorted or reverse-sorted input can cause poor
              performance.

            ### Randomized QuickSort

            The pivot is selected randomly before partitioning.

            - Expected Time: **O(n log n)**
            - Worst Time: **O(n²)**
            - Reduces the chance of consistently getting
              a bad pivot.
            - Usually performs more consistently across
              different input arrangements.
            """
        )


# ==========================================
# Initial Instructions
# ==========================================
else:

    st.info(
        """
        Choose an array size from the sidebar and click
        **Run Comparison** to compare both QuickSort algorithms.
        """
    )
 
