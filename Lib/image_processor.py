"""
Image Processing Utilities

Handles image loading, saving, resizing, and format conversions.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional, Union

from PIL import Image
import numpy as np


class ImageProcessor:
    """Image processing utilities for Visual Scripting nodes"""

    RESOLUTION_MAP = {
        "1K": (1024, 1024),
        "2K": (2048, 2048),
        "4K": (4096, 4096),
    }

    def __init__(self, temp_dir: Optional[str] = None):
        """
        Initialize image processor

        Args:
            temp_dir: Directory for temporary files. If None, uses default.
        """

        if temp_dir:
            self.temp_dir = Path(temp_dir)
        else:
            self.temp_dir = Path("C:/Temp/AllplanRenderAI")

        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def load_image(self, file_path: str) -> Image.Image:
        """
        Load image from file

        Args:
            file_path: Path to image file

        Returns:
            PIL Image object

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be loaded
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")

        try:
            image = Image.open(file_path)
            # Convert to RGB if necessary (handles RGBA, palette, etc.)
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGB")
            return image
        except Exception as e:
            raise IOError(f"Failed to load image {file_path}: {e}")

    def save_image(
        self,
        image: Image.Image,
        file_path: str,
        format: str = "PNG",
        quality: int = 95
    ) -> str:
        """
        Save image to file

        Args:
            image: PIL Image to save
            file_path: Destination path
            format: Image format (PNG, JPEG, etc.)
            quality: Quality for JPEG (1-100)

        Returns:
            Absolute path to saved file
        """

        # Ensure directory exists
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save with appropriate settings
        save_kwargs = {}
        if format.upper() == "JPEG" or file_path.suffix.lower() in (".jpg", ".jpeg"):
            save_kwargs["quality"] = quality
            # Convert RGBA to RGB for JPEG
            if image.mode == "RGBA":
                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                image = rgb_image

        image.save(str(file_path), format=format, **save_kwargs)

        return str(file_path.resolve())

    def save_temp_image(
        self,
        image: Image.Image,
        prefix: str = "temp",
        format: str = "PNG"
    ) -> str:
        """
        Save image to temporary location

        Args:
            image: PIL Image to save
            prefix: Prefix for temp filename
            format: Image format

        Returns:
            Path to saved temp file
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{prefix}_{timestamp}_{unique_id}.{format.lower()}"

        temp_path = self.temp_dir / filename

        return self.save_image(image, str(temp_path), format=format)

    def resize_to_resolution(
        self,
        image: Image.Image,
        resolution: str,
        maintain_aspect_ratio: bool = True
    ) -> Image.Image:
        """
        Resize image to target resolution

        Args:
            image: PIL Image to resize
            resolution: Target resolution ("1K", "2K", "4K")
            maintain_aspect_ratio: If True, fits image within target size

        Returns:
            Resized PIL Image
        """

        if resolution not in self.RESOLUTION_MAP:
            raise ValueError(f"Invalid resolution: {resolution}. Must be 1K, 2K, or 4K")

        target_size = self.RESOLUTION_MAP[resolution]

        if maintain_aspect_ratio:
            # Fit within target size maintaining aspect ratio
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            return image
        else:
            # Exact resize (may distort)
            return image.resize(target_size, Image.Resampling.LANCZOS)

    def resize_to_dimensions(
        self,
        image: Image.Image,
        width: int,
        height: int,
        maintain_aspect_ratio: bool = True
    ) -> Image.Image:
        """
        Resize image to specific dimensions

        Args:
            image: PIL Image to resize
            width: Target width
            height: Target height
            maintain_aspect_ratio: If True, fits image within dimensions

        Returns:
            Resized PIL Image
        """

        if maintain_aspect_ratio:
            image.thumbnail((width, height), Image.Resampling.LANCZOS)
            return image
        else:
            return image.resize((width, height), Image.Resampling.LANCZOS)

    def to_numpy(self, image: Image.Image) -> np.ndarray:
        """Convert PIL Image to numpy array"""
        return np.array(image)

    def from_numpy(self, array: np.ndarray) -> Image.Image:
        """Convert numpy array to PIL Image"""
        return Image.fromarray(array)

    def get_image_info(self, image: Image.Image) -> dict:
        """
        Get image metadata

        Args:
            image: PIL Image

        Returns:
            Dict with image information
        """

        return {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "format": image.format,
            "size_bytes": len(image.tobytes()) if image else 0,
        }

    def create_thumbnail(
        self,
        image: Image.Image,
        max_size: Tuple[int, int] = (256, 256)
    ) -> Image.Image:
        """
        Create thumbnail of image

        Args:
            image: Source image
            max_size: Maximum dimensions (width, height)

        Returns:
            Thumbnail image
        """

        thumb = image.copy()
        thumb.thumbnail(max_size, Image.Resampling.LANCZOS)
        return thumb

    def cleanup_temp_files(self, older_than_hours: int = 24):
        """
        Clean up old temporary files

        Args:
            older_than_hours: Delete files older than this many hours
        """

        import time

        current_time = time.time()
        cutoff_time = current_time - (older_than_hours * 3600)

        deleted_count = 0

        for file_path in self.temp_dir.glob("*"):
            if file_path.is_file():
                file_age = file_path.stat().st_mtime
                if file_age < cutoff_time:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                    except Exception as e:
                        print(f"Warning: Failed to delete {file_path}: {e}")

        print(f"Cleaned up {deleted_count} temporary files")
