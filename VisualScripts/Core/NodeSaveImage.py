"""
Node: Save Image

Saves an image to disk with custom filename and format.

Inputs:
- ImagePath (String): Path to input image
- OutputPath (String): Destination file path
- Format (String): "PNG" or "JPEG"
- Quality (Integer): JPEG quality 1-100
- AddTimestamp (Boolean): Add timestamp to filename

Outputs:
- SavedPath (String): Final saved file path
- FileSize (Integer): File size in KB
- Success (Boolean): True if save successful
"""

from __future__ import annotations
import os
import sys
from typing import TYPE_CHECKING, Any
from datetime import datetime
from pathlib import Path

# Add Lib to path
lib_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Lib')
if lib_path not in sys.path:
    sys.path.insert(0, os.path.abspath(lib_path))

from config import get_config
from logger import get_logger
from image_processor import ImageProcessor

import AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement, _version: float) -> bool:
    return True


def create_element(build_ele: BuildingElement, doc: AllplanEleAdapter.DocumentAdapter) -> Any:
    element = NodeSaveImage(doc)
    return element.execute(build_ele)


class NodeSaveImage:
    """Save Image Node implementation"""

    def __init__(self, doc: AllplanEleAdapter.DocumentAdapter):
        self.doc = doc
        self.logger = get_logger("NodeSaveImage")
        self.config = get_config()
        self.processor = ImageProcessor()

    def execute(self, build_ele: BuildingElement) -> tuple:
        self.logger.info("="*60)
        self.logger.info("NODE: Save Image")
        self.logger.info("="*60)

        try:
            # Get inputs
            image_path = build_ele.ImagePath.value
            output_path = build_ele.OutputPath.value
            format_type = build_ele.Format.value
            quality = build_ele.Quality.value
            add_timestamp = build_ele.AddTimestamp.value

            self.logger.info(f"Input image: {image_path}")
            self.logger.info(f"Output path: {output_path}")
            self.logger.info(f"Format: {format_type}, Quality: {quality}")
            self.logger.info(f"Add timestamp: {add_timestamp}")

            # Validate input
            if not image_path or not os.path.exists(image_path):
                self.logger.error(f"Input image not found: {image_path}")
                return ([], [None, 0, False])

            if not output_path:
                self.logger.error("No output path provided")
                return ([], [None, 0, False])

            # Load image
            image = self.processor.load_image(image_path)

            # Add timestamp to filename if requested
            final_output_path = output_path
            if add_timestamp:
                path_obj = Path(output_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{path_obj.stem}_{timestamp}{path_obj.suffix}"
                final_output_path = str(path_obj.parent / filename)

            # Save image
            self.logger.info(f"Saving to: {final_output_path}")
            saved_path = self.processor.save_image(
                image,
                final_output_path,
                format=format_type,
                quality=quality
            )

            # Get file size
            file_size_kb = os.path.getsize(saved_path) // 1024

            self.logger.info(f"✓ Image saved successfully ({file_size_kb} KB)")
            self.logger.info("="*60 + "\n")

            # Return: SavedPath, FileSize, Success
            return ([], [saved_path, file_size_kb, True])

        except Exception as e:
            self.logger.error(f"Failed to save image: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return ([], [None, 0, False])
