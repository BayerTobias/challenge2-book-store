from rest_framework import serializers
from .models import Book
from users.serializers import CustomUserSerializer


class BookSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("author",)
