from django.urls import include, path
from rest_framework import routers

from alarm import views

router = routers.DefaultRouter()
router.register("alarms", views.AlarmViewSet)
router.register("commands", views.CommandViewSet)
router.register("alarm_statuses", views.AlarmStatusViewSet)


urlpatterns = [
    path("", include(router.urls)),
]