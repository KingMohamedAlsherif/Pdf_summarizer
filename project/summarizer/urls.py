from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('summary/<int:pk>/', views.view_summary, name='view_summary'),
]