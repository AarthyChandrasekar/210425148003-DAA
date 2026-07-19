import streamlit as st
import pandas as pd
import heapq
import random
import time

# ---------------------------------
# Dijkstra Algorithm
# ---------------------------------
def dijkstra(graph, source):

    n = len(graph)

    dist = [float("inf")] * n
    prev = [None] * n

    dist[source] = 0

    pq = [(0, source)]
    visited = set()

    while pq:

        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, w in graph[u]:

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

                heapq.heappush(pq, (dist[v], v))

    return dist, prev


# ---------------------------------
# Reconstruct Path
# ---------------------------------
def reconstruct_path(prev, source, target):

    path = []

    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path

    return []


# ---------------------------------
# Performance Analysis
# ---------------------------------
def performance():

    vertices = [100, 500, 1000, 2000]

    results = []

    for n in vertices:

        graph = {i: [] for i in range(n)}

        for i in range(n):

            for _ in range(3):

                v = random.randint(0, n - 1)

                if v != i:
                    w = random.randint(1, 20)
                    graph[i].append((v, w))

        start = time.perf_counter()

        dijkstra(graph, 0)

        elapsed = (time.perf_counter() - start) * 1000

        results.append({
            "Vertices": n,
            "Execution Time (ms)": round(elapsed, 5)
        })

    return pd.DataFrame(results)


# =====================================
# Streamlit UI
# =====================================

st.set_page_config(
    page_title="Dijkstra Algorithm",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ Dijkstra's Shortest Path Algorithm")

st.write(
"""
Find the shortest path from a source vertex to all other vertices
using **Dijkstra's Algorithm**.
"""
)

default_graph = """0 1 4
0 2 1
1 3 1
2 1 2
2 3 5
3 4 3
4 5 2"""

vertices = st.number_input(
    "Number of Vertices",
    min_value=2,
    value=6
)

source = st.number_input(
    "Source Vertex",
    min_value=0,
    max_value=vertices - 1,
    value=0
)

edge_input = st.text_area(
    "Enter Edges (Source Destination Weight)",
    default_graph,
    height=200
)

if st.button("Find Shortest Paths"):

    try:

        graph = {i: [] for i in range(vertices)}

        for line in edge_input.strip().split("\n"):

            u, v, w = map(int, line.split())

            graph[u].append((v, w))

        dist, prev = dijkstra(graph, source)

        output = []

        for v in range(vertices):

            path = reconstruct_path(prev, source, v)

            output.append({
                "Vertex": v,
                "Distance": "INF" if dist[v] == float("inf") else dist[v],
                "Path": " -> ".join(map(str, path)) if path else "No Path"
            })

        st.subheader("Shortest Paths")

        st.dataframe(
            pd.DataFrame(output),
            use_container_width=True
        )

    except:
        st.error("Invalid Input Format.")


st.divider()

st.subheader("Performance Analysis")

if st.button("Run Performance Test"):

    df = performance()

    st.dataframe(df, use_container_width=True)

    st.line_chart(
        df.set_index("Vertices")
    )
