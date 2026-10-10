from PIL import Image, ImageDraw, ImageFont

old = "old-atlas.png" # old atlas image file
tile = 32 # Pixels. Each tile is a 32px by 32px square
border = 1 # Each tile shares a 1px border with the tiles around it
x = 0 # start at left
y = 0 # start at top
image = Image.open(old)
columns = (image.width - x + border) // (tile + border)
rows = (image.height - y + border) // (tile + border)
tiles = columns * rows
print("There are ", tiles, " textures in this atlas.")
count = 1
while count * count < tiles:
    count += 1

atlas = Image.new("RGBA",
                  (count * tile, count * tile),
                  (0, 0, 0, 0))
for index in range(tiles):
    target = tiles - 1 - index
    column = target % columns
    # Floor divide by columns
    # columns = number of tiles that fit in a single row
    row = target // columns
    # read from the old, rectangular image and paste
    # into the new, square image
    a = x + column * (tile + border)
    b = y + row * (tile + border)
    paste = image.crop((a, b, a + tile, b + tile))
    a = index % count * tile
    b = index // count * tile
    atlas.paste(paste, (a, b))
atlas.save("atlas.png")

# Draw translucent red numbers on a separate overlay.
overlay = Image.new("RGBA", atlas.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
font = ImageFont.load_default()
for index in range(tiles):
    column = index % columns
    row = index // columns
    label = str(index)
    box = draw.textbbox((0, 0), label, font=font)
    width = box[2] - box[0]
    height = box[3] - box[1]
    x = index % count * tile
    y = index // count * tile
    draw.text((x, y), label, font=font, fill=(255, 0, 0, 150))
Image.alpha_composite(atlas, overlay).save("numbered-atlas.png")
