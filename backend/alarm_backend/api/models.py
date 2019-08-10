from django.db import models


class CronJob(models.Model):
    minute = models.CharField(max_length=20, default="*")
    hour = models.CharField(max_length=20, default="*")
    day_of_month = models.CharField(max_length=20, default="*")
    month = models.CharField(max_length=20, default="*")
    day_of_week = models.CharField(max_length=20, default="*")
    script_path = models.CharField(max_length=100, default="TEST")
