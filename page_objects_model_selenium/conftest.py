import os
import sys
import pytest
import allure
import json
import time
import logging
import shutil
import glob
import requests
from datetime import datetime
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from utils.webdriver_factory import WebDriverFactory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('test_execution.log')]
)
logger = logging.getLogger(__name__)

BROWSERS = ['chrome', 'firefox', 'edge']
REPORT_DIRS = ["reports/videos", "reports/screenshots", "reports/logs", 
               "reports/allure-results", "reports/downloads"]

for dir_path in REPORT_DIRS:
    os.makedirs(dir_path, exist_ok=True)

def pytest_addoption(parser):
    parser.addoption("--browser-type", action="store", default="chrome")
    parser.addoption("--browser-version", action="store", default="latest")
    parser.addoption("--remote", action="store_true", default=True)
    parser.addoption("--hub", action="store", default=None)
    parser.addoption("--url", action="store", default=None)
    parser.addoption("--enable-video", action="store_true", default=True)
    parser.addoption("--enable-vnc", action="store_true", default=True)
    parser.addoption("--enable-log", action="store_true", default=True)
    parser.addoption("--screen-resolution", action="store", default="1920x1080x24")

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "nondestructive: mark the test as nondestructive, i.e., it doesn't change application state"
    )

def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.nondestructive)

def pytest_generate_tests(metafunc):
    if "selenium_browser" in metafunc.fixturenames:
        browser_option = metafunc.config.getoption("--browser-type")
        browsers = BROWSERS if browser_option.lower() == "all" else [browser_option]
        metafunc.parametrize("selenium_browser", browsers, scope="function")

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url") or WebDriverFactory.get_app_url()

@pytest.fixture(scope="session")
def remote_url(request):
    return request.config.getoption("--hub") or WebDriverFactory.get_grid_url()

@pytest.fixture(scope="function")
def driver(request, selenium_browser, base_url, remote_url):
    is_remote = request.config.getoption("--remote")
    browser_version = request.config.getoption("--browser-version")
    enable_video = request.config.getoption("--enable-video")
    enable_vnc = request.config.getoption("--enable-vnc")
    enable_log = request.config.getoption("--enable-log")
    screen_resolution = request.config.getoption("--screen-resolution")
    
    test_name = request.node.name
    clean_test_name = ''.join(c if c.isalnum() else '_' for c in test_name)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    driver = None
    try:
        driver = WebDriverFactory.create_driver(
            browser=selenium_browser,
            remote=is_remote, 
            remote_url=remote_url,
            test_name=clean_test_name,
            enable_video=enable_video,
            enable_vnc=enable_vnc,
            enable_log=enable_log,
            screen_resolution=screen_resolution,
            browser_version=browser_version
        )
        
        session_id = driver.session_id
        _write_metadata(driver, test_name, selenium_browser, browser_version)
        
        driver.get(base_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        yield driver
        
    except WebDriverException as e:
        allure.attach(str(e), name=f"webdriver_exception_{selenium_browser}", 
                     attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Could not initialize WebDriver for {selenium_browser}: {str(e)}")
        return
    
    finally:
        if driver:
            failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False
            session_id = driver.session_id
            
            if failed:
                _capture_failure_evidence(driver, selenium_browser, clean_test_name, timestamp)
            
            driver.quit()
            time.sleep(2)
            
            if enable_video:
                _attach_media(session_id, clean_test_name, test_name, selenium_browser, 
                           browser_version, remote_url, "video")
            
            if enable_log:
                _attach_media(session_id, clean_test_name, test_name, selenium_browser, 
                           browser_version, remote_url, "log")
            
            if is_remote:
                _cleanup_remote_files(remote_url, session_id)

def _write_metadata(driver, test_name, browser, browser_version):
    session_id = driver.session_id
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    clean_test_name = ''.join(c if c.isalnum() else '_' for c in test_name)
    
    metadata = {
        "session_id": session_id,
        "test_name": test_name,
        "clean_test_name": clean_test_name,
        "browser": browser,
        "browser_version": browser_version,
        "timestamp": timestamp,
        "url": driver.current_url,
        "title": driver.title
    }
    
    metadata_path = f"reports/videos/{session_id}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

def _capture_failure_evidence(driver, browser, test_name, timestamp):
    screenshot_name = f"failure_{browser}_{test_name}_{timestamp}"
    screenshot_path = f"reports/screenshots/{screenshot_name}.png"
    
    try:
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name=screenshot_name, 
                         attachment_type=allure.attachment_type.PNG)
        
        page_source = driver.page_source
        allure.attach(page_source, name=f"page_source_on_failure_{browser}",
                    attachment_type=allure.attachment_type.HTML)
    except Exception as e:
        logger.error(f"Failed to capture evidence: {str(e)}")

def _attach_media(session_id, clean_test_name, test_name, browser, version, remote_url, media_type):
    if media_type == "video":
        file_ext = "mp4"
        finder_func = _find_file
        downloader_func = _download_file
    else:
        file_ext = "log"
        finder_func = _find_file
        downloader_func = _download_file
    
    file_path = finder_func(session_id, clean_test_name, remote_url, file_ext)
    if file_path:
        logger.info(f"Found {media_type} file: {file_path}")
        if media_type == "video":
            _attach_video_to_allure(file_path, test_name, browser, version)
        else:
            _attach_log_to_allure(file_path, test_name, browser, version)

def _find_file(session_id, test_name, remote_url, file_ext, retries=10, wait_time=1):
    local_dir = f"reports/{file_ext}s"
    
    # Try direct download first
    if remote_url:
        local_path = os.path.join(local_dir, f"{session_id}.{file_ext}")
        if _download_file(remote_url, session_id, local_path, file_ext):
            return local_path
    
    # Then look for existing files
    patterns = [
        f"{session_id}.{file_ext}",
        f"{test_name}.{file_ext}",
        f"*.{file_ext}"
    ]
    
    for _ in range(retries):
        for pattern in patterns:
            matches = glob.glob(os.path.join(local_dir, pattern))
            if matches:
                return max(matches, key=os.path.getmtime)
        time.sleep(wait_time)
    
    return None

def _download_file(remote_url, session_id, local_path, file_type):
    if file_type == "mp4":
        url = f"{remote_url.replace('/wd/hub', '')}/video/{session_id}.mp4"
    else:
        url = f"{remote_url.replace('/wd/hub', '')}/logs/{session_id}.log"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        logger.warning(f"Error downloading {file_type}: {str(e)}")
    
    return False

def _cleanup_remote_files(remote_url, session_id):
    try:
        requests.delete(f"{remote_url.replace('/wd/hub', '')}/video/{session_id}.mp4")
        requests.delete(f"{remote_url.replace('/wd/hub', '')}/logs/{session_id}.log")
    except Exception:
        pass

def _attach_video_to_allure(video_path, test_name, browser_name, browser_version):
    if not video_path or not os.path.exists(video_path):
        return False
    
    try:
        clean_test_name = ''.join(c if c.isalnum() else '_' for c in test_name)
        attachment_name = f"Test Video - {clean_test_name} ({browser_name} {browser_version})"
        
        allure_results_dir = "reports/allure-results"
        video_filename = f"video_{clean_test_name}_{browser_name}_{browser_version}.mp4"
        target_path = os.path.join(allure_results_dir, video_filename)
        
        shutil.copy2(video_path, target_path)
        
        allure.attach.file(
            target_path,
            name=attachment_name,
            attachment_type=allure.attachment_type.MP4
        )
        return True
    except Exception as e:
        logger.error(f"Failed to attach video: {str(e)}")
        return False

def _attach_log_to_allure(log_path, test_name, browser_name, browser_version):
    if not log_path or not os.path.exists(log_path):
        return False
    
    try:
        clean_test_name = ''.join(c if c.isalnum() else '_' for c in test_name)
        attachment_name = f"Session Log - {clean_test_name} ({browser_name} {browser_version})"
        
        with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
            log_content = f.read()
        
        allure.attach(
            log_content,
            name=attachment_name,
            attachment_type=allure.attachment_type.TEXT
        )
        return True
    except Exception as e:
        logger.error(f"Failed to attach log: {str(e)}")
        return False

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture
def download_file(driver):
    def _download_file(session_id, filename):
        remote_url = WebDriverFactory.get_grid_url().replace("/wd/hub", "")
        download_url = f"{remote_url}/download/{session_id}/{filename}"
        local_path = os.path.join("reports/downloads", filename)
        
        try:
            response = requests.get(download_url, timeout=10)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                return local_path
        except Exception:
            pass
        
        return None
    
    return _download_file