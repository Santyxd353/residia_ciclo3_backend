from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_superuser')
    list_filter = ('role', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'national_id', 'phone', 'photo_url')}),
        ('Permisos', {'fields': ('role', 'is_active', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'national_id', 'phone',
                       'photo_url', 'password1', 'password2', 'role', 'is_active'),
        }),
    )
    search_fields = ('email', 'national_id', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups',)

admin.site.register(User, UserAdmin)
