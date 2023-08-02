from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from users.models import Student

# class course(models.Model):
#     name = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='course_name')
#     description = models.TextField()

#     def __str__(self):
#         return self.group.name

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

    # Many-to-many relationship with Group model
    # This allows multiple groups (courses) to have the same module
    groups = models.ManyToManyField(Group, related_name='modules')

    def __str__(self):
        return self.code + ' - ' + self.name
    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs = {'pk': self.pk})

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


# class Course(models.Model):
#     name = models.CharField(Group.name,max_length=255)
#     code = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self):
#         return self.name


