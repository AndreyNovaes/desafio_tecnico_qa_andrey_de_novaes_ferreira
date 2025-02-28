from pages.base_page import BasePage
from locators import RegisterLocators

class RegisterPage(BasePage):
    """Page object for the registration page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = RegisterLocators()
        self.url = "http://web:8000/accounts/register/"
    
    def open(self):
        """Navigate to register page"""
        self.navigate_to(self.url)
        return self
    
    def enter_username(self, username):
        """Enter username in field"""
        self.send_keys_to_element(self.locators.USERNAME_INPUT, username)
        return self
    
    def enter_email(self, email):
        """Enter email in field"""
        self.send_keys_to_element(self.locators.EMAIL_INPUT, email)
        return self
    
    def enter_password1(self, password):
        """Enter password in first field"""
        self.send_keys_to_element(self.locators.PASSWORD1_INPUT, password)
        return self
    
    def enter_password2(self, password):
        """Enter password in confirmation field"""
        self.send_keys_to_element(self.locators.PASSWORD2_INPUT, password)
        return self
    
    def click_submit(self):
        """Click submit button"""
        self.click_element(*self.locators.SUBMIT_BUTTON)
        return self
    
    def click_login_link(self):
        """Click login link"""
        self.click_element(*self.locators.LOGIN_LINK)
        return self
    
    def get_error_message(self):
        """Get error message"""
        return self.get_text(*self.locators.ALERT_ERROR)
    
    def get_success_message(self):
        """Get success message"""
        return self.get_text(*self.locators.ALERT_SUCCESS)
        
    def enter_registration_details(self, user_data):
        """Enter all registration details from user data"""
        self.enter_username(user_data['username'])
        self.enter_email(user_data['email'])
        self.enter_password1(user_data['password'])
        self.enter_password2(user_data['password'])
        return self
        
    def submit_form(self):
        """Submit the registration form"""
        return self.click_submit()