from selenium.webdriver.common.by import By
from dataclasses import dataclass
from .base_locators import BaseLocators

@dataclass
class ForgotPasswordLocators(BaseLocators):
    """Locators specific to the forgot password page"""
    # Form fields
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='email']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Links
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/accounts/login/']")