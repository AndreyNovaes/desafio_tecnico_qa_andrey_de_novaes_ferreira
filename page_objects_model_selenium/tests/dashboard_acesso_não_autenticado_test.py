import pytest
import allure
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utils.test_data import get_valid_user

@allure.epic("Authentication")
@allure.feature("Dashboard")
@allure.story("Unauthorized Access")
@pytest.mark.security
def test_dashboard_acesso_nao_autenticado(driver):
    """TP-14: Dashboard - Tentativa de Acesso Não Autenticado"""
    # Arrange
    dashboard_page = DashboardPage(driver)
    login_page = LoginPage(driver)
    user = get_valid_user()
    
    # Act - Try to access dashboard directly without login
    dashboard_page.open()
    dashboard_page.take_screenshot("dashboard_direct_access_attempt")
    
    # Assert - Verify redirect to login page
    current_url = driver.current_url
    assert "login" in current_url, "Should be redirected to login page when accessing dashboard without authentication"
    
    # Check that login page is displayed
    assert login_page.is_login_page_displayed(), "Login page should be displayed after redirect"
    
    # Verify that after logging in, we can access the dashboard
    login_page.enter_username(user["username"])
    login_page.enter_password(user["password"])
    login_page.click_submit()
    
    # Should now be on dashboard
    dashboard_page.take_screenshot("dashboard_after_authentication")
    assert "dashboard" in driver.current_url, "Should be on dashboard after authentication"
    
    # Clean up - logout
    dashboard_page.logout()