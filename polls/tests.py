import datetime

from django.urls import reverse
from django.utils import timezone

from django.test import TestCase

from polls.models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text='Past question', days=-30)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_future_question(self):
        create_question(question_text='Future question', days=30)

        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_future_and_past_question(self):
        create_question(question_text='Past question', days=-30)
        create_question(question_text='Future question', days=30)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_two_past_questions(self):
        create_question(question_text='Past question 1', days=-30)
        create_question(question_text='Past question 2', days=-5)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2>', '<Question: Past question 1>']
        )

    def test_more_than_five_questions(self):
        create_question(question_text='Past question 1', days=-30)
        create_question(question_text='Past question 2', days=-25)
        create_question(question_text='Past question 3', days=-20)
        create_question(question_text='Past question 4', days=-15)
        create_question(question_text='Past question 5', days=-10)
        create_question(question_text='Past question 6', days=-5)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 6>', '<Question: Past question 5>',
             '<Question: Past question 4>', '<Question: Past question 3>',
             '<Question: Past question 2>']
        )


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
