import pytest
import allure
from pages.register_page import RegisterPage
from utils.test_data import generate_random_user

@allure.epic("Authentication")
@allure.feature("Registration")
@allure.story("Password Mismatch")
@pytest.mark.function
def test_register_senhas_diferentes(driver):
    """TP-9: Register - Senhas Diferentes"""
    # Arrange
    register_page = RegisterPage(driver)
    user_data = generate_random_user()
    password1 = user_data["password"]
    password2 = user_data["password"] + "different"  # Make passwords different
    
    # Act - Navigate to register page
    register_page.open()
    register_page.take_screenshot("register_page_different_passwords")
    
    # Fill form with different passwords
    register_page.enter_username(user_data["username"])
    register_page.enter_email(user_data["email"])
    register_page.enter_password1(password1)
    register_page.enter_password2(password2)
    register_page.take_screenshot("register_form_different_passwords")
    
    # Submit form
    register_page.click_submit()
    register_page.take_screenshot("after_different_passwords_submit")
    
    # Assert - User should remain on register page with error
    assert "register" in driver.current_url, "User should remain on registration page"
    
    # Check for error message about passwords not matching
    page_source = driver.page_source.lower()
    has_error = register_page.is_element_displayed(*register_page.locators.ALERT_ERROR) or \
                any(msg in page_source for msg in ["senhas não coincidem", "passwords do not match", 
                                                  "senhas diferentes", "senhas não conferem",
                                                  "não são iguais", "don't match", "do not match"])
    
    assert has_error, "Error message about password mismatch should be displayed"
    
    # Verify form still retains other data (optional)
    username_field = register_page.find_element(*register_page.locators.USERNAME_INPUT)
    email_field = register_page.find_element(*register_page.locators.EMAIL_INPUT)
    
    assert username_field.get_attribute("value") == user_data["username"], "Username should be retained"
    assert email_field.get_attribute("value") == user_data["email"], "Email should be retained"
