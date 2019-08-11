from rest_framework import viewsets

from alarm.models import CronJob, Command, AlarmStatus
from alarm.serializers import CronJobSerializer, CommandSerializer, AlarmStatusSerializer


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = CronJob.objects.all()
    serializer_class = CronJobSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer


class AlarmStatusViewSet(viewsets.ModelViewSet):
    queryset = AlarmStatus.objects.all()
    serializer_class = AlarmStatusSerializer

"""
TODO:
    1. on CRUD, after each operation, repopulate crontab -> need crontab service -> delete and update
    2. alarm on/off alarm endpoint: update only
       need kill command
    3. !command get list: only get list
    4. script -> lock file

"""