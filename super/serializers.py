from rest_framework import serializers

from logger.settings import console_logger
from users.models import User, Company


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = ("id", "title")


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


