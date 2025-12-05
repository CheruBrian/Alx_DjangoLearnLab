# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView, comment_reply, PostSearchView, PostsByTagView, TagCloudView, PostAdvancedSearchView
)
from .api import tag_suggestions_api

urlpatterns = [
    path("", views.home, name="home"),
    
    

    # Registration
    path("register/", views.register, name="register"),

    # Login & logout via built-in views
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),

    # Profile
    path("profile/", views.profile, name="profile"),
    
    # Post views
     path("", views.PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    
     # Post URLs
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/comments/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comment/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('comment/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Comment URLs
    path('posts/<int:post_pk>/comments/new/', 
         CommentCreateView.as_view(), 
         name='comment-create'),
    path('comments/<int:pk>/edit/', 
         CommentUpdateView.as_view(), 
         name='comment-update'),
    path('comments/<int:pk>/delete/', 
         CommentDeleteView.as_view(), 
         name='comment-delete'),
    path('comments/<int:pk>/reply/', 
         comment_reply, 
         name='comment-reply'),
    
     # Tag and Search URLs
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('search/advanced/', PostAdvancedSearchView.as_view(), name='post-search-advanced'),
    path('tags/', TagCloudView.as_view(), name='tag-cloud'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),
    
    # API URLs
    path('api/tag-suggestions/', tag_suggestions_api, name='api-tag-suggestions'),
]
