# Huffman File Compressor — Setup, Run & Test (Simple Guide)

## What this project does
It shrinks a text file (compress) and can rebuild it back exactly
(decompress), using an algorithm called Huffman Coding.

## 1. Install (one time only)
Open a terminal/command prompt inside this folder, then type:
```
pip install -r requirements.txt
```

## 2. Create sample test files (one time only)
```
python generate_test_data.py
```
This creates files inside `test_data/` for you to test with.

## 3. Run the app
```
python app.py
```
It will print a web address like `http://127.0.0.1:5000`. Open that
in your browser.

## 4. Use it
- **Compress page:** pick a file (try `test_data/normal_text.txt`) → click Compress → see the shrunk size.
- **Decompress page:** pick the `.huff` file you just downloaded → click Decompress → see "SUCCESS", meaning the file was rebuilt perfectly.
- **Performance page:** click "Run Experiment" → see real numbers and charts comparing this algorithm to a simple baseline.

## 5. Run the automatic tests (optional, proves it works)
```
python test_huffman.py
```
You should see every check say "PASS".

## That's it
Everything above is real — no fake numbers, nothing pre-recorded.
Every time you click a button, it actually runs the algorithm live.
