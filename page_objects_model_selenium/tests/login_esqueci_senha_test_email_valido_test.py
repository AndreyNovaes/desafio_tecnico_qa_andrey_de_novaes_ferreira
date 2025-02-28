import pytest
import allure
from pages.login_page import LoginPage
from pages.forgot_password import ForgotPasswordPage
from utils.test_data import get_valid_user

@allure.epic("Authentication")
@allure.feature("Password Recovery")
@allure.story("Forgot Password")
@pytest.mark.smoke
def test_login_esqueci_senha(driver):
    """TP-4: Login - Esqueci Minha Senha"""
    # Arrange
    login_page = LoginPage(driver)
    user = get_valid_user()
    
    # Act - Navigate to login and click forgot password
    login_page.open()
    login_page.take_screenshot("login_page_before_forgot_password")
    login_page.click_forgot_password_link()
    
    # Assert - Verify redirect to forgot password page
    forgot_page = ForgotPasswordPage(driver)
    forgot_page.take_screenshot("forgot_password_page")
    
    assert "forget-password" in driver.current_url or "reset-password" in driver.current_url, \
           "Should be redirected to password reset page"
    
    # Act - Enter email for password recovery
    forgot_page.enter_email(user["email"])
    forgot_page.take_screenshot("forgot_password_email_entered")
    forgot_page.click_submit()
    
    # Assert - Success message or redirect should happen
    forgot_page.take_screenshot("forgot_password_submitted")
    
    # Check for confirmation (either message or redirect)
    current_url = driver.current_url
    page_source = driver.page_source.lower()
    
    assert any(term in page_source for term in ["email enviado", "email sent", "verifique seu email"]) or \
           "login" in current_url, \
           "Should show success message or redirect to login"
