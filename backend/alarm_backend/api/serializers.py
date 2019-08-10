from rest_framework import serializers

from api.models import CronJob


class CronJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CronJob
        fields = ["id", "minute", "hour", "day_of_month", "month", "day_of_week"]
