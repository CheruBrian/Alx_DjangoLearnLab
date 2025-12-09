from django.urls import path
from .views import RegisterAPIView, UserDetailAPIView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", obtain_auth_token, name="api_token_auth"),  # POST username & password -> token
    path("profile/<str:username>/", UserDetailAPIView.as_view(), name="profile"),
     path('follow/<int:user_id>', FollowToggleAPIView.as_view(), {'action': 'follow'}, name='follow-user'),
    path('unfollow/<int:user_id>/', FollowToggleAPIView.as_view(), {'action': 'unfollow'}, name='unfollow-user'),
]
