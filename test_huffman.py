"""
test_huffman.py

Simple test suite (no pytest dependency needed - plain assertions)
that checks correctness of the Huffman implementation and the
fixed-length baseline across the required test cases:

  1. Normal text file
  2. Highly repetitive file
  3. Different-size files
  4. Single-symbol file
  5. Empty file (must raise a clear error, not crash silently)
  6. Decompression correctness (round-trip)
  7. Invalid compressed file (must raise a clear error)
  8. File with spaces, numbers, punctuation

Run with:
    python test_huffman.py
"""

import os
import sys

from huffman import compress_file, decompress_file, verify_lossless
from baseline import run_fixed_length_baseline

TEST_DIR = "test_data"
TMP_DIR = "tmp_test_output"
os.makedirs(TMP_DIR, exist_ok=True)

PASS = 0
FAIL = 0


def check(condition, message):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {message}")
    else:
        FAIL += 1
        print(f"  [FAIL] {message}")


def round_trip(filename):
    """Compress then decompress a file, return (stats, verified)."""
    original_path = os.path.join(TEST_DIR, filename)
    compressed_path = os.path.join(TMP_DIR, filename + ".huff")
    decompressed_path = os.path.join(TMP_DIR, filename + ".out")

    stats = compress_file(original_path, compressed_path)
    decompress_file(compressed_path, decompressed_path)
    verified = verify_lossless(original_path, decompressed_path)
    return stats, verified


def test_normal_text():
    print("\nTest 1: Normal text file")
    stats, verified = round_trip("normal_text.txt")
    check(verified, "normal_text.txt round-trips losslessly")
    check(stats["compressed_size"] < stats["original_size"],
          "normal_text.txt compresses smaller than original")


def test_repetitive():
    print("\nTest 2: Highly repetitive file")
    stats, verified = round_trip("repetitive.txt")
    check(verified, "repetitive.txt round-trips losslessly")
    check(stats["compression_ratio"] < 0.5,
          "repetitive.txt achieves strong compression (ratio < 0.5)")


def test_different_sizes():
    print("\nTest 3: Different-size files (small/medium/large)")
    for name in ("small.txt", "medium.txt", "large.txt"):
        stats, verified = round_trip(name)
        check(verified, f"{name} round-trips losslessly")


def test_single_symbol():
    print("\nTest 4: Single-symbol file")
    stats, verified = round_trip("single_symbol.txt")
    check(verified, "single_symbol.txt round-trips losslessly")
    check(stats["unique_symbols"] == 1, "single_symbol.txt has exactly 1 unique symbol")


def test_empty_file():
    print("\nTest 5: Empty file must raise a clear error")
    original_path = os.path.join(TEST_DIR, "empty.txt")
    compressed_path = os.path.join(TMP_DIR, "empty.txt.huff")
    try:
        compress_file(original_path, compressed_path)
        check(False, "empty.txt should have raised ValueError")
    except ValueError as e:
        check(True, f"empty.txt correctly raised ValueError: {e}")


def test_invalid_compressed_file():
    print("\nTest 6: Invalid compressed file must raise a clear error")
    bad_path = os.path.join(TMP_DIR, "not_really_compressed.huff")
    with open(bad_path, "wb") as f:
        f.write(b"this is not a valid huffman file")
    try:
        decompress_file(bad_path, os.path.join(TMP_DIR, "bad_out.txt"))
        check(False, "invalid file should have raised ValueError")
    except ValueError as e:
        check(True, f"invalid file correctly raised ValueError: {e}")


def test_mixed_content():
    print("\nTest 7: File with spaces, numbers, punctuation")
    stats, verified = round_trip("mixed_content.txt")
    check(verified, "mixed_content.txt round-trips losslessly")


def test_fixed_length_baseline():
    print("\nTest 8: Fixed-length baseline runs and returns sane values")
    with open(os.path.join(TEST_DIR, "normal_text.txt"), "rb") as f:
        data = f.read()
    result = run_fixed_length_baseline(data)
    check(result["fixed_length_size"] > 0, "fixed-length baseline produces a positive size")
    check(result["unique_symbols"] > 0, "fixed-length baseline counts unique symbols")


def main():
    test_normal_text()
    test_repetitive()
    test_different_sizes()
    test_single_symbol()
    test_empty_file()
    test_invalid_compressed_file()
    test_mixed_content()
    test_fixed_length_baseline()

    print(f"\n{'='*40}\nRESULTS: {PASS} passed, {FAIL} failed\n{'='*40}")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
