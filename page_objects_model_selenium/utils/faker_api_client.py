import requests
import logging
import allure
import json
import os
import random
import string
from requests.exceptions import RequestException, Timeout, ConnectionError
from faker import Faker

logger = logging.getLogger(__name__)
faker = Faker()

class FakerApiClient:
    """Client to interact with the Faker API for test data generation with enhanced data cleaning"""
    
    def __init__(self, base_url=None):
        """Initialize the Faker API client"""
        self.base_url = base_url or os.environ.get('FAKER_API_URL', 'http://faker:5000')
        self.local_faker = Faker()
        logger.info(f"Initialized Faker API client with base URL: {self.base_url}")
    
    def _make_request(self, endpoint, params=None, timeout=10):
        """Make a request to the Faker API with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        with allure.step(f"Make request to Faker API: {url}"):
            try:
                logger.info(f"Making request to {url} with params: {params}")
                
                response = requests.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                
                logger.info(f"Received response from {url} with status code: {response.status_code}")
                
                return response.json()
                
            except (Timeout, ConnectionError, RequestException) as e:
                logger.error(f"Error making request to {url}: {str(e)}")
                raise
    
    def get_users(self, quantity=1, invalid=False):
        """
        Get and clean user data from Faker API or generate locally
        
        Args:
            quantity (int): Number of users to generate (1-100)
            invalid (bool): Whether to generate invalid user data
            
        Returns:
            list: List of user dictionaries with clean data
        """
        try:
            # Try to get users from API first
            params = {
                'quantity': quantity,
                'invalid': str(invalid).lower()
            }
            
            try:
                response = self._make_request('/generate/user', params)
                
                # Check if response is valid
                if isinstance(response, list) and len(response) > 0:
                    # Clean and validate the data
                    return [self._clean_user_data(user, invalid) for user in response]
            except Exception as e:
                logger.warning(f"Could not fetch users from API: {e}")
            
            # If we get here, we need to generate users locally
            return self._generate_local_users(quantity, invalid)
            
        except Exception as e:
            logger.error(f"Error in get_users: {e}")
            return self._generate_local_users(quantity, invalid)
    
    def _clean_user_data(self, user, invalid=False):
        """
        Clean and standardize user data
        
        Args:
            user (dict): User dictionary to clean
            invalid (bool): Whether user data should be invalid
            
        Returns:
            dict: Cleaned user dictionary
        """
        # Create a basic clean user structure
        clean_user = {
            "username": "",
            "email": "",
            "password": "",
            "first_name": "",
            "last_name": ""
        }
        
        # Extract and clean relevant fields
        if user:
            # Clean username - remove whitespace and special chars if needed
            username = user.get('username', '')
            if username:
                clean_user['username'] = username.strip()
            
            # Clean email - ensure it's a valid format
            email = user.get('email', '')
            if email and '@' in email:
                clean_user['email'] = email.strip()
            else:
                clean_user['email'] = f"{clean_user['username']}@example.com"
            
            # Ensure password meets requirements
            password = user.get('password', '')
            if password and len(password) >= 8:
                clean_user['password'] = password.strip()
            else:
                clean_user['password'] = f"Password123!" if not invalid else "short"
            
            # Clean name fields
            clean_user['first_name'] = user.get('first_name', 'Test').strip()
            clean_user['last_name'] = user.get('last_name', 'User').strip()
            clean_user['full_name'] = f"{clean_user['first_name']} {clean_user['last_name']}"
        
        # For invalid users, we might need to adjust the data
        if invalid:
            if random.choice([True, False]):
                # Make username invalid (empty or too short)
                clean_user['username'] = "" if random.choice([True, False]) else "a"
            else:
                # Make password invalid (too short)
                clean_user['password'] = "123"
        
        return clean_user
    
    def _generate_local_users(self, quantity=1, invalid=False):
        """
        Generate user data locally using Faker library
        
        Args:
            quantity (int): Number of users to generate
            invalid (bool): Whether to generate invalid user data
            
        Returns:
            list: List of user dictionaries
        """
        users = []
        
        for i in range(quantity):
            username = self.local_faker.user_name()
            password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%^&*', k=12))
            
            user = {
                "username": username,
                "email": self.local_faker.email(),
                "password": password,
                "first_name": self.local_faker.first_name(),
                "last_name": self.local_faker.last_name(),
            }
            
            user["full_name"] = f"{user['first_name']} {user['last_name']}"
            
            # Modify data if invalid is requested
            if invalid:
                invalid_type = random.choice(['username', 'password', 'email'])
                
                if invalid_type == 'username':
                    user['username'] = "" if random.choice([True, False]) else "a"
                elif invalid_type == 'password':
                    user['password'] = "123"
                else:
                    user['email'] = user['email'].replace('@', '')
            
            users.append(user)
        
        logger.info(f"Generated {len(users)} users locally")
        return users
    
    def get_test_account(self):
        """
        Get a reliable test account - good for testing known credentials
        
        Returns:
            dict: User dictionary with test account
        """
        return {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Test@123456",
            "first_name": "Test",
            "last_name": "User",
            "full_name": "Test User"
        }