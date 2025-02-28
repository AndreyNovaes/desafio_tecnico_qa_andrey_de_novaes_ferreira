from selenium.webdriver.common.by import By
from dataclasses import dataclass
from .base_locators import BaseLocators

@dataclass
class LoginLocators(BaseLocators):
    """Locators specific to the login page"""
    # Form fields
    USERNAME_LABEL = (By.CSS_SELECTOR, "label[for='username']")
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='username']")
    PASSWORD_LABEL = (By.CSS_SELECTOR, "label[for='password']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Links
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href='/accounts/register/']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href='/accounts/forget-password/']")
