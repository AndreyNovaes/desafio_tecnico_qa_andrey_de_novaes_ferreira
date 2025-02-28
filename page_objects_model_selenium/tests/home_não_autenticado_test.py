import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

@allure.epic("User Interface")
@allure.feature("Home Page")
@allure.story("Unauthenticated View")
@pytest.mark.ui
def test_home_elementos_nao_autenticado(driver):
    """TP-15: Home - Elementos para Usuário Não Autenticado"""
    # Arrange
    home_page = HomePage(driver)
    
    # Act - Navigate to home page
    home_page.open()
    home_page.take_screenshot("home_page_unauthenticated")
    
    # Assert - Check hero elements
    hero_elements_visible = False
    if home_page.is_element_displayed(*home_page.locators.HERO_CONTAINER):
        if (home_page.is_element_displayed(*home_page.locators.HERO_TITLE) or 
            home_page.is_element_displayed(*home_page.locators.HERO_SUBTITLE)):
            hero_elements_visible = True
    
    assert hero_elements_visible, "Hero section elements should be visible"
    
    # Check login and register buttons
    assert home_page.is_element_displayed(*home_page.locators.LOGIN_BUTTON), \
           "Login button should be visible"
    assert home_page.is_element_displayed(*home_page.locators.REGISTER_BUTTON), \
           "Register button should be visible"
    
    # Check the navbar links are working
    assert home_page.is_element_displayed(*home_page.locators.navbar.LOGIN_LINK), \
           "Login link should be visible in navbar"
    assert home_page.is_element_displayed(*home_page.locators.navbar.REGISTER_LINK), \
           "Register link should be visible in navbar"
    
    # Test navigation to login page
    home_page.click_login_button()
    login_page = LoginPage(driver)
    login_page.take_screenshot("login_page_from_home_button")
    assert "login" in driver.current_url, "Should navigate to login page when clicking login button"
    
    # Go back to home and test navigation to register page
    driver.back()
    home_page.click_register_button()
    register_page = RegisterPage(driver)
    register_page.take_screenshot("register_page_from_home_button")
    assert "register" in driver.current_url, "Should navigate to register page when clicking register button"
