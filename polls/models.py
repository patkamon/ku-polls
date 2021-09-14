import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    #Charfield need to define the max_length agrument
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')
    def __str__(self):
        return self.question_text
    # this function return true if question was published with 1 day from the func calling day.
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        return  timezone.now() >= self.pub_date

    def can_vote(self):
        return self.end_date > timezone.now() >= self.pub_date

class Choice(models.Model):
    #Give ForeignKey to show that this class was relate to other class
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
