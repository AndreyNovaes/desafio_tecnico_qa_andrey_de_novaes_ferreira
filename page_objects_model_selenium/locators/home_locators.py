from selenium.webdriver.common.by import By
from dataclasses import dataclass
from .base_locators import BaseLocators

@dataclass
class HomeLocators(BaseLocators):
    """Home page locators that inherit from BaseLocators"""
    # Hero section locators
    HERO_CONTAINER = (By.CSS_SELECTOR, "div.container.d-flex.flex-column.justify-content-center")
    HERO_TITLE = (By.CSS_SELECTOR, "h1.fw-bold.text-primary")
    HERO_SUBTITLE = (By.CSS_SELECTOR, "p.text-muted")
    
    # Action buttons - unauthenticated
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a.btn.btn-primary.btn-lg[href='/accounts/login/']")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "a.btn.btn-outline-primary.btn-lg[href='/accounts/register/']")
    
    # Action buttons - authenticated
    DASHBOARD_BUTTON = (By.CSS_SELECTOR, "a.btn.btn-success.btn-lg[href='/accounts/dashboard/']")