import datetime

from django.utils import timezone
from django.db import models

class Question(models.Model):
    """Class representation question in database."""

    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('Date Published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    def __str__(self):
        return f'{self.question_text}'

class Choice(models.Model):
    """Class representation choice in database where Question is Foreign Key."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=250)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.choice_text}'

   


 



