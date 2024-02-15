from django.shortcuts import render
from .models import Bean, StockEntry, StockOffset, StockTotal

def home(request):
    # show the homepage
    return render(request, 'home.html', {})

def stock_management(request):
    # get stock management information
    stock_totals = StockTotal.objects.all()

    # show the page and pass through stock information
    return render(request, 'stock.html', {'stock_totals': stock_totals})

def bean_information(request):
    # get the bean information from the database
    beans = Bean.objects.all()

    # shows bean information and passes through bean information
    return render(request, 'bean.html', {'beans':beans})