from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum
from django.forms import formset_factory
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Bean, StockEntry, StockAdjustment, StockTotal
from .forms import StockEntryForm, BeanDetailsForm, StockAdjustmentForm
from .todoist_controller import TodoistController # type: ignore
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

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
            "cost":bean.cost,
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
    

def consumption_30_days(request):
    # Calculate the date 30 days ago
    thirty_days_ago = date.today() - timedelta(days=30)

    # Filter StockEntry instances in the last 30 days
    recent_stock_entries = StockEntry.objects.filter(date__gte=thirty_days_ago)

    # Calculate total consumption for each bean in the last 30 days
    consumption_data = []
    for bean in Bean.objects.filter(is_hidden=False):
        total_qty_used = recent_stock_entries.filter(bean=bean).aggregate(Sum('qty_used'))['qty_used__sum'] or 0
        # Include adjustment if necessary
        total_adjustment = StockAdjustment.objects.filter(bean=bean, date__gte=thirty_days_ago).aggregate(Sum('adj_amount'))['adj_amount__sum'] or 0
        total_consumption = total_qty_used + total_adjustment

        consumption_data.append({
            'bean_name': bean.name,
            'total_consumption': total_consumption
        })

    # Extract labels and values for the pie chart
    labels = [data['bean_name'] for data in consumption_data]
    values = [data['total_consumption'] for data in consumption_data]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Convert the plotly figure to JSON
    graph_json = pio.to_json(fig)

    return render(request, 'consumption-30-days.html', {'graph_json': graph_json, 'consumption_data':consumption_data})

def stock_use_over_time(request):
    # Query the stock entries
    stock_entries = (
        StockEntry.objects.values(
            'date',
            'bean__name',
            'qty_used'
        )
    )
    
    data = {}
    for entry in stock_entries:
        date = entry['date']
        bean = entry['bean__name']
        qty_used = entry['qty_used']
        
        if bean not in data:
            data[bean] = []
        
        data[bean].append({'date': date, 'qty_used': qty_used})
    
    # Prepare data for Plotly scatter plot
    plotly_data = []
    for bean, values in data.items():
        x = [v['date'] for v in values]
        y = [v['qty_used'] for v in values]
        plotly_data.append(go.Scatter(x=x, y=y, mode='lines', name=bean))
    
    # Create the scatter plot
    fig = go.Figure(data=plotly_data)

    # Convert the plotly figure to JSON
    graph_json = pio.to_json(fig)

    return render(request, 'stock_use_over_time.html', {'graph_json': graph_json})

def statistics(request):
    if request.user.is_authenticated:
        return render(request, 'statistics.html')

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