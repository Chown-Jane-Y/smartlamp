# -*- coding: utf-8 -*-
from django.conf.urls import url

from manage_auth.views import ObtainJSONWebToken, logout_user

urlpatterns = [
    url(r'^login/', ObtainJSONWebToken.as_view()),
    url(r'^logout/', logout_user),
]
