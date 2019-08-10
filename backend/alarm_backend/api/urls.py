from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register("alarms", views.AlarmViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
