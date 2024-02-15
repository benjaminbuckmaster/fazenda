from django.shortcuts import render
from .models import Bean

def home(request):
    # get the bean information from the database
    beans = Bean.objects.all()

    # show the homepage and pass through bean information
    return render(request, 'home.html', {'beans':beans})

def stock_management(request):
    pass

def bean_information(request):
    pass