import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_misc_only_rest_resource:dropdown_data")
def app_dropdown_data(locust):
    r = locust.get('/rest/mischrsrestresource/1.0/data', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')
    assert 'isEstimationsInstalled' in content