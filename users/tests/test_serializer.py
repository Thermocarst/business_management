from django.test import TestCase

from logger.settings import console_logger
from users.models import User, Company
from users.serializers import (CompanySerializer, EmployeeSerializer, UserSerializer, RegistrationCompanyOwnerSerializer,
    CreateCompanySerializer, CreateEmployeeSerializer, LoginUserSerializer)


class UsersSerializersTestCase(TestCase):

    def setUp(self):
        # register company owner
        self.company_owner = User.objects.create(username="test_company_owner", 
                                                 email="companyowner@mail.com",
                                                 role="COMPANY_OWNER")
        self.company_owner.set_password("qwerty")
        self.company_owner.save()

        # create company
        self.company = Company.objects.create(title="Tiny Logistics")
        self.company.user.add(self.company_owner)
        
        # create company employee
        self.employee = User.objects.create(username="company_employee", 
                                            email="employee@mail.com",
                                            role="EMPLOYEE")
        self.employee.set_password("qwerty")
        self.employee.save()
        self.company.user.add(self.employee)
        self.company.save()

    def test_company_serializer(self):
        """"""
        console_logger.debug("started")
        result = CompanySerializer(self.company).data
        expected = {"id": 1, "title": "Tiny Logistics", 
                                   "employees": [{"id": 1, "username": "test_company_owner",
                                                  "role": "COMPANY_OWNER", "first_name": "",
                                                  "last_name": ""},
                                                  {"id": 2, "username": "company_employee",
                                                   "role": "EMPLOYEE", "first_name": "",
                                                   "last_name": ""}]}
        self.assertEqual(expected, result)

    def test_employee_serializer(self):
        """"""
        console_logger.debug("started")
        result = EmployeeSerializer(self.employee).data
        expected = {"id": 2, "username": "company_employee", "role": "EMPLOYEE", 
                    "first_name": "", "last_name": ""}
        self.assertEqual(expected, result)

    def test_user_serializer(self):
        """"""
        console_logger.debug("started")
        result = UserSerializer(self.company_owner).data
        expected = {"id": 1, "username": "test_company_owner", "email": "companyowner@mail.com", 
                    "first_name": "", "last_name": "", "role": "COMPANY_OWNER", 
                    "companies": [{"id": 1, "title": "Tiny Logistics", 
                                   "employees": [{"id": 1, "username": "test_company_owner",
                                                  "role": "COMPANY_OWNER", "first_name": "",
                                                  "last_name": ""},
                                                  {"id": 2, "username": "company_employee",
                                                   "role": "EMPLOYEE", "first_name": "",
                                                   "last_name": ""}]}]}
        self.assertEqual(expected, result)

    def test_register_comapny_owner_serializer(self):
        """"""
        console_logger.debug("started")
        data = {"username": "company_owner", "email": "companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        result = RegistrationCompanyOwnerSerializer(data).data
        expected = {"username": "company_owner", "email": "companyowner@mail.com"}
        self.assertEqual(expected, result)

    def test_create_company_serializer(self):
        """"""
        console_logger.debug("started")
        data = {"title": "Advanced Software"}
        result = CreateCompanySerializer(data).data
        expected = {"title": "Advanced Software"}
        self.assertEqual(expected, result)

    def test_create_employee_serializer(self):
        """"""
        console_logger.debug("started")
        data = {"username": "company_employee", "email": "employee@mail.com",
                "role": "EMPLOYEE", "password": "qwerty", "password2": "qwerty",
                "company": 1}
        result = CreateEmployeeSerializer(data).data
        expected = {"username": "company_employee", "email": "employee@mail.com",
                    "role": "EMPLOYEE", "company": 1}
        self.assertEqual(expected, result)

    def test_login_serializer(self):
        """"""
        console_logger.debug("started")
        data = {"username": "company_employee", "password": "qwerty"}
        result = LoginUserSerializer(data).data
        expected = {"username": "company_employee"}
        self.assertEqual(expected, result)
