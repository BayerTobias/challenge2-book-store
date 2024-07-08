from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import BookSerializer
from .models import Book
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from .permissions import IsNotDathVader


class BookListView(APIView):
    """
    API view for listed books.

    This view supports GET requests to list all books or filter books based on a search query.

    Attributes:
    - permission_classes: List of permission classes allowed to access this view (AllowAny in this case).
    - renderer_classes: List of renderer classes to render the response in JSON or XML format.

    Methods:
    - get(self, request): Retrieves a list of books or filtered books based on search query.
    """

    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, XMLRenderer]

    def get(self, request):
        """
        GET method for retrieving a list of books.

        This method retrieves all books or filters books based on the 'search' query parameter.
        - If 'search' query parameter is provided, it filters books by title or description.
        - If no 'search' query parameter is provided, it retrieves all books.

        Args:
        - request: The HTTP request object.

        Returns:
        - Response: A JSON or XML response containing serialized book data.
        """

        books = Book.objects.all()
        search_query = request.query_params.get("search", None)
        if search_query:
            filterd_books = books.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
            )
            serializer = BookSerializer(filterd_books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class BookDetailView(APIView):
    """
    API view for retrieving details of a book.

    This view supports GET requests to retrieve details of a specific book identified by its ID.

    Attributes:
    - permission_classes: List of permission classes allowed to access this view (AllowAny in this case).

    Methods:
    - get(self, request, book_id): Retrieves details of a book identified by its ID.
    """

    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, XMLRenderer]

    def get(self, request, book_id):
        """
        GET method for retrieving details of a book.

        This method retrieves details of a specific book identified by its ID.

        Args:
        - request: The HTTP request object.
        - book_id: The ID of the book to retrieve.

        Returns:
        - Response: A JSON response containing serialized book data.
        """

        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageUserBooksView(APIView):
    """
    API view for managing books of the authenticated user.

    This view supports GET, POST, PATCH, and DELETE methods for managing books.
    The view requires the user to be authenticated with JWT authentication.

    Attributes:
    - permission_classes: List of permission classes allowed to access this view (IsNotDathVader in this case).

    Methods:
    - get(self, request): Retrieves books authored by the authenticated user.
    - post(self, request): Creates a new book entry for the authenticated user.
    - patch(self, request, book_id): Updates details of a book authored by the authenticated user.
    - delete(self, request, book_id): Deletes a book authored by the authenticated user.
    """

    permission_classes = [IsNotDathVader]
    renderer_classes = [JSONRenderer, XMLRenderer]

    def get(self, request):
        """
        GET method for retrieving books authored by the authenticated user.

        This method retrieves books filtered by the authenticated user as author.

        Args:
        - request: The HTTP request object.

        Returns:
        - Response: A JSON response containing serialized book data.
        """

        books = Book.objects.filter(author=request.user)
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        POST method for creating a new book entry for the authenticated user.

        This method creates a new book entry with the authenticated user as author.

        Args:
        - request: The HTTP request object containing book data.

        Returns:
        - Response: A JSON response containing serialized book data if successful, or errors if validation fails.
        """

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, book_id):
        """
        PATCH method for updating details of a book authored by the authenticated user.

        This method updates details of a specific book identified by its ID,
        authored by the authenticated user.

        Args:
        - request: The HTTP request object containing updated book data.
        - book_id: The ID of the book to update.

        Returns:
        - Response: A JSON response containing updated serialized book data if successful,
                    or errors if validation fails or book not found.
        """

        book = get_object_or_404(Book, pk=book_id, author=request.user)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        """
        DELETE method for deleting a book authored by the authenticated user.

        This method deletes a specific book identified by its ID, authored by the authenticated user.

        Args:
        - request: The HTTP request object.
        - book_id: The ID of the book to delete.

        Returns:
        - Response: A JSON response indicating successful deletion of the book.
        """

        book = get_object_or_404(Book, pk=book_id, author=request.user)
        if book:
            book.delete()
            return Response(
                {"message": "Book deleted."}, status=status.HTTP_204_NO_CONTENT
            )
