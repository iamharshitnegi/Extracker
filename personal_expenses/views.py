from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense
from django.contrib import messages
from django.http import JsonResponse
import json
from userSettings.models import UserSettings
import datetime

# Create your views here.
@never_cache
@login_required(login_url='/authentication/login')
def index(request):
    categories= Category.objects.all()
    expenses=Expense.objects.filter(owner=request.user).order_by("-date")
    try:
        currency_type = UserSettings.objects.get(user=request.user).currency
    except UserSettings.DoesNotExist:
        currency_type=None
    context={
        'expenses': expenses,
        'currency_type': currency_type
    }
    return render(request, 'personal_expenses/index.html', context)

def add_expenses(request):
    categories= Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    
    if request.method=='POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expenseDate']
        category = request.POST['category']
        # breakpoint()
        
        if not amount:
            messages.error(request, 'Amount cannot be left blank')
            return render(request, 'personal_expenses/add_expenses.html', context)
    
        
        if not description:
            messages.error(request, 'Description cannot be left blank')
            return render(request, 'personal_expenses/add_expenses.html', context)
        
        if not date:
            messages.error(request, 'Date cannot be left blank')
            return render(request, 'personal_expenses/add_expenses.html', context)
        

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Saved succcessfully')
        return redirect('personal_expenses')

        
    return render(request, 'personal_expenses/add_expenses.html', context)
    

def edit_expense(request, id):
    expense= Expense.objects.get(pk=id)
    categories= Category.objects.all()
    context={
        'expense': expense,
        'values': expense,
        'categories':categories
    }
    if request.method=='GET':
        return render(request, 'personal_expenses/edit_expense.html', context)
   
    if request.method=='POST':

        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expenseDate']
        category = request.POST['category']
        # breakpoint()
        
        if not amount:
            messages.error(request, 'Amount cannot be left blank')
            return render(request, 'personal_expenses/edit_expense.html', context)
    
        
        if not description:
            messages.error(request, 'Description cannot be left blank')
            return render(request, 'personal_expenses/edit_expense.html', context)
        

        expense.owner=request.user 
        expense.amount=amount 
        expense.date=date
        expense.category=category 
        expense.description=description

        expense.save()
        messages.success(request, 'Updated succcessfully')
        return redirect('personal_expenses')   



def delete_expense(request,id):
     expense=Expense.objects.get(pk=id)
     expense.delete()
     messages.success(request, 'Expense Removed')
     return redirect ('personal_expenses')

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
    
def expense_summary(request):
    present_date= datetime.date.today()
    past_date= present_date-datetime.timedelta(days=30*6)
    expenses= Expense.objects.filter( owner=request.user, date__gte=past_date, date__lte=present_date)

    finalrep={}

    def get_category(expense):
        return expense.category
    
    category_list= list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount=0
        filtered_by_category=expenses.filter(category=category)

        for item in filtered_by_category:
            amount+=item.amount
        
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'personal_expenses/stats.html')