from random import randint, sample
from string import ascii_lowercase

from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from .email_tool import send_email
from .models import User
from .validators import string_only_letters_validator

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username", "nick",
            "first_name", "last_name",
            "email", "birth_date"
        )
        field_classes = {'username': UsernameField}

    def clean_first_name(self):
        """
        Method check first_name field.
        Returns the first letter in uppercase from the lower case.
        """
        first_name = self.cleaned_data['first_name']
        return first_name[0].upper() + first_name[1:].lower()

    def clean_last_name(self):
        """
        Method check last_name field.
        Returns the first letter in uppercase from the lower case.
        """
        last_name = self.cleaned_data['last_name']
        return last_name[0].upper() + last_name[1:].lower()

class PasswordResetForm(forms.Form):
    username = forms.CharField(
        label=_('user name'),
        help_text=_('Enter username.'),
    )
    email = forms.EmailField(
        label=_('address email'),
        help_text=_('Enter adress email.')
    )

    def _get_new_password(self, password_lenght=8):
        """
        The method returns a new random user password.
        """
        return ''.join(sample(ascii_lowercase, password_lenght))

    def clean_email(self):
        """
        The method check if the email matches the username.
        """
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username, email=email)
        except ObjectDoesNotExist:
            raise ValidationError(
                message=_('The user with the given e-mail address or name does not exist.')
            )
        else:
            return email

    def save(self):
        """
        The method sets a new user password and 
        sends a message to the provided email address with a new password.
        """
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        user = User.objects.get(email=email)
        new_password = self._get_new_password()
        message = f'''
        Hi {username}.
        You are reset your password.
        Your new password: {new_password}
        '''
        user.set_password(new_password)
        user.save()
        send_email(
            mailFrom='Blog Administration',
            mailTo=[email],
            mailSubject='Reset Password',
            message=message
        )
        return new_password

      

        


        

    



        

