from django.contrib import messages
from django.shortcuts import render
8
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Student 
from django.contrib.auth.decorators import login_required
from users.forms import StudentRegistrationForm, LoginForm, UserUpdateForm
from django.views.decorators.csrf import csrf_exempt

# Student registration view


@csrf_exempt  

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Student.objects.create(
                user=user,
                date_of_birth=form.cleaned_data['date_of_birth'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country'],
                photo=form.cleaned_data['photo']
            )
            login(request, user)
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


# Home page view
def home(request):
    return render(request, 'home.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect(request, 'home.html')


@login_required    
def profile(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)  
        s_form = StudentRegistrationForm(request.POST, instance=student) 
        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            if student is None:
                student = s_form.save(commit=False)
                student.user = request.user
                student.save()
            else:
                s_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:         
        u_form = UserUpdateForm(instance=request.user)         
        s_form = StudentRegistrationForm(instance=student)         

    context = {
        'u_form': u_form,
        's_form': s_form
    }
    return render(request, 'profile.html', context)
