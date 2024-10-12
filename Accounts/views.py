from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from Employee.views import employee_list
def admin_dashboard(request):
    # employee=Employee.objects.all()
    # context={
    #     'employee':employee,
    # }
    return render(request,'admin_dashboard.html')


@login_required
def update_profile(request):
    user = request.user  # Get the logged-in user
    profile = Profile.objects.get(user=user)  # Get the user's profile

    if request.method == 'POST':
        # Get data from the POST request for User model fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Update User model fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        # Get data from the POST request
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')

        # Update profile fields
        profile.phone = phone
        profile.address1 = address1
        profile.address2 = address2
        profile.city = city
        profile.state = state
        profile.zipcode = zipcode
        profile.country = country
        
        # Handle profile photo upload
        if request.FILES.get('profile_photo'):
            profile.profile_photo = request.FILES.get('profile_photo')

        # Save the updated profile
        profile.save()

        # Add success message and redirect
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('update_profile')

    # Display the current profile details in the form
    context = {
        'profile': profile,
        'user': user,
    }
    return render(request, 'update_profile.html', context)


def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out...."))
    return redirect('home')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been Logged In"))
            return redirect('home')
        else:
            messages.error(request,("There was an error in logging"))
            return redirect('login_user')
    return render(request,'login.html',{})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Log the user in after successful registration
        login(request, user)
        messages.success(request, "Registration successful.")
        return redirect('home')

    return render(request, 'register.html')
