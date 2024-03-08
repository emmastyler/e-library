from django.urls import re_path
from django.urls import path
from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView, UserRegistrationAPIView, BookListAPIView, fetch_book_details
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Docs",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('createbooks/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('listbooks/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('user/', UserRegistrationAPIView.as_view(), name='user'),
    path('fetch/', fetch_book_details, name='fetch_book_details'),
    re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
