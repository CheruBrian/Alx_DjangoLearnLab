from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            data = UserSerializer(user).data
            data["token"] = token
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"  # get by username in URL

class FollowToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, action=None):
        """
        action is "follow" or "unfollow" (we'll route two endpoints to this view)
        """
        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == target:
            return Response({"detail": "You cannot follow/unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if action == "follow":
            # create relationship if not existing
            # If using Follow through model:
            request.user.following.add(target)  # works for ManyToMany
            return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)

        elif action == "unfollow":
            request.user.following.remove(target)
            return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)

        else:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)