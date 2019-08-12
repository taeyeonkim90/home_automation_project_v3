import tempfile
import shutil
from typing import Dict

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from crontab import CronTab

from alarm.services.cron import CrontabService, CronJobParser
from alarm.services.script import ScriptService
from alarm.services.alarm import AlarmService
from alarm.serializers import CronJobSerializer
from alarm.models import CronJob, Command


class TempDirectory:
    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp()
        return self.temp_dir

    def __exit__(self, *args):
        shutil.rmtree(self.temp_dir)


class CronJobSerializerTest(TestCase):
    def setUp(self):
        self._create_test_fixture()

    def tearDown(self) -> None:
        for model in Command.objects.all():
            model.delete()

    def _create_test_fixture(self):
        command = Command(name="name",
                          target_file="path")
        command.save()

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
            with self.assertRaises(ValidationError):
                self._test_validation(data)

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
            with self.assertRaises(ValidationError):
                self._test_validation(data)

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
            with self.assertRaises(ValidationError):
                self._test_validation(data)

    def _generate_data(self, minute: str, hour: str, day_of_month: str, day_of_week: str) -> Dict[str, str]:
        command = Command.objects.all()[0]

        data = {"minute": minute,
                "hour": hour,
                "day_of_month": day_of_month,
                "day_of_week": day_of_week,
                "command": command.id}
        return data

    def _test_validation(self, data: dict):
        serializer = CronJobSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))


class CronJobParserTest(TestCase):
    def setUp(self) -> None:
        self.parser = CronJobParser()

    def test_get_schedule(self):
        job = CronJob()
        schedule = self.parser.get_schedule(job)
        self.assertEqual(schedule, "* * * * *")

    def test_get_command(self):
        command = Command(name="name",
                          target_file="path")
        job = CronJob(command=command)
        command = self.parser.get_command(job)
        self.assertTrue(command.endswith("path"))


class AlarmServiceTest(TestCase):
    def setUp(self) -> None:
        crontab_service = CrontabService()
        script_service = ScriptService()
        parser = CronJobParser()
        self.alarm_service = AlarmService(crontab_service, script_service, parser)

        self._create_test_fixture()
        self._clear_crontab()

    def tearDown(self) -> None:
        for model in CronJob.objects.all():
            model.delete()

        for model in Command.objects.all():
            model.delete()

        self._clear_crontab()

    def _create_test_fixture(self):
        command = Command(name="name",
                          target_file="path")
        command.save()

        for i in range(10):
            job = CronJob(command=command, is_active=True)
            job.save()

    def _clear_crontab(self):
        crontab = CronTab(user=True)
        crontab.remove_all()
        crontab.write()

    def test_update_all_alarms(self):
        crontab = CronTab(user=True)
        self.assertEqual(len(crontab), 0)

        self.alarm_service.update_all_alarms()

        crontab = CronTab(user=True)
        self.assertEqual(len(crontab), 10)

