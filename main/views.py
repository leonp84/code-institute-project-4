from django.shortcuts import render, HttpResponse  # noqa


# Create your views here.
def index(request):
    return render(
        request,
        'main/index.html'
    )
