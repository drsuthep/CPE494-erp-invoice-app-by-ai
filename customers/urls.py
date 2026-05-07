from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.list_placeholder, name='list'),
    path('new/', views.customer_create, name='create'),
    path('<int:id>/edit/', views.customer_edit, name='edit'),
    path('<int:id>/delete/', views.customer_delete, name='delete'),
]