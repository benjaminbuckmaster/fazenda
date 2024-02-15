from django.shortcuts import render
from .models import Bean

def home(request):
    # show the homepage
    return render(request, 'home.html', {})

def stock_management(request):
    pass

def bean_information(request):
    # get the bean information from the database
    beans = Bean.objects.all()

    # shows bean information and passes through bean information
    return render(request, 'bean.html', {'beans':beans})