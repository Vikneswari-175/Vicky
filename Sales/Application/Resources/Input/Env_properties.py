import os

from Citpl_Fw.SeleniumBase import ClsSeleniumBase as sb


class ClsEnvProperties:
    PROJECT_NAME = "BUDGIE 2.4"
    PROJECT_ROOT_FOLDER_NAME = "/budgie_2_4"
    # URL = "http://216.48.191.170/budgie_qa_frontend/#/login"
    URL = "https://morphs.in/dashboard"
    USERNAME = "HEPL00001"
    PASSWORD = "12345678"
    CSV_FILE_PATH = "test_results.csv"
    TEST_DATE_FILE = PROJECT_ROOT_FOLDER_NAME + "/Application/Resources/Input/Test_Data_Excel.xlsx"
    TEST_RESULT_HTML_TEMPLATE_PATH = "/Input/test_result_template.html"
    TEST_RESULT_HTML_PATH = "/test_automation_results.html"


    @staticmethod
    def env_properties_qa():
        # automation_root_path = "/Users/citpl/Documents/automation/py_automation"
        return {
            "customer": "Cavin Kare",
            "env": "QA environment",
            "url": "http://216.48.191.170/budgie_qa_frontend/#/login",
            "username": "HEPL00001",
            "password": "12345678", }

    @staticmethod
    def get_test_results_file():
        test_result_file = str(os.path.join(ClsEnvProperties.get_base_dir_path(), ClsEnvProperties.CSV_FILE_PATH))
        # test_result_file = os.path.join(ClsEnvProperties.TEST_RESULT_HTML_TEMPATE_PATH, ClsEnvProperties.CSV_FILE_PATH)
        print("Test result file is :: " + test_result_file)
        return test_result_file

    @staticmethod
    def get_project_root_folder_path():
        # project_root = str(pb.get_parent_dir_path() + ClsEnvProperties.PROJECT_ROOT_FOLDER_NAME)
        project_root = str(ClsEnvProperties.get_parent_dir_path())
        print("Project root folder name and path :: " + project_root)
        return project_root

    @staticmethod
    def get_html_template_path():
        template_path = str(ClsEnvProperties.get_project_root_folder_path() + ClsEnvProperties.TEST_RESULT_HTML_TEMPLATE_PATH)
        print("Project root folder name and path :: " + template_path)
        return template_path

    @staticmethod
    def get_html_results_path():
        results_path = str(ClsEnvProperties.get_base_dir_path() + ClsEnvProperties.TEST_RESULT_HTML_PATH)
        print("Automation test results html file path :: " + results_path)
        return results_path  # class ClsEnvPropertiesUserCredentials:  #     HEPL00001 = "12345678"  #     HEPL00002 = "12345678"  #     HEPL00003 = "12345678"  #     HEPL00004 = "12345678"  #     HEPL00005 = "12345678"  #     HEPL00006 = "12345678"  #     HEPL00007 = "12345678"  #     HEPL00008 = "12345678"  #     HEPL00009 = "12345678"  #     HEPL00010 = "12345678"  #     HEPL00011 = "12345678"  #     HEPL00012 = "12345678"  #     HEPL00013 = "12345678"  #     HEPL00014 = "12345678"  #     HEPL00015 = "12345678"  #     HEPL00016 = "12345678"  #     HEPL00017 = "12345678"  #     HEPL00018 = "12345678"  #     HEPL00019 = "12345678"  #     HEPL00020 = "12345678"  #     NTS0028 = "12345678"  #     NTS0021 = "12345678"  #     A0623109380 = "12345678"  #     A022235944 = "12345678"  #     A0723155675 = "12345678"  #     A022329516 = "12345678"  #

    # @staticmethod
    # def get_base_dir_path():
    #     # Define the base directory for different operating systems
    #     TEST_AUTOMATION_FOLDER_PATH = os.path.expanduser('~/Documents/Test_Automation')
    #     sb.create_folder_if_not_exists(TEST_AUTOMATION_FOLDER_PATH)
    #     if os.name == 'posix':
    #         # For macOS and Linux
    #         base_dir = os.path.expanduser('~/Documents/Test_Automation')
    #         print("base_dir :: " + str(base_dir))
    #     elif os.name == 'nt':
    #         # For Windows
    #         base_dir = os.path.expanduser('~/Documents/Test_Automation')
    #         print("base_dir :: " + str(base_dir))
    #     else:
    #         raise Exception("base_dir :: Unsupported operating system")
    #     return base_dir

    @staticmethod
    def get_base_dir_path():
        # Define the base directory for different operating systems
        test_automation_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'Test_Automation')
        sb.create_folder_if_not_exists(test_automation_folder)

        if os.name == 'posix':
            # For macOS and Linux
            base_dir = test_automation_folder
            print("base_dir for posix (macOS/Linux): " + str(base_dir))
        elif os.name == 'nt':
            # For Windows
            base_dir = test_automation_folder
            print("base_dir for nt (Windows): " + str(base_dir))
        else:
            raise Exception("Unsupported operating system")

        return str(base_dir)

    @staticmethod
    def get_parent_dir_path():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        print("Current directory using os module:", current_directory)
        print("Parent directory using os module:", parent_directory)
        return str(parent_directory)
