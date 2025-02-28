import pytest
import allure
from pages.register_page import RegisterPage
from utils.test_data import get_valid_user, generate_random_user

@allure.epic("Authentication")
@allure.feature("Registration")
@allure.story("Duplicate Email")
@pytest.mark.function
def test_register_email_existente(driver):
    """TP-8: Register - Email já Existente"""
    # Arrange
    register_page = RegisterPage(driver)
    existing_user = get_valid_user()
    new_user = generate_random_user()
    
    # Act - Navigate to register page
    register_page.open()
    register_page.take_screenshot("register_page_duplicate_email")
    
    # Fill form with unique username but existing email
    register_page.enter_username(new_user["username"])  # Use unique username
    register_page.enter_email(existing_user["email"])  # Use existing email
    register_page.enter_password1(new_user["password"])
    register_page.enter_password2(new_user["password"])
    register_page.take_screenshot("register_form_duplicate_email")
    
    # Submit form
    register_page.click_submit()
    register_page.take_screenshot("after_duplicate_email_submit")
    
    # Assert - User should remain on register page with error
    assert "register" in driver.current_url, "User should remain on registration page"
    
    # Check for error message
    page_source = driver.page_source.lower()
    has_error = register_page.is_element_displayed(*register_page.locators.ALERT_ERROR) or \
                any(msg in page_source for msg in ["já existe", "already exists", "já cadastrado", 
                                                  "já está em uso", "already in use", "duplicado", 
                                                  "duplicate", "email"])
    
    assert has_error, "Error message about duplicate email should be displayed"
    
    # Verify form still has the data (optional)
    email_field = register_page.find_element(*register_page.locators.EMAIL_INPUT)
    current_email = email_field.get_attribute("value")
    assert current_email == existing_user["email"], "Email field should retain the entered value"
