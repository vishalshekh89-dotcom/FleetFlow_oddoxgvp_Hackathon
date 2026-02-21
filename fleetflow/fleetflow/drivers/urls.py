from django.urls import path
from . import views

urlpatterns = [
    path('', views.driver_list, name='driver_list'),
    path('add/', views.driver_add, name='driver_add'),
    path('edit/<int:pk>/', views.driver_edit, name='driver_edit'),
    path('delete/<int:pk>/', views.driver_delete, name='driver_delete'),
]