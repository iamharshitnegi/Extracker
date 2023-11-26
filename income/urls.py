from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="income"),
    path('add-income', views.add_income, name="add_income"),
    path('edit-income/<int:id>', views.edit_income, name="edit_income"),
    path('delete-income/<int:id>', views.delete_income, name="delete_income"),
    path('search-income', csrf_exempt(views.search_income),
         name="search_income")
]