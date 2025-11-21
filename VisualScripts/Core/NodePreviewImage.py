"""
Node: Preview Image

Opens image in system default viewer for quick preview.

Inputs:
- ImagePath (String): Path to image to preview
- AutoOpen (Boolean): Automatically open preview

Outputs:
- Previewed (Boolean): True if preview was shown
"""

from __future__ import annotations
import os
import sys
import subprocess
import platform
from typing import TYPE_CHECKING, Any

# Add Lib to path
lib_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Lib')
if lib_path not in sys.path:
    sys.path.insert(0, os.path.abspath(lib_path))

from logger import get_logger

import AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement, _version: float) -> bool:
    return True


def create_element(build_ele: BuildingElement, doc: AllplanEleAdapter.DocumentAdapter) -> Any:
    element = NodePreviewImage(doc)
    return element.execute(build_ele)


class NodePreviewImage:
    """Preview Image Node implementation"""

    def __init__(self, doc: AllplanEleAdapter.DocumentAdapter):
        self.doc = doc
        self.logger = get_logger("NodePreviewImage")

    def execute(self, build_ele: BuildingElement) -> tuple:
        self.logger.info("="*60)
        self.logger.info("NODE: Preview Image")
        self.logger.info("="*60)

        try:
            # Get inputs
            image_path = build_ele.ImagePath.value
            auto_open = build_ele.AutoOpen.value

            self.logger.info(f"Image path: {image_path}")
            self.logger.info(f"Auto open: {auto_open}")

            # Validate
            if not image_path or not os.path.exists(image_path):
                self.logger.error(f"Image not found: {image_path}")
                return ([], [False])

            # Open in default viewer if requested
            if auto_open:
                self.logger.info("Opening image in default viewer...")
                self._open_image(image_path)
                self.logger.info("✓ Preview opened")
            else:
                self.logger.info("Auto-open disabled, skipping preview")

            self.logger.info("="*60 + "\n")

            # Return: Previewed
            return ([], [auto_open])

        except Exception as e:
            self.logger.error(f"Failed to preview image: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return ([], [False])

    def _open_image(self, image_path: str):
        """Open image with system default viewer"""

        try:
            if platform.system() == 'Windows':
                # Windows
                os.startfile(image_path)
            elif platform.system() == 'Darwin':
                # macOS
                subprocess.run(['open', image_path])
            else:
                # Linux
                subprocess.run(['xdg-open', image_path])

        except Exception as e:
            self.logger.warning(f"Could not open image automatically: {e}")
            self.logger.info(f"Please open manually: {image_path}")
