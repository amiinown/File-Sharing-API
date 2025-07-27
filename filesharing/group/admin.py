from django.contrib import admin
from .models import Group, UserGroupPermission 

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    search_fields = ('name',)
    readonly_fields = ('created_at',)

@admin.register(UserGroupPermission)
class UserGroupPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'group',)
    list_filter = ('group',)
    search_fields = ('user__username', 'group__name')
