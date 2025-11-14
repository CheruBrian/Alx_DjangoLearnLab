from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

# View to list all books — requires "can_view" permission
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})
