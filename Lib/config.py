"""
Configuration Management for Allplan Render AI

Handles loading and managing API keys, paths, and settings.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for the plugin"""

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration

        Args:
            env_file: Path to .env file. If None, searches in standard locations.
        """

        # Determine .env file location
        if env_file and os.path.exists(env_file):
            self.env_file = env_file
        else:
            # Search in standard locations
            self.env_file = self._find_env_file()

        # Load environment variables
        if self.env_file:
            load_dotenv(self.env_file)
        else:
            print("Warning: .env file not found. Using environment variables only.")

        # Load configuration
        self._load_config()

    def _find_env_file(self) -> Optional[str]:
        """Find .env file in standard locations"""

        possible_paths = [
            # Current directory
            Path(".env"),
            # Parent directory
            Path("../.env"),
            # VisualScripts directory
            Path(__file__).parent.parent / ".env",
            # Allplan Etc directory (primary)
            Path("C:/ProgramData/Nemetschek/Allplan/2025/Etc/VisualScripts/AllplanAIRender/.env"),
            # Allplan Std directory (fallback)
            Path("C:/ProgramData/Nemetschek/Allplan/2025/Std/VisualScripts/AllplanAIRender/.env"),
        ]

        for path in possible_paths:
            if path.exists():
                return str(path.resolve())

        return None

    def _load_config(self):
        """Load configuration from environment variables"""

        # Google API Keys
        self.GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY", "")
        self.GOOGLE_CLOUD_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "")
        self.GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        self.MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

        # Plugin settings
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        # Paths
        self.OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "C:/Allplan_Output"))
        self.TEMP_DIR = Path(os.getenv("TEMP_DIR", "C:/Temp/AllplanRenderAI"))

        # Create directories if they don't exist
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.TEMP_DIR.mkdir(parents=True, exist_ok=True)

        # Default rendering settings
        self.DEFAULT_RESOLUTION = os.getenv("DEFAULT_RESOLUTION", "2K")
        self.DEFAULT_USE_PRO_MODEL = os.getenv("DEFAULT_USE_PRO_MODEL", "false").lower() == "true"
        self.DEFAULT_STYLE = os.getenv("DEFAULT_STYLE", "Modern")
        self.DEFAULT_LIGHTING = os.getenv("DEFAULT_LIGHTING", "Noon")

        # Cost tracking
        self.ENABLE_COST_TRACKING = os.getenv("ENABLE_COST_TRACKING", "true").lower() == "true"
        self.MAX_MONTHLY_COST_USD = float(os.getenv("MAX_MONTHLY_COST_USD", "100.0"))

    def validate(self) -> bool:
        """
        Validate that required configuration is present

        Returns:
            True if configuration is valid
        """

        if not self.GEMINI_API_KEY:
            print("ERROR: GOOGLE_GEMINI_API_KEY not configured in .env file")
            return False

        return True

    def get_model_name(self, use_pro: bool) -> str:
        """Get Gemini model name"""
        return "gemini-3-pro-image" if use_pro else "gemini-2.5-flash-image"

    def __repr__(self) -> str:
        return (
            f"Config(env_file={self.env_file}, "
            f"gemini_api_key={'*' * 8 if self.GEMINI_API_KEY else 'NOT SET'}, "
            f"debug={self.DEBUG_MODE})"
        )


# Global config instance
_config = None

def get_config() -> Config:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config
