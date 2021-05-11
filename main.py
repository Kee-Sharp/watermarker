from PIL import Image
import os
import pathlib

def main(args):
    #validate input
    if len(args) != 2: raise Exception("Input should be the watermark_image path name")
    watermark_image_name = args[1]
    if watermark_image_name not in os.listdir():
        raise Exception("Watermark image not found in directory")
    original_watermark = Image.open(f"{watermark_image_name}")
    #set visible pixels to be half transparent in watermark image
    watermark_data = original_watermark.getdata()
    WATERMARK_ALPHA = 90
    newdata = [(*item[:3], min(WATERMARK_ALPHA, item[3])) for item in watermark_data]
    original_watermark.putdata(newdata)
    #add watermark to each image in images
    for base_image_name in os.listdir("images"):
        base_image = Image.open(f"images/{base_image_name}")
        width, height = base_image.size
        watermark = original_watermark.copy()
        water_width, water_height = watermark.size
        #if watermark is too large, resize it
        if water_width > width / 2 or water_height > height / 2:
            watermark.thumbnail((int(width / 2), int(height / 2)))
            water_width, water_height = watermark.size
        transparent = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        transparent.paste(base_image, (0, 0))
        total_width = width + water_width/4
        total_height = height + water_height/4
        HORIZONTAL_SPACE_FACTOR = 5/6
        VERTICAL_SPACE_FACTOR = 1/3
        num_iterations = int(total_height/(water_height*VERTICAL_SPACE_FACTOR)) + 1
        positions = [((0 + i*water_width*HORIZONTAL_SPACE_FACTOR) % total_width, (0+i*water_height*VERTICAL_SPACE_FACTOR) % total_height) for i in range(num_iterations)]
        positions = [(int(pos[0] - water_width/2), int(pos[1] - water_height/2)) for pos in positions]
        for pos in positions:
            transparent.paste(watermark, pos, mask=watermark)
        base_image_root, _ = base_image_name.split(".")
        if not pathlib.os.path.exists("output_images"):
            pathlib.Path("output_images").mkdir()
        transparent.save(f"output_images/{base_image_root}_edited.png", format="png")

if __name__ == "__main__":
    import sys
    main(sys.argv)