from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'personal_expenses/index.html')
def add_expenses(request):
    return render(request, 'personal_expenses/add_expenses.html')