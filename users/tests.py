from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser


# Create your tests here.
class UserTests(APITestCase):

    def test_create_custom_user_view(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser1",
                "password": "Testpassword",
                "email": "test@test.de",
                "author_pseudonym": "testpseudonym",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomUser.objects.count(), 1)
