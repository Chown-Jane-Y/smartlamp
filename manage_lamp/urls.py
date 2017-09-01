from django.conf.urls import url, include
from manage_lamp import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'lamps', views.LampViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

# urlpatterns = [
#     url(r'^hubs/$', views.hubs_list),
#     url(r'^hubs/(?P<pk>[0-9]+)/$', views.hub_detail),
# ]
