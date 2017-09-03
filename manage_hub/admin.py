from django.contrib import admin
from manage_hub import models

# Register your models here.


class HubAdmin(admin.ModelAdmin):
    list_display = ('id', 'sn', 'status', 'rf_band', 'channel', 'address', 'registered_time', 'longitude', 'latitude',
                    'memo', 'is_deleted', 'created_time', 'updated_time', 'deleted_time')


admin.site.register(models.Hub, HubAdmin)