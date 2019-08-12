from rest_framework import viewsets

from alarm.models import CronJob, Command, AlarmStatus
from alarm.serializers import CronJobSerializer, CommandSerializer, AlarmStatusSerializer
from alarm.services.alarm import AlarmServiceFactory
from alarm.services.script import ScriptService


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = CronJob.objects.all()
    serializer_class = CronJobSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alarm_service = AlarmServiceFactory.get_alarm_service()

    def perform_create(self, serializer: CronJobSerializer):
        serializer.save()
        self.alarm_service.update_all_alarms()

    def perform_update(self, serializer: CronJobSerializer):
        serializer.save()
        self.alarm_service.update_all_alarms()

    def perform_destroy(self, instance: CronJob):
        instance.delete()
        self.alarm_service.update_all_alarms()


class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer


class AlarmStatusViewSet(viewsets.ModelViewSet):
    queryset = AlarmStatus.objects.all()
    serializer_class = AlarmStatusSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.script_service = ScriptService()

    def perform_update(self, serializer: CronJobSerializer):
        serializer.save()
        if not serializer.validated_data.get("is_active"):
            self.script_service.kill_all_scripts()

"""
TODO:
    1. !on CRUD, after each operation, repopulate crontab -> need crontab service -> delete and update
    2. !alarm on/off alarm endpoint: update only
       need kill command
    3. !command get list: only get list
    4. !script -> lock file
    5. fixture. single alarm_status + multiple commands

"""