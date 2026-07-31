import streamlit as st
import pandas as pd
import random
import time
import sys

sys.setrecursionlimit(20000)


# ============================================================
# Global comparison counter
# ============================================================
comparisons = 0


# ============================================================
# Partition
# ============================================================
def partition(arr, low, high):

    global comparisons

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):

        comparisons += 1

        if arr[j] <= pivot:

            i += 1

            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


# ============================================================
# Deterministic QuickSort
# ============================================================
def deterministic_quicksort(arr, low, high):

    if low < high:

        pi = partition(
            arr,
            low,
            high
        )

        deterministic_quicksort(
            arr,
            low,
            pi - 1
        )

        deterministic_quicksort(
            arr,
            pi + 1,
            high
        )


# ============================================================
# Randomized QuickSort
# ============================================================
def randomized_quicksort(arr, low, high):

    if low < high:

        # Choose a random pivot
        rand_idx = random.randint(
            low,
            high
        )

        # Move random pivot to the end
        arr[rand_idx], arr[high] = (
            arr[high],
            arr[rand_idx]
        )

        pi = partition(
            arr,
            low,
            high
        )

        randomized_quicksort(
            arr,
            low,
            pi - 1
        )

        randomized_quicksort(
            arr,
            pi + 1,
            high
        )


# ============================================================
# Run Test
# ============================================================
def run_test(sort_fn, arr):

    global comparisons

    # Copy original array
    a = arr[:]

    # Reset comparison counter
    comparisons = 0

    # Start timer
    start = time.perf_counter()

    # Run sorting algorithm
    sort_fn(
        a,
        0,
        len(a) - 1
    )

    # End timer
    elapsed = (
        time.perf_counter() - start
    ) * 1000

    return comparisons, elapsed, a


# ============================================================
# Generate Test Cases
# ============================================================
def generate_test_cases(n):

    test_cases = {

        "Random": [
            random.randint(1, 100000)
            for _ in range(n)
        ],

        "Sorted": list(range(n)),

        "Reverse": list(
            range(n, 0, -1)
        ),

        "Nearly Sorted": list(
            range(n)
        )
    }

    # Slightly shuffle Nearly Sorted array
    ns = test_cases["Nearly Sorted"]

    shuffle_count = max(1, n // 20)

    for _ in range(shuffle_count):

        i = random.randint(
            0,
            n - 1
        )

        j = random.randint(
            0,
            n - 1
        )

        ns[i], ns[j] = (
            ns[j],
            ns[i]
        )

    return test_cases


# ============================================================
# Streamlit Configuration
# ============================================================
st.set_page_config(
    page_title="QuickSort Comparison",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# Title
# ============================================================
st.title(
    "⚡ Deterministic vs Randomized QuickSort"
)

st.write(
    """
    Compare the performance of **Deterministic QuickSort**
    and **Randomized QuickSort** using different input types.
    """
)


# ============================================================
# Algorithm Information
# ============================================================
st.subheader("📚 Algorithm Information")

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
        ### Deterministic QuickSort

        - Pivot: Last element
        - Average: O(n log n)
        - Worst: O(n²)
        - Uses fixed pivot selection
        """
    )


with col2:

    st.info(
        """
        ### Randomized QuickSort

        - Pivot: Random element
        - Expected: O(n log n)
        - Worst: O(n²)
        - Randomizes pivot selection
        """
    )


# ============================================================
# Input Section
# ============================================================
st.divider()

st.subheader("⚙️ Test Configuration")

N = st.number_input(
    "Number of elements",
    min_value=10,
    max_value=10000,
    value=5000,
    step=100
)


run_button = st.button(
    "🚀 Run QuickSort Comparison"
)


# ============================================================
# Run Algorithms
# ============================================================
if run_button:

    N = int(N)

    # Generate test data
    with st.spinner(
        "Generating test cases..."
    ):

        test_cases = generate_test_cases(N)


    results = []


    # ========================================================
    # Run each test case
    # ========================================================
    with st.spinner(
        "Running QuickSort algorithms..."
    ):

        for case, arr in test_cases.items():

            # Deterministic QuickSort
            d_comps, d_time, d_sorted = run_test(
                deterministic_quicksort,
                arr
            )


            # Randomized QuickSort
            r_comps, r_time, r_sorted = run_test(
                randomized_quicksort,
                arr
            )


            results.append({

                "Input Type": case,

                "DQS Comparisons": d_comps,

                "DQS Time (ms)": round(
                    d_time,
                    4
                ),

                "RQS Comparisons": r_comps,

                "RQS Time (ms)": round(
                    r_time,
                    4
                )
            })


    # ========================================================
    # Results DataFrame
    # ========================================================
    df = pd.DataFrame(results)


    # ========================================================
    # Results Table
    # ========================================================
    st.divider()

    st.subheader(
        "📊 Performance Comparison"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # Comparison Metrics
    # ========================================================
    st.subheader(
        "📈 Comparison"
    )

    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "### Number of Comparisons"
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


    with col2:

        st.write(
            "### Execution Time"
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


    # ========================================================
    # Input Details
    # ========================================================
    st.divider()

    st.subheader(
        "🔍 Test Case Details"
    )

    for case, arr in test_cases.items():

        with st.expander(
            f"{case} Input"
        ):

            if N <= 100:

                st.write(arr)

            else:

                st.write(
                    f"Array contains {N} elements."
                )

                st.write(
                    "First 20 elements:"
                )

                st.write(
                    arr[:20]
                )


    # ========================================================
    # Explanation
    # ========================================================
    st.divider()

    st.subheader(
        "📖 Observation"
    )

    st.write(
        """
        **Random Input:**

        Both algorithms generally perform well because the
        input is not already ordered.


        **Sorted Input:**

        Deterministic QuickSort selects the last element as
        the pivot. Therefore, a sorted array can produce
        highly unbalanced partitions and approach O(n²).


        **Reverse Sorted Input:**

        Similar to sorted input, the fixed pivot can produce
        poor partitions.


        **Nearly Sorted Input:**

        Deterministic QuickSort can also suffer when the
        input is close to sorted.


        **Randomized QuickSort:**

        Random pivot selection helps avoid consistently bad
        pivot choices and gives an expected O(n log n)
        running time.
        """
    )


    # ========================================================
    # Complexity
    # ========================================================
    st.subheader(
        "⏱️ Time Complexity"
    )

    complexity_data = pd.DataFrame({

        "Algorithm": [
            "Deterministic QuickSort",
            "Randomized QuickSort"
        ],

        "Best Case": [
            "O(n log n)",
            "O(n log n)"
        ],

        "Average / Expected": [
            "O(n log n)",
            "O(n log n)"
        ],

        "Worst Case": [
            "O(n²)",
            "O(n²)"
        ]

    })


    st.dataframe(
        complexity_data,
        use_container_width=True,
        hide_index=True
    )
 
