from django.contrib import admin
from .models import File, FileVersion

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'group', 'folder', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('group', 'folder')
    readonly_fields = ('created_at',)

@admin.register(FileVersion)
class FileVersionAdmin(admin.ModelAdmin):
    list_display = ('file__name', 'version', 'uploaded_at')
    search_fields = ('file__name', 'version')
    readonly_fields = ('uploaded_at',)
    list_filter = ('file',)