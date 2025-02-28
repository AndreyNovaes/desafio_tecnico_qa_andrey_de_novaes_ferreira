import allure
from pages.base_page import BasePage
from locators import LoginLocators

class LoginPage(BasePage):
    """Page object for the login page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginLocators()
        self.url = "http://web:8000/accounts/login/"
    
    def open(self):
        """Navigate to login page"""
        self.navigate_to(self.url)
        return self
    
    def enter_username(self, username):
        """Enter username in the field"""
        self.send_keys_to_element(self.locators.USERNAME_INPUT, username)
        return self

    def enter_password(self, password):
        """Enter password in the field"""
        self.send_keys_to_element(self.locators.PASSWORD_INPUT, password)
        return self

    def click_submit(self):
        """Click the submit button"""
        self.click_element(*self.locators.SUBMIT_BUTTON)
        return self

    def click_forgot_password_link(self):
        """Click the forgot password link"""
        self.click_element(*self.locators.FORGOT_PASSWORD_LINK)
        return self

    def click_register_link(self):
        """Click the register link"""
        self.click_element(*self.locators.REGISTER_LINK)
        return self

    def get_error_message(self):
        """Get error message text"""
        try:
            return self.get_text(*self.locators.ALERT_ERROR)
        except:
            self.take_screenshot("error_message_not_found")
            return None

    def get_password_field_type(self):
        """Get password field type attribute"""
        return self.get_attribute(self.locators.PASSWORD_INPUT, "type")

    def is_navbar_visible(self):
        """Check if navbar is visible"""
        return self.is_element_displayed(*self.locators.navbar.CONTAINER)

    def is_footer_visible(self):
        """Check if footer is visible"""
        return self.is_element_displayed(*self.locators.footer.CONTAINER)

    def get_footer_text(self):
        """Get footer copyright text"""
        return self.get_text(*self.locators.footer.COPYRIGHT_TEXT)
    
    @allure.step("Login with {username}")
    def login(self, username, password):
        """Perform login and verify result"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()
        self.take_screenshot("after_login_attempt")
        
        return self.wait_for_url_contains('dashboard', timeout=5)
    
    def is_login_page_displayed(self):
        """Verify login page is displayed"""
        username_field = self.is_element_displayed(*self.locators.USERNAME_INPUT)
        password_field = self.is_element_displayed(*self.locators.PASSWORD_INPUT)
        submit_button = self.is_element_displayed(*self.locators.SUBMIT_BUTTON)
        
        if not all([username_field, password_field, submit_button]):
            self.take_screenshot("login_page_verification_failed")
            
        return all([username_field, password_field, submit_button])