"""
Cost Calculator for API Usage

Tracks and estimates costs for Google API calls.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import json


class CostCalculator:
    """Calculate and track API costs"""

    # Pricing per operation (USD)
    PRICING = {
        # Gemini Image Generation
        "gemini-2.5-flash-image": {
            "1K": 0.039,  # Per 1024x1024 image
            "2K": 0.039,  # Same price up to 2K
            "4K": 0.039,  # Same price
        },
        "gemini-3-pro-image": {
            "1K": 0.134,  # Per 1K-2K image
            "2K": 0.134,
            "4K": 0.240,  # Per 4K image
        },
        # Gemini Segmentation (Vision)
        "gemini-segmentation": 0.012,  # Per image
        # Imagen 3 Inpainting
        "imagen-inpainting": 0.05,  # Approximate per operation
        # Google Maps
        "maps-street-view": 0.0,  # Free (within quota)
        "maps-aerial-view": 0.0,  # Free (within quota)
    }

    def __init__(self, tracking_file: Optional[str] = None):
        """
        Initialize cost calculator

        Args:
            tracking_file: Path to JSON file for cost tracking. If None, doesn't persist.
        """

        self.tracking_file = tracking_file
        self.current_session_cost = 0.0
        self.monthly_cost = 0.0

        if self.tracking_file:
            self._load_tracking()

    def _load_tracking(self):
        """Load cost tracking from file"""

        try:
            tracking_path = Path(self.tracking_file)
            if tracking_path.exists():
                with open(tracking_path, "r") as f:
                    data = json.load(f)

                # Check if we're in the same month
                last_month = data.get("month", "")
                current_month = datetime.now().strftime("%Y-%m")

                if last_month == current_month:
                    self.monthly_cost = data.get("monthly_cost", 0.0)
                else:
                    # New month - reset
                    self.monthly_cost = 0.0

        except Exception as e:
            print(f"Warning: Could not load cost tracking: {e}")

    def _save_tracking(self):
        """Save cost tracking to file"""

        if not self.tracking_file:
            return

        try:
            tracking_path = Path(self.tracking_file)
            tracking_path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "month": datetime.now().strftime("%Y-%m"),
                "monthly_cost": self.monthly_cost,
                "last_updated": datetime.now().isoformat(),
            }

            with open(tracking_path, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Warning: Could not save cost tracking: {e}")

    def estimate_render_cost(self, model_name: str, resolution: str) -> float:
        """
        Estimate cost for a single render

        Args:
            model_name: "gemini-2.5-flash-image" or "gemini-3-pro-image"
            resolution: "1K", "2K", or "4K"

        Returns:
            Estimated cost in USD
        """

        if model_name not in self.PRICING:
            return 0.0

        if resolution not in self.PRICING[model_name]:
            resolution = "2K"  # Default

        return self.PRICING[model_name][resolution]

    def estimate_segmentation_cost(self, num_images: int = 1) -> float:
        """Estimate cost for image segmentation"""
        return self.PRICING["gemini-segmentation"] * num_images

    def estimate_inpainting_cost(self, num_operations: int = 1) -> float:
        """Estimate cost for inpainting operations"""
        return self.PRICING["imagen-inpainting"] * num_operations

    def record_cost(self, operation: str, cost: float):
        """
        Record an actual cost

        Args:
            operation: Description of operation
            cost: Cost in USD
        """

        self.current_session_cost += cost
        self.monthly_cost += cost

        print(f"💰 Cost recorded: ${cost:.4f} for {operation}")
        print(f"   Session total: ${self.current_session_cost:.4f}")
        print(f"   Monthly total: ${self.monthly_cost:.4f}")

        self._save_tracking()

    def get_session_cost(self) -> float:
        """Get total cost for current session"""
        return self.current_session_cost

    def get_monthly_cost(self) -> float:
        """Get total cost for current month"""
        return self.monthly_cost

    def reset_session(self):
        """Reset session cost counter"""
        self.current_session_cost = 0.0

    def generate_cost_report(self) -> Dict[str, any]:
        """
        Generate cost report

        Returns:
            Dict with cost breakdown
        """

        return {
            "session_cost_usd": self.current_session_cost,
            "monthly_cost_usd": self.monthly_cost,
            "month": datetime.now().strftime("%Y-%m"),
            "pricing_info": {
                "nano_banana_flash": {
                    "1K-4K": "$0.039 per image",
                },
                "nano_banana_pro": {
                    "1K-2K": "$0.134 per image",
                    "4K": "$0.240 per image",
                },
            },
        }

    def check_budget_limit(self, max_monthly_budget: float) -> bool:
        """
        Check if monthly budget limit is exceeded

        Args:
            max_monthly_budget: Maximum monthly budget in USD

        Returns:
            True if within budget, False if exceeded
        """

        if self.monthly_cost >= max_monthly_budget:
            print(f"⚠ WARNING: Monthly budget limit reached!")
            print(f"   Current: ${self.monthly_cost:.2f}")
            print(f"   Limit: ${max_monthly_budget:.2f}")
            return False

        return True


# Default tracking file location
DEFAULT_TRACKING_FILE = "C:/Temp/AllplanRenderAI/cost_tracking.json"

def get_cost_calculator() -> CostCalculator:
    """Get global cost calculator instance"""
    return CostCalculator(tracking_file=DEFAULT_TRACKING_FILE)
