from datetime import timedelta

from django.utils import timezone

from .models import Choice, Question

def create_question(text_question, days):
    """
    Function return question, about given text and 
    the number of days forward and back.
    """
    return Question.objects.create(question_text=text_question, pub_date=timezone.now() + timedelta(days=days))

def create_choice_for_question(question, choice_text):
    return question.choice_set.create(choice_text=choice_text)
    
    
