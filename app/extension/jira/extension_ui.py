import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from util.conf import JIRA_SETTINGS
from selenium_ui.jira.pages.pages import Login, Issue, PopupManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    #issue_page = Issue(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']
        issue_id = datasets['custom_issue_id']

    # @print_timing("selenium_app_custom_action_edit_timetracking")
    # def measure():
    #
    #     issue_page = Issue(webdriver, issue_id=datasets['custom_issue_id'])
    #
    #     @print_timing("selenium_app_custom_action_edit_timetracking:open_edit_issue_form")
    #     def sub_measure():
    #         issue_page.go_to_edit_issue()  # open editor
    #     sub_measure()
    #
    #     issue_page.fill_summary_edit()  # edit summary
    #     issue_page.fill_description_edit("Editing to add time tracking info")  # edit description
    #     issue_page.set_resolution()
    #
    #     @print_timing("selenium_app_custom_action_edit_timetracking:fill_timetracking")
    #     def sub_measure():
    #         issue_page.fill_timetracking_role("2h") #time tracking
    #     sub_measure()
    #
    #     @print_timing("selenium_app_custom_action_edit_timetracking:assign_role")
    #     def sub_measure():
    #         issue_page.assign_to_me_role()
    #     sub_measure()
    #
    #     # @print_timing("selenium_app_custom_action_edit_timetracking:fill_logwork")
    #     # def sub_measure():
    #     #     issue_page.fill_logwork_role("1h") #logwork
    #     # sub_measure()
    #
    #     @print_timing("selenium_app_custom_action_edit_timetracking:save_edit_issue_form")
    #     def sub_measure():
    #         issue_page.edit_issue_submit()  # submit edit issue
    #         issue_page.wait_for_issue_title()
    #     sub_measure()
    # measure()
    #
    # # @print_timing("selenium_app_custom_action_create_timetracking")
    # # def measure():
    #
    # #     issue_modal = Issue(webdriver)
    #
    # #     @print_timing("selenium_create_timetracking:open_create_issue_form")
    # #     def sub_measure():
    # #         issue_modal.open_create_issue_modal()  # open create
    # #     sub_measure()
    #
    # #     @print_timing("selenium_create_issue:fill_and_submit_issue_form")
    # #     def sub_measure():
    # #         issue_modal.fill_summary_create()  # Fill summary field
    # #         issue_modal.fill_description_create("Testing !!!")  # Fill description field
    # #         issue_modal.assign_to_me()  # Click assign to me
    # #         issue_modal.set_resolution()  # Set resolution if there is such field
    # #         issue_modal.set_issue_type()  # Set issue type, use non epic type
    # #     sub_measure()
    #
    # #     # @print_timing("selenium_create_timetracking:fill_timetracking")
    # #     # def sub_measure():
    # #     #     issue_page.fill_timetracking_role_create("3h", webdriver) #time tracking
    # #     # sub_measure()
    #
    # #     @print_timing("selenium_create_timetracking:assign_role")
    # #     def sub_measure():
    # #         issue_modal.assign_to_me_role()
    # #     sub_measure()
    #
    # #     @print_timing("selenium_create_timetracking:fill_logwork")
    # #     def sub_measure():
    # #         issue_modal.fill_logwork_role("30m") #logwork
    # #     sub_measure()
    #
    # #     @print_timing("selenium_create_timetracking:save_edit_issue_form")
    # #     def sub_measure():
    # #         issue_modal.submit_issue()
    # #     sub_measure()
    # # measure()
    # # PopupManager(webdriver).dismiss_default_popup()
    #
    # @print_timing("selenium_app_role_based_tracking")
    # def measure():
    #     @print_timing("selenium_app_role_based_tracking:view_issue")
    #     def sub_measure():
    #         page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{datasets['custom_issue_key']}")
    #         page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
    #         page.wait_until_visible((By.ID, "log-work-link"))  # Wait for you app-specific UI element by ID selector
    #     sub_measure()
    #
    #     @print_timing("selenium_app_role_based_tracking:sprint_workloadTab")
    #     def sub_measure():
    #         page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/AANES?selectedItem=com.adweb.estimations.estimationUpdate:sprint-workloadTab")
    #         page.wait_until_visible((By.ID, "sprint-workload-page"))
    #     sub_measure()
    #
    #     @print_timing("selenium_app_role_based_tracking:estimation_reports")
    #     def sub_measure():
    #         page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/ConfigureReport.jspa?viewOption=roleWise&reportKey=com.adweb.estimations.estimationUpdate%3Aestimations-by-roles-report")
    #         page.wait_until_visible((By.CLASS_NAME, "timeReportHeader"))
    #     sub_measure()
    #
    #     @print_timing("selenium_app_role_based_tracking:estimation_accuracy_reports")
    #     def sub_measure():
    #         page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/ConfigureReport.jspa?projectId=-1&userId=all&issues=all&fixVersion=-1&filterId=-1&projectRole=all&selectedProjectId=10396&reportKey=com.adweb.estimations.estimationUpdate%3Aestimation-accuracy-by-roles")
    #         page.wait_until_visible((By.CLASS_NAME, "timeReportHeader"))
    #     sub_measure()
    #
    #     @print_timing("selenium_app_role_based_tracking:app_jql_functions")
    #     def sub_measure():
    #         page.go_to_url(f'{JIRA_SETTINGS.server_url}/issues/?jql="Time Tracking (By Roles)" = timeTrackingRole() AND "Assignees (By Roles)" = assignedRole() AND "Time Tracking (By Roles)" = originalEstByRole("")')
    #         page.wait_until_visible((By.CLASS_NAME, "results-panel"))
    #     sub_measure()
    # measure()


# def app_specific_action_logwork(webdriver, datasets):
#     page = BasePage(webdriver)
#     @print_timing("selenium_app_custom_action_timetracking:log_work")
#     def measure():
#         page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{datasets['custom_issue_key']}")
#         page.wait_until_clickable((By.ID, "log-work-link")).click()
#         page.wait_until_clickable((By.ID, "log-work-time-logged")).send_keys("1h")
#         role_dropdown = Select(page.get_element((By.ID, "log-work-role")))
#         role_dropdown.select_by_index(1)
#
#         @print_timing("selenium_app_custom_action_timetracking:submit_log_work_form")
#         def sub_measure():
#             page.wait_until_clickable((By.ID, "aui-dialog-log")).click()
#             page.wait_until_visible((By.CLASS_NAME, "aui-message-success"))
#         sub_measure()

def app_specific_action_misc_logwork(webdriver, datasets):
    page = BasePage(webdriver)
    wait = WebDriverWait(webdriver, 10)

    @print_timing("selenium_app_custom_action_misc:log_work")
    @print_timing("selenium_app_custom_action")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/Dashboard.jspa")

        logwork_dropdown = page.wait_until_clickable((By.ID, "log-misc-hours-link"))
        logwork_dropdown.click()

        page.wait_until_clickable((By.CLASS_NAME, "trigger-dialog")).click()
        page.wait_until_clickable((By.ID, "log-work-time-logged")).send_keys("1h")

        @print_timing("selenium_app_custom_action_misc:submit_log_work_form")
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.wait_until_clickable((By.ID, "log-work-submit")).click()

            wait.until(EC.staleness_of(logwork_dropdown))

            page.wait_until_clickable((By.ID, "log-misc-hours-link"))

        sub_measure()
    measure()

def app_specific_action_misc_report(webdriver, datasets):
    page = BasePage(webdriver)
    @print_timing("selenium_app_custom_action_misc:view_report")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/ConfigureReport.jspa?selectedProjectId=10396&projectSprint=0&userID=all&reportKey=au.com.adweb.plugin.mischrs:misc-hours-report")

        page.wait_until_visible((By.CLASS_NAME, "timeReport"))
    measure()

def app_specific_action_misc_config(webdriver, datasets):
    page = BasePage(webdriver)

    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    @print_timing("selenium_app_custom_action_misc:configure_project")

    def measure():
        @print_timing("selenium_app_custom_action_misc:user_login")
        def sub_measure():
            def app_specific_user_login(username='admin', password='admin'):
                login_page = Login(webdriver)
                login_page.delete_all_cookies()
                login_page.go_to()
                login_page.set_credentials(username=username, password=password)
                if login_page.is_first_login():
                    login_page.first_login_setup()
                if login_page.is_first_login_second_page():
                    login_page.first_login_second_page_setup()
                login_page.wait_for_page_loaded()

            app_specific_user_login(username='admin', password='admin')
        sub_measure()

        @print_timing("selenium_app_custom_action_misc:load_configure_project_page")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/MiscHoursConfig!default.jspa")
            page.wait_until_visible((By.ID, "projectKey"))
        sub_measure()

        @print_timing("selenium_app_custom_action_misc:save_config_project")
        def sub_measure():
            project_dropdown = Select(page.get_element((By.ID, "projectKey")))
            project_dropdown.select_by_index(1)

            page.wait_until_clickable((By.ID, "config-submit")).click()
            page.wait_until_visible((By.CLASS_NAME, "aui-message"))
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "log-misc-hours-link"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()