from django.conf.urls import url, include
from manage_user import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

# urlpatterns = [
#     url(r'^hubs/$', views.hubs_list),
#     url(r'^hubs/(?P<pk>[0-9]+)/$', views.hub_detail),
# ]
