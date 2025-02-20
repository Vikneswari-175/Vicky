from Citpl_Fw.SeleniumBase import ClsSeleniumBase

from Application.Resources.Input.Env_properties import ClsEnvProperties


class Cls_Po_Login(ClsSeleniumBase):
    # LOGIN_USERNAME_TXT_BX_XPATH = "//input[@id='empId']"
    # LOGIN_PASSWORD_TXT_BX_XPATH = "//input[@id='password']"
    # LOGIN_SIGN_IN_BTN_XPATH = "//button[@type='submit']/span[contains(text(),'LOGIN')]"
    #
    # USER_PROFILE_IMG_XPATH = "//div[@class='ant-space-item']/img[@class='user']"
    # SIGN_OUT_LNK_XPATH = "//span[contains(text(),'Sign Out')]"

    LOGIN_USERNAME_TXT_BX_XPATH = "//input[@id='email']"
    LOGIN_PASSWORD_TXT_BX_XPATH = "//input[@id='password']"
    LOGIN_SIGN_IN_BTN_XPATH = "//button[text()='Sign in']"

    USER_PROFILE_IMG_XPATH = "//div[@class='ant-space-item']/img[@class='user']"
    SIGN_OUT_LNK_XPATH = "//span[contains(text(),'Sign Out')]"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.cls_Env_Properties = ClsEnvProperties()
        # self.url, self.username, self.password = self.cls_Env_Properties.env_properties_qa().get("url")
        self.url = self.cls_Env_Properties.URL
        self.username = self.cls_Env_Properties.USERNAME
        self.password = self.cls_Env_Properties.PASSWORD

    def logout(self):
        ClsSeleniumBase.print_in_console(self, "About to logout!")
        ClsSeleniumBase.click(self, "xpath", self.USER_PROFILE_IMG_XPATH)
        ClsSeleniumBase.click(self, "xpath", self.SIGN_OUT_LNK_XPATH)
        ClsSeleniumBase.sleep(self, 3)
        ClsSeleniumBase.assert_condition(self, ClsSeleniumBase.is_element_visible(self, "xpath", self.LOGIN_USERNAME_TXT_BX_XPATH), "Logout success!", "Logout failure!")

    def login(self, username, password):
        ClsSeleniumBase.sleep(self, 3)
        ClsSeleniumBase.print_in_console(self, "About to login!")
        self.driver.get(self.url)
        self.driver.maximize_window()
        ClsSeleniumBase.print_in_console(self, "Login username :: " + str(username))
        ClsSeleniumBase.print_in_console(self, "Login password :: " + str(password))
        ClsSeleniumBase.enter_text(self, "xpath", self.LOGIN_USERNAME_TXT_BX_XPATH, username)
        ClsSeleniumBase.enter_text(self, "xpath", self.LOGIN_PASSWORD_TXT_BX_XPATH, password)
        ClsSeleniumBase.click(self, "xpath", self.LOGIN_SIGN_IN_BTN_XPATH)
