import streamlit as st
import pandas as pd
import math


# ==========================================
# First Fit
# ==========================================
def first_fit(items, capacity=1.0):

    bins = []
    bin_contents = []

    for item in items:

        placed = False

        for i, space in enumerate(bins):

            if space >= item:

                bins[i] -= item
                bin_contents[i].append(item)

                placed = True
                break

        if not placed:

            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ==========================================
# First Fit Decreasing
# ==========================================
def first_fit_decreasing(items, capacity=1.0):

    sorted_items = sorted(
        items,
        reverse=True
    )

    return first_fit(
        sorted_items,
        capacity
    )


# ==========================================
# Best Fit Decreasing
# ==========================================
def best_fit_decreasing(items, capacity=1.0):

    sorted_items = sorted(
        items,
        reverse=True
    )

    bins = []
    bin_contents = []

    for item in sorted_items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):

            remaining = space - item

            if (
                space >= item
                and remaining < best_space
            ):
                best_space = remaining
                best_idx = i

        if best_idx >= 0:

            bins[best_idx] -= item
            bin_contents[best_idx].append(item)

        else:

            bins.append(
                capacity - item
            )

            bin_contents.append(
                [item]
            )

    return bin_contents


# ==========================================
# Create Bin Table
# ==========================================
def create_bin_table(bins, capacity):

    data = []

    for i, items in enumerate(bins, 1):

        used = sum(items)
        remaining = capacity - used
        utilization = (
            used / capacity
        ) * 100

        data.append({
            "Bin": f"Bin {i}",
            "Items": ", ".join(
                str(round(x, 2))
                for x in items
            ),
            "Used": round(used, 3),
            "Remaining": round(
                remaining,
                3
            ),
            "Utilization (%)": round(
                utilization,
                2
            )
        })

    return pd.DataFrame(data)


# ==========================================
# Streamlit Configuration
# ==========================================
st.set_page_config(
    page_title="Bin Packing Algorithms",
    page_icon="📦",
    layout="wide"
)


# ==========================================
# Title
# ==========================================
st.title("📦 Bin Packing Algorithms")

st.write(
    """
    Compare three bin-packing heuristics:

    - **First Fit (FF)**
    - **First Fit Decreasing (FFD)**
    - **Best Fit Decreasing (BFD)**
    """
)


# ==========================================
# Input Section
# ==========================================
st.subheader("Input")

items_input = st.text_input(
    "Enter item sizes separated by commas",
    value="0.5,0.7,0.3,0.9,0.2,0.6,0.8,0.4,0.1,0.5"
)

capacity = st.number_input(
    "Bin Capacity",
    min_value=0.01,
    value=1.0,
    step=0.1
)


# ==========================================
# Solve
# ==========================================
if st.button("🚀 Pack Items"):

    try:

        # Convert input
        items = [
            float(x.strip())
            for x in items_input.split(",")
            if x.strip()
        ]

        # ======================================
        # Validation
        # ======================================

        if len(items) == 0:

            st.error(
                "Please enter at least one item."
            )

            st.stop()

        if any(x <= 0 for x in items):

            st.error(
                "Item sizes must be greater than 0."
            )

            st.stop()

        if any(x > capacity for x in items):

            st.error(
                "An item cannot be larger than "
                "the bin capacity."
            )

            st.stop()


        # ======================================
        # Lower Bound
        # ======================================

        total_size = sum(items)

        lower_bound = math.ceil(
            total_size / capacity
        )


        # ======================================
        # Run Algorithms
        # ======================================

        ff_bins = first_fit(
            items,
            capacity
        )

        ffd_bins = first_fit_decreasing(
            items,
            capacity
        )

        bfd_bins = best_fit_decreasing(
            items,
            capacity
        )


        # ======================================
        # Input Information
        # ======================================

        st.subheader("📊 Input Information")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Number of Items",
                len(items)
            )

        with col2:
            st.metric(
                "Bin Capacity",
                capacity
            )

        with col3:
            st.metric(
                "Total Item Size",
                round(total_size, 3)
            )

        with col4:
            st.metric(
                "Lower Bound",
                lower_bound
            )


        # ======================================
        # Summary
        # ======================================

        st.subheader("🏆 Algorithm Comparison")

        summary = pd.DataFrame({
            "Algorithm": [
                "First Fit (FF)",
                "First Fit Decreasing (FFD)",
                "Best Fit Decreasing (BFD)"
            ],
            "Number of Bins": [
                len(ff_bins),
                len(ffd_bins),
                len(bfd_bins)
            ]
        })

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )


        # ======================================
        # Chart
        # ======================================

        chart_data = summary.set_index(
            "Algorithm"
        )

        st.bar_chart(
            chart_data["Number of Bins"]
        )


        # ======================================
        # First Fit
        # ======================================

        st.divider()

        st.subheader(
            f"📦 First Fit (FF) — "
            f"{len(ff_bins)} bins"
        )

        ff_table = create_bin_table(
            ff_bins,
            capacity
        )

        st.dataframe(
            ff_table,
            use_container_width=True,
            hide_index=True
        )

        for i, b in enumerate(
            ff_bins,
            1
        ):

            used = sum(b)

            st.write(
                f"**Bin {i}** — "
                f"Used: {used:.3f} / {capacity}"
            )

            st.progress(
                min(
                    used / capacity,
                    1.0
                )
            )


        # ======================================
        # First Fit Decreasing
        # ======================================

        st.divider()

        st.subheader(
            f"📦 First Fit Decreasing (FFD) — "
            f"{len(ffd_bins)} bins"
        )

        ffd_table = create_bin_table(
            ffd_bins,
            capacity
        )

        st.dataframe(
            ffd_table,
            use_container_width=True,
            hide_index=True
        )

        for i, b in enumerate(
            ffd_bins,
            1
        ):

            used = sum(b)

            st.write(
                f"**Bin {i}** — "
                f"Used: {used:.3f} / {capacity}"
            )

            st.progress(
                min(
                    used / capacity,
                    1.0
                )
            )


        # ======================================
        # Best Fit Decreasing
        # ======================================

        st.divider()

        st.subheader(
            f"📦 Best Fit Decreasing (BFD) — "
            f"{len(bfd_bins)} bins"
        )

        bfd_table = create_bin_table(
            bfd_bins,
            capacity
        )

        st.dataframe(
            bfd_table,
            use_container_width=True,
            hide_index=True
        )

        for i, b in enumerate(
            bfd_bins,
            1
        ):

            used = sum(b)

            st.write(
                f"**Bin {i}** — "
                f"Used: {used:.3f} / {capacity}"
            )

            st.progress(
                min(
                    used / capacity,
                    1.0
                )
            )


        # ======================================
        # Final Summary
        # ======================================

        st.divider()

        st.subheader("📋 Final Summary")

        st.success(
            f"""
            Lower Bound = {lower_bound}

            First Fit (FF) = {len(ff_bins)} bins

            First Fit Decreasing (FFD) = {len(ffd_bins)} bins

            Best Fit Decreasing (BFD) = {len(bfd_bins)} bins
            """
        )


    except ValueError:

        st.error(
            "Invalid input. Please enter only numbers "
            "separated by commas."
        )
