from alarm.models import CronJob
from alarm.services.cron import CrontabService, CronJobParser


class AlarmService:
    def __init__(self, crontab_service: CrontabService, job_parser: CronJobParser):
        self.crontab_service = crontab_service
        self.job_parser = job_parser

    def update_all_alarms(self):
        self.crontab_service.clear()

        alarm_jobs = CronJob.objects.all()
        for job in alarm_jobs:
            schedule = self.job_parser.get_schedule(job)
            command = self.job_parser.get_command(job)
            self.crontab_service.add_job(schedule, command)

        self.crontab_service.save()


class AlarmServiceFactory:
    @staticmethod
    def get_alarm_service() -> AlarmService:
        crontab_service = CrontabService()
        job_parser = CronJobParser()
        return AlarmService(crontab_service, job_parser)