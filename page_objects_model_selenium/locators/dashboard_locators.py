from selenium.webdriver.common.by import By
from dataclasses import dataclass
from .base_locators import BaseLocators

@dataclass
class DashboardLocators(BaseLocators):
    """Locators specific to the dashboard page"""
    # Header section
    HEADER_CONTAINER = (By.CSS_SELECTOR, "div.container.py-4")
    HEADER_TITLE = (By.CSS_SELECTOR, "h3.text-center.fw-bold")
    HEADER_SUBTITLE = (By.CSS_SELECTOR, "p.text-muted.text-center")
    
    # Content sections
    OVERVIEW_SECTION = (By.CSS_SELECTOR, "div.dashboard-overview")
    STATS_SECTION = (By.CSS_SELECTOR, "div.dashboard-stats")
    ACTIONS_SECTION = (By.CSS_SELECTOR, "div.dashboard-actions")