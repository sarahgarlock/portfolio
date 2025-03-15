import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
print("Current Working Directory: ", os.getcwd())


# Load the dataset
df = pd.read_csv("/mount/src/portfolio/projects/music_data/data/dataset.csv")


# Handle missing values
df = df.fillna({'artists': 'Unknown Artist', 
                'album_name': 'Unknown Album', 
                'track_name': 'Untitled Track'})


# 🎨 Streamlit App Layout
st.title("Spotify Popularity Analysis 🎵")
st.write("Explore the most popular artists and track trends!")

# 🎤 Most Popular Artists
st.subheader("Top Artists by Popularity")
artist_popularity = df.groupby("artists")["popularity"].mean().reset_index()
top_artists = artist_popularity.sort_values(by="popularity", ascending=False).head(10)

st.dataframe(top_artists)  # Display as interactive table

# 📈 Popularity Over Time
st.subheader("Popularity Over Time")
df["year"] = df["album_name"].str.extract(r'(\d{4})').astype(float)
popularity_by_year = df.groupby("year")["popularity"].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(popularity_by_year, marker="o", linestyle="-", color="blue")
ax.set_xlabel("Year")
ax.set_ylabel("Popularity")
ax.set_title("Average Song Popularity Over Time")
st.pyplot(fig)

# 🎶 Tempo vs Popularity
st.subheader("Tempo vs Popularity")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x=df["tempo"], y=df["popularity"], alpha=0.5, ax=ax)
ax.set_xlabel("Tempo (BPM)")
ax.set_ylabel("Popularity")
ax.set_title("Song Tempo vs Popularity")
st.pyplot(fig)

st.write("🎵 *Data sourced from Spotify*")
