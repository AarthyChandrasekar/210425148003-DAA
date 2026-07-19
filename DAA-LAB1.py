import streamlit as st
import time
import random
import pandas as pd

# -----------------------------
# Interpolation Search
# -----------------------------
def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while (
        low <= high
        and low < len(arr)
        and high >= 0
        and arr[low] <= target <= arr[high]
    ):
        comparisons += 1

        if arr[low] == arr[high]:
            if arr[low] == target:
                return low, comparisons
            break

        pos = low + int(
            ((target - arr[low]) * (high - low))
            / (arr[high] - arr[low])
        )

        if pos < low or pos > high:
            break

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


# -----------------------------
# Binary Search
# -----------------------------
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


# -----------------------------
# Performance Analysis
# -----------------------------
def performance_analysis():
    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        # Interpolation Search
        start = time.perf_counter()
        for _ in range(100):
            _, comp_is = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000

        # Binary Search
        start = time.perf_counter()
        for _ in range(100):
            _, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        results.append({
            "Array Size": size,
            "Interpolation Time (ms)": round(is_time, 5),
            "Binary Time (ms)": round(bs_time, 5),
            "Interpolation Comparisons": comp_is,
            "Binary Comparisons": comp_bs
        })

    return pd.DataFrame(results)


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Interpolation Search", page_icon="🔍", layout="wide")

st.title("🔍 Interpolation Search Visualization")

st.write("""
This application compares **Interpolation Search** and **Binary Search**.
Enter a sorted array and a target value.
""")

default_array = "2,5,10,15,23,35,48,60,75,90,105,120"

array_input = st.text_input(
    "Enter Sorted Array (comma separated)",
    default_array
)

target = st.number_input(
    "Enter Target Value",
    value=35,
    step=1
)

if st.button("Search"):

    try:
        arr = list(map(int, array_input.split(",")))
        arr.sort()

        idx_is, comp_is = interpolation_search(arr, target)
        idx_bs, comp_bs = binary_search(arr, target)

        st.subheader("Search Results")

        col1, col2 = st.columns(2)

        with col1:
            st.success("Interpolation Search")
            if idx_is != -1:
                st.write(f"**Index:** {idx_is}")
            else:
                st.write("Target Not Found")
            st.write(f"**Comparisons:** {comp_is}")

        with col2:
            st.info("Binary Search")
            if idx_bs != -1:
                st.write(f"**Index:** {idx_bs}")
            else:
                st.write("Target Not Found")
            st.write(f"**Comparisons:** {comp_bs}")

    except:
        st.error("Please enter a valid sorted integer array.")


st.divider()

st.subheader("Performance Analysis")

if st.button("Run Performance Analysis"):
    df = performance_analysis()
    st.dataframe(df, use_container_width=True)

    st.line_chart(
        df.set_index("Array Size")[
            ["Interpolation Time (ms)", "Binary Time (ms)"]
        ]
    )
