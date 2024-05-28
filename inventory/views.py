from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Bean, Product, ProductBean, ProductPackaging, ProductShipping, Shipping, StockEntry, StockAdjustment, StockTotal
from .forms import StockEntryForm, BeanDetailsForm, StockAdjustmentForm
from .todoist_controller import TodoistController # type: ignore
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def home(request):
    # initialise context to pass through to page
    context = {}

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
            messages.error(request, "Login error. Plase try again.")
            return redirect('home')
        
    # Check if the page is being rendered after a successful login or a manual refresh
    if request.method == 'GET':
        # Instantiate TodoistController
        todoist = TodoistController()

        # Fetch data from Todoist API
        todoist_today = todoist.get_today()
        todoist_overdue = todoist.get_overdue()

        # Add fetched data to context
        context = {
            'todoist_today': todoist_today,
            'todoist_overdue': todoist_overdue,
            'api_in_progress': True  # Set a flag indicating that the API call is in progress
        }

        # Show the homepage
        return render(request, 'home.html', context)

    # Default case
    return render(request, 'home.html')

def stock_management(request):
    if request.user.is_authenticated:
        # get stock management information
        stock_totals = StockTotal.objects.all().order_by('bean__name') # order by name descending

        # show the page and pass through stock information
        return render(request, 'stock.html', {'stock_totals': stock_totals})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')

def bean_information(request):
    if request.user.is_authenticated:
        # define context dictionary
        context = {}

        # get the bean information from the database
        beans = Bean.objects.all().order_by('name')

        stock_totals = StockTotal.objects.all().order_by('-total_quantity')

        chart = chart_stock_totals(stock_totals)

        # context to pass through
        context['beans'] = beans
        context['stock_totals'] = stock_totals
        context['chart'] = chart

        # shows bean information and passes through context
        return render(request, 'bean.html', context)
    else:
        messages.error(request, "You must be logged in to view this page.")
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
                # check if an entry already exists for the current day
                if StockEntry.objects.filter(date=timezone.now().date(), bean=bean).exists():
                    messages.error(request, "An entry for today already exists.")
                    return redirect('bean-information')
                if form.is_valid():
                    form.save()
                    messages.success(request, "New entry added.")
                    return redirect('bean-information')
            elif 'cancel' in request.POST:
                return redirect('bean-information')

        # show page
        return render(request, 'new-stock-entry.html', context)
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')

def bean_details(request, pk):
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
            "is_hidden":bean.is_hidden,
            "is_ordered":bean.is_ordered
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
                    messages.success(request, "Changes saved.")
                    return redirect('bean-information')
            elif 'cancel' in request.POST:
                return redirect('bean-information')
        
        # show page
        return render(request, 'bean-details.html', context)
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def new_stock_adjustment(request, pk=None):
    if request.user.is_authenticated:
        # define context dictionary
        context = {}

        # initialise stock entry form with the bean chosen if 'pk' is provided
        form_initial = {'bean': pk} if pk else None
        form = StockAdjustmentForm(initial=form_initial)

        # get the bean information from the database if 'pk' is provided
        bean = Bean.objects.filter(id=pk).first() if pk else None

        # context to pass through
        context['pk'] = pk
        context['form'] = form
        context['bean'] = bean

        if request.method == 'POST':
            if 'save' in request.POST:
                form = StockAdjustmentForm(request.POST)
                # check if an entry already exists for the current day
                if StockAdjustment.objects.filter(date=timezone.now().date(), bean=bean).exists():
                    messages.error(request, "An adjustment for today already exists.")
                    return redirect('bean-information')
                if form.is_valid():
                    form.save()
                    return redirect('bean-information')
            elif 'cancel' in request.POST:
                return redirect('bean-information')

        # show page
        return render(request, 'new-stock-adjustment.html', context)
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')
    
def view_stock_entries(request, pk):
    if request.user.is_authenticated:
        context = {}

        bean = Bean.objects.get(id=pk)
        context['bean'] = bean

        entries = StockEntry.objects.filter(bean=pk).all().order_by('-date') # order by date descending
        context['entries'] = entries

        return render(request, 'stock-entries.html', context)

    else:
        messages.error(request, "You must be logged in to view this page.")
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
                    return redirect('bean-information')
                else:
                    messages.error(request, form.errors)
            elif 'cancel' in request.POST:
                return redirect('bean-information')

        # show page
        return render(request, 'edit-stock-entry.html', context)

    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')
    
def view_stock_adjustments(request, pk=None):
    if request.user.is_authenticated:
        # initialise values to pass through to page
        context = {}

        if pk:
            bean = Bean.objects.get(id=pk)

        adjustments = StockAdjustment.objects.filter(bean=pk).all().order_by('-date') # order by date descending

        # define context to pass through
        context['adjustments'] = adjustments
        context['bean'] = bean

        # show page
        return render(request, 'stock-adjustments.html', context)

    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')

def edit_stock_adjustment(request, id):
    if request.user.is_authenticated:
        # initialise values to pass through to page
        context = {}

        # get stock adjustment with id
        adjustment = StockAdjustment.objects.filter(id=id).get()

        # get bean
        bean = Bean.objects.filter(pk=adjustment.bean.id).get()

        # initialise stock adjustment form with the bean chosen if 'pk' is provided
        form_initial = {
            'bean': bean,
            'adj_amount': adjustment.adj_amount,
            }
        form = StockAdjustmentForm(initial=form_initial)

        # define context to pass through
        context['adjustment'] = adjustment
        context['form'] = form

        if request.method == 'POST':
            if 'save' in request.POST:
                form = StockAdjustmentForm(request.POST, instance=adjustment)
                if form.is_valid():
                    form.save()
                    return redirect('bean-information')
                else:
                    messages.error(request, form.errors)
            elif 'cancel' in request.POST:
                return redirect('bean-information')

        # show page
        return render(request, 'edit-stock-adjustment.html', context)

    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')
    
def statistics(request):
    def beans_consumption_last_30_days():
        # Calculate the date 30 days ago
        thirty_days_ago = date.today() - timedelta(days=30)

        # Filter StockEntry instances in the last 30 days
        recent_stock_entries = StockEntry.objects.filter(date__gte=thirty_days_ago)

        # Calculate total consumption for each bean in the last 30 days
        consumption_data = []
        for bean in Bean.objects.filter(is_hidden=False):
            total_qty_used = recent_stock_entries.filter(bean=bean).aggregate(Sum('qty_used'))['qty_used__sum'] or 0
            # can include adjustment if decided that it is necessary
            total_adjustment = StockAdjustment.objects.filter(bean=bean, date__gte=thirty_days_ago).aggregate(Sum('adj_amount'))['adj_amount__sum'] or 0
            total_consumption = total_qty_used + total_adjustment

            consumption_data.append({
                'bean_name': bean.name,
                'total_consumption': total_qty_used
            })

        return consumption_data
    
    if request.user.is_authenticated:
        # initialise values to pass through to page
        context = {}

        consumption_data_last_30_days = beans_consumption_last_30_days()

        # define context to pass through to page
        context['consumption_data_last_30_days'] = consumption_data_last_30_days

        # show page
        return render(request, 'statistics.html', context)

    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')
    
def chart_stock_totals(stock_totals):
    color = ['#008042']

    df = pd.DataFrame(list(stock_totals.values("bean__name", "total_quantity")))
    fig = go.Figure()
    for index, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['bean__name']],
            y=[row['total_quantity']],
            marker=dict(color=color[0],),
            name=row['bean__name']
        ))
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='#ffffff',
        margin=dict(l=0, r=0, t=40, b=20),
        bargap=0.15,
        bargroupgap=0.1,
        showlegend=False,
        autosize=True,
    )

    chart_html = fig.to_html()
    return chart_html
    
def calculate_cogs(product):
    raw_cost = Decimal(0)
    
    productbeans = ProductBean.objects.filter(product=product)
    for productbean in productbeans:
        if productbean.product.size == '250g':
            raw_cost += productbean.bean.cost * Decimal('0.25') * (productbean.percentage / 100)
        elif productbean.product.size == '500g':
            raw_cost += productbean.bean.cost * Decimal('0.5') * (productbean.percentage / 100)
        else:
            raw_cost += productbean.bean.cost * (productbean.percentage / 100)
        
    cogs = raw_cost * Decimal('1.2')
    return cogs

def product_pricing(request):
    if request.user.is_authenticated:
        context = {}
        products = Product.objects.all()
        for product in products:
            cogs = calculate_cogs(product)
            context[product] = cogs

        return render(request, 'product-pricing.html', {'product_costs': context})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')