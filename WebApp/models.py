from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from users.models import Student


class StudentGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse("group_detail", kwargs={"pk": self.pk})
    
    
class Module(models.Model):
    name = models.CharField(max_length=255)  # The name of the module
    code = models.CharField(max_length=255)  # The unique code of the module
    credit = models.IntegerField()  # The credit points for the module
    category = models.CharField(max_length=255)  # The category of the module
    description = models.TextField()  # The detailed description of the module
    availability = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(StudentGroup, related_name='modules')

    def __str__(self):
        return self.code + ' - ' + self.name
    
    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs = {'module_code': self.code})

    class Meta:
        # Ensuring that the combination of name and code is unique
        unique_together = ('name', 'code',)

class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    date_of_registration = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'module',)
    def __str__(self):
        return f'{self.student.user.get_full_name()} {self.module.name}'

class Course(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.DO_NOTHING)
    student = models.OneToOneField(Student, on_delete=models.DO_NOTHING)
   
    def __str__(self):
        return f'{self.group.name} {self.student.user.get_full_name()}'

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})
    
