import os

from PIL import Image


def check_image_dpi(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with Image.open(file_path) as img:
                dpi = img.info.get('dpi')
                if dpi and (dpi[0] != 96 or dpi[1] != 96):
                    print(f'Image with non-96x96 DPI: {file_path}')


if __name__ == '__main__':
    check_image_dpi('output/01')
