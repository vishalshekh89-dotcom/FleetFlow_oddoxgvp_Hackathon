from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('fuel/add/', views.fuel_add, name='fuel_add'),
]