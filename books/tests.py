
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, UserProfile
from django.urls import reverse

class BookListCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@example.com')

        # Create a user profile for the user
        self.user_profile = UserProfile.objects.create(user=self.user,)

        # Authenticate the client
        self.client.force_authenticate(user=self.user)

    def test_create_book(self):
        # Make a POST request to create a book
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'publication_date': '2022-01-01'
        }
        response = self.client.post('/createbooks/', data, format='json')

        # Verify that the request was successful (HTTP 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the book was created in the database
        self.assertTrue(Book.objects.filter(title='Test Book').exists())

    def test_create_book_unauthenticated(self):
        # Unauthenticate the client
        self.client.force_authenticate(user=None)

        # Make a POST request to create a book without authentication
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'publication_date': '2022-01-01'
        }
        response = self.client.post('/createbooks/', data, format='json')

        # Verify that the request was unsuccessful (HTTP 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify that the book was not created in the database
        self.assertFalse(Book.objects.filter(title='Test Book').exists())


class BookListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@example.com')

        # Create a user profile for the user
        self.user_profile = UserProfile.objects.create(user=self.user)

        # Authenticate the client
        self.client.force_authenticate(user=self.user)

        # Create some books
        self.book1 = Book.objects.create(title='Book 1', author='Author 1', isbn='1234567890', publication_date='2022-01-01', user=self.user_profile)
        self.book2 = Book.objects.create(title='Book 2', author='Author 2', isbn='0987654321', publication_date='2022-02-01', user=self.user_profile)

    def test_list_books_authenticated_with_pagination(self):
        # Make a GET request to list books while authenticated
        url = reverse('book-list')  # Assuming 'book-list' is the name of the URL pattern for BookListAPIView
        response = self.client.get(url)

        # Verify that the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the response contains paginated data
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        # Verify the structure of the paginated data
        self.assertEqual(len(response.data['results']), 1)  # Assuming two books are created in setUp

    def test_list_books_unauthenticated(self):
        # Unauthenticate the client
        self.client.force_authenticate(user=None)

        # Make a GET request to list books without authentication
        url = reverse('book-list')  # Assuming 'book-list' is the name of the URL pattern for BookListAPIView
        response = self.client.get(url)

        # Verify that the request was unsuccessful (HTTP 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class BookRetrieveUpdateDestroyAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@example.com')

        # Create a user profile for the user
        self.user_profile = UserProfile.objects.create(user=self.user)

        # Authenticate the client
        self.client.force_authenticate(user=self.user)

        # Create a book
        self.book = Book.objects.create(title='Test Book', author='Test Author', isbn='1234567890', publication_date='2022-01-01', user=self.user_profile)

    def test_delete_book_authenticated(self):
        # Make a DELETE request to delete the book while authenticated
        response = self.client.delete(f'/books/{self.book.id}/')

        # Verify that the request was successful (HTTP 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the book was deleted from the database
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_unauthenticated(self):
        # Unauthenticate the client
        self.client.force_authenticate(user=None)

        # Make a DELETE request to delete the book without authentication
        response = self.client.delete(f'/books/{self.book.id}/')

        # Verify that the request was unsuccessful (HTTP 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify that the book still exists in the database
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())


class UserRegistrationAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        # Make a POST request to register a new user
        data = {'username': 'testuser', 'email': 'test@example.com'}
        response = self.client.post('/user/', data, format='json')

        # Verify that the request was successful (HTTP 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the user was created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Verify that the user profile was created in the database
        user = User.objects.get(username='testuser')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

        # Verify that a token was generated for the user
        self.assertIn('token', response.data)

    def test_duplicate_username(self):
        # Create a user with the same username
        User.objects.create(username='existinguser', email='existing@example.com')

        # Make a POST request to register a new user with the same username
        data = {'username': 'existinguser', 'email': 'newuser@example.com'}
        response = self.client.post('/user/', data, format='json')

        # Verify that the request was unsuccessful (HTTP 400 Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Username already exists')

    def test_duplicate_email(self):
        # Create a user with the same email
        User.objects.create(username='newuser', email='existing@example.com')

        # Make a POST request to register a new user with the same email
        data = {'username': 'newuser', 'email': 'existing@example.com'}
        response = self.client.post('/user/', data, format='json')

        # Verify that the request was unsuccessful (HTTP 400 Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email already exists')
    

