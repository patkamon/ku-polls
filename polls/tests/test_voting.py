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

    def test_can_vote_new_question(self):
        """can_vote() must return True when polls are still publishing."""
        new_question = create_question("new_question", -1, 3)
        self.assertIs(new_question.can_vote(), True)

    def test_can_vote_future_question(self):
        """can_vote() must return False when a poll is not published yet."""
        future_question = create_question("future_question", 3)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_passed_question(self):
        """can_vote() must return False when a poll is not publishing anymore."""
        future_question = create_question("passed_question", -5)
        self.assertIs(future_question.can_vote(), False)
