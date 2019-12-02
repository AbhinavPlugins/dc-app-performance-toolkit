import sys
import os
import re
from pathlib import Path
import requests
from datetime import datetime
import hashlib
import platform

from util.conf import JIRA_SETTINGS, CONFLUENCE_SETTINGS, TOOLKIT_VERSION

JIRA = 'jira'
CONFLUENCE = 'confluence'
BITBUCKET = 'bitbucket'
# List in value in case of specific output appears for some OS for command platform.system()
OS = {'macOS': ['Darwin'], 'Windows': ['Windows'], 'Linux': ['Linux']}
DT_REGEX = r'(\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2})'

BASE_URL = 'http://dcapps-ua-test.s3.us-east-2.amazonaws.com/stats.html?'
DEV_BASE_URL = 'http://dcapps-ua-test.s3.us-east-2.amazonaws.com/stats_dev.html?'


def application_type():
    app_type = None
    try:
        app_type = sys.argv[1]
    except IndexError:
        exit(0)
    return app_type.lower() if app_type.lower() in [JIRA, CONFLUENCE, BITBUCKET] else exit(0)


class StatisticFormer:

    def __init__(self, application_type):
        self.application_type = application_type
        self.run_id = ""
        self.application_url = ""
        self.tool_version = ""
        self.os = ""
        self.duration = 0
        self.concurrency = 0
        self.actual_duration = 0
        self.selenium_test_count = 0
        self.jmeter_test_count = 0

    @property
    def config_yml(self):
        if self.application_type.lower() == JIRA:
            return JIRA_SETTINGS
        elif self.application_type.lower() == CONFLUENCE:
            return CONFLUENCE_SETTINGS
        # TODO Bitbucket the same approach

    @property
    def __last_log_dir(self):
        results_dir = f'{Path(__file__).parents[2]}/results/{self.application_type.lower()}'
        try:
            last_run_log_dir = max([os.path.join(results_dir, d) for d in
                                os.listdir(results_dir)], key=os.path.getmtime)
            return last_run_log_dir
        except:
            exit(0)

    @property
    def last_bzt_log_file(self):
        with open(f'{self.__last_log_dir}/bzt.log') as log_file:
            log_file = log_file.readlines()
            return log_file

    @staticmethod
    def get_os():
        os_type = platform.system()
        for key, value in OS.items():
            os_type = key if os_type in value else os_type
        return os_type

    @staticmethod
    def id_generator(string):
        dt = datetime.now().strftime("%H%M%S%f")
        string_to_hash = str.encode(f'{dt}{string}')
        hash_str = hashlib.sha1(string_to_hash).hexdigest()
        min_hash = hash_str[:len(hash_str)//3]
        return min_hash

    def is_statistic_enabled(self):
        return True if str(self.config_yml.statistic_collector).lower() in ['yes', 'true'] else False

    def __validate_bzt_log_not_empty(self):
        if len(self.last_bzt_log_file) == 0:
            raise sys.exit(0)

    def get_duration_by_start_finish_strings(self):
        self.__validate_bzt_log_not_empty()
        first_string = self.last_bzt_log_file[0]
        last_string = self.last_bzt_log_file[len(self.last_bzt_log_file) - 1]
        start_time = re.findall(DT_REGEX, first_string)[0]
        start_datetime_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        finish_time = re.findall(DT_REGEX, last_string)[0]
        finish_datetime_obj = datetime.strptime(finish_time, '%Y-%m-%d %H:%M:%S')
        duration = finish_datetime_obj - start_datetime_obj
        return duration.seconds

    def get_duration_by_test_duration(self):
        self.__validate_bzt_log_not_empty()
        test_duration = None
        for string in self.last_bzt_log_file:
            if 'Test duration' in string:
                str_duration = string.split('duration:')[1].replace('\n', '')
                duration_datetime_obj = datetime.strptime(str_duration, ' %H:%M:%S')
                test_duration = duration_datetime_obj.hour*3600 + \
                                duration_datetime_obj.minute*60 + duration_datetime_obj.second
                break
        return test_duration

    def get_actual_run_time(self):
        run_time_bzt = self.get_duration_by_test_duration()
        run_time_start_finish = self.get_duration_by_start_finish_strings()
        return run_time_bzt if run_time_bzt else run_time_start_finish

    def get_actual_test_count(self):
        jmeter_test = ' jmeter_'
        selenium_test = ' selenium_'
        for line in self.last_bzt_log_file:
            if jmeter_test in line:
                self.jmeter_test_count = self.jmeter_test_count + 1
            elif selenium_test in line:
                self.selenium_test_count = self.selenium_test_count +  1

    def generate_statistics(self):
        self.application_url = self.config_yml.server_url
        self.run_id = self.id_generator(string=self.application_url)
        self.concurrency = self.config_yml.concurrency
        self.duration = self.config_yml.duration
        self.os = self.get_os()
        self.actual_duration = self.get_actual_run_time()
        self.tool_version = TOOLKIT_VERSION
        self.get_actual_test_count()


class StatisticSender:

    def __init__(self, statstic_instance):
        self.run_statistic = statstic_instance

    def send_request(self):
        base_url = BASE_URL
        params_string=f'app_type={self.run_statistic.application_type}&os={self.run_statistic.os}&' \
                      f'tool_ver={self.run_statistic.tool_version}&run_id={self.run_statistic.run_id}&' \
                      f'exp_dur={self.run_statistic.duration}&act_dur={self.run_statistic.actual_duration}&' \
                      f'sel_count={self.run_statistic.selenium_test_count}&jm_count={self.run_statistic.jmeter_test_count}&' \
                      f'concurrency={self.run_statistic.concurrency}'

        r = requests.get(url=f'{base_url}{params_string}')
        return r.content

if __name__ == '__main__':
    app_type = application_type()
    p = StatisticFormer(app_type)
    if p.is_statistic_enabled():
        p.generate_statistics()
        sender = StatisticSender(p)
        sender.send_request()
