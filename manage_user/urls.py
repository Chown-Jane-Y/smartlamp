from django.conf.urls import url
from manage_user.views import UserViewSet


urlpatterns = [
    url(r'^', UserViewSet),
]


# urlpatterns = [
#     url(r'^hubs/$', views.hubs_list),
#     url(r'^hubs/(?P<pk>[0-9]+)/$', views.hub_detail),
# ]
