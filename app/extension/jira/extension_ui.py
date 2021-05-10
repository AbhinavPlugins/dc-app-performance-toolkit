import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


# def app_specific_action(webdriver, datasets):
#     page = BasePage(webdriver)
#     if datasets['custom_issues']:
#         issue_key = datasets['custom_issue_key']

#     # To run action as specific user uncomment code bellow.
#     # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
#     # just before test_2_selenium_z_log_out action
#     #
#     # @print_timing("selenium_app_specific_user_login")
#     # def measure():
#     #     def app_specific_user_login(username='admin', password='admin'):
#     #         login_page = Login(webdriver)
#     #         login_page.delete_all_cookies()
#     #         login_page.go_to()
#     #         login_page.set_credentials(username=username, password=password)
#     #         if login_page.is_first_login():
#     #             login_page.first_login_setup()
#     #         if login_page.is_first_login_second_page():
#     #             login_page.first_login_second_page_setup()
#     #         login_page.wait_for_page_loaded()
#     #     app_specific_user_login(username='admin', password='admin')
#     # measure()

#     @print_timing("selenium_app_custom_action")
#     def measure():
#         @print_timing("selenium_app_custom_action:view_issue")
#         def sub_measure():
#             page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
#             page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
#             page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector
#         sub_measure()
#     measure()


def app_specific_action_misc_logwork(webdriver, datasets):
    page = BasePage(webdriver)
    wait = WebDriverWait(webdriver, 10)

    @print_timing("selenium_app_custom_action_misc:log_work")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/Dashboard.jspa")
        
        logwork_dropdown = page.wait_until_clickable((By.ID, "log-misc-hours-link"))
        logwork_dropdown.click()

        page.wait_until_clickable((By.CLASS_NAME, "trigger-dialog")).click()
        page.wait_until_clickable((By.ID, "log-work-time-logged")).send_keys("1h")

        @print_timing("selenium_app_custom_action_misc:submit_log_work_form")
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
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/ConfigureReport.jspa?selectedProjectId=10000&projectSprint=0&userID=all&reportKey=au.com.adweb.plugin.mischrs%3Amisc-hours-report")

        page.wait_until_visible((By.CLASS_NAME, "timeReport"))
    measure()

def app_specific_action_misc_config(webdriver, datasets):
    page = BasePage(webdriver)
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
        sub_measure()
    measure()