# -*- coding: utf-8 -*-
from manage_users.models import Accounts
from rest_framework import status
from rest_framework.response import Response

from api.message import MessageError
from utils import permission


def auth_permission(function_id, operation_type, user):
    if operation_type == 'public':
        auth_code = user.code_public
    else:
        auth_code = user.code_group
    key_list = permission.auth_map.get('user')
    bit = [x for x in key_list if x.get("function_id") == function_id][0].get("auth_key") * -1
    bit_real = list(bin(auth_code)[2:].zfill(32))[bit]
    if bit_real == '1':
        return True
    else:
        return False


def auth_function_permission(function_id, operation_type):
    def _function_permission(func):
        def wrapper(self, request, *args, **kwargs):
            user = Accounts.objects.get(id=request.user.id)
            if operation_type == 'public':
                auth_code = user.code_public
            else:
                auth_code = user.code_group
            key_list = permission.auth_map.get('manage_users')
            bit = [x for x in key_list if x.get("function_id") == function_id][0].get("auth_key") * -1
            bit_real = list(bin(auth_code)[2:].zfill(32))[bit]
            if bit_real == '1':
                return func(self, request, *args, **kwargs)
            else:
                return_message = MessageError(code=403, message="You don't have this permission!")
                return Response(return_message.data(), status=status.HTTP_200_OK)
        return wrapper
    return _function_permission
