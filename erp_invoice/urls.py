from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    # Customer app
    path('customers/', include('customers.urls')),

    # Placeholder URLs for future apps
    path('products/', TemplateView.as_view(template_name='placeholders/products_list.html'), name='products_list'),
    path('products/new/', TemplateView.as_view(template_name='placeholders/products_form.html'), name='products_create'),
    path('invoices/', TemplateView.as_view(template_name='placeholders/invoices_list.html'), name='invoices_list'),
    path('invoices/new/', TemplateView.as_view(template_name='placeholders/invoices_form.html'), name='invoices_create'),
]