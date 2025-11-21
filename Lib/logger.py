"""
Logging utilities for Allplan Render AI

Provides consistent logging across all nodes.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """Simple logger for Visual Scripting nodes"""

    def __init__(self, node_name: str, log_file: Optional[str] = None):
        """
        Initialize logger

        Args:
            node_name: Name of the node (for prefixing messages)
            log_file: Optional log file path. If None, logs to stdout only.
        """

        self.node_name = node_name
        self.log_file = log_file

        # Create log file if specified
        if self.log_file:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

    def _format_message(self, level: str, message: str) -> str:
        """Format log message with timestamp and node name"""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] [{level}] [{self.node_name}] {message}"

    def _write(self, formatted_message: str):
        """Write message to stdout and optionally to file"""

        # Print to stdout
        print(formatted_message)

        # Write to file if configured
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(formatted_message + "\n")
            except Exception as e:
                print(f"Warning: Failed to write to log file: {e}")

    def debug(self, message: str):
        """Log debug message"""
        self._write(self._format_message("DEBUG", message))

    def info(self, message: str):
        """Log info message"""
        self._write(self._format_message("INFO", message))

    def warning(self, message: str):
        """Log warning message"""
        self._write(self._format_message("WARNING", message))

    def error(self, message: str):
        """Log error message"""
        self._write(self._format_message("ERROR", message))

    def critical(self, message: str):
        """Log critical error message"""
        self._write(self._format_message("CRITICAL", message))


# Global log file path
DEFAULT_LOG_FILE = "C:/Temp/AllplanRenderAI/allplan_render_ai.log"

def get_logger(node_name: str) -> Logger:
    """
    Get a logger instance for a node

    Args:
        node_name: Name of the node

    Returns:
        Logger instance
    """
    return Logger(node_name, DEFAULT_LOG_FILE)
