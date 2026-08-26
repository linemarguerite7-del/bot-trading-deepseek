#!/usr/bin/env python3
"""
Tests for configuration module
"""

import os
import pytest
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig, get_config


class TestConfig:
    """Test configuration classes"""
    
    def test_development_config(self):
        """Test development configuration"""
        config = DevelopmentConfig
        assert config.DEBUG is True
        assert config.TESTING is False
    
    def test_production_config(self):
        """Test production configuration"""
        config = ProductionConfig
        assert config.DEBUG is False
        assert config.TESTING is False
    
    def test_testing_config(self):
        """Test testing configuration"""
        config = TestingConfig
        assert config.DEBUG is True
        assert config.TESTING is True
        assert config.TRADING_ENABLED is False
    
    def test_get_config_development(self):
        """Test get_config for development"""
        config = get_config('development')
        assert config.DEBUG is True
    
    def test_get_config_production(self):
        """Test get_config for production"""
        config = get_config('production')
        assert config.DEBUG is False
    
    def test_get_config_default(self):
        """Test get_config default"""
        config = get_config()
        assert config is not None
