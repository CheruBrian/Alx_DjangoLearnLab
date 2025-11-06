from django.views.generic import DetailView
from .models import Library

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
