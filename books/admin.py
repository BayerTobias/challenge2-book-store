from django.contrib import admin
from .models import Book


# Register your models here.
class Book_Admin(admin.ModelAdmin):
    list_display = ("id", "title", "price")
    list_display_links = ("id", "title", "price")


admin.site.register(Book, Book_Admin)
