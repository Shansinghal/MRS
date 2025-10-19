import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import download_file
import os
import gdown
from dotenv import load_dotenv

load_dotenv()

# Download only if the file doesn't exist already
if not os.path.exists("movie_dict.pkl"):
    gdown.download("https://drive.google.com/uc?id=1571AGYhYSOmCdFxVpa49RPk-IPXJLX_o", "movie_dict.pkl", quiet=False)


# Constants
API_KEY = os.getenv("TMDB_API_KEY")
TMDB_URL = "https://api.themoviedb.org/3/movie/popular"
POSTER_URL = "https://image.tmdb.org/t/p/w500"

# Setup requests session with retry logic
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))


def get_movies():
    try:
        response = session.get(TMDB_URL, params={"api_key": API_KEY}, timeout=10)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            st.error(f"TMDB API Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")
    return []


# Get poster from TMDB using movie ID (from local movie dataset)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": API_KEY}
    data = session.get(url, params=params).json()
    poster_path = data.get("poster_path")
    if poster_path:
        return POSTER_URL + poster_path
    return ""


# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_df = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similiarity.pkl', 'rb'))


def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_titles.append(movies_df.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters


# ----------------------------
# Streamlit App Frontend
# ----------------------------

st.set_page_config(layout="wide")
st.title("🔍 Movie Recommender System")

# --- Search Bar ---
selected_movie = st.selectbox("Search for a movie to get recommendations:", movies_df['title'].values)

# --- Recommend Button ---
if st.button("Recommend"):
    titles, posters = recommend(selected_movie)
    st.subheader("🎯 Recommended Movies:")
    rec_cols = st.columns(5)
    for idx, col in enumerate(rec_cols):
        with col:
            st.image(posters[idx], caption=titles[idx], use_container_width=True)

# --- Popular Movies Section ---
st.markdown("---")
st.title("🎬 Popular Movies Right Now")

movies = get_movies()
if movies:
    cols = st.columns(3)
    for idx, movie in enumerate(movies):
        with cols[idx % 3]:
            if movie.get("poster_path"):
                st.image(f"{POSTER_URL}{movie['poster_path']}", caption=movie["title"], use_container_width=True)
else:
    st.warning("No movies found. Check your API key or network connection.")
