from django.shortcuts import render
from .models import Event


def home(request):
    events = Event.objects.filter(is_active=True)

    context = {
        'events': events
    }

    return render(request, 'events/home.html', context)
