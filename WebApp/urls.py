from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# from users import views as user_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),
    path('list_modules/<int:course_id>/', views.list_modules, name='list_modules'),
    path('module_detail/<int:module_id>/', views.module_detail, name='module_detail'),
    path('registermod/<int:module_id>/', views.registermod, name='registermod'),
    path('unregister/<int:registration_id>/', views.unregister, name='unregister'),
    # path('logout', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    # path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),

    path('courses/', views.courses, name='courses'),
    path('youtube', views.youtube, name = 'youtube'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
