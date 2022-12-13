from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question,Choice


# Create your views here.
#def index(request):
#    latest_questions_list = Question.objects.all()
#    return render(request, 'polls/index.html',{"latest_question_list":latest_questions_list})

#def detail(request,question_id):
#    question = get_object_or_404(Question,pk=question_id)
#    return render(request, 'polls/detail.html',{"question":question})
    
#def results(request,question_id):
#    question = get_object_or_404(Question,pk=question_id)
#    return render(request, 'polls/results.html',{"question":question})

class indexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="latest_question_list"

    def get_queryset(self):
        """Returns tha last five published questions"""
        #El - pub_date is order from oldest to newest
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class detailView(generic.DetailView):
    template_name="polls/detail.html"
    model = Question

    def get_queryset(self):
        """Excludes any questions that aren't published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class resultsView(generic.DetailView):
    template_name="polls/results.html"
    model = Question



def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError,Choice.DoesNotExist):
        return render(request,"polls/detail.html",{
            'question': question,
            'error_messege':"No elegiste una respuesta"
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Redirect to new page after post, its a good practice
        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))
