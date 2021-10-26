from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse

import datetime
from django.utils import timezone
from polls.models import Question


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


class UserAuthTest(TestCase):

    def setUp(self):
        super().setUp()
        self.username = "Patlom"
        self.password = "lompat-rankrank!"
        self.user1 = User.objects.create_user(
                         username=self.username,
                         password=self.password,
                         email="lompat@patlom.com")
        self.user1.first_name = "Patlom-RankMak"
        self.user1.save()

    def test_login_view(self):
        """Test that a user can login via the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using POST
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": self.username, "password": self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))
        #check is there name of user in index page
        index_url = reverse("polls:index")
        index_response = self.client.get(index_url)
        self.assertContains(index_response, self.username)

    def test_logout_view(self):
        """Test that there is logout views"""
        self.client.login(username=self.username, password=self.password)
        logout_url = reverse("logout")
        response = self.client.get(logout_url)
        self.assertContains(response, "Good bye!")
        self.assertNotContains(response, self.username)

    def test_authenticate_vote(self):
        """Test that authenticated user be able to vote."""
        self.client.login(username=self.username, password=self.password)
        question = create_question(question_text='This is a question', days=-5)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(200, response.status_code)

    def test_non_authenticate_vote(self):
        """Test the outsider vote."""
        question = create_question(question_text='This is a question', days=-5)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(302, response.status_code)
        #redirect to login page
        self.assertRedirects(response, "/accounts/login/?next=/polls/1/vote/")
