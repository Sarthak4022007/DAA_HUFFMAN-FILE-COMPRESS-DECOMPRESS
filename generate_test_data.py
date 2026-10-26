"""
generate_test_data.py

Creates the sample files used for testing and the performance
experiment. Run this once before using the app:

    python generate_test_data.py

All text here is self-written filler text (not copied from any
external or copyrighted source), so it is safe to include in the
submitted project.
"""

import os

TEST_DIR = "test_data"
os.makedirs(TEST_DIR, exist_ok=True)

PARAGRAPH = (
    "Data compression is the process of reducing the number of bits "
    "needed to represent information. Lossless compression algorithms, "
    "such as Huffman coding, allow the original data to be perfectly "
    "reconstructed from the compressed data. Huffman coding works by "
    "assigning shorter binary codes to symbols that occur more "
    "frequently and longer codes to symbols that occur less "
    "frequently. This simple greedy idea, combined with a binary "
    "prefix-code tree, produces an encoding that is provably optimal "
    "among all prefix codes for a given set of symbol frequencies. "
)


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {path} ({os.path.getsize(path)} bytes)")


def main():
    # 1. repetitive.txt - highly repetitive, should compress very well
    write_file(os.path.join(TEST_DIR, "repetitive.txt"), "AAAA BBBB " * 2000)

    # 2. normal_text.txt - ordinary paragraph-style text
    write_file(os.path.join(TEST_DIR, "normal_text.txt"), PARAGRAPH * 20)

    # 3. single_symbol.txt - edge case: only one unique symbol
    write_file(os.path.join(TEST_DIR, "single_symbol.txt"), "A" * 5000)

    # 4. empty.txt - edge case: empty file
    write_file(os.path.join(TEST_DIR, "empty.txt"), "")

    # 5. mixed_content.txt - letters, numbers, punctuation, spaces
    mixed = "The Quick Brown Fox Jumps Over 12345 Lazy Dogs! @#$%^&*() " * 100
    write_file(os.path.join(TEST_DIR, "mixed_content.txt"), mixed)

    # Sized datasets for the input-size experiment (small / medium / large)
    unit = PARAGRAPH  # ~470 bytes per repetition

    small_target = 10 * 1024      # ~10 KB
    medium_target = 100 * 1024    # ~100 KB
    large_target = 1024 * 1024    # ~1 MB

    def build_to_size(target_size):
        repeats = max(1, target_size // len(unit) + 1)
        text = unit * repeats
        return text[:target_size]

    write_file(os.path.join(TEST_DIR, "small.txt"), build_to_size(small_target))
    write_file(os.path.join(TEST_DIR, "medium.txt"), build_to_size(medium_target))
    write_file(os.path.join(TEST_DIR, "large.txt"), build_to_size(large_target))

    print("\nAll test files generated in the 'test_data' directory.")


if __name__ == "__main__":
    main()
