from django.shortcuts import render


def index(request):
    context = {
        'message': 'Welcome to the home page!',
    }
    return render(request, 'base.html', context)
# Create your views here.
