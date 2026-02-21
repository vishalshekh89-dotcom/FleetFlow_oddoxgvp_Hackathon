from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('add/', views.trip_add, name='trip_add'),
    path('edit/<int:pk>/', views.trip_edit, name='trip_edit'),
    path('dispatch/<int:pk>/', views.trip_dispatch, name='trip_dispatch'),
    path('complete/<int:pk>/', views.trip_complete, name='trip_complete'),
]