# -*- coding: utf-8 -*-
from utils import permission


def auth_get_key(data_list, opre_type):
    key_list = permission.auth_map.get(opre_type)
    code_list = list('0' * 32)
    for key_list_item in key_list:
        if str(key_list_item.get("function_id")) in data_list:
            code_list[key_list_item.get("auth_key") - 1] = '1'
    code_list.reverse()
    code = '0b'
    for code_list_item in code_list:
        code = code + code_list_item
    code = int(code, 2)
    return code


def auth_functions(auth_code, opre_type):
    key_list = permission.auth_map.get(opre_type)
    bits_real = list(bin(auth_code)[2:].zfill(32))
    bits_real.reverse()
    numbers = range(len(bits_real) + 1)[1:]
    bits_dict = dict(zip(numbers, bits_real))
    auth_dict = {}
    for key_index, key in bits_dict.iteritems():
        if key == '1':
            auth_dict[key_list[key_index-1].get("function_id")] = True
        else:
            auth_dict[key_list[key_index-1].get("function_id")] = False
    return auth_dict
