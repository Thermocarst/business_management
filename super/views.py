from django.shortcuts import render

from rest_framework import permissions, generics

from users.models import User, Company
from super.serializers import UserSerializer
# from users.serializers import CompanySerializer

# Create your views here.

class GetCompaniesOwnersView(generics.ListAPIView):
    model = User
    queryset = User.objects.filter(role=User.Roles.COMPANY_OWNER).prefetch_related("companies__user")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    