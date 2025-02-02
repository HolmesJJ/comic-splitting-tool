import os
import cv2
import fitz

from tqdm import tqdm


INPUT_DIR = 'raw'
OUTPUT_DIR = 'output'
MIN_RATIO = 0.1


def pdf_to_images(pdf_path, output_folder, zoom_factor=2.0, image_format='png'):
    os.makedirs(output_folder, exist_ok=True)
    pdf_document = fitz.open(pdf_path)
    for page_number in tqdm(range(len(pdf_document)), desc='Converting PDF to images'):
        page = pdf_document[page_number]
        matrix = fitz.Matrix(zoom_factor, zoom_factor)
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        output_file = os.path.join(output_folder, f'page_{page_number + 1}.{image_format}')
        pixmap.save(output_file)
    pdf_document.close()


def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for root, dirs, files in os.walk(INPUT_DIR):
        files = [file for file in files if file.endswith(('.png', '.jpg'))]
        for file in tqdm(files, desc=f'Processing files in {root}'):
            image_path = os.path.join(root, file)
            image = cv2.imread(image_path)
            if image is None:
                continue
            image_height, image_width = image.shape[:2]
            min_width = image_width * MIN_RATIO
            min_height = image_height * MIN_RATIO
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # 显示灰度图像
            # cv2.imshow('Gray Image', gray)
            # cv2.waitKey(0)
            _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
            # 显示二值化图像
            # cv2.imshow('Binary Image', thresh)
            # cv2.waitKey(0)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours,
                              key=lambda c: cv2.boundingRect(c)[1] * image.shape[1] + cv2.boundingRect(c)[0])
            filtered_contours = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w > min_width and h > min_height:
                    filtered_contours.append(contour)
            output_image = image.copy()
            for contour in filtered_contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 显示处理过的图像
            # cv2.imshow('Image with Bounding Boxes', output_image)
            # cv2.waitKey(0)
            relative_path = os.path.relpath(root, INPUT_DIR)
            image_name = os.path.splitext(file)[0]
            output_sub_folder = os.path.join(OUTPUT_DIR, relative_path, image_name)
            os.makedirs(output_sub_folder, exist_ok=True)
            for i, contour in enumerate(filtered_contours):
                x, y, w, h = cv2.boundingRect(contour)
                cropped = image[y:y + h, x:x + w]
                output_path = os.path.join(output_sub_folder, f'{i + 1}.jpg')
                cv2.imwrite(output_path, cropped)


if __name__ == '__main__':
    for i in range(10, 43):
        pdf_name = f'{i:02}.pdf'
        pdf_to_images(os.path.join(INPUT_DIR, pdf_name), os.path.join(INPUT_DIR, str(i).zfill(2)), zoom_factor=4)
    # run()
