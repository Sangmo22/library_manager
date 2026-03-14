from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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

