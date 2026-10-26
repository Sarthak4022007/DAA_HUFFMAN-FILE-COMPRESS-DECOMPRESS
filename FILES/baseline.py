"""
baseline.py

Fixed-Length Encoding Baseline.

This is NOT a competing compression algorithm. It is a simple
reference point used to show why Huffman Coding's variable-length,
frequency-based codes are useful.

Every unique symbol in the file is given a code of the SAME length
(enough bits to represent all unique symbols), regardless of how
often it occurs.

Example: if there are 4 unique symbols,
    A -> 00
    B -> 01
    C -> 10
    D -> 11
"""

import math
import time


def calculate_fixed_length_size(original_size: int, unique_symbols: int) -> int:
    """Compute the size (in bytes) of the fixed-length encoded output.

    Each symbol needs ceil(log2(k)) bits, where k = number of unique
    symbols. If there is only one unique symbol, 1 bit is still
    needed per occurrence (a real encoder cannot use 0 bits/symbol).
    """
    if unique_symbols <= 1:
        bits_per_symbol = 1
    else:
        bits_per_symbol = math.ceil(math.log2(unique_symbols))

    total_bits = original_size * bits_per_symbol
    total_bytes = math.ceil(total_bits / 8)
    return total_bytes, bits_per_symbol


def run_fixed_length_baseline(data: bytes) -> dict:
    """Run the fixed-length baseline "encoding" and measure timing.

    We do not need to physically write the bits to disk to make a
    fair comparison of size; the size is determined exactly by the
    number of unique symbols and the file length. We do measure the
    time to at least build the symbol table, so a timing figure is
    still meaningful (not fabricated).
    """
    t0 = time.perf_counter()
    unique_symbols = len(set(data))
    fixed_size, bits_per_symbol = calculate_fixed_length_size(len(data), unique_symbols)
    elapsed = time.perf_counter() - t0

    return {
        "unique_symbols": unique_symbols,
        "bits_per_symbol": bits_per_symbol,
        "fixed_length_size": fixed_size,
        "time": elapsed,
    }
