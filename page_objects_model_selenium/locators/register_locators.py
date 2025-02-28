
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from .base_locators import BaseLocators

@dataclass
class RegisterLocators(BaseLocators):
    """Locators specific to the registration page"""
    # Form fields
    USERNAME_LABEL = (By.CSS_SELECTOR, "label[for='username']")
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='username']")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='email']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD1_LABEL = (By.CSS_SELECTOR, "label[for='password1']")
    PASSWORD1_INPUT = (By.CSS_SELECTOR, "input[name='password1']")
    PASSWORD2_LABEL = (By.CSS_SELECTOR, "label[for='password2']")
    PASSWORD2_INPUT = (By.CSS_SELECTOR, "input[name='password2']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Links
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/accounts/login/']")