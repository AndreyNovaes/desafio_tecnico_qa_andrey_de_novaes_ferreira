import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.test_data import get_valid_user

@allure.epic("Authentication")
@allure.feature("Dashboard")
@allure.story("Authenticated Access")
@pytest.mark.function
def test_dashboard_acesso_autenticado(driver):
    """TP-13: Dashboard - Acesso Autenticado"""
    # Arrange
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    user = get_valid_user()
    
    # Act - Login with valid credentials
    login_page.open()
    login_page.enter_username(user["username"])
    login_page.enter_password(user["password"])
    login_page.click_submit()
    
    # Assert - Verify dashboard loads correctly
    dashboard_page.take_screenshot("dashboard_after_login")
    
    assert "dashboard" in driver.current_url, "Should be redirected to dashboard after login"
    
    # Check dashboard elements
    assert dashboard_page.is_element_displayed(*dashboard_page.locators.HEADER_TITLE), \
           "Dashboard title should be visible"
           
    # Check if any of the dashboard sections are displayed
    sections_visible = any([
        dashboard_page.is_element_displayed(*dashboard_page.locators.OVERVIEW_SECTION),
        dashboard_page.is_element_displayed(*dashboard_page.locators.STATS_SECTION),
        dashboard_page.is_element_displayed(*dashboard_page.locators.ACTIONS_SECTION)
    ])
    
    assert sections_visible, "At least one dashboard section should be visible"
    
    # Verify logout link is available
    assert dashboard_page.is_element_displayed(*dashboard_page.locators.navbar.LOGOUT_LINK), \
           "Logout link should be visible"
           
    # Get and log dashboard content for analysis
    if dashboard_page.is_element_displayed(*dashboard_page.locators.HEADER_TITLE):
        title_text = dashboard_page.get_text(*dashboard_page.locators.HEADER_TITLE)
        allure.attach(
            f"Dashboard Title: {title_text}",
            name="dashboard_title",
            attachment_type=allure.attachment_type.TEXT
        )
    
    # Clean up - logout
    dashboard_page.logout()
    assert "login" in driver.current_url, "Should be redirected to login page after logout"