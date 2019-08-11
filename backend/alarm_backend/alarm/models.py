from django.db import models


class AlarmStatus(models.Model):
    is_active = models.BooleanField(default=False)


class Command(models.Model):
    script_name = models.CharField(max_length=100)
    script_path = models.CharField(max_length=100)


class CronJob(models.Model):
    minute = models.CharField(max_length=20, default="*")
    hour = models.CharField(max_length=20, default="*")
    day_of_month = models.CharField(max_length=20, default="*")
    month = models.CharField(max_length=20, default="*")
    day_of_week = models.CharField(max_length=20, default="*")
    command = models.ForeignKey(Command, on_delete=models.CASCADE)

