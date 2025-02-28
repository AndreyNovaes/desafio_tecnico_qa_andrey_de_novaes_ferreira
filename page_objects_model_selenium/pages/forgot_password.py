from pages.base_page import BasePage
from locators import ForgotPasswordLocators

class ForgotPasswordPage(BasePage):
    """Page object for the forgot password page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = ForgotPasswordLocators()
        self.url = "http://web:8000/accounts/forget-password/"
    
    def open(self):
        """Navigate to forgot password page"""
        self.navigate_to(self.url)
        return self
    
    def enter_email(self, email):
        """Enter email in field"""
        self.send_keys_to_element(self.locators.EMAIL_INPUT, email)
        return self
    
    def click_submit(self):
        """Click submit button"""
        self.click_element(*self.locators.SUBMIT_BUTTON)
        return self
    
    def click_login_link(self):
        """Click login link"""
        self.click_element(*self.locators.LOGIN_LINK)
        return self
    
    def get_success_message(self):
        """Get success message"""
        return self.get_text(*self.locators.ALERT_SUCCESS)
    
    def get_error_message(self):
        """Get error message"""
        return self.get_text(*self.locators.ALERT_ERROR)