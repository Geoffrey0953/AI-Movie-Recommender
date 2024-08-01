import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

'''
NECESSARY INFORMATION: 
adult, genres, title, overview, popularity, vote_average, runtime
Ranked in terms of relevancy, highest rated
Filters: Highest rated, closest match in terms of description, Adult, Horror
Maybe implement a sublist for that genre recommended
'''

# Load the detailed movies CSV file
data = pd.read_csv('detailed_movies.csv')

# Content Based Filtering
content_df = data[['title', 'genres', 'adult', 'overview', 
                   'popularity', 'vote_average', 'runtime']]

# Initialize an empty list to store the processed genres
processed_genres = []

# Convert genres (list of dictionaries) to a string
for genres in content_df['genres']:
    genre_list = eval(genres)
    genre_names = ''
    for genre in genre_list:
        if genre_names:
            genre_names += ' '
        genre_names += genre['name']
    processed_genres.append(genre_names)

# Assign the processed genres back to the DataFrame
content_df.loc[:, 'genres'] = processed_genres

# Combine multiple features into a single 'Content' column
content_df.loc[:, 'Content'] = content_df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

# Initialize the TFIDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the 'Content' column
tfidf_matrix = tfidf_vectorizer.fit_transform(content_df['Content'])

# Function to recommend movies based on user input (Content based)
def content_based_recommendations(user_input, content_df=content_df, tfidf_matrix=tfidf_matrix):
    user_input_tfidf = tfidf_vectorizer.transform([user_input])

    cosine_sim_with_input = linear_kernel(user_input_tfidf, tfidf_matrix)

    sim_scores = list(enumerate(cosine_sim_with_input[0]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[:10]
    
    movie_indices = [i[0] for i in sim_scores]
    
    return content_df.iloc[movie_indices]

# Example usage with user's input
user_input = input()
recommended_movies = content_based_recommendations(user_input)

# Print the recommended movies
print(recommended_movies[['title', 'genres', 'vote_average', 'overview']])


# Implement Collaborative Filtering
# Hybrid recommender system with Content based and Collaborative 
# For Content Based Filtering, do not include title when looking for movies. Use purely the overview. 