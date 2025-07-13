from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request, 'dashboard.html', {'text': 'Enabhorena'})

def settings(request):
    return render(request, 'settings.html', {'text': 'Enabhorena'})

def convert(request, slip):
    return render(request, 'convert.html', {'text': 'Enabhorena'})

def contact(request):
    return render(request, 'contact.html')