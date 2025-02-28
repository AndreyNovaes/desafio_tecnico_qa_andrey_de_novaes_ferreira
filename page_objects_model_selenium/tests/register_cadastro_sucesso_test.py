import pytest
import json
import os
import allure
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from utils.test_data import generate_random_user

@allure.epic("Authentication")
@allure.feature("Registration")
@allure.story("Successful Registration")
@pytest.mark.integration
def test_register_cadastro_sucesso(driver):
    """TP-6: Register - Cadastro com Sucesso"""
    # Arrange
    register_page = RegisterPage(driver)
    user_data = generate_random_user()
    
    # Act - Navigate to register page
    register_page.open()
    register_page.take_screenshot("register_page")
    
    # Fill in registration form
    register_page.enter_username(user_data["username"])
    register_page.enter_email(user_data["email"])
    register_page.enter_password1(user_data["password"])
    register_page.enter_password2(user_data["password"])
    register_page.take_screenshot("register_form_filled")
    
    # Submit registration
    register_page.click_submit()
    register_page.take_screenshot("after_registration_submit")
    
    # Assert - Check for success (either redirect to login or success message)
    current_url = driver.current_url
    page_source = driver.page_source.lower()
    
    # Success criteria could be redirect to login or success message
    success = "login" in current_url or any(msg in page_source for msg in 
                                            ["sucesso", "success", "cadastro realizado", 
                                             "registro completo", "conta criada"])
    
    assert success, "Registration should succeed with redirect to login or success message"
    
    # Save user data for future tests if registration succeeded
    if success:
        try:
            os.makedirs("reports", exist_ok=True)
            with open("reports/test_user_data.json", "w") as f:
                json.dump(user_data, f, indent=2)
                
            allure.attach(
                f"Saved new user data:\nUsername: {user_data['username']}\nEmail: {user_data['email']}",
                name="registered_user",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as e:
            allure.attach(
                f"Failed to save user data: {str(e)}",
                name="save_error",
                attachment_type=allure.attachment_type.TEXT
            )
    
    # Verify we can login with the new account if redirected to login page
    if "login" in current_url:
        login_page = LoginPage(driver)
        login_page.enter_username(user_data["username"])
        login_page.enter_password(user_data["password"])
        login_page.click_submit()
        
        # Check if login was successful
        login_page.take_screenshot("login_with_new_account")
        assert "dashboard" in driver.current_url, "Should be able to login with newly created account"
