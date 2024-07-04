from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

urlpatterns = [
    path('v1/api/employees/', views.EmployeeList.as_view(), name='employees'),
    path('v1/api/user/', views.UserList.as_view(), name='user'),
    path('v1/api/employees/register/', views.EmployeeRegister.as_view(), name='employee-register'),
    path('v1/api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]   