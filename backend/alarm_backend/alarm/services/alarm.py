from alarm.models import CronJob
from alarm.services.cron import CrontabService, CronJobParser
from alarm.services.script import ScriptService


class AlarmService:
    def __init__(self,
                 crontab_service: CrontabService,
                 script_service: ScriptService,
                 job_parser: CronJobParser):
        self.crontab_service = crontab_service
        self.script_service = script_service
        self.job_parser = job_parser

    def update_all_alarms(self):
        self.crontab_service.clear()

        alarm_jobs = CronJob.objects.all()
        for job in alarm_jobs:
            if job.is_active:
                schedule = self.job_parser.get_schedule(job)
                command = self.job_parser.get_command(job)
                self.crontab_service.add_job(schedule, command)

        self.crontab_service.save()

    def kill_all_scripts(self):
        self.script_service.kill_all_scripts()


class AlarmServiceFactory:
    @staticmethod
    def get_alarm_service() -> AlarmService:
        crontab_service = CrontabService()
        script_service = ScriptService()
        job_parser = CronJobParser()
        return AlarmService(crontab_service, script_service, job_parser)
