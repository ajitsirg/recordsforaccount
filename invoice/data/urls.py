from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/new/', views.invoice_create, name='invoice_create'),
    path('invoice/<int:invoice_id>/item/new/', views.item_create, name='item_create'),
]
