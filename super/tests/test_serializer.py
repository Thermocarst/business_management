from django.test import TestCase
from users.models import User, Company
from super.serializers import CompanySerializer, UserSerializer


class SuperSerializersTestCase(TestCase):

    def setUp(self):
        
        self.admin = User.objects.create_superuser(username="admin",
                                                   email="admin@mail.com",
                                                   role="NULL")
        self.admin.set_password("qwerty")
        self.admin.save()
        
        self.company_owner = User.objects.create(username="test_company_owner", 
                                                 email="companyowner@mail.com",
                                                 role="COMPANY_OWNER")
        self.company_owner.set_password("qwerty")
        self.company_owner.save()

        self.company = Company.objects.create(title="Tiny Logistics")
        self.company.user.add(self.company_owner)
        self.company.save()

    def test_company_serializer(self):
        """"""
        result = CompanySerializer(self.company).data
        expected = {"id": 1, "title": "Tiny Logistics"}
        self.assertEqual(expected, result)

    def test_user_serializator(self):
        """"""
        result = UserSerializer(self.company_owner).data
        expected = {"id": 2, "username": "test_company_owner", "role": "COMPANY_OWNER", 
                    "first_name": "", "last_name": "", "comapnies": [{"id": 1, "title": "Tiny Logistics"}, ]}
