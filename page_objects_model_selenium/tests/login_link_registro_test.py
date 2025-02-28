import pytest
import allure
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

@allure.epic("Authentication")
@allure.feature("Registration")
@allure.story("Registration Link")
@pytest.mark.integration
def test_login_link_registro(driver):
    """TP-5: Login - Link de Registro"""
    # Arrange
    login_page = LoginPage(driver)
    
    # Act - Test navbar registration link
    login_page.open()
    login_page.take_screenshot("login_page_before_register_link")
    
    # Verify navbar register link exists
    assert login_page.is_element_displayed(*login_page.locators.navbar.REGISTER_LINK), \
           "Register link in navbar should be visible"
    
    # Click navbar register link
    login_page.click_element(*login_page.locators.navbar.REGISTER_LINK)
    
    # Assert - Check we're on registration page
    register_page = RegisterPage(driver)
    register_page.take_screenshot("register_page_from_navbar")
    assert "register" in driver.current_url, "Should be redirected to registration page from navbar link"
    
    # Now test the form registration link
    login_page.open()
    login_page.take_screenshot("login_page_before_form_register_link")
    
    # Check if form register link exists and click it
    if login_page.is_element_displayed(*login_page.locators.REGISTER_LINK):
        login_page.click_register_link()
        
        # Assert - Check we're on registration page
        register_page.take_screenshot("register_page_from_form_link")
        assert "register" in driver.current_url, "Should be redirected to registration page from form link"
    
    # Verify no automatic login occurred
    assert "dashboard" not in driver.current_url, "User should not be automatically logged in"
    
    # Verify register form appears with correct fields
    assert register_page.is_element_displayed(*register_page.locators.USERNAME_INPUT), \
           "Username field should be visible"
    assert register_page.is_element_displayed(*register_page.locators.EMAIL_INPUT), \
           "Email field should be visible"
