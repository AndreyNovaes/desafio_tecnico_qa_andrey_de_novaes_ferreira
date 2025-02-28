from selenium.webdriver.common.by import By
from dataclasses import dataclass

@dataclass
class BaseLocators:
    """Base locators common across pages"""
    
    class navbar:
        """Navbar locators common across pages"""
        CONTAINER = (By.CSS_SELECTOR, "nav.navbar.navbar-expand-lg.navbar-light.bg-white.shadow-sm.fixed-top")
        INNER_CONTAINER = (By.CSS_SELECTOR, "nav.navbar > div.container")
        BRAND = (By.CSS_SELECTOR, "a.navbar-brand.fw-bold.text-primary")
        TOGGLE_BUTTON = (By.CSS_SELECTOR, "button.navbar-toggler")
        TOGGLE_ICON = (By.CSS_SELECTOR, "span.navbar-toggler-icon")
        NAV_COLLAPSE = (By.CSS_SELECTOR, "div#navbarNav.collapse.navbar-collapse")
        NAV_LIST = (By.CSS_SELECTOR, "ul.navbar-nav.ms-auto")
        HOME_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/']")
        LOGIN_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/accounts/login/']")
        REGISTER_LINK = (By.CSS_SELECTOR, "a.nav-link.btn.btn-primary.text-white.px-3[href='/accounts/register/']")
        DASHBOARD_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/accounts/dashboard/']")
        LOGOUT_LINK = (By.CSS_SELECTOR, "a.nav-link.btn.btn-outline-danger.text-danger[href='/accounts/logout/']")

    class footer:
        """Footer locators common across pages"""
        CONTAINER = (By.CSS_SELECTOR, "footer.footer.mt-auto")
        INNER_CONTAINER = (By.CSS_SELECTOR, "footer.footer > div.container")
        COPYRIGHT_TEXT = (By.CSS_SELECTOR, "footer.footer span")

    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[href*='login']")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "a[href*='register']")
    ALERT_ERROR = (By.CSS_SELECTOR, ".alert-error")
    ALERT_SUCCESS = (By.CSS_SELECTOR, ".alert-success")