import pytest
import allure
import time
from pages.register_page import RegisterPage
from utils.test_data import generate_random_user

@allure.epic("Authentication")
@allure.feature("Registration")
@allure.story("Empty Fields")
@pytest.mark.function
def test_register_campos_branco(driver):
    """TP-10: Register - Campos em Branco"""
    # Arrange
    register_page = RegisterPage(driver)
    user_data = generate_random_user()
    
    # Define test cases for different empty field combinations
    test_cases = [
        {"desc": "all_empty", "username": "", "email": "", "password1": "", "password2": ""},
        {"desc": "empty_username", "username": "", "email": user_data["email"], 
         "password1": user_data["password"], "password2": user_data["password"]},
        {"desc": "empty_email", "username": user_data["username"], "email": "", 
         "password1": user_data["password"], "password2": user_data["password"]},
        {"desc": "empty_password1", "username": user_data["username"], "email": user_data["email"], 
         "password1": "", "password2": user_data["password"]},
        {"desc": "empty_password2", "username": user_data["username"], "email": user_data["email"], 
         "password1": user_data["password"], "password2": ""}
    ]
    
    for case in test_cases:
        with allure.step(f"Testing {case['desc']} scenario"):
            # Act - Navigate to register page
            register_page.open()
            register_page.take_screenshot(f"register_page_{case['desc']}")
            
            # Fill form based on the test case
            if case["username"]:
                register_page.enter_username(case["username"])
            if case["email"]:
                register_page.enter_email(case["email"])
            if case["password1"]:
                register_page.enter_password1(case["password1"])
            if case["password2"]:
                register_page.enter_password2(case["password2"])
                
            register_page.take_screenshot(f"register_form_{case['desc']}")
            
            # Try to submit form
            try:
                register_page.click_submit()
            except Exception as e:
                # If click fails due to HTML5 validation, this is expected
                allure.attach(
                    f"Submit button click failed (expected): {str(e)}",
                    name=f"submit_error_{case['desc']}",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            time.sleep(0.5)  # Wait briefly for any client-side validation
            register_page.take_screenshot(f"after_submit_{case['desc']}")
            
            # Assert - Verify we're still on register page and not registered
            assert "register" in driver.current_url, f"Should remain on register page ({case['desc']})"
            assert "dashboard" not in driver.current_url, f"Should not be logged in ({case['desc']})"
            
            # Check for validation indications (either explicit message or HTML5 validation)
            page_source = driver.page_source.lower()
            
            # Look for validation indications in page source
            has_validation = any(msg in page_source for msg in [
                "obrigatório", "required", "empty", "blank", "vazio", "campo", "field"
            ])
            
            # If no validation message found in page source, check if form elements show validation state
            if not has_validation:
                # For browsers that support HTML5 validation
                if case["username"] == "":
                    username_field = register_page.find_element(*register_page.locators.USERNAME_INPUT)
                    has_validation = (username_field.get_attribute("validity") and 
                                    not username_field.get_attribute("validity").get("valid", True))
            
            assert has_validation, f"Form should show validation errors ({case['desc']})"
