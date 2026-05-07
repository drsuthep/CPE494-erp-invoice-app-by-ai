from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Customer
from .forms import CustomerForm

def list_placeholder(request):
    """
    Renders a placeholder page for the customer list view.
    The real list view will be implemented in a future sprint.
    """
    return render(request, 'customers/list_placeholder.html')

def customer_create(request):
    """
    Handles the creation of a new customer.
    GET: Displays an empty form for creating a new customer.
    POST: Validates the submitted data. If valid, creates a new customer
          and redirects to the edit view for the new customer. If invalid,
          re-renders the form with validation errors.
    """
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Saving... Save successful")
            return redirect('customers:edit', id=obj.id)
    else:
        form = CustomerForm()

    context = {
        'form': form,
        'obj': None, # No object instance on create
    }
    return render(request, 'customers/form.html', context)

def customer_edit(request, id):
    """
    Handles the editing of an existing customer.
    GET: Displays a form pre-filled with the customer's current data.
    POST: Validates the submitted data. If valid, updates the customer
          and redirects back to the edit view. If invalid, re-renders
          the form with validation errors.
    """
    customer = get_object_or_404(Customer, pk=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Saving... Save successful")
            return redirect('customers:edit', id=obj.id)
    else:
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'obj': customer,
    }
    return render(request, 'customers/form.html', context)

@require_POST
def customer_delete(request, id):
    """
    Handles the deletion of a customer. This view only accepts POST requests.
    Deletes the specified customer and redirects to the customer list view.
    """
    customer = get_object_or_404(Customer, pk=id)
    customer.delete()
    # A success message for deletion might be added in a future sprint.
    return redirect('customers:list')