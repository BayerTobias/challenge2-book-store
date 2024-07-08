# Django Bookstore API

This is a RESTful API for a book management application, providing user registration, authentication, and book management functionalities. The API endpoints support viewing, creating, updating, and deleting books, as well as user registration and JWT token-based authentication.

## Pre-Created Users for Testing

You can use the following pre-created users for testing the API:

- **Username:** `testuser1`

  - **Password:** `Testpassword`

- **Username:** `darthvader`
  - **Password:** `Testpassword`

## Endpoints

### User Registration and Authentication

- **POST /signup/**

  - Register a new user.
  - Example request:
    ```json
    {
      "username": "testuser",
      "email": "testuser@example.com",
      "password": "Testpassword",
      "author_pseudonym": "testpseudonym"
    }
    ```
  - Example response:
    ```json
    {
      "id": 1,
      "username": "testuser",
      "email": "testuser@example.com",
      "author_pseudonym": "testpseudonym"
    }
    ```

- **POST /api/token/**

  - Obtain a JWT access and refresh token.
  - Example request:
    ```json
    {
      "username": "testuser",
      "password": "Testpassword"
    }
    ```
  - Example response:
    ```json
    {
      "refresh": "your_refresh_token",
      "access": "your_access_token"
    }
    ```

- **POST /api/token/refresh/**
  - Refresh a JWT access token using a refresh token.
  - Example request:
    ```json
    {
      "refresh": "your_refresh_token"
    }
    ```
  - Example response:
    ```json
    {
      "access": "your_new_access_token"
    }
    ```

### Book Management

- **GET /books/**

  - Retrieve a list of all books.
  - Optional query parameter `search` to filter books by title or description.
  - Example response:
    ```json
    [
      {
        "id": 1,
        "title": "Book One",
        "description": "Description of Book One",
        "author": {
          "id": 1,
          "username": "testuser",
          "email": "testuser@example.com",
          "author_pseudonym": "testpseudonym"
        },
        "cover_image": "url_to_cover_image",
        "price": "19.99"
      },
      ...
    ]
    ```

- **GET /books/<int:book_id>/**
  - Retrieve details of a specific book.
  - Example response:
    ```json
    {
      "id": 1,
      "title": "Book One",
      "description": "Description of Book One",
      "author": {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "author_pseudonym": "testpseudonym"
      },
      "cover_image": "url_to_cover_image",
      "price": "19.99"
    }
    ```

### Authenticated User Book Management

- **GET /user_books/**

  - Retrieve a list of books created by the authenticated user.
  - Example response:
    ```json
    [
      {
        "id": 1,
        "title": "User's Book",
        "description": "Description of User's Book",
        "author": {
          "id": 1,
          "username": "testuser",
          "email": "testuser@example.com",
          "author_pseudonym": "testpseudonym"
        },
        "cover_image": "url_to_cover_image",
        "price": "19.99"
      },
      ...
    ]
    ```

- **POST /user_books/**

  - Create a new book for the authenticated user.
  - Example request:
    ```json
    {
      "title": "New Book",
      "description": "Description of New Book",
      "price": "29.99"
    }
    ```
  - Example response:
    ```json
    {
      "id": 2,
      "title": "New Book",
      "description": "Description of New Book",
      "author": {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "author_pseudonym": "testpseudonym"
      },
      "cover_image": null,
      "price": "29.99"
    }
    ```

- **PATCH /user_books/<int:book_id>/**

  - Update an existing book created by the authenticated user.
  - Example request:
    ```json
    {
      "title": "Updated Book"
    }
    ```
  - Example response:
    ```json
    {
      "id": 1,
      "title": "Updated Book",
      "description": "Description of User's Book",
      "author": {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "author_pseudonym": "testpseudonym"
      },
      "cover_image": "url_to_cover_image",
      "price": "19.99"
    }
    ```

- **DELETE /user_books/<int:book_id>/**
  - Delete an existing book created by the authenticated user.
  - Example response:
    ```json
    {
      "message": "Book deleted."
    }
    ```

## Authentication

The API uses JSON Web Tokens (JWT) for authentication. To access protected endpoints, you must include the `Authorization` header with the JWT access token:
