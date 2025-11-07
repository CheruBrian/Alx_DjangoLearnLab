# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# --- Add Book ---
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        publication_year = request.POST.get('year')

        # Create or get the author
        author, _ = Author.objects.get_or_create(name=author_name)

        # Create book
        Book.objects.create(title=title, author=author, publication_year=publication_year)
        return redirect('book_list')

    return render(request, 'add_book.html')


# --- Edit Book ---
@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.publication_year = request.POST.get('year')
        book.save()
        return redirect('book_list')

    return render(request, 'edit_book.html', {'book': book})


# --- Delete Book ---
@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')


# --- List Books (no permission required) ---
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')
    
class UserCreationForm(request):
    model = UserCreationForm()
    template_name = 'relationship_app/register.html'
    
# Role checking functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html')


# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')


# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')