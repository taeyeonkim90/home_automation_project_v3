from typing import List

from .models import CronJob


class CronService:
    def update_cron_jobs(self, cron_jobs: List[CronJob]):
        for job in cron_jobs:
            pass
        pass

    @staticmethod
    def cron_job_to_str(cron_job: CronJob) -> str:
        crontab_line = "{} {} {} {} {} {}".format(cron_job.minute,
                                                  cron_job.hour,
                                                  cron_job.day_of_month,
                                                  cron_job.month,
                                                  cron_job.day_of_week,
                                                  cron_job.command.script_path)
        return crontab_line
