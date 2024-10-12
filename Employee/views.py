# employee/views.py
from django.shortcuts import render, redirect, get_object_or_404
from . models import Employee
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

# Check if user is a superuser
def superuser_required(user):
    return user.is_superuser

# List all employees
# @user_passes_test(superuser_required)
def employee_list(request):
    if not request.user.is_superuser:
        return render(request,'access_denied.html')
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

# Add a new employee
@user_passes_test(superuser_required)
def employee_add(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit employee data.")
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        department = request.POST.get('department')
        position = request.POST.get('position')
        salary = request.POST.get('salary')
        date_of_hire = request.POST.get('date_of_hire')

        Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            department=department,
            position=position,
            salary=salary,
            date_of_hire=date_of_hire
        )
        return redirect('employee_list')
    return render(request, 'employee_form.html')

# Edit an existing employee
@user_passes_test(superuser_required)
def employee_edit(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit employee data.")
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        employee.phone_number = request.POST.get('phone_number')
        employee.department = request.POST.get('department')
        employee.position = request.POST.get('position')
        employee.salary = request.POST.get('salary')
        employee.date_of_hire = request.POST.get('date_of_hire')
        employee.save()
        return redirect('employee_list')
    return render(request, 'employee_form.html', {'employee': employee})

# Delete an employee
@user_passes_test(superuser_required)
def employee_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit employee data.")
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})
