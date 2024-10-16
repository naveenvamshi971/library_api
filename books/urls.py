from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BookListView, BookListCreateView, BookDetailView, RecentBooksView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # GET (list books) & POST (create book)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # GET, PUT, DELETE for specific book
    path('books/recent/', RecentBooksView.as_view(), name='recent-books'),  # GET books published in the last 30 days
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token generation
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh

]