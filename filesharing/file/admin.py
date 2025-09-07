from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_name', 'owner', 'group', 'folder__name', 'version', 'uploaded_at')
    raw_id_fields = ('owner', 'group', 'folder')
    search_fields = ('title', 'owner__username', 'group__name', 'folder__name')
    readonly_fields = ('uploaded_at',)