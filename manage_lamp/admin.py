from django.contrib import admin
from manage_lamp import models


# Register your models here.


class LampAdmin(admin.ModelAdmin):
    list_display = ('sn', 'sequence', 'status', 'type', 'hub_id', 'is_repeated', 'rf_band', 'channel', 'address',
                    'registered_time', 'longitude', 'latitude', 'memo', 'is_deleted', 'created_time', 'updated_time',
                    'deleted_time')


admin.site.register(models.Lamp, LampAdmin)

