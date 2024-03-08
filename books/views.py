from books.models import Book
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from books.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination


# Create your views here.

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny

import requests
from django.http import  JsonResponse




class BookListCreateAPIView(generics.ListCreateAPIView):
     """
       Create Book

        This endpoint create books by the users.
    """
     queryset = Book.objects.all()
     serializer_class = BookSerializer
     permission_classes = [IsAuthenticated]  # Ensure user is authenticated to create books

     def post(self, request):

        """
        Post data to the server.

        This endpoint post data from the server.
        """

        # Get the authenticated user's profile
        user_profile = UserProfile.objects.get(user=request.user)

        # Add the user_profile to the book data before serializing
        book_data = request.data
        book_data['user'] = user_profile.id

        # Serialize the book data
        serializer = BookSerializer(data=book_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
#book list for specific user

class BookListAPIView(generics.ListAPIView):
    """
        Retrieve Book List from the server.

        This endpoint retrieves books list from the server.
    """
    throttle_classes = [UserRateThrottle]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    pagination_class = PageNumberPagination  # Add pagination class

    def get_queryset(self):
        # You can override this method to filter the queryset if needed
        return super().get_queryset()

    def get_serializer_context(self):
        # Include pagination information in serializer context
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'paginator': self.paginator,
            'view': self
        })
        return context

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, Update and Delete Book List, from the server.

        This endpoint retrieves, update and delete book list from the server based on autheneticated and authorized user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

#quick registration view for testing purposes
    
class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            # Check if user with the same username or email already exists
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Create User
            user = User.objects.create(username=username, email=email)
            user_profile1 = UserProfile.objects.create(user=user)
            user_profile1.save()
            # Generate token
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def fetch_book_details_from_open_library(isbn):
    url = f"https://openlibrary.org/isbn/{isbn}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors

        book_data = response.json()

        # Extract relevant book details from the response
        title = book_data.get('title', '')
        author = book_data.get('authors', [{}])[0].get('name', '') if 'authors' in book_data else ''
        publication_date = book_data.get('publish_date', '')

        return title, author, publication_date

    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., network errors)
        print(f"Error fetching book details: {e}")
        return None, None, None

def fetch_book_details(request):
    isbn = request.GET.get('isbn')

    if not isbn:
        return JsonResponse({'error': 'ISBN is required'}, status=400)

    title, author, publication_date = fetch_book_details_from_open_library(isbn)

    if title is None and author is None and publication_date is None:
        return JsonResponse({'error': 'Book details not found'}, status=404)

    data = {
        'title': title,
        'author': author,
        'publication_date': publication_date
    }
    return JsonResponse(data)


