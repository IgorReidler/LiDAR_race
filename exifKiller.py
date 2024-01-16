import os
from PIL import Image

# Set the path to the folder containing the PNG images
folder_path = 'D:\Python\LiDAR_race\media_noExif'

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        # Open the image file
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)

        # Remove EXIF data
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)

        # Save the image file without EXIF data
        image_without_exif.save(image_path)