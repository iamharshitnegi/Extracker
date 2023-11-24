from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense
from django.contrib import messages

# Create your views here.
@never_cache
@login_required(login_url='/authentication/login')
def index(request):
    categories= Category.objects.all()
    expenses=Expense.objects.filter(owner=request.user).order_by("-date")
    context={
        'expenses': expenses
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
        return render(request, 'personal_expenses/editExpense.html', context)
   
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

        