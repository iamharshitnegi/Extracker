from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.
@never_cache
@login_required(login_url='/authentication/login')
def index(request):
    return render(request, 'personal_expenses/index.html')
def add_expenses(request):
    return render(request, 'personal_expenses/add_expenses.html')