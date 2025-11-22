"""
Node: AI Render Basic

Generate photorealistic architectural renders using Google Gemini (Nano Banana / Nano Banana Pro).

Inputs:
- InputImagePath (String): Path to input viewport image
- Prompt (String): Description of desired render
- StylePreset (String): Architectural style preset
- LightingPreset (String): Lighting/time of day preset
- Resolution (String): Output resolution (1K, 2K, 4K)
- UseProModel (Boolean): Use Nano Banana Pro (higher quality, higher cost)

Outputs:
- RenderedImagePath (String): Path to generated render
- Cost (Float): API cost in USD
- ProcessTime (Float): Generation time in seconds
- Success (Boolean): True if successful
"""

from __future__ import annotations
import os
import sys
import time
from typing import TYPE_CHECKING, Any

# Add Lib to path
lib_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Lib')
if lib_path not in sys.path:
    sys.path.insert(0, os.path.abspath(lib_path))

from config import get_config
from logger import get_logger
from image_processor import ImageProcessor
from ai_client import GeminiClient
from cost_calculator import get_cost_calculator

import AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement, _version: float) -> bool:
    return True


def create_element(build_ele: BuildingElement, doc: AllplanEleAdapter.DocumentAdapter) -> Any:
    element = NodeAIRenderBasic(doc)
    return element.execute(build_ele)


class NodeAIRenderBasic:
    """AI Render Basic Node - Nano Banana integration"""

    def __init__(self, doc: AllplanEleAdapter.DocumentAdapter):
        self.doc = doc
        self.logger = get_logger("NodeAIRenderBasic")
        self.config = get_config()
        self.processor = ImageProcessor()
        self.cost_calc = get_cost_calculator()

    def execute(self, build_ele: BuildingElement) -> tuple:
        self.logger.info("\n" + "="*70)
        self.logger.info("NODE: AI RENDER BASIC (NANO BANANA)")
        self.logger.info("="*70)

        try:
            # Get inputs
            input_image_path = build_ele.InputImagePath.value
            prompt = build_ele.Prompt.value
            style_preset = build_ele.StylePreset.value
            lighting_preset = build_ele.LightingPreset.value
            resolution = build_ele.Resolution.value
            use_pro_model = build_ele.UseProModel.value

            self.logger.info(f"Input image: {input_image_path}")
            self.logger.info(f"Prompt: {prompt}")
            self.logger.info(f"Style: {style_preset}")
            self.logger.info(f"Lighting: {lighting_preset}")
            self.logger.info(f"Resolution: {resolution}")
            self.logger.info(f"Model: {'Nano Banana Pro' if use_pro_model else 'Nano Banana (Flash)'}")

            # Validate inputs
            if not input_image_path or not os.path.exists(input_image_path):
                self.logger.error(f"Input image not found: {input_image_path}")
                return ([], [None, 0.0, 0.0, False])

            if not prompt or prompt.strip() == "":
                self.logger.error("Prompt cannot be empty")
                return ([], [None, 0.0, 0.0, False])

            # Validate configuration
            if not self.config.validate():
                self.logger.error("Configuration invalid - check API keys in .env file")
                return ([], [None, 0.0, 0.0, False])

            # Estimate cost
            model_name = self.config.get_model_name(use_pro_model)
            estimated_cost = self.cost_calc.estimate_render_cost(model_name, resolution)

            self.logger.info(f"\n💰 Estimated cost: ${estimated_cost:.4f} USD")

            # Check budget limit
            if not self.cost_calc.check_budget_limit(self.config.MAX_MONTHLY_COST_USD):
                self.logger.error("Monthly budget limit exceeded!")
                return ([], [None, 0.0, 0.0, False])

            # Load input image
            self.logger.info("\n📥 Loading input image...")
            input_image = self.processor.load_image(input_image_path)
            input_width, input_height = input_image.size
            self.logger.info(f"Input size: {input_width}x{input_height}")

            # Resize if necessary
            target_resolution = self.processor.RESOLUTION_MAP[resolution]
            if input_width > target_resolution[0] or input_height > target_resolution[1]:
                self.logger.info(f"Resizing to fit {resolution}...")
                input_image = self.processor.resize_to_resolution(
                    input_image,
                    resolution,
                    maintain_aspect_ratio=True
                )
                self.logger.info(f"Resized to: {input_image.size}")

            # Initialize Gemini client
            self.logger.info("\n🤖 Initializing Gemini AI...")
            try:
                gemini_client = GeminiClient(api_key=self.config.GEMINI_API_KEY)
                self.logger.info("✓ Gemini client initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize Gemini client: {e}")
                return ([], [None, 0.0, 0.0, False])

            # Generate render
            self.logger.info("\n🎨 Generating AI render...")
            self.logger.info(f"This may take 30-90 seconds for {resolution} resolution...")

            start_time = time.time()

            try:
                rendered_image = gemini_client.generate_architectural_render(
                    input_image=input_image,
                    prompt=prompt,
                    style_preset=style_preset if style_preset != "None" else None,
                    lighting_preset=lighting_preset if lighting_preset != "None" else None,
                    use_pro_model=use_pro_model,
                    resolution=resolution,
                    num_images=1,
                    safety_filter="block_few"
                )

                process_time = time.time() - start_time

                self.logger.info(f"\n✓ Render generated successfully!")
                self.logger.info(f"⏱️  Generation time: {process_time:.1f} seconds")

            except Exception as e:
                self.logger.error(f"\n✗ Render generation failed: {e}")
                import traceback
                self.logger.error(traceback.format_exc())
                return ([], [None, 0.0, 0.0, False])

            # Save rendered image
            self.logger.info("\n💾 Saving rendered image...")
            output_path = self.processor.save_temp_image(
                rendered_image,
                prefix=f"render_{resolution.lower()}"
            )
            self.logger.info(f"Saved to: {output_path}")

            # Record cost
            self.cost_calc.record_cost(f"AI Render ({model_name}, {resolution})", estimated_cost)

            # Final summary
            self.logger.info("\n" + "="*70)
            self.logger.info("✓ AI RENDER COMPLETE")
            self.logger.info("="*70)
            self.logger.info(f"Output: {output_path}")
            self.logger.info(f"Cost: ${estimated_cost:.4f} USD")
            self.logger.info(f"Time: {process_time:.1f}s")
            self.logger.info(f"Resolution: {rendered_image.size}")
            self.logger.info("="*70 + "\n")

            # Return: RenderedImagePath, Cost, ProcessTime, Success
            return ([], [output_path, estimated_cost, process_time, True])

        except Exception as e:
            self.logger.error(f"\n✗ Unexpected error: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return ([], [None, 0.0, 0.0, False])
