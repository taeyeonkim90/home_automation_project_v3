from rest_framework import viewsets

from .models import CronJob
from .serializers import CronJobSerializer


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = CronJob.objects.all()
    serializer_class = CronJobSerializer

"""
TODO:
    1. on CRUD, after each operation, repopulate crontab -> need crontab service -> delete and update
    2. alarm on/off alarm endpoint: update only
       need kill command
    3. command get list: only get list
    4. script -> lock file

"""