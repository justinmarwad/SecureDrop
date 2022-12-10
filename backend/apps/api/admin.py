from django.contrib import admin
from .models import SecureDropUser

class SecureDropUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(SecureDropUser, SecureDropUserAdmin)

