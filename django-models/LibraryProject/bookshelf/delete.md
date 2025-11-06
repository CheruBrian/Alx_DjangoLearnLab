from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())

# Output: <QuerySet []>  # means all books deleted