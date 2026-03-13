from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import BookForm
from .models import Book


def book_list(request):
	query = request.GET.get("q", "").strip()
	books = Book.objects.order_by("title")
	if query:
		books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
	paginator = Paginator(books, 5)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	return render(
		request,
		"books/book_list.html",
		{"books": page_obj, "page_obj": page_obj, "query": query},
	)


def book_create(request):
	if request.method == "POST":
		form = BookForm(request.POST)
		if form.is_valid():
			book = form.save()
			messages.success(request, f'"{book.title}" was added successfully.')
			return redirect("books:book_list")
	else:
		form = BookForm()

	return render(request, "books/book_form.html", {"form": form})


def book_edit(request, pk):
	book = Book.objects.get(pk=pk)
	if request.method == "POST":
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			book = form.save()
			messages.success(request, f'"{book.title}" was updated successfully.')
			return redirect("books:book_list")
	else:
		form = BookForm(instance=book)

	return render(request, "books/book_form.html", {"form": form})


def book_delete(request, pk):
	book = Book.objects.get(pk=pk)
	if request.method == "POST":
		title = book.title
		book.delete()
		messages.success(request, f'"{title}" was deleted successfully.')
		return redirect("books:book_list")
	return render(request, "books/book_confirm_delete.html", {"book": book})


def book_detail(request, pk):
	book = Book.objects.get(pk=pk)
	return render(request, "books/book_detail.html", {"book": book})
