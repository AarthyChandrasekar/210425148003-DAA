import streamlit as st
import pandas as pd
import random


# ==========================================
# Divide and Conquer Min-Max
# ==========================================

def min_max_dc(arr, low, high):
    # Base case: one element
    if low == high:
        return arr[low], arr[low], 0

    # Base case: two elements
    if high == low + 1:
        if arr[low] < arr[high]:
            return arr[low], arr[high], 1
        else:
            return arr[high], arr[low], 1

    # Divide
    mid = (low + high) // 2

    lmin, lmax, left_comps = min_max_dc(
        arr, low, mid
    )

    rmin, rmax, right_comps = min_max_dc(
        arr, mid + 1, high
    )

    # Conquer
    min_comp = 1
    max_comp = 1

    overall_min = (
        lmin if lmin < rmin else rmin
    )

    overall_max = (
        lmax if lmax > rmax else rmax
    )

    total_comps = (
        left_comps
        + right_comps
        + min_comp
        + max_comp
    )

    return overall_min, overall_max, total_comps


# ==========================================
# Naive Method
# ==========================================

def min_max_naive(arr):

    mn = arr[0]
    mx = arr[0]

    comparisons = 0

    for x in arr[1:]:

        comparisons += 1

        if x < mn:
            mn = x

        comparisons += 1

        if x > mx:
            mx = x

    return mn, mx, comparisons


# ==========================================
# Performance Analysis
# ==========================================

def performance_analysis():

    sizes = [10, 100, 1000, 10000]

    results = []

    for size in sizes:

        arr = [
            random.randint(1, 10000)
            for _ in range(size)
        ]

        # Divide and Conquer
        mn, mx, dc_comps = min_max_dc(
            arr, 0, len(arr) - 1
        )

        # Naive
        _, _, naive_comps = min_max_naive(arr)

        # Theoretical formula
        formula = (3 * size // 2) - 2

        results.append({
            "Array Size": size,
            "D&C Comparisons": dc_comps,
            "Naive Comparisons": naive_comps,
            "Formula (3n/2 - 2)": formula
        })

    return pd.DataFrame(results)


# ==========================================
# Streamlit Configuration
# ==========================================

st.set_page_config(
    page_title="Min-Max Divide and Conquer",
    page_icon="🔢",
    layout="wide"
)


# ==========================================
# Main UI
# ==========================================

st.title("🔢 Min-Max using Divide and Conquer")

st.write(
    """
    Find the **minimum and maximum elements** of an array
    using **Divide and Conquer** and compare its number of
    comparisons with the **Naive approach**.
    """
)


# ==========================================
# Input Array
# ==========================================

st.subheader("Enter Array")

array_input = st.text_input(
    "Enter integers separated by commas",
    value="3,1,7,4,9,2,8,5,6,0"
)


# ==========================================
# Find Min-Max
# ==========================================

if st.button("Find Minimum and Maximum"):

    try:

        arr = [
            int(x.strip())
            for x in array_input.split(",")
            if x.strip()
        ]

        if len(arr) == 0:

            st.error("Please enter at least one number.")

        else:

            # Divide and Conquer
            mn_dc, mx_dc, dc_comps = min_max_dc(
                arr,
                0,
                len(arr) - 1
            )

            # Naive
            mn_naive, mx_naive, naive_comps = (
                min_max_naive(arr)
            )

            # ==================================
            # Display Array
            # ==================================

            st.subheader("Input Array")

            st.write(arr)


            # ==================================
            # Results
            # ==================================

            st.subheader("Results")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.success("Minimum")

                st.metric(
                    "Minimum Value",
                    mn_dc
                )

            with col2:

                st.info("Maximum")

                st.metric(
                    "Maximum Value",
                    mx_dc
                )

            with col3:

                st.warning("Array Size")

                st.metric(
                    "Number of Elements",
                    len(arr)
                )


            # ==================================
            # Comparison Table
            # ==================================

            st.subheader("Comparison Count")

            formula = (
                3 * len(arr) // 2
            ) - 2

            comparison_data = pd.DataFrame({
                "Method": [
                    "Divide & Conquer",
                    "Naive",
                    "Theoretical Formula"
                ],
                "Comparisons": [
                    dc_comps,
                    naive_comps,
                    formula
                ]
            })

            st.dataframe(
                comparison_data,
                use_container_width=True,
                hide_index=True
            )


            # ==================================
            # Explanation
            # ==================================

            st.subheader("Algorithm Analysis")

            st.write(
                f"""
                **Divide & Conquer:**
                {dc_comps} comparisons

                **Naive Approach:**
                {naive_comps} comparisons

                **Theoretical formula:**
                3n/2 - 2 = {formula}
                """
            )


# ==========================================
# Performance Analysis
# ==========================================

st.divider()

st.subheader("⚡ Performance Analysis")

st.write(
    """
    Compare the number of comparisons for different
    array sizes.
    """
)

if st.button("Run Performance Analysis"):

    df = performance_analysis()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Comparison graph
    chart_df = df.set_index("Array Size")

    st.line_chart(
        chart_df[
            [
                "D&C Comparisons",
                "Naive Comparisons",
                "Formula (3n/2 - 2)"
            ]
        ]
    )
