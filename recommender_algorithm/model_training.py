import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import joblib  # For saving and loading precomputed embeddings

# Load the data
df = pd.read_csv('detailed_movies.csv')

# Preprocess the Data
df['overview'] = df['overview'].fillna('')
df['genres'] = df['genres'].fillna('')
df['content'] = df['overview'] + ' ' + df['genres']

# Sentence-BERT Model
model = SentenceTransformer('all-mpnet-base-v2')

# Precompute and save embeddings (do this once)
def precompute_embeddings():
    movie_embeddings = model.encode(df['content'].tolist(), convert_to_tensor=True)
    joblib.dump(movie_embeddings, 'all-mpnet-base-v2_movie_embeddings.pkl')

# Uncomment the line below to run this once to save the embeddings
# precompute_embeddings()

# Load precomputed embeddings
movie_embeddings = joblib.load('all-mpnet-base-v2_movie_embeddings.pkl')

def get_content_based_recommendations(user_input, top_n=5):
    # Encode user input
    user_input_embedding = model.encode(user_input, convert_to_tensor=True)
    
    # Compute cosine similarity
    cosine_sim = util.pytorch_cos_sim(user_input_embedding, movie_embeddings)
    
    # Get top N recommendations
    top_indices = cosine_sim.argsort(descending=True).squeeze()[:top_n]
    
    return df.iloc[top_indices][['title']]

# Collaborative Filtering using 'vote_average' and 'vote_count'
df['rating_score'] = df['vote_average'] * df['vote_count']
df['normalized_rating'] = (df['rating_score'] - df['rating_score'].min()) / (df['rating_score'].max() - df['rating_score'].min())

def get_hybrid_recommendations(user_input, top_n=5):
    # Content-based recommendations
    content_recommendations = get_content_based_recommendations(user_input, top_n)
    
    # Merge with collaborative filtering (normalized rating score)
    recommendations = content_recommendations.merge(df[['title', 'normalized_rating']], on='title', how='left')
    
    # Compute a more refined combined score
    content_weight = 0.7
    collaborative_weight = 0.3
    recommendations['combined_score'] = (
        content_weight * (recommendations.index / top_n) + 
        collaborative_weight * recommendations['normalized_rating']
    )
    
    # Rank the combined scores and return the top N movies
    final_recommendations = recommendations.sort_values(by='combined_score', ascending=False).head(top_n)
    
    return final_recommendations[['title', 'combined_score']]

# Generate Recommendations
user_input = input("Enter Movie Descriptions: ")
recommendations = get_hybrid_recommendations(user_input, top_n=5)

print("Top Recommendations with Combined Scores:")
print(recommendations)
