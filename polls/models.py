"""Handle models in polls app."""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    """Handle question model."""

    # Charfield need to define the max_length agrument
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        """Show question text."""
        return self.question_text

    # this function return true if question was published with 1 day from the func calling day.
    def was_published_recently(self):
        """Check is question was published less than 1 day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check is question was published."""
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """Check is question still during the vote period."""
        return self.end_date > timezone.now() >= self.pub_date


class Choice(models.Model):
    """Handle choice."""

    # Give ForeignKey to show that this class was relate to other class
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    def __str__(self):
        """Show choice text."""
        return self.choice_text

    @property
    def votes(self):
        count = Vote.objects.filter(choice=self).count()
        return count

class Vote(models.Model):
    # id = models.AutoField()
    user = models.ForeignKey(
            User,
            null=False,
            blank=False,
            on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.choice} vote by {self.user.username}"
