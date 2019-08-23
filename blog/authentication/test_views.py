from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from .forms import SignUpForm
from .views import sign_up_view, reset_password_view
from .models import User

class TestSignUpView(TestCase):
    """
    This test only tests positive behavior, because all bad ones 
    were tested while testing the registration form.
    """

    def setUp(self):
        """
        Create data for test form.
        This data are correct.
        """
        self.sign_up_data = {
            'username' : 'tester',
            'nick' : 'testowy',
            'password1' : 'test123456',
            'password2' : 'test123456',
            'first_name' : 'John',
            'last_name' : 'Kowalski',
            'email' : 'tester@gmail.com',
            'birth_date' : date(1996, 12, 3)
        }

    def test_sign_up_view_with_correct_data(self):
        """
        Test create user and check correct fields in database.
        """
        response = self.client.post(path=reverse(viewname='authentication:sign_up'), data=self.sign_up_data)
        user = User.objects.get(nick='testowy')
        self.assertEqual(user.username, self.sign_up_data['username'])
        self.assertEqual(user.nick, self.sign_up_data['nick'])
        self.assertEqual(user.first_name, self.sign_up_data['first_name'])
        self.assertEqual(user.last_name, self.sign_up_data['last_name'])
        self.assertEqual(user.email, self.sign_up_data['email'])
        self.assertEqual(user.birth_date, self.sign_up_data['birth_date'])
        self.assertTrue(user.check_password(self.sign_up_data['password1']))

class TestResetPasswordView(TestCase):
    """
    This test only tests positive behavior, because all bad ones 
    were tested while testing the reset password form.
    """

    def setUp(self):
        """
        Create data for test form.
        This data are correct.
        """
        self.user_data = {
            'username' : 'tester',
            'nick' : 'testowy',
            'password1' : 'test123456',
            'password2' : 'test123456',
            'first_name' : 'John',
            'last_name' : 'Kowalski',
            'email' : 'przemyslaw.rozycki@smcebi.edu.pl',
            'birth_date' : date(1996, 12, 3)
        }
        self.change_password_data = {
            'username' : self.user_data['username'],
            'email' : self.user_data['email']
        }
        form = SignUpForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        form.save()

    def test_reset_password_view_with_correct_data(self):
        """
        Test check validation with correct data 
        Test checks if the old password has been replaced by a new password.
        """
        response = self.client.post(path=reverse(viewname='authentication:reset_password'), data=self.change_password_data)
        user = User.objects.get(nick='testowy')
        self.assertFalse(check_password(password=self.user_data['password1'], encoded=user.password))
       
        






