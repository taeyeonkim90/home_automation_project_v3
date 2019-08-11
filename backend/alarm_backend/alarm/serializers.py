from rest_framework import serializers

from .models import CronJob


class CronJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CronJob
        fields = ["id", "minute", "hour", "day_of_month", "month", "day_of_week", "command"]

    def validate_minute(self, value):
        self._validate_num_in_range(value, 0, 59)
        return value

    def validate_hour(self, value):
        self._validate_num_in_range(value, 0, 23)
        return value

    def validate_day_of_week(self, value):
        if "," in value:
            days = value.split(",")
            for day in days:
                self._validate_num_in_range(day, 0, 6)
            return value

        self._validate_num_in_range(value, 0, 6)
        return value

    @staticmethod
    def _validate_num_in_range(val: str, low_range: int, upper_range):
        try:
            int(val)
        except ValueError:
            raise serializers.ValidationError()

        num = int(val)
        if not (low_range <= num <= upper_range):
            raise serializers.ValidationError(f"Provided value is not within {low_range}-{upper_range} range")
