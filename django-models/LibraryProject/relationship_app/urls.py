# relationship_app/urls.py
from django.urls import path
from . import views
from .views import list_books

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view URL pattern
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view URL pattern
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]