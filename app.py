import streamlit as st
import requests
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender ", layout="wide")

movies = pickle.load(open("movies.pkl", "rb"))
api_key = st.secrets["OMDB_API_KEY"]


@st.cache_resource
def create_similarity():
    tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
    vectors = tfidf.fit_transform(movies["tags"])
    similarity = cosine_similarity(vectors)
    return similarity


similarity = create_similarity()


def fetch_poster(movie_name):
    try:
        url = f"https://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
        data = requests.get(url).json()

        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
    except Exception:
        pass

    return "https://via.placeholder.com/300x450?text=No+Image"


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

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


st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a Movie",
    movies["title"].values
)

recommended_movies, recommended_posters = recommend(selected_movie)

cols = st.columns(5)

for i in range(5):
    with cols[i]:
        st.image(recommended_posters[i], use_container_width=True)
        st.caption(recommended_movies[i])

st.markdown("---")
st.markdown("🚀 Built with ML + Streamlit By Bhargav😉....")