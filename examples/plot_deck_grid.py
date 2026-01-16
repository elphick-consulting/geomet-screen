"""
Screen Deck Grid Visualization
================================

This example demonstrates how to load a screen deck layout from an Excel workbook
and visualize it using Plotly.
"""

# %%
# Load and Visualize Screen Deck
# -------------------------------
# We'll load a deck from an Excel workbook, store it in the database,
# and create a plotly visualization.

import numpy as np
import pandas as pd
from pathlib import Path

from geomet_screen.database import DatabaseConnection, ExcelLoader
from geomet_screen.visualization import plot_deck_grid

# %%
# First, create a sample Excel workbook with deck data

# Create sample data for demonstration (5x5 grid)
deck_data = np.array([
    [10.5, 12.3, 11.8, 13.2, 10.9],
    [9.8, 11.5, 10.2, 12.7, 11.3],
    [11.2, 10.8, 12.5, 11.9, 10.5],
    [12.1, 11.7, 10.3, 11.4, 12.8],
    [10.7, 12.9, 11.1, 10.6, 11.8],
])
df = pd.DataFrame(deck_data)

# Create a temporary Excel file
example_dir = Path(__file__).parent
workbook_path = example_dir / "example_screen.xlsx"
with pd.ExcelWriter(workbook_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Deck1', header=False, index=False)

print(f"Created example workbook: {workbook_path}")

# %%
# Set up the database and load the deck

# Initialize database (in-memory for this example)
db = DatabaseConnection()
db.create_tables()

# Load the deck from Excel
loader = ExcelLoader(db.get_session())
deck = loader.load_deck_from_excel(
    workbook_path=str(workbook_path),
    sheet_name='Deck1',
    screen_name='Screen_A',
    deck_name='Deck_1',
)

print(f"Loaded deck: {deck}")
print(f"Number of grid cells: {len(deck.grid_cells)}")

# %%
# Extract and visualize the deck data

# Get the deck data as a DataFrame
grid_df = loader.get_deck_data(deck.id)

print("Grid data shape:", grid_df.shape)
print("\nGrid data:\n", grid_df)

# %%
# Create the plotly visualization

fig = plot_deck_grid(
    grid_df,
    title="Screen Deck A - Deck 1 Layout",
    colorscale="Viridis",
    width=700,
    height=600,
)

# Display the figure
fig.show()

# %%
# Clean up

db.close()
if workbook_path.exists():
    workbook_path.unlink()
