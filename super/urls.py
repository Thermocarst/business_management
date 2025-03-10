from django.urls import path
from super.views import GetCompaniesOwnersView


urlpatterns = [
    path("companies-owners/", GetCompaniesOwnersView.as_view(), name="companies-owners"),
]
