from crontab import CronTab

from alarm.models import CronJob


class CronJobParser:
    @staticmethod
    def get_schedule(cron_job: CronJob) -> str:
        schedule = "{} {} {} {} {}".format(cron_job.minute,
                                           cron_job.hour,
                                           cron_job.day_of_month,
                                           cron_job.month,
                                           cron_job.day_of_week)
        return schedule

    @staticmethod
    def get_command(cron_job: CronJob) -> str:
        return cron_job.command.script_path


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
