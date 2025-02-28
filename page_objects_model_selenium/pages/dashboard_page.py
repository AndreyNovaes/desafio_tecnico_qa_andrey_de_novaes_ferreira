from pages.base_page import BasePage
from locators import DashboardLocators

class DashboardPage(BasePage):
    """Page object for the dashboard page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = DashboardLocators()
        self.url = "http://web:8000/accounts/dashboard/"
    
    def open(self):
        """Navigate to dashboard page"""
        self.navigate_to(self.url)
        return self
    
    def get_header_title(self):
        """Get dashboard header title"""
        return self.get_text(*self.locators.HEADER_TITLE)
    
    def get_header_subtitle(self):
        """Get dashboard header subtitle"""
        return self.get_text(*self.locators.HEADER_SUBTITLE)
    
    def get_overview_section(self):
        """Get overview section element"""
        return self.find_element(*self.locators.OVERVIEW_SECTION)
    
    def get_stats_section(self):
        """Get stats section element"""
        return self.find_element(*self.locators.STATS_SECTION)
    
    def get_actions_section(self):
        """Get actions section element"""
        return self.find_element(*self.locators.ACTIONS_SECTION)
    
    def logout(self):
        """Click logout link"""
        self.click_element(*self.locators.navbar.LOGOUT_LINK)
        return self