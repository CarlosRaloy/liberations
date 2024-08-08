from django.db import models
from aplications.users.models import Profile

"""
Notes: Massive changes the boolean 0 is direct and number 1
is massive changes
"""


class ReleaseModel(models.Model):
    id_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    default_code = models.CharField(max_length=20)
    massive_changes = models.BooleanField(default=0)
    deleted_parts = models.CharField(max_length=20)
    before_img = models.FileField(upload_to="img/before")
    after_img = models.FileField(upload_to="img/after")

    def __str__(self):
        return self.default_code
