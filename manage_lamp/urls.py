from django.conf.urls import url
from .views import LampViewSet


urlpatterns = [
    url(r'^', LampViewSet),
]
