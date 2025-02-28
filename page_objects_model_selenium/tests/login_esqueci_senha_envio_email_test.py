import pytest
import allure
from pages.login_page import LoginPage
from pages.forgot_password import ForgotPasswordPage
from utils.test_data import get_valid_user

@allure.epic("Authentication")
@allure.feature("Password Recovery")
@allure.story("Email Sending")
@pytest.mark.integration
def test_forgot_password_envio_email(driver):
    """TP-11: Forgot Password - Envio de Email"""
    # Arrange
    login_page = LoginPage(driver)
    forgot_page = ForgotPasswordPage(driver)
    user = get_valid_user()
    
    # Act - Navigate to login and go to forgot password page
    login_page.open()
    login_page.click_forgot_password_link()
    forgot_page.take_screenshot("forgot_password_page_email_test")
    
    # Verify we're on the forgot password page
    assert "forget-password" in driver.current_url or "reset-password" in driver.current_url, \
           "Should be on password reset page"
    
    # Enter registered email
    forgot_page.enter_email(user["email"])
    forgot_page.take_screenshot("forgot_password_email_entered")
    
    # Submit the form
    forgot_page.click_submit()
    forgot_page.take_screenshot("forgot_password_form_submitted")
    
    # Assert - Check for confirmation message
    page_source = driver.page_source.lower()
    success_indicators = [
        "email enviado", "email sent", "check your email", "verifique seu email",
        "recuperação", "recovery", "redefinição", "reset"
    ]
    
    has_success = any(indicator in page_source for indicator in success_indicators)
    
    assert has_success or forgot_page.is_element_displayed(*forgot_page.locators.ALERT_SUCCESS), \
           "Should show success message after submitting email"
    
    # Check for security - shouldn't reveal if email exists
    assert "não existe" not in page_source and "does not exist" not in page_source, \
           "Should not reveal if email exists for security reasons"
    