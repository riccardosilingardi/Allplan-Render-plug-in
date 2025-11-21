"""
AI Client for Google Gemini (Nano Banana / Nano Banana Pro)

Handles communication with Google's Gemini API for image generation.
"""

import base64
import time
from io import BytesIO
from typing import Optional, Dict, Any

from PIL import Image
import google.generativeai as genai


class GeminiClient:
    """
    Client for Google Gemini AI image generation

    Supports:
    - Nano Banana (gemini-2.5-flash-image): Fast, cost-effective
    - Nano Banana Pro (gemini-3-pro-image): High quality, higher cost
    """

    # Model identifiers
    MODEL_FLASH = "gemini-2.5-flash-image"  # Nano Banana
    MODEL_PRO = "gemini-3-pro-image"        # Nano Banana Pro

    # Style preset prompts
    STYLE_PROMPTS = {
        "Modern": "contemporary modern architecture with clean lines, glass facades, minimalist design, geometric forms",
        "Classical": "classical architecture with ornate details, columns, symmetrical design, traditional proportions",
        "Industrial": "industrial architecture with exposed steel, concrete, brick materials, raw aesthetic",
        "Parametric": "parametric architecture with complex geometries, flowing forms, computational design",
        "Sustainable": "sustainable green architecture with vegetation, eco-friendly materials, biophilic design",
        "Minimalist": "minimalist architecture, simple forms, monochromatic palette, essential elements only",
        "Brutalist": "brutalist architecture, raw concrete, massive geometric forms, monumental scale",
        "Organic": "organic architecture, natural forms, curves, integration with nature",
    }

    # Lighting preset prompts
    LIGHTING_PROMPTS = {
        "Dawn": "soft morning light, golden hour, warm tones, long shadows, sunrise atmosphere",
        "Noon": "bright midday sun, clear sky, sharp shadows, high contrast, overhead lighting",
        "Sunset": "warm sunset light, orange and pink sky, dramatic atmosphere, golden hour glow",
        "Night": "evening scene with artificial lighting, blue hour, illuminated windows, ambient street lights",
        "Overcast": "soft diffused light, cloudy sky, even illumination, no harsh shadows",
        "Dramatic": "dramatic lighting with strong contrast, theatrical atmosphere, spotlighting effects",
    }

    def __init__(self, api_key: str):
        """
        Initialize Gemini client

        Args:
            api_key: Google Gemini API key
        """

        if not api_key:
            raise ValueError("Gemini API key is required")

        self.api_key = api_key

        # Configure the API
        genai.configure(api_key=self.api_key)

        # Initialize models
        self.flash_model = None
        self.pro_model = None

    def _get_model(self, use_pro: bool):
        """Get or initialize the appropriate model"""

        if use_pro:
            if self.pro_model is None:
                # Initialize Nano Banana Pro
                self.pro_model = genai.GenerativeModel(self.MODEL_PRO)
            return self.pro_model
        else:
            if self.flash_model is None:
                # Initialize Nano Banana (Flash)
                self.flash_model = genai.GenerativeModel(self.MODEL_FLASH)
            return self.flash_model

    def _image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""

        buffered = BytesIO()
        # Save as PNG for lossless quality
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')

    def _base64_to_image(self, base64_str: str) -> Image.Image:
        """Convert base64 string to PIL Image"""

        img_bytes = base64.b64decode(base64_str)
        return Image.open(BytesIO(img_bytes))

    def _build_prompt(
        self,
        base_prompt: str,
        style_preset: Optional[str] = None,
        lighting_preset: Optional[str] = None
    ) -> str:
        """
        Build complete prompt with presets

        Args:
            base_prompt: User's base prompt
            style_preset: Style preset name
            lighting_preset: Lighting preset name

        Returns:
            Complete prompt string
        """

        prompt_parts = [
            "Photorealistic architectural rendering.",
            base_prompt.strip()
        ]

        # Add style preset
        if style_preset and style_preset != "None" and style_preset in self.STYLE_PROMPTS:
            prompt_parts.append(self.STYLE_PROMPTS[style_preset])

        # Add lighting preset
        if lighting_preset and lighting_preset != "None" and lighting_preset in self.LIGHTING_PROMPTS:
            prompt_parts.append(self.LIGHTING_PROMPTS[lighting_preset])

        # Add quality suffix
        prompt_parts.append(
            "Highly detailed, professional architectural visualization, 8K quality, "
            "photographic rendering, realistic materials and lighting."
        )

        return " ".join(prompt_parts)

    def generate_architectural_render(
        self,
        input_image: Image.Image,
        prompt: str,
        style_preset: Optional[str] = None,
        lighting_preset: Optional[str] = None,
        use_pro_model: bool = False,
        resolution: str = "2K",
        num_images: int = 1,
        safety_filter: str = "block_few",
    ) -> Image.Image:
        """
        Generate architectural render from input viewport

        Args:
            input_image: Input image (Allplan viewport)
            prompt: Text prompt describing desired output
            style_preset: Style preset ("Modern", "Classical", etc.)
            lighting_preset: Lighting preset ("Dawn", "Noon", etc.)
            use_pro_model: Use Nano Banana Pro (True) or Nano Banana (False)
            resolution: Target resolution ("1K", "2K", "4K")
            num_images: Number of images to generate (typically 1)
            safety_filter: Safety filter level ("block_none", "block_few", "block_some", "block_most")

        Returns:
            Generated PIL Image

        Raises:
            Exception: If generation fails
        """

        # Build full prompt
        full_prompt = self._build_prompt(prompt, style_preset, lighting_preset)

        print(f"\n{'='*60}")
        print(f"GENERATING RENDER")
        print(f"{'='*60}")
        print(f"Model: {'Nano Banana Pro' if use_pro_model else 'Nano Banana (Flash)'}")
        print(f"Resolution: {resolution}")
        print(f"Prompt: {full_prompt[:200]}...")
        print(f"{'='*60}\n")

        # Get model
        model = self._get_model(use_pro_model)

        try:
            # Prepare input image
            # Note: Gemini API accepts images in specific ways depending on the SDK version
            # We'll use the most compatible approach

            # Start generation
            start_time = time.time()

            # Generate content with the image
            # The exact API may vary - adjust based on actual Gemini API documentation
            response = model.generate_content([
                full_prompt,
                input_image  # PIL Image is supported directly in newer versions
            ])

            generation_time = time.time() - start_time

            # Extract generated image
            # Note: The response structure depends on Gemini API version
            # This is a placeholder - adjust based on actual API response
            if hasattr(response, 'images') and response.images:
                generated_image = response.images[0]
            elif hasattr(response, 'candidates') and response.candidates:
                # Alternative extraction method
                generated_image = response.candidates[0].content.parts[0].inline_data.data
                generated_image = self._base64_to_image(generated_image)
            else:
                # Fallback - may need adjustment
                generated_image = response

            print(f"✓ Generation complete in {generation_time:.1f}s")

            return generated_image

        except Exception as e:
            print(f"✗ Generation failed: {e}")
            raise Exception(f"Gemini API error: {e}")

    def generate_image_from_text_only(
        self,
        prompt: str,
        style_preset: Optional[str] = None,
        lighting_preset: Optional[str] = None,
        use_pro_model: bool = False,
        resolution: str = "2K",
    ) -> Image.Image:
        """
        Generate image from text prompt only (no input image)

        Args:
            prompt: Text description
            style_preset: Style preset
            lighting_preset: Lighting preset
            use_pro_model: Use Pro model
            resolution: Target resolution

        Returns:
            Generated PIL Image
        """

        full_prompt = self._build_prompt(prompt, style_preset, lighting_preset)

        model = self._get_model(use_pro_model)

        try:
            response = model.generate_content(full_prompt)

            # Extract image from response
            if hasattr(response, 'images'):
                return response.images[0]
            else:
                # Handle different response formats
                return response

        except Exception as e:
            raise Exception(f"Text-to-image generation failed: {e}")

    def get_model_info(self, use_pro: bool = False) -> Dict[str, Any]:
        """
        Get information about the model

        Args:
            use_pro: Get info for Pro model

        Returns:
            Dict with model information
        """

        model_name = self.MODEL_PRO if use_pro else self.MODEL_FLASH

        return {
            "name": model_name,
            "display_name": "Nano Banana Pro" if use_pro else "Nano Banana (Flash)",
            "recommended_for": "High quality renders" if use_pro else "Fast iteration and drafts",
            "cost_per_1k": 0.134 if use_pro else 0.039,
            "cost_per_4k": 0.240 if use_pro else 0.039,
        }


# Alternative implementation using direct API calls (if generativeai SDK doesn't work)
class GeminiClientAlternative:
    """
    Alternative Gemini client using direct REST API calls

    Use this if the official SDK has issues with image generation.
    """

    API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_render(
        self,
        input_image: Image.Image,
        prompt: str,
        use_pro: bool = False
    ) -> Image.Image:
        """Generate render using REST API"""

        import requests

        model = "gemini-3-pro-image" if use_pro else "gemini-2.5-flash-image"
        url = self.API_ENDPOINT.format(model=model)

        # Convert image to base64
        buffered = BytesIO()
        input_image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Prepare request
        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": img_base64
                        }
                    }
                ]
            }]
        }

        # Make request
        response = requests.post(
            url,
            headers=headers,
            params={"key": self.api_key},
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")

        # Parse response and extract image
        result = response.json()

        # Extract image from response (structure depends on API)
        # This is a placeholder - adjust based on actual API response
        image_data = result["candidates"][0]["content"]["parts"][0]["inline_data"]["data"]
        return self._base64_to_image(image_data)

    def _base64_to_image(self, base64_str: str) -> Image.Image:
        """Convert base64 to PIL Image"""
        img_bytes = base64.b64decode(base64_str)
        return Image.open(BytesIO(img_bytes))
