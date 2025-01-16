import os

from PIL import Image


def check_image_resolution(folder_path, max_width, max_height):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    if width < max_width and height < max_height:
                        print(f'Image below resolution {max_width}x{max_height}: {file_path} ({width}x{height})')
            except Exception as e:
                print(f'Error processing file {file_path}: {e}')


if __name__ == '__main__':
    check_image_resolution('output/01', 1000, 1000)
