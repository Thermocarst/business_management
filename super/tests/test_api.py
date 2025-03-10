import json
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User, Company
from logger.settings import console_logger


class SuperAdminAPITestCase(APITestCase):

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

        self.admin = User.objects.create_superuser(username="admin",
                                                   email="admin@mail.com",
                                                   role="NULL")
        self.admin.set_password("qwerty")
        self.admin.save()
        
        self.company_owner = User.objects.create(username="test_company_owner", 
                                                 email="companyowner@mail.com",
                                                 role="COMPANY_OWNER")
        self.company_owner.set_password("qwerty")
        self.company_owner.groups.add(company_owner)
        self.company_owner.save()

        self.company = Company.objects.create(title="Tiny Logistics")
        self.company.user.add(self.company_owner)
        self.company.save()

    def test_admin_get_companies_owners(self):
        """"""
        # login admin
        url = reverse("login")
        data = {"username": "admin", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("admin", response.data["username"])
        # admin get company owners
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("companies-owners")
        response = client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_get_compnaies_owners(self):
        url = reverse("login")
        data = {"username": "test_company_owner", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("test_company_owner", response.data["username"])
        # user try get company owners
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("companies-owners")
        response = client.get(path=url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_admin_get_company_detail(self):
        """"""
        # login admin
        url = reverse("login")
        data = {"username": "admin", "password": "qwerty"}
        response = self.client.post(path=url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("admin", response.data["username"])
        # get company detail
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        url = reverse("company", kwargs={"pk": 1})
        response = client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = {"id": 1, "title": "Tiny Logistics", "employees": [
            {"id": 2, "username": "test_company_owner", "role": "COMPANY_OWNER", 
             "first_name": "", "last_name": ""}
        ]}
        self.assertEqual(expected, response.data)
