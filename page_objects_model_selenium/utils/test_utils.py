import allure
import logging
import time

logger = logging.getLogger(__name__)

def add_visual_indicator(driver, message, color="#e0f7fa", duration=0.5):
    """
    Add visual indicator to the page for better video recordings
    
    Args:
        driver: WebDriver instance
        message: Message to display
        color: Background color for the overlay
        duration: Duration to show the overlay in seconds
    """
    script = f"""
        var overlay = document.createElement('div');
        overlay.style = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: {color}; opacity: 0.7; display: flex; align-items: center; justify-content: center; z-index: 9999;';
        var msg = document.createElement('h1');
        msg.textContent = '{message}';
        msg.style = 'font-weight: bold; font-size: 24px; text-align: center; color: black; text-shadow: 0 0 5px white;';
        overlay.appendChild(msg);
        document.body.appendChild(overlay);
        setTimeout(() => {{ overlay.style.opacity = '0'; setTimeout(() => {{ document.body.removeChild(overlay); }}, 500); }}, {int(duration * 1000)});
    """
    try:
        driver.execute_script(script)
        time.sleep(duration)
    except Exception as e:
        logger.warning(f"Failed to add visual indicator: {e}")

def attach_browser_logs(driver):
    """
    Attach browser console logs to Allure report
    
    Args:
        driver: WebDriver instance
    """
    try:
        browser_logs = driver.get_log('browser')
        if browser_logs:
            log_text = "\n".join([f"{log['level']}: {log['message']}" for log in browser_logs])
            allure.attach(
                log_text,
                name="browser_console_logs",
                attachment_type=allure.attachment_type.TEXT
            )
    except Exception as e:
        logger.warning(f"Failed to attach browser logs: {e}")

def check_html5_validation(driver, element):
    """
    Check if an element has HTML5 validation errors
    
    Args:
        driver: WebDriver instance
        element: WebElement to check
        
    Returns:
        tuple: (is_valid, validation_message)
    """
    try:
        is_valid = driver.execute_script("return arguments[0].validity.valid;", element)
        validation_message = driver.execute_script("return arguments[0].validationMessage;", element)
        return is_valid, validation_message
    except Exception as e:
        logger.warning(f"Failed to check HTML5 validation: {e}")
        return True, ""

def wait_for_absence_of_spinner(driver, spinner_selector, timeout=10):
    """
    Wait for a loading spinner to disappear
    
    Args:
        driver: WebDriver instance
        spinner_selector: CSS selector for the spinner
        timeout: Maximum time to wait in seconds
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            spinner = driver.find_element_by_css_selector(spinner_selector)
            # If spinner is displayed, wait a bit
            if spinner.is_displayed():
                time.sleep(0.1)
            else:
                return True
        except:
            # Spinner not found in DOM
            return True
    
    # If we get here, spinner was still visible after timeout
    logger.warning(f"Loading spinner still visible after {timeout}s")
    return False
