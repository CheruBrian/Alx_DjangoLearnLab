from django.db import models

class Author(models.Model):
    """
    Represents a book author.
    Each author can have multiple related Book objects.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book written by an Author.
    Links to Author via a foreign key (one-to-many).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, related_name='books', on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"