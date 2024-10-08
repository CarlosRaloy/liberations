from django.contrib import admin
from .models import ReleaseModel, DeletePartsModel, EmailOptions

admin.site.register(ReleaseModel)
admin.site.register(DeletePartsModel)
admin.site.register(EmailOptions)

