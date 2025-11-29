from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
#from django_filters import rest_framework
    

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [ DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    ordering_fields = ['publication_year', 'title']
    # Filtering fields
    filterset_fields = ['title', 'publication_year', 'author']
    # Search fields (text match)
    search_fields = ['title', 'author__name']
    # Ordering fields (sorting)
    ordering_fields = ['title', 'publication_year']
    # Default ordering (optional)
    ordering = ['title']

    permission_classes = [AllowAny]
    def get_queryset(self):
        # Optional custom filtering
        return Book.objects.filter(publication_year__lte=2025)



class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single Book instance by its primary key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        """
        Custom logic when a book is created.
        Could log events, enforce constraints, etc.
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  



class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]