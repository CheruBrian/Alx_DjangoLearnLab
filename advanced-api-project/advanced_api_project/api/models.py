from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores basic information about authors and establishes
    a one-to-many relationship with the Book model, where one author
    can have multiple books.
    """
    name = models.CharField(
        max_length=200,
        help_text="Full name of the author"
    )
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model representing a published book.
    
    This model stores book information and maintains a foreign key
    relationship with the Author model. Each book is associated with
    one author, but an author can have multiple books.
    """
    title = models.CharField(
        max_length=300,
        help_text="Title of the book"
    )
    publication_year = models.IntegerField(
        help_text="Year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',  # Enables author.books reverse relationship
        help_text="Author who wrote this book"
    )
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']
        # Ensure unique constraint for book titles per author
        unique_together = ['title', 'author']
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"