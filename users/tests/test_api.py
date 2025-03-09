import json
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User, Company
from logger.settings import console_logger


class UsersCompanyOwnerCredentialsAPITestCase(APITestCase):

    def setUp(self):
        company_owner = Group.objects.create(name="Company owner")
        
        create_user = Permission.objects.get(codename="add_user")
        delete_user = Permission.objects.get(codename="delete_user")

        create_company = Permission.objects.get(codename="add_company")
        change_company = Permission.objects.get(codename="change_company")
        delete_company = Permission.objects.get(codename="delete_company")
        view_company = Permission.objects.get(codename="view_company")

        company_owner.permissions.add(create_user)
        company_owner.permissions.add(delete_user)
        company_owner.permissions.add(create_company)
        company_owner.permissions.add(change_company)
        company_owner.permissions.add(delete_company)
        company_owner.permissions.add(view_company)
        company_owner.save()

        company_administrator = Group.objects.create(name="Company administrator")
        company_administrator.permissions.add(create_user)
        company_administrator.permissions.add(delete_user)
        company_administrator.save()


    def test_register_company_owner(self):
        """test register company owner"""
        console_logger.debug("started")
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner", "email":"companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
    
    def test_get_token_pair(self):
        """test get token obtain pair"""
        console_logger.debug("started")
        # register company owner
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner", "email":"companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
        # get refresh and access tokens
        url = reverse("token_obtain_pair")
        data = {"username": "test_company_owner", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        return response.data["access"]

    def test_create_company(self):
        """test company owner create company"""
        console_logger.debug("started")
        # register company owner
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner", "email":"companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
        # create company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-company")
        data = {"title": "Tiny Logistics"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"title": "Tiny Logistics"}
        self.assertEqual(expected, response.data)

    def test_create_company_administrator(self):
        """test company owner create company administrator"""
        console_logger.debug("started")
        # register company owner
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner", "email":"companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
        # create company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-company")
        data = {"title": "Tiny Logistics"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"title": "Tiny Logistics"}
        self.assertEqual(expected, response.data)
        # create company administrator
        url = reverse("create-employee")
        data = {"username": "company_administrator", "email": "administrator@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "ADMINISTRATOR"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"username": "company_administrator", "email": "administrator@mail.com", 
                    "role": User.Roles.ADMINISTRATOR, "company": 1}
        self.assertEqual(expected, response.data)

    def test_create_company_role_null(self):
        """test company owner create employee with role null"""
        console_logger.debug("started")
        # register company owner
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner", "email":"companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
        # create company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-company")
        data = {"title": "Tiny Logistics"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"title": "Tiny Logistics"}
        self.assertEqual(expected, response.data)
        # try create company null
        url = reverse("create-employee")
        data = {"username": "company_employee", "email": "employee@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "NULL"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_info(self):
        """test get user info"""
        console_logger.debug("started")
        # register company owner
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner", "email":"companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
        # create company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-company")
        data = {"title": "Tiny Logistics"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"title": "Tiny Logistics"}
        self.assertEqual(expected, response.data)
        # get user info
        url = reverse("user-info")
        response = client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = {"id": 1, "username": "test_company_owner", "email": "companyowner@mail.com", 
                    "first_name": "", "last_name": "", "role": "COMPANY_OWNER", 
                    "companies": [{"id": 1, "title": "Tiny Logistics", 
                                   "employees": [{"id": 1, "username": "test_company_owner",
                                                  "role": "COMPANY_OWNER", "first_name": "",
                                                  "last_name": ""}]}]}
        self.assertEqual(expected, response.data)

    def test_user_info_unautorized(self):
        """try get access to user info without token"""
        console_logger.debug("started")
        url = reverse("user-info")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_try_create_emolyee_without_owning_company(self):
        """try company owner create employee to someone else company"""
        console_logger.debug("started")
        # create owner comapny 2
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner_2", "email":"companyowner2@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner_2"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
        # try create employee without owning the company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-employee")
        data = {"username": "company_employee_2", "email": "employee2@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "ADMINISTRATOR"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class UsersAdministratorCredentialsAPITestCase(APITestCase):

    def setUp(self):
        company_owner = Group.objects.create(name="Company owner")
        
        create_user = Permission.objects.get(codename="add_user")
        delete_user = Permission.objects.get(codename="delete_user")

        create_company = Permission.objects.get(codename="add_company")
        change_company = Permission.objects.get(codename="change_company")
        delete_company = Permission.objects.get(codename="delete_company")
        view_company = Permission.objects.get(codename="view_company")

        company_owner.permissions.add(create_user)
        company_owner.permissions.add(delete_user)
        company_owner.permissions.add(create_company)
        company_owner.permissions.add(change_company)
        company_owner.permissions.add(delete_company)
        company_owner.permissions.add(view_company)
        company_owner.save()

        company_administrator = Group.objects.create(name="Company administrator")
        company_administrator.permissions.add(create_user)
        company_administrator.permissions.add(delete_user)
        company_administrator.save()

        # register company owner
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner", "email":"companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")

         # create company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-company")
        data = {"title": "Tiny Logistics"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")

        # create company administrator
        url = reverse("create-employee")
        data = {"username": "company_administrator", "email": "administrator@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "ADMINISTRATOR"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")

    def test_administrator_create_employee(self):
        """test administrator credentials to create employee for his company"""
        console_logger.debug("started")
        # login company administrator
        url = reverse("login")
        data = {"username": "company_administrator", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("company_administrator", response.data["username"])
        # administrator authorization credentials
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        # administrator create employee
        url = reverse("create-employee")
        data = {"username": "company_employee", "email": "employee@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "EMPLOYEE"}
        response = client.post(path=url, data=json.dumps(data),
                            content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"username": "company_employee", "email": "employee@mail.com", 
                    "role": User.Roles.EMPLOYEE, "company": 1}
        self.assertEqual(expected, response.data)
    
    def test_administrator_create_employee_to_someone_else_company(self):
        """test company administrator create employee to comeone else company"""
        console_logger.debug("started")
        # create company owner 2
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner_2", "email":"companyowner2@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner_2"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
        # create company 2
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-company")
        data = {"title": "Advanced Software"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"title": "Advanced Software"}
        self.assertEqual(expected, response.data)
        company = Company.objects.get(title="Advanced Software")
        # login company 1 administrator
        url = reverse("login")
        data = {"username": "company_administrator", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("company_administrator", response.data["username"])
        # administrator authorization credentials
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        # administrator create employee to someone else company
        url = reverse("create-employee")
        data = {"username": "company_employee", "email": "employee@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": company.id, "role": "EMPLOYEE"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_try_administrator_create_company(self):
        """test try adminstrator create company"""
        console_logger.debug("started")
        # login company administrator
        url = reverse("login")
        data = {"username": "company_administrator", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("company_administrator", response.data["username"])
        # create company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-company")
        data = {"title": "Advanced Software"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class UsersEmployeeCredentialsAPITestCase(APITestCase):

    def setUp(self):
        company_owner = Group.objects.create(name="Company owner")
        
        create_user = Permission.objects.get(codename="add_user")
        delete_user = Permission.objects.get(codename="delete_user")

        create_company = Permission.objects.get(codename="add_company")
        change_company = Permission.objects.get(codename="change_company")
        delete_company = Permission.objects.get(codename="delete_company")
        view_company = Permission.objects.get(codename="view_company")

        company_owner.permissions.add(create_user)
        company_owner.permissions.add(delete_user)
        company_owner.permissions.add(create_company)
        company_owner.permissions.add(change_company)
        company_owner.permissions.add(delete_company)
        company_owner.permissions.add(view_company)
        company_owner.save()

        company_administrator = Group.objects.create(name="Company administrator")
        company_administrator.permissions.add(create_user)
        company_administrator.permissions.add(delete_user)
        company_administrator.save()

        # register company owner
        company_owner = User.objects.create(username="test_company_owner", 
                                            email="companyowner@mail.com",
                                            role="COMPANY_OWNER")
        company_owner.set_password("qwerty")
        company_owner.save()

        # create company
        company = Company.objects.create(title="Tiny Logistics")
        company.user.add(company_owner)

        # create company employee
        employee = User.objects.create(username="company_employee", 
                                       email="employee@mail.com",
                                       role="EMPLOYEE")
        employee.set_password("qwerty")
        employee.save()
        company.user.add(employee)
        company.save()
        
    def test_employee_create_employee(self):
        """test employee create employee"""
        console_logger.debug("started")
        # login company employee
        url = reverse("login")
        data = {"username": "company_employee", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("company_employee", response.data["username"])
        # employee authorization credentials
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        # employee create employee
        url = reverse("create-employee")
        data = {"username": "company_employee_2", "email": "employee2@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "EMPLOYEE"}
        response = client.post(path=url, data=json.dumps(data),
                            content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_employee_create_company(self):
        """test employee create company"""
        console_logger.debug("started")
        # login company employee
        url = reverse("login")
        data = {"username": "company_employee", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("company_employee", response.data["username"])
        # create company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-company")
        data = {"title": "Advanced Software"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
