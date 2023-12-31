from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="personal_expenses"),
    path('add-expenses', views.add_expenses, name="add_expenses"),
    path('edit-expense/<int:id>', views.edit_expense, name="edit_expense"),
    path('delete-expense/<int:id>', views.delete_expense, name="delete_expense"),
    path('search-expenses', csrf_exempt(views.search_expenses),
         name="search_expenses"),
    path('expense-summary', views.expense_summary, name="expense_summary"),
    path('stats', views.stats_view, name="stats"),
    path('export_csv', views.export_csv,
         name="export_csv"),
    path('export_pdf', views.export_pdf,
         name="export_pdf")
]