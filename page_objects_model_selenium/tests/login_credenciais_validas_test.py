import pytest
import allure
import json
import os
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.test_data import get_valid_user

@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("Valid Credentials")
@pytest.mark.smoke
def test_login_credenciais_validas(driver):
    """
    TP-1: Login - Credenciais Validas
    
    Objetivo:
    - Verificar se o login ocorre com sucesso quando as credenciais estão corretas.
    - Garantir que o usuário é redirecionado à página principal ou dashboard.
    
    Critérios de Aceite:
    - Usuário deve ser direcionado ao dashboard.
    - Navbar ou similar deve exibir que o usuário está logado (ex.: "Logout").
    """
    # Arrange
    login_page = LoginPage(driver)
    user = get_valid_user()
    
    # Log which user we're testing with
    allure.attach(
        f"Username: {user['username']}\nPassword: {'*' * len(user['password'])}",
        name="test_credentials",
        attachment_type=allure.attachment_type.TEXT
    )
    
    # Act
    login_page.open()
    login_page.take_screenshot("login_page_valid_creds_test")
    
    login_page.enter_username(user['username'])
    login_page.enter_password(user['password'])
    login_page.click_submit()
    
    # Assert
    login_page.take_screenshot("after_valid_login_attempt")
    
    # Check if we were redirected to the dashboard
    dashboard_page = DashboardPage(driver)
    assert "dashboard" in driver.current_url, "User was not redirected to dashboard"
    
    # Check if logout link is visible (indicating user is logged in)
    assert dashboard_page.is_element_displayed(*dashboard_page.locators.navbar.LOGOUT_LINK), \
           "Logout link is not visible"
    
    dashboard_page.take_screenshot("dashboard_after_login")
    
    # Save user data for future test runs
    try:
        os.makedirs("reports", exist_ok=True)
        with open("reports/test_user_data.json", "w") as f:
            json.dump(user, f, indent=2)
    except Exception as e:
        allure.attach(
            f"Error saving user data: {str(e)}",
            name="save_user_error",
            attachment_type=allure.attachment_type.TEXT
        )
    
    # Cleanup - logout
    dashboard_page.logout()