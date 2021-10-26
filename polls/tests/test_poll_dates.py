"""Test models, views of ku-polls."""

from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question
from django.urls import reverse

def create_question(question_text, days, end=1):
    """
    Create question mockup.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end_time = time + datetime.timedelta(days=end)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_time)

class QuestionModelTests(TestCase):
    """Test quention model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recenly() returns False for questions whose pub_date is in the furture."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_new_question(self):
        """is_published() must return False if date now is before pub_date."""
        time = timezone.now() + datetime.timedelta(days=1)
        end_time = timezone.now() + datetime.timedelta(days=2)
        new_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(new_question.is_published(), False)

    def test_is_published_end_question(self):
        """is_published() must return True if date now is after pub_date."""
        time_end = timezone.now() - datetime.timedelta(days=1)
        time_pub = timezone.now() - datetime.timedelta(days=2)
        end_question = Question(pub_date=time_pub, end_date=time_end)
        self.assertIs(end_question.is_published(), True)

class QuestionDetailViewTests(TestCase):
    """Test detail views."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 302 redirect page found."""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5, end=10)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
