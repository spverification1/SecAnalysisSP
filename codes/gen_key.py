
import hashlib
import time
import random
import math
import csv
import os

os.makedirs("x", exist_ok=True)
output_file = "testy_rundy_klucze.csv"

def generate_random_coordinates():
    return [(random.randint(0, 300), random.randint(0, 300)) for _ in range(6)]

def coords_to_binary(coords):
    values = [coord for point in coords for coord in point]
    binary = ''.join(bin(v)[2:].zfill(16) for v in values)
    return binary

def process_key_rounds(binary_data, rounds):
    start = time.time()
    data = binary_data
    for _ in range(rounds):
        blocks = [data[i:i+4] for i in range(0, len(data), 4)]
        half = len(blocks) // 2
        mixed = [val for pair in zip(blocks[:half], blocks[half:][::-1]) for val in pair]
        for i in range(1, len(mixed) - 2, 4):
            mixed[i], mixed[i + 2] = mixed[i + 2], mixed[i]
        mixed = [mixed[-1]] + mixed[:-1]
        data = ''.join(mixed)
    end = time.time()
    return data, end - start

def diffusion_test(binary_data, rounds):
    flipped = list(binary_data)
    i = random.randint(0, len(flipped) - 1)
    flipped[i] = '1' if flipped[i] == '0' else '0'
    flipped = ''.join(flipped)
    original, _ = process_key_rounds(binary_data, rounds)
    modified, _ = process_key_rounds(flipped, rounds)
    diff_bits = sum(1 for a, b in zip(original, modified) if a != b)
    return diff_bits / len(original)

def entropy(binary_data):
    probs = [binary_data.count(bit) / len(binary_data) for bit in '01']
    return -sum(p * math.log2(p) for p in probs if p > 0)

def collision_resistance(keys):
    return 1 - (len(set(keys)) / len(keys))

def main():
    rounds_set = [1, 3, 5, 10, 15]
    results = []

    for rounds in rounds_set:
        keys = []
        for i in range(10):
            coords = generate_random_coordinates()
            binary_input = coords_to_binary(coords)
            key, proc_time = process_key_rounds(binary_input, rounds)
            keys.append(key)
            diff_score = diffusion_test(binary_input, rounds)
            ent = entropy(key)
            results.append({
                "coords": coords,
                "key": key,
                "rounds": rounds,
                "processing_time": proc_time,
                "diffusion": round(diff_score, 4),
                "entropy": round(ent, 4),
                "collision_rate": None
            })
        collision_score = round(collision_resistance(keys), 4)
        for r in results:
            if r["rounds"] == rounds:
                r["collision_rate"] = collision_score

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["coords", "key", "rounds", "processing_time", "diffusion", "entropy", "collision_rate"])
        for r in results:
            writer.writerow([
                r["coords"],
                r["key"],
                r["rounds"],
                r["processing_time"],
                r["diffusion"],
                r["entropy"],
                r["collision_rate"]
            ])



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_analysis(csv_path="testy_rundy_klucze.csv"):
    df = pd.read_csv(csv_path)

    df["rounds"] = pd.to_numeric(df["rounds"], errors='coerce')
    df["processing_time"] = pd.to_numeric(df["processing_time"], errors='coerce')
    df["diffusion"] = pd.to_numeric(df["diffusion"], errors='coerce')
    df["entropy"] = pd.to_numeric(df["entropy"], errors='coerce')
    df["collision_rate"] = pd.to_numeric(df["collision_rate"], errors='coerce')
    df["key_length"] = df["key"].apply(len)

    # Key length histogram
    plt.figure(figsize=(12, 8))#, constrained_layout=True)
    plt.tight_layout()
    sns.histplot(df["key_length"], bins=10, kde=True, color='skyblue')
    plt.title("Histogram of Binary Key Lengths")
    plt.xlabel("Key Length (bits)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.savefig("histogram_key_length.png")
    plt.close()

    # Entropy histogram
    plt.figure(figsize=(10, 6), constrained_layout=True)
    sns.histplot(df["entropy"], bins=10, kde=True, color='salmon')
    plt.title("Histogram of Key Entropy")
    plt.xlabel("Entropy")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.savefig("histogram_entropy.png")
    plt.close()

    # Rounds vs Entropy
    plt.figure(figsize=(10, 6), constrained_layout=True)
    sns.lineplot(data=df, x="rounds", y="entropy", marker='o', errorbar=None)
    plt.title("Impact of Number of Rounds on Key Entropy")
    plt.xlabel("Number of Rounds")
    plt.ylabel("Entropy")
    plt.grid(True)
    plt.savefig("rounds_vs_entropy.png")
    plt.close()

    # Rounds vs Processing Time
    plt.figure(figsize=(10, 6), constrained_layout=True)
    sns.lineplot(data=df, x="rounds", y="processing_time", marker='s', color='orange', errorbar=None)
    plt.title("Impact of Number of Rounds on Processing Time")
    plt.xlabel("Number of Rounds")
    plt.ylabel("Processing Time [s]")
    plt.grid(True)
    plt.savefig("rounds_vs_time.png")
    plt.close()

    # Collision heatmap
    pivot = df.pivot_table(index='key', columns='rounds', aggfunc='size', fill_value=0)
    collision_matrix = (pivot > 1).astype(int)
    plt.figure(figsize=(16, 8))#, constrained_layout=True)
    plt.tight_layout()
    sns.heatmap(collision_matrix, cmap="Greens", cbar=False, linewidths=0.5, linecolor='lightgray')
    plt.title("Collision Heatmap (0 = Unique, 1 = Collision)")
    plt.xlabel("Number of Rounds")
    plt.ylabel("Generated Keys")
    plt.savefig("collision_heatmap.png")
    plt.close()


if __name__ == '__main__':
    main()
    visualize_analysis()