# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.views import logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView, jwt_response_payload_handler, api_settings

from api.message import MessageSuccess, MessageError


# 通过用户名密码认证得到token
# POST /auth/login/
class ObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        账户登录(获取token)
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(
                    api_settings.JWT_AUTH_COOKIE,
                    token,
                    expires=expiration,
                    httponly=True)
            response.data['success'] = True
            response.data['code'] = 200
            response.data['data'] = {'token': response.data['token']}
            del response.data['token']
            return response
        else:
            msgs = ''
            for error in serializer.errors:
                if error == 'non_field_errors':
                    msgs += serializer.errors[error][0]
                else:
                    msgs += error + ':' + serializer.errors[error][0] + '\n '
            message = MessageError(code=1001, message=msgs)
            return Response(message.data(), status=status.HTTP_200_OK)


# 账户登出
# GET /auth/logout/
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication, ))
def logout_user(request):
    """
    账户登出(会话删除)
    """
    data = request.GET.get("ok", "")
    if data:
        print(data)
    else:
        print('no data')
    logout(request)
    message = MessageSuccess(data="User Logout Success!")
    return Response(message.data(), status=status.HTTP_200_OK)
