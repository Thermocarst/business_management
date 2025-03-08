from django.contrib.auth.models import Group
from rest_framework import serializers
from users.models import User, Company


class CreateUserUtils:

    def create_company_owner(validated_data: dict[str: str]):
        """
        create company owner
        :param validated_data: dict[str:str]
            example: {"username": "company_owner", "email": "companyowner@mail.com",
                      "password": "qwerty123", "password2": "qwerty123"}
        """
        return CreateUserUtils()._create_company_owner(validated_data)

    @staticmethod
    def create_employee(validated_data: dict[str: str], creator: User):
        """
        check user role and create user with user credentials
        :param validated_data: dict[str:str]
            example: {"username": "company_administrator", "email": "companyadministrator@mail.com", 
                      "password": "qwerty123", "password2": "qwerty123",
                      "company": 5, "role": "COMPANY_ADMINISTRATOR"}
        :param creator: <class User>, needed for create employee 
                        to check creator belongs this company
        """
        return CreateUserUtils()._create_company_employee_with_credentials(validated_data=validated_data, 
                                                                           creator=creator)

    def _set_password(self, validated_data):
        """
        :param validated_data: dict[str: str]
        :return: <class User> or raise exception
        """
        if validated_data["password"] != validated_data["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match"})
        user = User.objects.create(username=validated_data["username"],
                                    email=validated_data["email"])
        user.set_password(validated_data["password"])
        return user

    def _create_company_owner(self, validated_data: dict[str: str]):
        """
        :param validated_data: dict[str: str]
        :return: <class User>
        """
        user = self._set_password(validated_data)
        return self._register_company_owner(user=user)

    def _create_company_employee_with_credentials(self, validated_data: dict[str: str], creator: User):
        """
        :param validated_data: dict[str: str]
        :param creator: <class User> or None
        :return: <class User>
        """
        # check company credentials, before create user need check creator belongs this company
        company_id :int = validated_data.get("company")
        company = self.get_or_except_company(company_id=company_id, creator=creator)
        # check role
        role: str = self.get_or_except_role(role=validated_data.get("role"))
        # create user
        user = self._set_password(validated_data)
        return self._manager(user=user, role=role, company=company, creator=creator)

    @staticmethod
    def get_or_except_role(role: str):
        """"""
        if role in [User.Roles.EMPLOYEE, User.Roles.ADMINISTRATOR]:
            return role
        else:
            raise serializers.ValidationError({"role": "Empty role"})

    def _manager(self, role: str, user: User, company: int, creator: User):
        """
        check which role need to create
        """
        if role == User.Roles.ADMINISTRATOR:
            return self._create_administrator(user=user, company=company, creator=creator)
        else: # == User.Roles.EMPLOYEE
            return self._create_employee(user=user,company=company, creator=creator)

    @staticmethod
    def _register_company_owner(user: User):
        """company owner credentials"""
        user.role = User.Roles.COMPANY_OWNER
        user.save()
        company_owner_permission = Group.objects.get(name="Company owner")
        user.groups.add(company_owner_permission)
        return user

    @staticmethod
    def _create_administrator(user: User, company: int, creator: User):
        """company administrator credentials"""
        user.role = User.Roles.ADMINISTRATOR
        user.save()
        user.companies.add(company)
        company_owner_permission = Group.objects.get(name="Company administrator")
        user.groups.add(company_owner_permission)
        return user
            
    
    @staticmethod
    def _create_employee(user: User, company: int, creator: User):
        """employee credentials"""
        user.role = User.Roles.EMPLOYEE
        user.save()
        user.companies.add(company)
        return user
        
    def get_or_except_company(self, company_id, creator):
        """get company inst if creator belongs this company"""
        try:
            company = Company.objects.get(id=company_id, user=creator)
            return company
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company": "Company does not exist or creator haven't permissions"})
