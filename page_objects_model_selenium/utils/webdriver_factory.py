import logging
import os
import socket
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import WebDriverException

logger = logging.getLogger(__name__)

class WebDriverFactory:
    """
    Factory class for creating WebDriver instances with Selenoid support.
    Supports local and remote WebDriver creation for different browsers.
    """

    @staticmethod
    def is_docker_container(hostname, port, timeout=1):
        """
        Check if a hostname:port is accessible directly (inside Docker).
        
        Args:
            hostname: Hostname to check
            port: Port number
            timeout: Connection timeout in seconds
            
        Returns:
            bool: True if hostname is accessible, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((hostname, port))
            sock.close()
            return result == 0
        except:
            return False

    @staticmethod
    def get_grid_url():
        """
        Get the Selenoid Grid URL based on environment.
        Try Docker service name first, fall back to localhost if not available.
        
        Returns:
            str: Selenoid Grid URL
        """
        # Try environment variable first
        grid_url = os.environ.get("SELENIUM_URL") or os.environ.get("SELENIUM_HUB_URL")
        if grid_url:
            # Ensure URL has the correct format and endpoint
            if not grid_url.endswith("/wd/hub"):
                if not grid_url.endswith("/"):
                    grid_url += "/"
                grid_url += "wd/hub"
            return grid_url
            
        # Try Docker service name for Selenoid
        if WebDriverFactory.is_docker_container("selenoid", 4444):
            logger.info("Detected Docker environment - using selenoid:4444/wd/hub")
            return "http://selenoid:4444/wd/hub"
        
        # Fall back to localhost
        logger.info("Using localhost:4444/wd/hub for Selenoid Grid")
        return "http://localhost:4444/wd/hub"
        
    @staticmethod
    def get_app_url():
        """
        Get the application URL based on environment.
        Try Docker service name first, fall back to localhost if not available.
        
        Returns:
            str: Application URL
        """
        # Try environment variable first
        app_url = os.environ.get("APP_URL")
        if app_url:
            return app_url
            
        # Try Docker service name
        if WebDriverFactory.is_docker_container("web", 8000):
            logger.info("Detected Docker environment - using web:8000")
            return "http://web:8000"
        
        # Fall back to localhost
        logger.info("Using localhost:8000 for application")
        return "http://localhost:8000"

    @staticmethod
    def check_selenoid_connection(remote_url):
        """
        Check if Selenoid is accessible and responding correctly
        
        Args:
            remote_url: URL of Selenoid Grid hub
            
        Returns:
            bool: True if Selenoid is accessible, False otherwise
        """
        status_url = remote_url.replace("/wd/hub", "/status")
        try:
            response = requests.get(status_url, timeout=5)
            if response.status_code == 200:
                # Attempt to parse response as JSON
                status_data = response.json()
                logger.info(f"Selenoid is accessible at {status_url}")
                logger.info(f"Selenoid version: {status_data.get('version', 'unknown')}")
                return True
            else:
                logger.warning(f"Selenoid returned status code {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error connecting to Selenoid: {e}")
            return False
        except json.JSONDecodeError as e:
            logger.warning(f"Selenoid is not returning valid JSON: {e}")
            logger.warning(f"Response content: {response.content[:100]}...")
            return False

    @staticmethod
    def create_driver(browser="chrome", remote=True, remote_url=None, test_name=None, 
                      enable_video=True, enable_vnc=True, enable_log=True, 
                      screen_resolution=None, browser_version="latest"):
        """
        Create a WebDriver instance based on specified parameters
        
        Args:
            browser (str): Browser to use (chrome, firefox, edge)
            remote (bool): Whether to use a remote WebDriver
            remote_url (str): URL of the Selenoid Grid hub
            test_name (str): Name of the test for reporting
            enable_video (bool): Whether to enable video recording
            enable_vnc (bool): Whether to enable VNC for live viewing
            enable_log (bool): Whether to enable session logs
            screen_resolution (str): Custom screen resolution (e.g. "1920x1080x24")
            browser_version (str): Browser version to use
            
        Returns:
            WebDriver: Configured WebDriver instance
        """
        driver = None
        browser = browser.lower()
        
        # Determine remote URL based on environment if not provided
        if remote and not remote_url:
            remote_url = WebDriverFactory.get_grid_url()
            
        logger.info(f"Creating {browser} {browser_version} WebDriver with remote={remote}, remote_url={remote_url}")
        
        # Verify Selenoid connection if remote
        if remote:
            # Check if we can connect to Selenoid
            if not WebDriverFactory.check_selenoid_connection(remote_url):
                logger.warning(f"Could not verify Selenoid connection at {remote_url}")
                logger.warning("Proceeding anyway, but this might cause issues")
        
        try:
            if browser == "chrome":
                driver = WebDriverFactory._create_chrome_driver(
                    remote, remote_url, test_name, enable_video, enable_vnc, 
                    enable_log, screen_resolution, browser_version
                )
            elif browser == "firefox":
                driver = WebDriverFactory._create_firefox_driver(
                    remote, remote_url, test_name, enable_video, enable_vnc, 
                    enable_log, screen_resolution, browser_version
                )
            elif browser == "edge":
                driver = WebDriverFactory._create_edge_driver(
                    remote, remote_url, test_name, enable_video, enable_vnc, 
                    enable_log, screen_resolution, browser_version
                )
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            
            # Configure driver
            if driver:
                driver.maximize_window()
                driver.implicitly_wait(10)
                
                # Store custom attributes for reference
                driver.browser_name = browser
                driver.browser_version = browser_version
                if test_name:
                    driver.test_name = test_name
                    
                logger.info(f"Created {browser} {browser_version} WebDriver instance successfully with session ID: {driver.session_id}")
                return driver
            else:
                raise WebDriverException(f"Failed to create WebDriver instance for {browser}")
                
        except Exception as e:
            logger.error(f"Failed to create WebDriver: {str(e)}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            raise
    
    @staticmethod
    def _create_selenoid_capabilities(browser_name, browser_version, test_name, 
                                      enable_video, enable_vnc, enable_log, screen_resolution):
        """
        Create capabilities for Selenoid
        
        Args:
            browser_name (str): Browser name
            browser_version (str): Browser version
            test_name (str): Test name for logging
            enable_video (bool): Whether to enable video recording
            enable_vnc (bool): Whether to enable VNC
            enable_log (bool): Whether to enable session logs
            screen_resolution (str): Custom screen resolution
            
        Returns:
            dict: Capabilities for Selenoid
        """
        # Format test name for use as filename
        clean_test_name = None
        if test_name:
            clean_test_name = ''.join(c if c.isalnum() else '_' for c in test_name)
        
        # Create basic capabilities
        capabilities = {
            "browserName": browser_name,
            "browserVersion": browser_version,
        }
        
        # Create selenoid:options
        selenoid_options = {
            "enableVNC": enable_vnc,
            "enableVideo": enable_video,
            "enableLog": enable_log,
            "name": test_name or "UI Test",
            "sessionTimeout": "15m",
            "timeZone": "America/Sao_Paulo",
            "labels": {
                "test": clean_test_name or "test",
                "browser": browser_name,
                "version": browser_version
            }
        }
        
        # Set video parameters
        if enable_video:
            selenoid_options["videoName"] = f"{clean_test_name or 'video'}.mp4"
            selenoid_options["videoScreenSize"] = "1920x1080"
            selenoid_options["videoFrameRate"] = 12
            selenoid_options["videoCodec"] = "mpeg4"
            
        # Set log parameters
        if enable_log:
            selenoid_options["logName"] = f"{clean_test_name or 'log'}.log"
            
        # Set screen resolution
        if screen_resolution:
            selenoid_options["screenResolution"] = screen_resolution
        else:
            selenoid_options["screenResolution"] = "1920x1080x24"
        
        # Add selenoid:options to capabilities
        capabilities["selenoid:options"] = selenoid_options
        
        return capabilities
    
    @staticmethod
    def _create_chrome_driver(remote=True, remote_url=None, test_name=None, 
                             enable_video=True, enable_vnc=True, enable_log=True, 
                             screen_resolution=None, browser_version="latest"):
        """Create Chrome WebDriver instance with Selenoid support"""
        options = ChromeOptions()
        
        # Common Chrome options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        
        # Configure download behavior
        prefs = {
            "download.default_directory": "/home/selenium/Downloads",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "plugins.always_open_pdf_externally": True
        }
        options.add_experimental_option("prefs", prefs)
        
        if remote:
            # Create Selenoid capabilities
            capabilities = WebDriverFactory._create_selenoid_capabilities(
                "chrome", browser_version, test_name, 
                enable_video, enable_vnc, enable_log, screen_resolution
            )
            
            # Update Chrome options with Selenoid capabilities
            for key, value in capabilities.items():
                options.set_capability(key, value)
            
            # Create Remote WebDriver
            try:
                # Use a more robust way to create the remote WebDriver
                logger.info(f"Connecting to Selenoid at {remote_url} with Chrome {browser_version}")
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=options
                )
                return driver
            except Exception as e:
                logger.error(f"Failed to create Remote WebDriver: {str(e)}")
                # Try to get more information about the failure
                try:
                    status_url = remote_url.replace("/wd/hub", "/status")
                    response = requests.get(status_url, timeout=5)
                    logger.info(f"Selenoid status response: {response.status_code}")
                    logger.info(f"Response content: {response.content[:200]}...")
                except Exception as e2:
                    logger.error(f"Could not get Selenoid status: {str(e2)}")
                raise
        else:
            # Create local Chrome WebDriver
            service = ChromeService()
            return webdriver.Chrome(service=service, options=options)
    
    @staticmethod
    def _create_firefox_driver(remote=True, remote_url=None, test_name=None, 
                              enable_video=True, enable_vnc=True, enable_log=True, 
                              screen_resolution=None, browser_version="latest"):
        """Create Firefox WebDriver instance with Selenoid support"""
        options = FirefoxOptions()
        
        # Add common Firefox options
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        # Configure download behavior
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", "/home/selenium/Downloads")
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                              "application/octet-stream,application/pdf,application/x-pdf,application/zip")
        
        if remote:
            # Create Selenoid capabilities
            capabilities = WebDriverFactory._create_selenoid_capabilities(
                "firefox", browser_version, test_name, 
                enable_video, enable_vnc, enable_log, screen_resolution
            )
            
            # Update Firefox options with Selenoid capabilities
            for key, value in capabilities.items():
                options.set_capability(key, value)
            
            # Firefox needs a different path for Selenoid
            ff_remote_url = remote_url
            if "/wd/hub" not in ff_remote_url:
                if not ff_remote_url.endswith("/"):
                    ff_remote_url += "/"
                ff_remote_url += "wd/hub"
            
            # Create Remote WebDriver
            try:
                logger.info(f"Connecting to Selenoid at {ff_remote_url} with Firefox {browser_version}")
                driver = webdriver.Remote(
                    command_executor=ff_remote_url,
                    options=options
                )
                return driver
            except Exception as e:
                logger.error(f"Failed to create Remote WebDriver: {str(e)}")
                raise
        else:
            # Create local Firefox WebDriver
            service = FirefoxService()
            return webdriver.Firefox(service=service, options=options)
    
    @staticmethod
    def _create_edge_driver(remote=True, remote_url=None, test_name=None, 
                           enable_video=True, enable_vnc=True, enable_log=True, 
                           screen_resolution=None, browser_version="latest"):
        """Create Edge WebDriver instance with Selenoid support"""
        options = EdgeOptions()
        
        # Add common Edge options
        options.add_argument('--start-maximized')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        if remote:
            # Create Selenoid capabilities
            capabilities = WebDriverFactory._create_selenoid_capabilities(
                "MicrosoftEdge", browser_version, test_name, 
                enable_video, enable_vnc, enable_log, screen_resolution
            )
            
            # Update Edge options with Selenoid capabilities
            for key, value in capabilities.items():
                options.set_capability(key, value)
            
            # Create Remote WebDriver
            try:
                logger.info(f"Connecting to Selenoid at {remote_url} with Edge {browser_version}")
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=options
                )
                return driver
            except Exception as e:
                logger.error(f"Failed to create Remote WebDriver: {str(e)}")
                raise
        else:
            # Create local Edge WebDriver
            service = EdgeService()
            return webdriver.Edge(service=service, options=options)