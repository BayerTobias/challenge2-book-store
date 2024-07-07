from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from .models import Book
from rest_framework_simplejwt.tokens import RefreshToken


class BookTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username="testuser1",
            email="testuser1@example.com",
            password="Testpassword",
            author_pseudonym="testpseudonym",
        )

        self.user2 = CustomUser.objects.create(
            username="testuser2",
            email="testuser2@example.com",
            password="Testpassword",
            author_pseudonym="test2pseudonym",
        )

        self.vader = CustomUser.objects.create_user(
            username="darthvader",
            email="darthvader@example.com",
            password="Testpassword",
            author_pseudonym="SithLord",
        )

        self.book1 = Book.objects.create(
            title="Book One",
            description="Description for book one",
            author=self.user,
            price="10.00",
        )

        self.book2 = Book.objects.create(
            title="Book Two",
            description="Description for book two",
            author=self.user,
            price="15.00",
        )

        self.book3 = Book.objects.create(
            title="Book Three",
            description="Description for book three",
            author=self.user2,
            price="20.00",
        )

        self.user_token = self.get_token_for_user(self.user)
        self.vader_token = self.get_token_for_user(self.vader)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

    def test_get_unfiltert_books_list_view(self):
        response = self.client.get(reverse("books_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_get_filterd_books_list_view(self):
        response = self.client.get(reverse("books_list"), {"search": "Book One"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book One")

    def test_get_detail_book_view(self):
        response = self.client.get(reverse("books_details", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Book One")

    def test_get_detail_book_view_with_wrong_id(self):
        response = self.client.get(reverse("books_details", args=[4]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "No Book matches the given query.")

    def test_get_all_books_of_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_token["access"]
        )
        response = self.client.get(reverse("auth_books"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_all_books_of_user_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "WrongToken123")
        response = self.client.get(reverse("auth_books"))
        self.assertEqual(response.status_code, 401)

    def test_vader_tryes_to_access_get(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.vader_token["access"]
        )
        response = self.client.get(reverse("auth_books"))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "Even the dark side has limits, Darth. You can't publish on Wookiee books!",
        )

    def test_user_post_to_auth_books_view(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_token["access"]
        )
        data = {
            "title": "Test Book",
            "description": "This is a test book",
            "price": "19.99",
        }
        response = self.client.post(reverse("auth_books"), data)
        self.assertEqual(response.status_code, 201)

    def test_vader_tryes_to_publish(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.vader_token["access"]
        )
        data = {
            "title": "Vader Book",
            "description": "This is a Vader test book",
            "price": "99.99",
        }
        response = self.client.post(reverse("auth_books"), data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "Even the dark side has limits, Darth. You can't publish on Wookiee books!",
        )

    def test_user_patch_to_auth_books_view(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_token["access"]
        )
        data = {
            "title": "Patched Book",
            "description": "This is a Patched book",
            "price": "19.99",
        }

        response = self.client.patch(
            reverse("auth_books_details", args=[self.book1.pk]), data
        )
        self.assertEqual(response.status_code, 200)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Patched Book")

    def test_user_tryes_to_patch_user2s_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_token["access"]
        )
        data = {
            "title": "Patched Book",
            "description": "This is a Patched book",
            "price": "19.99",
        }

        response = self.client.patch(
            reverse("auth_books_details", args=[self.book3.pk]), data
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "No Book matches the given query.")

    def test_user_delete_to_auth_books_view(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_token["access"]
        )
        response = self.client.delete(
            reverse("auth_books_details", args=[self.book1.pk])
        )
        self.assertEqual(response.status_code, 204)

    def test_user_tryes_to_delete_user2s_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_token["access"]
        )
        data = {
            "title": "Patched Book",
            "description": "This is a Patched book",
            "price": "19.99",
        }

        response = self.client.delete(
            reverse("auth_books_details", args=[self.book3.pk]), data
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "No Book matches the given query.")
