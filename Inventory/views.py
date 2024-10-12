from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem,Category
from django.contrib.auth.decorators import user_passes_test

# Only superusers can access the inventory management pages
@user_passes_test(lambda u: u.is_superuser)
def inventory_list(request):
    """View to list all inventory items."""
    items = InventoryItem.objects.all()
    return render(request, 'inventory_list.html', {'items': items})

@user_passes_test(lambda u: u.is_superuser)
def inventory_detail(request, pk):
    """View to show details of a single inventory item."""
    item = get_object_or_404(InventoryItem, pk=pk)
    return render(request, 'inventory_detail.html', {'item': item})

@user_passes_test(lambda u: u.is_superuser)
def inventory_create(request):
    """View to create a new inventory item."""
    if request.method == 'POST':
        # Handle form submission to create a new inventory item
        name = request.POST['name']
        category_id = request.POST['category']
        quantity = request.POST['quantity']
        price = request.POST['price']
        description = request.POST.get('description', '')

        category = get_object_or_404(Category, id=category_id)
        item = InventoryItem.objects.create(
            name=name, category=category, quantity=quantity, price=price, description=description
        )
        return redirect('inventory_list')

    categories = Category.objects.all()
    return render(request, 'inventory_form.html', {'categories': categories})

@user_passes_test(lambda u: u.is_superuser)
def inventory_delete(request, pk):
    """View to delete an inventory item."""
    item = get_object_or_404(InventoryItem, pk=pk)
    item.delete()
    return redirect('inventory_list')
