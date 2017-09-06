# -*- coding: utf-8 -*-
import django.utils.timezone as timezone
from .models import Logs


class ALog(object):

    def __init__(self, content_type, content_id):
        self.content_type = content_type
        self.content_id = content_id

    def record(self, action, result):
        admin_log = Logs(
            content_type=self.content_type,
            content_type_id=self.content_id,
            action=action,
            running_status=result,
            running_time=timezone.now().strftime("%Y-%m-%d %H:%I:%S")
        )
        try:
            admin_log.save()
            return True
        except Exception as e:
            print '\033[1;31;44m%s !\033[0m' % e
            return False
