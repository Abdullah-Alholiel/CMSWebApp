from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from users import views as user_views


app_name = 'WebApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),
    path('list_modules/', views.list_modules, name='list_modules'),
    path('registermod/<int:module_id>/', views.registermod, name='registermod'),
    path('unregister/<int:registration_id>/', views.unregister, name='unregister'),
    path('logout', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
]