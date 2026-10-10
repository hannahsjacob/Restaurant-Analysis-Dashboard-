import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Restaurant Intelligence Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# Load Data
df = pd.read_csv("zomato_cleaned.csv")

# Title
st.title("🍽️ What Makes a Restaurant Successful in Bengaluru?")
st.subheader("An analytical study of 41,263 restaurants using ratings, pricing, locations and cuisine preferences.")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Restaurants", len(df))

with col2:
    st.metric("Average Rating", round(df['rate'].mean(), 2))

with col3:
    st.metric(
        "Average Cost for Two",
        f"₹{round(df['approx_cost(for two people)'].mean())}"
    )

with col4:
    st.metric(
        "Top Cuisine",
        "North Indian"
    )

    # Sidebar Filters
st.sidebar.header("Filters")

selected_location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + sorted(df["location"].dropna().unique().tolist())
)

# Apply Filter
if selected_location != "All":
    filtered_df = df[df["location"] == selected_location]
else:
    filtered_df = df

col1, col2 = st.columns(2)

with col1:

    st.subheader("⭐ Rating Distribution")

    fig_rating = px.histogram(
        filtered_df,
        x="rate",
        nbins=20,
        title=""
    )

    st.plotly_chart(fig_rating, use_container_width=True)

with col2:

    st.subheader("📍 Top 10 Locations")

    top_locations = (
        filtered_df["location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_locations.columns = ["Location", "Count"]

    fig_location = px.bar(
        top_locations,
        x="Location",
        y="Count",
        color="Count",
        title=""
    )

    st.plotly_chart(fig_location, use_container_width=True)
    fig_location = px.bar(
    top_locations,
    x="Location",
    y="Count",
    color="Count",
    title=""
)

fig_location.update_layout(
    coloraxis_showscale=False
)

st.plotly_chart(fig_location, use_container_width=True)

col3, col4 = st.columns([3, 1])

with col3:

    st.subheader("🍜 Cuisine Market Share")

    top_cuisines = (
        filtered_df["cuisines"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    top_cuisines.columns = ["Cuisine", "Count"]

    fig = px.treemap(
        top_cuisines,
        path=["Cuisine"],
        values="Count",
        title=""
    )

    fig.update_traces(
    textfont_size=22
    )

    fig.update_layout(
    height=450
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:

    st.subheader("📊 Key Insights")

    st.metric("Top Location", "BTM")
    st.metric("Most Common Rating", "3.8")
    st.metric("Top Cuisine", "North Indian")
    st.metric("Avg Cost", "₹604")