import streamlit as st
import pandas as pd
import random
import time

# -------------------------------
# Naive String Matching
# -------------------------------
def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)

    return matches, comparisons


# -------------------------------
# Compute LPS Array
# -------------------------------
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


# -------------------------------
# KMP Search
# -------------------------------
def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]

        elif i < n and j < m and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


# -------------------------------
# Rabin Karp
# -------------------------------
def rabin_karp(text, pattern, q=101):
    n = len(text)
    m = len(pattern)

    d = 256
    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:

            for k in range(m):
                comparisons += 1

                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)

        if s < n - m:
            t_hash = (
                d * (t_hash - ord(text[s]) * h)
                + ord(text[s + m])
            ) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# -------------------------------
# Performance Analysis
# -------------------------------
def performance_analysis():

    text_large = ''.join(random.choices("ABCD", k=10000))
    patterns = ["AB", "ABCD", "ABCDAB", "ABCDABCD"]

    results = []

    for p in patterns:

        # Naive
        start = time.perf_counter()
        for _ in range(50):
            _, c1 = naive_search(text_large, p)
        naive_time = (time.perf_counter() - start) / 50 * 1000

        # KMP
        start = time.perf_counter()
        for _ in range(50):
            _, c2 = kmp_search(text_large, p)
        kmp_time = (time.perf_counter() - start) / 50 * 1000

        # Rabin-Karp
        start = time.perf_counter()
        for _ in range(50):
            _, c3 = rabin_karp(text_large, p)
        rk_time = (time.perf_counter() - start) / 50 * 1000

        results.append({
            "Pattern": p,
            "Naive Comparisons": c1,
            "KMP Comparisons": c2,
            "RK Comparisons": c3,
            "Naive Time(ms)": round(naive_time, 5),
            "KMP Time(ms)": round(kmp_time, 5),
            "RK Time(ms)": round(rk_time, 5)
        })

    return pd.DataFrame(results)


# ===============================
# Streamlit UI
# ===============================

st.set_page_config(
    page_title="String Matching Algorithms",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 String Matching Algorithms")

st.write(
    "Compare **Naive Search**, **Knuth-Morris-Pratt (KMP)** and **Rabin-Karp** algorithms."
)

text = st.text_area(
    "Enter Text",
    "AABAACAADAABAABA"
)

pattern = st.text_input(
    "Enter Pattern",
    "AABA"
)

if st.button("Search Pattern"):

    if pattern == "":
        st.error("Pattern cannot be empty.")

    elif len(pattern) > len(text):
        st.error("Pattern length cannot be greater than text length.")

    else:

        naive_match, naive_comp = naive_search(text, pattern)
        kmp_match, kmp_comp = kmp_search(text, pattern)
        rk_match, rk_comp = rabin_karp(text, pattern)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("Naive Search")
            st.write("Matches:", naive_match)
            st.write("Comparisons:", naive_comp)

        with col2:
            st.info("KMP")
            st.write("Matches:", kmp_match)
            st.write("Comparisons:", kmp_comp)

        with col3:
            st.warning("Rabin-Karp")
            st.write("Matches:", rk_match)
            st.write("Comparisons:", rk_comp)


st.divider()

st.subheader("Performance Comparison")

if st.button("Run Performance Analysis"):

    df = performance_analysis()

    st.dataframe(df, use_container_width=True)

    st.line_chart(
        df.set_index("Pattern")[
            [
                "Naive Time(ms)",
                "KMP Time(ms)",
                "RK Time(ms)"
            ]
        ]
    )
