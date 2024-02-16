from django.shortcuts import render, redirect
from .models import Bean, StockEntry, StockOffset, StockTotal
from .forms import StockEntryForm, BeanDetailsForm

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

def stock_entry(request, pk):
    # define context dictionary
    context = {}

    # initialise stock entry form with the bean chosen
    form = StockEntryForm(initial={'bean': pk})

    # get the bean information from the database
    bean = Bean.objects.filter(id=pk).get()

    # context to pass through
    context['pk'] = pk
    context['form'] = form
    context['bean'] = bean

    if request.method == 'POST':
        # if the save button was pressed
        if 'save' in request.POST:
            form = StockEntryForm(request.POST)
            form.save()

    # show page
    return render(request, 'stock-entry.html', context)

def edit_bean(request, pk):
    # initialise values to pass through to page
    context = {}

    # get the bean information from the database
    bean = Bean.objects.filter(id=pk).get()

    # initialise bean details form with the existing values
    form = BeanDetailsForm(initial={
        "name":bean.name,
        "origin":bean.origin,
        "supplier":bean.supplier,
        "notes":bean.notes,
        "reorder_trigger":bean.reorder_trigger,
        "reorder_qty":bean.reorder_qty,
    })

    # context to pass through
    context['pk'] = pk
    context['form'] = form
    context['bean'] = bean

    if request.method == 'POST':
        # if the save button was pressed
        if 'save' in request.POST:
            form = BeanDetailsForm(request.POST, instance=bean)
            form.save()
            return redirect('bean-information')
    
    # show page
    return render(request, 'edit-bean.html', context)
