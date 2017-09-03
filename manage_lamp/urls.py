from django.conf.urls import url, include
from manage_lamp.views import LampViewSet


urlpatterns = [
    url(r'^', LampViewSet),
]

# urlpatterns = [
#     url(r'^hubs/$', views.hubs_list),
#     url(r'^hubs/(?P<pk>[0-9]+)/$', views.hub_detail),
# ]
