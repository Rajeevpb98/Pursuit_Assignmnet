import re
import time
from playwright.sync_api import expect
from utils.config import *

class CreatePursuitPage:
    def __init__(self, page):
        self.page= page

    def test_create_pursuit_full_flow(self):

        #Open Create Pursuit page
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(5000)

        #Verify page loaded
        expect(self.page.get_by_role("textbox").first).to_be_visible()
        print("Create Pursuit page loaded")

        #Validate Bottom Buttons
        expect(self.page.get_by_role("button",name="Cancel").first).to_be_visible()
        expect(self.page.get_by_role("button",name="Cancel")).to_be_visible()
        print("Button visible")

        #Click Create Button Without Data
        self.page.locator("button:has-text('Create')").click()
        self.page.wait_for_timeout(2000)

        expect(self.page.get_by_text("Client name is required")).to_be_visible()
        expect(self.page.get_by_text("Pursuit name is required")).to_be_visible()
        expect(self.page.get_by_text("Proposal type is required")).to_be_visible()

        #Add New Client
        self.page.locator("text=Add New Client").click()
        self.page.wait_for_timeout(2000)

        #Verify popup
        expect(self.page.get_by_text("Client Details", exact=True)).to_be_visible()
        print("Client popup opened")

        #Enter Client Name
        self.page.get_by_placeholder("Add New Client").fill(CLIENT_NAME)

        #Self Industry
        self.page.locator("input#rc_select_14").fill(INDUSTRY)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")

        #Select Sector
        self.page.locator("input#rc_select_15").fill(SECTOR)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")

        #Save Client
        self.page.locator("button:has-text('Save')").click()
        self.page.wait_for_timeout(3000)

        # Fill Create Pursuit Form

        # #Client
        # self.page.locator("input#rc_select_7").fill("abcd")
        # self.page.keyboard.press("ArrowDown")
        # self.page.keyboard.press("Enter")
        # self.page.wait_for_timeout(3000)

        #verify Industry auto selected and disabled
        expect(self.page.locator(".ant-select-selection-item").nth(1)
               ).to_contain_text("Technology Media and Telecom")

        #Verify Sector auto selected and disabled
        expect(self.page.locator(".ant-select-selection-item").nth(2)
               ).to_contain_text("Technology (Tech)")

        #Pursuit Name
        self.page.locator("input[placeholder='Enter pursuit name']").fill(PURSUIT_NAME)

        # Proposal Type
        self.page.locator("input#rc_select_8").fill(PROPOSAL_TYPE)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")

        #Type of Project
        self.page.locator("input#rc_select_9").fill(TYPE_OF_PROJECT)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")

        #Country
        self.page.locator("input#rc_select_10").fill(COUNTRY)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")

        # Billing Arrangement
        self.page.locator("input#rc_select_13").fill(BILLING_ARRANGEMENT)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")

        # Project Duration
        #Open Calendar
        self.page.locator(".ant-picker").click()
        self.page.wait_for_timeout(2000)

        #Select Start Date =20
        self.page.locator(".ant-picker-cell").filter(has_text="20").first.click()

        #Select End Date =25
        self.page.locator(".ant-picker-cell").filter(has_text="25").first.click()

        #Click Done button
        self.page.locator("button:has-text('Done')").click()

        self.page.wait_for_timeout(2000)
        print("Dates selected successfully")

        # Jupiter ID
        self.page.locator("text=Jupiter ID").scroll_into_view_if_needed()
        self.page.wait_for_timeout(2000)
        self.page.locator("input[placeholder*='jupiter']").first.fill(JUPITER_ID)

        #Utilizing AI Assist =No
        self.page.get_by_role("radio",name="No").check()

        #Description
        self.page.locator("div[data-placeholder='Enter description']").click()
        self.page.keyboard.type(DESCRIPTION)

        #Click Create
        self.page.locator("button:has-text('Create')").click()

        # Success Message Validation
        expect(self.page.locator("text=Successfully submitted")).to_be_visible(timeout=10000)
        expect(self.page.locator("text=New pursuit is created")).to_be_visible(timeout=10000)
