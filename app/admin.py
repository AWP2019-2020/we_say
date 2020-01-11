from django.contrib import admin

from app import models

admin.site.register(models.Theme)
admin.site.register(models.Poll)
admin.site.register(models.Vote)