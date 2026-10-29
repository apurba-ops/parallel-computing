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

# -------------------------------------------------------------
# 1. lec16_matrix_vector_decomp.png
# Matrix-Vector Multiplication: Fine-Grained vs Coarse-Grained
# -------------------------------------------------------------
def create_matrix_vector_decomp():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(20, bold=True)
    font_subhead = get_font(15, bold=False)
    font_mono = get_font(14, bold=True)
    font_badge = get_font(14, bold=True)
    font_text = get_font(15, bold=False)

    draw.text((W // 2, 28), "Matrix-Vector Multiplication: Task Granularity Decomposition", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Computing y = A × b : Comparing Fine-Grained (Row/Element) vs Coarse-Grained (Block) Partitioning", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Fine-Grained Decomposition
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Fine-Grained Decomposition (n Tasks)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 136), "Each task computes one row dot product: y[i] = dot(A[i, :], b)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Draw Matrix A, Vector b, Vector y for fine-grained
    ox, oy = 120, 170
    cell = 28
    n = 8
    draw.text((ox + n * cell // 2, oy - 16), "Matrix A (n × n)", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(n):
        for c in range(n):
            x1, y1 = ox + c * cell, oy + r * cell
            x2, y2 = x1 + cell, y1 + cell
            fill_c = (239, 246, 255) if r == 0 else (255, 255, 255)
            border_c = HIGHLIGHT_BLUE if r == 0 else (203, 213, 225)
            draw.rectangle([x1, y1, x2, y2], fill=fill_c, outline=border_c, width=1)
    # Highlight Row 0 as Task 1
    draw.rectangle([ox, oy, ox + n * cell, oy + cell], outline=CRIMSON, width=2)
    draw.text((ox - 12, oy + cell // 2), "Task 1", fill=CRIMSON, font=font_mono, anchor="rm")
    draw.text((ox - 12, oy + cell + cell // 2), "Task 2", fill=TEXT_MUTED, font=font_mono, anchor="rm")
    draw.text((ox - 12, oy + (n - 1) * cell + cell // 2), "Task n", fill=CRIMSON, font=font_mono, anchor="rm")
    for i in range(2, n - 1):
        draw.text((ox - 18, oy + i * cell + cell // 2), "·", fill=TEXT_MUTED, font=font_mono, anchor="rm")

    # Times sign
    draw.text((ox + n * cell + 24, oy + n * cell // 2), "×", fill=TEXT_DARK, font=font_head, anchor="mm")

    # Vector b: 8x1
    bx = ox + n * cell + 50
    draw.text((bx + cell // 2, oy - 16), "b", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(n):
        x1, y1 = bx, oy + r * cell
        x2, y2 = x1 + cell, y1 + cell
        draw.rectangle([x1, y1, x2, y2], fill=(241, 245, 249), outline=NAVY, width=1)

    # Equals sign
    draw.text((bx + cell + 24, oy + n * cell // 2), "=", fill=TEXT_DARK, font=font_head, anchor="mm")

    # Vector y: 8x1
    yx = bx + cell + 50
    draw.text((yx + cell // 2, oy - 16), "y", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(n):
        x1, y1 = yx, oy + r * cell
        x2, y2 = x1 + cell, y1 + cell
        fill_y = (254, 226, 226) if r == 0 else (255, 255, 255)
        border_y = CRIMSON if r == 0 else (203, 213, 225)
        draw.rectangle([x1, y1, x2, y2], fill=fill_y, outline=border_y, width=1)
    draw.rectangle([yx, oy, yx + cell, oy + cell], outline=CRIMSON, width=2)
    draw.text((yx + cell + 12, oy + cell // 2), "y[0]", fill=CRIMSON, font=font_mono, anchor="lm")
    draw.text((yx + cell + 12, oy + (n - 1) * cell + cell // 2), "y[n-1]", fill=TEXT_MUTED, font=font_mono, anchor="lm")

    # Summary box for left panel
    draw.rounded_rectangle([60, 420, 600, 635], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    left_notes = [
        "• Number of Tasks: n tasks (or up to n² at scalar granularity)",
        "• Workload per Task: Uniform (n multiplications + n additions)",
        "• Task Independence: Zero inter-task dependencies!",
        "• Concurrency Bound: Degree of concurrency = n (or n²)",
        "• Bottleneck: Excessive communication & scheduling overhead"
    ]
    for idx, line in enumerate(left_notes):
        color = CRIMSON if "Bottleneck" in line else (NAVY if "Independence" in line else TEXT_DARK)
        draw.text((78, 438 + idx * 38), line, fill=color, font=font_text)

    # RIGHT PANEL: Coarse-Grained Decomposition
    rx0 = 660
    draw.rounded_rectangle([rx0, 80, rx0 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx0 + p_w // 2, 110), "Coarse-Grained Decomposition (4 Tasks)", fill=NAVY, font=font_head, anchor="mm")
    draw.text((rx0 + p_w // 2, 136), "Matrix rows grouped into blocks: Task k computes (n/4) rows", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Draw Matrix A, Vector b, Vector y for coarse-grained
    cox = rx0 + 60
    coy = 170
    draw.text((cox + n * cell // 2, coy - 16), "Matrix A (Blocked Rows)", fill=NAVY, font=font_badge, anchor="mm")
    block_colors = [
        ((238, 242, 255), HIGHLIGHT_BLUE),
        ((254, 243, 199), GOLD),
        ((220, 252, 231), HIGHLIGHT_GREEN),
        ((243, 232, 255), (147, 51, 234))
    ]
    for b_idx in range(4):
        r_start = b_idx * 2
        fill_b, border_b = block_colors[b_idx]
        for r in range(r_start, r_start + 2):
            for c in range(n):
                x1, y1 = cox + c * cell, coy + r * cell
                x2, y2 = x1 + cell, y1 + cell
                draw.rectangle([x1, y1, x2, y2], fill=fill_b, outline=(203, 213, 225), width=1)
        # Block border
        draw.rectangle([cox, coy + r_start * cell, cox + n * cell, coy + (r_start + 2) * cell], outline=border_b, width=2)
        draw.text((cox - 12, coy + r_start * cell + cell), f"Task {b_idx+1}", fill=border_b, font=font_mono, anchor="rm")

    # Times sign
    draw.text((cox + n * cell + 24, coy + n * cell // 2), "×", fill=TEXT_DARK, font=font_head, anchor="mm")

    # Vector b: 8x1
    cbx = cox + n * cell + 50
    draw.text((cbx + cell // 2, coy - 16), "b", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(n):
        x1, y1 = cbx, coy + r * cell
        x2, y2 = x1 + cell, y1 + cell
        draw.rectangle([x1, y1, x2, y2], fill=(241, 245, 249), outline=NAVY, width=1)

    # Equals sign
    draw.text((cbx + cell + 24, coy + n * cell // 2), "=", fill=TEXT_DARK, font=font_head, anchor="mm")

    # Vector y: 8x1 (grouped into blocks)
    cyx = cbx + cell + 50
    draw.text((cyx + cell // 2, coy - 16), "y", fill=NAVY, font=font_badge, anchor="mm")
    for b_idx in range(4):
        r_start = b_idx * 2
        fill_b, border_b = block_colors[b_idx]
        for r in range(r_start, r_start + 2):
            x1, y1 = cyx, coy + r * cell
            x2, y2 = x1 + cell, y1 + cell
            draw.rectangle([x1, y1, x2, y2], fill=fill_b, outline=(203, 213, 225), width=1)
        draw.rectangle([cyx, coy + r_start * cell, cyx + cell, coy + (r_start + 2) * cell], outline=border_b, width=2)
        draw.text((cyx + cell + 12, coy + r_start * cell + cell), f"y[{r_start}:{r_start+2}]", fill=border_b, font=font_mono, anchor="lm")

    # Summary box for right panel
    draw.rounded_rectangle([rx0 + 20, 420, rx0 + p_w - 20, 635], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    right_notes = [
        "• Number of Tasks: p tasks (e.g., p = 4 cores/processors)",
        "• Workload per Task: Coarse block of (n/p) rows × n ops",
        "• Cache Locality: High spatial reuse of vector b in caches",
        "• Amortized Overhead: Low message startup & sync cost",
        "• Sweet Spot: Maximizes effective FLOPS and speedup"
    ]
    for idx, line in enumerate(right_notes):
        color = HIGHLIGHT_GREEN if "Sweet Spot" in line else (NAVY if "Cache" in line else TEXT_DARK)
        draw.text((rx0 + 38, 438 + idx * 38), line, fill=color, font=font_text)

    # Bottom footer card
    draw.rounded_rectangle([40, 660, W - 40, 690], radius=4, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((W // 2, 675), "Core Principle: Finer decomposition unlocks maximum concurrency, but coarse-graining amortizes communication latency!", fill=(22, 101, 52), font=font_text, anchor="mm")

    img.save("extracted_images/lec16_matrix_vector_decomp.png")
    print("Saved extracted_images/lec16_matrix_vector_decomp.png")

# -------------------------------------------------------------
# 2. lec16_db_query_dag1.png
# Database Query Processing Dependency Graph 1
# -------------------------------------------------------------
def create_db_query_dag1():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(17, bold=True)
    font_subhead = get_font(14, bold=False)
    font_mono = get_font(13, bold=True)
    font_badge = get_font(14, bold=True)
    font_text = get_font(14, bold=False)
    font_stage = get_font(13, bold=True)

    draw.text((W // 2, 26), "Database Query Processing: Task Dependency Graph-1", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 52), "Query: MODEL = 'CIVIC' AND YEAR = 2001 AND (COLOR = 'GREEN' OR COLOR = 'WHITE')", fill=CRIMSON, font=font_sub, anchor="mm")

    # Table preview box at top right
    draw.rounded_rectangle([860, 72, 1240, 230], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text((1050, 90), "Database Table (10 Tuples)", fill=NAVY, font=font_head, anchor="mm")
    db_samples = [
        "4523 Civic  2002 Blue  MN $18k",
        "3476 Corolla 1999 White IL $15k",
        "7623 Camry  2001 Green NY $21k",
        "9834 Prius  2001 Green CA $18k",
        "6734 Civic  2001 White OR $17k ✓",
        "4395 Civic  2001 Red   CA $17k",
    ]
    for idx, s in enumerate(db_samples):
        color = HIGHLIGHT_GREEN if "✓" in s else TEXT_DARK
        draw.text((878, 114 + idx * 18), s, fill=color, font=font_mono)

    # LEVEL 1: Independent Selection Tasks (4 parallel tasks)
    y_l1 = 140
    boxes_l1 = [
        {"x": 120, "label": "Model = Civic", "tuples": ["4523, 6734", "4395, 7352"], "color": NAVY},
        {"x": 300, "label": "Year = 2001", "tuples": ["7623, 6734, 5342", "3845, 4395"], "color": NAVY},
        {"x": 500, "label": "Color = White", "tuples": ["3476, 6734"], "color": NAVY_LIGHT},
        {"x": 680, "label": "Color = Green", "tuples": ["7623, 9834", "5342, 8354"], "color": NAVY_LIGHT}
    ]

    for b in boxes_l1:
        bx, by = b["x"], y_l1
        bw, bh = 155, 100
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(241, 245, 249), outline=b["color"], width=2)
        draw.text((bx + bw // 2, by + 18), b["label"], fill=b["color"], font=font_badge, anchor="mm")
        draw.line([(bx + 10, by + 32), (bx + bw - 10, by + 32)], fill=BOX_BORDER, width=1)
        for t_idx, t_str in enumerate(b["tuples"][:3]):
            draw.text((bx + bw // 2, by + 50 + t_idx * 20), t_str, fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Level 1 label - moved right to avoid clipping
    draw.rounded_rectangle([20, y_l1 + 15, 112, y_l1 + 80], radius=6, fill=(254, 242, 242), outline=CRIMSON, width=1)
    draw.text((66, y_l1 + 35), "Stage 1:", fill=CRIMSON, font=font_stage, anchor="mm")
    draw.text((66, y_l1 + 55), "Parallel σ", fill=CRIMSON, font=font_stage, anchor="mm")

    # LEVEL 2: Intermediate Joins / Unions (2 parallel tasks)
    y_l2 = 310
    b_l2_1 = {"x": 200, "w": 210, "h": 90, "label": "Civic ∩ 2001", "tuples": ["6734, 4395"], "color": HIGHLIGHT_BLUE}
    b_l2_2 = {"x": 560, "w": 210, "h": 90, "label": "White ∪ Green", "tuples": ["3476, 7623, 9834,", "6734, 5342, 8354"], "color": HIGHLIGHT_BLUE}

    for b in [b_l2_1, b_l2_2]:
        bx, by, bw, bh = b["x"], y_l2, b["w"], b["h"]
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(238, 242, 255), outline=b["color"], width=2)
        draw.text((bx + bw // 2, by + 18), b["label"], fill=b["color"], font=font_head, anchor="mm")
        draw.line([(bx + 15, by + 34), (bx + bw - 15, by + 34)], fill=BOX_BORDER, width=1)
        for t_idx, t_str in enumerate(b["tuples"]):
            draw.text((bx + bw // 2, by + 52 + t_idx * 18), t_str, fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Dependency Edges L1 -> L2
    draw.line([(197, y_l1 + 100), (260, y_l2)], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([(377, y_l1 + 100), (360, y_l2)], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([(577, y_l1 + 100), (620, y_l2)], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([(757, y_l1 + 100), (720, y_l2)], fill=HIGHLIGHT_BLUE, width=2)

    # Stage 2 label
    draw.rounded_rectangle([20, y_l2 + 10, 112, y_l2 + 75], radius=6, fill=(238, 242, 255), outline=HIGHLIGHT_BLUE, width=1)
    draw.text((66, y_l2 + 30), "Stage 2:", fill=HIGHLIGHT_BLUE, font=font_stage, anchor="mm")
    draw.text((66, y_l2 + 50), "Combine", fill=HIGHLIGHT_BLUE, font=font_stage, anchor="mm")

    # LEVEL 3: Final Intersection (1 task)
    y_l3 = 470
    bx, by = 310, y_l3
    bw, bh = 380, 80
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((bx + bw // 2, by + 18), "Civic ∩ 2001 ∩ (White ∪ Green)", fill=(22, 101, 52), font=font_head, anchor="mm")
    draw.line([(bx + 20, by + 36), (bx + bw - 20, by + 36)], fill=CARD_BORDER_GOOD, width=1)
    draw.text((bx + bw // 2, by + 56), "ID# 6734 | Civic | 2001 | White | OR | $17,000", fill=CRIMSON, font=font_badge, anchor="mm")

    # Dependency Edges L2 -> L3
    draw.line([(305, y_l2 + 90), (420, y_l3)], fill=HIGHLIGHT_GREEN, width=3)
    draw.line([(665, y_l2 + 90), (580, y_l3)], fill=HIGHLIGHT_GREEN, width=3)

    # Stage 3 label
    draw.rounded_rectangle([20, y_l3 + 10, 112, y_l3 + 70], radius=6, fill=CARD_BG_GOOD, outline=HIGHLIGHT_GREEN, width=1)
    draw.text((66, y_l3 + 28), "Stage 3:", fill=(22, 101, 52), font=font_stage, anchor="mm")
    draw.text((66, y_l3 + 48), "Final ∩", fill=(22, 101, 52), font=font_stage, anchor="mm")

    # Right side analysis box
    draw.rounded_rectangle([860, 250, 1240, 560], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=2)
    draw.text((1050, 275), "DAG-1 Structural Properties", fill=NAVY, font=font_head, anchor="mm")
    props = [
        ("Tree Structure:", "Balanced Binary Tree"),
        ("Critical Path (Span):", "3 Stages (L1 → L2 → L3)"),
        ("Max Concurrency:", "4 Tasks (at Stage 1)"),
        ("Intermediate State:", "2 Intermediate sub-tables"),
        ("Tuple Selectivity:", "Prunes early on Model & Year"),
        ("Pipelining Potential:", "High between stages"),
        ("Parallel Speedup:", "High on multi-core DB engines")
    ]
    for idx, (k, v) in enumerate(props):
        draw.text((878, 310 + idx * 34), k, fill=NAVY, font=font_badge)
        draw.text((878, 328 + idx * 34), v, fill=TEXT_DARK, font=font_text)

    # Bottom footer card
    draw.rounded_rectangle([40, 665, W - 40, 695], radius=4, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((W // 2, 680), "Key Takeaway: Dependency DAG specifies precedence constraints — tasks in the same stage execute concurrently without hazard!", fill=(22, 101, 52), font=font_text, anchor="mm")

    img.save("extracted_images/lec16_db_query_dag1.png")
    print("Saved extracted_images/lec16_db_query_dag1.png")

# -------------------------------------------------------------
# 3. lec16_db_query_dag2.png
# Database Query Processing Dependency Graph 2
# -------------------------------------------------------------
def create_db_query_dag2():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(17, bold=True)
    font_subhead = get_font(14, bold=False)
    font_mono = get_font(13, bold=True)
    font_badge = get_font(14, bold=True)
    font_text = get_font(14, bold=False)
    font_stage = get_font(13, bold=True)

    draw.text((W // 2, 26), "Database Query Processing: Task Dependency Graph-2 (Alternative Plan)", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 52), "Alternative Query Execution Tree: Skewed Pipeline with Cascading Dependencies", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # LEVEL 1: Selections (Civic, 2001, White, Green)
    y_l1 = 100
    box_w, box_h = 160, 80
    sel_boxes = [
        {"x": 80, "label": "Model = Civic", "tuples": "{4523, 6734, 4395, 7352}", "count": "4 Tuples", "color": NAVY},
        {"x": 280, "label": "Year = 2001", "tuples": "{7623, 6734, 5342, 3845, 4395}", "count": "5 Tuples", "color": NAVY},
        {"x": 480, "label": "Color = White", "tuples": "{3476, 6734}", "count": "2 Tuples", "color": NAVY_LIGHT},
        {"x": 680, "label": "Color = Green", "tuples": "{7623, 9834, 5342, 8354}", "count": "4 Tuples", "color": NAVY_LIGHT}
    ]
    for b in sel_boxes:
        bx = b["x"]
        draw.rounded_rectangle([bx, y_l1, bx + box_w, y_l1 + box_h], radius=8, fill=(241, 245, 249), outline=b["color"], width=2)
        draw.text((bx + box_w // 2, y_l1 + 18), b["label"], fill=b["color"], font=font_badge, anchor="mm")
        draw.text((bx + box_w // 2, y_l1 + 42), b["tuples"][:22], fill=TEXT_DARK, font=font_mono, anchor="mm")
        draw.text((bx + box_w // 2, y_l1 + 62), b["count"], fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # STAGE 2: Union (White OR Green)
    y_l2 = 230
    draw.rounded_rectangle([520, y_l2, 740, y_l2 + 80], radius=8, fill=(238, 242, 255), outline=HIGHLIGHT_BLUE, width=2)
    draw.text((630, y_l2 + 18), "White ∪ Green", fill=HIGHLIGHT_BLUE, font=font_head, anchor="mm")
    draw.text((630, y_l2 + 42), "{3476, 7623, 9834, 6734, 5342, 8354}", fill=TEXT_DARK, font=font_mono, anchor="mm")
    draw.text((630, y_l2 + 62), "(6 Tuples unioned)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Edges into White OR Green
    draw.line([(560, y_l1 + box_h), (580, y_l2)], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([(760, y_l1 + box_h), (700, y_l2)], fill=HIGHLIGHT_BLUE, width=2)

    # STAGE 3: Intersection 2001 AND (White OR Green)
    y_l3 = 370
    draw.rounded_rectangle([340, y_l3, 620, y_l3 + 80], radius=8, fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((480, y_l3 + 18), "2001 ∩ (White ∪ Green)", fill=(180, 83, 9), font=font_head, anchor="mm")
    draw.text((480, y_l3 + 42), "{7623, 6734, 5342}", fill=TEXT_DARK, font=font_mono, anchor="mm")
    draw.text((480, y_l3 + 62), "(3 Matched Tuples)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Edges into 2001 AND (White OR Green)
    draw.line([(360, y_l1 + box_h), (420, y_l3)], fill=GOLD, width=2)
    draw.line([(630, y_l2 + 80), (540, y_l3)], fill=GOLD, width=2)

    # STAGE 4: Final Intersection Civic AND (2001 AND (White OR Green))
    y_l4 = 500
    draw.rounded_rectangle([150, y_l4, 570, y_l4 + 75], radius=8, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((360, y_l4 + 18), "Civic ∩ 2001 ∩ (White ∪ Green)", fill=(22, 101, 52), font=font_head, anchor="mm")
    draw.text((360, y_l4 + 50), "ID# 6734 | Civic 2001 White OR $17,000", fill=CRIMSON, font=font_badge, anchor="mm")

    # Long edge from Civic down to Final
    draw.line([(160, y_l1 + box_h), (160, y_l4 + 37)], fill=NAVY, width=2)
    draw.line([(160, y_l4 + 37), (150, y_l4 + 37)], fill=NAVY, width=2)
    # Edge from Stage 3 down to Final
    draw.line([(480, y_l3 + 80), (420, y_l4)], fill=HIGHLIGHT_GREEN, width=3)

    # Comparative analysis box on right
    draw.rounded_rectangle([870, 90, 1240, 580], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=2)
    draw.text((1055, 118), "DAG-1 vs DAG-2 Comparison", fill=CRIMSON, font=font_head, anchor="mm")
    diffs = [
        ("Topology:", "DAG-1: Balanced binary tree\nDAG-2: Left-skewed sequential chain"),
        ("Critical Path (Span):", "DAG-1: 3 stages (Shorter)\nDAG-2: 4 stages (25% Longer!)"),
        ("Average Concurrency:", "DAG-1: Higher parallel concurrency\nDAG-2: Lower; Civic waits idle 2 stages"),
        ("Intermediate Tuples:", "DAG-1: 2 + 6 = 8 tuples buffered\nDAG-2: 6 + 3 = 9 tuples buffered"),
        ("Query Optimizer Choice:", "Optimizers evaluate Cost Models\nto pick DAG with minimal work & span!")
    ]
    for idx, (k, v) in enumerate(diffs):
        draw.text((888, 155 + idx * 85), k, fill=NAVY, font=font_badge)
        lines = v.split('\n')
        draw.text((888, 175 + idx * 85), lines[0], fill=TEXT_DARK, font=font_text)
        draw.text((888, 195 + idx * 85), lines[1], fill=TEXT_MUTED, font=font_text)

    # Bottom footer card
    draw.rounded_rectangle([40, 665, W - 40, 695], radius=4, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((W // 2, 680), "Algorithmic Lesson: Multiple distinct task dependency graphs can solve the exact same problem with radically different performance!", fill=(22, 101, 52), font=font_text, anchor="mm")

    img.save("extracted_images/lec16_db_query_dag2.png")
    print("Saved extracted_images/lec16_db_query_dag2.png")

# -------------------------------------------------------------
# 4. lec16_dag_critical_path_examples.png
# Quantitative Analysis: Work, Critical Path, and Concurrency
# -------------------------------------------------------------
def create_dag_critical_path_examples():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_subhead = get_font(14, bold=False)
    font_mono = get_font(14, bold=True)
    font_badge = get_font(14, bold=True)
    font_text = get_font(14, bold=False)
    font_large_val = get_font(22, bold=True)

    draw.text((W // 2, 26), "Degree of Concurrency & Critical Path Analysis", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 52), "Average Concurrency = Total Work / Critical Path Length (Grama Section 3.1.2)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 575

    # Helper function to draw node with circle and weight inside
    def draw_task_node(cx, cy, label, weight, is_crit=False):
        r = 25
        fill_c = (254, 226, 226) if is_crit else (238, 242, 255)
        border_c = CRIMSON if is_crit else HIGHLIGHT_BLUE
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill_c, outline=border_c, width=3 if is_crit else 2)
        draw.text((cx, cy), str(weight), fill=border_c, font=font_badge, anchor="mm")
        draw.text((cx, cy - r - 14), label, fill=NAVY if not is_crit else CRIMSON, font=font_badge, anchor="mm")

    # ==========================
    # LEFT PANEL: GRAPH (a)
    # ==========================
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 108), "Graph (a): Symmetric Tree Reduction", fill=NAVY, font=font_head, anchor="mm")

    # Coordinates for Graph (a) - spread out more
    y_root = 180
    x_t4, x_t3, x_t2, x_t1 = 120, 230, 390, 500
    y_mid = 300
    x_t6, x_t5 = 175, 445
    y_sink = 420
    x_t7 = 310

    # Edges for Graph (a)
    draw.line([(x_t1, y_root + 25), (x_t5, y_mid - 25)], fill=LINE_COLOR, width=2)
    draw.line([(x_t2, y_root + 25), (x_t5, y_mid - 25)], fill=LINE_COLOR, width=2)
    draw.line([(x_t5, y_mid + 25), (x_t7, y_sink - 25)], fill=LINE_COLOR, width=2)
    draw.line([(x_t4, y_root + 25), (x_t6, y_mid - 25)], fill=LINE_COLOR, width=2)

    # CRITICAL PATH EDGES (Task 3 -> Task 6 -> Task 7) in RED
    draw.line([(x_t3, y_root + 25), (x_t6, y_mid - 25)], fill=CRIMSON, width=4)
    draw.line([(x_t6, y_mid + 25), (x_t7, y_sink - 25)], fill=CRIMSON, width=4)

    # Draw Nodes
    draw_task_node(x_t4, y_root, "Task 4", 10, is_crit=False)
    draw_task_node(x_t3, y_root, "Task 3", 10, is_crit=True)
    draw_task_node(x_t2, y_root, "Task 2", 10, is_crit=False)
    draw_task_node(x_t1, y_root, "Task 1", 10, is_crit=False)

    draw_task_node(x_t6, y_mid, "Task 6", 9, is_crit=True)
    draw_task_node(x_t5, y_mid, "Task 5", 6, is_crit=False)

    draw_task_node(x_t7, y_sink, "Task 7", 8, is_crit=True)

    # Metrics Card for Graph (a)
    draw.rounded_rectangle([60, 470, 600, 640], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((80, 488), "Critical Path (Red): T3 (10) → T6 (9) → T7 (8)", fill=CRIMSON, font=font_badge)
    draw.text((80, 512), "• Total Work (W) = 10+10+10+10+6+9+8 = 63", fill=TEXT_DARK, font=font_text)
    draw.text((80, 534), "• Critical Path Length (Span L) = 10+9+8 = 27", fill=TEXT_DARK, font=font_text)
    draw.text((80, 556), "• Alt Paths: T1/2→T5→T7 = 10+6+8 = 24 < 27", fill=TEXT_MUTED, font=font_text)
    draw.rounded_rectangle([80, 578, 580, 630], radius=4, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((330, 604), "Avg Concurrency = 63 / 27 ≈ 2.33 Tasks", fill=(22, 101, 52), font=font_large_val, anchor="mm")

    # ==========================
    # RIGHT PANEL: GRAPH (b)
    # ==========================
    rx0 = 660
    draw.rounded_rectangle([rx0, 80, rx0 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx0 + p_w // 2, 108), "Graph (b): Cascading Dependency Chain", fill=NAVY, font=font_head, anchor="mm")

    # Coordinates for Graph (b)
    bx_t4, bx_t3, bx_t2, bx_t1 = rx0 + 80, rx0 + 200, rx0 + 370, rx0 + 490
    by_root = 180
    by_t5 = 275
    bx_t5 = rx0 + 430
    by_t6 = 365
    bx_t6 = rx0 + 310
    by_t7 = 445
    bx_t7 = rx0 + 200

    # Edges for Graph (b)
    draw.line([(bx_t2, by_root + 25), (bx_t5, by_t5 - 25)], fill=LINE_COLOR, width=2)
    draw.line([(bx_t3, by_root + 25), (bx_t6, by_t6 - 25)], fill=LINE_COLOR, width=2)
    draw.line([(bx_t4, by_root + 25), (bx_t7, by_t7 - 25)], fill=LINE_COLOR, width=2)

    # CRITICAL PATH EDGES (Task 1 -> Task 5 -> Task 6 -> Task 7) in RED
    draw.line([(bx_t1, by_root + 25), (bx_t5, by_t5 - 25)], fill=CRIMSON, width=4)
    draw.line([(bx_t5, by_t5 + 25), (bx_t6, by_t6 - 25)], fill=CRIMSON, width=4)
    draw.line([(bx_t6, by_t6 + 25), (bx_t7, by_t7 - 25)], fill=CRIMSON, width=4)

    # Draw Nodes
    draw_task_node(bx_t4, by_root, "Task 4", 10, is_crit=False)
    draw_task_node(bx_t3, by_root, "Task 3", 10, is_crit=False)
    draw_task_node(bx_t2, by_root, "Task 2", 10, is_crit=False)
    draw_task_node(bx_t1, by_root, "Task 1", 10, is_crit=True)

    draw_task_node(bx_t5, by_t5, "Task 5", 6, is_crit=True)
    draw_task_node(bx_t6, by_t6, "Task 6", 11, is_crit=True)
    draw_task_node(bx_t7, by_t7, "Task 7", 7, is_crit=True)

    # Metrics Card for Graph (b)
    draw.rounded_rectangle([rx0 + 20, 470, rx0 + p_w - 20, 640], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((rx0 + 40, 488), "Critical Path (Red): T1 (10) → T5 (6) → T6 (11) → T7 (7)", fill=CRIMSON, font=font_badge)
    draw.text((rx0 + 40, 512), "• Total Work (W) = 10+10+10+10+6+11+7 = 64", fill=TEXT_DARK, font=font_text)
    draw.text((rx0 + 40, 534), "• Critical Path Length (Span L) = 10+6+11+7 = 34", fill=TEXT_DARK, font=font_text)
    draw.text((rx0 + 40, 556), "• Alt Paths: T3→T6→T7 = 28; T4→T7 = 17", fill=TEXT_MUTED, font=font_text)
    draw.rounded_rectangle([rx0 + 40, 578, rx0 + p_w - 40, 630], radius=4, fill=(254, 242, 242), outline=CARD_BORDER_BAD, width=1)
    draw.text((rx0 + p_w // 2, 604), "Avg Concurrency = 64 / 34 ≈ 1.88 Tasks", fill=CRIMSON, font=font_large_val, anchor="mm")

    # Bottom footer card
    draw.rounded_rectangle([40, 665, W - 40, 695], radius=4, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((W // 2, 680), "Theoretical Bound: By Brent's Theorem, execution time on p processors is bounded by: T_p ≥ max(W / p, L)", fill=(22, 101, 52), font=font_text, anchor="mm")

    img.save("extracted_images/lec16_dag_critical_path_examples.png")
    print("Saved extracted_images/lec16_dag_critical_path_examples.png")

# -------------------------------------------------------------
# 5. lec16_granularity_overhead_tradeoff.png
# Limit on Parallel Performance & Granularity Tradeoff
# -------------------------------------------------------------
def create_granularity_overhead_tradeoff():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(19, bold=True)
    font_subhead = get_font(15, bold=False)
    font_badge = get_font(14, bold=True)
    font_text = get_font(15, bold=False)
    font_axis = get_font(14, bold=True)

    draw.text((W // 2, 28), "Decomposition Granularity vs. Overhead Trade-off", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Balancing Concurrency against Inter-Task Communication and Scheduling Overhead", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # Draw Graph on Left
    gx, gy, gw, gh = 80, 100, 660, 510
    draw.rounded_rectangle([gx - 10, gy - 10, gx + gw + 10, gy + gh + 10], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=1)

    # Axes
    ox, oy = gx + 70, gy + gh - 60
    xmax, ymax = gx + gw - 40, gy + 40
    draw.line([(ox, oy), (xmax, oy)], fill=LINE_COLOR, width=2)  # X axis
    draw.line([(ox, oy), (ox, ymax)], fill=LINE_COLOR, width=2)  # Y axis

    draw.polygon([(xmax, oy - 5), (xmax + 10, oy), (xmax, oy + 5)], fill=LINE_COLOR)
    draw.polygon([(ox - 5, ymax), (ox, ymax - 10), (ox + 5, ymax)], fill=LINE_COLOR)

    draw.text((ox + (xmax - ox) // 2, oy + 30), "Granularity (Coarse  →  Fine / Task Count)", fill=NAVY, font=font_axis, anchor="mm")
    draw.text((ox - 20, ymax + 15), "Execution\nTime", fill=NAVY, font=font_axis, anchor="rm")

    # Inherent Granularity Bound vertical line at right
    x_bound = gx + gw - 80
    for y in range(ymax + 10, oy, 10):
        draw.line([(x_bound, y), (x_bound, min(y + 5, oy))], fill=CRIMSON, width=2)
    draw.text((x_bound, ymax - 5), "Inherent Bound", fill=CRIMSON, font=font_badge, anchor="mm")
    draw.text((x_bound, ymax + 12), "(Single Scalar Op)", fill=CRIMSON, font=font_subhead, anchor="mm")

    # Curves
    pts_comp = []
    pts_comm = []
    pts_total = []
    steps = 100
    for i in range(steps + 1):
        frac = i / steps
        x = ox + frac * (x_bound - ox)
        t_comp_val = 300 / (1 + 4 * frac) + 30
        t_comm_val = 15 + 260 * (frac ** 2.2)
        t_tot_val = t_comp_val + t_comm_val

        y_comp = oy - t_comp_val
        y_comm = oy - t_comm_val
        y_tot = oy - t_tot_val

        pts_comp.append((x, y_comp))
        pts_comm.append((x, y_comm))
        pts_total.append((x, y_tot))

    # Draw curves
    for i in range(len(pts_comp) - 1):
        draw.line([pts_comp[i], pts_comp[i+1]], fill=HIGHLIGHT_BLUE, width=3)
        draw.line([pts_comm[i], pts_comm[i+1]], fill=GOLD, width=3)
        draw.line([pts_total[i], pts_total[i+1]], fill=CRIMSON, width=4)

    # Curve Labels - positioned to avoid overlap
    draw.text((pts_comp[30][0] + 20, pts_comp[30][1] + 10), "Computation Time (T_comp)", fill=HIGHLIGHT_BLUE, font=font_badge)
    draw.text((pts_comm[65][0] - 200, pts_comm[65][1] - 15), "Overhead & Comm (T_comm)", fill=(180, 83, 9), font=font_badge)
    draw.text((pts_total[20][0] + 20, pts_total[20][1] - 25), "Total Parallel Time (T_P)", fill=CRIMSON, font=font_head)

    # Find minimum of T_total (Sweet Spot)
    min_idx = min(range(len(pts_total)), key=lambda idx: pts_total[idx][1])
    opt_x, opt_y = pts_total[min_idx]

    draw.ellipse([opt_x - 8, opt_y - 8, opt_x + 8, opt_y + 8], fill=HIGHLIGHT_GREEN, outline=(22, 101, 52), width=2)
    draw.line([(opt_x, opt_y + 8), (opt_x, oy)], fill=HIGHLIGHT_GREEN, width=2)
    draw.text((opt_x, oy + 14), "Optimal", fill=(22, 101, 52), font=font_badge, anchor="mm")
    draw.text((opt_x, oy + 30), "(Sweet Spot)", fill=(22, 101, 52), font=font_subhead, anchor="mm")

    # Right Explanatory Cards
    rx = 790
    rw = 450
    draw.rounded_rectangle([rx, 100, rx + rw, 600], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + rw // 2, 130), "Key Performance Insights", fill=NAVY, font=font_head, anchor="mm")

    insights = [
        ("1. Fallacy of Arbitrary Finesse:",
         "Parallel time cannot be made arbitrarily small by subdividing tasks. Atomic operations enforce a lower bound."),
        ("2. Surface-to-Volume Ratio:",
         "As task size shrinks, computation scales as O(s³) but interaction scales as O(s²). Small tasks communicate more than they compute!"),
        ("3. Matrix-Vector Upper Bound:",
         "Multiplying an n×n matrix with vector b yields at most n² concurrent tasks. Beyond n², no further concurrency exists."),
        ("4. Architectural Overheads:",
         "Finer tasks create thread sync barriers, cache invalidation storms, OS context switches, and network contention.")
    ]

    for idx, (title, desc) in enumerate(insights):
        iy = 165 + idx * 105
        draw.text((rx + 18, iy), title, fill=CRIMSON if idx == 0 else NAVY, font=font_badge)
        words = desc.split(' ')
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) > 48:
                lines.append(cur)
                cur = w
            else:
                cur = cur + " " + w if cur else w
        if cur:
            lines.append(cur)
        for l_idx, line in enumerate(lines):
            draw.text((rx + 18, iy + 22 + l_idx * 20), line, fill=TEXT_DARK, font=font_text)

    # Bottom footer card
    draw.rounded_rectangle([40, 660, W - 40, 695], radius=4, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((W // 2, 678), "Rule of Thumb: Maximize computation-to-communication ratio by choosing the coarsest granularity that saturates all processors!", fill=(22, 101, 52), font=font_text, anchor="mm")

    img.save("extracted_images/lec16_granularity_overhead_tradeoff.png")
    print("Saved extracted_images/lec16_granularity_overhead_tradeoff.png")

# -------------------------------------------------------------
# 6. lec16_task_interaction_graph_sparse.png
# Sparse Matrix-Vector Multiplication: Task Interaction Graph
# -------------------------------------------------------------
def create_task_interaction_graph_sparse():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_subhead = get_font(14, bold=False)
    font_mono = get_font(12, bold=True)
    font_badge = get_font(14, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 26), "Task Interaction Graphs: Sparse Matrix-Vector Multiplication", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 52), "Interaction Topology Isomorphism: Task Interaction Graph ≅ Adjacency Graph of Matrix A", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: (a) Sparse Matrix A & Partitioned Vector b
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 108), "(a) Sparse Matrix A & Partitioned Vector b", fill=NAVY, font=font_head, anchor="mm")

    # 12 x 12 grid
    ox, oy = 100, 155
    cell = 26
    n = 12

    # Column numbers at top
    for c in range(n):
        draw.text((ox + c * cell + cell // 2, oy - 12), str(c), fill=TEXT_MUTED, font=font_mono, anchor="mm")

    # Non-zero entries
    nz_map = {
        0: [0, 4, 5],
        1: [1, 2, 4, 5],
        2: [1, 2, 3, 6],
        3: [2, 3, 7],
        4: [0, 1, 4, 5, 8],
        5: [0, 1, 4, 5, 6, 9],
        6: [2, 5, 6, 7, 10],
        7: [3, 6, 7, 11],
        8: [4, 8, 9],
        9: [5, 8, 9, 10],
        10: [6, 9, 10, 11],
        11: [7, 10, 11]
    }

    for r in range(n):
        draw.text((ox - 12, oy + r * cell + cell // 2), f"T{r}", fill=NAVY if r in [0, 11] else TEXT_MUTED, font=font_mono, anchor="rm")
        for c in range(n):
            x1, y1 = ox + c * cell, oy + r * cell
            x2, y2 = x1 + cell, y1 + cell
            is_nz = c in nz_map.get(r, [])
            draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            if is_nz:
                draw.ellipse([x1 + 4, y1 + 4, x2 - 4, y2 - 4], fill=CRIMSON if r == c else NAVY)

    # Vector b
    bx = ox + n * cell + 35
    draw.text((bx + cell // 2, oy - 12), "b", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(n):
        y1 = oy + r * cell
        draw.rectangle([bx, y1, bx + cell, y1 + cell], fill=(241, 245, 249), outline=NAVY, width=1)
        draw.text((bx + cell // 2, y1 + cell // 2), f"b{r}", fill=NAVY, font=font_mono, anchor="mm")

    # Notes under matrix
    draw.rounded_rectangle([60, 490, 600, 635], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    matrix_notes = [
        "• Task Assignment: Task i computes y[i] and holds b[i]",
        "• Non-Zero Interaction: Task i requires b[j] iff A[i,j] ≠ 0",
        "• Data Distribution: Task i must receive b[j] from Task j",
        "• Communication: Pure peer-to-peer exchange (not a DAG!)"
    ]
    for idx, line in enumerate(matrix_notes):
        draw.text((78, 505 + idx * 30), line, fill=TEXT_DARK, font=font_text)

    # RIGHT PANEL: (b) Task Interaction Graph
    rx0 = 660
    draw.rounded_rectangle([rx0, 80, rx0 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx0 + p_w // 2, 108), "(b) Task Interaction Graph G = (V, E)", fill=CRIMSON, font=font_head, anchor="mm")

    # Node positions - spread out for clarity in larger canvas
    node_coords = {
        0: (rx0 + 90, 175),
        1: (rx0 + 240, 165),
        2: (rx0 + 390, 185),
        3: (rx0 + 520, 175),
        4: (rx0 + 160, 275),
        5: (rx0 + 310, 285),
        6: (rx0 + 430, 310),
        7: (rx0 + 530, 330),
        8: (rx0 + 90, 400),
        9: (rx0 + 260, 410),
        10: (rx0 + 410, 410),
        11: (rx0 + 520, 420)
    }

    # Draw Edges first
    for u in range(n):
        for v in nz_map.get(u, []):
            if u < v:  # Draw undirected edge once
                p1 = node_coords[u]
                p2 = node_coords[v]
                draw.line([p1, p2], fill=LINE_COLOR, width=2)

    # Draw Nodes on top of edges
    for u, (nx, ny) in node_coords.items():
        r = 20
        draw.ellipse([nx - r, ny - r, nx + r, ny + r], fill=(238, 242, 255), outline=NAVY, width=2)
        draw.text((nx, ny), str(u), fill=NAVY, font=font_badge, anchor="mm")

    # Notes under graph
    draw.rounded_rectangle([rx0 + 20, 490, rx0 + p_w - 20, 635], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    graph_notes = [
        "• Vertex Set V = {Task 0, Task 1, ..., Task 11}",
        "• Edge (u,v) ∈ E iff Task u & Task v communicate",
        "• Graph Isomorphism: Topology ≅ matrix sparsity!",
        "• Mapping Target: Embedded onto hardware (Lec 14)"
    ]
    for idx, line in enumerate(graph_notes):
        color = CRIMSON if "Isomorphism" in line else TEXT_DARK
        draw.text((rx0 + 38, 505 + idx * 30), line, fill=color, font=font_text)

    # Bottom footer card
    draw.rounded_rectangle([40, 660, W - 40, 695], radius=4, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((W // 2, 678), "Crucial Contrast: Dependency Graphs are Directed Acyclic (Precedence), Interaction Graphs are Undirected (Communication)!", fill=(22, 101, 52), font=font_text, anchor="mm")

    img.save("extracted_images/lec16_task_interaction_graph_sparse.png")
    print("Saved extracted_images/lec16_task_interaction_graph_sparse.png")

# -------------------------------------------------------------
# 7. lec16_decomposition_techniques.png
# Four Classical Decomposition Techniques
# -------------------------------------------------------------
def create_decomposition_techniques():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(18, bold=True)
    font_badge = get_font(14, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 28), "Decomposition Techniques for Parallel Algorithms", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Systematic Strategies to Expose Concurrency in Computational Problems (Grama Chapter 3.2)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # 4 Quadrants - better proportioned for 1280x720
    card_w = 580
    card_h = 270
    gap_x = 20
    gap_y = 16
    start_x = 40
    start_y = 80

    cards = [
        {
            "x": start_x, "y": start_y, "w": card_w, "h": card_h,
            "title": "1. Recursive Decomposition",
            "tag": "Divide-and-Conquer Paradigm",
            "color": NAVY, "bg": (238, 242, 255),
            "points": [
                "• Decomposes problem into independent subproblems of the same type.",
                "• Concurrency generated dynamically at each recursive branch level.",
                "• Examples: Parallel Quicksort, Merge Sort, Prefix Sum, FFT, Tree Reductions.",
                "• Task Graph: Formally models a tree-structured Task Dependency Graph."
            ]
        },
        {
            "x": start_x + card_w + gap_x, "y": start_y, "w": card_w, "h": card_h,
            "title": "2. Data Decomposition",
            "tag": "Domain & Spatial Partitioning",
            "color": CRIMSON, "bg": (254, 242, 242),
            "points": [
                "• Partitioning data associated with the computation into disjoint subsets.",
                "• Input Data Partitioning: Each task processes a slice of input (e.g. Matrix-Vector).",
                "• Output Data Partitioning: Each task computes a subset of output elements.",
                "• Intermediate Data: Dense Matrix Multiplication (Cannon / Fox algorithms).",
                "• Most widely applied technique in scientific computing and HPC Linpack."
            ]
        },
        {
            "x": start_x, "y": start_y + card_h + gap_y, "w": card_w, "h": card_h,
            "title": "3. Exploratory Decomposition",
            "tag": "Search Space & State Trees",
            "color": GOLD, "bg": (254, 243, 199),
            "points": [
                "• Used to decompose problems involving searches of large state spaces.",
                "• Concurrency arises from searching disparate subtrees simultaneously.",
                "• Superlinear Speedup or Slowdown: A task may find goal early and prune!",
                "• Examples: 15-Puzzle, Chess/Game Trees, Branch-and-Bound, SAT, TSP."
            ]
        },
        {
            "x": start_x + card_w + gap_x, "y": start_y + card_h + gap_y, "w": card_w, "h": card_h,
            "title": "4. Speculative Decomposition",
            "tag": "Optimistic Execution & Rollback",
            "color": HIGHLIGHT_GREEN, "bg": (240, 253, 244),
            "points": [
                "• Used when task dependencies cannot be determined prior to execution.",
                "• Tasks execute optimistically assuming no dependency violation will occur.",
                "• If a conflict or dependency violation is detected, work is rolled back.",
                "• Examples: Discrete Event Simulation, Speculative Lock Elision, OoO Pipelines."
            ]
        }
    ]

    for c in cards:
        draw.rounded_rectangle([c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"]], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
        # Header banner
        draw.rounded_rectangle([c["x"], c["y"], c["x"] + c["w"], c["y"] + 48], radius=10, fill=c["bg"], outline=c["color"], width=1)
        draw.text((c["x"] + 22, c["y"] + 24), c["title"], fill=c["color"], font=font_head, anchor="lm")
        draw.text((c["x"] + c["w"] - 22, c["y"] + 24), c["tag"], fill=c["color"], font=font_badge, anchor="rm")

        for idx, pt in enumerate(c["points"]):
            words = pt.split(' ')
            line = ""
            lines = []
            for w in words:
                if len(line + " " + w) > 68:
                    lines.append(line)
                    line = "    " + w
                else:
                    line = line + " " + w if line else w
            if line:
                lines.append(line)
            for l_idx, l_str in enumerate(lines):
                draw.text((c["x"] + 22, c["y"] + 62 + idx * 44 + l_idx * 18), l_str, fill=TEXT_DARK, font=font_text)

    # Bottom footer card
    draw.rounded_rectangle([40, 660, W - 40, 695], radius=4, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((W // 2, 678), "Hybrid Decomposition: Real-world HPC codes frequently combine multiple paradigms (e.g., Data + Recursive Decomposition)!", fill=(22, 101, 52), font=font_text, anchor="mm")

    img.save("extracted_images/lec16_decomposition_techniques.png")
    print("Saved extracted_images/lec16_decomposition_techniques.png")

if __name__ == "__main__":
    create_matrix_vector_decomp()
    create_db_query_dag1()
    create_db_query_dag2()
    create_dag_critical_path_examples()
    create_granularity_overhead_tradeoff()
    create_task_interaction_graph_sparse()
    create_decomposition_techniques()
    print("All Lecture 16 diagram images successfully generated!")
