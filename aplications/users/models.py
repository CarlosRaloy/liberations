from django.contrib.auth.models import User
from django.db import models

""" 
-----------------------------------------------------------
    Note: nivel 0 = Normal User / nivel 1 = Admin User 
-----------------------------------------------------------
"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username