from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import CustomUser, UserProfile, Education


class CustomUserAdmin(ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined',
                    'updated_at','last_login')
    list_filter = ('email', 'is_superuser')
    search_fields = ('email', 'is_superuser', 'last_name')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.site_header = "WeConnect App"
