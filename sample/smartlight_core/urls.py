# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from manage_users.views import UserViewSet, UserInformationViewSet, \
    UserPasswordViewSet, UserPermissionViewSet, UserEnableViewSet

schema_view = get_swagger_view(title='Conspace-core API')

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserInformationViewSet)
router.register(r'users', UserPasswordViewSet)
router.register(r'users', UserPermissionViewSet)
router.register(r'users', UserEnableViewSet)

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('manage_auth.urls', namespace='auth')),
    url(r'^API/', schema_view)
]
