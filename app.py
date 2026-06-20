import streamlit as st
import pickle
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Netflix Movie Recommender", layout="wide")

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
api_key = st.secrets["OMDB_API_KEY"]

# ---------------- CSS ----------------
st.markdown("""
<style>

body {
    background-color: #141414;
    color: white;
}

.main-title {
    font-size: 45px;
    font-weight: bold;
    color: #E50914;
    text-align: center;
    margin-bottom: 10px;
}

.sub-title {
    color: #bbb;
    text-align: center;
    margin-bottom: 20px;
}

.movie-card {
    transition: 0.3s;
    border-radius: 10px;
}

.movie-card:hover {
    transform: scale(1.08);
}

.movie-title {
    text-align: center;
    font-size: 13px;
    margin-top: 5px;
    color: white;
}

.section-title {
    font-size: 22px;
    margin: 20px 0 10px 0;
    color: #fff;
}

hr {
    border: 1px solid #333;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 class='main-title'> YOUR RECOMMENDED MOVIES 🎬</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>ML Powered Movie Recommendation System</p>", unsafe_allow_html=True)

# ---------------- POSTER FETCH ----------------
def fetch_poster(movie_name):
    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    data = requests.get(url).json()

    if data.get("Poster") and data["Poster"] != "N/A":
        return data["Poster"]

    return "https://via.placeholder.com/300x450?text=No+Image"

# ---------------- RECOMMENDATION ----------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_posters

# ---------------- MAIN SELECT ----------------
selected_movie = st.selectbox("🔍 Search Movie", movies['title'].values)

# ---------------- MAIN: RECOMMENDATIONS ----------------
st.markdown("<h3 class='section-title'>🎯 Recommended for You</h3>", unsafe_allow_html=True)

recommended_movies, recommended_posters = recommend(selected_movie)

cols = st.columns(5)

for i in range(5):
    with cols[i]:
        st.image(recommended_posters[i], use_container_width=True)
        st.caption(recommended_movies[i])

# ---------------- SIDEBAR: TRENDING ----------------
with st.sidebar:
    st.subheader("🔥 Trending Movies")

    trending_movies = movies['title'].head(5).tolist()

    for m in trending_movies:
        poster = fetch_poster(m)
        st.image(poster, use_container_width=True)
        st.caption(m)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🚀 Built with ML + Streamlit By Bhargav😉.... ")