from django.test import TestCase
from django.urls import reverse

from .helpty_function_test import create_question, create_choice_for_question

class IndexViewTests(TestCase):
 
    def test_no_questions(self):
        response = self.client.get(reverse('poll:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions.")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_question(self):
        create_question(text_question='I am the test.', days=-30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: I am the test.>'] 
            )
    
    def test_future_question(self):
        create_question(text_question='I am the test.', days=30)
        response = self.client.get(reverse('poll:index'))
        self.assertContains(response, "No questions.")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_future_and_past_question(self):
        create_question(text_question='Future question.', days=30)
        create_question(text_question='Past question.', days=-30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question.>'] 
            )

    def test_two_past_questions(self):
        create_question(text_question='Past question 1.', days=-30)
        create_question(text_question='Past question 2.', days=-30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question 1.>', '<Question: Past question 2.>'], ordered=False 
            )

class DetailViewTests(TestCase):

    def test_question_no_choice(self):
        question = create_question(text_question='Future question.', days=5)
        url = reverse('poll:detail', args=[question.id])
        response = self.client.get(url)
        self.assertContains(response, 'You must create minimum two answer.')

    def test_question_with_one_choice(self):

        question = create_question(text_question='Future question.', days=5)
        create_choice_for_question(question, 'Choice 1.')
        url = reverse('poll:detail', args=[question.id])
        response = self.client.get(url)
        self.assertContains(response, 'You must create minimum two answer.')

    def test_question_with_two_choice(self):
    
        question = create_question(text_question='Future question.', days=5)
        create_choice_for_question(question, 'Choice 1.')
        create_choice_for_question(question, 'Choice 2.')
        url = reverse('poll:detail', args=[question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
        self.assertEqual(len(question.choice_set.all()), 2)
        

class VoteViewTests(TestCase):

    def test_bad_primary_key_question(self):

        create_question(text_question='Bad primary key.', days=-10)
        url = reverse(viewname='poll:vote', args=[1000])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_question_no_choice(self):
        question = create_question(text_question='Future question.', days=5)
        url = reverse(viewname='poll:vote', args=[question.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='You did not answer.')
        self.assertContains(response, question.question_text)
        self.assertEqual(list(question.choice_set.all()), [])

    def test_question_two_choice(self):
        question = create_question(text_question='Future question.', days=5)
        create_choice_for_question(question, 'Choice 1.')
        create_choice_for_question(question, 'Choice 2.')
        url = reverse(viewname='poll:vote', args=[question.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)








        



    

    













