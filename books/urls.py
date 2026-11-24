from django.urls import path

from . import views

app_name = "books"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("<int:book_id>", views.book, name="book"),
    path("<int:book_id>/reserve", views.reserve, name="reserve"),
    path("<int:book_id>/update", views.update, name="update"),
    path("<int:book_id>/delete", views.delete, name="delete"),
]
