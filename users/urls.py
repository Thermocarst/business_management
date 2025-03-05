from django.urls import path
from users.views import InfoView, RegistrationCompanyOwnerView, CreateEmployeeView, LoginView, LogoutView, \
    CreateCompanyView

urlpatterns = [
    path("info/", InfoView.as_view(), name="user-info"),
    path("register-company-owner/", RegistrationCompanyOwnerView.as_view(), name="register-company-owner"),
    path("create-employee/", CreateEmployeeView.as_view(), name="create-employee"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create-company/", CreateCompanyView.as_view(), name="create-company"),
]
