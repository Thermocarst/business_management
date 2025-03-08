import json
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class UsersAPITestCase(APITestCase):

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
        """"""
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner", "email":"companyowner@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
    
    def test_get_token_pair(self):
        """"""
        # register company owner
        self.test_register_company_owner()
        # get refresh and access tokens
        url = reverse("token_obtain_pair")
        data = {"username": "test_company_owner", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        return response.data["access"]

    def test_create_company(self):
        """"""
        # get refresh and access tokens
        access_token: str = self.test_get_token_pair()
        # create company
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("create-company")
        data = {"title": "Tiny Logistics"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"title": "Tiny Logistics"}
        self.assertEqual(expected, response.data)
        return access_token

    def test_create_company_administrator(self):
        """"""
        # register company onwer and company
        access_token = self.test_create_company()
        # create company administrator
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("create-employee")
        data = {"username": "company_employee", "email": "employee@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "ADMINISTRATOR"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        expected = {"username": "company_employee", "email": "employee@mail.com", 
                    "role": User.Roles.ADMINISTRATOR, "company": 1}
        self.assertEqual(expected, response.data)

    def test_create_company_null(self):
        """"""
        # register company onwer and company
        access_token = self.test_create_company()
        # try create company null
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("create-employee")
        data = {"username": "company_employee", "email": "employee@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "NULL"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_info(self):
        """"""
        access_token = self.test_get_token_pair()
        # try create company null
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        url = reverse("user-info")
        response = client.get(url)
        self.assertAlmostEqual(status.HTTP_200_OK, response.status_code)
        expected = {"id": 1, "username": "test_company_owner", "email": "companyowner@mail.com", 
                    "first_name": "", "last_name": "", "role": "COMPANY_OWNER", "companies": []}
        self.assertEqual(expected, response.data)

    def test_user_info_unautorized(self):
        """"""
        url = reverse("user-info")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_try_create_emolyee_without_owninig_company(self):
        """"""
        """create owner comapny 2"""
        url = reverse("register-company-owner")
        data = {"username": "test_company_owner_2", "email":"companyowner2@mail.com",
                "password": "qwerty", "password2": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = "test_company_owner_2"         # {"username": "", "access": "", "refresh": ""}
        self.assertEqual(expected, response.data["username"])
        """try create employee without owning the company"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("create-employee")
        data = {"username": "company_employee_2", "email": "employee2@mail.com",
                "password": "qwerty", "password2": "qwerty", "company": 1, "role": "ADMINISTRATOR"}
        response = client.post(path=url, data=json.dumps(data),
                               content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
