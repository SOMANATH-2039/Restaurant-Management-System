from django.shortcuts import render
from . models import MenuItems,Category
from Accounts.models import Profile
# Create your views here.


def menu(request,category=None):
    user=request.user
    profile=Profile.objects.get(user=user)
    
    categories = Category.objects.all()
    if category:
        menu_items = MenuItems.objects.filter(category__name=category)
    else:
        menu_items = MenuItems.objects.all()

    context = {
        'menu_items': menu_items,
        'categories': categories,
        'category': category,
        'profile': profile,
    }
    return render(request,'Menu_.html',context)


def product(request,pk):
    user=request.user
    profile=Profile.objects.get(user=user)
    product=MenuItems.objects.get(id=pk)
    context={
        'profile':profile,
        'product':product,
    }
    return render(request,'product.html',context)