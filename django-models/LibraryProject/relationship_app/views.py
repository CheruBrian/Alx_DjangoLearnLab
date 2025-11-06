from django.views.generic import DetailView
from .models import Library

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app'
    context_object_name = 'list_books.html', 'Book.objects.all()'
