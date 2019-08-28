from datetime import date

from django.test import TestCase
from django.contrib.auth.hashers import check_password

from authentication.forms import PasswordResetForm, SignUpForm
from authentication.models import User

class TestSignUpForm(TestCase):

    def setUp(self):
        """
        Create data for test form.
        This data are correct.
        """
        self.form_data = {
            'username' : 'tester',
            'nick' : 'testowy',
            'password1' : 'test123456',
            'password2' : 'test123456',
            'first_name' : 'John',
            'last_name' : 'Kowalski',
            'email' : 'tester@gmail.com',
            'birth_date' : date(1996, 12, 3)
        }

    def test_form_with_correct_data(self):
        """
        Test check validation correct data and dict with clean data.
        Save data for database and check field.
        """ 
        form = SignUpForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        for key in self.form_data.keys():  
            self.assertEqual(form.cleaned_data[key], self.form_data[key])
        form.save()
        user = User.objects.get(nick='testowy')
        self.assertEqual(user.username, self.form_data['username'])
        self.assertEqual(user.nick, self.form_data['nick'])
        self.assertEqual(user.first_name, self.form_data['first_name'])
        self.assertEqual(user.last_name, self.form_data['last_name'])
        self.assertEqual(user.email, self.form_data['email'])
        self.assertEqual(user.birth_date, self.form_data['birth_date'])

    def test_form_with_bad_format_last_name_and_first_name(self):
        """
        The test checks if the first name and last name are in upper case, the rest is lower case.
        If not, the form automatically corrects to this format.
        Next test check if numbers or special symbols are in last name or first name.
        If so form validaton is False and exceptions will be raised.
        """
        self.form_data['first_name'] = 'jOhN'
        self.form_data['last_name'] = 'kOwaLski'
        form = SignUpForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], 'John')
        self.assertEqual(form.cleaned_data['last_name'], 'Kowalski')
        self.form_data['first_name'] = 'Jo1hn'
        self.form_data['last_name'] = 'Kowal!ski'
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'][0], 'String: Jo1hn must be only digits')
        self.assertEqual(form.errors['last_name'][0], 'String: Kowal!ski must be only digits')

    def test_form_with_bad_format_nick(self):
        """
        The test check if the nick has the right format (only digits and letters).
        Additional test check bad length (max = 50, min = 5)
        If not form validation is False and exceptions will be raised.
        """
        self.form_data['nick'] = 'teka!$#'
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['nick'][0], "Nick: teka!$# must be only letters and digits.")
        self.form_data['nick'] = 'ads'
        form = SignUpForm(data=self.form_data)
        self.assertEqual(form.errors['nick'][0], "Ensure this value has at least 5 characters (it has 3).")
        self.form_data['nick'] = 20 * 'ads'
        form = SignUpForm(data=self.form_data)
        self.assertEqual(form.errors['nick'][0], "Ensure this value has at most 50 characters (it has 60).")

    def test_form_with_empty_and_not_unique_nick(self):
        """
        The test check if the nick is empty or is not unique.
        If is form validation is False and exceptions will be raised.
        """
        del self.form_data['nick']
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['nick'][0], "This field is required.")
        self.form_data['nick'] = 'kasanga'
        for _ in range(2): # test with exists nick
            form = SignUpForm(data=self.form_data)
            is_valid = False
            if form.is_valid():
                is_valid = True
                form.save()
                self.assertTrue(is_valid)
            else:
                self.assertFalse(is_valid)
                self.assertEqual(form.errors['nick'][0], 'A user with that nick already exists.')

    def test_form_with_empty_and_not_unique_email(self):
        """
        The test check if the email is empty or is not unique.
        If is form validation is False and exceptions will be raised.
        """
        del self.form_data['email']
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], "This field is required.")
        self.form_data['email'] = 'kasanga@gmail.com'
        for _ in range(2): # test with exists email
            form = SignUpForm(data=self.form_data)
            is_valid = False
            if form.is_valid():
                is_valid = True
                form.save()
                self.assertTrue(is_valid)
            else:
                self.assertFalse(is_valid)
                self.assertEqual(form.errors['email'][0], 'A user with that email address already exists.')

    def test_form_with_empty_and_not_unique_username(self):
        """
        The test check if the username is empty or is not unique.
        If is form validation is False and exceptions will be raised.
        """
        del self.form_data['username']
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], "This field is required.")
        self.form_data['username'] = 'kasanga'
        for _ in range(2): # test with exists username
            form = SignUpForm(data=self.form_data)
            is_valid = False
            if form.is_valid():
                is_valid = True
                form.save()
                self.assertTrue(is_valid)
            else:
                self.assertFalse(is_valid)
                self.assertEqual(form.errors['username'][0], 'A user with that username already exists.')

    def test_form_with_empty_last_name_and_first_name(self):
        """
        The test check if the last name and first name is empty,
        if are form validation is False and exceptions will be raised.
        """
        del self.form_data['first_name']
        del self.form_data['last_name']
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'][0], "This field is required.")
        self.assertEqual(form.errors['last_name'][0], "This field is required.")

class TestPasswordResetForm(TestCase):

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
        self.user = User.objects.get(nick='testowy')

    def test_change_password_with_correct_data(self):
        """
        Test check validation with correct data 
        Test checks if the old password has been replaced by a new password.
        """
        
        form = PasswordResetForm(data=self.change_password_data)
        self.assertTrue(form.is_valid())
        new_password = form.save()
        user = User.objects.get(nick='testowy')
        self.assertFalse(check_password(password=self.user_data['password1'], encoded=user.password))
        self.assertTrue(check_password(password=new_password, encoded=user.password))

    def test_change_password_with_bad_username(self):
        """
        The test check if the username is bad,
        if is form validation is False and exceptions will be raised.
        """
        self.change_password_data['username'] = 'bad nick'
        form = PasswordResetForm(data=self.change_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], "The user with the given e-mail address or name does not exist.")

    def test_change_password_with_bad_email(self):
        """
        The test check if the email is bad,
        if is form validation is False and exceptions will be raised.
        """
        self.change_password_data['email'] = 'bademail@gmail.com'
        form = PasswordResetForm(data=self.change_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], "The user with the given e-mail address or name does not exist.")




        


        
            
    







    
  
