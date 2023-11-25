from django.shortcuts import render, redirect
from .models import Source, Income
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from userSettings.models import UserSettings
from django.contrib import messages
from django.http import JsonResponse
import json

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = incomes.values()
        return JsonResponse(list(data), safe=False)

@never_cache
@login_required(login_url='/authentication/login')
def index(request):
    source= Source.objects.all()
    income=Income.objects.filter(owner=request.user).order_by("-date")
    try:
        currency_type = UserSettings.objects.get(user=request.user).currency
    except UserSettings.DoesNotExist:
        currency_type=None
    context={
        'income': income,
        'currency': currency_type
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources= Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    
    if request.method=='POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['incomeDate']
        source = request.POST['source']
        # breakpoint()
        
        if not amount:
            messages.error(request, 'Amount cannot be left blank')
            return render(request, 'income/add_income.html', context)
    
        
        if not description:
            messages.error(request, 'Description cannot be left blank')
            return render(request, 'income/add_income.html', context)
        
        if not date:
            messages.error(request, 'Date cannot be left blank')
            return render(request, 'income/add_income.html', context)
      

        Income.objects.create(owner=request.user, amount=amount, date=date,
                               source=source, description=description)
        messages.success(request, 'Saved succcessfully')
        return redirect('income')

        
    return render(request, 'income/add_income.html', context)


def edit_income(request, id):
    income= Income.objects.get(pk=id)
    sources= Source.objects.all()
    context={
        'income': income,
        'values': income,
        'sources':sources
    }
    if request.method=='GET':
        return render(request, 'income/edit_income.html', context)
   
    if request.method=='POST':

        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['incomeDate']
        source = request.POST['source']
        # breakpoint()
        
        if not amount:
            messages.error(request, 'Amount cannot be left blank')
            return render(request, 'income/edit_income.html', context)
    
        
        if not description:
            messages.error(request, 'Description cannot be left blank')
            return render(request, 'income/edit_income.html', context)
        

        income.owner=request.user 
        income.amount=amount 
        income.date=date
        income.source=source 
        income.description=description

        income.save()
        messages.success(request, 'Updated succcessfully')
        return redirect('income')   



def delete_income(request,id):
     income=Income.objects.get(pk=id)
     income.delete()
     messages.success(request, 'Income Removed')
     return redirect ('income')

    