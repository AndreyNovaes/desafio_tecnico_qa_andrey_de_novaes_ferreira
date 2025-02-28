import os
import json
import logging
from utils.faker_api_client import FakerApiClient

logger = logging.getLogger(__name__)
_faker_client = None

def _get_faker_client():
    """Get the singleton FakerApiClient instance"""
    global _faker_client
    if _faker_client is None:
        _faker_client = FakerApiClient()
    return _faker_client

def get_valid_user():
    """
    Get valid user credentials for testing.
    Priority:
    1. From test_user_data.json file (previously registered user)
    2. From Faker API
    3. From fallback data
    """
    try:
        # Try to read from saved file first
        with open("reports/test_user_data.json", "r") as f:
            user_data = json.load(f)
            logger.info(f"Using saved user data for: {user_data.get('username')}")
            return user_data
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, try to get from Faker API
        faker_client = _get_faker_client()
        try:
            # Get a user from the Faker API
            users = faker_client.get_users(quantity=1, invalid=False)
            if users and len(users) > 0:
                logger.info(f"Using Faker API generated user: {users[0].get('username')}")
                return users[0]
        except Exception as e:
            logger.warning(f"Failed to get user from Faker API: {e}")
        
        # Use the test account as last resort
        logger.info("Using default test account")
        return faker_client.get_test_account()

def generate_random_user():
    """
    Generate random user data for registration tests.
    """
    faker_client = _get_faker_client()
    users = faker_client.get_users(quantity=1, invalid=False)
    if users and len(users) > 0:
        return users[0]
    return faker_client.get_test_account()

def get_invalid_credentials():
    """
    Return a list of invalid credential combinations for negative testing.
    """
    faker_client = _get_faker_client()
    valid_user = get_valid_user()
    
    # Generate some invalid users
    invalid_users = faker_client.get_users(quantity=2, invalid=True)
    
    # Build credential sets
    credentials = [
        {
            "username": invalid_users[0]['username'] if invalid_users else "usuario_inexistente",
            "password": "senha123",
            "description": "Non-existent user"
        },
        {
            "username": valid_user["username"],
            "password": "senha_incorreta",
            "description": "Valid user with incorrect password"
        }
    ]
    
    # Add an invalid user from Faker if available
    if len(invalid_users) > 1:
        credentials.append({
            "username": invalid_users[1]['username'],
            "password": invalid_users[1]['password'],
            "description": "Invalid credentials from Faker"
        })
    
    return credentials
