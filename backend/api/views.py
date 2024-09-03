import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer, util
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# Load the detailed movies CSV file
df = pd.read_csv('detailed_movies.csv')

# Preprocess the Data
df['overview'] = df['overview'].fillna('')
df['genres'] = df['genres'].fillna('')
df['content'] = df['overview'] + ' ' + df['genres']

# Load precomputed embeddings
movie_embeddings = joblib.load('all-mpnet-base-v2_movie_embeddings.pkl')

# Sentence-BERT Model
model = SentenceTransformer('all-mpnet-base-v2')

def get_hybrid_recommendations(user_input, top_n=5):
    # Encode user input
    user_input_embedding = model.encode(user_input, convert_to_tensor=True)
    
    # Compute cosine similarity
    cosine_sim = util.pytorch_cos_sim(user_input_embedding, movie_embeddings)
    
    # Get top N recommendations
    top_indices = cosine_sim.argsort(descending=True).squeeze()[:top_n]
    
    # Collaborative Filtering using 'vote_average' and 'vote_count'
    df['rating_score'] = df['vote_average'] * df['vote_count']
    df['normalized_rating'] = (df['rating_score'] - df['rating_score'].min()) / (df['rating_score'].max() - df['rating_score'].min())

    # Content-based recommendations
    content_recommendations = df.iloc[top_indices][['title', 'genres', 'vote_average', 'overview']]

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
    
    # Ensure we are returning the necessary columns
    return final_recommendations[['title', 'genres', 'vote_average', 'overview', 'combined_score']]


@csrf_exempt
def recommend_view(request):
    if request.method == 'POST':
        try:
            # Parse the input from the request
            data = json.loads(request.body)
            user_input = data.get('text', '')

            print(f"User input received: {user_input}")  # Debug
            
            # Get the top recommendations
            recommended_movies = get_hybrid_recommendations(user_input, top_n=3)  # Get only the top recommendation

            # Extract the top recommendation
            top_movie = recommended_movies.iloc[0]  # Extract the first (and only) recommendation
            
            # Parse the genres field to extract only the genre names
            genre_list = eval(top_movie['genres'])  # Convert the string representation of list to an actual list
            genre_names = ', '.join([genre['name'] for genre in genre_list])  # Extract the names and join them

            second_movie_title = recommended_movies.iloc[1]['title']  # Get the 2nd best movie title
            third_movie_title = recommended_movies.iloc[2]['title']  # Get the 3rd best movie title


            # Format the response as a paragraph
            response_text = (
                f"I recommend you watch '{top_movie['title']}'. "
                f"It's a {genre_names} movie with a rating of {top_movie['vote_average']}/10.\n"
                f"Here’s a brief overview: {top_movie['overview']}\n"
                f"Other movies you might like are: '{second_movie_title}' and '{third_movie_title}'."
            )

            print(response_text)  # Debug

            return JsonResponse({'recommendation': response_text}, status=200)
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

