import streamlit as st
import pandas as pd
import heapq
import time
import random

# -----------------------------
# Union Find
# -----------------------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# -----------------------------
# Kruskal Algorithm
# -----------------------------
def kruskal(n, edges):

    edges = sorted(edges)

    uf = UnionFind(n)

    mst = []
    cost = 0

    for w, u, v in edges:

        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w

            if len(mst) == n - 1:
                break

    return mst, cost


# -----------------------------
# Prim Algorithm
# -----------------------------
def prim(n, adj, start=0):

    INF = float("inf")

    key = [INF] * n
    parent = [-1] * n
    visited = [False] * n

    key[start] = 0

    pq = [(0, start)]

    mst = []
    cost = 0

    while pq:

        w, u = heapq.heappop(pq)

        if visited[u]:
            continue

        visited[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj.get(u, []):

            if not visited[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost


# -----------------------------
# Performance Test
# -----------------------------
def performance():

    vertices = [50, 100, 200, 500]

    data = []

    for n in vertices:

        edges = []

        for i in range(n):

            for j in range(i + 1, min(i + 6, n)):
                edges.append((random.randint(1, 100), i, j))

        adj = {}

        for w, u, v in edges:
            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, []).append((u, w))

        start = time.perf_counter()
        kruskal(n, edges.copy())
        k_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        prim(n, adj)
        p_time = (time.perf_counter() - start) * 1000

        data.append({
            "Vertices": n,
            "Kruskal Time(ms)": round(k_time, 5),
            "Prim Time(ms)": round(p_time, 5)
        })

    return pd.DataFrame(data)


# =====================================================
# Streamlit UI
# =====================================================

st.set_page_config(
    page_title="Minimum Spanning Tree",
    page_icon="🌳",
    layout="wide"
)

st.title("🌳 Minimum Spanning Tree Algorithms")

st.write(
"""
Compare **Kruskal's Algorithm** and **Prim's Algorithm**
for finding the Minimum Spanning Tree (MST).
"""
)

st.subheader("Default Graph")

default_edges = """7 0 1
5 0 3
8 1 2
9 1 3
7 1 4
5 2 4
15 3 4
6 3 5
8 4 5
9 4 6
11 5 6"""

vertices = st.number_input(
    "Number of Vertices",
    min_value=2,
    value=7
)

edge_input = st.text_area(
    "Enter Edges (weight source destination)",
    default_edges,
    height=250
)

if st.button("Find MST"):

    try:

        edges = []

        adj = {}

        for line in edge_input.strip().split("\n"):

            w, u, v = map(int, line.split())

            edges.append((w, u, v))

            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, []).append((u, w))

        k_mst, k_cost = kruskal(vertices, edges.copy())

        p_mst, p_cost = prim(vertices, adj)

        col1, col2 = st.columns(2)

        with col1:

            st.success("Kruskal Algorithm")

            st.table(
                pd.DataFrame(
                    k_mst,
                    columns=["Source", "Destination", "Weight"]
                )
            )

            st.write("### Total Cost =", k_cost)

        with col2:

            st.info("Prim Algorithm")

            st.table(
                pd.DataFrame(
                    p_mst,
                    columns=["Source", "Destination", "Weight"]
                )
            )

            st.write("### Total Cost =", p_cost)

    except:
        st.error("Invalid Input.")


st.divider()

st.subheader("Performance Comparison")

if st.button("Run Performance Test"):

    df = performance()

    st.dataframe(df, use_container_width=True)

    st.bar_chart(
        df.set_index("Vertices")[
            ["Kruskal Time(ms)", "Prim Time(ms)"]
        ]
    )

