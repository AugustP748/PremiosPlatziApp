from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Estas en la pagina principal de platzi premios!")


def detail(request,question_id):
    return HttpResponse(f"Estás viendo la pregunta numero {question_id}")



def results(request,question_id):
    return HttpResponse(f"Estás viendo los resulltados de la pregunta {question_id}")

    
def vote(request,question_id):
    return HttpResponse(f"Estás votando a la pregunta {question_id}")