from functools import partial

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import SetPasswordForm

from authentication.email_tool import send_email

class ChangePasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'old_password_mismatch': _("Old password does not match existing password.")
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        help_text = 'Enter the old password.',
        widget=forms.PasswordInput
    )

    def clean_old_password(self):
        """ 
            If the password given is different from the old one, 
        an exception is raised.
        """
        enter_old_password = self.cleaned_data['old_password']
        if not check_password(password=enter_old_password, encoded=self.user.password):
            raise ValidationError(
                message=self.error_messages['old_password_mismatch'],
                code='old_password_mismatch'
            )
        return enter_old_password

    def save(self, commit=True, send_message=True):
        print('save')
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        message = '''
        You change password.
        If it's you who disregards this message.
        '''
        if send_message:
            send_email(
                mail_from='Blog Administration',
                mail_to=[self.user.email],
                mail_subject='Change password.',
                message=message
            )
        if commit:
            self.user.save()
        return self.user

class ChangeEmailForm(forms.Form):
    error_messages = {
        'email_mismatch': _("The two email fields didn't match."),
        
    }
    new_adress_email1 = forms.EmailField(
        label=_('New e-mail adress.'),
        max_length=275,
        help_text=_('Enter the new adress e-mail.')
    )

    new_adress_email2 = forms.EmailField(
        label=_('Confirmation new e-mail adress.'),
        max_length=275,
        help_text=_("Enter the same email as before, for verification.")
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_adress_email2(self):
        """
            If the two emails provided do not match, 
        an exception is raised.
        """
        email1 = self.cleaned_data.get("new_adress_email1")
        email2 = self.cleaned_data.get("new_adress_email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return email2

    def save(self, send_message=True):
        new_email = self.cleaned_data['new_adress_email2']
        old_email = self.user.email
        self.user.email = new_email
        self.user.save()
        message_to_old_email = f'''
        You change adress e-mail.
        Old email: {old_email}
        New email: {new_email}
        If it's you who disregards this message.
        '''
        message_to_new_email = '''
        Congratulations! 
        You have successfully changed your email address.
        '''
        if send_message:
            send = partial(
                send_email,
                mail_from='Blog Administration',
                mail_subject='Change e-mail'
            )
            send(
                mail_to=[old_email],
                message=message_to_old_email
            )
            send(
                mail_to=[new_email],
                message=message_to_new_email
            )
    

        
        


    



        