
"""
Deck Renderer
=============

Provides functionality to render a deck mosaic image using panel images.
"""

from pathlib import Path
from typing import Dict
from PIL import Image

from geomet.screen.models.deck import DeckSpec
from geomet.screen.models.panel import PanelSpec


class DeckRenderer:
    """Handles rendering of deck mosaics using panel images."""

    @staticmethod
    def create_mosaic(deck: DeckSpec, panels: Dict[str, PanelSpec], output_path: Path) -> Path:
        """Generate a mosaic image for a deck using panel images.

        Args:
            deck (DeckSpec): The deck specification containing layout and dimensions.
            panels (Dict[str, PanelSpec]): Dictionary of panel specifications keyed by panel ID.
            output_path (Path): Path where the mosaic image will be saved.

        Returns:
            Path: Path to the saved mosaic image.

        Raises:
            ValueError: If any panel ID in the deck layout does not exist in panels.
            FileNotFoundError: If any panel image file is missing.
        """
        # Validate panel references and image paths
        for row in deck.layout:
            for panel_id in row:
                if panel_id not in panels:
                    raise ValueError(f"Panel ID '{panel_id}' not found in panels dictionary.")
                if panels[panel_id].image_path is None or not panels[panel_id].image_path.exists():
                    raise FileNotFoundError(f"Image for panel '{panel_id}' not found at {panels[panel_id].image_path}")

        # Calculate mosaic dimensions
        row_heights = [max(panels[panel_id].panel_h_mm for panel_id in row) for row in deck.layout]
        col_widths = [max(panels[row[col_idx]].panel_w_mm for row in deck.layout) for col_idx in range(deck.cols)]

        total_width = sum(col_widths)
        total_height = sum(row_heights)

        # Create blank canvas
        mosaic = Image.new("RGBA", (total_width, total_height), color=(255, 255, 255, 255))

        # Paste panel images
        y_offset = 0
        for row_idx, row in enumerate(deck.layout):
            x_offset = 0
            for col_idx, panel_id in enumerate(row):
                panel_img = Image.open(panels[panel_id].image_path)
                panel_img = panel_img.resize((panels[panel_id].panel_w_mm, panels[panel_id].panel_h_mm))
                mosaic.paste(panel_img, (x_offset, y_offset))
                x_offset += col_widths[col_idx]
            y_offset += row_heights[row_idx]

        # Save mosaic
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mosaic.save(output_path)

