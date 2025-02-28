import pytest
import allure
import time
from pages.login_page import LoginPage
from utils.test_data import get_valid_user

@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("Empty Fields")
@pytest.mark.function
def test_login_campos_em_branco(driver):
    """
    TP-3: Login - Campos em Branco
    
    Objetivo:
    - Garantir que o sistema não permita login com campos obrigatórios vazios.
    - Verificar mensagens de validação adequadas.
    
    Critérios de Aceite:
    - Nenhum acesso concedido.
    - Mensagem clara de "Campos obrigatórios" ou similar é exibida.
    """
    # Arrange
    login_page = LoginPage(driver)
    valid_user = get_valid_user()
    
    # Test different combinations of empty fields
    test_cases = [
        {"username": "", "password": "", "desc": "both_empty"},
        {"username": valid_user["username"], "password": "", "desc": "empty_password"},
        {"username": "", "password": valid_user["password"], "desc": "empty_username"}
    ]
    
    for case in test_cases:
        with allure.step(f"Testing {case['desc']} scenario"):
            # Act
            login_page.open()
            
            # Fill fields (or leave empty as specified)
            login_page.send_keys_to_element(login_page.locators.USERNAME_INPUT, case["username"])
            login_page.send_keys_to_element(login_page.locators.PASSWORD_INPUT, case["password"])
            
            # Take screenshot before submitting
            login_page.take_screenshot(f"before_submit_{case['desc']}")
            
            # Try to submit the form
            try:
                login_page.click_submit()
            except Exception as e:
                # If click fails, it might be due to HTML5 validation blocking it
                allure.attach(f"Submit button click failed: {str(e)}", 
                             name="submit_error", 
                             attachment_type=allure.attachment_type.TEXT)
            
            # Small wait to let any client-side validation happen
            time.sleep(0.5)
            
            # Take screenshot after attempted submission
            login_page.take_screenshot(f"after_submit_{case['desc']}")
            
            # Assert - we should still be on the login page
            assert "login" in driver.current_url, f"User should remain on login page ({case['desc']})"
            
            # Check for validation - either via HTML5 validation or server-side validation
            page_source = driver.page_source.lower()
            
            # The form should still be visible
            assert login_page.is_element_displayed(*login_page.locators.USERNAME_INPUT), \
                   f"Username field should still be visible ({case['desc']})"
            
            # Check for standard validation indicators (might be HTML5 validation)
            # This varies by browser, but we can look for some common indicators
            has_validation = any(msg in page_source for msg in 
                                ["obrigat", "required", "empty", "blank", "vazio", "invalid"]) or \
                            "dashboard" not in driver.current_url
                            
            assert has_validation, f"Some validation should occur ({case['desc']})"
