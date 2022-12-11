from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse
import datetime

# Create your tests here.
class QuestionModelTests(TestCase):

    def test_Was_Published_Recently_With_Future_Question(self):
        """Was published recently return false for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(questionText="¿Quién es el mejor Couse Director de platzi?",
        pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_Was_Published_Recently_With_Past_Question(self):
        """Was published recently return false for questions whose pub_date is in the past."""
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(questionText="¿Quién es el mejor Couse Director de platzi?",
        pub_date=time)
        self.assertIs(past_question.was_published_recently(),False)

    def test_Was_Published_Recently_With_Current_Question(self):
        """Was published recently return true for questions whose pub_date is in the present."""
        time = timezone.now()
        current_question = Question(questionText="¿Quién es el mejor Couse Director de platzi?", 
        pub_date=time)
        self.assertIs(current_question.was_published_recently(),True)

    def test_Was_Published_Recently_With_Yesterday_Question(self):
        """Was published recently return true for questions whose pub_date is yesterday."""
        time = timezone.now() - datetime.timedelta(days=1)
        yesterday_question = Question(questionText="¿Quién es el mejor Couse Director de platzi?",
        pub_date=time)
        self.assertIs(yesterday_question.was_published_recently(),True)



def create_question(question_Text,d):
    """Creates a question with the given "question_Text" and published the given number of days offset to now
    (negative for question published in the past, positive for question that have yet to be published) ."""
    time = timezone.now() + datetime.timedelta(days=d)
    return Question(questionText=question_Text,pub_date=time)
    

class QestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If no questions exist, an appropiate message is displayed."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_no_display_future_questions(self):
        """If  question is in the furure, it's not displayed."""
        futureQuestion=create_question(question_Text="Esta es una pregunta para el futuro",d=30)
        futureQuestion.save()
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])


    def test_display_questions(self):
        """If  question is in the current, it's displayed."""
        past_question=create_question(question_Text="Esta es una pregunta en el pasado",d=-10)
        past_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"],[past_question])