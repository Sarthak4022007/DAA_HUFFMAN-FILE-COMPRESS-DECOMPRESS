import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "DAA Mini Project: Huffman File Compressor — Presentation Guide | Tirth Shah")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)
        
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 40, 576, 40)
        self.drawString(36, 28, "Confidential Academic Presentation Notes • Huffman Coding Project")
        self.drawRightString(576, 28, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename="Huffman_Project_Presentation_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    # Custom palette
    PRIMARY = colors.HexColor("#1E3A8A")
    SECONDARY = colors.HexColor("#0F766E")
    DARK_TEXT = colors.HexColor("#1E293B")
    MUTED_TEXT = colors.HexColor("#475569")
    BG_LIGHT = colors.HexColor("#F8FAFC")
    BG_CARD = colors.HexColor("#F1F5F9")
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography styles
    styles.add(ParagraphStyle(
        name='MainTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name='SubTitle',
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=MUTED_TEXT,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='BodyCustom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='TipBox',
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#854D0E"),
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='SpeechQuote',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='QAQuestion',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=PRIMARY,
        spaceAfter=3,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='QAAnswer',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=DARK_TEXT
    ))
    styles.add(ParagraphStyle(
        name='TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=PRIMARY
    ))

    story = []

    # Banner / Title
    story.append(Paragraph("DAA MINI PROJECT: FILE COMPRESSION USING HUFFMAN CODING", ParagraphStyle(
        'Badge', fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=SECONDARY, spaceAfter=4
    )))
    story.append(Paragraph("Master Presentation Script & Defense Handbook", styles['MainTitle']))
    story.append(Paragraph("<b>Presenter:</b> Tirth Shah &nbsp;|&nbsp; <b>Algorithm:</b> Greedy Huffman Coding &nbsp;|&nbsp; <b>Subject:</b> Design & Analysis of Algorithms", styles['SubTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=10))

    # Mental Model Box
    mental_model_data = [[
        Paragraph(
            "<b>Mental Model for Tirth (Web Tech Analogy):</b><br/>"
            "Even though this project is in Python, think of it in terms of web development: "
            "<b>templates/</b> & <b>static/</b> is your Frontend (HTML/CSS). "
            "<b>app.py</b> is your Node/Express Backend Server handling URL routes and form uploads. "
            "<b>huffman.py</b> is the core Algorithm Engine doing the mathematical compression. "
            "<b>baseline.py</b> is a benchmark comparator proving why Huffman is superior to fixed-length bits.",
            styles['TipBox']
        )
    ]]
    t_model = Table(mental_model_data, colWidths=[540])
    t_model.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEFCE8")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#FEF08A")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_model)
    story.append(Spacer(1, 10))

    # SECTION 1: FILE GUIDE
    story.append(Paragraph("1. Complete Project Structure & File Guide", styles['SectionHeading']))
    story.append(Paragraph("What every file does and why it was created:", styles['BodyCustom']))

    file_table_data = [
        [Paragraph("File / Folder", styles['TableHeader']), Paragraph("Role", styles['TableHeader']), Paragraph("What It Does & Why It Exists", styles['TableHeader'])],
        [Paragraph("<b>huffman.py</b>", styles['TableCellBold']), Paragraph("Core Algorithm", styles['TableCell']), Paragraph("<b>The heart of the project.</b> Pure Python implementation: counts byte frequencies, builds binary tree using a Min-Heap, generates variable-length prefix codes, encodes data, and writes the custom <code>.huff</code> file format with headers.", styles['TableCell'])],
        [Paragraph("<b>app.py</b>", styles['TableCellBold']), Paragraph("Web Server (Flask)", styles['TableCell']), Paragraph("The web controller (like Express.js). Manages routes (<code>/compress</code>, <code>/decompress</code>, <code>/performance</code>), receives uploaded files, calls <code>huffman.py</code>, and displays results in HTML.", styles['TableCell'])],
        [Paragraph("<b>baseline.py</b>", styles['TableCellBold']), Paragraph("Benchmark Reference", styles['TableCell']), Paragraph("Calculates fixed-length encoding size (&lceil;log<sub>2</sub> k&rceil; bits/char) to prove to the professor why Huffman's variable-length frequency codes achieve vastly superior space savings.", styles['TableCell'])],
        [Paragraph("<b>performance.py</b>", styles['TableCellBold']), Paragraph("Experiment Engine", styles['TableCell']), Paragraph("Runs automated benchmark experiments across 5 datasets (small/medium/large/repetitive), generates <code>results/performance_results.csv</code>, and plots comparison graphs using <code>matplotlib</code>.", styles['TableCell'])],
        [Paragraph("<b>generate_test_data.py</b>", styles['TableCellBold']), Paragraph("Test Data Creator", styles['TableCell']), Paragraph("Generates realistic sample files in <code>test_data/</code> (small ~10KB, medium ~100KB, large ~1MB, repetitive, single symbol, and empty) for live demonstrations and testing.", styles['TableCell'])],
        [Paragraph("<b>test_huffman.py</b>", styles['TableCellBold']), Paragraph("Unit Test Suite", styles['TableCell']), Paragraph("8 automated unit tests verifying correctness, round-trip lossless verification, single-symbol handling, and invalid file error safety.", styles['TableCell'])],
        [Paragraph("<b>utils.py</b>", styles['TableCellBold']), Paragraph("Helper Functions", styles['TableCell']), Paragraph("Utilities to convert raw bytes into readable strings (e.g., 1024 B &rarr; '1.00 KB') and sanitize uploaded filenames.", styles['TableCell'])],
        [Paragraph("<b>templates/ & static/</b>", styles['TableCellBold']), Paragraph("Frontend UI", styles['TableCell']), Paragraph("HTML templates (<code>index.html</code>, <code>compress.html</code>, <code>decompress.html</code>, <code>performance.html</code>) and CSS stylesheets providing the web interface.", styles['TableCell'])],
    ]
    t_files = Table(file_table_data, colWidths=[110, 95, 335])
    t_files.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
    ]))
    story.append(t_files)
    story.append(Spacer(1, 10))

    # SECTION 2: SETUP
    story.append(Paragraph("2. Quick Pre-Presentation Terminal Commands", styles['SectionHeading']))
    setup_data = [[
        Paragraph(
            "<b>Step 1: Install dependencies (one-time):</b> <code>pip install -r requirements.txt</code><br/>"
            "<b>Step 2: Start the server before going on stage:</b> <code>python app.py</code><br/>"
            "<b>Step 3: Open in browser:</b> Navigate to <b>http://127.0.0.1:5000</b> and leave the tab open ready to demonstrate.",
            styles['BodyCustom']
        )
    ]]
    t_setup = Table(setup_data, colWidths=[540])
    t_setup.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BORDER', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_setup)

    story.append(PageBreak())

    # SECTION 3: SLIDE 11 SCRIPT
    story.append(Paragraph("3. Slide 11: Live Project Demo Script (What to Click & What to Say)", styles['SectionHeading']))
    demo_script_content = (
        "<b>[Opening Statement]:</b><br/>"
        "<i>\"Now, let's look at the live demonstration of our application. "
        "We built an interactive web interface using Python's Flask framework so we can test and visualize compression in real time.\"</i><br/><br/>"
        "<b>[Step 1: Compress Tab] &rarr; Click on 'Compress' in top navigation:</b><br/>"
        "<i>\"Here on the Compress page, I will select a sample file — <code>test_data/normal_text.txt</code> — and click Compress.\"</i><br/><br/>"
        "<b>[Step 2: Show Compression Results] &rarr; Click Compress button:</b><br/>"
        "<i>\"As you can see, the file is compressed instantly. Our application gives us exact metrics:<br/>"
        "• Original size vs compressed size.<br/>"
        "• Number of unique characters.<br/>"
        "• Compression ratio and space savings percentage.<br/>"
        "• Total execution time in milliseconds.<br/>"
        "We can now download this <code>.huff</code> file directly.\"</i><br/><br/>"
        "<b>[Step 3: Decompress Tab] &rarr; Click on 'Decompress' in top navigation:</b><br/>"
        "<i>\"Now, to prove that Huffman coding is completely <b>lossless</b>, we go to the Decompress page, upload that exact <code>.huff</code> file, and click Decompress.\"</i><br/><br/>"
        "<b>[Step 4: Show Lossless Verification] &rarr; Point to green badge on screen:</b><br/>"
        "<i>\"Notice this badge right here: <b>Verification: SUCCESS</b>. Our algorithm performed an exact byte-for-byte comparison between the original file and the recovered file, proving zero data was lost.\"</i><br/><br/>"
        "<b>[Step 5: Performance Tab] &rarr; Click on 'Performance' in top navigation:</b><br/>"
        "<i>\"Finally, on the Performance page, we compare Huffman coding against a standard Fixed-Length baseline across multiple file sizes. "
        "Huffman consistently achieves significantly smaller file sizes because frequent symbols use as few as 1 or 2 bits, whereas fixed-length encoding is forced to use the exact same number of bits for every character.\"</i>"
    )
    t_demo = Table([[Paragraph(demo_script_content, styles['SpeechQuote'])]], colWidths=[540])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDFA")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#99F6E4")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 10))

    # SECTION 4: SLIDE 12 SCRIPT
    story.append(Paragraph("4. Slide 12: Source Code Walkthrough (What to Show in VS Code)", styles['SectionHeading']))
    code_script_content = (
        "<b>[Opening Statement with VS Code open]:</b><br/>"
        "<i>\"Now let's quickly walk through the code structure and how the algorithm is implemented. "
        "The entire algorithm is cleanly isolated in <b>huffman.py</b>, structured into 5 logical stages:\"</i><br/><br/>"
        "<b>1. Frequency Counter (<code>calculate_frequencies</code>, line 49):</b><br/>"
        "<i>\"We read the raw file as bytes and count character occurrences in O(n) time using Python's Counter.\"</i><br/><br/>"
        "<b>2. Greedy Min-Heap Tree Construction (<code>build_huffman_tree</code>, line 60):</b><br/>"
        "<i>\"We insert all unique characters into a Priority Queue (Min-Heap). Then, in a loop, we repeatedly extract the two nodes with the lowest frequencies, merge them into a parent node, and push it back until one root node remains. This runs in O(k log k) time, where k is the number of unique characters.\"</i><br/><br/>"
        "<b>3. Prefix Code Generation (<code>generate_codes</code>, line 106):</b><br/>"
        "<i>\"We traverse the binary tree from the root: assigning binary '0' to left branches and '1' to right branches. Frequent characters end up near the root with the shortest codes.\"</i><br/><br/>"
        "<b>4. Bit Packaging (<code>pad_encoded_data</code> & <code>bits_to_bytes</code>, lines 151-166):</b><br/>"
        "<i>\"Since storage media write full 8-bit bytes, we pad the final bit-string to a multiple of 8 and record the padding bit count.\"</i><br/><br/>"
        "<b>5. Custom Binary File Header (lines 175-238):</b><br/>"
        "<i>\"In the compressed <code>.huff</code> file, we write a magic header ('HUFF') and the frequency table so the decompressor can rebuild the exact same tree without needing the original file.\"</i><br/><br/>"
        "<i>\"Meanwhile, <b>baseline.py</b> provides our analytical fixed-length baseline for comparison, and <b>app.py</b> connects everything to our web frontend.\"</i>"
    )
    t_code = Table([[Paragraph(code_script_content, styles['SpeechQuote'])]], colWidths=[540])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)

    story.append(PageBreak())

    # SECTION 5: COUNTER QUESTIONS
    story.append(Paragraph("5. Master Counter-Question Defense Shield (Top 10 Viva Questions)", styles['SectionHeading']))
    story.append(Paragraph("Memorize these clear, direct answers for professor Q&A:", styles['BodyCustom']))

    qa_list = [
        ("Q1: What makes Huffman Coding a Greedy Algorithm?",
         "At every step, we make the locally optimal choice: we always select and combine the two nodes with the smallest frequencies without looking ahead. This local greedy choice is mathematically proven to produce an optimal prefix code (global optimum)."),
        
        ("Q2: What is the Time and Space Complexity?",
         "• Time Complexity: O(n) for frequency counting (n = total bytes) + O(k log k) for tree building using a Min-Heap (k = unique characters ≤ 256). Overall time is O(n).<br/>• Space Complexity: O(k) to store the tree nodes and frequency table (at most 256 unique bytes, so very compact)."),
        
        ("Q3: What data structure did you use to find the two minimums?",
         "We used a Min-Heap (Priority Queue) from Python's standard heapq module. Extracting the minimum element from a Min-Heap takes O(log k) time, which makes tree construction very fast."),
        
        ("Q4: What is a 'Prefix-Free Code' (Prefix Property)?",
         "A prefix-free code means no character's binary code is a prefix of another character's code. Because characters only exist at the LEAF NODES of our binary tree, this property is automatically guaranteed. During decompression, we can decode continuously without needing any delimiters or separators between bits."),
        
        ("Q5: How does Decompression work? Does it need the original file?",
         "No, the original file is never needed. When compressing, we save the frequency table in the header of the .huff file. During decompression, the program reads the table, rebuilds the identical tree, and walks down the tree bit-by-bit (0 = left, 1 = right) to reconstruct original characters."),
        
        ("Q6: Can a compressed file ever be larger than the original file?",
         "Yes! For very tiny files (under ~50 bytes) or completely random/encrypted data. This happens because the compressed file must store the header (frequency table). If the file is too small, the header overhead exceeds the space saved by compression."),
        
        ("Q7: What happens if a file has only ONE unique character, like 'AAAAA'?",
         "Normally, a single character cannot form a binary tree with two children. In our code (huffman.py, lines 83-90), we handle this edge-case by wrapping that single leaf node under an artificial parent node and assigning it code '0'. It compresses and decompresses with 100% accuracy."),
        
        ("Q8: Why did you create baseline.py?",
         "To establish an empirical comparison for DAA analysis. Fixed-length encoding uses the same bit length (⌈log₂ k⌉) for every symbol. Huffman uses variable lengths based on frequency. Comparing them side-by-side demonstrates the superiority of Huffman's greedy approach."),
        
        ("Q9: Is Huffman coding Lossless or Lossy?",
         "It is strictly Lossless. The reconstructed file is 100% byte-for-byte identical to the original. Our decompress function automatically executes verify_lossless() to prove this."),
        
        ("Q10: What happens if the total encoded bits are not a multiple of 8?",
         "Computers store data in whole 8-bit bytes. If the encoded bit-string is 19 bits, we add 5 extra padding zero bits to make it 24 bits (3 bytes). We store the padding count (5) in the header so the decompressor strips off those extra bits.")
    ]

    for q, a in qa_list:
        qa_card = [
            [Paragraph(q, styles['QAQuestion'])],
            [Paragraph(a, styles['QAAnswer'])]
        ]
        t_qa = Table(qa_card, colWidths=[540])
        t_qa.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BORDER', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_qa)
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    build_pdf()
