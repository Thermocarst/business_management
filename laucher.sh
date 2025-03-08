
# run migrations
python manage.py makemigrations
python manage.py migrate

# dependencies and some data
echo "

from django.db import IntegrityError;


from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
try:
    company_owner = Group.objects.create(name=\"Company owner\")

    create_user = Permission.objects.get(codename=\"add_user\")
    delete_user = Permission.objects.get(codename=\"delete_user\")

    create_company = Permission.objects.get(codename=\"add_company\")
    change_company = Permission.objects.get(codename=\"change_company\")
    delete_company = Permission.objects.get(codename=\"delete_company\")
    view_company = Permission.objects.get(codename=\"view_company\")
    
    company_owner.permissions.add(create_user)
    company_owner.permissions.add(delete_user)
    company_owner.permissions.add(create_company)
    company_owner.permissions.add(change_company)
    company_owner.permissions.add(delete_company)
    company_owner.permissions.add(view_company)
    company_owner.save()

    company_administrator = Group.objects.create(name=\"Company administrator\")

    company_administrator.permissions.add(create_user)
    company_administrator.permissions.add(delete_user)
    company_administrator.save()

except IntegrityError:
    print(\"dependencies already created\");" | python manage.py shell
