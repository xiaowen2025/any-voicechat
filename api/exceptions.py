class ApiKeyError(Exception):
    """Custom exception for API key errors."""
    pass

class ImageGenerationError(Exception):
    """Custom exception for image generation errors."""
    pass

class AppNotFoundError(Exception):
    """Custom exception for when an app is not found."""
    pass

class MalformedAppConfigError(Exception):
    """Custom exception for malformed app configuration files."""
    pass
