from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import User, Otp

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_staff',)
    list_filter = ('is_staff',)
    readonly_fields = ('last_login', 'created_at')
    fieldsets = (
        ('User information', {'fields':('email', 'username', 'password',)}),
        ('Permissions', {'fields':('is_staff', 'is_active', 'last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {'fields':('email', 'username', 'is_staff', 'password1', 'password2')}),
    )
    search_fields = ('email', 'username')
    ordering = ('username',)
    filter_horizontal = []

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

@admin.register(Otp)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at')
    search_fields = ('user__email', 'otp_code')
    readonly_fields = ('created_at',)