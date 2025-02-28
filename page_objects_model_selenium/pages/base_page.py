from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import allure
import logging
import time

class BasePage:
    """Base page class with common methods for all pages"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.default_timeout = 10
    
    def wait_for_element(self, locator, timeout=None, condition=EC.presence_of_element_located):
        """Wait for element with specified condition"""
        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout, poll_frequency=0.5, 
                          ignored_exceptions=[StaleElementReferenceException])
        try:
            return wait.until(condition(locator))
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"element_not_found", 
                       attachment_type=allure.attachment_type.PNG)
            raise
    
    def find_element(self, *locator, timeout=None):
        """Find element with wait for presence"""
        return self.wait_for_element(locator, timeout, EC.presence_of_element_located)
    
    def find_clickable_element(self, *locator, timeout=None):
        """Find clickable element with wait"""
        return self.wait_for_element(locator, timeout, EC.element_to_be_clickable)
    
    def find_visible_element(self, *locator, timeout=None):
        """Find visible element with wait"""
        return self.wait_for_element(locator, timeout, EC.visibility_of_element_located)
    
    def find_elements(self, *locator, timeout=None):
        """Find all elements matching locator with wait"""
        timeout = timeout or self.default_timeout
        try:
            self.wait_for_element(locator, timeout, EC.presence_of_element_located)
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
    
    def click_element(self, *locator, timeout=None):
        """Click element with retry mechanism"""
        timeout = timeout or self.default_timeout
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            try:
                element = self.find_clickable_element(*locator, timeout=2)
                element.click()
                return element
            except (StaleElementReferenceException, TimeoutException):
                if time.time() >= end_time:
                    allure.attach(self.driver.get_screenshot_as_png(), name="click_failed", 
                               attachment_type=allure.attachment_type.PNG)
                    raise
                time.sleep(0.5)
    
    def send_keys_to_element(self, locator, text, timeout=None, clear_first=True):
        """Send keys to element"""
        element = self.find_element(*locator, timeout=timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element
    
    def get_text(self, *locator, timeout=None):
        """Get text from element"""
        return self.find_visible_element(*locator, timeout=timeout).text
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute from element"""
        return self.find_element(*locator, timeout=timeout).get_attribute(attribute)
    
    def is_element_displayed(self, *locator, timeout=5):
        """Check if element is displayed"""
        try:
            self.find_visible_element(*locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_element_present(self, *locator, timeout=5):
        """Check if element is present in DOM"""
        try:
            self.find_element(*locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def wait_for_url_contains(self, text, timeout=None):
        """Wait for URL to contain text"""
        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.url_contains(text))
        except TimeoutException:
            return False
    
    def wait_for_url_to_be(self, url, timeout=None):
        """Wait for URL to match exactly"""
        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))
        except TimeoutException:
            return False
    
    def take_screenshot(self, name="screenshot"):
        """Take screenshot and attach to report"""
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot
    
    def navigate_to(self, url):
        """Navigate to URL"""
        self.driver.get(url)
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def get_title(self):
        """Get page title"""
        return self.driver.title
    
    def accept_alert(self):
        """Accept alert and return its text"""
        alert = WebDriverWait(self.driver, self.default_timeout).until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text