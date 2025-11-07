# relationship_app/urls.py
from django.urls import path
from . import views
from .views import list_books
from django.urls import path
from .import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view URL pattern
    path('books/', views.list_books, name='list_books'),
    
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    
    # Class-based view URL pattern
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
     # Authentication URL patterns
    path('register/', views.register_view, name='register'),
    path('login/', views.LoginView.as_view(template_name="login")),
    path('logout/', views.LogoutView.as_view(template_name="logout")),
    path('admin-view/', views.admin_view, name='Admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
