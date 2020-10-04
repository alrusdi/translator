from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def login(request):
    return render(request, 'ui/login.html')


@login_required
def translations(request):
    context = {}
    return render(request, 'ui/translations.html', context=context)


def home(request):
    return render(request, 'ui/home.html')
