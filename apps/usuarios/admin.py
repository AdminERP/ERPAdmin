from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OldUserAdmin
from .models import *
# Register your models here.

class UserAdmin(OldUserAdmin):
    prepopulated_fields = {'username': ('first_name' , 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name',
                       'last_name',
                       'username',
                       'email','cedula','direccion','cargo','estado_civil','fecha_nacimiento','telefono',
                       'password1', 'password2', ),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email','cedula','direccion','cargo','estado_civil','fecha_nacimiento','telefono',)}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, UserAdmin);
#admin.site.register(Rol);
#admin.site.register(Cargo);
admin.site.register(Cliente);
