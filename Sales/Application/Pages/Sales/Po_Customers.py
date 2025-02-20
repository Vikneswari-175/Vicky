import os
import random
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException

from Application.Pages.Po_Login import Cls_Po_Login
from faker import Faker


class Locators:
    Login_success_message = "//div[text()='Login successful, redirecting to dashboard....']"

    # Company Details
    Sales_module = "//span[text()='Sales']"
    skip = "//button[text()='Skip']"
    Customer_Module = "//span[text()='Customers']"
    Add_NewCustomer = "//div[@class='flex items-center space-x-1 relative']/child::button[4]"
    Company_name = "//input[@name='company_name']"
    Date_onBoarding = "//label[text()='Date of Onboarding']/parent::div/child::button[@type='button']"
    Drug_License_Number_textBox = "//input[@id='drug_license_number']"
    Drug_License_Expiry_Date = "//label[text()='Drug License Expiry Date']/parent::div/child::button[@type='button']"
    Food_License_Number = "//input[@name='food_license_number']"
    Food_License_Expiry_date = "(//span[text()='Select Date'])[3]"

    # Point of Contact
    First_name = "//input[@name='point_of_contact.0.first_name']"
    Last_name = "//input[@name='point_of_contact.0.last_name']"
    Designation = "//input[@name='point_of_contact.0.designation']"
    Email = "//input[@name='point_of_contact.0.email']"
    Mobile_Number = "//input[@name='point_of_contact.0.mobile']"

    # Save as Draft
    Saveasdraft = "//button[text()='Save As Draft']"
    Draft_success_message = "//div[text()='Draft Created!']"


class Cls_Po_Create_Customer(Cls_Po_Login):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def generate_unique_name(self, length):
        letters = string.ascii_letters.upper() + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    def verify_create_new_customer_and_Save_AS_Draft(self):
        self.assert_condition(self.is_element_visible("xpath", Locators.Login_success_message),
                              "Successfully logged into the app", "Failure to login")

        # Customer Details
        self.click("xpath", Locators.skip)
        try:
            alert = self.driver.switch_to.alert
            print("Alert text:", alert.text)
            alert.accept()
            print("Alert accepted")
        except NoAlertPresentException:
            print("No alert present")

        self.click("xpath", Locators.Sales_module)
        self.click_by_actions("xpath", Locators.Customer_Module)
        self.click_by_actions("xpath", Locators.Add_NewCustomer)
        self.sleep(3)

        expected_company = self.generate_unique_name(5)
        self.enter_text("xpath", Locators.Company_name, expected_company)

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[text()='Type']/parent::div/following::button[1]/following::select[1]"))
        )
        select = Select(dropdown)
        select.select_by_index(1)

        self.click_by_actions("xpath", Locators.Date_onBoarding)
        self.driver.find_element(By.XPATH,
                                 "//table[@class='w-full border-collapse space-y-1']/tbody/tr[3]/td[1]").click()

        self.sleep(3)
        self.enter_text_by_jse("xpath", Locators.Drug_License_Number_textBox, self.generate_unique_name(5))
        self.driver.find_element(By.XPATH, Locators.Drug_License_Expiry_Date).click()
        self.driver.find_element(By.XPATH,
                                 "//table[@class='w-full border-collapse space-y-1']/tbody/tr[4]/td[1]").click()

        self.enter_text("xpath", Locators.Food_License_Number, self.generate_unique_name(5))
        self.click_by_actions("xpath", Locators.Food_License_Expiry_date)
        self.driver.find_element(By.XPATH,
                                 "//table[@class='w-full border-collapse space-y-1']/tbody/tr[5]/td[1]").click()

        # Point of Contact
        fake = Faker()
        self.enter_text("xpath", Locators.First_name, fake.first_name())
        self.enter_text("xpath", Locators.Last_name, self.generate_unique_name(1))
        self.enter_text("xpath", Locators.Designation, fake.job())
        self.enter_text("xpath", Locators.Email, fake.email())
        self.enter_text("xpath", Locators.Mobile_Number, fake.phone_number())

        self.click_by_jse("xpath", Locators.Saveasdraft)
        self.assert_condition(self.is_element_visible("xpath", Locators.Draft_success_message),
                              "Successfully drafted the customer", "Failure to draft the customer")
        rows_xpath = "//tbody[@class='[&_tr:last-child]:border-0']/tr"
        next_button_xpath = "//div[@class='rounded-md w-full relative']/div[@class='flex justify-end items-center m-2']/div[@class='flex items-center']/button[2]//*[name()='svg']"

        while True:
            rows = self.driver.find_elements(By.XPATH, rows_xpath)
            found = False

            for row in rows:
                company_cells = row.find_elements(By.XPATH, "./td[3]")  # Use find_elements to avoid exceptions
                if company_cells:
                    company_text = company_cells[0].text.strip()

                    if company_text == expected_company:
                        company_cells[0].click()
                        print(f"Clicked on company: {expected_company}")
                        found = True
                        break  # Exit for-loop

            if found:
                break
            next_buttons = self.driver.find_elements(By.XPATH, next_button_xpath)

            if not next_buttons:
                print("Next button not found. Ending search.")
                break

            next_button = next_buttons[0]
            if "disabled" in next_button.get_attribute("class"):
                print("Reached last page. Company not found.")
                break

            next_button.click()
            print("Company not found in current page. Clicked on Next.")
            time.sleep(2)



