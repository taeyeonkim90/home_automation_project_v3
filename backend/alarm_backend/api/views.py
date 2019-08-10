from rest_framework import viewsets

from api.models import CronJob
from api.serializers import CronJobSerializer


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = CronJob.objects.all()
    serializer_class = CronJobSerializer
