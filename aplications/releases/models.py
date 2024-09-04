from django.db import models
from aplications.users.models import Profile

"""
Notes: Massive changes the boolean 0 is direct and number 1
is massive changes
"""


class ReleaseModel(models.Model):
    id_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    default_code = models.CharField(max_length=20)
    change_code = models.CharField(max_length=20)
    massive_changes = models.BooleanField(default=0)
    before_img = models.URLField(max_length=200)
    after_img = models.URLField(max_length=200)

    def __str__(self):
        return self.default_code


class DeletePartsModel(models.Model):
    id_release = models.ForeignKey(ReleaseModel, on_delete=models.CASCADE)
    part = models.CharField(max_length=20)

    def __str__(self):
        return self.part
