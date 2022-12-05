from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    questionText = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.questionText

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    questionFK = models.ForeignKey(Question,on_delete=models.CASCADE)
    choiceText = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choiceText

