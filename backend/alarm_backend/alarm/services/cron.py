from crontab import CronTab
from django.conf import settings

from alarm.models import CronJob


class CronJobParser:
    SCHEDULE_FORMAT = "{} {} {} {} {}"
    CRON_COMMAND_FORMAT = "python3 {}/{}"

    def get_schedule(self, cron_job: CronJob) -> str:
        schedule = self.SCHEDULE_FORMAT.format(cron_job.minute,
                                               cron_job.hour,
                                               cron_job.day_of_month,
                                               cron_job.month,
                                               cron_job.day_of_week)
        return schedule

    def get_command(self, cron_job: CronJob) -> str:
        scripts_dir = settings.SCRIPTS_DIR
        target_file = cron_job.command.target_file
        cron_command = self.CRON_COMMAND_FORMAT.format(scripts_dir, target_file)
        return cron_command


class CrontabService:
    def __init__(self):
        self.crontab = CronTab(user=True)

    def add_job(self, schedule: str, command: str):
        job = self.crontab.new(command=command)
        job.setall(schedule)

    def clear(self):
        self.crontab.remove_all()

    def save(self):
        self.crontab.write()