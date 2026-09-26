import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs('extracted_images', exist_ok=True)

# Theme Palette (BITS Pilani Colors)
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
# 1. lec13_brents_theorem_schedule.png
# Clean, intuitive level-by-level circuit emulation on P processors
# -------------------------------------------------------------
def create_brents_theorem_schedule():
    W, H = 1100, 540
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(21, bold=True)
    font_sub = get_font(13, bold=False)
    font_head = get_font(15, bold=True)
    font_bold = get_font(13, bold=True)
    font_label = get_font(12, bold=True)
    font_sm = get_font(11, bold=False)
    font_mono = get_font(11, bold=True)
    font_math = get_font(13, bold=True)

    # Main Slide Title
    draw.text((W // 2, 26), "Brent's Theorem: Level-by-Level Circuit Emulation", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 50), "How an arbitrary circuit DAG of Work W and Depth D is mapped onto P physical processors", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # ---------------------------------------------------------
    # LEFT PANEL: Circuit DAG Partitioned by Levels (x: 45 to 495)
    # ---------------------------------------------------------
    lx1, ly1, lx2, ly2 = 45, 75, 495, 475
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)

    draw.text(((lx1 + lx2) // 2, ly1 + 22), "1. Circuit DAG Partitioned by Levels", fill=NAVY, font=font_head, anchor="mm")
    draw.text(((lx1 + lx2) // 2, ly1 + 42), "Nodes on the same level are mutually independent", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    # Level 1
    l1_y = ly1 + 65
    draw.rounded_rectangle([lx1 + 20, l1_y, lx2 - 20, l1_y + 60], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx1 + 32, l1_y + 16), "Level 1 (l1 operations)", fill=NAVY, font=font_label)
    draw.text((lx2 - 80, l1_y + 16), "Depth 1", fill=TEXT_MUTED, font=font_sm)
    # 5 clean circles
    c_x_start = lx1 + 55
    c_gap = (lx2 - lx1 - 110) / 4
    for i in range(5):
        cx = c_x_start + i * c_gap
        cy = l1_y + 40
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(219, 234, 254), outline=NAVY_LIGHT, width=2)
        draw.text((cx, cy), f"v{i+1}", fill=NAVY, font=font_sm, anchor="mm")

    # Arrow from Level 1 to Level 2
    arr_y1 = l1_y + 60
    arr_y2 = arr_y1 + 18
    draw.line([(270, arr_y1), (270, arr_y2)], fill=NAVY_LIGHT, width=2)
    draw.polygon([(266, arr_y2 - 4), (274, arr_y2 - 4), (270, arr_y2 + 2)], fill=NAVY_LIGHT)

    # Level 2
    l2_y = arr_y2 + 4
    draw.rounded_rectangle([lx1 + 20, l2_y, lx2 - 20, l2_y + 60], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx1 + 32, l2_y + 16), "Level 2 (l2 operations)", fill=NAVY, font=font_label)
    draw.text((lx2 - 80, l2_y + 16), "Depth 2", fill=TEXT_MUTED, font=font_sm)
    # 4 clean circles
    c_gap2 = (lx2 - lx1 - 110) / 3
    for i in range(4):
        cx = c_x_start + i * c_gap2
        cy = l2_y + 40
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(219, 234, 254), outline=NAVY_LIGHT, width=2)
        draw.text((cx, cy), f"v{i+6}", fill=NAVY, font=font_sm, anchor="mm")

    # Vertical indicator for intermediate levels
    dots_y = l2_y + 70
    draw.text((270, dots_y), "...  ...  (Total D Levels)  ...  ...", fill=TEXT_MUTED, font=font_bold, anchor="mm")

    # Level D
    ld_y = dots_y + 20
    draw.rounded_rectangle([lx1 + 20, ld_y, lx2 - 20, ld_y + 60], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx1 + 32, ld_y + 16), "Level D (l_D operations)", fill=NAVY, font=font_label)
    draw.text((lx2 - 80, ld_y + 16), "Depth D", fill=TEXT_MUTED, font=font_sm)
    # 2 output circles with larger width to avoid text clipping
    draw.rounded_rectangle([200, ld_y + 26, 265, ld_y + 52], radius=13, fill=(219, 234, 254), outline=NAVY_LIGHT, width=2)
    draw.text((232, ld_y + 39), "v[W-1]", fill=NAVY, font=font_sm, anchor="mm")
    draw.rounded_rectangle([285, ld_y + 26, 340, ld_y + 52], radius=13, fill=(219, 234, 254), outline=NAVY_LIGHT, width=2)
    draw.text((312, ld_y + 39), "v[W]", fill=NAVY, font=font_sm, anchor="mm")

    # Bottom equation in Left Panel
    draw.rounded_rectangle([lx1 + 20, ld_y + 68, lx2 - 20, ly2 - 12], radius=6, fill=(255, 255, 255), outline=LINE_COLOR, width=1)
    draw.text(((lx1 + lx2) // 2, (ld_y + 68 + ly2 - 12) // 2), "Total Work:  W = l1 + l2 + ... + l_D = Sum(li)", fill=NAVY, font=font_bold, anchor="mm")

    # ---------------------------------------------------------
    # RIGHT PANEL: PRAM Scheduling for Level i (x: 525 to 1055)
    # ---------------------------------------------------------
    rx1, ry1, rx2, ry2 = 525, 75, 1055, 475
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)

    draw.text(((rx1 + rx2) // 2, ry1 + 22), "2. PRAM Execution of Level i on P Processors", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text(((rx1 + rx2) // 2, ry1 + 42), "Chunking li independent operations into parallel batches of size P", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    # Example setup label
    draw.text((rx1 + 25, ry1 + 65), "Concrete Example: Level i has li = 10 operations, P = 4 processors", fill=TEXT_DARK, font=font_bold)

    # 3 Execution Steps (Horizontal lanes)
    lane_x1 = rx1 + 25
    lane_x2 = rx2 - 150
    lane_w = lane_x2 - lane_x1
    slot_w = lane_w // 4

    # Step 1: Batch 1 (4 full slots)
    s1_y = ry1 + 95
    draw.text((lane_x1, s1_y), "Time Step 1 (Batch 1: 4 ops):", fill=NAVY, font=font_label)
    s1_bar_y = s1_y + 18
    for p in range(4):
        sx1 = lane_x1 + p * slot_w
        sx2 = sx1 + slot_w - 4
        draw.rounded_rectangle([sx1, s1_bar_y, sx2, s1_bar_y + 34], radius=4, fill=(219, 234, 254), outline=NAVY_LIGHT, width=1)
        draw.text(((sx1 + sx2) // 2, s1_bar_y + 17), f"P{p}: Op {p+1}", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((lane_x2 + 10, s1_bar_y + 17), "[OK] 4 Active (100% busy)", fill=HIGHLIGHT_GREEN, font=font_label, anchor="lm")

    # Step 2: Batch 2 (4 full slots)
    s2_y = s1_bar_y + 48
    draw.text((lane_x1, s2_y), "Time Step 2 (Batch 2: 4 ops):", fill=NAVY, font=font_label)
    s2_bar_y = s2_y + 18
    for p in range(4):
        sx1 = lane_x1 + p * slot_w
        sx2 = sx1 + slot_w - 4
        draw.rounded_rectangle([sx1, s2_bar_y, sx2, s2_bar_y + 34], radius=4, fill=(219, 234, 254), outline=NAVY_LIGHT, width=1)
        draw.text(((sx1 + sx2) // 2, s2_bar_y + 17), f"P{p}: Op {p+5}", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((lane_x2 + 10, s2_bar_y + 17), "[OK] 4 Active (100% busy)", fill=HIGHLIGHT_GREEN, font=font_label, anchor="lm")

    # Step 3: Batch 3 (Partial: 2 active, 2 idle)
    s3_y = s2_bar_y + 48
    draw.text((lane_x1, s3_y), "Time Step 3 (Batch 3: Remaining 2 ops):", fill=NAVY, font=font_label)
    s3_bar_y = s3_y + 18
    for p in range(2):
        sx1 = lane_x1 + p * slot_w
        sx2 = sx1 + slot_w - 4
        draw.rounded_rectangle([sx1, s3_bar_y, sx2, s3_bar_y + 34], radius=4, fill=(219, 234, 254), outline=NAVY_LIGHT, width=1)
        draw.text(((sx1 + sx2) // 2, s3_bar_y + 17), f"P{p}: Op {p+9}", fill=NAVY, font=font_mono, anchor="mm")
    for p in range(2, 4):
        sx1 = lane_x1 + p * slot_w
        sx2 = sx1 + slot_w - 4
        draw.rounded_rectangle([sx1, s3_bar_y, sx2, s3_bar_y + 34], radius=4, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
        draw.text(((sx1 + sx2) // 2, s3_bar_y + 17), f"P{p}: IDLE", fill=TEXT_MUTED, font=font_mono, anchor="mm")
    draw.text((lane_x2 + 10, s3_bar_y + 17), "[!] 2 Active, 2 Idle", fill=(180, 83, 9), font=font_label, anchor="lm")

    # Bracket for total time on Level i
    draw.rounded_rectangle([rx1 + 25, s3_bar_y + 46, rx2 - 25, ry2 - 14], radius=6, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=1)
    draw.text(((rx1 + rx2) // 2, (s3_bar_y + 46 + ry2 - 14) // 2 - 8),
              "Time for Level i:   T(i) = ceil( li / P ) = ceil( 10 / 4 ) = 3 Steps",
              fill=CRIMSON, font=font_math, anchor="mm")
    draw.text(((rx1 + rx2) // 2, (s3_bar_y + 46 + ry2 - 14) // 2 + 12),
              "Idling is bounded: at most (P - 1) idle slots occur at the final step of a level!",
              fill=TEXT_MUTED, font=font_sm, anchor="mm")

    # ---------------------------------------------------------
    # BOTTOM BANNER: Summation Over All D Levels (x: 45 to 1055)
    # ---------------------------------------------------------
    draw.rounded_rectangle([45, 485, 1055, 532], radius=6, fill=(255, 247, 237), outline=GOLD, width=1)
    draw.text((W // 2, 508),
              "Total Parallel Runtime:  T_P = Sum ceil(li / P) <= Sum (li/P + 1) = (1/P) Sum(li) + D = W/P + D = O(W/P + D)",
              fill=CRIMSON, font=font_head, anchor="mm")

    img.save("extracted_images/lec13_brents_theorem_schedule.png", quality=95)
    print("Generated extracted_images/lec13_brents_theorem_schedule.png")


# -------------------------------------------------------------
# 2. lec13_naive_merge_sort_dag.png
# Computation DAG of naive parallel merge sort showing serial merge bottleneck
# -------------------------------------------------------------
def create_naive_merge_sort_dag():
    W, H = 1000, 520
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(20, bold=True)
    font_sub = get_font(13, bold=False)
    font_label = get_font(13, bold=True)
    font_sm = get_font(11, bold=False)
    font_math = get_font(13, bold=True)

    # Title
    draw.text((W // 2, 26), "Naive Parallel Merge Sort: The Serial Merge Choke Point", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 50), "Spawning recursive sorts concurrently, but merging sequentially with standard Merge(A, p, q, r)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # Level 0
    draw.rounded_rectangle([420, 80, 580, 115], radius=6, fill=(238, 242, 255), outline=NAVY, width=2)
    draw.text((500, 97), "Par-Merge-Sort(n)", fill=NAVY, font=font_label, anchor="mm")

    # Branches to Level 1
    draw.line([(470, 115), (300, 160)], fill=LINE_COLOR, width=2)
    draw.line([(530, 115), (700, 160)], fill=LINE_COLOR, width=2)
    draw.text((370, 130), "spawn", fill=HIGHLIGHT_BLUE, font=font_sm)
    draw.text((630, 130), "call", fill=NAVY_LIGHT, font=font_sm)

    # Level 1
    draw.rounded_rectangle([210, 160, 390, 195], radius=6, fill=(238, 242, 255), outline=NAVY, width=2)
    draw.text((300, 177), "Par-Merge-Sort(n/2)", fill=NAVY, font=font_label, anchor="mm")

    draw.rounded_rectangle([610, 160, 790, 195], radius=6, fill=(238, 242, 255), outline=NAVY, width=2)
    draw.text((700, 177), "Par-Merge-Sort(n/2)", fill=NAVY, font=font_label, anchor="mm")

    # Branches to Level 2
    draw.line([(260, 195), (170, 240)], fill=LINE_COLOR, width=2)
    draw.line([(340, 195), (410, 240)], fill=LINE_COLOR, width=2)
    draw.line([(660, 195), (590, 240)], fill=LINE_COLOR, width=2)
    draw.line([(740, 195), (830, 240)], fill=LINE_COLOR, width=2)

    l2_x = [170, 410, 590, 830]
    for lx in l2_x:
        draw.rounded_rectangle([lx - 75, 240, lx + 75, 275], radius=6, fill=(241, 245, 249), outline=BOX_BORDER, width=1)
        draw.text((lx, 257), "Sort(n/4)...", fill=TEXT_DARK, font=font_sm, anchor="mm")

    # Bottom indicators: Sync points and Serial Merges!
    draw.text((290, 305), "[sync]", fill=GOLD, font=font_label, anchor="mm")
    draw.text((710, 305), "[sync]", fill=GOLD, font=font_label, anchor="mm")

    # Serial Merge blocks
    draw.rounded_rectangle([200, 325, 400, 365], radius=6, fill=(254, 242, 242), outline=CRIMSON, width=2)
    draw.text((300, 345), "Serial Merge(n/2) : Theta(n/2)", fill=CRIMSON, font=font_label, anchor="mm")

    draw.rounded_rectangle([600, 325, 800, 365], radius=6, fill=(254, 242, 242), outline=CRIMSON, width=2)
    draw.text((700, 345), "Serial Merge(n/2) : Theta(n/2)", fill=CRIMSON, font=font_label, anchor="mm")

    # Final Serial Merge at root
    draw.line([(300, 365), (480, 405)], fill=CRIMSON, width=2)
    draw.line([(700, 365), (520, 405)], fill=CRIMSON, width=2)

    draw.rounded_rectangle([320, 405, 680, 450], radius=8, fill=(254, 226, 226), outline=CRIMSON, width=3)
    draw.text((500, 427), "CRITICAL PATH BOTTLENECK: Serial Merge(n)  -->  Theta(n) Span!", fill=CRIMSON, font=font_title, anchor="mm")

    # Side callout metrics box
    draw.rounded_rectangle([45, 465, 955, 508], radius=6, fill=BOX_BG, outline=BOX_BORDER, width=1)
    metrics_text = "Work: T1(n) = 2*T1(n/2) + Theta(n) = Theta(n log n)   |   Span: T_inf(n) = T_inf(n/2) + Theta(n) = Theta(n)   |   Parallelism: Theta(log n)"
    draw.text((W // 2, 486), metrics_text, fill=NAVY, font=font_math, anchor="mm")

    img.save("extracted_images/lec13_naive_merge_sort_dag.png", quality=95)
    print("Generated extracted_images/lec13_naive_merge_sort_dag.png")


# -------------------------------------------------------------
# 3. lec13_parallel_merge_split.png
# High-res reproduction of CLRS Figure 27.3
# -------------------------------------------------------------
def create_parallel_merge_split():
    W, H = 1100, 600
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(21, bold=True)
    font_sub = get_font(13, bold=False)
    font_label = get_font(13, bold=True)
    font_bold = get_font(14, bold=True)
    font_sm = get_font(11, bold=False)
    font_pivot = get_font(15, bold=True)

    # Title
    draw.text((W // 2, 28), "Parallel Merge Algorithm: Divide-and-Conquer Decomposition", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "CLRS 3rd Ed. Section 27.3: Using Binary Search to Partition the Second Subarray Around Pivot x", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    y_t = 120
    box_h = 44

    # Top Left Array: T[p1..r1] (n1 elements)
    t1_x1, t1_x2 = 80, 500
    t1_w = t1_x2 - t1_x1
    q1_x = t1_x1 + t1_w // 2

    # Bracket for n1
    draw.line([(t1_x1, y_t - 16), (t1_x2, y_t - 16)], fill=TEXT_MUTED, width=1)
    draw.line([(t1_x1, y_t - 22), (t1_x1, y_t - 16)], fill=TEXT_MUTED, width=1)
    draw.line([(t1_x2, y_t - 22), (t1_x2, y_t - 16)], fill=TEXT_MUTED, width=1)
    draw.text(((t1_x1 + t1_x2) // 2, y_t - 28), "Subarray 1:  n1 = r1 - p1 + 1   (assume n1 >= n2)", fill=NAVY, font=font_label, anchor="mm")

    draw.text((t1_x1 - 35, y_t + box_h // 2), "T :", fill=NAVY, font=font_bold, anchor="mm")

    # T[p1..q1-1] (<= x)
    draw.rectangle([t1_x1, y_t, q1_x - 22, y_t + box_h], fill=(241, 245, 249), outline=LINE_COLOR, width=1)
    draw.text(((t1_x1 + q1_x - 22) // 2, y_t + box_h // 2), "<= x  (n1 / 2 elements)", fill=TEXT_DARK, font=font_label, anchor="mm")
    draw.text((t1_x1 + 10, y_t - 8), "p1", fill=TEXT_MUTED, font=font_sm)

    # Pivot cell x at q1
    draw.rectangle([q1_x - 22, y_t, q1_x + 22, y_t + box_h], fill=(254, 226, 226), outline=CRIMSON, width=2)
    draw.text((q1_x, y_t + box_h // 2), "x", fill=CRIMSON, font=font_pivot, anchor="mm")
    draw.text((q1_x, y_t - 8), "q1 (mid)", fill=CRIMSON, font=font_label, anchor="mm")

    # T[q1+1..r1] (>= x)
    draw.rectangle([q1_x + 22, y_t, t1_x2, y_t + box_h], fill=(226, 232, 240), outline=LINE_COLOR, width=1)
    draw.text(((q1_x + 22 + t1_x2) // 2, y_t + box_h // 2), ">= x  (n1 / 2 elements)", fill=TEXT_DARK, font=font_label, anchor="mm")
    draw.text((t1_x2 - 12, y_t - 8), "r1", fill=TEXT_MUTED, font=font_sm)

    # Top Right Array: T[p2..r2] (n2 elements)
    t2_x1, t2_x2 = 600, 980
    t2_w = t2_x2 - t2_x1
    q2_x = t2_x1 + int(t2_w * 0.42)

    # Bracket for n2
    draw.line([(t2_x1, y_t - 16), (t2_x2, y_t - 16)], fill=TEXT_MUTED, width=1)
    draw.line([(t2_x1, y_t - 22), (t2_x1, y_t - 16)], fill=TEXT_MUTED, width=1)
    draw.line([(t2_x2, y_t - 22), (t2_x2, y_t - 16)], fill=TEXT_MUTED, width=1)
    draw.text(((t2_x1 + t2_x2) // 2, y_t - 28), "Subarray 2:  n2 = r2 - p2 + 1", fill=NAVY, font=font_label, anchor="mm")

    # T[p2..q2-1] (< x)
    draw.rectangle([t2_x1, y_t, q2_x, y_t + box_h], fill=(241, 245, 249), outline=LINE_COLOR, width=1)
    draw.text(((t2_x1 + q2_x) // 2, y_t + box_h // 2), "< x", fill=TEXT_DARK, font=font_label, anchor="mm")
    draw.text((t2_x1 + 10, y_t - 8), "p2", fill=TEXT_MUTED, font=font_sm)

    # Split line q2
    draw.line([(q2_x, y_t - 2), (q2_x, y_t + box_h + 2)], fill=HIGHLIGHT_BLUE, width=3)
    draw.text((q2_x, y_t - 8), "q2", fill=HIGHLIGHT_BLUE, font=font_bold, anchor="mm")

    # T[q2..r2] (>= x)
    draw.rectangle([q2_x, y_t, t2_x2, y_t + box_h], fill=(226, 232, 240), outline=LINE_COLOR, width=1)
    draw.text(((q2_x + t2_x2) // 2, y_t + box_h // 2), ">= x", fill=TEXT_DARK, font=font_label, anchor="mm")
    draw.text((t2_x2 - 12, y_t - 8), "r2", fill=TEXT_MUTED, font=font_sm)

    # Step 2 Annotation arrow: Binary Search
    bs_arrow_y = y_t + box_h + 25
    draw.line([(q1_x, y_t + box_h + 4), (q1_x, bs_arrow_y), (q2_x, bs_arrow_y), (q2_x, y_t + box_h + 4)], fill=HIGHLIGHT_BLUE, width=2)
    draw.polygon([(q2_x - 4, y_t + box_h + 10), (q2_x + 4, y_t + box_h + 10), (q2_x, y_t + box_h + 3)], fill=HIGHLIGHT_BLUE)
    draw.text(((q1_x + q2_x) // 2, bs_arrow_y + 14), "Binary Search for x in T[p2..r2] finds split index q2 in O(log n2) time", fill=HIGHLIGHT_BLUE, font=font_label, anchor="mm")

    # Output Array A[p3..r3] at bottom
    y_a = 320
    a_x1, a_x2 = 120, 960
    a_w = a_x2 - a_x1
    left_elements_w = int(a_w * 0.44)
    q3_x = a_x1 + left_elements_w

    draw.text((a_x1 - 35, y_a + box_h // 2), "A :", fill=CRIMSON, font=font_bold, anchor="mm")

    # A left: <= x
    draw.rectangle([a_x1, y_a, q3_x - 22, y_a + box_h], fill=(241, 245, 249), outline=LINE_COLOR, width=1)
    draw.text(((a_x1 + q3_x - 22) // 2, y_a + box_h // 2), "<= x  (Merged Left Subproblem)", fill=TEXT_DARK, font=font_label, anchor="mm")
    draw.text((a_x1 + 10, y_a - 8), "p3", fill=TEXT_MUTED, font=font_sm)

    # Pivot placed directly at q3
    draw.rectangle([q3_x - 22, y_a, q3_x + 22, y_a + box_h], fill=(254, 226, 226), outline=CRIMSON, width=2)
    draw.text((q3_x, y_a + box_h // 2), "x", fill=CRIMSON, font=font_pivot, anchor="mm")
    draw.text((q3_x, y_a - 8), "q3", fill=CRIMSON, font=font_bold, anchor="mb")

    # Formula for q3 placed cleanly directly below the pivot cell
    draw.text((q3_x, y_a + box_h + 8), "q3 = p3 + (q1 - p1) + (q2 - p2)", fill=CRIMSON, font=font_bold, anchor="mt")

    # A right: >= x
    draw.rectangle([q3_x + 22, y_a, a_x2, y_a + box_h], fill=(226, 232, 240), outline=LINE_COLOR, width=1)
    draw.text(((q3_x + 22 + a_x2) // 2, y_a + box_h // 2), ">= x  (Merged Right Subproblem)", fill=TEXT_DARK, font=font_label, anchor="mm")
    draw.text((a_x2 - 12, y_a - 8), "r3", fill=TEXT_MUTED, font=font_sm)

    # A bracket (positioned below q3 formula)
    br_y = y_a + box_h + 36
    draw.line([(a_x1, br_y), (a_x2, br_y)], fill=TEXT_MUTED, width=1)
    draw.line([(a_x1, br_y), (a_x1, br_y + 6)], fill=TEXT_MUTED, width=1)
    draw.line([(a_x2, br_y), (a_x2, br_y + 6)], fill=TEXT_MUTED, width=1)
    draw.text(((a_x1 + a_x2) // 2, br_y + 14), "Merged Output:  A[p3..r3]   (Total Elements:  n3 = r3 - p3 + 1 = n1 + n2)", fill=NAVY, font=font_label, anchor="mm")

    # Routing Arrows from T to A
    draw.line([(q1_x, y_t + box_h), (q3_x, y_a)], fill=CRIMSON, width=2)
    draw.polygon([(q3_x - 5, y_a - 10), (q3_x + 5, y_a - 10), (q3_x, y_a - 2)], fill=CRIMSON)
    draw.text(((q1_x + q3_x) // 2 + 30, (y_t + box_h + y_a) // 2 - 10), "Step 3: Copy x", fill=CRIMSON, font=font_bold)

    draw.line([((t1_x1 + q1_x - 22) // 2, y_t + box_h), ((a_x1 + q3_x - 22) // 2 - 20, y_a)], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([((t2_x1 + q2_x) // 2, y_t + box_h), ((a_x1 + q3_x - 22) // 2 + 20, y_a)], fill=HIGHLIGHT_BLUE, width=2)
    draw.text(((a_x1 + q3_x) // 2 - 80, y_a - 28), "spawn Step 4(a): Par-Merge left", fill=HIGHLIGHT_BLUE, font=font_label)

    draw.line([((q1_x + 22 + t1_x2) // 2, y_t + box_h), ((q3_x + 22 + a_x2) // 2 - 20, y_a)], fill=HIGHLIGHT_GREEN, width=2)
    draw.line([((q2_x + t2_x2) // 2, y_t + box_h), ((q3_x + 22 + a_x2) // 2 + 20, y_a)], fill=HIGHLIGHT_GREEN, width=2)
    draw.text(((q3_x + a_x2) // 2, y_a - 28), "Step 4(b): Par-Merge right (parallel)", fill=HIGHLIGHT_GREEN, font=font_label)

    # Bottom summary box
    draw.rounded_rectangle([60, 485, 1040, 565], radius=8, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=1)
    draw.text((W // 2, 510),
              "Key Insight: Both recursive merge subproblems are executed CONCURRENTLY via fork-join spawn!",
              fill=NAVY, font=font_bold, anchor="mm")
    draw.text((W // 2, 538),
              "Worst-case subproblem size <= 3n/4   |   Span: T_inf(n) = T_inf(3n/4) + Theta(log n) = Theta(log^2 n)   |   Work: T1(n) = Theta(n) [Work-Efficient]",
              fill=CRIMSON, font=font_label, anchor="mm")

    img.save("extracted_images/lec13_parallel_merge_split.png", quality=95)
    print("Generated extracted_images/lec13_parallel_merge_split.png")


# -------------------------------------------------------------
# 4. lec13_worst_case_3n4_bound.png
# Visual proof of the 3n/4 subproblem bound
# -------------------------------------------------------------
def create_worst_case_3n4_bound():
    W, H = 1020, 520
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(20, bold=True)
    font_sub = get_font(13, bold=False)
    font_bold = get_font(14, bold=True)
    font_label = get_font(12, bold=True)
    font_math = get_font(13, bold=False)

    # Title
    draw.text((W // 2, 26), "Derivation: Worst-Case Subproblem Size <= 3n / 4", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 52), "Proving that recursive calls in Par-Merge process at most 75% of total elements n = n1 + n2", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # Left: Mathematical derivation cards
    draw.rounded_rectangle([45, 90, 525, 480], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text((285, 115), "Formal Algebraic Steps", fill=NAVY, font=font_bold, anchor="mm")

    steps = [
        ("1. Array Size Convention", "We ensure n1 >= n2 by swapping pointers if needed.\nThus:  2*n2 <= n1 + n2 = n   =>   n2 <= n / 2"),
        ("2. Subarray 1 Bisection", "Midpoint q1 divides T[p1..r1] into two halves:\nEach half contains at most ceil(n1 / 2) elements."),
        ("3. Worst-Case Binary Search Split", "Binary search could find all elements of T[p2..r2] fall on\none side of pivot x (e.g., q2 = p2 or q2 = r2 + 1)."),
        ("4. Worst-Case Subproblem Sum", "Worst-case elements = ceil(n1 / 2) + n2\n<= n1/2 + 1/2 + n2\n<= n1/2 + n2/2 + n2/2  =  (n1 + n2)/2 + 2*n2/4\n<= n/2 + n/4  =  3n / 4   (since 2*n2 <= n)")
    ]

    sy = 145
    for title, body in steps:
        draw.text((65, sy), title, fill=CRIMSON, font=font_label)
        sy += 20
        for line in body.split("\n"):
            draw.text((75, sy), line, fill=TEXT_DARK, font=font_math)
            sy += 18
        sy += 12

    # Right: Visual diagram of extreme case
    draw.rounded_rectangle([555, 90, 975, 480], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text((765, 115), "Extreme Case Visualization", fill=NAVY, font=font_bold, anchor="mm")

    # Bar 1: Total n elements
    draw.text((580, 155), "Total Problem Size n = n1 + n2", fill=TEXT_DARK, font=font_label)
    draw.rectangle([580, 175, 950, 210], fill=(226, 232, 240), outline=LINE_COLOR, width=1)
    n1_end = 580 + int((950 - 580) * 0.65)
    draw.rectangle([580, 175, n1_end, 210], fill=(219, 234, 254), outline=NAVY_LIGHT, width=1)
    draw.text(((580 + n1_end) // 2, 192), "n1 (>= n/2)", fill=NAVY, font=font_label, anchor="mm")
    draw.rectangle([n1_end, 175, 950, 210], fill=(254, 243, 199), outline=GOLD, width=1)
    draw.text(((n1_end + 950) // 2, 192), "n2 (<= n/2)", fill=(180, 83, 9), font=font_label, anchor="mm")

    # Bar 2: Worst-case subproblem composition
    draw.text((580, 240), "Worst-Case Subproblem: ceil(n1/2) from Array 1 + ALL n2 from Array 2", fill=CRIMSON, font=font_label)
    draw.rectangle([580, 260, 950, 305], fill=(248, 250, 252), outline=LINE_COLOR, width=1)

    half_n1_w = (n1_end - 580) // 2
    draw.rectangle([580, 260, 580 + half_n1_w, 305], fill=(219, 234, 254), outline=NAVY_LIGHT, width=1)
    draw.text((580 + half_n1_w // 2, 282), "n1 / 2", fill=NAVY, font=font_label, anchor="mm")

    draw.rectangle([580 + half_n1_w, 260, 580 + half_n1_w + (950 - n1_end), 305], fill=(254, 243, 199), outline=GOLD, width=1)
    draw.text((580 + half_n1_w + (950 - n1_end) // 2, 282), "All n2 elements", fill=(180, 83, 9), font=font_label, anchor="mm")

    mark_34_x = 580 + int((950 - 580) * 0.75)
    draw.line([(mark_34_x, 245), (mark_34_x, 325)], fill=CRIMSON, width=2)
    draw.text((mark_34_x, 335), "Maximum Bound = 3n / 4 (75%)", fill=CRIMSON, font=font_bold, anchor="mm")

    draw.rounded_rectangle([580, 370, 950, 460], radius=6, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=1)
    draw.text((765, 395), "Consequence on Recursive Span", fill=HIGHLIGHT_GREEN, font=font_bold, anchor="mm")
    draw.text((765, 420), "T_inf(n) <= T_inf(3n/4) + Theta(log n)", fill=TEXT_DARK, font=font_math, anchor="mm")
    draw.text((765, 442), "=>  T_inf(n) = Theta(log^2 n)   [Master Theorem Case 2]", fill=CRIMSON, font=font_bold, anchor="mm")

    img.save("extracted_images/lec13_worst_case_3n4_bound.png", quality=95)
    print("Generated extracted_images/lec13_worst_case_3n4_bound.png")


# -------------------------------------------------------------
# 5. lec13_mergesort_span_comparison.png
# Comparative infographic: Naive vs Fully Parallel Merge Sort
# -------------------------------------------------------------
def create_mergesort_span_comparison():
    W, H = 1040, 540
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(21, bold=True)
    font_sub = get_font(13, bold=False)
    font_head = get_font(14, bold=True)
    font_bold = get_font(13, bold=True)
    font_label = get_font(12, bold=True)
    font_sm = get_font(11, bold=False)
    font_mono = get_font(12, bold=True)

    draw.text((W // 2, 28), "Algorithm Comparison: Naive vs. Fully Parallel Merge Sort", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "How Parallelizing the Merge Subroutine Breaks the Span Bottleneck and Unlocks Massive Concurrency", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # Left Card: Naive Parallel Merge Sort
    draw.rounded_rectangle([45, 85, 500, 340], radius=8, fill=(254, 242, 242), outline=CRIMSON, width=2)
    draw.text((272, 115), "1. Naive Parallel Merge Sort", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((272, 138), "Parallel recursive sorts + Serial Merge subroutine", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    naive_metrics = [
        ("Work T1(n):", "Theta(n log n)", "Optimal sequential work"),
        ("Span T_inf(n):", "Theta(n)", "Choked by serial merge"),
        ("Parallelism:", "Theta(log n)", "Very poor scaling!"),
        ("For n = 10^6:", "P approx 20", "Cannot saturate multicore")
    ]
    ny = 165
    for label, val, note in naive_metrics:
        draw.text((65, ny), label, fill=TEXT_DARK, font=font_bold)
        draw.text((195, ny), val, fill=CRIMSON, font=font_mono)
        draw.text((310, ny), note, fill=TEXT_MUTED, font=font_sm)
        ny += 38

    # Right Card: Fully Parallel Merge Sort (CLRS)
    draw.rounded_rectangle([540, 85, 995, 340], radius=8, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((767, 115), "2. Fully Parallel Merge Sort (CLRS 27.3)", fill=HIGHLIGHT_GREEN, font=font_head, anchor="mm")
    draw.text((767, 138), "Parallel recursive sorts + Parallel Divide-&-Conquer Merge", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    clrs_metrics = [
        ("Work T1(n):", "Theta(n log n)", "Optimal work-efficient"),
        ("Span T_inf(n):", "Theta(log^3 n)", "Polylogarithmic span"),
        ("Parallelism:", "Theta(n / log^2 n)", "Scales almost linearly with n"),
        ("For n = 10^6:", "P approx 2,500", "125x greater concurrency!")
    ]
    cy = 165
    for label, val, note in clrs_metrics:
        draw.text((560, cy), label, fill=TEXT_DARK, font=font_bold)
        draw.text((690, cy), val, fill=HIGHLIGHT_GREEN, font=font_mono)
        draw.text((805, cy), note, fill=TEXT_MUTED, font=font_sm)
        cy += 38

    # Bottom Scaling Table across Problem Sizes
    draw.rounded_rectangle([45, 360, 995, 510], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text((W // 2, 385), "Scaling of Parallelism T1(n) / T_inf(n) Across Problem Sizes (n)", fill=NAVY, font=font_bold, anchor="mm")

    col_x = [70, 250, 480, 720]
    headers = ["Problem Size (n)", "log2 n", "Naive Parallelism Theta(log n)", "CLRS Parallelism Theta(n / log^2 n)"]

    draw.line([(60, 410), (980, 410)], fill=BOX_BORDER, width=1)
    for c_idx, h in enumerate(headers):
        draw.text((col_x[c_idx], 400), h, fill=NAVY, font=font_label)

    rows = [
        ("n = 1,000 (10^3)", "approx 10", "P approx 10", "P approx 10"),
        ("n = 1,000,000 (10^6)", "approx 20", "P approx 20", "P approx 2,500  (125x increase!)"),
        ("n = 1,000,000,000 (10^9)", "approx 30", "P approx 30", "P approx 1,111,000  (37,000x increase!)")
    ]

    ry = 425
    for r_idx, row in enumerate(rows):
        color = TEXT_DARK if r_idx < 2 else CRIMSON
        for c_idx, val in enumerate(row):
            font = font_mono if c_idx >= 2 else font_sm
            draw.text((col_x[c_idx], ry), val, fill=color, font=font)
        ry += 26

    img.save("extracted_images/lec13_mergesort_span_comparison.png", quality=95)
    print("Generated extracted_images/lec13_mergesort_span_comparison.png")

if __name__ == "__main__":
    create_brents_theorem_schedule()
    create_naive_merge_sort_dag()
    create_parallel_merge_split()
    create_worst_case_3n4_bound()
    create_mergesort_span_comparison()
    print("All 5 Lecture 13 diagrams generated successfully!")
