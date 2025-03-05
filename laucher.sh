
# run migrations
python manage.py makemigrations
python manage.py migrate

# dependencies and some data
echo "

from django.db import IntegrityError;


from django.contrib.auth.models import Group
try:
    Group.objects.create(name=\"Company owner\")
except IntegrityError:
    print(\"dependencies already created\");" | python manage.py shell
