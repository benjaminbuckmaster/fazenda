from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Bean, StockEntry, StockOffset, StockTotal
from .forms import StockEntryForm, BeanDetailsForm, StockOffsetForm

def home(request):

    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Login error. Plase try again.")
            return redirect('home')

    # show the homepage
    return render(request, 'home.html', {})

def stock_management(request):
    if request.user.is_authenticated:
        # get stock management information
        stock_totals = StockTotal.objects.all().order_by('bean__name') # order by name descending

        # show the page and pass through stock information
        return render(request, 'stock.html', {'stock_totals': stock_totals})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')

def bean_information(request):
    if request.user.is_authenticated:
        # get the bean information from the database
        beans = Bean.objects.all()

        # shows bean information and passes through bean information
        return render(request, 'bean.html', {'beans':beans})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')
    
def new_stock_entry(request, pk=None):
    if request.user.is_authenticated:
        # define context dictionary
        context = {}

        # initialise stock entry form with the bean chosen if 'pk' is provided
        form_initial = {'bean': pk} if pk else None
        form = StockEntryForm(initial=form_initial)

        # get the bean information from the database if 'pk' is provided
        bean = Bean.objects.filter(id=pk).first() if pk else None

        # context to pass through
        context['pk'] = pk
        context['form'] = form
        context['bean'] = bean

        if request.method == 'POST':
            if 'save' in request.POST:
                form = StockEntryForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('stock-management')
            elif 'cancel' in request.POST:
                return redirect('stock-management')

        # show page
        return render(request, 'new-stock-entry.html', context)
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')

def edit_bean(request, pk):
    if request.user.is_authenticated:
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
            if 'save' in request.POST:
                form = BeanDetailsForm(request.POST, instance=bean)
                if form.is_valid():
                    form.save()
                    return redirect('bean-information')
            elif 'cancel' in request.POST:
                return redirect('bean-information')
        
        # show page
        return render(request, 'edit-bean.html', context)
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def stock_offset(request, pk):
    if request.user.is_authenticated:
        # initialise values to pass through to page
        context = {}

        # get the bean information from the database
        offset = StockOffset.objects.filter(id=pk).get()

        # initialise bean details form with the existing values
        form = StockOffsetForm(initial={
            "bean":offset.bean,
            "total_offset":offset.total_offset,
        })

        # context to pass through
        context['form'] = form
        context['stock_offset'] = offset

        if request.method == 'POST':
            if 'save' in request.POST:
                form = StockOffsetForm(request.POST, instance=offset)
                if form.is_valid():
                    form.save()
                    return redirect('stock-management')
            elif 'cancel' in request.POST:
                return redirect('stock-management')

        # show page
        return render(request, 'stock-offset.html', context)
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')
    
def view_stock_entries(request, pk=None):
    if request.user.is_authenticated:
        # initialise values to pass through to page
        context = {}

        # get entries if pk else get all
        if pk:
            entries = StockEntry.objects.filter(bean=pk).all().order_by('-date') # order by date descending
        else:
            entries = StockEntry.objects.all().order_by('-date') # order by date descending

        # define context to pass through
        context['entries'] = entries

        # show page
        return render(request, 'stock-entries.html', context)

    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')

def edit_stock_entry(request, id):
    if request.user.is_authenticated:
        # initialise values to pass through to page
        context = {}

        # get stock entry with id
        entry = StockEntry.objects.filter(id=id).get()

        # get bean
        bean = Bean.objects.filter(pk=entry.bean.id).get()

        # initialise stock entry form with the bean chosen if 'pk' is provided
        form_initial = {
            'bean': bean,
            'qty_added': entry.qty_added,
            'qty_used': entry.qty_used,
            }
        form = StockEntryForm(initial=form_initial)

        # define context to pass through
        context['entry'] = entry
        context['form'] = form

        if request.method == 'POST':
            if 'save' in request.POST:
                form = StockEntryForm(request.POST, instance=entry)
                if form.is_valid():
                    form.save()
                    return redirect('stock-management')
                else:
                    messages.success(request, form.errors)
            elif 'cancel' in request.POST:
                return redirect('stock-management')

        # show page
        return render(request, 'edit-stock-entry.html', context)

    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')