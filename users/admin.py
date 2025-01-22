from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'google_id')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'user_type', 'google_id')}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)