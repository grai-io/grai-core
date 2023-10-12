from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "grAI/index.html")


def room(request, room_name):
    return render(request, "grAI/room.html", {"room_name": room_name})
