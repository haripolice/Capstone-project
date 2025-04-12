import streamlit as st
import pandas as pd

# Load IMDb Data
df = pd.read_csv("IMDb_2024_Movies.csv")

# Sidebar Filters
st.sidebar.header("Filter Movies")
selected_genre = st.sidebar.multiselect("Select Genre", df["Genre"].unique())
selected_rating = st.sidebar.slider("Select Minimum Rating", 0.0, 10.0, 5.0)
selected_votes = st.sidebar.slider("Select Minimum Votes", 0, int(df["Voting Counts"].max()), 1000)

# Apply Filters
filtered_df = df[
    (df["Ratings"] >= selected_rating) & 
    (df["Voting Counts"] >= selected_votes)
]

if selected_genre:
    filtered_df = filtered_df[df["Genre"].isin(selected_genre)]

# Display Data
st.title("🎬 IMDb 2024 Movies Dashboard")
st.write("## 📊 Filtered Movie Data")
st.dataframe(filtered_df)

# Top 10 Movies Chart
st.write("## ⭐ Top 10 Movies by Rating")
top_movies = filtered_df.nlargest(10, "Ratings")
st.bar_chart(top_movies.set_index("Movie Name")["Ratings"])

# Genre Distribution
st.write("## 🎭 Genre Distribution")
st.bar_chart(df["Genre"].value_counts())

# Run the app    
# Execute in terminal: `streamlit run app.py`
