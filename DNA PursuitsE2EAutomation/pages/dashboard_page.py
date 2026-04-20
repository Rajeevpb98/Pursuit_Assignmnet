from asyncio import timeout

from playwright.sync_api import expect


class DashboardPage:
    def __init__(self, page):
        self.page = page

    #Cards
        self.cards = page.locator("div.ant-card")

    #Category + Value
        self.categories=self.cards.locator("span:first-child")
        self.card_values=self.cards.locator("span:nth-child(2)")

    # Pursuit List Section
        self.pursuit_list=page.locator("text=List of all Pursuits")

    #Sidebar buttons
        self.expand_menu=page.get_by_role("button", name="Expand menu")
        self.collapse_menu=page.get_by_role("button", name="Collapse menu")
        self.demand_menu=page.get_by_role("button", name="Demand Pursuits")
        self.create_menu=page.get_by_role("button", name="Create Pursuit")

    #Cookies popup
        self.cookie_close=page.locator("button[aria-label='Close']")

    #Handle Cookie Popup
    def handle_cookie_popup(self):
        try:
            if self.cookie_close.is_visible(timeout=5000):
                self.cookie_close.first.click(force=True)
                self.page.wait_for_timeout(2000)
                print("Cookie popup closed")
        except Exception as e:
            print("No cookies pop found:", e)
    #Ensure Sidebar is Open
    def ensure_sidebar_open(self):
        try:
            if self.expand_menu.is_visible(timeout=3000):
                self.expand_menu.click()
                self.page.wait_for_timeout(2000)
        except:
            pass

    #1. Validate Categories
    def validate_categories(self):
        expected=["All", "New", "In Progress", "Cancelled", "Won", "Deferred"]
        actual=[]
        count=self.categories.count()
        print("\nCategories Found:")

        for i in range(count):
            text=self.categories.nth(i).inner_text().strip()
            actual.append(text)

        print(actual)
        return sorted(actual) == sorted(expected)

    #2. Print Card Counts
    def print_card_counts(self):
        count=self.categories.count()
        print("\nCard Counts:")

        if count ==0:
            print("No cards found")
            return False
        all_valid=True

        for i in range(count):
            category=self.categories.nth(i).inner_text().strip()
            value=self.card_values.nth(i).inner_text().strip()
            print(f"{category}: {value}")

            if value=="" or not value.isdigit():
                print("Invalid value for {category}")
                all_valid=False

            return all_valid

    #3 Validate Pursuit List
    def validate_pursuit_list(self):
        visible=self.pursuit_list.is_visible()
        print("\nPursuit List visible:", visible)
        return visible

    #4 Validate left Menu
    def validate_left_menu(self):
        #Step1: Open sidebar visible
        self.ensure_sidebar_open()
        try:
            demand=self.demand_menu.is_visible(timeout=5000)
            create=self.create_menu.is_visible(timeout=5000)
            try:
                collapse=self.collapse_menu.is_visible(timeout=3000)
            except:
                collapse=False
            print("\nSidebar:")
            print("Collapse:", collapse)
            print("Demand:", demand)
            print("Create:", create)
            return demand and create
        except Exception as e:
            print("Error is sidebar validation:", e)
            return False
    def open_create_pursuit(self):
        try:
            #Expand menu if hidden
            if self.page.get_by_role("button", name="Expand menu").is_visible(timeout=3000):
                self.page.get_by_role("button", name="Expand menu").click()
                self.page.wait_for_timeout(2000)
            #Click Create Pursuit
            self.page.get_by_role("button", name="Create Pursuit").click()
            self.page.wait_for_timeout(3000)

            print("Create Pursuit opened")
        except Exception as e:
            print("Create Pursuit not opened:", e)