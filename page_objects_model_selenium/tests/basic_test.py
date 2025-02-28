import pytest
import allure
import time
import json
from utils.webdriver_factory import WebDriverFactory

pytestmark = pytest.mark.nondestructive

def add_visual_indicator(driver, message, color="#e0f7fa", duration=0.5):
    """Add visual indicator to the page"""
    script = f"""
        var overlay = document.createElement('div');
        overlay.id = 'test-overlay';
        overlay.style = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; backgroundColor: "{color}"; opacity: 0.7; zIndex: 9999; display: flex; alignItems: center; justifyContent: center; transition: opacity 0.5s';
        var message = document.createElement('h1');
        message.textContent = '{message}';
        message.style = 'color: black; fontSize: 32px; fontWeight: bold; textAlign: center; textShadow: 0 0 10px white';
        overlay.appendChild(message);
        document.body.appendChild(overlay);
        setTimeout(function() {{
            overlay.style.opacity = '0';
            setTimeout(function() {{
                document.body.removeChild(overlay);
            }}, 500);
        }}, {int(duration * 1000)});
    """
    driver.execute_script(script)
    time.sleep(duration + 0.5)

@allure.epic("Setup Verification")
@allure.feature("Basic Test")
class TestBasic:
    
    @allure.story("Simple Test")
    @allure.severity(allure.severity_level.NORMAL)
    def test_basic_setup(self, driver, selenium_browser, browser_version):
        """Basic test to verify setup is working"""
        allure.dynamic.description(f"Testing basic setup with {selenium_browser} {browser_version}")
        
        add_visual_indicator(driver, f"BASIC TEST - {selenium_browser} {browser_version}", "#e3f2fd", 1.0)
        
        app_url = WebDriverFactory.get_app_url()
        driver.get(app_url)
        session_id = driver.session_id
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"home_page_{selenium_browser}_{browser_version}",
            attachment_type=allure.attachment_type.PNG
        )
        
        browser_info = {
            "Browser": selenium_browser,
            "Version": browser_version,
            "Session ID": session_id,
            "URL": driver.current_url,
            "Title": driver.title
        }
        allure.attach(json.dumps(browser_info, indent=2), 
                    name="browser_info", 
                    attachment_type=allure.attachment_type.JSON)
        
        add_visual_indicator(driver, "TESTING PAGE LOAD", "#bbdefb", 1.0)
        
        page_title = driver.title
        assert page_title is not None, "Page title should not be None"
        assert driver.current_url.startswith(app_url), f"URL should start with {app_url}"
        
        add_visual_indicator(driver, "TEST PASSED", "#81c784", 1.0)
            
    @allure.story("Failing Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.issue("DEMO-1234", "https://example.com/issue/1234")
    def test_intentional_failure(self, driver, selenium_browser, browser_version):
        """Test that intentionally fails to demonstrate failure handling"""
        add_visual_indicator(driver, f"FAILURE TEST - {selenium_browser} {browser_version}", "#ffcdd2", 1.0)
        
        driver.get(WebDriverFactory.get_app_url())
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"before_failure_{selenium_browser}_{browser_version}",
            attachment_type=allure.attachment_type.PNG
        )
        
        for i in range(3):
            color = ["#ffdddd", "#ddffdd", "#ffffff"][i]
            driver.execute_script(f"document.body.style.backgroundColor = '{color}';")
            time.sleep(0.5)
        
        add_visual_indicator(driver, "ABOUT TO FAIL...", "#f44336", 1.0)
        
        assert "Non-existent Title" in driver.title, "Expected title not found"