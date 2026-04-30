import threading
import time
import random
import csv
import glob

# Tutaj importuj swoją funkcję!
from extract_key_from_faces2 import generate_key_from_two_faces
 
device_times = []  # nowa lista na czasy urządzeń

def simulate_device(device_id, img_pairs, results, device_times):
    """
    Każde urządzenie w jednym wątku obsługuje listę par zdjęć.
    """
    device_start = time.time()
    for img1_path, img2_path in img_pairs:
        key = generate_key_from_two_faces(img1_path, img2_path)
        results.append({
            'device': device_id,
            'img1': img1_path,
            'img2': img2_path,
            'key': key,
            'timestamp': time.time()
        })
    device_end = time.time()
    elapsed = device_end - device_start
    print(f"Device {device_id} finished in {elapsed:.2f}s") 
    device_times.append({'device': device_id, 'seconds': elapsed})

def generate_image_pairs(images, pairs_per_device):
    """
    Tworzy listę N unikalnych (ale losowych) par zdjęć dla jednego urządzenia.
    """
    pairs = []
    num_images = len(images)
    for _ in range(pairs_per_device):
        img1, img2 = random.sample(images, 2)
        pairs.append((img1, img2))
    return pairs

def main():
    # Pobierz wszystkie zdjęcia z katalogu
    images = glob.glob('images/*.jpg')
    total_images = len(images)
    num_devices = 100
    pairs_per_device = 20  # Liczba sesji (par) na urządzenie

    # Dla każdego urządzenia generujemy losowe pary zdjęć
    devices_img_pairs = [
        generate_image_pairs(images, pairs_per_device)
        for _ in range(num_devices)
    ]

    results = []
    device_times = []

    threads = []
    start = time.time()
    for idx, img_pairs in enumerate(devices_img_pairs):
        t = threading.Thread(target=simulate_device, args=(idx, img_pairs, results, device_times))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    end = time.time()

    print(f"\nTotal runtime for all devices: {end-start:.2f} seconds")
    print(f"Total generated keys: {len(results)}")

    # Zapisz wyniki do CSV
    with open("experiment_results_100_20.csv", "w", newline="") as csvfile:
        fieldnames = ["device", "img1", "img2", "key", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    print("Results saved to experiment_results_100_20.csv")

    with open("device_times_100_20.csv", "w", newline="") as csvfile:
        fieldnames = ["device", "seconds"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in device_times:
            writer.writerow(r)
    print("Device times saved to device_times_100_20.csv")

if __name__ == "__main__":
    main()
    # Po zakończeniu eksperymentu generujemy wykresy i tabele:
    import pandas as pd
    import matplotlib.pyplot as plt

    # Wczytanie wyników z pliku device_times.csv
    df = pd.read_csv('device_times_100_20.csv')

    # Wykres słupkowy: Czas działania poszczególnych urządzeń
    plt.bar(df['device'], df['seconds'])
    plt.xlabel('Device number')
    plt.ylabel('Operation time [s]')
    plt.title('Session service time per device')
    plt.tight_layout()
    plt.savefig('device_time_chart_100_20.png')
    #plt.show()

    # Podstawowe statystyki - wydruk w konsoli (można zapisać do pliku, jeśli chcesz)
    print("Device uptime statistics:")
    print(df['seconds'].describe())
    stats = df['seconds'].describe()
    stats.to_csv("device_time_stats_100_20.csv")
    print("Statystyki zapisane do device_time_stats.csv")

    # Wczytanie wyników sesji z pliku experiment_results.csv
    df2 = pd.read_csv('experiment_results_100_20.csv')

    # Histogram różnic czasowych między sesjami (optional, jeśli masz timestamp)
    all_times = df2['timestamp'].diff().fillna(0)
    plt.hist(all_times, bins=30)
    plt.xlabel('Time difference between subsequent sessions [s]')
    plt.title('Session generation time schedule')
    plt.tight_layout()
    plt.savefig('session_time_hist_100_20.png')
    #plt.show()