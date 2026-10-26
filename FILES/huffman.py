"""
huffman.py

Core implementation of Huffman Coding (Greedy Algorithm).

This file contains only the algorithm itself:
    - frequency counting
    - min-heap based Huffman tree construction
    - code generation
    - bit-level encoding / decoding
    - file compression / decompression using a simple custom file format

No third-party libraries are used. Everything is built with the
Python standard library (heapq, collections, os, time).
"""

import heapq
import os
import time
from collections import Counter


class Node:
    """A single node of the Huffman tree.

    A node is either a leaf (holds one byte value, 0-255) or an
    internal node (holds two children and no byte value).
    """

    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte      # only set for leaf nodes
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

    # heapq needs a way to compare nodes when frequencies are equal.
    # We break ties using an insertion counter supplied from outside,
    # so this method is only a fallback and is rarely used directly.
    def __lt__(self, other):
        return self.freq < other.freq


# ---------------------------------------------------------------------
# Step 1: Frequency calculation
# ---------------------------------------------------------------------
def calculate_frequencies(data: bytes) -> dict:
    """Count how many times each byte value appears in the data.

    Time complexity: O(n), where n = number of bytes in the input.
    """
    return dict(Counter(data))


# ---------------------------------------------------------------------
# Step 2 & 3: Build the Huffman tree using a min-heap (greedy step)
# ---------------------------------------------------------------------
def build_huffman_tree(freq_table: dict) -> Node:
    """Build the Huffman tree from a frequency table.

    Greedy strategy:
        Repeatedly remove the two nodes with the smallest frequency
        and merge them into a new parent node, until only one node
        (the root) remains.

    Time complexity: O(k log k), where k = number of unique symbols,
    because every heap push/pop costs O(log k) and we do this
    roughly 2k times.
    """
    if not freq_table:
        return None

    heap = []
    # 'counter' makes every heap entry unique so heapq never has to
    # compare two Node objects directly when their frequencies tie.
    counter = 0
    for byte, freq in freq_table.items():
        heapq.heappush(heap, (freq, counter, Node(freq, byte=byte)))
        counter += 1

    # Special case: only one unique symbol in the whole file.
    # A single leaf cannot produce a valid prefix code by itself,
    # so we wrap it under one artificial parent node. This guarantees
    # the symbol gets the code "0" instead of an empty code.
    if len(heap) == 1:
        _, _, only_node = heap[0]
        return Node(only_node.freq, left=only_node)

    while len(heap) > 1:
        freq1, _, node1 = heapq.heappop(heap)
        freq2, _, node2 = heapq.heappop(heap)

        # Combine the two least frequent nodes (greedy choice).
        merged = Node(freq1 + freq2, left=node1, right=node2)
        heapq.heappush(heap, (merged.freq, counter, merged))
        counter += 1

    return heap[0][2]


# ---------------------------------------------------------------------
# Step 4: Generate Huffman codes by traversing the tree
# ---------------------------------------------------------------------
def generate_codes(root: Node) -> dict:
    """Walk the Huffman tree and assign a binary code to every byte.

    Left branch  -> '0'
    Right branch -> '1'

    Time complexity: O(k), where k = number of unique symbols
    (there are exactly k leaves and k-1 internal nodes in the tree).
    """
    codes = {}
    if root is None:
        return codes

    # Iterative traversal (stack) to avoid recursion-depth issues on
    # files with many unique symbols.
    stack = [(root, "")]
    while stack:
        node, code = stack.pop()
        if node.is_leaf():
            # Guarantee a non-empty code even for the one-symbol case.
            codes[node.byte] = code if code else "0"
            continue
        if node.left:
            stack.append((node.left, code + "0"))
        if node.right:
            stack.append((node.right, code + "1"))

    return codes


# ---------------------------------------------------------------------
# Step 5: Encode data using the generated codes
# ---------------------------------------------------------------------
def encode_data(data: bytes, codes: dict) -> str:
    """Replace every byte with its Huffman code, producing one long
    string of '0'/'1' characters.

    Time complexity: O(n), where n = number of bytes in the input.
    """
    return "".join(codes[byte] for byte in data)


# ---------------------------------------------------------------------
# Padding: bit-string -> bytes
# ---------------------------------------------------------------------
def pad_encoded_data(encoded: str) -> tuple:
    """Pad the bit-string so its length is a multiple of 8, and record
    how many padding bits were added so decoding can remove them.
    """
    extra_padding = (8 - len(encoded) % 8) % 8
    padded = encoded + ("0" * extra_padding)
    return padded, extra_padding


def bits_to_bytes(bit_string: str) -> bytes:
    """Convert a padded '0'/'1' string into real bytes."""
    out = bytearray()
    for i in range(0, len(bit_string), 8):
        byte_chunk = bit_string[i:i + 8]
        out.append(int(byte_chunk, 2))
    return bytes(out)


def bytes_to_bits(data: bytes) -> str:
    """Convert bytes back into a '0'/'1' string."""
    return "".join(f"{byte:08b}" for byte in data)


# ---------------------------------------------------------------------
# Compressed file format
# ---------------------------------------------------------------------
# The compressed file stores everything needed to reconstruct the
# Huffman tree and decode the data:
#
#   [4 bytes]  number of entries in the frequency table (unsigned int)
#   for each entry:
#       [1 byte]  the byte value (0-255)
#       [4 bytes] its frequency (unsigned int)
#   [1 byte]   number of padding bits added to the final byte
#   [...]      the encoded data itself, as raw bytes
#
# Storing the frequency table (rather than the tree shape) is the
# simplest reliable way to let the decompressor rebuild the exact
# same Huffman tree that the compressor used.
MAGIC_HEADER = b"HUFF"  # simple marker so decompression can sanity-check the file


def compress_file(input_path: str, output_path: str) -> dict:
    """Compress a file using Huffman coding.

    Returns a dictionary of statistics about the run, including
    timings for each stage (used by the performance experiment).
    """
    timings = {}

    t0 = time.perf_counter()
    with open(input_path, "rb") as f:
        data = f.read()
    timings["read_time"] = time.perf_counter() - t0

    original_size = len(data)

    if original_size == 0:
        raise ValueError("Cannot compress an empty file.")

    t0 = time.perf_counter()
    freq_table = calculate_frequencies(data)
    timings["frequency_time"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    tree_root = build_huffman_tree(freq_table)
    timings["tree_build_time"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    codes = generate_codes(tree_root)
    timings["code_gen_time"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    encoded_bits = encode_data(data, codes)
    padded_bits, padding = pad_encoded_data(encoded_bits)
    encoded_bytes = bits_to_bytes(padded_bits)
    timings["encode_time"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    with open(output_path, "wb") as f:
        f.write(MAGIC_HEADER)
        f.write(len(freq_table).to_bytes(4, "big"))
        for byte_val, freq in freq_table.items():
            f.write(byte_val.to_bytes(1, "big"))
            f.write(freq.to_bytes(4, "big"))
        f.write(padding.to_bytes(1, "big"))
        f.write(encoded_bytes)
    timings["write_time"] = time.perf_counter() - t0

    compressed_size = os.path.getsize(output_path)
    total_time = sum(timings.values())

    return {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "unique_symbols": len(freq_table),
        "compression_ratio": compressed_size / original_size,
        "space_saving_percent": (1 - compressed_size / original_size) * 100,
        "timings": timings,
        "total_time": total_time,
    }


def decompress_file(input_path: str, output_path: str) -> dict:
    """Decompress a Huffman-compressed file created by compress_file()."""
    timings = {}

    t0 = time.perf_counter()
    with open(input_path, "rb") as f:
        header = f.read(4)
        if header != MAGIC_HEADER:
            raise ValueError("Not a valid Huffman-compressed file.")

        num_entries = int.from_bytes(f.read(4), "big")
        freq_table = {}
        for _ in range(num_entries):
            byte_val = int.from_bytes(f.read(1), "big")
            freq = int.from_bytes(f.read(4), "big")
            freq_table[byte_val] = freq

        padding = int.from_bytes(f.read(1), "big")
        encoded_bytes = f.read()
    timings["read_time"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    tree_root = build_huffman_tree(freq_table)
    timings["tree_rebuild_time"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    bit_string = bytes_to_bits(encoded_bytes)
    if padding:
        bit_string = bit_string[:-padding]

    output = bytearray()
    node = tree_root
    # If the tree is a single leaf wrapped under one parent (the
    # one-unique-symbol special case), every '0' bit maps to that
    # one symbol.
    for bit in bit_string:
        node = node.left if bit == "0" else node.right
        if node.is_leaf():
            output.append(node.byte)
            node = tree_root
    timings["decode_time"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    with open(output_path, "wb") as f:
        f.write(output)
    timings["write_time"] = time.perf_counter() - t0

    total_time = sum(timings.values())

    return {
        "decompressed_size": len(output),
        "timings": timings,
        "total_time": total_time,
    }


def verify_lossless(original_path: str, decompressed_path: str) -> bool:
    """Compare the original file and the decompressed file byte-for-byte."""
    with open(original_path, "rb") as f1, open(decompressed_path, "rb") as f2:
        return f1.read() == f2.read()
