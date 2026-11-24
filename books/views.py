from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Book


class NewBookForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    author = forms.CharField(label="Author", max_length=64)
    genre = forms.CharField(label="Genre", max_length=64)
    year = forms.IntegerField(label="Year", min_value=0)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=False)


def index(request):
    # if the user is not logged in send him to the login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "books/index.html", {
        "books": Book.objects.all()
    })


def book(request, book_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return HttpResponseRedirect(reverse("books:index"))
    return render(request, "books/book.html", {
        "book": book,
        "reserved": request.user in book.reserved_by.all(),
        "readers": book.reserved_by.all()
    })


def reserve(request, book_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if request.method == "POST":
        book = Book.objects.get(pk=book_id)
        if request.user in book.reserved_by.all():
            book.reserved_by.remove(request.user)
        else:
            book.reserved_by.add(request.user)
    return HttpResponseRedirect(reverse("books:book", args=(book_id,)))


def add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))

    if request.method == "POST":
        form = NewBookForm(request.POST)
        if form.is_valid():
            Book.objects.create(
                title=form.cleaned_data["title"],
                author=form.cleaned_data["author"],
                genre=form.cleaned_data["genre"],
                year=form.cleaned_data["year"],
                description=form.cleaned_data["description"]
            )
            # show the user that the book was added and give him an empty form again
            return render(request, "books/add.html", {
                "form": NewBookForm(),
                "message": "The book was added successfully!"
            })
        else:
            return render(request, "books/add.html", {
                "form": form
            })

    return render(request, "books/add.html", {
        "form": NewBookForm()
    })


def update(request, book_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    book = Book.objects.get(pk=book_id)

    if request.method == "POST":
        form = NewBookForm(request.POST)
        if form.is_valid():
            book.title = form.cleaned_data["title"]
            book.author = form.cleaned_data["author"]
            book.genre = form.cleaned_data["genre"]
            book.year = form.cleaned_data["year"]
            book.description = form.cleaned_data["description"]
            book.save()
            return HttpResponseRedirect(reverse("books:book", args=(book.id,)))
        else:
            return render(request, "books/update.html", {
                "form": form,
                "book": book
            })

    # fill the form with the current data of the book
    form = NewBookForm(initial={
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "year": book.year,
        "description": book.description
    })
    return render(request, "books/update.html", {
        "form": form,
        "book": book
    })


def delete(request, book_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if request.method == "POST":
        book = Book.objects.get(pk=book_id)
        book.delete()
    return HttpResponseRedirect(reverse("books:index"))
