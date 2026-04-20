
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.create_pursuit_page import CreatePursuitPage
from pages.demand_pursuit_page import DemandPursuitPage
from utils.config import *

#Helper function to launch browser
def launch_browser(p):
    browser= p.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    return browser, page

#Test Case 1: Valid Login
def test_valid_login():
    with sync_playwright() as p:
        browser, page = launch_browser(p)
        try:
            login=LoginPage(page)

            # Step 1: Open URL
            login.load(BASE_URL)

            # Step 2: Click SSO
            login.click_sso()

            # Step 3: Enter valid credentials
            login.login(USERNAME, PASSWORD)

            # Step 4: Validate login success
            assert login.verify_login_success()

            # Step 5: Dashboard  Validations
            dashboard = DashboardPage(page)

            # Handle cookie popup
            dashboard.handle_cookie_popup()

            # Validate Dashboard
            assert dashboard.validate_categories()
            assert dashboard.print_card_counts()
            assert dashboard.validate_pursuit_list()
            assert dashboard.validate_left_menu()
        finally:
            browser.close()

#Test Case 2: Invalid Password
def test_invalid_password():
    with sync_playwright() as p:
        browser, page = launch_browser(p)

        login=LoginPage(page)

        login.load(BASE_URL)
        login.click_sso()

        #Enter valid username + invalid password
        login.login(USERNAME, INVALID_PASSWORD)

    #Validate error message
        assert login.verify_login_fail()
        browser.close()
#Test case 3: Empty Fields
def test_empty_fields():
    with sync_playwright() as p:
        browser, page = launch_browser(p)

        login=LoginPage(page)

        login.load(BASE_URL)
        login.click_sso()

        #No input provided
        login.login("", "")

        #Validate browser validation message
        assert login.verify_empty_fields()

        browser.close()

#Test Case 4: Create Pursuit

def test_create_pursuit():
    with sync_playwright() as p:
        browser, page = launch_browser(p)
        try:
            #Login Steps
            login=LoginPage(page)
            login.load(BASE_URL)
            login.click_sso()
            login.login(USERNAME, PASSWORD)
            assert login.verify_login_success()

            #Dashboard
            dashboard=DashboardPage(page)
            dashboard.handle_cookie_popup()
            dashboard.open_create_pursuit()

            #Create Pursuit
            create_pursuit=CreatePursuitPage(page)
            create_pursuit.test_create_pursuit_full_flow()
        finally:
            browser.close()

#Test Case 5: Demand Pursuit
def test_demand_pursuit():
    with sync_playwright() as p:
        browser, page = launch_browser(p)
        try:
            # Login Steps
            login=LoginPage(page)
            login.load(BASE_URL)
            login.click_sso()
            login.login(USERNAME, PASSWORD)

            assert login.verify_login_success()

            #Dashboard
            dashboard=DashboardPage(page)
            dashboard.handle_cookie_popup()

            #Open Demand Pursuit page
            page.locator("text=Demand Pursuit").click()

            #Demand Pursuit
            demand_pursuit=DemandPursuitPage(page)
            demand_pursuit.test_demand_pursuit_full_flow()
        finally:
            browser.close()