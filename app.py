# import streamlit as st
# import pickle
# import pandas as pd
# import requests


# # ---------------- FETCH POSTER ---------------- #

# import requests
# import time

# def fetch_poster(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bf7752c471b2eb9b27442d3d80a077fc&language=en-US"
        
#         response = requests.get(url, timeout=10)
#         data = response.json()

#         time.sleep(0.2)   # 👈 small delay (important)

#         poster_path = data.get('poster_path')

#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500" + poster_path
#         else:
#             return "https://via.placeholder.com/500x750?text=No+Poster"

#     except Exception as e:
#         print("Error:", e)
#         return "https://via.placeholder.com/500x750?text=Error"

# # ---------------- RECOMMEND FUNCTION ---------------- #


# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]

#     movies_list = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )

#     recommended_movies = []
#     recommended_posters = []

#     for i in movies_list:
#         if len(recommended_movies) == 5:
#             break

#         movie_id = movies.iloc[i[0]].movie_id
#         title = movies.iloc[i[0]].title

#         poster = fetch_poster(movie_id)

#         # only add if valid poster
#         if "No+Poster" not in poster and "Error" not in poster:
#             recommended_movies.append(title)
#             recommended_posters.append(poster)

#     return recommended_movies, recommended_posters


# # ---------------- LOAD DATA ---------------- #

# movies_dict = pickle.load(open('movies.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)

# similarity = pickle.load(open('similarity.pkl', 'rb'))


# # ---------------- STREAMLIT UI ---------------- #

# st.title("🎬 Movie Recommender System")

# selected_movie_name = st.selectbox(
#     "Select a movie",
#     movies['title'].values
# )

# if st.button("Recommend"):

#     names, posters = recommend(selected_movie_name)

#     col1, col2, col3, col4, col5 = st.columns(5)
#     cols = [col1, col2, col3, col4, col5]

#     for idx in range(5):
#         with cols[idx]:
#             st.text(names[idx])
#             st.image(posters[idx])


import streamlit as st
import pickle
import pandas as pd
import requests
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- FETCH POSTER ---------------- #

API_KEY = "bf7752c471b2eb9b27442d3d80a077fc"

@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bf7752c471b2eb9b27442d3d80a077fc&language=en-US"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750.png?text=API+Error"

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster"

    except:
        return "https://via.placeholder.com/500x750.png?text=Error"

# ---------------- LOAD DATA ---------------- #

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


# ---------------- CREATE SIMILARITY (NO PKL NEEDED) ---------------- #

@st.cache_data
def create_similarity(data):
    tfidf = TfidfVectorizer(max_features=3000)
    vectors = tfidf.fit_transform(data['tags']).toarray()
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix

similarity = create_similarity(movies)


# ---------------- RECOMMEND FUNCTION ---------------- #

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]   # 👈 skip selected movie

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title

        poster = fetch_poster(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters


# ---------------- STREAMLIT UI ---------------- #

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.text(names[idx])
            st.image(posters[idx])