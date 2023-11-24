from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="personal_expenses"),
    path('add-expenses', views.add_expenses, name="add_expenses"),
    path('edit-expense/<int:id>', views.edit_expense, name="edit_expense"),
    path('delete-expense/<int:id>', views.delete_expense, name="delete_expense")
]