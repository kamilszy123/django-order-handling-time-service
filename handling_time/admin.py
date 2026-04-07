from django.contrib import admin
from .models import Account, HandlingTimeConfig

# Register your models here.
admin.site.register(Account)
admin.site.register(HandlingTimeConfig)