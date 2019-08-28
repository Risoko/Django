from django.test import TestCase

from authentication.email_tool import send_email

class TestSendEmail(TestCase):

    def setUp(self):
        self.mail_from = 'Blog administration'
        self.mail_to = ['przemyslaw.rozycki@smcebi.edu.pl']
        self.mail_subject = 'test'
        self.message = ' I am tester.'

    def test_send_email_with_correct_data(self):
        self.assertTrue(send_email(
            mail_from=self.mail_from, 
            mail_to=self.mail_to, 
            mail_subject=self.mail_subject,
            message = self.message
            )
        )
        
