import cv2
import mediapipe as mp
from face2_zmieniony import (
    zamien_na_liste_wartosci,
    przemieszaj_wartosci,
    przelicz_na_binarny,
    zlacz_binarnie,
    generuj_timestamp,
    przetworz_binarna_liczbe,
    binarna_na_ascii,
)


from image_mods import change_brightness, blur_image, add_noise, rotate_image

# Przykład: losowa modyfikacja jednego zdjęcia przed testem
import random

def random_mod(input_path):
    output_path = "temp_mod.jpg"  # plik tymczasowy
    mod = random.choice(['brightness', 'blur', 'noise', 'rotate', 'none'])
    if mod == 'brightness':
        return change_brightness(input_path, output_path, factor=random.uniform(0.7,1.5))
    elif mod == 'blur':
        return blur_image(input_path, output_path, radius=random.randint(1,5))
    elif mod == 'noise':
        return add_noise(input_path, output_path, noise_level=random.randint(10,40))
    elif mod == 'rotate':
        return rotate_image(input_path, output_path, angle=random.randint(-20, 20))
    else:
        return input_path  # bez zmian




mp_face_mesh = mp.solutions.face_mesh

def extract_face_points_mediapipe(image_path, num_points=3):
    """Wyciąga trzy punkty charakterystyczne twarzy z obrazu."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image {image_path}")

    # Konwersja do RGB (MediaPipe działa w RGB)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            raise ValueError(f"No face detected in {image_path}")

        face_landmarks = results.multi_face_landmarks[0]

        # Przykładowe landmarki:
        NOSE_TIP = 1
        LEFT_EYE_OUTER = 33
        MOUTH_CORNER_LEFT = 61

        selected_indices = [NOSE_TIP, LEFT_EYE_OUTER, MOUTH_CORNER_LEFT]
        h, w, _ = image.shape
        points = []

        for idx in selected_indices[:num_points]:
            lm = face_landmarks.landmark[idx]
            x, y = int(lm.x * w), int(lm.y * h)
            points.append((x, y))

        return points

def generate_key_from_two_faces(img1, img2, rounds=10):
    """Tworzy klucz na podstawie 2 obrazów twarzy (po 3 punkty każdy)."""
    #img1_mod = random_mod(img1)
    #points1 = extract_face_points_mediapipe(img1_mod)
    points1 = extract_face_points_mediapipe(img1)
    points2 = extract_face_points_mediapipe(img2)
    wspolrzedne = points1 + points2

    # Przetwarzanie tak jak w Twoim kodzie
    lista_wartosci = zamien_na_liste_wartosci(wspolrzedne)
    przemieszane_wartosci = przemieszaj_wartosci(lista_wartosci)
    binarne_wartosci = przelicz_na_binarny(przemieszane_wartosci)
    zlaczone_binarnie = zlacz_binarnie(binarne_wartosci)

    # Timestampy
    timestamp1 = generuj_timestamp()
    timestamp2 = generuj_timestamp()
    timestamp_bin = bin(timestamp1)[2:].zfill(64) + bin(timestamp2)[2:].zfill(64)

    duza_liczba_binarna = zlaczone_binarnie + timestamp_bin

    for _ in range(rounds):
        duza_liczba_binarna = przetworz_binarna_liczbe(duza_liczba_binarna)

    klucz_ascii = binarna_na_ascii(duza_liczba_binarna)
    return klucz_ascii, wspolrzedne

#if __name__ == "__main__":
   # key, coords = generate_key_from_two_faces("images/face1.jpg", "images/face2.jpg")
   # print("Generated key:", key)
   # print("Coordinates:", coords)
