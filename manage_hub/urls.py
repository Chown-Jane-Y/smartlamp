from django.conf.urls import url
from manage_hub.views import HubViewSet as hub_viewset


urlpatterns = [
    url(r'^', hub_viewset),
]
