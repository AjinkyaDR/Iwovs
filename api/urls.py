from rest_framework import routers
from django.urls import path, include, re_path
# from django.conf.urls import url, include
from api import views as api_views
from accounts import views as accounts_views

router = routers.DefaultRouter()

router.register(r'login', api_views.LoginViewSet, basename='login')
router.register(r'department_list', api_views.DepartmentList, basename='department_list')
router.register(r'employee_list', api_views.EmployeeList, basename='employee_list')

urlpatterns = [
    re_path(r'^', include(router.urls)),]