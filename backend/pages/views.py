from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return render(
        request,
        "home.html",
        {"new_bird_name": request.POST.get("bird_name", "")}
        )


