import streamlit as st
import pandas as pd
import random


# ==========================================
# Divide and Conquer Min-Max
# ==========================================
def min_max_dc(arr, low, high):

    # One element
    if low == high:
        return arr[low], arr[low], 0

    # Two elements
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
    overall_min = lmin if lmin < rmin else rmin
    overall_max = lmax if lmax > rmax else rmax

    total_comps = (
        left_comps
        + right_comps
        + 2
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
# Theoretical Comparison Formula
# ==========================================
def theoretical_comparisons(n):

    if n <= 1:
        return 0

    if n % 2 == 0:
        return (3 * n // 2) - 2

    return (3 * (n - 1) // 2)


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
        _, _, dc_comps = min_max_dc(
            arr,
            0,
            len(arr) - 1
        )

        # Naive
        _, _, naive_comps = min_max_naive(arr)

        # Theoretical formula
        formula = theoretical_comparisons(size)

        results.append({
            "Array Size": size,
            "D&C Comparisons": dc_comps,
            "Naive Comparisons": naive_comps,
            "Formula": formula
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
# Main Title
# ==========================================
st.title("🔢 Min-Max using Divide and Conquer")

st.write(
    """
    Find the **minimum and maximum elements** of an array
    using the **Divide and Conquer** technique and compare
    it with the **Naive approach**.
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
# Find Min-Max Button
# ==========================================
if st.button("🔍 Find Minimum and Maximum"):

    try:

        arr = [
            int(x.strip())
            for x in array_input.split(",")
            if x.strip()
        ]

    except ValueError:

        st.error(
            "Invalid input! Please enter integers only."
        )

        st.stop()


    if len(arr) == 0:

        st.error(
            "Please enter at least one number."
        )

        st.stop()


    # ======================================
    # Divide and Conquer
    # ======================================

    mn_dc, mx_dc, dc_comps = min_max_dc(
        arr,
        0,
        len(arr) - 1
    )


    # ======================================
    # Naive
    # ======================================

    mn_naive, mx_naive, naive_comps = (
        min_max_naive(arr)
    )


    # ======================================
    # Input Array
    # ======================================

    st.subheader("📋 Input Array")

    st.code(str(arr))


    # ======================================
    # Results
    # ======================================

    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Minimum",
            mn_dc
        )

    with col2:

        st.metric(
            "Maximum",
            mx_dc
        )

    with col3:

        st.metric(
            "Array Size",
            len(arr)
        )


    # ======================================
    # Verify Results
    # ======================================

    if (
        mn_dc == mn_naive
        and mx_dc == mx_naive
    ):

        st.success(
            "✓ Divide & Conquer and Naive results match!"
        )


    # ======================================
    # Comparison Count
    # ======================================

    st.subheader("🔢 Comparison Count")

    formula = theoretical_comparisons(
        len(arr)
    )

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


    # ======================================
    # Comparison Chart
    # ======================================

    st.subheader("📈 Comparison Chart")

    chart_data = comparison_data.set_index(
        "Method"
    )

    st.bar_chart(
        chart_data["Comparisons"]
    )


    # ======================================
    # Algorithm Analysis
    # ======================================

    st.subheader("📚 Algorithm Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            ### Divide & Conquer

            Comparisons: **{dc_comps}**

            Time Complexity: **O(n)**

            Space Complexity: **O(log n)**
            """

        )

    with col2:

        st.markdown(
            f"""
            ### Naive Approach

            Comparisons: **{naive_comps}**

            Time Complexity: **O(n)**

            Space Complexity: **O(1)**
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


if st.button("🚀 Run Performance Analysis"):

    with st.spinner(
        "Running performance analysis..."
    ):

        df = performance_analysis()


    # ======================================
    # Table
    # ======================================

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # Chart
    # ======================================

    st.subheader(
        "📈 Comparison Growth"
    )

    chart_df = df.set_index(
        "Array Size"
    )

    st.line_chart(
        chart_df[
            [
                "D&C Comparisons",
                "Naive Comparisons",
                "Formula"
            ]
        ]
    )


    # ======================================
    # Explanation
    # ======================================

    st.info(
        """
        **Observation:**

        The Divide & Conquer method reduces the number
        of comparisons compared with the naive method.

        Both methods have O(n) time complexity, but
        Divide & Conquer uses fewer comparisons.
        """
    )
