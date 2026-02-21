from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics, name='analytics'),
    path('export/', views.export_csv, name='export_csv'),
]