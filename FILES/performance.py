"""
performance.py

Runs the performance experiment described in the project report:
compresses the small/medium/large datasets (and a few extra sample
files) with Huffman coding, runs the fixed-length baseline on the
same data, and records ACTUAL measured results.

Nothing here is hard-coded. Every number comes from a real run of
the algorithm on this machine, at the time the script is executed.

Outputs:
    results/performance_results.csv
    results/compression_time.png
    results/compression_size.png
    results/algorithm_comparison.png

Run with:
    python performance.py
"""

import csv
import os

from huffman import compress_file, decompress_file, verify_lossless
from baseline import run_fixed_length_baseline

TEST_DIR = "test_data"
TMP_DIR = "tmp_perf_output"
RESULTS_DIR = "results"

DATASETS = ["small.txt", "medium.txt", "large.txt", "repetitive.txt", "normal_text.txt"]


def run_experiment():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    rows = []

    for filename in DATASETS:
        input_path = os.path.join(TEST_DIR, filename)
        if not os.path.exists(input_path):
            print(f"Skipping {filename} (not found). Run generate_test_data.py first.")
            continue

        compressed_path = os.path.join(TMP_DIR, filename + ".huff")
        decompressed_path = os.path.join(TMP_DIR, filename + ".out")

        print(f"Running Huffman compression on {filename} ...")
        huff_stats = compress_file(input_path, compressed_path)
        decompress_file(compressed_path, decompressed_path)
        verified = verify_lossless(input_path, decompressed_path)

        with open(input_path, "rb") as f:
            data = f.read()
        baseline_stats = run_fixed_length_baseline(data)

        row = {
            "dataset": filename,
            "original_size_bytes": huff_stats["original_size"],
            "unique_symbols": huff_stats["unique_symbols"],
            "huffman_compressed_bytes": huff_stats["compressed_size"],
            "huffman_compression_ratio": round(huff_stats["compression_ratio"], 4),
            "huffman_space_saving_percent": round(huff_stats["space_saving_percent"], 2),
            "huffman_total_time_sec": round(huff_stats["total_time"], 6),
            "fixed_length_bytes": baseline_stats["fixed_length_size"],
            "fixed_length_bits_per_symbol": baseline_stats["bits_per_symbol"],
            "verification": "PASS" if verified else "FAIL",
        }
        rows.append(row)
        print(f"  -> original={row['original_size_bytes']}B, "
              f"huffman={row['huffman_compressed_bytes']}B, "
              f"fixed-length={row['fixed_length_bytes']}B, "
              f"verification={row['verification']}")

    write_csv(rows)
    try:
        generate_charts(rows)
    except Exception as e:
        print(f"Chart generation skipped ({e}). CSV results are still available.")

    return rows


def write_csv(rows):
    csv_path = os.path.join(RESULTS_DIR, "performance_results.csv")
    if not rows:
        print("No results to write.")
        return
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nResults written to {csv_path}")


def generate_charts(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = [r["dataset"] for r in rows]

    # Chart 1: Input size vs compression time
    sizes = [r["original_size_bytes"] for r in rows]
    times = [r["huffman_total_time_sec"] for r in rows]
    plt.figure(figsize=(7, 4.5))
    plt.plot(sizes, times, marker="o")
    for x, y, label in zip(sizes, times, labels):
        plt.annotate(label, (x, y), fontsize=7, textcoords="offset points", xytext=(4, 4))
    plt.xlabel("Original file size (bytes)")
    plt.ylabel("Total compression time (seconds)")
    plt.title("Input Size vs Compression Time (Huffman)")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "compression_time.png"), dpi=120)
    plt.close()

    # Chart 2: Original size vs compressed size
    compressed = [r["huffman_compressed_bytes"] for r in rows]
    x = range(len(labels))
    plt.figure(figsize=(7, 4.5))
    width = 0.35
    plt.bar([i - width / 2 for i in x], sizes, width=width, label="Original size")
    plt.bar([i + width / 2 for i in x], compressed, width=width, label="Huffman compressed size")
    plt.xticks(list(x), labels, rotation=20, ha="right", fontsize=8)
    plt.ylabel("Size (bytes)")
    plt.title("Original Size vs Compressed Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "compression_size.png"), dpi=120)
    plt.close()

    # Chart 3: Huffman vs Fixed-Length encoded size
    fixed = [r["fixed_length_bytes"] for r in rows]
    plt.figure(figsize=(7, 4.5))
    plt.bar([i - width / 2 for i in x], compressed, width=width, label="Huffman size")
    plt.bar([i + width / 2 for i in x], fixed, width=width, label="Fixed-length size")
    plt.xticks(list(x), labels, rotation=20, ha="right", fontsize=8)
    plt.ylabel("Size (bytes)")
    plt.title("Huffman vs Fixed-Length Encoded Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "algorithm_comparison.png"), dpi=120)
    plt.close()

    print(f"Charts saved in {RESULTS_DIR}/ "
          f"(compression_time.png, compression_size.png, algorithm_comparison.png)")


if __name__ == "__main__":
    run_experiment()
