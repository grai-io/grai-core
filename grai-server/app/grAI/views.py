from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "grAI/index.html")


def room(request, workspace):
    return render(request, "grAI/room.html", {"workspace": workspace})
