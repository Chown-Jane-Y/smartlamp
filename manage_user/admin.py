from django.contrib import admin
from manage_user import models


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id')  # 'name', 'user', 'email', 'is_deleted', 'created_time', 'updated_time', 'deleted_time')


admin.site.register(models.User, UserAdmin)