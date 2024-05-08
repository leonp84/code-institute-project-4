from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import AppUser


class AppUserInline(admin.StackedInline):
    model = AppUser
    can_delete = False
    verbose_name_plural = "app users"


class UserAdmin(BaseUserAdmin):
    inlines = [AppUserInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
