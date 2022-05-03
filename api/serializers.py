from rest_framework import serializers
from .models import *


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class EmployeeSerializer(serializers.ModelSerializer):
    date_of_joining = serializers.DateField(required=False, format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    date_of_birth = serializers.DateField(required=False, format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    department = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'name', 'department', 'photo', 'resume', 'date_of_joining', 'date_of_birth')

    def get_department(self, instance):
        return instance.department.name if instance.department else ''



