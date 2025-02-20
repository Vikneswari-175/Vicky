import csv
import os

import pyautogui
import pytest
from selenium import webdriver

from Application.Resources.Input.Env_properties import ClsEnvProperties as env
from Citpl_Fw.SeleniumBase import ClsSeleniumBase as sb


# csv_file_path = '/Users/Citpl/Documents/test_results.csv'
# csv_file_path = os.path.join(base_dir, test_results_file_name)
# csv_file_path = ""
test_results_file_name = "test_results.csv"
browser_to_execute = ""
GET_TEST_DATA = {}


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser: chrome or edge or ff or safari or opera")


@pytest.fixture(scope='module')
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="module")
def setup_and_tear_down(browser):
    if browser == 'chrome':
        browser_to_execute = browser
        wd = webdriver.Chrome()
        yield wd
    elif browser == 'edge':
        browser_to_execute = browser
        wd = webdriver.Edge()
        yield wd
    elif browser == 'safari':
        browser_to_execute = browser
        wd = webdriver.Safari()
        yield wd
    elif browser == 'ff':
        browser_to_execute = browser
        wd = webdriver.Firefox()
        yield wd
        yield browser_to_execute


# @pytest.fixture(scope='module', autouse=True)
# def csv_file_setup(request):
#     csv_file_path = env.get_test_results_file()
#     results = []
#     yield results
#     if not os.path.exists(csv_file_path):
#         with open(csv_file_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Test Case Name', 'Status', 'Duration'])
#             writer.writerows(results)
#     else:
#         with open(csv_file_path, mode='a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerows(results)
#
#     def teardown():
#         # Teardown: (if needed)
#         pass
#
#     request.addfinalizer(teardown)
#     return csv_file_path
#

@pytest.fixture(scope='module')
def store_test_data(request):
    # A dictionary to hold test data
    print(f"Fixture received: {request.param}")

    # print("request.node.test_data :: "+str(request.param))
    return request.param


@pytest.hookimpl(tryfirst=True)
def pytest_report_teststatus(report):
    SCREENSHOT_NAME = ""
    GENERATED_SCREENSHOT_PATH = ""
    test_status_to_write_in_csv = []
    get_env_prop = {}
    if report.when == "call":
        current_module_path = os.path.abspath(__file__)
        parent_directory_path = os.path.dirname(current_module_path)
        print("PKApath:", parent_directory_path)


        print("Hook triggered! outcome ", str(report.outcome))
        print("Hook triggered! nodeid ", str(report.nodeid))
        module = getattr(report, 'get_additional_test_case_info', {}).get('module', 'N/A')
        print("module::" + module)
        test_data = getattr(report, 'test_data', {}).get('module_name', 'PKA')

        if report.outcome == 'failed':
            SCREENSHOT_NAME = sb.split_string(report.nodeid, "::", 1) + sb.get_current_date("_%Y_%m_%d_") + sb.get_current_time("%H_%M_%S")
            GENERATED_SCREENSHOT_PATH = take_screenshot(SCREENSHOT_NAME, "jpeg", 5)
        elif report.outcome == 'passed':
            pass

        # test_status_to_write_in_csv.append(GET_TEST_DATA.get('module_name'))
        test_status_to_write_in_csv.append(sb.get_current_date("%Y-%m-%d"))
        test_status_to_write_in_csv.append(sb.get_current_time("%H:%M:%S"))
        test_status_to_write_in_csv.append(browser_to_execute)
        test_status_to_write_in_csv.append(env.PROJECT_NAME)
        test_status_to_write_in_csv.append(module)
        test_status_to_write_in_csv.append("")
        # test_status_to_write_in_csv.append(report.nodeid)
        test_status_to_write_in_csv.append(sb.split_string(report.nodeid, "::", 1))
        test_status_to_write_in_csv.append(report.outcome)
        test_status_to_write_in_csv.append(sb.round_decimal(report.duration, 2))
        test_status_to_write_in_csv.append(GENERATED_SCREENSHOT_PATH)
        write_into_csv(test_status_to_write_in_csv)

        get_env_prop['url'] = env.env_properties_qa().get("url")
        get_env_prop['customer'] = env.env_properties_qa().get("customer")
        get_env_prop['env'] = env.env_properties_qa().get("env")

        sb.get_test_result_data_frame("csv", env.get_test_results_file(), get_env_prop, env.get_html_template_path(), env.get_html_results_path())


def write_into_csv(results):
    print("input to write into csv :: " + str(results))
    csv_file_path = env.get_test_results_file()
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Time', 'Browser', 'Project', 'Module', 'Sub_Module', 'Test_Case_Name', 'Status', 'Duration', 'Screenshot'])
            writer.writerow(results)
    else:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write test results
            writer.writerow(results)


def get_project_name(test_case_name):
    parts = test_case_name.split(os.sep)
    print("parts :: " + str(parts))
    if len(parts) > 1:
        return parts[1]  # Adjust the index based on your directory structure
    return "Unknown Project"


@pytest.fixture
def get_additional_test_case_info(request):
    # Dictionary to hold custom data for the test
    request.node.get_additional_test_case_info = {}
    return request.node.get_additional_test_case_info


def take_screenshot(test_name, file_extn, quality):
    screenshot_dir = env.get_base_dir_path() + "/screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}.PNG")
    screenshot = pyautogui.screenshot()
    # Convert to RGB and save as JPG with quality setting
    screenshot = screenshot.convert("RGB")
    if file_extn == "jpeg":
        screenshot.save(screenshot_path, "JPEG", quality=quality)  # Adjust quality as needed (0-100)
    if file_extn == "png":
        screenshot.save(screenshot_path, "PNG", quality=quality)  # Adjust quality as needed (0-100)
    print(f"Screenshot saved :: Path :: {screenshot_path}")
    return screenshot_path
