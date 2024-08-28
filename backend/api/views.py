import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
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
data = pd.read_csv('detailed_movies.csv')

# Content Based Filtering
content_df = data[['title', 'genres', 'adult', 'overview', 
                   'popularity', 'vote_average', 'runtime']]

# Process genres and create a content-based filtering matrix
processed_genres = []

for genres in content_df['genres']:
    genre_list = eval(genres)
    genre_names = ''
    for genre in genre_list:
        if genre_names:
            genre_names += ' '
        genre_names += genre['name']
    processed_genres.append(genre_names)

content_df['genres'] = processed_genres

content_df['Content'] = content_df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(content_df['Content'])

def content_based_recommendations(user_input, content_df=content_df, tfidf_matrix=tfidf_matrix):
    user_input_tfidf = tfidf_vectorizer.transform([user_input])

    cosine_sim_with_input = linear_kernel(user_input_tfidf, tfidf_matrix)

    sim_scores = list(enumerate(cosine_sim_with_input[0]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # TOP 10
    # sim_scores = sim_scores[:10]
    # movie_indices = [i[0] for i in sim_scores]

    # BEST MATCH
    best_match_index = sim_scores[0][0]

    return content_df.iloc[best_match_index]

# TOP 10 LIST SENDING TO FRONTEND
# @csrf_exempt
# def recommend_view(request):
#     if request.method == 'POST':
#         try:
#             # Parse the input from the request
#             data = json.loads(request.body)
#             user_input = data.get('text', '')

#             print(f"User input received: {user_input}")  # Debug

#             # Get recommendations
#             recommended_movies = content_based_recommendations(user_input)

#             print(f"Recommended movies: {recommended_movies[['title', 'genres', 'vote_average', 'overview']]}")  # Debug

#             # Prepare the response data
#             response_data = recommended_movies[['title', 'genres', 'vote_average', 'overview']].to_dict(orient='records')

#             return JsonResponse({'recommendations': response_data}, status=200)
#         except Exception as e:
#             print(f"Error: {str(e)}")  # Debug
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def recommend_view(request):
    if request.method == 'POST':
        try:
            # Parse the input from the request
            data = json.loads(request.body)
            user_input = data.get('text', '')

            print(f"User input received: {user_input}")  # Debug

            # Get the top recommendation
            recommended_movie = content_based_recommendations(user_input)

            print(f"Recommended movie: {recommended_movie[['title', 'genres', 'vote_average', 'overview']]}")  # Debug

            # Format the response as a few sentences
            response_text = (
                f"I recommend you watch '{recommended_movie['title']}'. "
                f"It's a {recommended_movie['genres']} movie with a rating of {recommended_movie['vote_average']}/10. "
                f"Here’s a brief overview: {recommended_movie['overview']}"
            )

            return JsonResponse({'recommendation': response_text}, status=200)
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
