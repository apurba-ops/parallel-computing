import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs('extracted_images', exist_ok=True)

# Slide dimensions matching RevealJS config (16:9)
SLIDE_W, SLIDE_H = 1280, 720

# Theme Palette (BITS Pilani Colors & Modern Academic Slide Palette)
BG_COLOR = (255, 255, 255)
TEXT_DARK = (15, 23, 42)
TEXT_MUTED = (100, 116, 139)
NAVY = (0, 51, 102)
NAVY_LIGHT = (22, 78, 135)
CRIMSON = (215, 25, 32)
GOLD = (229, 169, 60)
BOX_BG = (248, 250, 252)
BOX_BORDER = (203, 213, 225)
LINE_COLOR = (51, 65, 85)
HIGHLIGHT_BLUE = (37, 99, 235)
HIGHLIGHT_RED = (220, 38, 38)
HIGHLIGHT_GREEN = (16, 185, 129)
ACCENT_CYAN = (6, 182, 212)
CARD_BG_GOOD = (240, 253, 244)
CARD_BORDER_GOOD = (134, 239, 172)
CARD_BG_BAD = (254, 242, 242)
CARD_BORDER_BAD = (252, 165, 165)

def get_font(size, bold=False):
    font_names = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_arrow(draw, x1, y1, x2, y2, color=LINE_COLOR, width=2, arrow_len=8):
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    tip1 = (x2 - arrow_len * math.cos(angle - math.pi / 6), y2 - arrow_len * math.sin(angle - math.pi / 6))
    tip2 = (x2 - arrow_len * math.cos(angle + math.pi / 6), y2 - arrow_len * math.sin(angle + math.pi / 6))
    draw.polygon([ (x2, y2), tip1, tip2 ], fill=color)

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def wrap_text_multi(draw, text, font, first_w, rest_w):
    words = text.split()
    lines = []
    current_line = []
    w_limit = first_w
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font) if draw else font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w <= w_limit:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                w_limit = rest_w
            else:
                lines.append(word)
                w_limit = rest_w
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# -------------------------------------------------------------
# 1. lec19_block_array_higher_dims.png
# Replicating Slide 1: 4x4 Square Mesh vs 2x8 Rectangular Grid
# -------------------------------------------------------------
def create_block_array_higher_dims():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_badge = get_font(14, bold=True)
    font_mono = get_font(16, bold=True)
    font_text = get_font(13.5, bold=False)

    draw.text((W // 2, 28), "Static Mapping: Block Array Distribution Scheme in Higher Dimensions", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Generalizing 1-D Block Partitions to 2-D Process Meshes (Grama Sec 3.4.1)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: 4x4 Square Mesh
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 108), "(a) Square Process Grid (4 × 4 Mesh, p = 16)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 132), "Ideal for isotropic 2-D arrays (Equal Aspect Ratio)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 4x4 Grid
    ox1 = 40 + (p_w - 280) // 2
    oy1 = 160
    cell_s = 70
    for r in range(4):
        for c in range(4):
            pid = r * 4 + c
            x1 = ox1 + c * cell_s
            y1 = oy1 + r * cell_s
            bg = (239, 246, 255) if (r + c) % 2 == 0 else (255, 255, 255)
            draw.rectangle([x1, y1, x1 + cell_s, y1 + cell_s], fill=bg, outline=LINE_COLOR, width=1)
            draw.text((x1 + cell_s // 2, y1 + cell_s // 2), f"P_{{{pid}}}", fill=NAVY, font=font_mono, anchor="mm")

    # Left card description
    draw.rounded_rectangle([60, 465, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 478), "Square Grid Characteristics (4 × 4 Mesh):", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([75, 498, 40 + p_w - 35, 498], fill=BOX_BORDER, width=1)
    
    notes_left = [
        ("Sub-block Dimensions", "Each process owns (n/4) × (n/4) array elements."),
        ("Min-Perimeter Property", "Square blocks minimize perimeter-to-area communication ratio."),
        ("Communication Volume", "Per-process communication scales as O(n/√p) = O(n/4)."),
        ("ScaLAPACK Standard", "Default layout for 2-D dense linear algebra algorithms.")
    ]
    ny = 508
    for lbl, desc in notes_left:
        draw.text((75, ny), f"• {lbl}:", fill=CRIMSON, font=get_font(13, bold=True), anchor="lt")
        pw = get_font(13, bold=True).getbbox(f"• {lbl}: ")[2]
        draw.text((75 + pw + 4, ny), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 28

    # RIGHT PANEL: 2x8 Rectangular Grid
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 108), "(b) Non-Square Process Grid (2 × 8 Mesh, p = 16)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 132), "Adapted for asymmetric algorithms or physical interconnects", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 2x8 Grid
    ox2 = rx + (p_w - 480) // 2
    oy2 = 200
    cw2 = 60
    ch2 = 100
    for r in range(2):
        for c in range(8):
            pid = r * 8 + c
            x1 = ox2 + c * cw2
            y1 = oy2 + r * ch2
            bg = (240, 253, 244) if (r + c) % 2 == 0 else (255, 255, 255)
            draw.rectangle([x1, y1, x1 + cw2, y1 + ch2], fill=bg, outline=LINE_COLOR, width=1)
            draw.text((x1 + cw2 // 2, y1 + ch2 // 2), f"P_{{{pid}}}", fill=NAVY, font=font_mono, anchor="mm")

    # Right card description
    draw.rounded_rectangle([rx + 20, 465, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((rx + 35, 478), "Non-Square Grid Characteristics (2 × 8 Mesh):", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([rx + 35, 498, rx + p_w - 35, 498], fill=BOX_BORDER, width=1)

    notes_right = [
        ("Sub-block Dimensions", "Each process owns (n/2) × (n/8) rectangular elements."),
        ("Asymmetric Data", "Ideal when matrix dimensions differ heavily (e.g., n_rows << n_cols)."),
        ("Hardware Affinity", "Maps to cluster nodes with asymmetric inter-node vs intra-node bandwidth."),
        ("Trade-off", "Perimeter is larger than 4×4: 2(n/2 + n/8) = 1.25n vs 1.0n.")
    ]
    ny = 508
    for lbl, desc in notes_right:
        draw.text((rx + 35, ny), f"• {lbl}:", fill=CRIMSON, font=get_font(13, bold=True), anchor="lt")
        pw = get_font(13, bold=True).getbbox(f"• {lbl}: ")[2]
        draw.text((rx + 35 + pw + 4, ny), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 28

    img.save("extracted_images/lec19_block_array_higher_dims.png")
    print("Saved lec19_block_array_higher_dims.png")

# -------------------------------------------------------------
# 2. lec19_dense_matrix_mult_data_sharing.png
# Replicating Slide 3: Data Sharing in Dense Matrix Multiplication
# -------------------------------------------------------------
def create_dense_matrix_mult_data_sharing():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_badge = get_font(14, bold=True)
    font_mono = get_font(13, bold=True)
    font_math = get_font(24, bold=True)
    font_text = get_font(13, bold=False)

    draw.text((W // 2, 26), "Data Sharing in Dense Matrix Multiplication (C = A × B)", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Comparing Required Input Footprints: 1-D Row Partitioning vs. 2-D Checkerboard Partitioning", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 1200
    p_h = 270

    # TOP SECTION: (a) 1-D Partitioning
    ty1 = 80
    draw.rounded_rectangle([40, ty1, 40 + p_w, ty1 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((60, ty1 + 18), "(a) One-Dimensional Row Partitioning of Output Matrix C (p = 16 Processes)", fill=CRIMSON, font=font_head, anchor="lt")
    draw.text((60, ty1 + 42), "Shaded process P5 computes Row Strip 5 of C by multiplying Row Strip 5 of A with ENTIRE Matrix B", fill=TEXT_MUTED, font=font_subhead, anchor="lt")

    # Matrices A, B, C for 1D
    box_s = 150
    gap = 40
    start_x = 70
    my = ty1 + 75

    # Matrix A (1D)
    draw.rectangle([start_x, my, start_x + box_s, my + box_s], fill=(255, 255, 255), outline=LINE_COLOR, width=2)
    draw.text((start_x + box_s // 2, my - 14), "Matrix A", fill=NAVY, font=font_badge, anchor="mm")
    # Shaded row strip 5
    strip_h = box_s / 16
    ay1 = my + 5 * strip_h
    draw.rectangle([start_x, ay1, start_x + box_s, ay1 + strip_h], fill=(186, 230, 253), outline=HIGHLIGHT_BLUE, width=1)
    draw.text((start_x + box_s + 12, ay1 + strip_h // 2), "Row strip 5", fill=HIGHLIGHT_BLUE, font=get_font(11, bold=True), anchor="lm")

    # Multiplication sign
    draw.text((start_x + box_s + gap // 2 + 25, my + box_s // 2), "×", fill=NAVY, font=font_math, anchor="mm")

    # Matrix B (1D) - COMPLETELY SHADED!
    bx = start_x + box_s + gap + 40
    draw.rectangle([bx, my, bx + box_s, my + box_s], fill=(254, 202, 202), outline=CRIMSON, width=2)
    draw.text((bx + box_s // 2, my - 14), "Matrix B (ALL REQUIRED!)", fill=CRIMSON, font=font_badge, anchor="mm")
    draw.text((bx + box_s // 2, my + box_s // 2), "100% of B Required\nby EVERY Process!\n(Volume = n²)", fill=CRIMSON, font=get_font(12, bold=True), anchor="mm")

    # Equals sign
    draw.text((bx + box_s + gap // 2 + 10, my + box_s // 2), "=", fill=NAVY, font=font_math, anchor="mm")

    # Matrix C (1D)
    cx = bx + box_s + gap + 20
    draw.rectangle([cx, my, cx + box_s, my + box_s], fill=(255, 255, 255), outline=LINE_COLOR, width=2)
    draw.text((cx + box_s // 2, my - 14), "Output Matrix C", fill=NAVY, font=font_badge, anchor="mm")
    for i in range(16):
        ry1 = my + i * strip_h
        fill_col = (186, 230, 253) if i == 5 else (255, 255, 255)
        out_col = HIGHLIGHT_BLUE if i == 5 else BOX_BORDER
        draw.rectangle([cx, ry1, cx + box_s, ry1 + strip_h], fill=fill_col, outline=out_col, width=1)
        if i % 3 == 0 or i == 5 or i == 15:
            draw.text((cx + 15, ry1 + strip_h // 2), f"P{i}", fill=NAVY if i != 5 else CRIMSON, font=get_font(9, bold=(i == 5)), anchor="mm")

    # 1D Takeaway card
    card_1d_x = cx + box_s + 35
    card_1d_w = 40 + p_w - card_1d_x - 15
    draw.rounded_rectangle([card_1d_x, my, card_1d_x + card_1d_w, my + box_s], radius=8, fill=(254, 242, 242), outline=CARD_BORDER_BAD, width=1)
    draw.text((card_1d_x + 14, my + 14), "1-D Partitioning Communication Bottleneck:", fill=CRIMSON, font=font_badge, anchor="lt")
    draw.line([card_1d_x + 14, my + 32, card_1d_x + card_1d_w - 14, my + 32], fill=BOX_BORDER, width=1)
    
    t1_notes = [
        "• Memory Footprint: Each process requires n²/p of A, n²/p of C, but ALL n² of B!",
        "• Comm Overhead: B must be fully broadcast or circulated -> Total Comm = O(n²).",
        "• Scalability Limit: Cannot scale beyond p ≤ n processors."
    ]
    ny = my + 42
    for note in t1_notes:
        draw.text((card_1d_x + 14, ny), note, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 28

    # BOTTOM SECTION: (b) 2-D Partitioning
    ty2 = ty1 + p_h + 15
    draw.rounded_rectangle([40, ty2, 40 + p_w, ty2 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((60, ty2 + 18), "(b) Two-Dimensional Checkerboard Partitioning of Output Matrix C (4 × 4 Mesh)", fill=CRIMSON, font=font_head, anchor="lt")
    draw.text((60, ty2 + 42), "Process P5 (row 1, col 1) requires ONLY row-block 1 of A and col-block 1 of B -> Drastic Communication Reduction!", fill=TEXT_MUTED, font=font_subhead, anchor="lt")

    my2 = ty2 + 75
    # Matrix A (2D)
    draw.rectangle([start_x, my2, start_x + box_s, my2 + box_s], fill=(255, 255, 255), outline=LINE_COLOR, width=2)
    draw.text((start_x + box_s // 2, my2 - 14), "Matrix A", fill=NAVY, font=font_badge, anchor="mm")
    # Row block 1 shaded
    block_h = box_s / 4
    ay2 = my2 + 1 * block_h
    draw.rectangle([start_x, ay2, start_x + box_s, ay2 + block_h], fill=(186, 230, 253), outline=HIGHLIGHT_BLUE, width=1)
    draw.text((start_x + box_s + 12, ay2 + block_h // 2), "Row block 1\n(Size n²/√p)", fill=HIGHLIGHT_BLUE, font=get_font(10, bold=True), anchor="lm")

    # Multiplication sign
    draw.text((start_x + box_s + gap // 2 + 25, my2 + box_s // 2), "×", fill=NAVY, font=font_math, anchor="mm")

    # Matrix B (2D) - VERTICAL STRIP SHADED!
    draw.rectangle([bx, my2, bx + box_s, my2 + box_s], fill=(255, 255, 255), outline=LINE_COLOR, width=2)
    draw.text((bx + box_s // 2, my2 - 14), "Matrix B", fill=NAVY, font=font_badge, anchor="mm")
    # Col block 1 shaded
    bx2_col = bx + 1 * block_h
    draw.rectangle([bx2_col, my2, bx2_col + block_h, my2 + box_s], fill=(254, 215, 170), outline=GOLD, width=1)
    draw.text((bx2_col + block_h // 2, my2 + box_s // 2), "Col block 1\n(Size n²/√p)", fill=(194, 65, 12), font=get_font(10, bold=True), anchor="mm")

    # Equals sign
    draw.text((bx + box_s + gap // 2 + 10, my2 + box_s // 2), "=", fill=NAVY, font=font_math, anchor="mm")

    # Matrix C (2D Checkerboard)
    draw.rectangle([cx, my2, cx + box_s, my2 + box_s], fill=(255, 255, 255), outline=LINE_COLOR, width=2)
    draw.text((cx + box_s // 2, my2 - 14), "Output Matrix C", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(4):
        for c in range(4):
            pid = r * 4 + c
            px = cx + c * block_h
            py = my2 + r * block_h
            is_p5 = (pid == 5)
            f_col = (186, 230, 253) if is_p5 else ((240, 253, 244) if (r + c) % 2 == 0 else (255, 255, 255))
            o_col = CRIMSON if is_p5 else BOX_BORDER
            draw.rectangle([px, py, px + block_h, py + block_h], fill=f_col, outline=o_col, width=2 if is_p5 else 1)
            draw.text((px + block_h // 2, py + block_h // 2), f"P{pid}", fill=CRIMSON if is_p5 else NAVY, font=get_font(11, bold=is_p5), anchor="mm")

    # 2D Takeaway card
    draw.rounded_rectangle([card_1d_x, my2, card_1d_x + card_1d_w, my2 + box_s], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((card_1d_x + 14, my2 + 14), "2-D Checkerboard Asymptotic Superiority:", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")
    draw.line([card_1d_x + 14, my2 + 32, card_1d_x + card_1d_w - 14, my2 + 32], fill=BOX_BORDER, width=1)

    t2_notes = [
        "• Memory Footprint: Each process needs only n²/√p of A and n²/√p of B!",
        "• Communication Overhead: Reduces volume from O(n²) down to O(n²/√p).",
        "• Asymptotic Speedup: Saves a factor of √p in network data transfer volume!",
        "• Scalability: Enables massive concurrency up to p ≤ n² processors."
    ]
    ny = my2 + 40
    for note in t2_notes:
        draw.text((card_1d_x + 14, ny), note, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 25

    img.save("extracted_images/lec19_dense_matrix_mult_data_sharing.png")
    print("Saved lec19_dense_matrix_mult_data_sharing.png")

# -------------------------------------------------------------
# 3. lec19_lu_factorization_imbalance.png
# Replicating Slide 5 & 6: 14 Tasks & Process Grid Load Imbalance
# -------------------------------------------------------------
def create_lu_factorization_imbalance():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_badge = get_font(14, bold=True)
    font_mono = get_font(13, bold=True)
    font_text = get_font(13.5, bold=False)

    draw.text((W // 2, 28), "LU Factorization: Task Decomposition & Severe Load Imbalance", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "3×3 Block Decomposition into 14 Tasks and the Failure of 2-D Block Mapping (Grama Sec 3.4.2)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: 14 Tasks in 3 Stages
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 108), "LU Decomposition into 14 Block Tasks (3×3 Block Matrix)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 132), "A = L · U Factorization: 3 sequential diagonal iterations", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    stages = [
        ("Iteration 1 (Eliminate Row 1 & Col 1): 9 Tasks", [
            ("T1:", "A1,1 -> L1,1 · U1,1 (Factor pivot block)"),
            ("T2, T3:", "L2,1 = A2,1 · U1,1⁻¹  ;  L3,1 = A3,1 · U1,1⁻¹ (Col solve)"),
            ("T4, T5:", "U1,2 = L1,1⁻¹ · A1,2  ;  U1,3 = L1,1⁻¹ · A1,3 (Row solve)"),
            ("T6..T9:", "Submatrix updates: A_ij = A_ij - L_i,1 · U_1,j (for i,j in {2,3})")
        ], (239, 246, 255), HIGHLIGHT_BLUE),

        ("Iteration 2 (Eliminate Row 2 & Col 2): 4 Tasks", [
            ("T10:", "A2,2 -> L2,2 · U2,2 (Factor second diagonal pivot)"),
            ("T11, T12:", "L3,2 = A3,2 · U2,2⁻¹  ;  U2,3 = L2,2⁻¹ · A2,3"),
            ("T13:", "Trailing update: A3,3 = A3,3 - L3,2 · U2,3")
        ], (254, 243, 199), GOLD),

        ("Iteration 3 (Final Pivot): 1 Task", [
            ("T14:", "A3,3 -> L3,3 · U3,3 (Factor final scalar/block pivot)")
        ], (240, 253, 244), HIGHLIGHT_GREEN)
    ]

    ty = 154
    for st_title, task_list, bg_c, bord_c in stages:
        box_h = 32 + len(task_list) * 24
        draw.rounded_rectangle([60, ty, 40 + p_w - 20, ty + box_h], radius=8, fill=bg_c, outline=bord_c, width=1)
        draw.text((75, ty + 10), st_title, fill=NAVY, font=font_badge, anchor="lt")
        draw.line([75, ty + 28, 40 + p_w - 35, ty + 28], fill=BOX_BORDER, width=1)
        
        curr_y = ty + 34
        for t_label, t_desc in task_list:
            draw.text((75, curr_y), t_label, fill=CRIMSON, font=get_font(13, bold=True), anchor="lt")
            draw.text((140, curr_y), t_desc, fill=TEXT_DARK, font=font_text, anchor="lt")
            curr_y += 24
        ty += box_h + 12

    # Left Callout: Work Shrinkage
    draw.rounded_rectangle([60, ty + 2, 40 + p_w - 20, 80 + p_h - 18], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, ty + 12), "The Shrinking Active Matrix Phenomenon:", fill=CRIMSON, font=font_badge, anchor="lt")
    draw.text((75, ty + 34), "Notice work drops from 9 tasks -> 4 tasks -> 1 task!", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((75, ty + 56), "The active subproblem shrinks toward bottom-right as elimination progresses.", fill=TEXT_MUTED, font=font_text, anchor="lt")

    # RIGHT PANEL: Block Mapping onto 3x3 Process Mesh
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 108), "Static Block Mapping onto 3×3 Process Mesh (P0..P8)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 132), "Process P_r,c owns block A_r+1, c+1 (Owner-Computes Rule)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 3x3 Grid
    gx = rx + (p_w - 270) // 2
    gy = 158
    cs = 90
    proc_tasks = [
        ("P0", "T1", 1),
        ("P3", "T4", 1),
        ("P6", "T5", 1),
        ("P1", "T2", 1),
        ("P4", "T6, T10", 2),
        ("P7", "T8, T12", 2),
        ("P2", "T3", 1),
        ("P5", "T7, T11", 2),
        ("P8", "T9, T13, T14", 3)
    ]
    # Replicating slide 6 table arrangement
    grid_layout = [
        [("P0", "T1"), ("P3", "T4"), ("P6", "T5")],
        [("P1", "T2"), ("P4", "T6, T10"), ("P7", "T8, T12")],
        [("P2", "T3"), ("P5", "T7, T11"), ("P8", "T9, T13, T14")]
    ]

    for r in range(3):
        for c in range(3):
            pname, tnames = grid_layout[r][c]
            x1 = gx + c * cs
            y1 = gy + r * cs
            # highlight P0 (bad idle) vs P8 (bottleneck)
            if pname == "P0":
                bg = (254, 242, 242)
                bcol = HIGHLIGHT_RED
            elif pname == "P8":
                bg = (254, 243, 199)
                bcol = GOLD
            else:
                bg = (255, 255, 255)
                bcol = LINE_COLOR
            draw.rectangle([x1, y1, x1 + cs, y1 + cs], fill=bg, outline=bcol, width=2 if pname in ["P0", "P8"] else 1)
            draw.text((x1 + cs // 2, y1 + 28), pname, fill=NAVY, font=get_font(18, bold=True), anchor="mm")
            draw.text((x1 + cs // 2, y1 + 58), tnames, fill=CRIMSON if pname == "P8" else TEXT_DARK, font=get_font(12, bold=True), anchor="mm")

    # Bottom Imbalance Analysis Card
    draw.rounded_rectangle([rx + 20, 455, rx + p_w - 20, 80 + p_h - 18], radius=8, fill=(254, 242, 242), outline=CARD_BORDER_BAD, width=1)
    draw.text((rx + 35, 468), "Failure of 2-D Block Mapping in Triangular Elimination:", fill=CRIMSON, font=font_badge, anchor="lt")
    draw.line([rx + 35, 488, rx + p_w - 35, 488], fill=BOX_BORDER, width=1)

    fail_points = [
        ("• P0 Idling:", "P0 finishes T1 in Step 1 and sits IDLE for the entire rest of execution!"),
        ("• P8 Bottleneck:", "P8 must execute T9, T13, and T14 sequentially, becoming the serial critical path."),
        ("• Processor Utilization:", "Average processor utilization plummets below 50% as matrix size grows!"),
        ("• Solution:", "Block-Cyclic Distribution (interleaving blocks cyclically across processes).")
    ]
    ny = 496
    for lbl, desc in fail_points:
        draw.text((rx + 35, ny), lbl, fill=NAVY, font=get_font(13, bold=True), anchor="lt")
        pw = get_font(13, bold=True).getbbox(lbl + " ")[2]
        draw.text((rx + 35 + pw, ny), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 25

    img.save("extracted_images/lec19_lu_factorization_imbalance.png")
    print("Saved lec19_lu_factorization_imbalance.png")

# -------------------------------------------------------------
# 4. lec19_block_cyclic_distribution.png
# Replicating Slide 8: 1-D & 2-D Block-Cyclic Distribution
# -------------------------------------------------------------
def create_block_cyclic_distribution():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_badge = get_font(14, bold=True)
    font_mono = get_font(14, bold=True)
    font_text = get_font(13, bold=False)

    draw.text((W // 2, 28), "1-D and 2-D Block-Cyclic Distributions", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Eliminating Load Imbalance in Triangular Elimination via Wraparound Mapping (Grama Sec 3.4.2)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: (a) 1-D Block-Cyclic
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 108), "(a) 1-D Row Block-Cyclic Distribution (b = 2 Rows, p = 4)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 132), "16 rows partitioned into 8 blocks of 2 rows each -> Distributed cyclically to P0..P3", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 1D Grid visualization
    ox1 = 60
    oy1 = 160
    grid_w = 320
    grid_h = 240
    row_h = grid_h / 16

    proc_colors = [
        (239, 246, 255),  # P0 Light Blue
        (254, 243, 199),  # P1 Light Yellow
        (240, 253, 244),  # P2 Light Green
        (254, 242, 242)   # P3 Light Red
    ]

    for blk_idx in range(8):
        proc_id = blk_idx % 4
        y_top = oy1 + blk_idx * (2 * row_h)
        draw.rectangle([ox1, y_top, ox1 + grid_w, y_top + 2 * row_h], fill=proc_colors[proc_id], outline=LINE_COLOR, width=1)
        draw.text((ox1 + grid_w // 2, y_top + row_h), f"Block {blk_idx}  ->  Process P{proc_id} (Rows {blk_idx*2}, {blk_idx*2+1})", fill=NAVY, font=font_mono, anchor="mm")

    # Legend next to 1D grid
    lx = ox1 + grid_w + 20
    draw.text((lx, oy1 + 10), "Block-to-Process Mapping:", fill=NAVY, font=font_badge, anchor="lt")
    for pid in range(4):
        py = oy1 + 40 + pid * 45
        draw.rounded_rectangle([lx, py, lx + 160, py + 34], radius=6, fill=proc_colors[pid], outline=LINE_COLOR, width=1)
        draw.text((lx + 12, py + 17), f"Process P{pid}:", fill=CRIMSON, font=get_font(13, bold=True), anchor="lm")
        draw.text((lx + 90, py + 17), f"Blk {pid}, {pid+4}", fill=NAVY, font=get_font(12, bold=True), anchor="lm")

    # 1D Bottom notes
    draw.rounded_rectangle([60, 440, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 452), "Why 1-D Block-Cyclic Resolves LU Imbalance:", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([75, 472, 40 + p_w - 35, 472], fill=BOX_BORDER, width=1)
    notes_1d = [
        "• Uniform Row Spreading: Every process owns rows from the top, middle, and bottom.",
        "• Continuous Workload: When top rows are eliminated, P0 still owns rows in Block 4!",
        "• No Processor Left Idle: All 4 processes stay active until the final block elimination.",
        "• Block Size Trade-off: b = 1 is pure cyclic; b > 1 preserves spatial cache locality."
    ]
    ny = 482
    for n in notes_1d:
        draw.text((75, ny), n, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 26

    # RIGHT PANEL: (b) 2-D Block-Cyclic
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 108), "(b) 2-D Block-Cyclic Distribution (4×4 Blocks on 2×2 Mesh)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 132), "Matrix blocked into 16 blocks (size 4×4), mapped onto 2×2 process grid (P0..P3)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 2D Grid
    gx2 = rx + 60
    gy2 = 160
    cw = 65
    mesh_layout = [
        [0, 1, 0, 1],
        [2, 3, 2, 3],
        [0, 1, 0, 1],
        [2, 3, 2, 3]
    ]
    for r in range(4):
        for c in range(4):
            pid = mesh_layout[r][c]
            bx = gx2 + c * cw
            by = gy2 + r * cw
            draw.rectangle([bx, by, bx + cw, by + cw], fill=proc_colors[pid], outline=LINE_COLOR, width=1)
            draw.text((bx + cw // 2, by + cw // 2), f"P{pid}", fill=NAVY, font=get_font(16, bold=True), anchor="mm")

    # Legend next to 2D grid
    lx2 = gx2 + 4 * cw + 25
    draw.text((lx2, gy2 + 10), "2-D Periodic Tiles:", fill=NAVY, font=font_badge, anchor="lt")
    draw.text((lx2, gy2 + 38), "The 2×2 process grid:", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((lx2 + 15, gy2 + 60), "[ P0   P1 ]", fill=CRIMSON, font=font_mono, anchor="lt")
    draw.text((lx2 + 15, gy2 + 82), "[ P2   P3 ]", fill=CRIMSON, font=font_mono, anchor="lt")
    draw.text((lx2, gy2 + 115), "is tiled periodically\nacross both rows &\ncolumns of the matrix!", fill=TEXT_MUTED, font=font_text)

    # 2D Bottom notes
    draw.rounded_rectangle([rx + 20, 440, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((rx + 35, 452), "ScaLAPACK Gold Standard: 2-D Block-Cyclic:", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")
    draw.line([rx + 35, 472, rx + p_w - 35, 472], fill=BOX_BORDER, width=1)
    notes_2d = [
        "• Combines Best of Both Worlds: 2-D surface-to-volume ratio + cyclic load balance.",
        "• High BLAS-3 Efficiency: Tuning block size b (e.g. 32 to 64) achieves peak GEMM FLOPS.",
        "• Minimum Communication: Reduces network messages by factor √p vs 1-D block-cyclic.",
        "• LINPACK Benchmark: The universal layout used by TOP500 supercomputing rankings!"
    ]
    ny = 482
    for n in notes_2d:
        draw.text((rx + 35, ny), n, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 26

    img.save("extracted_images/lec19_block_cyclic_distribution.png")
    print("Saved lec19_block_cyclic_distribution.png")

# -------------------------------------------------------------
# 5. lec19_randomized_block_cyclic.png
# Replicating Slide 9 & 10: Banded Sparse Matrix Randomization
# Based on Grama, Gupta, Karypis, Kumar (2nd Ed.), Fig. 3.31 & 3.33
# -------------------------------------------------------------
def create_randomized_block_cyclic():
    import numpy as np
    W, H = SLIDE_W, 680
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Typography
    font_title = get_font(23, bold=True)
    font_sub = get_font(13.5, bold=False)
    font_card_head = get_font(14.5, bold=True)
    font_card_sub = get_font(11.5, bold=False)
    font_badge = get_font(11, bold=True)
    font_grid_head = get_font(12, bold=True)
    font_grid_sub = get_font(10, bold=False)
    font_mono = get_font(11, bold=True)
    font_mono_sm = get_font(9.5, bold=True)
    font_bullet = get_font(11, bold=False)
    font_bullet_bold = get_font(11, bold=True)

    # 1. Header Bar
    draw.text((W // 2, 22), "Structured Sparse Matrix Load Balancing: Block-Cyclic vs. Randomized Mapping", fill=(15, 23, 42), font=font_title, anchor="mm")
    draw.text((W // 2, 45), "Based on Grama, Gupta, Karypis, Kumar — 'Introduction to Parallel Computing' (2nd Ed.), Section 3.4.1, Figures 3.31 & 3.33 (pp. 129–130)", fill=(71, 85, 105), font=font_sub, anchor="mm")

    # Data setup
    # Original 16x16 sparse matrix A from Grama Fig 3.31(a)
    M_a = np.zeros((16, 16), dtype=int)
    nz_ranges = [
        (0, 0, 3), (1, 0, 3), (2, 0, 6), (3, 0, 6),
        (4, 2, 6), (5, 2, 6), (6, 2, 8), (7, 5, 8),
        (8, 5, 8), (9, 5, 9), (10, 8, 11), (11, 9, 11),
        (12, 9, 13), (13, 9, 15), (14, 11, 15), (15, 13, 15)
    ]
    for r, c1, c2 in nz_ranges:
        M_a[r, c1:c2+1] = 1

    # Permutations from Grama Fig 3.33(b)
    pi = [6, 10, 14, 1, 5, 13, 0, 9, 3, 15, 4, 11, 7, 12, 2, 8]
    sigma = [10, 6, 4, 0, 11, 3, 1, 8, 7, 14, 2, 13, 9, 5, 15, 12]

    # Permuted matrix A'
    M_perm = np.zeros((16, 16), dtype=int)
    for r in range(16):
        for c in range(16):
            M_perm[r, c] = M_a[pi[r], sigma[c]]

    # Block counts for original matrix (4x4 process blocks)
    orig_counts = np.zeros((4, 4), dtype=int)
    for pr in range(4):
        for pc in range(4):
            orig_counts[pr, pc] = M_a[pr*4:(pr+1)*4, pc*4:(pc+1)*4].sum()

    # Block counts for permuted matrix (Grama Fig 3.33c)
    perm_counts = np.zeros((4, 4), dtype=int)
    for pr in range(4):
        for pc in range(4):
            perm_counts[pr, pc] = M_perm[pr*4:(pr+1)*4, pc*4:(pc+1)*4].sum()

    card_y = 65
    card_w = 595
    card_h = 598
    gap_x = 30
    x_left = 30
    x_right = x_left + card_w + gap_x

    # =========================================================================
    # LEFT PANEL: FIGURE 3.31 - PATHOLOGICAL LOAD IMBALANCE
    # =========================================================================
    draw.rounded_rectangle([x_left, card_y, x_left + card_w, card_y + card_h], radius=10, fill=(255, 255, 255), outline=(239, 68, 68), width=2)
    
    # Left Card Header Badge
    draw.rounded_rectangle([x_left + 16, card_y + 14, x_left + 420, card_y + 36], radius=6, fill=(254, 242, 242), outline=(252, 165, 165), width=1)
    draw.text((x_left + 24, card_y + 25), "GRAMA FIG. 3.31: 2-D BLOCK-CYCLIC FAILURE", fill=(185, 28, 28), font=font_badge, anchor="lm")
    draw.text((x_left + 16, card_y + 52), "Pathological Work Imbalance on Banded Sparse Matrix (p = 16)", fill=(15, 23, 42), font=font_card_head, anchor="lt")
    draw.text((x_left + 16, card_y + 73), "Structural periodicity of non-zero band synchronizes with process mesh stride", fill=(100, 116, 139), font=font_card_sub, anchor="lt")

    # Matrices inside Left Panel
    m_size = 176
    cs = m_size / 16.0
    gx1 = x_left + 36
    gy1 = card_y + 114

    draw.text((gx1 + m_size // 2, gy1 - 18), "(a) Sparse Banded Matrix A (16 × 16)", fill=(15, 23, 42), font=font_grid_head, anchor="mm")
    draw.text((gx1 + m_size // 2, gy1 - 5), "79 Nonzeros along Stepped Diagonal (Shaded)", fill=(100, 116, 139), font=font_grid_sub, anchor="mm")

    # Draw matrix A cells
    for r in range(16):
        for c in range(16):
            cx = gx1 + c * cs
            cy = gy1 + r * cs
            if M_a[r, c]:
                draw.rectangle([cx, cy, cx + cs, cy + cs], fill=(71, 85, 105), outline=(148, 163, 184), width=1)
            else:
                draw.rectangle([cx, cy, cx + cs, cy + cs], fill=(255, 255, 255), outline=(241, 245, 249), width=1)

    # 4x4 Process Block Super-Grid over Matrix A
    bs = m_size / 4.0
    for br in range(4):
        for bc in range(4):
            bx = gx1 + bc * bs
            by = gy1 + br * bs
            is_diag = (br == bc)
            border_col = (220, 38, 38) if is_diag else (203, 213, 225)
            border_w = 2 if is_diag else 1
            draw.rectangle([bx, by, bx + bs, by + bs], outline=border_col, width=border_w)

    # Arrow from (a) to (b)
    arrow_x = gx1 + m_size + 18
    arrow_y = gy1 + m_size // 2
    draw.line([arrow_x, arrow_y, arrow_x + 38, arrow_y], fill=(185, 28, 28), width=2)
    draw.polygon([(arrow_x + 40, arrow_y), (arrow_x + 32, arrow_y - 5), (arrow_x + 32, arrow_y + 5)], fill=(185, 28, 28))
    draw.text((arrow_x + 20, arrow_y - 12), "Map to", fill=(185, 28, 28), font=font_mono_sm, anchor="mm")
    draw.text((arrow_x + 20, arrow_y + 12), "4×4 Mesh", fill=(185, 28, 28), font=font_mono_sm, anchor="mm")

    # Grid 2: Process Grid (b)
    gx2 = gx1 + m_size + 68
    draw.text((gx2 + m_size // 2, gy1 - 18), "(b) Process Grid (4 × 4 Mesh, p = 16)", fill=(15, 23, 42), font=font_grid_head, anchor="mm")
    draw.text((gx2 + m_size // 2, gy1 - 5), "Assigned Non-zero Elements per Process", fill=(100, 116, 139), font=font_grid_sub, anchor="mm")

    for pr in range(4):
        for pc in range(4):
            pid = pr * 4 + pc
            cx = gx2 + pc * bs
            cy = gy1 + pr * bs
            cnt = orig_counts[pr, pc]
            is_diag = (pr == pc)
            is_idle = (cnt == 0)

            if is_diag:
                bg = (254, 226, 226) # light red
                out = (220, 38, 38)
                txt_col = (185, 28, 28)
            elif is_idle:
                bg = (248, 250, 252) # slate light
                out = (203, 213, 225)
                txt_col = (148, 163, 184)
            else:
                bg = (255, 255, 255)
                out = (203, 213, 225)
                txt_col = (51, 65, 85)

            draw.rectangle([cx, cy, cx + bs, cy + bs], fill=bg, outline=out, width=2 if (is_diag or pid == 12) else 1)
            draw.text((cx + bs // 2, cy + bs // 2 - 9), f"P_{{{pid}}}", fill=txt_col, font=font_mono, anchor="mm")
            
            if is_diag:
                draw.text((cx + bs // 2, cy + bs // 2 + 9), f"{cnt} nz", fill=(185, 28, 28), font=get_font(10.5, bold=True), anchor="mm")
            elif is_idle:
                draw.text((cx + bs // 2, cy + bs // 2 + 9), "0 (IDLE)", fill=(220, 38, 38) if pid == 12 else (148, 163, 184), font=get_font(9, bold=True), anchor="mm")
            else:
                draw.text((cx + bs // 2, cy + bs // 2 + 9), f"{cnt} nz", fill=txt_col, font=get_font(10, bold=False), anchor="mm")

    # Highlighting Callout for P12
    p12_x = gx2
    p12_y = gy1 + 3 * bs
    draw.rectangle([p12_x, p12_y, p12_x + bs, p12_y + bs], outline=(220, 38, 38), width=3)

    # Explanation card below Left Panel
    note_box_y = gy1 + m_size + 24
    draw.rounded_rectangle([x_left + 16, note_box_y, x_left + card_w - 16, card_y + card_h - 16], radius=8, fill=(254, 242, 242), outline=(252, 165, 165), width=1)
    
    draw.text((x_left + 24, note_box_y + 12), "Diagnostic Findings from Grama et al. (Figure 3.31):", fill=(185, 28, 28), font=font_badge, anchor="lt")
    draw.line([x_left + 24, note_box_y + 30, x_left + card_w - 24, note_box_y + 30], fill=(252, 165, 165), width=1)

    bullets_left = [
        ("Periodicity Resonance", "Non-zero band falls with stride matching the process mesh."),
        ("Catastrophic Imbalance", "P0(16), P5(13), P10(10), P15(13) take 52/79 nonzeros (66% of all work!)."),
        ("Severe Starvation", "6 out of 16 processes (P2, P3, P7, P8, P11, P12, P13) receive ZERO work!"),
        ("Grama Quote (p. 129)", "\"In fact some processes, like P12, will not get any work.\"")
    ]
    by = note_box_y + 40
    for title, desc in bullets_left:
        draw.text((x_left + 24, by), f"• {title}: ", fill=(185, 28, 28), font=font_bullet_bold, anchor="lt")
        tw = font_bullet_bold.getbbox(f"• {title}: ")[2]
        draw.text((x_left + 24 + tw, by), desc, fill=(15, 23, 42), font=font_bullet, anchor="lt")
        by += 24

    draw.text((x_left + 24, card_y + card_h - 24), "Citation: Grama, Gupta, Karypis, Kumar — Introduction to Parallel Computing (2nd Ed.), Fig. 3.31 (p. 129)", fill=(156, 163, 175), font=get_font(9.5, bold=False), anchor="lb")

    # =========================================================================
    # RIGHT PANEL: FIGURE 3.33 - 2-D RANDOMIZED BLOCK DISTRIBUTION
    # =========================================================================
    draw.rounded_rectangle([x_right, card_y, x_right + card_w, card_y + card_h], radius=10, fill=(255, 255, 255), outline=(34, 197, 94), width=2)
    
    # Right Card Header Badge
    draw.rounded_rectangle([x_right + 16, card_y + 14, x_right + 440, card_y + 36], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.text((x_right + 24, card_y + 25), "GRAMA FIG. 3.33: 2-D RANDOMIZED DISTRIBUTION", fill=(21, 128, 61), font=font_badge, anchor="lm")
    draw.text((x_right + 16, card_y + 52), "Uniform Load Balance Achieved via Random Permutations (p = 16)", fill=(15, 23, 42), font=font_card_head, anchor="lt")
    draw.text((x_right + 16, card_y + 73), "Decouples data matrix structure from process topology via random index bijections", fill=(100, 116, 139), font=font_card_sub, anchor="lt")

    # Matrices inside Right Panel
    gx3 = x_right + 36
    draw.text((gx3 + m_size // 2, gy1 - 18), "(b) Permuted Matrix A' (16 × 16)", fill=(15, 23, 42), font=font_grid_head, anchor="mm")
    draw.text((gx3 + m_size // 2, gy1 - 5), "A'[i, j] = A[π(i), σ(j)] (Non-zeros Dispersed)", fill=(100, 116, 139), font=font_grid_sub, anchor="mm")

    # Draw permuted matrix cells
    for r in range(16):
        for c in range(16):
            cx = gx3 + c * cs
            cy = gy1 + r * cs
            if M_perm[r, c]:
                draw.rectangle([cx, cy, cx + cs, cy + cs], fill=(14, 165, 233), outline=(125, 211, 252), width=1)
            else:
                draw.rectangle([cx, cy, cx + cs, cy + cs], fill=(255, 255, 255), outline=(241, 245, 249), width=1)

    # 4x4 Process Block Super-Grid over Permuted Matrix
    for br in range(4):
        for bc in range(4):
            bx = gx3 + bc * bs
            by = gy1 + br * bs
            draw.rectangle([bx, by, bx + bs, by + bs], outline=(34, 197, 94), width=1)

    # Arrow from (b) to (c)
    arrow2_x = gx3 + m_size + 18
    arrow2_y = gy1 + m_size // 2
    draw.line([arrow2_x, arrow2_y, arrow2_x + 38, arrow2_y], fill=(22, 163, 74), width=2)
    draw.polygon([(arrow2_x + 40, arrow2_y), (arrow2_x + 32, arrow2_y - 5), (arrow2_x + 32, arrow2_y + 5)], fill=(22, 163, 74))
    draw.text((arrow2_x + 20, arrow2_y - 12), "Blocks to", fill=(22, 163, 74), font=font_mono_sm, anchor="mm")
    draw.text((arrow2_x + 20, arrow2_y + 12), "Processors", fill=(22, 163, 74), font=font_mono_sm, anchor="mm")

    # Grid 4: Process Grid (c)
    gx4 = gx3 + m_size + 68
    draw.text((gx4 + m_size // 2, gy1 - 18), "(c) Uniform Workload Grid (4 × 4 Mesh)", fill=(15, 23, 42), font=font_grid_head, anchor="mm")
    draw.text((gx4 + m_size // 2, gy1 - 5), "Grama Fig. 3.33(c) Exact Nonzeros per Process", fill=(100, 116, 139), font=font_grid_sub, anchor="mm")

    for pr in range(4):
        for pc in range(4):
            pid = pr * 4 + pc
            cx = gx4 + pc * bs
            cy = gy1 + pr * bs
            cnt = perm_counts[pr, pc]

            bg = (240, 253, 244) # clean light green
            out = (34, 197, 94)
            txt_col = (21, 128, 61)

            draw.rectangle([cx, cy, cx + bs, cy + bs], fill=bg, outline=out, width=2)
            draw.text((cx + bs // 2, cy + bs // 2 - 9), f"P_{{{pid}}}", fill=(15, 23, 42), font=font_mono, anchor="mm")
            draw.text((cx + bs // 2, cy + bs // 2 + 9), f"{cnt} nz", fill=txt_col, font=get_font(11, bold=True), anchor="mm")

    # Explanation card below Right Panel
    draw.rounded_rectangle([x_right + 16, note_box_y, x_right + card_w - 16, card_y + card_h - 16], radius=8, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    
    draw.text((x_right + 24, note_box_y + 12), "Mathematical Proof & Results from Grama et al. (Figure 3.33):", fill=(21, 128, 61), font=font_badge, anchor="lt")
    draw.line([x_right + 24, note_box_y + 30, x_right + card_w - 24, note_box_y + 30], fill=(187, 247, 208), width=1)

    bullets_right = [
        ("Row Permutation π", "[6, 10, 14, 1, 5, 13, 0, 9, 3, 15, 4, 11, 7, 12, 2, 8]"),
        ("Col Permutation σ", "[10, 6, 4, 0, 11, 3, 1, 8, 7, 14, 2, 13, 9, 5, 15, 12]"),
        ("Near-Perfect Balance", "Work per process tightly bounded: 4 to 7 nonzeros (mean = 4.94)."),
        ("100% Core Utilization", "Zero idle processors (vs. 6 starving processors in Fig 3.31!).")
    ]
    by = note_box_y + 40
    for title, desc in bullets_right:
        draw.text((x_right + 24, by), f"• {title}: ", fill=(21, 128, 61), font=font_bullet_bold, anchor="lt")
        tw = font_bullet_bold.getbbox(f"• {title}: ")[2]
        draw.text((x_right + 24 + tw, by), desc, fill=(15, 23, 42), font=font_bullet, anchor="lt")
        by += 24

    draw.text((x_right + 24, card_y + card_h - 24), "Citation: Grama, Gupta, Karypis, Kumar — Introduction to Parallel Computing (2nd Ed.), Fig. 3.33 (p. 130)", fill=(156, 163, 175), font=get_font(9.5, bold=False), anchor="lb")

    img.save("extracted_images/lec19_randomized_block_cyclic.png", dpi=(150, 150))
    print("Saved lec19_randomized_block_cyclic.png")

# -------------------------------------------------------------
# 6. lec19_dynamic_load_balancing_schemes.png
# Replicating Slide 11, 12, 13: Centralized vs Distributed Dynamic Mapping
# -------------------------------------------------------------
def create_dynamic_load_balancing_schemes():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_badge = get_font(14, bold=True)
    font_q_title = get_font(13.5, bold=True)
    font_text = get_font(13, bold=False)

    draw.text((W // 2, 28), "Dynamic Load Balancing: Centralized vs. Distributed Schemes", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Comparing Master-Worker Queue Scheduling with Distributed Peer-to-Peer Load Balancing (Grama Sec 3.5)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Centralized Master-Worker
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 108), "Centralized Dynamic Mapping (Master-Worker)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 132), "Designated master coordinates global task queue; workers request tasks", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Diagram of Master + Workers + Chunk Scheduling
    mx = 40 + p_w // 2
    my = 160
    draw.rounded_rectangle([mx - 150, my, mx + 150, my + 48], radius=8, fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
    draw.text((mx, my + 14), "Master Process (P0)", fill=NAVY, font=font_badge, anchor="mm")
    draw.text((mx, my + 32), "Global Task Pool / Task Queue", fill=CRIMSON, font=get_font(12, bold=True), anchor="mm")

    # 4 Workers
    wy = 250
    w_xs = [80, 200, 320, 440]
    for i in range(4):
        wx = w_xs[i]
        draw.rounded_rectangle([wx, wy, wx + 80, wy + 42], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=2)
        draw.text((wx + 40, wy + 14), f"Worker {i+1}", fill=NAVY, font=font_badge, anchor="mm")
        draw.text((wx + 40, wy + 28), f"Chunk K_t", fill=TEXT_MUTED, font=get_font(10), anchor="mm")
        draw_arrow(draw, mx - 90 + i * 60, my + 48, wx + 40, wy, color=HIGHLIGHT_BLUE, width=2)

    # Chunk Scheduling Box
    draw.rounded_rectangle([60, 315, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 328), "Chunk Scheduling & Guided Self-Scheduling (GSS):", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([75, 348, 40 + p_w - 35, 348], fill=BOX_BORDER, width=1)

    c_points = [
        ("• Fixed Chunk Dilemma:", "Large K causes severe tail idling; K = 1 overwhelms master with lock contention."),
        ("• Guided Self-Scheduling:", "Dynamically shrinks chunk size proportionally to remaining work:"),
        ("  Formula:", "K_t = ceil( R_t / p )  (where R_t is remaining tasks, p is active workers)"),
        ("• Geometric Reduction:", "Dispatches 50% of remaining work across the first p worker requests!"),
        ("• Tail Optimization:", "Chunk sizes smoothly taper down to K = 1 near the end for perfect tail balance."),
        ("• Scalability Bottleneck:", "Central master serializes as p > 64 -> Mandates distributed dynamic mapping.")
    ]
    ny = 358
    for lbl, desc in c_points:
        draw.text((75, ny), lbl, fill=CRIMSON if "Formula" in lbl or "Bottleneck" in lbl else NAVY, font=get_font(12.5, bold=True), anchor="lt")
        pw = get_font(12.5, bold=True).getbbox(lbl + " ")[2]
        draw.text((75 + pw, ny), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 25

    # RIGHT PANEL: Distributed Dynamic Mapping & 4 Questions
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 108), "Distributed Dynamic Mapping (Grama Sec 3.5.2)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 132), "No master bottleneck; peer processes coordinate load balancing locally", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # The 4 Critical Questions
    questions = [
        ("1. How are senders and receivers paired together?",
         "• Global Random: Victim chosen uniformly at random (robust, simple).\n"
         "• Nearest Neighbor: Processes exchange load only along topological mesh/ring edges.\n"
         "• Dimension Exchange: Systematically balance along hypercube dimensions d = 0..k-1."),

        ("2. Who initiates the work transfer?",
         "• Sender-Initiated: Overloaded process (Queue > L_high) pushes work to underloaded peers.\n"
         "• Receiver-Initiated (Work Stealing): Starving worker (Queue < L_low) pulls from busy peers.\n"
         "• Asymptotic Rule: Sender-initiated excels at light load; Receiver-initiated excels at heavy load!"),

        ("3. How much work is transferred at each step?",
         "• Half Remaining Work (ΔW = W_local / 2): Equalizes load between pair in 1 transfer.\n"
         "• Single Coarsest Task: Stealing highest ancestor task minimizes future communication."),

        ("4. When is a transfer triggered?",
         "• Threshold Trigger: Queue size crosses upper bound L_high or lower bound L_low.\n"
         "• Starvation Trigger: Worker deque becomes completely empty (pure Work Stealing).")
    ]

    qy = 155
    for q_title, q_desc in questions:
        draw.rounded_rectangle([rx + 20, qy, rx + p_w - 20, qy + 112], radius=6, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
        draw.text((rx + 34, qy + 8), q_title, fill=NAVY, font=font_q_title, anchor="lt")
        draw.line([rx + 34, qy + 26, rx + p_w - 34, qy + 26], fill=(187, 247, 208), width=1)
        
        lines = q_desc.split("\n")
        cy = qy + 32
        for line in lines:
            draw.text((rx + 34, cy), line, fill=TEXT_DARK, font=get_font(11.5, bold=False), anchor="lt")
            cy += 18
        qy += 122

    img.save("extracted_images/lec19_dynamic_load_balancing_schemes.png")
    print("Saved lec19_dynamic_load_balancing_schemes.png")

if __name__ == "__main__":
    create_block_array_higher_dims()
    create_dense_matrix_mult_data_sharing()
    create_lu_factorization_imbalance()
    create_block_cyclic_distribution()
    create_randomized_block_cyclic()
    create_dynamic_load_balancing_schemes()
    print("All Lecture 19 images generated successfully!")
