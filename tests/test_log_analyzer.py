import json
from inspect import getsourcefile
import os
import shutil
import subprocess
import unittest

test_module_path = os.path.abspath(getsourcefile(lambda: 0))
test_dir_path = os.path.dirname(test_module_path)
script_dir_path = os.path.dirname(test_dir_path)

TEST_DATA_DIR = os.path.join(test_dir_path, 'test_data')
TEST_INPUT_LOGS_DIR = os.path.join(test_dir_path, 'logs')
DEFAULT_CONFIG_PATH = os.path.join(script_dir_path, 'log_analyzer_config.json')
CUSTOM_CONFIG_PATH = os.path.join(test_dir_path, 'test_config.json')
TEST_REPORTS_DIR = os.path.join(test_dir_path, 'test_reports')

FIRST_LOG_NAME = 'nginx-access-ui.log-20170101'
LATEST_LOG_NAME = 'nginx-access-ui.log-20190930'
OTHER_SERVICE_LOG_NAME = 'other_service.log-20300101'
CORRECT_REPORT_NAME = 'correct_report-2019.09.30.html'

CORRECT_REPORT_PATH = os.path.join(TEST_DATA_DIR, CORRECT_REPORT_NAME)
EXPECTED_REPORT_NAME = 'report-2019.09.30.html'
EXPECTED_REPORT_PATH = os.path.join(TEST_REPORTS_DIR, EXPECTED_REPORT_NAME)

SHELL_ARGS = ['python', 'log_analyzer.py', '--config']


class SetConfigParam(unittest.TestCase):
    """Launch the script with a parameter "--config <filepath>"."""
    def setUp(self) -> None:
        os.mkdir(TEST_REPORTS_DIR)
        os.mkdir(TEST_INPUT_LOGS_DIR)
        log_names = [FIRST_LOG_NAME, LATEST_LOG_NAME, OTHER_SERVICE_LOG_NAME]
        for log_name in log_names:
            log_path = os.path.join(TEST_DATA_DIR, log_name)
            test_log = os.path.join(TEST_INPUT_LOGS_DIR, log_name)
            shutil.copy2(log_path, test_log)

        with open(CUSTOM_CONFIG_PATH, 'w') as config_file:
            config = {
                'REPORT_SIZE': 10,
                'REPORT_DIR': TEST_REPORTS_DIR,
                'LOG_DIR': TEST_INPUT_LOGS_DIR
            }
            json.dump(config, config_file)

    def test_set_config(self):
        res = subprocess.run([*SHELL_ARGS, CUSTOM_CONFIG_PATH])
        self.assertEqual(res.returncode, 0, msg='The script suddenly failed.')

        files_in_reports = [file for _, _, file in os.walk(TEST_REPORTS_DIR)]
        reason = f'The script doesn`t output a report {EXPECTED_REPORT_PATH}.'
        err_msg = f'{reason}\nAvailable files: {files_in_reports}'
        self.assertTrue(os.path.exists(EXPECTED_REPORT_PATH), msg=err_msg)
        self.assertTrue(os.path.isfile(EXPECTED_REPORT_PATH), msg=err_msg)

        with open(EXPECTED_REPORT_PATH, 'r') as report_file:
            report = report_file.read()

        with open(CORRECT_REPORT_PATH, 'r') as expected_report_file:
            expected_report = expected_report_file.read()

        self.assertEqual(report, expected_report, msg='Invalid report.')

    def tearDown(self) -> None:
        shutil.rmtree(TEST_REPORTS_DIR)
        os.remove(CUSTOM_CONFIG_PATH)
        shutil.rmtree(TEST_INPUT_LOGS_DIR)


class DefaultConfigParam(unittest.TestCase):
    """Launch the script with a bare parameter "--config"."""
    def setUp(self) -> None:
        os.mkdir(TEST_REPORTS_DIR)
        os.mkdir(TEST_INPUT_LOGS_DIR)
        log_names = [FIRST_LOG_NAME, LATEST_LOG_NAME, OTHER_SERVICE_LOG_NAME]
        for log_name in log_names:
            log_path = os.path.join(TEST_DATA_DIR, log_name)
            test_log = os.path.join(TEST_INPUT_LOGS_DIR, log_name)
            shutil.copy2(log_path, test_log)

        with open(DEFAULT_CONFIG_PATH, 'w') as config_file:
            config = {
                'REPORT_SIZE': 10,
                'REPORT_DIR': TEST_REPORTS_DIR,
                'LOG_DIR': TEST_INPUT_LOGS_DIR
            }
            json.dump(config, config_file)

    def test_default_config(self):
        res = subprocess.run(SHELL_ARGS)
        self.assertEqual(res.returncode, 0, msg='The script suddenly failed.')

        files_in_reports = [file for _, _, file in os.walk(TEST_REPORTS_DIR)]
        reason = f'The script doesn`t output a report {EXPECTED_REPORT_PATH}.'
        err_msg = f'{reason}\nAvailable files: {files_in_reports}'
        self.assertTrue(os.path.exists(EXPECTED_REPORT_PATH), msg=err_msg)
        self.assertTrue(os.path.isfile(EXPECTED_REPORT_PATH), msg=err_msg)

        with open(EXPECTED_REPORT_PATH, 'r') as report_file:
            report = report_file.read()

        with open(CORRECT_REPORT_PATH, 'r') as expected_report_file:
            expected_report = expected_report_file.read()

        self.assertEqual(report, expected_report, msg='Invalid report.')

    def tearDown(self) -> None:
        shutil.rmtree(TEST_REPORTS_DIR)
        os.remove(DEFAULT_CONFIG_PATH)
        shutil.rmtree(TEST_INPUT_LOGS_DIR)


if __name__ == '__main__':
    unittest.main()
