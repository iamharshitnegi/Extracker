from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense
from django.contrib import messages

# Create your views here.
@never_cache
@login_required(login_url='/authentication/login')
def index(request):
    categories= Category.objects.all()
    return render(request, 'personal_expenses/index.html')
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
        
    return render(request, 'personal_expenses/add_expenses.html', context)
    
