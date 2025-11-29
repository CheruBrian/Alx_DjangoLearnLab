from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        """
        Create initial data for tests: a user, an author, and some books.
        """
        self.client = APIClient()

        # Create a user for authenticated actions
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        # Create an author
        self.author = Author.objects.create(name="Test Author")

        # Create some books
        self.book1 = Book.objects.create(
            title="Alpha Book", publication_year=2001, author=self.author
        )
        self.book2 = Book.objects.create(
            title="Beta Story", publication_year=1999, author=self.author
        )
        self.book3 = Book.objects.create(
            title="Gamma Tales", publication_year=2010, author=self.author
        )

        # URLs
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        self.update_url = lambda pk: reverse("book-update", kwargs={"pk": pk})
        self.delete_url = lambda pk: reverse("book-delete", kwargs={"pk": pk})

    # -------------------------
    #   CRUD TESTS
    # -------------------------

    def test_list_books(self):
        """Test retrieving list of books (publicly accessible)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_single_book(self):
        """Test retrieving one book by ID (publicly accessible)."""
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Alpha Book")

    def test_create_book_authenticated(self):
        """Test creating a book when authenticated."""
        self.client.login(username="testuser", password="password123")

        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author.id,
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_book_unauthenticated(self):
        """Unauthenticated users should NOT be able to create a book."""
        data = {
            "title": "Fail Book",
            "publication_year": 2020,
            "author": self.author.id,
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_update_book_authenticated(self):
        """Authenticated user can update a book."""
        self.client.login(username="testuser", password="password123")

        data = {"title": "Updated Title"}
        response = self.client.patch(self.update_url(self.book1.id), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_update_book_unauthenticated(self):
        """Unauthenticated user should not update a book."""
        data = {"title": "Should Not Update"}
        response = self.client.patch(self.update_url(self.book1.id), data, format="json")
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book."""
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book_unauthenticated(self):
        """Unauthenticated user should not delete a book."""
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    # -------------------------
    #   FILTERING TESTS
    # -------------------------

    def test_filter_by_title(self):
        response = self.client.get(f"{self.list_url}?title=Alpha Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Alpha Book")

    def test_filter_by_publication_year(self):
        response = self.client.get(f"{self.list_url}?publication_year=1999")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["publication_year"], 1999)

    # -------------------------
    #   SEARCH TESTS
    # -------------------------

    def test_search_by_title(self):
        response = self.client.get(f"{self.list_url}?search=Gamma")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Gamma Tales")

    def test_search_by_author_name(self):
        response = self.client.get(f"{self.list_url}?search=Test Author")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    # -------------------------
    #   ORDERING TESTS
    # -------------------------

    def test_ordering_by_title_ascending(self):
        response = self.client.get(f"{self.list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_publication_year_desc(self):
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))