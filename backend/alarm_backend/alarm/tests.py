import tempfile
import shutil
from typing import Dict

from django.test import TestCase
from crontab import CronTab

from alarm.serializers import CronJobSerializer


class TempDirectory:
    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp()
        return self.temp_dir

    def __exit__(self, *args):
        shutil.rmtree(self.temp_dir)


class CrontabTest(TestCase):
    def tearDown(self) -> None:
        cron = CronTab(user=True)
        cron.remove_all()

    def test_job_create(self):
        cron = CronTab(user=True)
        cron.new("pwd")
        cron.write()

        jobs_found = list(cron.find_command("pwd"))
        self.assertTrue(len(jobs_found))
        for job in jobs_found:
            self.assertTrue(job.is_valid())


class CronJobSerializerTest(TestCase):
    def test_minute_validation(self):
        data_list = [
            self._generate_data("0", "1", "1", "1"),
            self._generate_data("20", "1", "1", "1"),
            self._generate_data("59", "1", "1", "1"),
        ]
        for data in data_list:
            self._test_validation(data)

    def test_minute_validation_fail(self):
        data_list = [
            self._generate_data("-1", "1", "1", "1"),
            self._generate_data("60", "1", "1", "1"),
            self._generate_data("a", "1", "1", "1"),
        ]
        for data in data_list:
            self._test_validation_fail(data)

    def test_hour_validation(self):
        data_list = [
            self._generate_data("1", "0", "1", "1"),
            self._generate_data("1", "12", "1", "1"),
            self._generate_data("1", "23", "1", "1"),
        ]
        for data in data_list:
            self._test_validation(data)

    def test_hour_validation_fail(self):
        data_list = [
            self._generate_data("1", "-1", "1", "1"),
            self._generate_data("1", "24", "1", "1"),
            self._generate_data("1", "a", "1", "1"),
        ]
        for data in data_list:
            self._test_validation_fail(data)

    def test_day_of_week_validation(self):
        data_list = [
            self._generate_data("1", "1", "1", "1"),
            self._generate_data("1", "1", "1", "3"),
            self._generate_data("1", "1", "1", "6"),
            self._generate_data("1", "1", "1", "1,6"),
            self._generate_data("1", "1", "1", "1,2,3,4,5,6"),
        ]
        for data in data_list:
            self._test_validation(data)

    def test_day_of_week_validation_fail(self):
        data_list = [
            self._generate_data("1", "1", "1", "-1"),
            self._generate_data("1", "1", "1", "7"),
            self._generate_data("1", "1", "1", ","),
            self._generate_data("1", "1", "1", ",1"),
        ]
        for data in data_list:
            self._test_validation_fail(data)

    def _generate_data(self, minute: str, hour: str, day_of_month: str, day_of_week: str) -> Dict[str, str]:
        data = {"minute": minute,
                "hour": hour,
                "day_of_month": day_of_month,
                "day_of_week": day_of_week}
        return data

    def _test_validation(self, data: dict):
        serializer = CronJobSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def _test_validation_fail(self, data: dict):
        serializer = CronJobSerializer(data=data)
        self.assertFalse(serializer.is_valid())
