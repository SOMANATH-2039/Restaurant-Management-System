from django.shortcuts import render,redirect
from django.contrib import messages
from . models import Booking
from Menu.models import MenuItems
from django.db.models import Q
from Accounts.models import Profile
from Menu.models import Category
import random
# Home
def home(request,category=None):
    categories = Category.objects.all()
    if category:
        menu_items = MenuItems.objects.filter(category__name=category)
    else:
        menu_items = MenuItems.objects.all()

    # Randomly select 9 menu items, but only if there are more than 9 items
    if menu_items.count() > 9:
        menu_items = random.sample(list(menu_items), 9)

    context = {
        'menu_items': menu_items,
        'categories': categories,
        'category': category,
        
    }
    return render(request,'home.html',context)

# Order
def order(request):

    return render(request,'home.html',{})

# About
def about(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    # context = {
    #     'profile': profile,
        
    # }
    return render(request,'about.html',)

# Book Table
def book_table(request):
    if request.method == 'POST':
        # Get the form data directly from the POST request
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        persons = request.POST.get('persons')
        date = request.POST.get('date')

        # Perform basic validation (if necessary)
        if not name or not phone_number or not email or not persons or not date:
            messages.error(request, 'Please fill in all fields.')
        else:
            # Save the booking data to the database
            booking = Booking(
                name=name,
                phone_number=phone_number,
                email=email,
                persons=persons,
                date=date
            )
            booking.save()

            # Show success message
            messages.success(request, 'Your table has been booked successfully!')

            # Redirect to the booking page or a success page
            return redirect('book_table')
    
    # Render the form if GET request
    return render(request, 'book_table.html',)

    # return render(request,'book_table.html',{})


#Contact us
def contact(request):
    return render(request,'contact.html',{})

def search(request):
    #check if user filled the form
    if request.method=="POST":
        searched=request.POST['searched']
        #Query the database for products
        searched=MenuItems.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        context = {

        'searched':searched,
        
    }
        if not searched:
            messages.error(request,("Product does not exit search for another product"))
            return render(request,'search.html',{})
        else:
            return render(request,'search.html',context)
    return render(request,'search.html',context)