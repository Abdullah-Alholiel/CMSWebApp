from django import forms
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from WebApp.models import Course, StudentGroup
from .models import Student
from django.contrib.auth.decorators import login_required
from .forms import (
    StudentRegistrationForm,
    LoginForm,
    UserUpdateForm,
    CustomPasswordResetForm,
    CustomPasswordConfirmForm,
    StudentUpdateForm,
)
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from CMSWebApp import settings
from django.core.mail import send_mail


# Student registration view


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                messages.error(request, f"user with {email} already exists")
                return redirect("register")
            user = form.save()
            if user.is_staff or user.is_superuser:
                pass

            student = Student.objects.create(
                user=user,
                date_of_birth=form.cleaned_data["date_of_birth"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                country=form.cleaned_data["country"],
                picture=form.cleaned_data["picture"],
            )
            group = form.cleaned_data.pop("group", None)
            student.save()
            Course.objects.create(group=group, student=student)
            messages.success(
                request,
                f"Your account has been created{user.username}! Now you can login!",
            )
            login(request, user)
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = StudentRegistrationForm()

    return render(request, "users/register.html", {"form": form})




# Login view
def login(request, form):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("profile")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


# Logout view
def logout(request):
    logout(request)
    courses = StudentGroup.objects.all()
    return redirect(request, "home.html", {"courses": courses})


@login_required
def profile(request):
    user_object = get_object_or_404(User, id=request.user.id)
    if user_object.is_superuser or user_object.is_staff :
       messages.info(request, "You are not allowed to visit here as an Administrator") 
       return redirect('home')
    student = Student.objects.get(user_id=user_object.pk)
    course = Course.objects.get(student_id=student.pk) 
    courses = StudentGroup.objects.all()
    print(f'coursename {course.group.name}')
    u_form = UserUpdateForm(instance=user_object)
    s_form = StudentUpdateForm(instance=student)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        s_form = StudentUpdateForm(request.POST, request.FILES, instance=student)

        if u_form.is_valid() and s_form.is_valid():
            s_form.save()
            u_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        s_form = StudentUpdateForm(instance=student)
    context = {"u_form": u_form, "s_form": s_form, "student": student, "course": course,"courses":courses}
    return render(request, "users/profile.html", context)

    
    # print(student.course.name)
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("custom_password_reset_sent")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        user = get_object_or_404(User, email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        reset_url = reverse_lazy(
            "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
        )
        valid_reset_url = self.request.build_absolute_uri(reset_url)
        context = {
            "valid_reset_link": valid_reset_url,
            "user": user,
            "domain": self.request.get_host(),
        }
        message = render_to_string("users/password_reset_email_link.html", context)

        subject = "Password reset"
        message = message
        receiver_email = email
        sender_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject=subject,
            message=message,
            from_email=sender_email,
            recipient_list=[receiver_email],
            fail_silently=True,
        )

        messages.success(
            self.request,
            f"Password reset mail sent succesfully. You should receive youe mail in less than 3 minutes",
        )
        return super().form_valid(form)


class CustomPasswordResetSentView(generic.TemplateView):
    template_name = "users/password_reset_sent.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("custom_password_reset_complete")
    form_class = CustomPasswordConfirmForm

    def form_valid(self, form):
        messages.success(self.request, f"Password reset successful.")
        return super().form_valid(form)


class CustomPasswordResetCompleteView(generic.TemplateView):
    template_name = "users/password_reset_complete.html"
