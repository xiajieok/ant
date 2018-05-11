from django.contrib import admin
from cow import models

# Register your models here.
admin.site.register(models.Assets)
admin.site.register(models.Server)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Tag)
admin.site.register(models.IDC)
admin.site.register(models.EventLog)
admin.site.register(models.Manufactory)