from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=64)
    genre = models.CharField(max_length=64)
    year = models.IntegerField()
    description = models.TextField(blank=True)

    # many to many: one user can reserve many books, one book can be reserved by many users
    reserved_by = models.ManyToManyField(User, blank=True, related_name="reserved_books")

    def __str__(self):
        return f"{self.title} by {self.author}"
