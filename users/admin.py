from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'email')
    search_fields = ('email', )
