import subprocess
import sys

from django.conf import settings


class ScriptService:
    @staticmethod
    def kill_all_scripts() -> bool:
        try:
            scripts_dir = settings.SCRIPTS_DIR
            args = ["pkill", "-f", f"\"{scripts_dir}/test_script.py\""]
            command = " ".join(args)
            subprocess.check_output(command, shell=True, encoding=sys.stdout.encoding)
        except subprocess.CalledProcessError:
            return False
        return True
