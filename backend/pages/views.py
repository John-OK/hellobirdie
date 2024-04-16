from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    react_index = open('static/index.html', 'r').read()
    return HttpResponse(react_index)


