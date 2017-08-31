# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import exception_handler


# 自定义错误信息返回
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response_data = response.data
        message_data = ''
        for res_data in dict(response_data):
            if res_data == "detail":
                message_data += res_data + ': ' + response_data[res_data] + '\n'
            else:
                message_data += res_data + ': ' + str(response_data[res_data][0]) + '\n'
            del response.data[res_data]
        response.data['code'] = response.status_code
        response.data['success'] = False
        response.data['message'] = message_data
        response.status_code = status.HTTP_200_OK
    return response
