import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load movies data
movies = pickle.load(open('movies.pkl','rb'))

# Convert to DataFrame
movies = pd.DataFrame(movies)

# TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=5000)
vectors = tfidf.fit_transform(movies['tags']).toarray()

# Cosine similarity
similarity = cosine_similarity(vectors)

# Save similarity file
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Similarity file created successfully!")