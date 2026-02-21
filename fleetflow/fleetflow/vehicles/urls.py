from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('add/', views.vehicle_add, name='vehicle_add'),
    path('edit/<int:pk>/', views.vehicle_edit, name='vehicle_edit'),
    path('delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),
]