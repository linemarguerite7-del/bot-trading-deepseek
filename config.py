#!/usr/bin/env python3
"""
Configuration module for Bot Trading Deepseek
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class"""
    
    # API Configuration
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
    
    # Trading Settings
    TRADING_ENABLED = os.getenv('TRADING_ENABLED', 'false').lower() == 'true'
    UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', '60'))
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))
    TIMEOUT = int(os.getenv('TIMEOUT', '30'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        required = ['DEEPSEEK_API_KEY']
        return all(getattr(cls, key) for key in required)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    TRADING_ENABLED = False


def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('ENVIRONMENT', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return config_map.get(env.lower(), DevelopmentConfig)
