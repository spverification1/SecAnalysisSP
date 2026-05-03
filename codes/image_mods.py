from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import os

def change_brightness(input_path, output_path, factor=1.5):
    """Zwiększa lub zmniejsza jasność obrazu."""
    img = Image.open(input_path)
    enhancer = ImageEnhance.Brightness(img)
    img_enhanced = enhancer.enhance(factor)  # >1 rozjaśnia, <1 przyciemnia
    img_enhanced.save(output_path)
    return output_path

def blur_image(input_path, output_path, radius=2):
    """Rozmywa obraz (GaussianBlur, Pillow)."""
    img = Image.open(input_path)
    img_blurred = img.filter(ImageFilter.GaussianBlur(radius))
    img_blurred.save(output_path)
    return output_path

def add_noise(input_path, output_path, noise_level=25):
    """Dodaje biały szum do obrazu (cv2 + numpy)."""
    img = cv2.imread(input_path)
    noise = np.random.normal(0, noise_level, img.shape).astype(np.uint8)
    noisy_img = cv2.add(img, noise)
    cv2.imwrite(output_path, noisy_img)
    return output_path

def rotate_image(input_path, output_path, angle=15):
    """Rotuje obraz o wybrany kąt (cv2)."""
    img = cv2.imread(input_path)
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    cv2.imwrite(output_path, rotated)
    return output_path

# Przykład użycia dla pojedynczego pliku
if __name__ == "__main__":
    in_file = "images/test.jpg"  # ścieżka wejściowa do zdjęcia
    
    change_brightness(in_file, "mod_bright.jpg", factor=1.3)
    blur_image(in_file, "mod_blur.jpg", radius=2)
    add_noise(in_file, "mod_noise.jpg", noise_level=30)
    rotate_image(in_file, "mod_rotate.jpg", angle=25)

    print("Obrazy po modyfikacji zostały zapisane.")
