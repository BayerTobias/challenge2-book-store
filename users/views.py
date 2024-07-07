from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny


class CreateCustomUser(APIView):
    """
    CreateCustomUser class for handling user registration requests.

    This view supports the POST method for creating a new user.
    The view does not require authentication, allowing any user to register.

    Methods:
    - post: Creates a new user with the provided data.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        POST method for creating a new user.

        This method validates the provided data using CustomUserSerializer.
        If the data is valid, it saves the new user and returns the serialized user data.
        If the data is invalid, it returns the validation errors.

        Args:
        - request: The HTTP request object containing user data.

        Returns:
        - Response: A JSON response containing the serialized user data or error messages.
        """

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
