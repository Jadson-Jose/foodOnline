from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomerUserAdmin(UserAdmin):
    list_display = (
        'email', 
        'first_name', 
        'last_name', 
        'username', 
        'role',
        'is_active'
    )
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'username', 'phone_number', 'role')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin')}),
    )


admin.site.register(User, CustomerUserAdmin)
admin.site.register(UserProfile)
