#!/usr/bin/env python3
"""
Test Runner Script for Authentication System Tests

This script automates the following workflow:
1. Starts the infrastructure using Docker Compose
2. Waits for services to be healthy/ready
3. Runs the tests in the test container
4. Displays results and links to reports
5. Offers cleanup options
"""

import os
import sys
import time
import argparse
import subprocess
import requests
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Configuration
INFRA_DIR = "infra"
DOCKER_COMPOSE_FILE = os.path.join(INFRA_DIR, "docker-compose.yaml")
TESTS_DIR = "page_objects_model_selenium"
SERVICE_URLS = {
    "web": "http://localhost:8000",
    "selenoid": "http://localhost:4444",
    "selenoid_ui": "http://localhost:4444/ui",
    "allure": "http://localhost:5050",
    "allure_ui": "http://localhost:5252",
    "kiwi": "http://localhost:8080",
    "dozzle": "http://localhost:8888",
}
SERVICES_TO_CHECK = ["web", "selenoid", "allure"]
TEST_CONTAINER_NAME = "infra-test-1"

def print_header(message):
    """Print a formatted header message"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_step(message):
    """Print a step message"""
    print(f"{Colors.BLUE}➡ {message}{Colors.ENDC}")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def run_command(command, cwd=None, check=True, shell=False):
    """Run a shell command and return the result"""
    try:
        if shell:
            result = subprocess.run(command, cwd=cwd, shell=True, check=check, 
                                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.run(command.split(), cwd=cwd, check=check, 
                                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return e

def check_prerequisites():
    """Check if Docker and Docker Compose are installed"""
    print_step("Checking prerequisites...")
    
    # Check Docker
    docker_result = run_command("docker --version", check=False)
    if docker_result.returncode != 0:
        print_error("Docker is not installed or not in PATH")
        return False
    
    # Check Docker Compose
    compose_result = run_command("docker-compose --version", check=False)
    if compose_result.returncode != 0:
        compose_v2_result = run_command("docker compose version", check=False)
        if compose_v2_result.returncode != 0:
            print_error("Docker Compose is not installed or not in PATH")
            return False
    
    # Check if Docker Compose file exists
    if not os.path.exists(DOCKER_COMPOSE_FILE):
        print_error(f"Docker Compose file not found at {DOCKER_COMPOSE_FILE}")
        return False
    
    print_success("Prerequisites check passed")
    return True

def start_infrastructure():
    """Start the infrastructure using Docker Compose"""
    print_step("Starting infrastructure with Docker Compose...")
    
    # Navigate to infra directory and run docker-compose up
    result = run_command("docker-compose up -d", cwd=INFRA_DIR)
    if result.returncode != 0:
        return False
    
    print_success("Infrastructure started successfully")
    return True

def wait_for_services(timeout=120):
    """Wait for all services to be ready"""
    print_step("Waiting for services to be ready...")
    
    start_time = time.time()
    services_ready = {service: False for service in SERVICES_TO_CHECK}
    
    while time.time() - start_time < timeout:
        all_ready = True
        
        for service in SERVICES_TO_CHECK:
            if not services_ready[service]:
                try:
                    response = requests.get(SERVICE_URLS[service], timeout=2)
                    if response.status_code < 400:
                        services_ready[service] = True
                        print_success(f"{service.capitalize()} is ready")
                    else:
                        all_ready = False
                except requests.RequestException:
                    all_ready = False
        
        if all_ready:
            print_success("All services are ready")
            return True
        
        # Only print waiting message if some services are still not ready
        if not all_ready:
            remaining = [s for s, ready in services_ready.items() if not ready]
            time_elapsed = time.time() - start_time
            print(f"Waiting for services: {', '.join(remaining)} ({time_elapsed:.0f}s elapsed)")
            time.sleep(5)
    
    # Timeout reached
    not_ready = [service for service, ready in services_ready.items() if not ready]
    print_error(f"Timeout waiting for services: {', '.join(not_ready)}")
    return False

def run_tests(test_path=None, markers=None):
    """Run the tests using docker-compose run"""
    print_step("Running tests...")
    
    # Build docker-compose command
    cmd = f"cd {INFRA_DIR} && docker-compose run --rm run_tests"
    
    # Add test path or default to tests/ directory
    test_path_arg = test_path if test_path else "tests/"
    
    # Build pytest args
    pytest_args = f"pytest {test_path_arg}"
    
    # Add markers if specified
    if markers:
        pytest_args += f" -m {markers}"
    
    # Add common options
    pytest_args += " -v --alluredir=/app/reports/allure-results"
    
    # Complete command with pytest args
    full_cmd = f"{cmd} {pytest_args}"
    
    print_step(f"Executing: {full_cmd}")
    
    # Execute the tests
    result = run_command(full_cmd, shell=True, check=False)
    
    # Display output 
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    # Check if tests were executed successfully
    if result.returncode == 0:
        print_success("Tests executed successfully")
    else:
        print_warning("Some tests failed or encountered errors")
    
    return result.returncode

def display_results():
    """Display results and links to reports"""
    print_header("Test Results")
    
    print("Report URLs:")
    print(f"{Colors.CYAN}Allure Report:{Colors.ENDC} {SERVICE_URLS['allure_ui']}")
    print(f"{Colors.CYAN}Selenoid UI:{Colors.ENDC} {SERVICE_URLS['selenoid_ui']}")
    print(f"{Colors.CYAN}Kiwi TCMS:{Colors.ENDC} {SERVICE_URLS['kiwi']}")
    print(f"{Colors.CYAN}Dozzle (Logs):{Colors.ENDC} {SERVICE_URLS['dozzle']}")

def cleanup_infrastructure():
    """Stop and remove the infrastructure"""
    print_step("Cleaning up infrastructure...")
    
    result = run_command("docker-compose down", cwd=INFRA_DIR)
    if result.returncode == 0:
        print_success("Infrastructure stopped and removed successfully")
    else:
        print_error("Failed to stop and remove infrastructure")

def cleanup_reports():
    """Clean up report directories"""
    print_step("Cleaning up reports...")
    
    # Define report directories to clean
    report_dirs = [
        "reports/allure-results",
        "reports/screenshots",
        "reports/videos"
    ]
    
    # Iterate through each directory
    for report_dir in report_dirs:
        dir_path = os.path.join(TESTS_DIR, report_dir)
        if os.path.exists(dir_path):
            try:
                # Remove all files but keep directory structure
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        for subitem in os.listdir(item_path):
                            subitem_path = os.path.join(item_path, subitem)
                            if os.path.isfile(subitem_path):
                                os.remove(subitem_path)
                print_success(f"Cleaned {report_dir}")
            except Exception as e:
                print_error(f"Failed to clean {report_dir}: {str(e)}")

def fix_common_issues():
    """Fix common issues that might cause tests to fail"""
    print_step("Fixing common issues...")
    
    # Fix 1: Make sure pytest.ini has all required markers
    pytest_ini_path = os.path.join(TESTS_DIR, "pytest.ini")
    if os.path.exists(pytest_ini_path):
        with open(pytest_ini_path, "r") as f:
            pytest_ini_content = f.read()
        
        # Check if required markers are defined
        required_markers = ["smoke", "acceptance", "function", "integration", "security", "ui", "nondestructive"]
        missing_markers = []
        
        for marker in required_markers:
            if marker + ":" not in pytest_ini_content:
                missing_markers.append(marker)
        
        if missing_markers:
            print_warning(f"Missing markers in pytest.ini: {', '.join(missing_markers)}")
            
            # Add missing markers
            markers_section = "markers =\n"
            for marker in required_markers:
                marker_desc = {
                    "smoke": "Smoke tests that verify basic functionality",
                    "acceptance": "Acceptance tests that verify critical user workflows",
                    "function": "Functional tests that verify specific features",
                    "integration": "Integration tests that verify interactions between components",
                    "security": "Security tests that verify system protection mechanisms",
                    "ui": "Tests that verify user interface elements and layout",
                    "nondestructive": "Tests that don't modify test data"
                }.get(marker, marker)
                
                if marker + ":" not in pytest_ini_content:
                    markers_section += f"    {marker}: {marker_desc}\n"
                else:
                    # Extract existing marker line
                    for line in pytest_ini_content.splitlines():
                        if line.strip().startswith(marker + ":"):
                            markers_section += f"    {line.strip()}\n"
                            break
            
            # Update pytest.ini
            new_content = pytest_ini_content
            if "markers =" in pytest_ini_content:
                # Replace markers section
                start_idx = pytest_ini_content.find("markers =")
                end_idx = start_idx
                for i, char in enumerate(pytest_ini_content[start_idx:], start_idx):
                    if char == '\n' and i > start_idx + 10:  # Look for newline after section
                        line = pytest_ini_content[end_idx:i].strip()
                        if not line or line[0] == '[' or ':' not in line:
                            end_idx = i
                            break
                        end_idx = i + 1
                
                new_content = pytest_ini_content[:start_idx] + markers_section + pytest_ini_content[end_idx:]
            else:
                # Add markers section after [pytest]
                if "[pytest]" in pytest_ini_content:
                    new_content = pytest_ini_content.replace("[pytest]", "[pytest]\n" + markers_section)
                else:
                    new_content = "[pytest]\n" + markers_section + "\n" + pytest_ini_content
            
            # Write updated content
            with open(pytest_ini_path, "w") as f:
                f.write(new_content)
            
            print_success(f"Updated pytest.ini with missing markers: {', '.join(missing_markers)}")
        else:
            print_success("All required markers are already defined in pytest.ini")
    else:
        print_warning(f"pytest.ini not found at {pytest_ini_path}")
        
        # Create pytest.ini with all required markers
        pytest_ini_content = """[pytest]
markers =
    smoke: Smoke tests that verify basic functionality
    acceptance: Acceptance tests that verify critical user workflows
    function: Functional tests that verify specific features
    integration: Integration tests that verify interactions between components
    security: Security tests that verify system protection mechanisms
    ui: Tests that verify user interface elements and layout
    nondestructive: Tests that don't modify test data

addopts = 
    --strict-markers
    --tb=native
    --alluredir=reports/allure-results

testpaths = tests

log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Default timeout for all tests
timeout = 60
"""
        # Create directories if needed
        os.makedirs(os.path.dirname(pytest_ini_path), exist_ok=True)
        
        # Write pytest.ini
        with open(pytest_ini_path, "w") as f:
            f.write(pytest_ini_content)
        
        print_success(f"Created pytest.ini with all required markers at {pytest_ini_path}")
    
    # Fix 2: Copy pytest.ini to docker container if needed
    if os.path.exists(pytest_ini_path):
        # Check if container is running
        container_check = run_command(f"docker ps -q -f name={TEST_CONTAINER_NAME}", shell=True, check=False)
        if container_check.stdout.strip():
            # Copy pytest.ini to container
            copy_cmd = f"docker cp {pytest_ini_path} {TEST_CONTAINER_NAME}:/app/pytest.ini"
            copy_result = run_command(copy_cmd, shell=True, check=False)
            if copy_result.returncode == 0:
                print_success(f"Copied pytest.ini to test container")
            else:
                print_warning(f"Failed to copy pytest.ini to test container: {copy_result.stderr}")
    
    # Other fixes can be added here as needed
    
    return True
def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Run Selenium tests with Docker infrastructure")
    parser.add_argument("--test", help="Specific test file or directory to run")
    parser.add_argument("--markers", help="PyTest markers to filter tests (e.g. 'smoke or acceptance')")
    parser.add_argument("--skip-infra", action="store_true", help="Skip starting infrastructure (use if already running)")
    parser.add_argument("--clean", action="store_true", help="Clean up infrastructure after tests")
    parser.add_argument("--clean-reports", action="store_true", help="Clean up reports before running tests")
    parser.add_argument("--fix", action="store_true", help="Fix common issues before running tests")
    
    args = parser.parse_args()
    
    print_header("Authentication System Test Runner")
    
    # Ensure we're in the project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check prerequisites
    if not check_prerequisites():
        return 1
    
    # Fix common issues if requested
    if args.fix:
        fix_common_issues()
    
    # Clean up reports if requested
    if args.clean_reports:
        cleanup_reports()
    
    # Start infrastructure if not skipped
    if not args.skip_infra:
        if not start_infrastructure():
            return 1
        
        # Wait for services to be ready
        if not wait_for_services():
            print_warning("Some services are not ready, but continuing anyway...")
    else:
        print_step("Skipping infrastructure startup as requested")
    
    # Run tests
    test_result = run_tests(args.test, args.markers)
    
    # Display results
    display_results()
    
    # Clean up if requested
    if args.clean:
        cleanup_infrastructure()
    
    return test_result

if __name__ == "__main__":
    sys.exit(main())