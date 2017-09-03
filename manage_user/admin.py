from django.contrib import admin
from manage_user import models


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role', 'email', 'is_superuser', 'is_active')


admin.site.register(models.User, UserAdmin)