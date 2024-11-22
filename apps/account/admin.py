# yourapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from .models import CustomUser


class CustomUserAdmin(UserAdmin):

    def group_names(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    group_names.short_description = 'Рол'
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (_('address'), _('phone'), _('avatar'))}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': (_('address'), _('phone'), _('avatar'))}),
    )
    list_display = ['username', 'email', 'phone', 'address', 'group_names']
    search_fields = ['username', 'email', 'phone', 'address']


admin.site.register(CustomUser, CustomUserAdmin)
