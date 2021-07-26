from django.http.response import HttpResponse
from django.shortcuts import render

def home_view(request):
    return render(request,'home.html')

def no_page_found(request,exception):
    return render(request,'P404.html')