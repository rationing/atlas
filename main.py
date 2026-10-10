from PIL import Image

old = "old-atlas.png" # old atlas image file
tile = 32 # Pixels. Each tile is a 32px by 32px square
border = 1 # Each tile shares a 1px border with the tiles around it
x = 0 # start at left
y = 0 # start at top
image = Image.open(old)
columns = (image.width - x + border) // (tile + border)
rows = (image.height - y + border) // (tile + border)
tiles = columns * rows
count = 1
while count * count < tiles:
    count += 1

atlas = Image.new("RGBA",
                  (count * tile, count * tile),
                  (0, 0, 0, 0))
for index in range(tiles):
    column = index % columns
    # Floor divide by columns
    # columns = number of tiles that fit in a single row
    row = index // columns
    a = x + column * (tile + border)
    b = y + row * (tile + border)
    paste = image.crop((a, b, a + tile, b + tile))
    a = index % count * tile
    b = index // count * tile
    atlas.paste(paste, (a, b))

atlas.save("atlas.png")
