"""my_smartlamp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers

from manage_lamp import views as lamp_views
from manage_hub import views as hub_views

router = routers.DefaultRouter()
router.register(r'hubs', hub_views.HubViewSet)
router.register(r'lamps', lamp_views.LampViewSet)


hub_lamps_view = lamp_views.HubLampViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^hubs/(?P<hub_sn>[0-9]+)/lamps/', hub_lamps_view, name='hub-lamps-list'),      # /hubs/{id}/lamps
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
