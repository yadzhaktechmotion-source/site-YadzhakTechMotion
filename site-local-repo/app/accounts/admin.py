from datetime import timedelta
from django.utils import timezone
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'phone',
        'is_active', 'is_staff', 'is_verified',
        'date_joined', 'colored_last_login',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_verified')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-last_login',)
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        ('Account Info', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_verified', 'groups', 'user_permissions'
            )
        }),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display_links = ('email', 'first_name', 'last_name')

    def colored_last_login(self, obj):
        """Display last login with color depending on recency."""
        if not obj.last_login:
            return format_html('<span style="color:#999;">Never logged in</span>')

        now = timezone.now()
        delta = now - obj.last_login

        if delta <= timedelta(days=7):
            color = "#0fa89f"      # green/turquoise
        elif delta <= timedelta(days=30):
            color = "#f4c430"      # gold
        else:
            color = "#c94e4e"      # red-gray

        return format_html('<span style="color:{};">{}</span>', color, obj.last_login.strftime("%Y-%m-%d %H:%M"))

    colored_last_login.short_description = "Last login"
