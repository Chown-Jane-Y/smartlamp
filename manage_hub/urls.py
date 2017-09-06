from django.conf.urls import url

from .views import HubViewSet


urlpatterns = [
    url(r'^', HubViewSet),
]
