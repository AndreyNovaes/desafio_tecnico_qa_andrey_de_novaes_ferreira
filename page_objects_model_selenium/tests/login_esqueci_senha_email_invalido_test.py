import pytest
import allure
import uuid
from pages.login_page import LoginPage
from pages.forgot_password import ForgotPasswordPage

@allure.epic("Authentication")
@allure.feature("Password Recovery")
@allure.story("Non-Existent Email")
@pytest.mark.security
def test_forgot_password_email_nao_cadastrado(driver):
    """TP-12: Forgot Password - Email Não Cadastrado"""
    # Arrange
    login_page = LoginPage(driver)
    forgot_page = ForgotPasswordPage(driver)
    
    # Generate a random email that's unlikely to exist
    random_email = f"nonexistent_{uuid.uuid4().hex[:8]}@example.com"
    
    # Act - Navigate to login and go to forgot password page
    login_page.open()
    login_page.click_forgot_password_link()
    forgot_page.take_screenshot("forgot_password_page_nonexistent_email")
    
    # Enter non-existent email
    forgot_page.enter_email(random_email)
    forgot_page.take_screenshot("forgot_password_nonexistent_email_entered")
    
    # Submit the form
    forgot_page.click_submit()
    forgot_page.take_screenshot("forgot_password_nonexistent_form_submitted")
    
    # Assert - Check for generic message (for security, should not indicate email doesn't exist)
    page_source = driver.page_source.lower()
    
    # First security check: Should not reveal email doesn't exist
    assert "não existe" not in page_source and "does not exist" not in page_source, \
           "Should not reveal if email exists for security reasons"
           
    # Second check: Should show same success message as with valid email
    success_indicators = [
        "email enviado", "email sent", "check your email", "verifique seu email",
        "recuperação", "recovery", "redefinição", "reset"
    ]
    
    has_success = any(indicator in page_source for indicator in success_indicators)
    
    assert has_success or forgot_page.is_element_displayed(*forgot_page.locators.ALERT_SUCCESS), \
           "Should show same success message as with valid email"
    
    # Third security check: Response time should be similar (to prevent timing attacks)
    # This is difficult to test in an automated test, but we can add a note
    allure.attach(
        "Security Note: Response time should be similar for existing and non-existing emails to prevent timing attacks",
        name="security_timing_note",
        attachment_type=allure.attachment_type.TEXT
    )