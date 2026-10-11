# First, we have to import three classes
# from Pillow.
from PIL import Image, ImageDraw, ImageFont
# Then we have to create some variables.
# These can customized for your specific atlas.
# What is the name of your original atlas?
old = "old.png"
# How long is each tile in pixels?
# This script assumes that all tiles are square.
tile = 32
# If there is a grid of lines separating each
# tile, how thick are the grid lines in pixels? 
grid = 1
# The top left corner pixel of an image
# is represented by the coordinate (0,0).
# If your tiles start immediately at (0,0),
# then no need to change this, but you can
# add an offset here based on when tiles
# actually start appearing in your PNG.
x = 0
y = 0
old = Image.open(old).convert("RGBA")
# Because we're starting with a rectangular
# PNG, we need to collect some width
# and height measurements. Get the width
# of the old atlas and subtract any horizontal
# offset to find the width of the area
# with tiles.
old_width = old.width - x
# then divide the width of the area with tiles
# by the width of each tile and the border size
# This 
# In a fencepost scenario, you would have to
# set x to whatever the size of border is
# on the far left and far right

columns = scratch // (tile + border)
rows = (old.height - y + border) // (tile + border)
original_tiles = columns * rows
total_tiles = original_tiles * 9
print(f"There are {original_tiles} original textures, expanding to {total_tiles} tiles.")
block_side = 1
while block_side * block_side < original_tiles:
    block_side += 1
atlas_size = block_side * 3 * tile
atlas = Image.new("RGBA", (atlas_size, atlas_size), (0, 0, 0, 0))
for original_index in range(original_tiles):
    source_index = original_tiles - 1 - original_index
    source_column = source_index % columns
    source_row = source_index // columns
    source_x = x + source_column * (tile + border)
    source_y = y + source_row * (tile + border)
    tile_image = image.crop(
        (source_x, source_y, source_x + tile, source_y + tile)
    )
    block_column = original_index % block_side
    block_row = original_index // block_side
    for copy_index in range(9):
        copy_column = copy_index % 3
        copy_row = copy_index // 3
        dest_x = (block_column * 3 + copy_column) * tile
        dest_y = (block_row * 3 + copy_row) * tile
        atlas.paste(tile_image, (dest_x, dest_y))
atlas.save("atlas.png")
numbered = atlas.copy()
draw = ImageDraw.Draw(numbered)
font = ImageFont.load_default()
grid_side = block_side * 3
index = 0
for tile_row in range(grid_side):
    for tile_column in range(grid_side):
        block_row = tile_row // 3
        block_column = tile_column // 3
        block_index = block_row * block_side + block_column
        if block_index >= original_tiles:
            continue
        px = tile_column * tile
        py = tile_row * tile
        draw.text((px, py),str(index),font=font,fill=(0, 0, 255))
        index += 1
numbered.save("numbered-atlas.png")
