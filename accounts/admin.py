# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import Group
from .models import Code

# Register your models here.

admin.site.unregister(Group)
admin.site.register(Code)
User = get_user_model()

class UserAdminConfig(UserAdmin):
    search_fields = ['email']
    
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    list_display = ['email','is_admin', 'user_name', 'phone_number','timestamp']
    list_filter = ['is_admin', 'is_staff', 'is_active']


    fieldsets = (
        (None, {'fields' : ('email', 'password', 'user_name', 'phone_number' )}),
        ('personal', {'fields': ()}),
        ('permissions', {'fields':('is_admin', 'is_staff', 'is_active', 'is_verified')}),

    ) 

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'phone_number', 'password1', 'password2')}
        ),
    )
    
    search_fields = ['email',]
    ordering = ['email',]
    filter_horizontal = ()


admin.site.register(User, UserAdminConfig)


