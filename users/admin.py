from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from news.models import Ward

class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {
            'fields': (
                'role',
                'assigned_country', 'assigned_state', 'assigned_district',
                'assigned_city', 'assigned_village', 'assigned_ward'
            )
        }),
        ('User Location', {
            'fields': (
                'user_country', 'user_state', 'user_district', 'user_city'
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': (
                'role',
                'assigned_country', 'assigned_state', 'assigned_district',
                'assigned_city', 'assigned_village', 'assigned_ward'
            )
        }),
        ('User Location', {
            'fields': (
                'user_country', 'user_state', 'user_district', 'user_city','user_ward'
            )
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_ward":
            kwargs["queryset"] = Ward.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(User, CustomUserAdmin)

