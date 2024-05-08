from django.db import models
from django.contrib.auth.models import User

ROLES = (
    (0, 'Hobbyist'),
    (1, 'Student'),
    (2, 'Developer'),
    (3, 'Researcher'),
    (4, 'Project Manager'),
    (5, 'Other'),
    )


# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLES, default=0)
