from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin

from .models import User


# @admin.register(User)
# class UserAdmin(UserAdmin):
#     pass

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    pass