from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_date = timezone.now() + timezone.timedelta(days=30)
        future_question = Question(pub_date=future_date)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        old_date = timezone.now() - timezone.timedelta(days=30)
        old_question = Question(pub_date=old_date)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        now = timezone.now() - timezone.timedelta(hours=1)
        recent_question = Question(pub_date=now)
        self.assertIs(recent_question.was_published_recently(), True)