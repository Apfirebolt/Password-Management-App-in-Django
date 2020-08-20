from django.contrib import admin
from . models import PasswordCategory, PasswordHint,FileEncrypt


admin.site.register(PasswordCategory)
admin.site.register(PasswordHint)
admin.site.register(FileEncrypt)

