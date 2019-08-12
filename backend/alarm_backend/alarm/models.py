from django.db import models


class Command(models.Model):
    name = models.CharField(max_length=100)
    target_file = models.CharField(max_length=100)

    def __str_(self):
        return f"{self.name}: {self.target_file}"


class CronJob(models.Model):
    minute = models.CharField(max_length=20, default="*")
    hour = models.CharField(max_length=20, default="*")
    day_of_month = models.CharField(max_length=20, default="*")
    month = models.CharField(max_length=20, default="*")
    day_of_week = models.CharField(max_length=20, default="*")
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

