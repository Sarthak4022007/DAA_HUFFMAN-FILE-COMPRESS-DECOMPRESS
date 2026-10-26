"""
app.py

Simple Flask web interface for the Huffman File Compressor.

This file only wires up the web pages and form handling. All of the
actual algorithm work happens in huffman.py and baseline.py.
"""

import os
import csv

from flask import Flask, render_template, request, send_file, flash, redirect, url_for

from huffman import compress_file, decompress_file, verify_lossless, calculate_frequencies
from baseline import run_fixed_length_baseline
from performance import run_experiment
from utils import format_bytes, safe_filename, ensure_dirs

app = Flask(__name__)
app.secret_key = "daa-huffman-mini-project"  # fine for a local academic demo

UPLOAD_DIR = "uploads"
COMPRESSED_DIR = "compressed"
DECOMPRESSED_DIR = "decompressed"
RESULTS_DIR = "results"

ensure_dirs(UPLOAD_DIR, COMPRESSED_DIR, DECOMPRESSED_DIR, RESULTS_DIR)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compress", methods=["GET", "POST"])
def compress():
    result = None
    error = None

    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            error = "No file selected."
        else:
            filename = safe_filename(file.filename)
            input_path = os.path.join(UPLOAD_DIR, filename)
            file.save(input_path)

            if os.path.getsize(input_path) == 0:
                error = "Cannot compress an empty file."
            else:
                output_path = os.path.join(COMPRESSED_DIR, filename + ".huff")
                try:
                    stats = compress_file(input_path, output_path)
                    result = {
                        "filename": filename,
                        "compressed_filename": filename + ".huff",
                        "original_size": format_bytes(stats["original_size"]),
                        "compressed_size": format_bytes(stats["compressed_size"]),
                        "unique_symbols": stats["unique_symbols"],
                        "compression_ratio": f"{stats['compression_ratio']:.4f}",
                        "space_saving": f"{stats['space_saving_percent']:.2f}%",
                        "total_time_ms": f"{stats['total_time'] * 1000:.3f} ms",
                    }
                except ValueError as e:
                    error = str(e)

    return render_template("compress.html", result=result, error=error)


@app.route("/download/compressed/<filename>")
def download_compressed(filename):
    filename = safe_filename(filename)
    path = os.path.join(COMPRESSED_DIR, filename)
    if not os.path.exists(path):
        flash("File not found.")
        return redirect(url_for("compress"))
    return send_file(path, as_attachment=True)


@app.route("/decompress", methods=["GET", "POST"])
def decompress():
    result = None
    error = None

    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            error = "No compressed file selected."
        else:
            filename = safe_filename(file.filename)
            input_path = os.path.join(COMPRESSED_DIR, filename)
            file.save(input_path)

            output_name = filename[:-5] if filename.endswith(".huff") else filename + ".decompressed"
            output_path = os.path.join(DECOMPRESSED_DIR, output_name)

            try:
                stats = decompress_file(input_path, output_path)
                result = {
                    "filename": filename,
                    "decompressed_filename": output_name,
                    "decompressed_size": format_bytes(stats["decompressed_size"]),
                    "total_time_ms": f"{stats['total_time'] * 1000:.3f} ms",
                }
                # If the original uploaded file (pre-compression) still
                # exists under the same base name, verify losslessness.
                possible_original = os.path.join(UPLOAD_DIR, output_name)
                if os.path.exists(possible_original):
                    result["verification"] = (
                        "SUCCESS" if verify_lossless(possible_original, output_path) else "FAILED"
                    )
            except ValueError as e:
                error = str(e)

    return render_template("decompress.html", result=result, error=error)


@app.route("/download/decompressed/<filename>")
def download_decompressed(filename):
    filename = safe_filename(filename)
    path = os.path.join(DECOMPRESSED_DIR, filename)
    if not os.path.exists(path):
        flash("File not found.")
        return redirect(url_for("decompress"))
    return send_file(path, as_attachment=True)


@app.route("/performance", methods=["GET", "POST"])
def performance():
    rows = []
    csv_path = os.path.join(RESULTS_DIR, "performance_results.csv")

    ran_now = False
    if request.method == "POST":
        run_experiment()
        ran_now = True

    if os.path.exists(csv_path):
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    charts = {
        "compression_time": os.path.exists(os.path.join(RESULTS_DIR, "compression_time.png")),
        "compression_size": os.path.exists(os.path.join(RESULTS_DIR, "compression_size.png")),
        "algorithm_comparison": os.path.exists(os.path.join(RESULTS_DIR, "algorithm_comparison.png")),
    }

    return render_template("performance.html", rows=rows, charts=charts, ran_now=ran_now)


@app.route("/results/<path:filename>")
def results_file(filename):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        flash("File not found.")
        return redirect(url_for("performance"))
    return send_file(path)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
