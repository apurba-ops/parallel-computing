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
CARD_BG_BLUE = (239, 246, 255)
CARD_BORDER_BLUE = (191, 219, 254)

def get_font(size, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf"
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

# -------------------------------------------------------------
# 1. lec17_recursive_decomp_min.png
# Recursive Decomposition: Divide-and-Conquer Paradigm & Reduction DAG
# -------------------------------------------------------------
def create_recursive_decomp_min():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_mono = get_font(14, bold=True)
    font_badge = get_font(13, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 28), "Recursive Decomposition: Divide-and-Conquer Paradigm & Reduction DAG", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Subproblems solved concurrently on separate threads/processes, then merged up the recursion tree", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Parallel Quicksort Tree
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Case 1: Parallel Quicksort Decomposition", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Pivot partition yields disjoint left & right sublists for concurrent sorting", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Quicksort tree levels
    # Level 0 (Root array)
    rx, ry = 40 + p_w // 2, 180
    root_arr = [5, 12, 11, 1, 10, 6, 8, 3, 7, 4, 9, 2]
    bw = 36
    start_x = rx - (len(root_arr) * bw) // 2
    for i, val in enumerate(root_arr):
        bg = (254, 243, 199) if val == 5 else (255, 255, 255)
        border = GOLD if val == 5 else BOX_BORDER
        draw.rectangle([start_x + i * bw, ry - 14, start_x + (i + 1) * bw, ry + 14], fill=bg, outline=border, width=1)
        draw.text((start_x + i * bw + bw // 2, ry), str(val), fill=CRIMSON if val == 5 else TEXT_DARK, font=font_mono, anchor="mm")
    draw.text((start_x - 10, ry), "Array:", fill=TEXT_MUTED, font=font_badge, anchor="rm")
    draw.text((start_x + len(root_arr) * bw + 10, ry), "Pivot = 5", fill=GOLD, font=font_badge, anchor="lm")

    # Level 1 Sublists
    y_l1 = 260
    left_arr = [1, 3, 4, 2]
    right_arr = [12, 11, 10, 6, 8, 7, 9]
    # Draw branches
    draw_arrow(draw, rx - 60, ry + 16, rx - 140, y_l1 - 16, color=NAVY, width=2)
    draw_arrow(draw, rx + 60, ry + 16, rx + 140, y_l1 - 16, color=NAVY, width=2)

    # Left box
    lx = rx - 150
    start_lx = lx - (len(left_arr) * bw) // 2
    for i, val in enumerate(left_arr):
        draw.rectangle([start_lx + i * bw, y_l1 - 14, start_lx + (i + 1) * bw, y_l1 + 14], fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=1)
        draw.text((start_lx + i * bw + bw // 2, y_l1), str(val), fill=NAVY, font=font_mono, anchor="mm")
    draw.text((lx, y_l1 + 22), "Task 1: Subproblem < 5", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="mm")

    # Right box
    right_x = rx + 150
    start_rx = right_x - (len(right_arr) * bw) // 2
    for i, val in enumerate(right_arr):
        draw.rectangle([start_rx + i * bw, y_l1 - 14, start_rx + (i + 1) * bw, y_l1 + 14], fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=1)
        draw.text((start_rx + i * bw + bw // 2, y_l1), str(val), fill=NAVY, font=font_mono, anchor="mm")
    draw.text((right_x, y_l1 + 22), "Task 2: Subproblem > 5", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="mm")

    # Level 2 Sublists
    y_l2 = 360
    # Left split: [1, 2] and [3, 4]
    draw_arrow(draw, lx - 40, y_l1 + 32, lx - 70, y_l2 - 16, color=NAVY, width=1)
    draw_arrow(draw, lx + 40, y_l1 + 32, lx + 70, y_l2 - 16, color=NAVY, width=1)
    for off, sub in [(-70, [1, 2]), (70, [3, 4])]:
        sx = lx + off - (len(sub) * bw) // 2
        for i, val in enumerate(sub):
            draw.rectangle([sx + i * bw, y_l2 - 12, sx + (i + 1) * bw, y_l2 + 12], fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=1)
            draw.text((sx + i * bw + bw // 2, y_l2), str(val), fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Right split: [6, 7, 8] and [10, 11, 12]
    draw_arrow(draw, right_x - 50, y_l1 + 32, right_x - 70, y_l2 - 16, color=NAVY, width=1)
    draw_arrow(draw, right_x + 50, y_l1 + 32, right_x + 70, y_l2 - 16, color=NAVY, width=1)
    for off, sub in [(-70, [6, 7, 8]), (70, [10, 11, 12])]:
        sx = right_x + off - (len(sub) * bw) // 2
        for i, val in enumerate(sub):
            draw.rectangle([sx + i * bw, y_l2 - 12, sx + (i + 1) * bw, y_l2 + 12], fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=1)
            draw.text((sx + i * bw + bw // 2, y_l2), str(val), fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Quicksort properties card
    draw.rounded_rectangle([60, 430, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    qs_bullets = [
        ("Concurrency Generation:", "Dynamic at runtime as subproblems are spawned."),
        ("Serial Bottleneck:", "Initial root partition of n elements is inherently sequential."),
        ("Concurrency Bound:", "Degrees of concurrency doubles at each recursion level 1, 2, 4, 8..."),
        ("Work & Span:", "Work = O(n log n), Span = O(n) without parallel partitioning.")
    ]
    by = 445
    for title, desc in qs_bullets:
        draw.text((75, by), f"• {title}", fill=NAVY, font=font_badge, anchor="lt")
        draw.text((250, by), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        by += 26

    # RIGHT PANEL: Recursive Min DAG
    rx_panel = 40 + p_w + 40
    draw.rounded_rectangle([rx_panel, 80, rx_panel + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx_panel + p_w // 2, 110), "Case 2: Recursive Min / Reduction DAG", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx_panel + p_w // 2, 134), "Finding min in {4, 9, 1, 7, 8, 11, 2, 12} via divide-and-conquer tree", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Tree of min operations
    # Leaf Level: 4 tasks: min(4,9)=4, min(1,7)=1, min(8,11)=8, min(2,12)=2
    leaf_nodes = [
        ("min(4,9)", "4"),
        ("min(1,7)", "1"),
        ("min(8,11)", "8"),
        ("min(2,12)", "2")
    ]
    leaf_y = 380
    leaf_xs = [rx_panel + 75, rx_panel + 215, rx_panel + 365, rx_panel + 505]
    nw, nh = 96, 36

    for i, (expr, res) in enumerate(leaf_nodes):
        x = leaf_xs[i]
        draw.rounded_rectangle([x - nw // 2, leaf_y - nh // 2, x + nw // 2, leaf_y + nh // 2], radius=6, fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
        draw.text((x, leaf_y - 4), expr, fill=NAVY, font=font_mono, anchor="mm")
        draw.text((x, leaf_y + 12), f"→ {res}", fill=CRIMSON, font=font_badge, anchor="mm")

    # Level 1 Nodes: min(4,1)=1 and min(8,2)=2
    l1_y = 270
    l1_xs = [(leaf_xs[0] + leaf_xs[1]) // 2, (leaf_xs[2] + leaf_xs[3]) // 2]
    l1_nodes = [("min(4,1)", "1"), ("min(8,2)", "2")]
    for i, (expr, res) in enumerate(l1_nodes):
        x = l1_xs[i]
        draw.rounded_rectangle([x - nw // 2, l1_y - nh // 2, x + nw // 2, l1_y + nh // 2], radius=6, fill=(254, 243, 199), outline=GOLD, width=2)
        draw.text((x, l1_y - 4), expr, fill=NAVY, font=font_mono, anchor="mm")
        draw.text((x, l1_y + 12), f"→ {res}", fill=CRIMSON, font=font_badge, anchor="mm")
        # arrows from leaves to l1
        draw_arrow(draw, leaf_xs[2*i], leaf_y - nh // 2, x - 15, l1_y + nh // 2, color=LINE_COLOR, width=2)
        draw_arrow(draw, leaf_xs[2*i + 1], leaf_y - nh // 2, x + 15, l1_y + nh // 2, color=LINE_COLOR, width=2)

    # Root Level: min(1,2)=1
    root_y = 175
    root_x = (l1_xs[0] + l1_xs[1]) // 2
    draw.rounded_rectangle([root_x - nw // 2 - 10, root_y - nh // 2 - 5, root_x + nw // 2 + 10, root_y + nh // 2 + 5], radius=8, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=3)
    draw.text((root_x, root_y - 6), "min(1, 2)", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((root_x, root_y + 12), "FINAL MIN = 1", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="mm")
    draw_arrow(draw, l1_xs[0], l1_y - nh // 2, root_x - 25, root_y + nh // 2 + 5, color=LINE_COLOR, width=2)
    draw_arrow(draw, l1_xs[1], l1_y - nh // 2, root_x + 25, root_y + nh // 2 + 5, color=LINE_COLOR, width=2)

    # Reduction comparison card
    draw.rounded_rectangle([rx_panel + 20, 440, rx_panel + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((rx_panel + 35, 455), "SERIAL_MIN vs. RECURSIVE_MIN Complexity Analysis", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([rx_panel + 35, 475, rx_panel + p_w - 35, 475], fill=BOX_BORDER, width=1)

    min_rows = [
        ("Serial Loop Execution:", "T1 = n - 1 comparisons. Strictly sequential execution order."),
        ("Parallel Tree Span (D):", "L = log2(n) stages. For n=8, only 3 critical steps required!"),
        ("Total Work (W):", "W = n - 1 total operations (Work-optimal parallel algorithm)."),
        ("Average Concurrency:", "W / L = (n - 1) / log2(n). Expands with problem size n."),
        ("Associative Generalization:", "Applies to any associative op: Sum, Product, AND, OR, Max.")
    ]
    my = 485
    for lbl, val in min_rows:
        draw.text((rx_panel + 35, my), f"• {lbl}", fill=CRIMSON, font=font_badge, anchor="lt")
        draw.text((rx_panel + 215, my), val, fill=TEXT_DARK, font=font_text, anchor="lt")
        my += 23

    img.save("extracted_images/lec17_recursive_decomp_min.png")
    print("Saved lec17_recursive_decomp_min.png")

# -------------------------------------------------------------
# 2. lec17_data_decomp_matrix.png
# Output Data Decomposition: Matrix-Matrix Multiplication & Non-Uniqueness
# -------------------------------------------------------------
def create_data_decomp_matrix():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_mono = get_font(14, bold=True)
    font_badge = get_font(13, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 28), "Output Data Decomposition: Matrix-Matrix Multiplication (C = A × B)", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Partitioning output data matrix C induces natural parallel tasks, but decomposition is NOT unique!", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: 4-Task Block Decomposition
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Standard 4-Task 2×2 Block Partitioning", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Each task computes an entire sub-block of C independently", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Draw Matrix A, B, C equation
    # A = [[A11, A12], [A21, A22]], B = [[B11, B12], [B21, B22]], C = [[C11, C12], [C21, C22]]
    ox = 70
    oy = 170
    cs = 44 # cell size

    def draw_2x2_matrix(x, y, name, sub_labels, color_bg, border_color):
        draw.text((x + cs, y - 16), name, fill=NAVY, font=font_badge, anchor="mm")
        for r in range(2):
            for c in range(2):
                x1, y1 = x + c * cs, y + r * cs
                draw.rectangle([x1, y1, x1 + cs, y1 + cs], fill=color_bg, outline=border_color, width=2)
                draw.text((x1 + cs // 2, y1 + cs // 2), sub_labels[r][c], fill=TEXT_DARK, font=font_mono, anchor="mm")

    draw_2x2_matrix(ox, oy, "Matrix A", [["A1,1", "A1,2"], ["A2,1", "A2,2"]], (239, 246, 255), HIGHLIGHT_BLUE)
    draw.text((ox + 2 * cs + 20, oy + cs), "×", fill=TEXT_DARK, font=font_head, anchor="mm")
    draw_2x2_matrix(ox + 2 * cs + 40, oy, "Matrix B", [["B1,1", "B1,2"], ["B2,1", "B2,2"]], (239, 246, 255), HIGHLIGHT_BLUE)
    draw.text((ox + 4 * cs + 60, oy + cs), "=", fill=TEXT_DARK, font=font_head, anchor="mm")
    draw_2x2_matrix(ox + 4 * cs + 80, oy, "Output C", [["C1,1", "C1,2"], ["C2,1", "C2,2"]], (254, 243, 199), GOLD)

    # Tasks boxes below
    ty = 300
    task_defs = [
        ("Task 1:", "C1,1 = A1,1·B1,1 + A1,2·B2,1", "Requires Row 1 of A, Col 1 of B"),
        ("Task 2:", "C1,2 = A1,1·B1,2 + A1,2·B2,2", "Requires Row 1 of A, Col 2 of B"),
        ("Task 3:", "C2,1 = A2,1·B1,1 + A2,2·B2,1", "Requires Row 2 of A, Col 1 of B"),
        ("Task 4:", "C2,2 = A2,1·B1,2 + A2,2·B2,2", "Requires Row 2 of A, Col 2 of B")
    ]
    for i, (tname, formula, req) in enumerate(task_defs):
        box_y = ty + i * 54
        draw.rounded_rectangle([60, box_y, 40 + p_w - 20, box_y + 46], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
        draw.text((75, box_y + 23), tname, fill=CRIMSON, font=font_badge, anchor="lm")
        draw.text((150, box_y + 14), formula, fill=NAVY, font=font_mono, anchor="lt")
        draw.text((150, box_y + 30), req, fill=TEXT_MUTED, font=font_text, anchor="lt")

    # Bottom summary
    draw.rounded_rectangle([60, 530, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((75, 545), "✓ Independence:", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")
    draw.text((190, 545), "All 4 tasks are mutually independent. Maximum Concurrency = 4.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((75, 575), "✓ Data Sharing:", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="lt")
    draw.text((190, 575), "Input blocks (A1,1 etc.) are shared across tasks (Read-Only).", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((75, 605), "✓ Owner Computes:", fill=CRIMSON, font=font_badge, anchor="lt")
    draw.text((190, 605), "Process assigned Ci,j performs all operations generating Ci,j.", fill=TEXT_DARK, font=font_text, anchor="lt")

    # RIGHT PANEL: Non-Uniqueness (Decomposition I vs II with 8 Tasks)
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "Non-Uniqueness: 8-Task Decompositions", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Partitioning each element computation into 2 tasks (Multiply & Accumulate)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Side-by-side subpanels for Decomp I and Decomp II
    sub_w = (p_w - 60) // 2
    # Decomp I
    draw.rounded_rectangle([rx + 20, 160, rx + 20 + sub_w, 480], radius=8, fill=(255, 255, 255), outline=HIGHLIGHT_BLUE, width=1)
    draw.text((rx + 20 + sub_w // 2, 180), "Decomposition I", fill=NAVY, font=font_head, anchor="mm")
    draw.text((rx + 20 + sub_w // 2, 202), "Canonical Row-Major Accumulation", fill=TEXT_MUTED, font=get_font(12), anchor="mm")
    draw.line([rx + 30, 215, rx + 10 + sub_w, 215], fill=BOX_BORDER, width=1)

    d1_tasks = [
        ("Task 1:", "C1,1 = A1,1·B1,1"),
        ("Task 2:", "C1,1 = C1,1 + A1,2·B2,1"),
        ("Task 3:", "C1,2 = A1,1·B1,2"),
        ("Task 4:", "C1,2 = C1,2 + A1,2·B2,2"),
        ("Task 5:", "C2,1 = A2,1·B1,1"),
        ("Task 6:", "C2,1 = C2,1 + A2,2·B2,1"),
        ("Task 7:", "C2,2 = A2,1·B1,2"),
        ("Task 8:", "C2,2 = C2,2 + A2,2·B2,2"),
    ]
    dy = 226
    for tname, formula in d1_tasks:
        draw.text((rx + 32, dy), tname, fill=CRIMSON, font=get_font(12, bold=True), anchor="lt")
        draw.text((rx + 82, dy), formula, fill=TEXT_DARK, font=get_font(12, bold=True), anchor="lt")
        dy += 31

    # Decomp II
    draw.rounded_rectangle([rx + 40 + sub_w, 160, rx + 40 + 2 * sub_w, 480], radius=8, fill=(255, 255, 255), outline=GOLD, width=1)
    draw.text((rx + 40 + sub_w + sub_w // 2, 180), "Decomposition II", fill=NAVY, font=font_head, anchor="mm")
    draw.text((rx + 40 + sub_w + sub_w // 2, 202), "Permuted Partial Sum Order", fill=TEXT_MUTED, font=get_font(12), anchor="mm")
    draw.line([rx + 50 + sub_w, 215, rx + 30 + 2 * sub_w, 215], fill=BOX_BORDER, width=1)

    d2_tasks = [
        ("Task 1:", "C1,1 = A1,1·B1,1"),
        ("Task 2:", "C1,1 = C1,1 + A1,2·B2,1"),
        ("Task 3:", "C1,2 = A1,2·B2,2"),
        ("Task 4:", "C1,2 = C1,2 + A1,1·B1,2"),
        ("Task 5:", "C2,1 = A2,2·B2,1"),
        ("Task 6:", "C2,1 = C2,1 + A2,1·B1,1"),
        ("Task 7:", "C2,2 = A2,1·B1,2"),
        ("Task 8:", "C2,2 = C2,2 + A2,2·B2,2"),
    ]
    dy = 226
    for tname, formula in d2_tasks:
        draw.text((rx + 52 + sub_w, dy), tname, fill=CRIMSON, font=get_font(12, bold=True), anchor="lt")
        draw.text((rx + 102 + sub_w, dy), formula, fill=TEXT_DARK, font=get_font(12, bold=True), anchor="lt")
        dy += 31

    # Card at bottom of right panel
    draw.rounded_rectangle([rx + 20, 500, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(254, 243, 199), outline=GOLD, width=1)
    draw.text((rx + 35, 515), "Why Decomposition is Non-Unique:", fill=NAVY, font=font_badge, anchor="lt")
    reasons = [
        "1. Algebraic commutativity of addition allows permuting accumulation steps.",
        "2. Inter-task dependencies differ (Task 2 depends on Task 1, Task 4 on 3, etc.).",
        "3. Cache spatial locality: Decomposition I keeps A1,1 in L1 cache for Tasks 1 and 3."
    ]
    ry_off = 540
    for r in reasons:
        draw.text((rx + 35, ry_off), r, fill=TEXT_DARK, font=font_text, anchor="lt")
        ry_off += 25

    img.save("extracted_images/lec17_data_decomp_matrix.png")
    print("Saved lec17_data_decomp_matrix.png")

# -------------------------------------------------------------
# 3. lec17_itemset_transactions.png
# Input vs Output vs Combined Decomposition in Database Mining
# -------------------------------------------------------------
def create_itemset_transactions():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(18, bold=True)
    font_subhead = get_font(14, bold=False)
    font_mono = get_font(12, bold=True)
    font_badge = get_font(12, bold=True)
    font_text = get_font(13, bold=False)

    draw.text((W // 2, 28), "Data Decomposition Paradigms: Frequent Itemset Transaction Mining", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Comparing Output Partitioning, Input Partitioning, and Combined 2D Grid Partitioning", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    col_w = 380
    col_h = 570
    gap = 20

    # Helper to draw a transaction table
    def draw_tx_table(x, y, tx_list, items_list, counts_list=None, title=""):
        draw.text((x + 10, y - 10), title, fill=CRIMSON, font=font_badge, anchor="lb")
        # Draw table header
        draw.rectangle([x, y, x + 160, y + 20], fill=NAVY, outline=NAVY)
        draw.text((x + 80, y + 10), "Transactions (Input)", fill=(255, 255, 255), font=get_font(11, bold=True), anchor="mm")

        draw.rectangle([x + 165, y, x + 250, y + 20], fill=NAVY, outline=NAVY)
        draw.text((x + 207, y + 10), "Itemsets", fill=(255, 255, 255), font=get_font(11, bold=True), anchor="mm")

        draw.rectangle([x + 255, y, x + 310, y + 20], fill=NAVY, outline=NAVY)
        draw.text((x + 282, y + 10), "Freq (Out)", fill=(255, 255, 255), font=get_font(11, bold=True), anchor="mm")

        row_y = y + 22
        max_rows = max(len(tx_list), len(items_list))
        for r in range(max_rows):
            # tx
            t_str = tx_list[r] if r < len(tx_list) else ""
            draw.rectangle([x, row_y, x + 160, row_y + 18], fill=(248, 250, 252), outline=BOX_BORDER)
            draw.text((x + 8, row_y + 9), t_str, fill=TEXT_DARK, font=font_mono, anchor="lm")
            # item
            i_str = items_list[r] if r < len(items_list) else ""
            draw.rectangle([x + 165, row_y, x + 250, row_y + 18], fill=(255, 255, 255), outline=BOX_BORDER)
            draw.text((x + 172, row_y + 9), i_str, fill=NAVY, font=font_mono, anchor="lm")
            # count
            c_str = str(counts_list[r]) if (counts_list and r < len(counts_list)) else "-"
            draw.rectangle([x + 255, row_y, x + 310, row_y + 18], fill=(254, 243, 199) if counts_list else (248, 250, 252), outline=BOX_BORDER)
            draw.text((x + 282, row_y + 9), c_str, fill=CRIMSON if counts_list else TEXT_MUTED, font=font_mono, anchor="mm")
            row_y += 19

    # COLUMN 1: Output Data Decomposition (Slide 19)
    c1_x = 40
    draw.rounded_rectangle([c1_x, 80, c1_x + col_w, 80 + col_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((c1_x + col_w // 2, 105), "1. Output Data Decomposition", fill=NAVY, font=font_head, anchor="mm")
    draw.text((c1_x + col_w // 2, 126), "Output itemset frequencies partitioned", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Task 1 & Task 2
    tx_all = ["A, B, C, E, G, H", "B, D, E, F, K, L", "A, B, F, H, L", "D, E, F, H", "F, G, H, K"]
    items_t1 = ["{A, B, C}", "{D, E}", "{C, F, G}", "{A, E}"]
    counts_t1 = [1, 2, 0, 1]
    draw_tx_table(c1_x + 35, 155, tx_all, items_t1, counts_t1, title="Task 1: Itemsets 1..4 (Counts: 1, 2, 0, 1)")

    items_t2 = ["{C, D}", "{D, K}", "{B, C, F}", "{C, D, K}"]
    counts_t2 = [0, 1, 0, 0]
    draw_tx_table(c1_x + 35, 330, tx_all, items_t2, counts_t2, title="Task 2: Itemsets 5..8 (Counts: 0, 1, 0, 0)")

    # Callout box 1
    draw.rounded_rectangle([c1_x + 15, 500, c1_x + col_w - 15, 80 + col_h - 15], radius=6, fill=(255, 255, 255), outline=HIGHLIGHT_BLUE, width=1)
    draw.text((c1_x + 25, 512), "• Transactions Replicated:", fill=NAVY, font=font_badge, anchor="lt")
    draw.text((c1_x + 25, 532), "Each task receives the FULL transaction DB.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((c1_x + 25, 554), "• Zero Communication:", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")
    draw.text((c1_x + 25, 574), "Tasks evaluate itemsets independently!", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((c1_x + 25, 596), "• Memory Penalty: Redundant DB storage.", fill=CRIMSON, font=font_badge, anchor="lt")

    # COLUMN 2: Input Data Decomposition (Slide 20)
    c2_x = c1_x + col_w + gap
    draw.rounded_rectangle([c2_x, 80, c2_x + col_w, 80 + col_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((c2_x + col_w // 2, 105), "2. Input Data Decomposition", fill=NAVY, font=font_head, anchor="mm")
    draw.text((c2_x + col_w // 2, 126), "Input transaction database partitioned", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    tx_p1 = ["A, B, C, E, G, H", "B, D, E, F, K, L", "A, B, F, H, L"]
    tx_p2 = ["D, E, F, H", "F, G, H, K", "A, E, F, K, L"]
    items_all_sub = ["{A, B, C}", "{D, E}", "{C, D}", "{D, K}"]
    draw_tx_table(c2_x + 35, 155, tx_p1, items_all_sub, [1, 1, 0, 0], title="Task 1: Transactions Subset 1")
    draw_tx_table(c2_x + 35, 330, tx_p2, items_all_sub, [0, 1, 0, 1], title="Task 2: Transactions Subset 2")

    # Callout box 2
    draw.rounded_rectangle([c2_x + 15, 500, c2_x + col_w - 15, 80 + col_h - 15], radius=6, fill=(255, 255, 255), outline=GOLD, width=1)
    draw.text((c2_x + 25, 512), "• Memory Optimal:", fill=NAVY, font=font_badge, anchor="lt")
    draw.text((c2_x + 25, 532), "Transaction database split across nodes.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((c2_x + 25, 554), "• Partial Counts Generated:", fill=CRIMSON, font=font_badge, anchor="lt")
    draw.text((c2_x + 25, 574), "Tasks only see a fraction of transactions.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((c2_x + 25, 596), "• Communication Required: Global reduction.", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="lt")

    # COLUMN 3: Combined Input & Output (2D Grid) (Slide 22)
    c3_x = c2_x + col_w + gap
    draw.rounded_rectangle([c3_x, 80, c3_x + col_w, 80 + col_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((c3_x + col_w // 2, 105), "3. Combined Input/Output Grid", fill=NAVY, font=font_head, anchor="mm")
    draw.text((c3_x + col_w // 2, 126), "2×2 Grid of Tasks with Reduction", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 2x2 grid mini representation
    gw = 150
    gh = 130
    gx = c3_x + 35
    gy = 160

    grid_cells = [
        (gx, gy, "Task 1", "Tx Subset 1\nItemsets 1..4", HIGHLIGHT_BLUE),
        (gx + gw + 10, gy, "Task 2", "Tx Subset 1\nItemsets 5..8", GOLD),
        (gx, gy + gh + 15, "Task 3", "Tx Subset 2\nItemsets 1..4", HIGHLIGHT_GREEN),
        (gx + gw + 10, gy + gh + 15, "Task 4", "Tx Subset 2\nItemsets 5..8", CRIMSON)
    ]
    for x, y, name, desc, col in grid_cells:
        draw.rounded_rectangle([x, y, x + gw, y + gh], radius=6, fill=(255, 255, 255), outline=col, width=2)
        draw.text((x + gw // 2, y + 20), name, fill=col, font=font_head, anchor="mm")
        draw.text((x + gw // 2, y + 65), desc, fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Reduction arrows down
    draw_arrow(draw, gx + gw // 2, gy + 2 * gh + 20, gx + gw // 2, 475, color=HIGHLIGHT_BLUE, width=2)
    draw_arrow(draw, gx + gw + 10 + gw // 2, gy + 2 * gh + 20, gx + gw + 10 + gw // 2, 475, color=CRIMSON, width=2)

    # Callout box 3
    draw.rounded_rectangle([c3_x + 15, 485, c3_x + col_w - 15, 80 + col_h - 15], radius=6, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((c3_x + 25, 498), "• 2D Decomposition Benefits:", fill=NAVY, font=font_badge, anchor="lt")
    draw.text((c3_x + 25, 518), "Scales when both DB size AND itemset", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((c3_x + 25, 536), "catalog exceed single node capacity.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((c3_x + 25, 558), "• Column-wise Tree Reduction:", fill=CRIMSON, font=font_badge, anchor="lt")
    draw.text((c3_x + 25, 578), "Partial counts for Itemsets 1..4 (T1 + T3)", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((c3_x + 25, 598), "and Itemsets 5..8 (T2 + T4) summed up.", fill=TEXT_DARK, font=font_text, anchor="lt")

    img.save("extracted_images/lec17_itemset_transactions.png")
    print("Saved lec17_itemset_transactions.png")

# -------------------------------------------------------------
# 4. lec17_intermediate_decomp_tensor.png
# Intermediate Data Partitioning: Multi-Stage Matrix Multiplication DAG
# -------------------------------------------------------------
def create_intermediate_decomp_tensor():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_mono = get_font(14, bold=True)
    font_badge = get_font(13, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 28), "Intermediate Data Partitioning: Multi-Stage Matrix Multiplication DAG", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Using intermediate product tensor D(k, i, j) = A(i, k) × B(k, j) generates a 12-Task 2-Stage DAG", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Mathematical formulation & Stage breakdown
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Stage-Based Transformation Pipeline", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Input Matrices (A, B) → Intermediate Tensor (D) → Output Matrix (C)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Stage I Box
    draw.rounded_rectangle([60, 160, 40 + p_w - 20, 360], radius=8, fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=1)
    draw.text((75, 175), "Stage I: 8 Intermediate Multiplications (Tasks 01 – 08)", fill=NAVY, font=font_badge, anchor="lt")
    draw.text((75, 195), "Computes outer-product blocks: D(k, i, j) = A(i, k) · B(k, j)", fill=TEXT_MUTED, font=font_text, anchor="lt")

    st1_tasks = [
        ("Task 01:", "D1,1,1 = A1,1·B1,1", "Task 02:", "D2,1,1 = A1,2·B2,1"),
        ("Task 03:", "D1,1,2 = A1,1·B1,2", "Task 04:", "D2,1,2 = A1,2·B2,2"),
        ("Task 05:", "D1,2,1 = A2,1·B1,1", "Task 06:", "D2,2,1 = A2,2·B2,1"),
        ("Task 07:", "D1,2,2 = A2,1·B1,2", "Task 08:", "D2,2,2 = A2,2·B2,2")
    ]
    sy = 225
    for t1, f1, t2, f2 in st1_tasks:
        draw.text((80, sy), t1, fill=CRIMSON, font=font_mono, anchor="lt")
        draw.text((150, sy), f1, fill=TEXT_DARK, font=font_mono, anchor="lt")
        draw.text((340, sy), t2, fill=CRIMSON, font=font_mono, anchor="lt")
        draw.text((410, sy), f2, fill=TEXT_DARK, font=font_mono, anchor="lt")
        sy += 30

    # Stage II Box
    draw.rounded_rectangle([60, 375, 40 + p_w - 20, 520], radius=8, fill=(254, 243, 199), outline=GOLD, width=1)
    draw.text((75, 390), "Stage II: 4 Intermediate Accumulations (Tasks 09 – 12)", fill=NAVY, font=font_badge, anchor="lt")
    draw.text((75, 410), "Reduces intermediate slices: C(i, j) = D(1, i, j) + D(2, i, j)", fill=TEXT_MUTED, font=font_text, anchor="lt")

    st2_tasks = [
        ("Task 09:", "C1,1 = D1,1,1 + D2,1,1", "Task 10:", "C1,2 = D1,1,2 + D2,1,2"),
        ("Task 11:", "C2,1 = D1,2,1 + D2,2,1", "Task 12:", "C2,2 = D1,2,2 + D2,2,2")
    ]
    sy = 438
    for t1, f1, t2, f2 in st2_tasks:
        draw.text((80, sy), t1, fill=CRIMSON, font=font_mono, anchor="lt")
        draw.text((150, sy), f1, fill=TEXT_DARK, font=font_mono, anchor="lt")
        draw.text((340, sy), t2, fill=CRIMSON, font=font_mono, anchor="lt")
        draw.text((410, sy), f2, fill=TEXT_DARK, font=font_mono, anchor="lt")
        sy += 32

    # Bottom comparison card
    draw.rounded_rectangle([60, 535, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((75, 550), "Key Advantage over Pure Output Decomposition:", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")
    draw.text((75, 575), "• Pure Output Decomposition yielded at most 4 concurrent tasks.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((75, 600), "• Intermediate Data Partitioning unleashes 8-way parallelism in Stage I!", fill=NAVY, font=font_badge, anchor="lt")

    # RIGHT PANEL: The 12-Task Dependency DAG (Slide 26)
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "12-Task Dependency DAG Structure", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Bipartite dependency structure with 4 independent reduction trees", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Draw DAG nodes
    # Top level: 8 nodes (Tasks 1..8)
    top_y = 210
    bot_y = 360
    r_node = 22

    # 4 groups of pairs: (1,2)->9, (3,4)->10, (5,6)->11, (7,8)->12
    group_centers = [rx + 75, rx + 205, rx + 345, rx + 485]
    for g, gc in enumerate(group_centers):
        t_left = 2 * g + 1
        t_right = 2 * g + 2
        t_bot = 9 + g

        # draw left top node
        x1 = gc - 32
        draw.ellipse([x1 - r_node, top_y - r_node, x1 + r_node, top_y + r_node], fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
        draw.text((x1, top_y), str(t_left), fill=NAVY, font=font_mono, anchor="mm")

        # draw right top node
        x2 = gc + 32
        draw.ellipse([x2 - r_node, top_y - r_node, x2 + r_node, top_y + r_node], fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
        draw.text((x2, top_y), str(t_right), fill=NAVY, font=font_mono, anchor="mm")

        # draw bottom sink node
        draw.ellipse([gc - r_node, bot_y - r_node, gc + r_node, bot_y + r_node], fill=(254, 243, 199), outline=GOLD, width=2)
        draw.text((gc, bot_y), str(t_bot), fill=CRIMSON, font=font_mono, anchor="mm")

        # draw arrows
        draw_arrow(draw, x1, top_y + r_node, gc - 10, bot_y - r_node, color=LINE_COLOR, width=2)
        draw_arrow(draw, x2, top_y + r_node, gc + 10, bot_y - r_node, color=LINE_COLOR, width=2)

        # Output label below
        c_names = ["C1,1", "C1,2", "C2,1", "C2,2"]
        draw.text((gc, bot_y + 35), f"yields {c_names[g]}", fill=NAVY, font=font_badge, anchor="mm")

    # Levels annotation
    draw.text((rx + 20, top_y), "Stage I\n(Tasks 1-8)", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="rm")
    draw.text((rx + 20, bot_y), "Stage II\n(Tasks 9-12)", fill=GOLD, font=font_badge, anchor="rm")

    # Graph metric analysis card
    draw.rounded_rectangle([rx + 20, 440, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((rx + 35, 455), "DAG Concurrency & Critical Path Metrics", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([rx + 35, 475, rx + p_w - 35, 475], fill=BOX_BORDER, width=1)

    dag_metrics = [
        ("Total Tasks (|V|):", "12 tasks across 2 topological levels."),
        ("Maximum Concurrency:", "8 concurrent tasks (at Stage I level)."),
        ("Critical Path Length (Span L):", "L = 2 task units (1 multiplication + 1 addition)."),
        ("Total Work (W):", "W = 8 · t_mult + 4 · t_add operations."),
        ("Average Degree of Concurrency:", "W / L ≈ 12 / 2 = 6 concurrent tasks on average!")
    ]
    my = 485
    for lbl, val in dag_metrics:
        draw.text((rx + 35, my), f"• {lbl}", fill=CRIMSON, font=font_badge, anchor="lt")
        draw.text((rx + 245, my), val, fill=TEXT_DARK, font=font_text, anchor="lt")
        my += 23

    img.save("extracted_images/lec17_intermediate_decomp_tensor.png")
    print("Saved lec17_intermediate_decomp_tensor.png")

# -------------------------------------------------------------
# 5. lec17_exploratory_15puzzle.png
# Exploratory Decomposition: State-Space Search & The 15-Puzzle
# -------------------------------------------------------------
def create_exploratory_15puzzle():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_mono = get_font(12, bold=True)
    font_badge = get_font(13, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 28), "Exploratory Decomposition: State-Space Search & The 15-Puzzle", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Problem decomposition is generated dynamically at runtime as the state-space tree is traversed", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: 15-Puzzle Move Sequence (Slide 29)
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "The 15-Tile Sliding Puzzle Benchmark", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Goal: Transform initial state (a) into ordered goal state (d)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Draw 4 puzzle grids in a 2x2 arrangement
    p_size = 110
    tile_s = p_size // 4

    def draw_15_puzzle(x, y, grid_data, label):
        draw.text((x + p_size // 2, y - 12), label, fill=NAVY, font=font_badge, anchor="mm")
        for r in range(4):
            for c in range(4):
                val = grid_data[r][c]
                x1, y1 = x + c * tile_s, y + r * tile_s
                bg = (241, 245, 249) if val == "" else (255, 255, 255)
                border = BOX_BORDER if val == "" else HIGHLIGHT_BLUE
                draw.rectangle([x1, y1, x1 + tile_s, y1 + tile_s], fill=bg, outline=border, width=1)
                if val != "":
                    draw.text((x1 + tile_s // 2, y1 + tile_s // 2), str(val), fill=TEXT_DARK, font=font_mono, anchor="mm")

    grid_a = [
        [1, 2, 3, 4],
        [5, 6, "", 8],
        [9, 10, 7, 11],
        [13, 14, 15, 12]
    ]
    grid_b = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, "", 11],
        [13, 14, 15, 12]
    ]
    grid_c = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, ""],
        [13, 14, 15, 12]
    ]
    grid_d = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, ""]
    ]

    p_ox = 110
    p_oy = 180
    draw_15_puzzle(p_ox, p_oy, grid_a, "(a) Initial State")
    draw_arrow(draw, p_ox + p_size + 15, p_oy + p_size // 2, p_ox + p_size + 45, p_oy + p_size // 2, color=CRIMSON, width=2)
    draw_15_puzzle(p_ox + p_size + 60, p_oy, grid_b, "(b) Move 7 UP")

    p_oy2 = 330
    draw_15_puzzle(p_ox, p_oy2, grid_c, "(c) Move 11 LEFT")
    draw_arrow(draw, p_ox + p_size + 15, p_oy2 + p_size // 2, p_ox + p_size + 45, p_oy2 + p_size // 2, color=CRIMSON, width=2)
    draw_15_puzzle(p_ox + p_size + 60, p_oy2, grid_d, "(d) Move 12 UP (GOAL)")

    # Callout card
    draw.rounded_rectangle([60, 480, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 495), "Characteristics of Exploratory Problems:", fill=NAVY, font=font_badge, anchor="lt")
    expl_bullets = [
        "• Search space size: 16! / 2 ≈ 1.04 × 10^13 reachable states.",
        "• Unpredictable tree shape: Cannot predict which branch leads to goal.",
        "• Applications: 0/1 Integer Programming, Chess/Go engines, SAT solvers.",
        "• Speculative nature: Most branches searched turn out to be dead ends!"
    ]
    by = 520
    for b in expl_bullets:
        draw.text((75, by), b, fill=TEXT_DARK, font=font_text, anchor="lt")
        by += 24

    # RIGHT PANEL: Search Tree Generation & Parallel Tasks (Slide 30)
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "State-Space Tree & Task Generation", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Each valid move spawns an independent successor task", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Tree root: Current state S0
    tx_root = rx + 80
    ty_root = 320
    draw.rounded_rectangle([tx_root - 40, ty_root - 25, tx_root + 40, ty_root + 25], radius=6, fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((tx_root, ty_root - 6), "State S0", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((tx_root, ty_root + 10), "Root Node", fill=CRIMSON, font=get_font(11, bold=True), anchor="mm")

    # 4 Successor Tasks (Up, Down, Left, Right)
    t_xs = rx + 240
    t_ys = [180, 270, 360, 450]
    task_labels = [
        ("Task 1 (Move UP)", "Explores Subtree 1", HIGHLIGHT_BLUE),
        ("Task 2 (Move DOWN)", "Explores Subtree 2", HIGHLIGHT_BLUE),
        ("Task 3 (Move LEFT)", "Explores Subtree 3", HIGHLIGHT_GREEN),
        ("Task 4 (Move RIGHT)", "Explores Subtree 4", HIGHLIGHT_BLUE)
    ]

    for i, (tname, tdesc, col) in enumerate(task_labels):
        y = t_ys[i]
        # arrow from root to task
        draw_arrow(draw, tx_root + 40, ty_root, t_xs - 10, y, color=LINE_COLOR, width=2)
        # task card
        draw.rounded_rectangle([t_xs, y - 22, t_xs + 160, y + 22], radius=6, fill=(255, 255, 255), outline=col, width=2)
        draw.text((t_xs + 80, y - 6), tname, fill=col, font=get_font(12, bold=True), anchor="mm")
        draw.text((t_xs + 80, y + 10), tdesc, fill=TEXT_MUTED, font=get_font(11), anchor="mm")

        # Subtree fans to right
        for k in range(-1, 2):
            draw.line([t_xs + 160, y, t_xs + 220, y + k * 18], fill=BOX_BORDER, width=1)
            draw.ellipse([t_xs + 220 - 4, y + k * 18 - 4, t_xs + 220 + 4, y + k * 18 + 4], fill=BOX_BORDER)

    # Highlight Task 3 finds goal!
    draw.rounded_rectangle([t_xs + 235, t_ys[2] - 18, rx + p_w - 20, t_ys[2] + 18], radius=6, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((t_xs + 245, t_ys[2]), "★ GOAL FOUND!", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lm")

    # Early termination note at bottom
    draw.rounded_rectangle([rx + 20, 500, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(254, 242, 242), outline=CARD_BORDER_BAD, width=1)
    draw.text((rx + 35, 515), "Early Termination & Work Discrepancy:", fill=CRIMSON, font=font_badge, anchor="lt")
    draw.text((rx + 35, 540), "• Once Task 3 discovers the goal, Tasks 1, 2, and 4 are IMMEDIATELY aborted.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((rx + 35, 565), "• Total work performed depends critically on which branch is explored first!", fill=NAVY, font=font_text, anchor="lt")
    draw.text((rx + 35, 590), "• Leads to Anomalous Superlinear (Sp > p) or Sublinear (Sp < 1) Speedups.", fill=CRIMSON, font=font_badge, anchor="lt")

    img.save("extracted_images/lec17_exploratory_15puzzle.png")
    print("Saved lec17_exploratory_15puzzle.png")

# -------------------------------------------------------------
# 6. lec17_anomalous_speedup.png
# Exploratory Decomposition: Anomalous Superlinear & Sublinear Speedup
# -------------------------------------------------------------
def create_anomalous_speedup():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_mono = get_font(14, bold=True)
    font_badge = get_font(13, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 28), "Exploratory Decomposition: Anomalous Speedup Phenomenon", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Because search halts upon finding the first solution, parallel execution can achieve speedup Sp > p or Sp < 1", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # Helper to draw search tree with 4 subtrees
    def draw_search_trees(panel_x, panel_y, sol_subtree_idx, sol_depth, title, subtitle):
        draw.rounded_rectangle([panel_x, panel_y, panel_x + p_w, panel_y + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
        draw.text((panel_x + p_w // 2, panel_y + 30), title, fill=CRIMSON, font=font_head, anchor="mm")
        draw.text((panel_x + p_w // 2, panel_y + 54), subtitle, fill=TEXT_MUTED, font=font_subhead, anchor="mm")

        # Root node
        rx = panel_x + p_w // 2
        ry = panel_y + 110
        draw.ellipse([rx - 14, ry - 14, rx + 14, ry + 14], fill=NAVY, outline=NAVY)
        draw.text((rx, ry), "S0", fill=(255, 255, 255), font=get_font(11, bold=True), anchor="mm")

        # 4 Subtrees (triangles)
        sw = 80
        sh = 90
        sub_xs = [panel_x + 90 + i * 115 for i in range(4)]
        sub_top_y = ry + 40
        sub_bot_y = sub_top_y + sh

        for i, cx in enumerate(sub_xs):
            # line from root
            draw.line([rx, ry + 14, cx, sub_top_y], fill=LINE_COLOR, width=2)
            # triangle
            pts = [(cx, sub_top_y), (cx - sw // 2, sub_bot_y), (cx + sw // 2, sub_bot_y)]
            is_sol = (i == sol_subtree_idx)
            fill_c = (240, 253, 244) if is_sol else (241, 245, 249)
            border_c = HIGHLIGHT_GREEN if is_sol else BOX_BORDER
            draw.polygon(pts, fill=fill_c, outline=border_c)

            # label
            draw.text((cx, sub_bot_y - 25), "m", fill=TEXT_MUTED, font=font_mono, anchor="mm")
            draw.text((cx, sub_bot_y + 15), f"Tree {i+1}", fill=NAVY, font=font_badge, anchor="mm")

            if is_sol:
                # draw solution dot
                dot_y = sub_top_y + int(sh * sol_depth)
                draw.ellipse([cx - 8, dot_y - 8, cx + 8, dot_y + 8], fill=CRIMSON, outline=HIGHLIGHT_RED, width=2)
                draw_arrow(draw, cx + 30, dot_y, cx + 12, dot_y, color=CRIMSON, width=2)
                draw.text((cx + 34, dot_y), "Solution", fill=CRIMSON, font=font_badge, anchor="lm")

    # LEFT PANEL: (a) Superlinear Speedup (Slide 31 a)
    # Solution is in subtree 3, near top (depth = 0.1)
    draw_search_trees(40, 80, 2, 0.15, "Case (a): Superlinear Speedup (Sp > p)", "Parallel search hits solution early; serial search wastes time on subtrees 1 & 2")

    # Metrics card left
    draw.rounded_rectangle([60, 390, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((75, 410), "Mathematical Work Breakdown (p = 4 Processors):", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")

    c1_rows = [
        ("Serial Search (DFS):", "Explores Tree 1 (m), Tree 2 (m), then 1 step in Tree 3."),
        ("Total Serial Work (Ts):", "Ts = 2m + 1 steps."),
        ("Parallel Search (p=4):", "Processor 3 hits solution in 1 step! Broadcasts abort signal."),
        ("Total Parallel Time (Tp):", "Tp = 1 step! (All other 3 processors aborted immediately)."),
        ("Effective Speedup (Sp):", "Sp = Ts / Tp = (2m + 1) / 1 = 2m + 1 >> 4 !"),
        ("Result:", "SUPERLINEAR SPEEDUP! Sp > p by an arbitrary factor m.")
    ]
    my = 438
    for lbl, val in c1_rows:
        draw.text((75, my), lbl, fill=NAVY, font=font_badge, anchor="lt")
        draw.text((250, my), val, fill=CRIMSON if "SUPERLINEAR" in val or "Sp =" in val else TEXT_DARK, font=font_text, anchor="lt")
        my += 28

    # RIGHT PANEL: (b) Sublinear Speedup / Slowdown (Slide 31 b)
    # Solution is in subtree 1, near top (depth = 0.1), but parallel does wasteful work
    rx = 40 + p_w + 40
    draw_search_trees(rx, 80, 0, 0.95, "Case (b): Sublinear Speedup (Sp < 1)", "Serial DFS hits solution quickly; parallel search expands 4× total work")

    # Metrics card right
    draw.rounded_rectangle([rx + 20, 390, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(254, 242, 242), outline=CARD_BORDER_BAD, width=1)
    draw.text((rx + 35, 410), "Mathematical Work Breakdown (p = 4 Processors):", fill=CRIMSON, font=font_badge, anchor="lt")

    c2_rows = [
        ("Serial Search (DFS):", "Lucky heuristic visits Tree 1 immediately. Finds goal at m."),
        ("Total Serial Work (Ts):", "Ts = m steps."),
        ("Parallel Search (p=4):", "If goal is deep in Tree 1, all 4 cores search concurrently."),
        ("Total Parallel Work (Wp):", "Wp = 4m (Processors 2, 3, 4 search useless branches)."),
        ("Parallel Time (Tp):", "Tp = m steps (assuming Tree 1 finishes at time m)."),
        ("Effective Speedup (Sp):", "Sp = Ts / Tp = m / m = 1 (Zero speedup despite 4 cores!)."),
        ("Result:", "SUBLINEAR SPEEDUP / SLOWDOWN (Sp << p).")
    ]
    my = 438
    for lbl, val in c2_rows:
        draw.text((rx + 35, my), lbl, fill=NAVY, font=font_badge, anchor="lt")
        draw.text((rx + 235, my), val, fill=CRIMSON if "SUBLINEAR" in val or "Sp =" in val else TEXT_DARK, font=font_text, anchor="lt")
        my += 28

    img.save("extracted_images/lec17_anomalous_speedup.png")
    print("Saved lec17_anomalous_speedup.png")

# -------------------------------------------------------------
# 7. lec17_speculative_vs_exploratory.png
# Speculative Decomposition vs Exploratory Decomposition
# -------------------------------------------------------------
def create_speculative_vs_exploratory():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_mono = get_font(13, bold=True)
    font_badge = get_font(13, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 28), "Speculative Decomposition vs. Exploratory Decomposition", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Comparing Concurrency Under Unknown Inputs (Speculative) vs Unknown Outputs (Exploratory)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Speculative Decomposition
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Speculative Decomposition", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Input at branch leading to multiple tasks is UNKNOWN", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Flowchart for speculative execution
    # Task A (Decider) running concurrently with Speculative Task B1 and B2
    fx = 40 + p_w // 2
    # Stage 0: Decider task
    draw.rounded_rectangle([fx - 140, 160, fx + 140, 210], radius=8, fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
    draw.text((fx, 175), "Preceding Task A", fill=NAVY, font=font_head, anchor="mm")
    draw.text((fx, 195), "Computing branch condition: flag = f(data)", fill=TEXT_MUTED, font=font_mono, anchor="mm")

    # Fork branches while Task A is executing!
    draw_arrow(draw, fx - 60, 210, fx - 120, 270, color=LINE_COLOR, width=2)
    draw_arrow(draw, fx + 60, 210, fx + 120, 270, color=LINE_COLOR, width=2)

    # Branch 1 (Speculated TRUE)
    draw.rounded_rectangle([fx - 240, 270, fx - 20, 350], radius=8, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((fx - 130, 290), "Speculative Task B1", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="mm")
    draw.text((fx - 130, 312), "Assumes: flag == TRUE", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((fx - 130, 332), "(Optimistic Execution)", fill=TEXT_MUTED, font=font_text, anchor="mm")

    # Branch 2 (Speculated FALSE)
    draw.rounded_rectangle([fx + 20, 270, fx + 240, 350], radius=8, fill=(254, 242, 242), outline=HIGHLIGHT_RED, width=2)
    draw.text((fx + 130, 290), "Speculative Task B2", fill=HIGHLIGHT_RED, font=font_badge, anchor="mm")
    draw.text((fx + 130, 312), "Assumes: flag == FALSE", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((fx + 130, 332), "(Rollback if TRUE)", fill=TEXT_MUTED, font=font_text, anchor="mm")

    # Outcome resolution
    draw_arrow(draw, fx - 130, 350, fx - 130, 410, color=HIGHLIGHT_GREEN, width=2)
    draw_arrow(draw, fx + 130, 350, fx + 130, 410, color=HIGHLIGHT_RED, width=2)

    draw.rounded_rectangle([60, 410, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 425), "Mechanisms of Speculation:", fill=NAVY, font=font_badge, anchor="lt")
    spec_points = [
        ("Conservative Approach:", "Evaluate only when independence is guaranteed; avoid rollback."),
        ("Optimistic Approach:", "Execute most likely branch concurrently. Must checkpoint state!"),
        ("Rollback Cost:", "If prediction fails, discard state, restore checkpoint, rerun correct path."),
        ("Hardware / Software:", "Used in Out-of-Order CPUs (branch prediction), Speculative OpenMP/STM.")
    ]
    sy = 450
    for title, desc in spec_points:
        draw.text((75, sy), f"• {title}", fill=CRIMSON, font=font_badge, anchor="lt")
        draw.text((235, sy), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        sy += 27

    # RIGHT PANEL: Exploratory Decomposition
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "Exploratory Decomposition", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Output of multiple tasks originating at a branch is UNKNOWN", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Flowchart for exploratory search
    r_fx = rx + p_w // 2
    draw.rounded_rectangle([r_fx - 140, 160, r_fx + 140, 210], radius=8, fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((r_fx, 175), "Known Input State S", fill=NAVY, font=font_head, anchor="mm")
    draw.text((r_fx, 195), "Search for valid goal satisfying constraints", fill=TEXT_MUTED, font=font_mono, anchor="mm")

    # 3 Exploratory tasks
    for i, off in enumerate([-160, 0, 160]):
        draw_arrow(draw, r_fx, 210, r_fx + off, 270, color=LINE_COLOR, width=2)
        bg = (240, 253, 244) if i == 1 else (241, 245, 249)
        border = HIGHLIGHT_GREEN if i == 1 else BOX_BORDER
        draw.rounded_rectangle([r_fx + off - 70, 270, r_fx + off + 70, 350], radius=8, fill=bg, outline=border, width=2)
        draw.text((r_fx + off, 290), f"Search Subtree {i+1}", fill=NAVY, font=font_badge, anchor="mm")
        draw.text((r_fx + off, 312), "Output: Unknown", fill=CRIMSON if i != 1 else HIGHLIGHT_GREEN, font=font_mono, anchor="mm")
        status_txt = "GOAL REACHED!" if i == 1 else "Dead End / Pruned"
        draw.text((r_fx + off, 332), status_txt, fill=HIGHLIGHT_GREEN if i == 1 else TEXT_MUTED, font=font_text, anchor="mm")

    # Callout card right
    draw.rounded_rectangle([rx + 20, 410, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((rx + 35, 425), "Summary Comparison:", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([rx + 35, 445, rx + p_w - 35, 445], fill=BOX_BORDER, width=1)

    comp_table = [
        ("Core Difference:", "Speculative: Input at branch is unknown.\nExploratory: Output of branch tasks is unknown."),
        ("Termination:", "Speculative: Resolves when decider task finishes.\nExploratory: Terminates when first solution is discovered."),
        ("Waste of Work:", "Speculative: Mispredicted branches must be discarded.\nExploratory: Subtrees without solution are discarded."),
        ("Anomalous Speedup:", "Exploratory search can achieve Sp > p due to search serendipity.")
    ]
    sy = 455
    for title, desc in comp_table:
        draw.text((rx + 35, sy), f"• {title}", fill=CRIMSON, font=font_badge, anchor="lt")
        lines = desc.split("\n")
        draw.text((rx + 185, sy), lines[0], fill=TEXT_DARK, font=font_text, anchor="lt")
        if len(lines) > 1:
            draw.text((rx + 185, sy + 18), lines[1], fill=TEXT_DARK, font=font_text, anchor="lt")
            sy += 18
        sy += 27

    img.save("extracted_images/lec17_speculative_vs_exploratory.png")
    print("Saved lec17_speculative_vs_exploratory.png")

# -------------------------------------------------------------
# 8. lec17_hybrid_quicksort.png
# Hybrid Decomposition: Overcoming Bottlenecks in Parallel Quicksort
# -------------------------------------------------------------
def create_hybrid_quicksort():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_mono = get_font(14, bold=True)
    font_badge = get_font(13, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 28), "Hybrid Decomposition: Overcoming Bottlenecks in Parallel Quicksort", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Combining Data Decomposition (Parallel Partitioning) with Recursive Decomposition (Tree Schedulers)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: The Problem with Pure Recursive Decomposition (Slide 34)
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "The Bottleneck of Pure Recursive Decomposition", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Why recursive decomposition alone limits concurrency (Slide 34)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Draw pyramid / bottleneck tree
    bx = 40 + p_w // 2
    # Top level: 1 processor works, p-1 idle!
    draw.rounded_rectangle([bx - 120, 160, bx + 120, 210], radius=8, fill=(254, 242, 242), outline=HIGHLIGHT_RED, width=2)
    draw.text((bx, 175), "Root Level: 1 Task", fill=CRIMSON, font=font_badge, anchor="mm")
    draw.text((bx, 195), "1 Core active, p-1 cores IDLE! (Time = O(n))", fill=TEXT_DARK, font=font_mono, anchor="mm")

    draw_arrow(draw, bx - 50, 210, bx - 100, 260, color=LINE_COLOR, width=2)
    draw_arrow(draw, bx + 50, 210, bx + 100, 260, color=LINE_COLOR, width=2)

    # Level 1: 2 tasks
    draw.rounded_rectangle([bx - 220, 260, bx - 20, 310], radius=8, fill=(254, 243, 199), outline=GOLD, width=1)
    draw.text((bx - 120, 285), "Level 1: 2 Tasks (p-2 cores IDLE)", fill=NAVY, font=font_mono, anchor="mm")

    draw.rounded_rectangle([bx + 20, 260, bx + 220, 310], radius=8, fill=(254, 243, 199), outline=GOLD, width=1)
    draw.text((bx + 120, 285), "Level 1: 2 Tasks (p-2 cores IDLE)", fill=NAVY, font=font_mono, anchor="mm")

    # Bottom summary card
    draw.rounded_rectangle([60, 345, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 365), "Mathematical Bottleneck Analysis:", fill=NAVY, font=font_badge, anchor="lt")

    flaws = [
        ("Amdahl's Law Trap:", "Root partition of n elements takes serial time c·n on 1 core."),
        ("Massive Core Idling:", "With p = 64 cores, 63 cores sit 100% idle at the start of sort!"),
        ("Span Bottleneck:", "Span is L = O(n). Theoretical speedup bounded by Sp ≤ O(log n)."),
        ("Load Imbalance:", "Unequal pivot splits exacerbate idle waiting across recursion tree.")
    ]
    fy = 395
    for title, desc in flaws:
        draw.text((75, fy), f"• {title}", fill=CRIMSON, font=font_badge, anchor="lt")
        draw.text((230, fy), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        fy += 32

    # RIGHT PANEL: The Hybrid Solution (Slide 34 Diagram)
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "The Hybrid Decomposition Architecture", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Data Partitioning at upper levels + Recursive Decomposition below", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Replicate Slide 34 diagram: 4 data blocks partitioned across processors
    # Array split into 4 blocks: [3 7 2 9], [11 4 5 8], [7 10 6 13], [1 19 3 9]
    hx = rx + 30
    hy = 170
    bw = 28
    blocks = [
        ([3, 7, 2, 9], "P0, P1"),
        ([11, 4, 5, 8], "P2, P3"),
        ([7, 10, 6, 13], "P4, P5"),
        ([1, 19, 3, 9], "P6, P7")
    ]
    for b_idx, (b_arr, p_lbl) in enumerate(blocks):
        bx_start = hx + b_idx * 130
        draw.text((bx_start + 2 * bw, hy - 14), p_lbl, fill=NAVY, font=font_badge, anchor="mm")
        for i, val in enumerate(b_arr):
            draw.rectangle([bx_start + i * bw, hy, bx_start + (i + 1) * bw, hy + 26], fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=1)
            draw.text((bx_start + i * bw + bw // 2, hy + 13), str(val), fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Annotation bracket for Data Decomposition
    draw.text((rx + p_w - 40, hy + 13), "} Data Decomposition", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="lm")

    # Tree lines down to intermediate merges: [2] and [1]
    hy2 = 250
    draw_arrow(draw, hx + 56, hy + 28, hx + 120, hy2 - 14, color=LINE_COLOR, width=2)
    draw_arrow(draw, hx + 186, hy + 28, hx + 120, hy2 - 14, color=LINE_COLOR, width=2)

    draw_arrow(draw, hx + 316, hy + 28, hx + 380, hy2 - 14, color=LINE_COLOR, width=2)
    draw_arrow(draw, hx + 446, hy + 28, hx + 380, hy2 - 14, color=LINE_COLOR, width=2)

    # Intermediate nodes
    for cx, num in [(hx + 120, 2), (hx + 380, 1)]:
        draw.rectangle([cx - 16, hy2 - 14, cx + 16, hy2 + 14], fill=(254, 243, 199), outline=GOLD, width=2)
        draw.text((cx, hy2), str(num), fill=CRIMSON, font=font_mono, anchor="mm")

    # Root node [1]
    hy3 = 330
    cx_root = (hx + 120 + hx + 380) // 2
    draw_arrow(draw, hx + 120, hy2 + 14, cx_root, hy3 - 14, color=LINE_COLOR, width=2)
    draw_arrow(draw, hx + 380, hy2 + 14, cx_root, hy3 - 14, color=LINE_COLOR, width=2)
    draw.rectangle([cx_root - 16, hy3 - 14, cx_root + 16, hy3 + 14], fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((cx_root, hy3), "1", fill=NAVY, font=font_mono, anchor="mm")

    draw.text((rx + p_w - 40, (hy2 + hy3) // 2), "} Recursive Decomposition", fill=CRIMSON, font=font_badge, anchor="lm")

    # Architecture explanation card
    draw.rounded_rectangle([rx + 20, 385, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((rx + 35, 400), "Why Hybrid Decomposition Excels:", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")

    h_bullets = [
        ("Phase 1: Parallel Data Partitioning", "All p processors participate in partitioning the array around the pivot using parallel prefix sums (Span = O(log n))."),
        ("Phase 2: Processor Subset Division", "Processors are partitioned into two groups {P0..P(p/2)-1} and {P(p/2)..P(p)-1} to tackle sublists."),
        ("Phase 3: Recursive Independent Sort", "Once sublists fit on single processors, switch to pure local recursive sorting with zero communication!"),
        ("Resulting Parallel Span:", "Span reduced from O(n) down to O(log^2 n)! Near-optimal speedup.")
    ]
    hy_off = 428
    for title, desc in h_bullets:
        draw.text((rx + 35, hy_off), f"✓ {title}:", fill=NAVY, font=font_badge, anchor="lt")
        draw.text((rx + 35, hy_off + 18), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        hy_off += 38

    img.save("extracted_images/lec17_hybrid_quicksort.png")
    print("Saved lec17_hybrid_quicksort.png")

if __name__ == "__main__":
    create_recursive_decomp_min()
    create_data_decomp_matrix()
    create_itemset_transactions()
    create_intermediate_decomp_tensor()
    create_exploratory_15puzzle()
    create_anomalous_speedup()
    create_speculative_vs_exploratory()
    create_hybrid_quicksort()
    print("All Lecture 17 images generated successfully!")
