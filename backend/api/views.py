from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Existing views related to notes (keep if still needed)
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# New recommendation view
def get_recommendation(text):
    # Implement your recommendation logic here
    # Example: just a placeholder logic for demonstration
    return f"Recommended movie for '{text}' is 'Inception'"

@csrf_exempt
def recommend_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        recommendation = get_recommendation(text)
        return JsonResponse({'recommendation': recommendation})
    return JsonResponse({'error': 'Invalid request'}, status=400)
