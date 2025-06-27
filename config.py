"""
Configuration file for SmeHub API.
Contains API keys, settings, and other configuration parameters.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings."""
    
    # Claude Anthropic API configuration
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')  # Default to Claude 3.5 Sonnet
    CLAUDE_MAX_TOKENS = int(os.getenv('CLAUDE_MAX_TOKENS', '4000'))
    
    # Web search configuration
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')  # For web search capabilities
    MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', '5'))
    
    # Report generation settings
    REPORT_GENERATION_TIMEOUT = int(os.getenv('REPORT_GENERATION_TIMEOUT', '60'))  # seconds
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        errors = []
        
        if not cls.CLAUDE_API_KEY:
            errors.append("CLAUDE_API_KEY is required")
        
        if not cls.TAVILY_API_KEY:
            errors.append("TAVILY_API_KEY is required for web search functionality")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True

# Create a global config instance
config = Config()
