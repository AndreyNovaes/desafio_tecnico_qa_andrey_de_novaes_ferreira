from pages.base_page import BasePage
from locators import HomeLocators

class HomePage(BasePage):
    """Page object for the home page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = HomeLocators()
        self.url = "http://web:8000/"
    
    def open(self):
        """Navigate to home page"""
        self.navigate_to(self.url)
        return self
    
    def click_login_button(self):
        """Click login button"""
        self.click_element(*self.locators.LOGIN_BUTTON)
        return self

    def click_register_button(self):
        """Click register button"""
        self.click_element(*self.locators.REGISTER_BUTTON)
        return self
    
    def toggle_mobile_menu(self):
        """Toggle mobile menu"""
        self.click_element(*self.locators.navbar.TOGGLE_BUTTON)
        return self
    
    def click_brand(self):
        """Click brand logo"""
        self.click_element(*self.locators.navbar.BRAND)
        return self
    
    def get_copyright(self):
        """Get copyright text"""
        return self.get_text(*self.locators.footer.COPYRIGHT_TEXT)
        
    def click_dashboard_button(self):
        """Click dashboard button for authenticated users"""
        self.click_element(*self.locators.DASHBOARD_BUTTON)
        return self