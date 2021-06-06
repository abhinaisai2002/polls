from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def polls_view(request):
    return render(request,'polls/polls.html')