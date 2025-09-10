from django.db import models
from books.models import Book

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, blank=True, related_name='libraries')

    def __str__(self):
        return self.name
