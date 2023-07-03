from django.db import models
from django.contrib.auth.models import User



class Student(User):
    # Inherit from the built-in Django User model

    # Additional fields specific for Students
    date_of_birth = models.DateField()  # Date of birth of the student
    address = models.CharField(max_length=255)  # Address of the student
    city = models.CharField(max_length=255)  # City of the student
    country = models.CharField(max_length=255)  # Country of the student

    # Image field to store student's photo, uploaded images will be stored in 'student_photos' directory
    photo = models.ImageField(upload_to='student_photos/')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

class Module(models.Model):
    # Fields for Module details
    name = models.CharField(max_length=255)  # The name of the module
    code = models.CharField(max_length=255)  # The unique code of the module
    credit = models.IntegerField()  # The credit points for the module
    category = models.CharField(max_length=255)  # The category of the module
    description = models.TextField()  # The detailed description of the module

    # Boolean field indicating if the module is available for registration
    availability = models.BooleanField(default=False)

    # Boolean field indicating if the module is active or not
    active = models.BooleanField(default=True)

    # Many-to-many relationship with Course model
    # This allows multiple courses to have the same module
    courses = models.ManyToManyField('Course')

    class Meta:
        # Ensuring that the combination of name and code is unique
        unique_together = ('name', 'code',)


class Registration(models.Model):
    # Foreign keys to Student and Module models
    # Each registration is associated with one student and one module
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    # Automatic timestamp for when the registration was created
    date_of_registration = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensuring that the combination of student and module is unique
        # This prevents a student from registering to the same module multiple times
        unique_together = ('student', 'module',)



class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name