from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Employee(models.Model):
    department = models.ForeignKey(Department, related_name='employee_department', blank=True, null=True,
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    photo = models.FileField(upload_to='employee_photo/', null=True, blank=True)
    resume = models.FileField(upload_to='employee_resume/', null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
