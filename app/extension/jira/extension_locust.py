import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='jira')

# @jira_measure("locust_app_specific_action")
# # @run_as_specific_user(username='admin', password='admin')  # run as specific user
# def app_specific_action(locust):
#     r = locust.get('/app/get_endpoint', catch_response=True)  # call app-specific GET endpoint
#     content = r.content.decode('utf-8')   # decode response content

#     token_pattern_example = '"token":"(.+?)"'
#     id_pattern_example = '"id":"(.+?)"'
#     token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
#     id = re.findall(id_pattern_example, content)    # get ID from response using regexp

#     logger.locust_info(f'token: {token}, id: {id}')  # log info for debug when verbose is true in jira.yml file
#     if 'assertion string' not in content:
#         logger.error(f"'assertion string' was not found in {content}")
#     assert 'assertion string' in content  # assert specific string in response content

#     body = {"id": id, "token": token}  # include parsed variables to POST request body
#     headers = {'content-type': 'application/json'}
#     r = locust.post('/app/post_endpoint', body, headers, catch_response=True)  # call app-specific POST endpoint
#     content = r.content.decode('utf-8')
#     if 'assertion string after successful POST request' not in content:
#         logger.error(f"'assertion string after successful POST request' was not found in {content}")
#     assert 'assertion string after successful POST request' in content  # assertion after POST request


@jira_measure("locust_app_specific_timetracking_role:role_worklog")
def app_role_worklog(locust):
    r = locust.get('/rest/adweb/2/assignee/roles/worklog/ATKEAA/admin', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')
    assert 'roleName' in content

@jira_measure("locust_app_specific_timetracking_role:role_assignee")
def app_role_assignee(locust):
    r = locust.get('/rest/adweb/2/assignee/roles/ATKEAA/admin', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')
    assert 'roleName' in content

@jira_measure("locust_app_specific_timetracking_role:legacy_worklog")
def app_legacy_worklog(locust):
    r = locust.get('/rest/adweb/2/legacyLogwork/project/ATKEAA', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')
    assert 'worklogroles' in content

@jira_measure("locust_app_specific_timetracking_role:subtaskenteries")
def app_subtaskenteries(locust):
    r = locust.get('/rest/adweb/2/timetracking/subTaskEntries/ATKEAA-54', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')
    assert 'subTaskRoleEntry' in content

@jira_measure("locust_app_specific_timetracking_role:timetracking")
def app_timetracking(locust):
    r = locust.get('/rest/adweb/2/timetracking/ATKEAA-56', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')
    assert 'estimates' in content

@jira_measure("locust_app_specific_timetracking_role:workratio")
def app_workratio(locust):
    r = locust.get('/rest/adweb/2/workRatioPerRole/ATKEAA-56', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')
    assert '[' in content
