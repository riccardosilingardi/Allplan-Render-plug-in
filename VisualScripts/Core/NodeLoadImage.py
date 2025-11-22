"""
Node: Load Image

Loads an image file and makes it available in the workflow.

Inputs:
- FilePath (String): Path to image file
- AutoResize (Boolean): Automatically resize to target resolution
- TargetResolution (String): "1K", "2K", or "4K"

Outputs:
- ImagePath (String): Path to loaded/processed image
- Width (Integer): Image width in pixels
- Height (Integer): Image height in pixels
- Success (Boolean): True if load successful
"""

from __future__ import annotations
import os
import sys
from typing import TYPE_CHECKING, Any

# Add Lib to path
lib_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Lib')
if lib_path not in sys.path:
    sys.path.insert(0, os.path.abspath(lib_path))

# Imports from our libraries
from config import get_config
from logger import get_logger
from image_processor import ImageProcessor

# Allplan imports
import AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement, _version: float) -> bool:
    """Check Allplan version"""
    return True


def create_element(build_ele: BuildingElement, doc: AllplanEleAdapter.DocumentAdapter) -> Any:
    """
    Create the Visual Scripting node element

    Args:
        build_ele: Building element with parameters
        doc: Document adapter

    Returns:
        Tuple of (model_ele_list, handles)
    """

    element = NodeLoadImage(doc)
    return element.execute(build_ele)


class NodeLoadImage:
    """Load Image Node implementation"""

    def __init__(self, doc: AllplanEleAdapter.DocumentAdapter):
        """
        Initialize node

        Args:
            doc: Document adapter
        """
        self.doc = doc
        self.logger = get_logger("NodeLoadImage")
        self.config = get_config()
        self.processor = ImageProcessor()

    def execute(self, build_ele: BuildingElement) -> tuple:
        """
        Execute the node

        Args:
            build_ele: Building element with input parameters

        Returns:
            Tuple of (model_ele_list, [output_values])
        """

        self.logger.info("="*60)
        self.logger.info("NODE: Load Image")
        self.logger.info("="*60)

        try:
            # Get input parameters
            file_path = build_ele.FilePath.value
            auto_resize = build_ele.AutoResize.value
            target_resolution = build_ele.TargetResolution.value

            self.logger.info(f"Input file: {file_path}")
            self.logger.info(f"Auto resize: {auto_resize}")
            if auto_resize:
                self.logger.info(f"Target resolution: {target_resolution}")

            # Validate input
            if not file_path:
                self.logger.error("No file path provided")
                return ([], [None, 0, 0, False])

            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return ([], [None, 0, 0, False])

            # Load image
            self.logger.info("Loading image...")
            image = self.processor.load_image(file_path)

            original_width, original_height = image.size
            self.logger.info(f"Original size: {original_width}x{original_height}")

            # Auto-resize if requested
            if auto_resize:
                self.logger.info(f"Resizing to {target_resolution}...")
                image = self.processor.resize_to_resolution(
                    image,
                    target_resolution,
                    maintain_aspect_ratio=True
                )

                new_width, new_height = image.size
                self.logger.info(f"Resized to: {new_width}x{new_height}")

            # Save to temp location for passing to next node
            output_path = self.processor.save_temp_image(image, prefix="loaded")
            self.logger.info(f"Saved to: {output_path}")

            # Get final dimensions
            width, height = image.size

            self.logger.info("✓ Image loaded successfully")
            self.logger.info("="*60 + "\n")

            # Return outputs: ImagePath, Width, Height, Success
            return ([], [output_path, width, height, True])

        except Exception as e:
            self.logger.error(f"Failed to load image: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return ([], [None, 0, 0, False])
