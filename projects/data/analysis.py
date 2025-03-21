import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests
from io import StringIO

# --- Data Loading ---
def load_data():
    url = 'https://raw.githubusercontent.com/sarahgarlock/portfolio/main/projects/data/dataset.csv'  # Use the raw URL
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None

# Load the data
df = load_data()

if df is not None:
    # Continue your visualizations!
    st.write("Data loaded successfully!")
else:
    st.stop()  # Stop execution if data fails to load

# Fill missing values in key columns to avoid issues during analysis
df = df.fillna({
    'artists': 'Unknown Artist', 
    'album_name': 'Unknown Album', 
    'track_name': 'Untitled Track'
})

# --- Streamlit App Layout ---
st.title("🎧 Spotify Popularity Analysis - March 2025")
st.write("Explore the most popular artists and track trends!")

# --- Top 10 Artists by Average Popularity (Bar Plot) ---
st.subheader("Top 10 Artists by Popularity")

# Calculate average popularity per artist
artist_popularity = df.groupby("artists")["popularity"].mean().reset_index()
top_artists = artist_popularity.sort_values(by="popularity", ascending=False).head(10)

# Visualize top artists using Seaborn bar plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_artists, x="popularity", y="artists", palette="viridis", ax=ax)
ax.set_xlabel("Average Popularity")
ax.set_ylabel("Artist")
ax.set_title("Top 10 Artists by Popularity")

# Add popularity labels next to bars
for i, v in enumerate(top_artists["popularity"]):
    ax.text(v + 0.5, i, f"{v:.1f}", va='center', fontsize=10, color='gray')

st.pyplot(fig)
st.dataframe(top_artists)  # Optional: Display data table

# --- Popularity Over Time (Line Plot) ---
st.subheader("Popularity Over Time")

# Extract release year from album name
df["year"] = df["album_name"].str.extract(r'(\d{4})')
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

# Filter realistic years
df = df[(df["year"] >= 1950) & (df["year"] <= 2025)]

# Group by year and calculate average popularity
popularity_by_year = df.groupby("year")["popularity"].mean().reset_index()

# Apply rolling average to smooth line chart
popularity_by_year["smoothed"] = popularity_by_year["popularity"].rolling(window=3, center=True).mean()

# Plot popularity trend over time
fig_line = px.line(
    popularity_by_year,
    x="year",
    y="smoothed",
    markers=True,
    title="Average Song Popularity Over Time (Smoothed)",
    labels={"year": "Year", "smoothed": "Avg Popularity"},
    template="plotly_dark"
)

fig_line.update_traces(mode="lines+markers", hovertemplate="Year: %{x}<br>Popularity: %{y:.2f}")
fig_line.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='gray')
fig_line.update_yaxes(range=[0, 100])

st.plotly_chart(fig_line, use_container_width=True)

# --- Tempo vs Popularity (Scatter Plot) ---
st.subheader("Tempo vs Popularity")

# Scatter plot: how tempo correlates to popularity
fig_scatter = px.scatter(
    df, 
    x="tempo", 
    y="popularity",
    color="popularity",
    title="Song Tempo vs Popularity",
    labels={"tempo": "Tempo (BPM)", "popularity": "Popularity"},
    opacity=0.6,
    template="plotly_dark",
    color_continuous_scale="Viridis"
)

fig_scatter.update_traces(marker=dict(size=8), hovertemplate="Tempo: %{x}<br>Popularity: %{y}")
st.plotly_chart(fig_scatter, use_container_width=True)

# --- Footer ---
st.write("🎵 *Data sourced from Spotify*")
