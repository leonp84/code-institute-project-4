from django.shortcuts import render, HttpResponse  # noqa


# Create your views here.
def index(request):
    return HttpResponse('Main Page coming soon...')
