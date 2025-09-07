from django.contrib import admin
from .models import Folder

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'parent', 'created_at')
    raw_id_fields = ('owner', 'group', 'parent')
    list_filter = ('owner',)
    search_fields = ('name', 'owner')
    ordering = ('created_at',)
    readonly_fields = ('created_at',)