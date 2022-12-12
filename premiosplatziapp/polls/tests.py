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

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed"""
        past_question = create_question(question_Text="This is a past question",d=-15)
        future_question = create_question(question_Text="This is a future question",d=30)
        past_question.save()
        future_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_question(self):
        """The questions index page may display multiple questions"""
        q1 = create_question(question_Text="This is one past question",d=-15)
        q2 = create_question(question_Text="This is another past question",d=-30)
        q1.save()
        q2.save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [q1,q2]
        )

    def test_two_future_question(self):
        """The questions index page may no display multiple future questions"""
        q1 = create_question(question_Text="This is one future question",d=30)
        q2 = create_question(question_Text="This is another future question",d=15)
        q1.save()
        q2.save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """The detail view of a question with a pub_date in the future return a 404 error not found"""
        q1 = create_question(question_Text="This is a future question",d=30)
        q1.save()
        url=reverse("polls:detail",args=(q1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question a text"""
        q1 = create_question(question_Text="This is a past question",d=-30)
        q1.save()
        url=reverse("polls:detail",args=(q1.pk,))
        response = self.client.get(url)
        self.assertContains(response,q1.questionText)

# Create tests for ResultsView
# Make sure that it be imposible create choice without a question
# Create the respective tests

class QuestionResultsViewText(TestCase):
    pass

