
from playwright.sync_api import expect
from utils.config import *
import re

class DemandPursuitPage:
    def __init__(self,page):
        self.page = page
    def test_demand_pursuit_full_flow(self):

    #1. Navigate to Demand Pursuit Page
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(8000)

        expect(self.page.locator("text=Demand Pursuits")).to_be_visible()

    #2. validate newly created pursuit in All category search using pursuit name
        self.page.wait_for_timeout(5000)
    #Scroll till top search visible
        for i in range(5):
            self.page.mouse.wheel(0,-1000)
            self.page.wait_for_timeout(1000)
        search_box=self.page.locator("input[placeholder*='Search']:visible").first

        search_box.click(force=True)
        search_box.fill("")
        search_box.type(CLIENT_NAME, delay=120)
        self.page.wait_for_timeout(5000)

        expect(self.page.locator(f"text={PURSUIT_NAME}")).to_be_visible()
        print("Created pursuit displayed in ALL Category")

    #3. Validate table details
    #Client Name
        expect(self.page.locator(f"text={CLIENT_NAME}")).to_be_visible()

    #Pursuit Name
        expect(self.page.locator(f"text={PURSUIT_NAME}")).to_be_visible()

    #Jupiter ID
        expect(self.page.locator(f"text={JUPITER_ID}")).to_be_visible()

    #Country
        expect(self.page.locator(f"text={COUNTRY}")).to_be_visible()

    #Proposal Type
        expect(self.page.locator(f"text={PROPOSAL_TYPE}")).to_be_visible()
        print("All table details validated successfully")

    #4. Click on created pursuit from table
        self.page.locator(f"text={PURSUIT_NAME}").click()
        self.page.wait_for_timeout(3000)
        print("Clicked on created pursuit")

    #5 Validate pursuit details page opened
        expect(self.page.locator(f"text={PURSUIT_NAME}")).to_be_visible()
        expect(self.page.locator(f"text={CLIENT_NAME}")).to_be_visible()
        expect(self.page.locator(f"text={JUPITER_ID}")).to_be_visible()
        print("Pursuit details page displayed successfully")