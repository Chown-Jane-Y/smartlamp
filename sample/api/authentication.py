# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from api.message import MessageError
from api.permission import auth_map

from manage_users.models import Accounts


def auth_permission(function_id, operation_type, user):
    """判断用户是否有某一权限"""
    if operation_type == 'public':
        auth_code = user.code_public
    else:
        auth_code = user.code_group
    key_list = auth_map.get('user')
    bit = [x for x in key_list if x.get("function_name") == function_id][0].get("auth_key") * -1
    bit_real = list(bin(auth_code)[2:].zfill(32))[bit]
    if bit_real == '1':
        return True
    else:
        return False


def auth_function_permission(function_id, operation_type):
    """判断用户是否有某一权限，装饰器使用"""
    def _function_permission(func):
        def wrapper(self, request, *args, **kwargs):
            user = Accounts.objects.get(id=request.user.id)
            if operation_type == 'public':
                auth_code = user.code_public
            else:
                auth_code = user.code_group
            key_list = auth_map.get('manage_users')
            bit = [x for x in key_list if x.get("function_name") == function_id][0].get("auth_key") * -1
            bit_real = list(bin(auth_code)[2:].zfill(32))[bit]
            if bit_real == '1':
                return func(self, request, *args, **kwargs)
            else:
                return_message = MessageError(code=403, message="You don't have this permission!")
                return Response(return_message.data(), status=status.HTTP_200_OK)
        return wrapper
    return _function_permission


def auth_get_code(data_list, data_type):
    """通过传入权限列表，得到权限码"""
    key_list = auth_map.get(data_type)
    code_list = list('0' * 32)
    for key_list_item in key_list:
        if str(key_list_item.get("function_name")) in data_list:
            code_list[key_list_item.get("auth_key") - 1] = '1'
    code_list.reverse()
    code = '0b'
    for code_list_item in code_list:
        code = code + code_list_item
    code = int(code, 2)
    return code


def auth_get_data(auth_code, data_type):
    """通过传入权限码，得到权限列表"""
    key_list = auth_map.get(data_type)
    bits_real = list(bin(auth_code)[2:].zfill(32))
    bits_real.reverse()
    numbers = range(len(bits_real) + 1)[1:]
    bits_dict = dict(zip(numbers, bits_real))
    auth_dict = {}
    for key_index, key in bits_dict.iteritems():
        if key == '1':
            auth_dict[key_list[key_index-1].get("function_name")] = True
    return auth_dict
