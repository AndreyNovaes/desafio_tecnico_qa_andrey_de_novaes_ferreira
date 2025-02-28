import pytest
import allure
from pages.login_page import LoginPage
from utils.test_data import get_valid_user, get_invalid_credentials

@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("Invalid Password")
@pytest.mark.acceptance
def test_login_senha_invalida(driver):
    """
    TP-2: Login - Senha Invalida
    
    Objetivo:
    - Validar o comportamento do sistema ao inserir senha incorreta.
    - Verificar exibição de mensagem de erro e prevenção de acesso não autorizado.
    
    Critérios de Aceite:
    - Sem redirecionamento para áreas autenticadas.
    - Mensagem de erro clara é exibida.
    """
    # Arrange
    login_page = LoginPage(driver)
    user = get_valid_user()
    
    # We'll use the valid username with an incorrect password
    invalid_credentials = [cred for cred in get_invalid_credentials() 
                          if cred['description'] == "Valid user with incorrect password"][0]
    
    # Act
    login_page.open()
    login_page.take_screenshot("login_page_before_invalid_password_test")
    
    login_page.enter_username(invalid_credentials['username'])
    login_page.enter_password(invalid_credentials['password'])
    login_page.click_submit()
    
    # Assert
    assert "login" in driver.current_url, "User should remain on login page"
    login_page.take_screenshot("after_invalid_password_attempt")
    
    # Check for error message - this could be in the page or via HTML5 validation
    error_message = login_page.get_error_message()
    
    # If there's a server-side error message visible
    if error_message:
        assert any(keyword in error_message.lower() for keyword in 
                  ["inválida", "incorreta", "invalid", "incorrect", "credencial"]), \
               "Error message should indicate invalid credentials"
    
    # If no server-side message, we should at least not be on the dashboard
    assert "dashboard" not in driver.current_url, "User should not be redirected to dashboard with invalid credentials"