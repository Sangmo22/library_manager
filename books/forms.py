from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "published_date", "available"]
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}),
        }
        help_texts = {
            "isbn": "Use 10 or 13 digits only.",
        }

    def clean_isbn(self):
        isbn = self.cleaned_data["isbn"].replace("-", "").replace(" ", "")
        if not isbn.isdigit():
            raise forms.ValidationError(
                "ISBN must use digits only and be 10 or 13 digits long."
            )
        if len(isbn) not in {10, 13}:
            raise forms.ValidationError("ISBN must be exactly 10 or 13 digits long.")

        existing_books = Book.objects.filter(isbn=isbn)
        if self.instance.pk:
            existing_books = existing_books.exclude(pk=self.instance.pk)
        if existing_books.exists():
            raise forms.ValidationError("A book with this ISBN already exists.")

        return isbn


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
