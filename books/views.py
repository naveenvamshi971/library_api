from django.shortcuts import render
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from .models import Book
from django.utils import timezone
from datetime import timedelta

from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class BookListView(generics.ListCreateAPIView):
    """
    List all books or create a new book.
    
    **GET** /api/books/
    - Retrieve a list of all books.
    
    **POST** /api/books/
    - Create a new book. Only admin users can create books.
    
    **Query Parameters:**
    - author (string): Filter books by author's name.
    
    **Responses:**
    - 200: A list of books.
    - 201: Book created successfully.
    - 403: Permission denied for non-admin users.
    """
    queryset = Book.objects.filter(is_archived=False)
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role == 'admin':
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to create books.")
   
    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get('author', None)
        
        if author:
            queryset = queryset.filter(author__icontains=author)  # Filter by author name

        return queryset
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({'detail': str(exc)}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)



class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a book instance.

    **GET** /api/books/{id}/
    - Retrieve a specific book by its ID. Only non-archived books can be retrieved.

    **PUT** /api/books/{id}/
    - Update an existing book. Only users with the role of 'admin' can update books.

    **DELETE** /api/books/{id}/
    - Delete a specific book by its ID. Only users with the role of 'admin' can delete books.

    **Responses:**
    - 200: Book details returned successfully (for GET).
    - 204: Book deleted successfully (for DELETE).
    - 403: Permission denied for non-admin users attempting to update or delete a book.
    - 404: Book not found.
    """
    queryset = Book.objects.filter(is_archived=False)
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user.role == 'admin':
            instance.is_archived = True  # Soft delete
            instance.save()
        else:
            raise PermissionDenied("You do not have permission to delete books.")

    def perform_update(self, serializer):
        if self.request.user.role == 'admin':
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update books.")

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({'detail': str(exc)}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)



class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create, update, or delete books.
    
    **Returns:**
    - True if the user is authenticated and has the role 'admin'.
    - False otherwise.
    
    Usage:
      This permission class can be used in views where admin-only access is required.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class BookListCreateView(generics.ListCreateAPIView):
    """
    List all books with filtering options or create a new book.

    **GET** /api/books/
    - Retrieve a list of all books with optional filtering by author or published date.

    **POST** /api/books/
    - Create a new book. Accessible to all authenticated users.

    **Query Parameters:**
    - author (string): Optional filter to return books by author's name.
    - published_date (date): Optional filter to return books published on a specific date.

    **Responses:**
    - 200: A list of books returned successfully (for GET).
    - 201: Book created successfully (for POST).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get('author', None)
        published_date = self.request.query_params.get('published_date', None)

        if author:
            queryset = queryset.filter(author__icontains=author)
        if published_date:
            queryset = queryset.filter(published_date=published_date)

        return queryset

class RecentBooksView(generics.ListAPIView):
    """
    Retrieve books published in the last 30 days.

    **GET** /api/books/recent/
    
   - Retrieve a list of recently published books that were published within the last 30 days.
   
   **Responses:**
   - 200: A list of recently published books returned successfully.
   """
   
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        return Book.objects.filter(published_date__gte=thirty_days_ago)