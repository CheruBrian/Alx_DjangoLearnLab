from django.core.management.base import BaseCommand
from api.models import Author, Book
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seeds the database with sample authors and books'

    def handle(self, *args, **options):
        # Clear existing data
        Book.objects.all().delete()
        Author.objects.all().delete()

        # Create authors
        authors_data = [
            {'name': 'J.K. Rowling'},
            {'name': 'George R.R. Martin'},
            {'name': 'Jane Austen'},
            {'name': 'Ernest Hemingway'},
        ]
        
        authors = []
        for author_data in authors_data:
            author = Author.objects.create(**author_data)
            authors.append(author)
            self.stdout.write(
                self.style.SUCCESS(f'Created author: {author.name}')
            )

        # Create books
        books_data = [
            {'title': 'Harry Potter and the Philosopher\'s Stone', 'publication_year': 1997, 'author': authors[0]},
            {'title': 'Harry Potter and the Chamber of Secrets', 'publication_year': 1998, 'author': authors[0]},
            {'title': 'A Game of Thrones', 'publication_year': 1996, 'author': authors[1]},
            {'title': 'A Clash of Kings', 'publication_year': 1998, 'author': authors[1]},
            {'title': 'Pride and Prejudice', 'publication_year': 1813, 'author': authors[2]},
            {'title': 'Sense and Sensibility', 'publication_year': 1811, 'author': authors[2]},
            {'title': 'The Old Man and the Sea', 'publication_year': 1952, 'author': authors[3]},
            {'title': 'A Farewell to Arms', 'publication_year': 1929, 'author': authors[3]},
        ]
        
        for book_data in books_data:
            book = Book.objects.create(**book_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created book: "{book.title}" by {book.author.name}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data!')
        )