from django.db import models
from users.models import CustomUser


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=250)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="books"
    )
    cover_image = models.FileField(upload_to="cover_images/", null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
