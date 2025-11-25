from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# Serializes a Book model.
class BookSerializer(serializers.ModelSerializer):

    # Custom validation: publication year cannot be in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


# Serializes an Author model with nested books.
class AuthorSerializer(serializers.ModelSerializer):

    # Nested serializer -> shows all related books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
