from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import User, Company


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

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    companies = serializers.SerializerMethodField(method_name="get_companies")

    def get_companies(self, obj: User):
        companies = obj.companies.all()
        if companies:
            companies = CompanySerializer(companies, many=True).data
            return companies
        return []

    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "companies", )


class RegistrationCompanyOwnerSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(max_length=255, write_only=True, style={"input_type": "password"})

    def save(self, **kwargs):
        print(f"{self.validated_data=}")
        if self.validated_data["password"] == self.validated_data["password2"]:
            user = User.objects.create(username=self.validated_data["username"],
                                       email=self.validated_data["email"])
            user.set_password(self.validated_data["password"])
            user.role = User.Roles.COMPANY_OWNER
            print(f"{User.Roles.COMPANY_OWNER=}")
            user.save()
            company_owner_permission = Group.objects.get(name="Company owner")
            user.groups.add(company_owner_permission)
            return user
        else:
            raise serializers.ValidationError({"password": _("Passwords must match")})

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
        if self.validated_data["password"] == self.validated_data["password2"]:
            user = User.objects.create(username=self.validated_data["username"],
                                       email=self.validated_data["email"])
            user.set_password(self.validated_data["password"])
            user.role = User.Roles.EMPLOYEE
            user.save()
            user.companies.add(self.validated_data["company"])
            return user
        else:
            raise serializers.ValidationError({"password": _("Passwords must match")})

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "company")
        extra_kwargs = {"password": {"write_only": True}}


class LoginUserSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise ValueError("Incorrect credentials")
