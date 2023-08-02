from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Module, Registration, StudentGroup, Course

# Register your models here.
admin.site.register(Module)
admin.site.register(Registration)
admin.site.register(StudentGroup)
admin.site.register(Course)

# admin.site.register(course)
