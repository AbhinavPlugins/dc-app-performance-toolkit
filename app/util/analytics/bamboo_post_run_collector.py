import re
from multiprocessing.pool import ThreadPool

from util.api.bamboo_clients import BambooClient
from util.conf import BAMBOO_SETTINGS
from multiprocessing import cpu_count

pool = ThreadPool(processes=cpu_count() * 3)


class BambooPostRunCollector:

    def __init__(self, locust_log):
        self.client = BambooClient(host=BAMBOO_SETTINGS.server_url,
                                   user=BAMBOO_SETTINGS.admin_login, password=BAMBOO_SETTINGS.admin_password)
        self.locust_log = locust_log
        self.locust_build_job_results = self.parallel_get_all_builds_results()

    def parallel_get_all_builds_results(self):
        locust_log_lines = self.locust_log.get_locust_log()
        build_job_id_list = []
        for string in locust_log_lines:
            build_job_id = re.search(r"\|.*\|", string)
            if build_job_id:
                build_job_id = build_job_id.group()
                build_job_id_list.append(build_job_id.replace('|', ''))

        all_builds_job_results_lists = pool.map(self.client.get_build_job_results, [i for i in build_job_id_list])
        return all_builds_job_results_lists

    @property
    def unexpected_status_plan_count(self):
        unexpected_finished_plan_count = 0
        for build_result in self.locust_build_job_results:
            plan_name = build_result['plan']['name']
            plan_result = build_result['state']
            expected_status = re.search(r'Project \d+ - \d+ - Plan (.*) - Job \d+', plan_name)
            if not expected_status:
                raise Exception(f'ERROR: Could not parse expected plan status from the plan name {plan_name}')
            expected_status = expected_status.group(1)
            if expected_status not in plan_result:
                unexpected_finished_plan_count = unexpected_finished_plan_count + 1
        return unexpected_finished_plan_count

    def get_plan_count_with_n_queue(self, n_sec):
        plan_count_with_n_sec = 0
        for build_result in self.locust_build_job_results:
            if build_result['queueTimeInSeconds'] >= n_sec:
                plan_count_with_n_sec = plan_count_with_n_sec + 1
        return plan_count_with_n_sec

    @property
    def unexpected_duration_plan_count(self):
        possible_diff_perc = 10
        expected_yml_build_duration = BAMBOO_SETTINGS.default_dataset_plan_duration
        expected_min_duration = expected_yml_build_duration - expected_yml_build_duration*possible_diff_perc/100
        expected_max_duration = expected_yml_build_duration + expected_yml_build_duration*possible_diff_perc/100
        unexpected_duration_plans_count = 0
        for build_result in self.locust_build_job_results:
            if not expected_min_duration <= build_result['buildDuration']/1000 <= expected_max_duration:
                unexpected_duration_plans_count = unexpected_duration_plans_count + 1
        return unexpected_duration_plans_count
