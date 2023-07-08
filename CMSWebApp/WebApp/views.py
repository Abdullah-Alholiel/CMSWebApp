from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Module, Student, Registration

def home(request):
    courses = Course.objects.all()
    return render(request, 'WebApp/home.html', {'courses': courses})

def about_us(request):
    return render(request, 'about.html')

def contact_us(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # TODO: Send email using the provided information
        return redirect('contact_us')
    else:
        return render(request, 'contact_us.html')

def list_modules(request):
    modules = Module.objects.all()
    return render(request, 'list_modules.html', {'modules': modules})

@login_required
def registermod(request, module_id):
    module = Module.objects.get(id=module_id)
    student = request.user.student
    registration = Registration(student=student, module=module)
    registration.save()
    return redirect('list_modules')

@login_required
def unregister(request, registration_id):
    registration = Registration.objects.get(id=registration_id)
    registration.delete()
    return redirect('list_modules')