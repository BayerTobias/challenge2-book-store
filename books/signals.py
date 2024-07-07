from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Book
import os


@receiver(post_delete, sender=Book)
def book_post_delete(sender, instance, **kwargs):
    """
    Signal handler for deleting a Book instance.

    This function is called after a Book instance is deleted. It checks if the
    instance has a cover image associated with it and deletes the image file from
    the filesystem if it exists.

    Args:
    - sender: The model class that sent the signal (Book in this case).
    - instance: The actual instance of the Book model that was deleted.
    - **kwargs: Additional keyword arguments.
    """

    if instance.cover_image:
        os.remove(instance.cover_image.path)
