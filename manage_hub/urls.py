from django.conf.urls import url
from manage_hub.views import HubViewSet


urlpatterns = [
    url(r'^', HubViewSet),
]
