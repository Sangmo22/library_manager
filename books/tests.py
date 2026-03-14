from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Book


class AuthFlowTests(TestCase):
	def test_signup_page_creates_user_and_logs_in(self):
		response = self.client.post(
			reverse('signup'),
			{
				'username': 'newuser',
				'email': 'newuser@example.com',
				'password1': 'StrongPassword123',
				'password2': 'StrongPassword123',
			},
		)

		self.assertRedirects(response, reverse('books:book_list'))
		self.assertTrue(User.objects.filter(username='newuser').exists())
		self.assertTrue(response.wsgi_request.user.is_authenticated)

	def test_login_page_shows_create_account_link(self):
		response = self.client.get(reverse('login'))

		self.assertContains(response, 'Create Account')
		self.assertNotContains(response, 'Back to Library')


class PublicBookAccessTests(TestCase):
	def setUp(self):
		self.book = Book.objects.create(
			title='Test Book',
			author='Test Author',
			isbn='1234567890',
		)

	def test_book_list_is_public(self):
		response = self.client.get(reverse('books:book_list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Add Book')

	def test_book_create_is_public(self):
		response = self.client.get(reverse('books:book_create'))

		self.assertEqual(response.status_code, 200)

	def test_book_detail_is_public(self):
		response = self.client.get(reverse('books:book_detail', args=[self.book.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.book.title)

	def test_book_edit_is_public(self):
		response = self.client.get(reverse('books:book_edit', args=[self.book.pk]))

		self.assertEqual(response.status_code, 200)

	def test_book_delete_is_public(self):
		response = self.client.get(reverse('books:book_delete', args=[self.book.pk]))

		self.assertEqual(response.status_code, 200)

