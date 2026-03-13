from django.shortcuts import redirect, render

from .forms import BookForm
from .models import Book


def book_list(request):
	books = Book.objects.order_by("title")
	return render(request, "books/book_list.html", {"books": books})


def book_create(request):
	if request.method == "POST":
		form = BookForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("books:book_list")
	else:
		form = BookForm()

	return render(request, "books/book_form.html", {"form": form})


def book_edit(request, pk):
	book = Book.objects.get(pk=pk)
	if request.method == "POST":
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			form.save()
			return redirect("books:book_list")
	else:
		form = BookForm(instance=book)

	return render(request, "books/book_form.html", {"form": form})
