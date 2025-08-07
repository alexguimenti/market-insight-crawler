import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'gemini')
    
    # Timeouts
    REQUEST_TIMEOUT = 30  # seconds for HTTP requests
    API_TIMEOUT = 60  # seconds for LLM API calls
    ANALYSIS_TIMEOUT = 240  # seconds for total analysis
    TOTAL_TIMEOUT = 300  # seconds for entire request
    
    # Content limits
    MAX_CONTENT_SIZE = 50000  # characters per page
    MAX_PAGES_TO_SCRAPE = 10  # maximum pages to analyze
    MAX_LINKS_TO_ANALYZE = 50  # maximum links to classify
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 5000))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    REQUEST_TIMEOUT = 60  # More lenient in development
    ANALYSIS_TIMEOUT = 300  # More time for debugging
    MAX_PAGES_TO_SCRAPE = 15  # More pages for testing

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    REQUEST_TIMEOUT = 30  # Stricter timeouts
    ANALYSIS_TIMEOUT = 180  # 3 minutes max
    MAX_PAGES_TO_SCRAPE = 8  # Fewer pages for performance
    MAX_CONTENT_SIZE = 30000  # Smaller content size
    
    # Production-specific settings
    THREADED = True
    WORKERS = int(os.getenv('WORKERS', 4))

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    REQUEST_TIMEOUT = 10  # Fast timeouts for tests
    ANALYSIS_TIMEOUT = 60  # Quick analysis for tests
    MAX_PAGES_TO_SCRAPE = 2  # Minimal pages for tests

# Environment-based configuration
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig

# Export current config
current_config = get_config()
