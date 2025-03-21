import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# --- Data Loading ---
# Get path relative to script
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'dataset.csv')

df = pd.read_csv(csv_path)

# Handle missing values
df = df.fillna({
    'artists': 'Unknown Artist', 
    'album_name': 'Unknown Album', 
    'track_name': 'Untitled Track'
})

# 🎨 Streamlit App Layout
st.title("🎧 Spotify Popularity Analysis")
st.write("Explore the most popular artists and track trends!")

# 🎤 Top Artists by Popularity - Bar Plot
st.subheader("Top 10 Artists by Popularity")
artist_popularity = df.groupby("artists")["popularity"].mean().reset_index()
top_artists = artist_popularity.sort_values(by="popularity", ascending=False).head(10)

# Bar Plot with Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_artists, x="popularity", y="artists", palette="viridis", ax=ax)
ax.set_xlabel("Average Popularity")
ax.set_ylabel("Artist")
ax.set_title("Top 10 Artists by Popularity")
st.pyplot(fig)

st.dataframe(top_artists)  # Optional: still show data table

# 📈 Popularity Over Time - Plotly Line Plot
st.subheader("Popularity Over Time")

# Extract year from album name
df["year"] = df["album_name"].str.extract(r'(\d{4})')

# Drop rows where year couldn't be extracted
df = df.dropna(subset=["year"])

# Convert year to integer
df["year"] = df["year"].astype(int)

# Optional: Keep only realistic years
df = df[(df["year"] >= 1950) & (df["year"] <= 2025)]

# Group by year and calculate average popularity
popularity_by_year = df.groupby("year")["popularity"].mean().reset_index()

# Plotly Line Chart
fig_line = px.line(
    popularity_by_year,
    x="year",
    y="popularity",
    markers=True,
    title="Average Song Popularity Over Time",
    labels={"year": "Year", "popularity": "Avg Popularity"},
    template="plotly_dark"
)

st.plotly_chart(fig_line, use_container_width=True)


# 🎶 Tempo vs Popularity - Plotly Scatter Plot
st.subheader("Tempo vs Popularity")
fig_scatter = px.scatter(
    df, 
    x="tempo", 
    y="popularity",
    color="popularity",
    title="Song Tempo vs Popularity",
    labels={"tempo": "Tempo (BPM)", "popularity": "Popularity"},
    opacity=0.6,
    template="plotly_dark"
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.write("🎵 *Data sourced from Spotify*")
