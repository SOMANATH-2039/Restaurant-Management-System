from django.shortcuts import render
from . models import MenuItems,Category
from Accounts.models import Profile
# Create your views here.


def menu(request,category=None):    
    categories = Category.objects.all()
    if category:
        menu_items = MenuItems.objects.filter(category__name=category)
    else:
        menu_items = MenuItems.objects.all()
    context = {
        'menu_items': menu_items,
        'categories': categories,
        'category': category,

    }
    return render(request,'Menu_.html',context)


def product(request,pk):
    product=MenuItems.objects.get(id=pk)
    context={
        'product':product,
    }
    return render(request,'product.html',context)