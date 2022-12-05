from django.db import models

class Question(models.Model):
    questionText = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published")

class Choice(models.Model):
    questionFK = models.ForeignKey(Question,on_delete=models.CASCADE)
    choiceText = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
