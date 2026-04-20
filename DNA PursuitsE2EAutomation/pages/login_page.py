class LoginPage:
    def __init__(self, page):
        self.page = page

        # Locaters (UI Elements)
        self.login_using_sso= "text=Login using SSO"
        self.username_input=page.locator("#signInFormUsername:visible").first
        self.password_input=page.locator("#signInFormPassword:visible")
        self.login_button=page.locator("input[type='Submit']:visible")

        #Dashboard validation
        self.dashboard_heading= "text=Demand Pursuits"
        #Error message
        self.error_message= "#loginErrorMessage"

    #Step 1: Open Application URL
    def load(self, url):
        self.page.goto(url)

    #Step2: Click Login using SSO
    def click_sso(self):
        self.page.locator(self.login_using_sso).click()
        #wait unitl login form is fully loaded
        self.page.wait_for_load_state("domcontentloaded")
        #wait until username field is visible
        self.username_input.wait_for(state="visible", timeout=60000)

    #Step 3: Enter Username
    def enter_username(self, username):
        self.username_input.fill(username)

    #Step 4: Enter Password
    def enter_password(self, password):
        self.password_input.fill(password)

    #Step 5: Click Login Button
    def click_login(self):
        self.login_button.click()

    #Combined Login Action
    def login(self, username,password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.click_login()

    #Step 6: Verify successful login
    def verify_login_success(self):
        # Wait until page fully loads after login
        self.page.wait_for_load_state("networkidle")

        #wait for dashboard heading
        self.page.wait_for_selector(self.dashboard_heading, timeout=15000)

        #Return True if visible
        return self.page.locator(self.dashboard_heading).is_visible()

    #Check redirect + heading visible
    def verify_redirect(self):
        return "demand" in self.page.url.lower()

    #Step 7: verify Login failure (Invalid credentials)
    def verify_login_fail(self):
        #Wait for error message to appear
        error=self.page.locator("#loginErrorMessage:visible").first
        error.wait_for(state="visible", timeout=20000)
        return error.is_visible()

    #Step 8: verify empty fields validation
    def verify_empty_fields(self):
        return self.page.locator("#signInFormUsername").first.evaluate("e1 => e1.validationMessage")
