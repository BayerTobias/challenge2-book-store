from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    CustomUserSerializer class for serializing and deserializing CustomUser instances.

    This serializer handles the serialization of CustomUser model data,
    including fields such as 'id', 'username', 'email', 'password', and 'author_pseudonym'.
    It ensures that the 'password' field is write-only.

    Methods:
    - create: Creates a new CustomUser instance with hashed password.
    """

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "author_pseudonym"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Creates a new CustomUser instance.

        This method overrides the default create method to ensure that
        the password is hashed before saving the user instance.

        Args:
        - validated_data: Dictionary containing the validated data for the user.

        Returns:
        - CustomUser: The newly created CustomUser instance.
        """

        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            author_pseudonym=validated_data["author_pseudonym"],
        )
        return user
