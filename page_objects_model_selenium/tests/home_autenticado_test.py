import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.test_data import get_valid_user

@allure.epic("User Interface")
@allure.feature("Home Page")
@allure.story("Authenticated View")
@pytest.mark.ui
def test_home_elementos_autenticado(driver):
    """TP-16: Home - Elementos para Usuário Autenticado"""
    # Arrange
    home_page = HomePage(driver)
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    user = get_valid_user()
    
    # Act - First login with valid credentials
    login_page.open()
    login_page.enter_username(user["username"])
    login_page.enter_password(user["password"])
    login_page.click_submit()
    
    # Verify login was successful
    assert "dashboard" in driver.current_url, "Should be redirected to dashboard after login"
    
    # Navigate to home page
    home_page.open()
    home_page.take_screenshot("home_page_authenticated")
    
    # Assert - Check that login/register buttons are NOT visible
    login_button_hidden = not home_page.is_element_displayed(*home_page.locators.LOGIN_BUTTON, timeout=2)
    register_button_hidden = not home_page.is_element_displayed(*home_page.locators.REGISTER_BUTTON, timeout=2)
    
    assert login_button_hidden, "Login button should NOT be visible for authenticated users"
    assert register_button_hidden, "Register button should NOT be visible for authenticated users"
    
    # Check that dashboard button IS visible
    dashboard_button_visible = home_page.is_element_displayed(*home_page.locators.DASHBOARD_BUTTON)
    assert dashboard_button_visible, "Dashboard button should be visible for authenticated users"
    
    # Check navbar items for authenticated users
    assert home_page.is_element_displayed(*home_page.locators.navbar.DASHBOARD_LINK), \
           "Dashboard link should be visible in navbar"
    assert home_page.is_element_displayed(*home_page.locators.navbar.LOGOUT_LINK), \
           "Logout link should be visible in navbar"
    
    navbar_login_hidden = not home_page.is_element_displayed(*home_page.locators.navbar.LOGIN_LINK, timeout=2)
    navbar_register_hidden = not home_page.is_element_displayed(*home_page.locators.navbar.REGISTER_LINK, timeout=2)
    
    assert navbar_login_hidden, "Login link should NOT be visible in navbar for authenticated users"
    assert navbar_register_hidden, "Register link should NOT be visible in navbar for authenticated users"
    
    # Test navigation to dashboard
    if dashboard_button_visible:
        home_page.click_dashboard_button()
        dashboard_page.take_screenshot("dashboard_from_home_button")
        assert "dashboard" in driver.current_url, "Should navigate to dashboard when clicking dashboard button"
    
    # Clean up - logout
    dashboard_page.logout()
    assert "login" in driver.current_url, "Should be redirected to login page after logout"