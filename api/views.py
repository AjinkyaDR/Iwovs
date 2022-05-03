from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator

from .serializers import DepartmentSerializer, EmployeeSerializer

from accounts.models import User
from .models import *


class LoginViewSet(viewsets.ModelViewSet):
    """User Login API"""
    queryset = User.objects.filter()

    def create(self, request, *args, **kwargs):

        data = request.data
        if data.get('email') and data.get('password'):
            if User.objects.filter(email__iexact=data.get('email')).exists():
                print("Exists")
                query = authenticate(email=data.get('email'), password=data.get('password'))
                if query:
                    user = User.objects.get(email__iexact=data.get('email'))
                    try:
                        token = user.auth_token.key
                    except:
                        token = Token.objects.create(user=user)
                        token = token.key
                    return Response({"user_details": user.email,
                                     "token": token,
                                     }, status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, "message": "Invalid credentials"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': False, "message": "User does not exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, "message": "Please provide email address and password"},
                            status=status.HTTP_400_BAD_REQUEST)


class DepartmentList(viewsets.ModelViewSet):
    """Api for department list and to create department record"""
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        obj = Department.objects.all()
        data = DepartmentSerializer(obj, many=True, context={"request": request}).data
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        if data.get('name'):
            Department.objects.create(name=data.get('name'))
            return Response({"message": "Department added successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Please provide department name"}, status=status.HTTP_404_NOT_FOUND)


class EmployeeList(viewsets.ModelViewSet):
    """Api for employee list with pagination and also employee creation api"""
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        employee_list = Employee.objects.filter().order_by('id')
        page_number = request.query_params.get('page', 1)
        paginator = Paginator(employee_list, 2)
        page_obj = paginator.get_page(page_number)

        context = {
            "per_page": paginator.per_page,
            "num_pages": paginator.num_pages,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "next_page_number": page_obj.next_page_number() if page_obj.has_next() else 0,
            "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else 0,
            'list': EmployeeSerializer(page_obj.object_list, many=True,
                                       context={"request": request}).data
        }
        return Response(context, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        if data.get('department_id'):
            if Department.objects.filter(id=data.get('department_id')).exists():
                department = Department.objects.get(id=data.get('department_id'))
            else:
                return Response({'status': False, "message": "Department id does not exists"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': False, "message": "Please provide department id"},
                            status=status.HTTP_404_NOT_FOUND)

        employee = Employee.objects.create()
        employee.department = department
        if data.get('name'):
            employee.name = data.get('name')
        if request.FILES.get('photo'):
            employee.photo = request.FILES.get('photo')

        if request.FILES.get('resume'):
            employee.resume = request.FILES.get('resume')

        if data.get('date_of_joining'):
            employee.date_of_joining = data.get('date_of_joining')

        if data.get('date_of_birth'):
            employee.date_of_birth = data.get('date_of_birth')
        employee.save()

        return Response({"message": "Employee added successfully"}, status=status.HTTP_200_OK)
    