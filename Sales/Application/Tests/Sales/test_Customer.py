import pytest
from Citpl_Fw import PyBase


from Application.Pages.Po_Login import Cls_Po_Login
from Application.Pages.Sales.Po_Customers import Cls_Po_Create_Customer
from Application.Resources.Input import Env_properties as env
from Application.Resources.Input.Env_properties import ClsEnvProperties as env
from conftest import setup_and_tear_down



def test_TC_003_Create_NewCustomer_And_SaveAsDraft(setup_and_tear_down):
    driver = setup_and_tear_down
    test_case_id = "test_bud24_004_446"
    tdd = PyBase.get_input_test_data(test_case_id, env.get_parent_dir_path())
    Cls_Po_Login(driver).login(tdd.get("Email"), tdd.get("Password"))
    Cls_Po_Create_Customer(driver). verify_create_new_customer_and_Save_AS_Draft()