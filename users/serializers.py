from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers

from logger.settings import console_logger
from users.models import User, Company
from users.utils import CreateUserUtils



# Serializers define the API representation.

class CompanySerializer(serializers.ModelSerializer):
    
    employees = serializers.SerializerMethodField(method_name="get_employees")
    
    def get_employees(self, obj):
        employees = obj.user.all()
        if employees:
            return EmployeeSerializer(employees, many=True).data
        return []

    class Meta:
        model = Company
        fields = ("id", "title", "employees")
        read_only_fields = ("user", )


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "role", "first_name", "last_name", )


class UserSerializer(serializers.ModelSerializer):

    companies = serializers.SerializerMethodField(method_name="get_companies")

    def get_companies(self, obj: User):
        companies = obj.companies.all()
        if companies:
            companies = CompanySerializer(companies, many=True).data
            return companies
        return []

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "companies", )


class RegistrationCompanyOwnerSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(max_length=255, write_only=True, style={"input_type": "password"})

    def save(self, **kwargs):
        return CreateUserUtils.create_company_owner(validated_data=self.validated_data)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", )
        extra_kwargs = {"password": {"write_only": True, "style": {"input_type": "password"}}}


class CreateCompanySerializer(serializers.Serializer):

    title: str = serializers.CharField(max_length=100, )

    def create(self, validate_data):
        company = Company.objects.create(title=validate_data["title"])
        company.user.add(self.context.get("request").user)
        return company

    class Meta:
        model = Company
        fields = ("title", "user", )


class CreateEmployeeSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(max_length=255, write_only=True, style={"input_type": "password"})
    company = serializers.IntegerField()

    def save(self, **kwargs):
        CreateUserUtils.create_employee(validated_data=self.validated_data, 
                                        creator=self.context["request"].user)
    
    class Meta:
        model = User
        fields = ("username", "email", "role", "password", "password2", "company")
        extra_kwargs = {"password": {"write_only": True, "style": {"input_type": "password"}}}


class LoginUserSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({"error": "Wrong login or password"})
