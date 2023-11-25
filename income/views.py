from django.shortcuts import render
from .models import Source, Income
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .userSettings.model import UserSettings
from django.contrib import messages

@never_cache
@login_required(login_url='/authentication/login')
def index(request):
    categories= Source.objects.all()
    income=Income.objects.filter(owner=request.user).order_by("-date")
    context={
        'income': income,
        'currency': currency
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources= Source.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    
    if request.method=='POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['incomeDate']
        source = request.POST['category']
        # breakpoint()
        
        if not amount:
            messages.error(request, 'Amount cannot be left blank')
            return render(request, 'income/add_income.html', context)
    
        
        if not description:
            messages.error(request, 'Description cannot be left blank')
            return render(request, 'income/add_income.html', context)
        

        Income.objects.create(owner=request.user, amount=amount, date=date,
                               source=source, description=description)
        messages.success(request, 'Saved succcessfully')
        return redirect('income')

        
    return render(request, 'income/add_income.html', context)
    