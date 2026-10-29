import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs('extracted_images', exist_ok=True)

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
# 1. lec15_fork_join_model.png
# Visualizing OpenMP Fork-Join execution model with Thread Pool
# -------------------------------------------------------------
def create_fork_join_model():
    W, H = 1200, 620
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(17, bold=True)
    font_subhead = get_font(14, bold=False)
    font_badge = get_font(13, bold=True)
    font_text = get_font(14, bold=False)
    font_mono = get_font(13, bold=True)

    draw.text((W // 2, 26), "OpenMP Fork-Join Computation Model", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Dynamic transition between sequential execution and parallel thread teams with thread-pool recycling", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # Time axis at bottom
    draw.line([(80, 560), (1120, 560)], fill=LINE_COLOR, width=2)
    draw.polygon([(1120, 555), (1135, 560), (1120, 565)], fill=LINE_COLOR)
    draw.text((1140, 560), "Time (t)", fill=NAVY, font=font_badge, anchor="lm")

    y_t0 = 200
    y_t1 = 280
    y_t2 = 360
    y_t3 = 440

    # Background shading for Parallel Regions
    draw.rounded_rectangle([250, 110, 570, 500], radius=10, fill=(238, 242, 255), outline=(199, 210, 254), width=2)
    draw.text((410, 130), "Parallel Region 1 (#pragma omp parallel)", fill=NAVY, font=font_head, anchor="mm")
    draw.text((410, 150), "Team of 4 threads executing concurrent tasks", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    draw.rounded_rectangle([690, 110, 1010, 500], radius=10, fill=(238, 242, 255), outline=(199, 210, 254), width=2)
    draw.text((850, 130), "Parallel Region 2 (Reusing Thread Pool)", fill=NAVY, font=font_head, anchor="mm")
    draw.text((850, 150), "Zero thread creation overhead (threads awakened)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Sequential annotations
    draw.text((160, 130), "Master Thread Only", fill=CRIMSON, font=font_badge, anchor="mm")
    draw.text((160, 150), "(Serial code execution)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    draw.text((630, 130), "Serial", fill=CRIMSON, font=font_badge, anchor="mm")
    draw.text((1060, 130), "Serial", fill=CRIMSON, font=font_badge, anchor="mm")

    # Thread 0 (Master Thread) - continuous across whole execution
    # Seq 1
    draw.line([(80, y_t0), (250, y_t0)], fill=CRIMSON, width=4)
    # Par 1
    draw.line([(250, y_t0), (570, y_t0)], fill=HIGHLIGHT_BLUE, width=4)
    # Seq 2
    draw.line([(570, y_t0), (690, y_t0)], fill=CRIMSON, width=4)
    # Par 2
    draw.line([(690, y_t0), (1010, y_t0)], fill=HIGHLIGHT_BLUE, width=4)
    # Seq 3
    draw.line([(1010, y_t0), (1110, y_t0)], fill=CRIMSON, width=4)

    # Worker Threads (T1, T2, T3) in Par 1
    for y_t, t_idx in [(y_t1, 1), (y_t2, 2), (y_t3, 3)]:
        # Fork 1 branching
        draw.line([(250, y_t0), (280, y_t)], fill=HIGHLIGHT_BLUE, width=2)
        # Par 1 line
        draw.line([(280, y_t), (540, y_t)], fill=HIGHLIGHT_BLUE, width=4)
        # Join 1 converging
        draw.line([(540, y_t), (570, y_t0)], fill=HIGHLIGHT_BLUE, width=2)

        # Inactive dotted line between par regions
        for x in range(570, 690, 8):
            draw.line([(x, y_t), (x + 4, y_t)], fill=(203, 213, 225), width=2)

        # Fork 2 branching
        draw.line([(690, y_t0), (720, y_t)], fill=HIGHLIGHT_BLUE, width=2)
        # Par 2 line
        draw.line([(720, y_t), (980, y_t)], fill=HIGHLIGHT_BLUE, width=4)
        # Join 2 converging
        draw.line([(980, y_t), (1010, y_t0)], fill=HIGHLIGHT_BLUE, width=2)

    # Labels for Threads on left
    draw.text((70, y_t0), "Thread 0 (Master)", fill=CRIMSON, font=font_badge, anchor="rm")
    draw.text((70, y_t1), "Thread 1 (Worker)", fill=TEXT_MUTED, font=font_subhead, anchor="rm")
    draw.text((70, y_t2), "Thread 2 (Worker)", fill=TEXT_MUTED, font=font_subhead, anchor="rm")
    draw.text((70, y_t3), "Thread 3 (Worker)", fill=TEXT_MUTED, font=font_subhead, anchor="rm")

    # Badges for FORK and JOIN
    def draw_badge(x, y, text, color, bg):
        w, h = 76, 26
        draw.rounded_rectangle([x - w//2, y - h//2, x + w//2, y + h//2], radius=6, fill=bg, outline=color, width=2)
        draw.text((x, y), text, fill=color, font=font_badge, anchor="mm")

    draw_badge(250, y_t0 - 35, "FORK", HIGHLIGHT_BLUE, (239, 246, 255))
    draw_badge(570, y_t0 - 35, "JOIN", HIGHLIGHT_GREEN, (240, 253, 244))
    draw_badge(690, y_t0 - 35, "FORK", HIGHLIGHT_BLUE, (239, 246, 255))
    draw_badge(1010, y_t0 - 35, "JOIN", HIGHLIGHT_GREEN, (240, 253, 244))

    # Barrier indicator
    draw.line([(550, 180), (550, 460)], fill=HIGHLIGHT_GREEN, width=3)
    draw.text((550, 480), "Implicit Barrier", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="mm")

    draw.line([(990, 180), (990, 460)], fill=HIGHLIGHT_GREEN, width=3)
    draw.text((990, 480), "Implicit Barrier", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="mm")

    # Callout at bottom: Key takeaway
    draw.rounded_rectangle([80, 580, 1120, 610], radius=6, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((600, 595), "Key Architecture Fact: Threads are not destroyed at JOIN; they hibernate in a thread pool to avoid OS context creation latency!", fill=(22, 101, 52), font=font_text, anchor="mm")

    img.save("extracted_images/lec15_fork_join_model.png")
    print("Saved extracted_images/lec15_fork_join_model.png")

# -------------------------------------------------------------
# 2. lec15_loop_worksharing.png
# Worksharing construct #pragma omp parallel for
# Iteration space partitioning across 4 threads
# -------------------------------------------------------------
def create_loop_worksharing():
    W, H = 1200, 600
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_subhead = get_font(14, bold=False)
    font_mono = get_font(13, bold=True)
    font_badge = get_font(14, bold=True)
    font_text = get_font(14, bold=False)

    draw.text((W // 2, 26), "OpenMP Loop Work-Sharing: Iteration Space Partitioning", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Parallelizing independent iterations of for(i=0; i<N; i++) A[i] = B[i] + k*C[i]", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 540
    p_h = 490

    # Left Box - Sequential
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 108), "Sequential Execution (1 Core)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 132), "Single thread executes all N = 1000 iterations in serial order", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Sequential iteration bar
    bar_y = 175
    draw.rounded_rectangle([70, bar_y, 550, bar_y + 45], radius=6, fill=(254, 226, 226), outline=CRIMSON, width=2)
    draw.text((310, bar_y + 22), "Iterations: i = 0, 1, 2, ..., 999 (Executed by Thread 0)", fill=CRIMSON, font=font_badge, anchor="mm")

    # Execution timeline
    draw.text((70, 245), "Sequential Time Breakdown:", fill=TEXT_DARK, font=font_badge, anchor="lm")
    draw.rounded_rectangle([70, 265, 550, 310], radius=4, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((310, 287), "Time T_seq = N x t_loop = 1000 x t_iter", fill=NAVY, font=font_mono, anchor="mm")

    # Sequential code box
    draw.rounded_rectangle([70, 335, 550, 520], radius=8, fill=(15, 23, 42), outline=LINE_COLOR, width=2)
    code_seq = [
        "// Sequential C Implementation",
        "void main() {",
        "    int i, k = 3, N = 1000;",
        "    double A[N], B[N], C[N];",
        "    // Single thread iterates 0 to N-1",
        "    for (i = 0; i < N; i++) {",
        "        A[i] = B[i] + k * C[i];",
        "    }",
        "}"
    ]
    for idx, cl in enumerate(code_seq):
        col = (148, 163, 184) if cl.startswith("//") else (248, 250, 252)
        if "for (" in cl:
            col = (253, 224, 71)
        draw.text((90, 355 + idx * 19), cl, fill=col, font=font_mono)

    # Right Box - Parallel Work-Sharing
    draw.rounded_rectangle([620, 80, 620 + p_w, 80 + p_h], radius=10, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=2)
    draw.text((620 + p_w // 2, 108), "OpenMP Parallel Work-Sharing (4 Threads)", fill=(22, 101, 52), font=font_head, anchor="mm")
    draw.text((620 + p_w // 2, 132), "Loop iterations divided equally among thread team", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 4 thread bars
    thread_data = [
        ("Thread 0", "i = 0 ... 249", (220, 252, 231), (22, 163, 74)),
        ("Thread 1", "i = 250 ... 499", (219, 234, 254), (37, 99, 235)),
        ("Thread 2", "i = 500 ... 749", (254, 243, 199), (217, 119, 6)),
        ("Thread 3", "i = 750 ... 999", (243, 232, 255), (147, 51, 234))
    ]
    t_bar_y = 170
    bw = 118
    for idx, (tname, trange, tbg, tborder) in enumerate(thread_data):
        bx = 645 + idx * (bw + 12)
        draw.rounded_rectangle([bx, t_bar_y, bx + bw, t_bar_y + 55], radius=6, fill=tbg, outline=tborder, width=2)
        draw.text((bx + bw // 2, t_bar_y + 16), tname, fill=tborder, font=font_badge, anchor="mm")
        draw.text((bx + bw // 2, t_bar_y + 38), trange, fill=TEXT_DARK, font=get_font(12, bold=True), anchor="mm")

    # Parallel Time Breakdown
    draw.text((645, 245), "Parallel Execution Timeline (All 4 threads run concurrently):", fill=TEXT_DARK, font=font_badge, anchor="lm")
    draw.rounded_rectangle([645, 265, 1135, 310], radius=4, fill=(240, 253, 244), outline=(134, 239, 172), width=1)
    draw.text((890, 287), "Time T_par = (N / P) x t_loop = 250 x t_iter   (Speedup ≈ 4x)", fill=(21, 128, 61), font=font_mono, anchor="mm")

    # Parallel code box
    draw.rounded_rectangle([645, 335, 1135, 520], radius=8, fill=(15, 23, 42), outline=LINE_COLOR, width=2)
    code_par = [
        "#include <omp.h>",
        "void main() {",
        "    int i, k = 3, N = 1000;",
        "    double A[N], B[N], C[N];",
        "    // Fork thread team and split iterations across threads",
        "    #pragma omp parallel for",
        "    for (i = 0; i < N; i++) {",
        "        A[i] = B[i] + k * C[i];",
        "    }",
        "}"
    ]
    for idx, cl in enumerate(code_par):
        col = (148, 163, 184) if cl.startswith("//") else (248, 250, 252)
        if "#pragma omp" in cl:
            col = (134, 239, 172)
        elif "for (" in cl:
            col = (253, 224, 71)
        draw.text((665, 350 + idx * 17), cl, fill=col, font=font_mono)

    # Bottom footer note
    draw.rounded_rectangle([40, 550, 1160, 585], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((600, 567), "Pragma Semantic: Combining '#pragma omp parallel' + '#pragma omp for' into '#pragma omp parallel for' creates team AND divides loop", fill=NAVY, font=font_text, anchor="mm")

    img.save("extracted_images/lec15_loop_worksharing.png")
    print("Saved extracted_images/lec15_loop_worksharing.png")

# -------------------------------------------------------------
# 3. lec15_loop_scheduling.png
# Detailed comparison of static, dynamic, guided scheduling
# -------------------------------------------------------------
def wrap_text_pixels(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        w = draw.textlength(test_line, font=font)
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def create_loop_scheduling():
    W, H = 1200, 660
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(15, bold=False)
    font_head = get_font(17, bold=True)
    font_subhead = get_font(13, bold=False)
    font_badge = get_font(13, bold=True)
    font_text = get_font(12, bold=False)
    font_mono = get_font(12, bold=True)

    draw.text((W // 2, 24), "OpenMP Loop Scheduling Policies", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 50), "How the schedule(kind [, chunk]) clause maps loop iterations onto executing threads", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    sched_types = [
        {
            "name": "1. schedule(static [, chunk])",
            "tag": "Compile-Time / Zero Overhead",
            "tag_col": (22, 101, 52),
            "tag_bg": (220, 252, 231),
            "desc": "Iterations divided into chunks of size 'chunk' and assigned round-robin to threads before loop execution.",
            "best": "Uniform, highly predictable iteration workloads with zero communication or irregular branching.",
            "chunks": [
                [("T0", "0..3"), ("T1", "4..7"), ("T2", "8..11"), ("T3", "12..15")],
                [("T0", "16..19"), ("T1", "20..23"), ("T2", "24..27"), ("T3", "28..31")]
            ],
            "adv": "Zero runtime scheduling overhead; optimal spatial memory locality.",
            "dis": "Vulnerable to severe load imbalance if iteration execution times vary."
        },
        {
            "name": "2. schedule(dynamic [, chunk])",
            "tag": "Runtime Work-Queue / Adaptive",
            "tag_col": (30, 64, 175),
            "tag_bg": (219, 234, 254),
            "desc": "Each thread grabs 'chunk' iterations off a shared work-queue; fetches a new chunk upon completion.",
            "best": "Unpredictable, irregular iterations (e.g. while loops, sparse matrices, adaptive meshes).",
            "chunks": [
                [("T1", "0..3"), ("T0", "4..7"), ("T3", "8..11"), ("T2", "12..15")],
                [("T0", "16..19"), ("T2", "20..23"), ("T1", "24..27"), ("T3", "28..31")]
            ],
            "adv": "Optimal load balancing; no thread idles while unassigned work exists.",
            "dis": "High runtime overhead due to synchronized queue locks and contention."
        },
        {
            "name": "3. schedule(guided [, chunk])",
            "tag": "Exponential Decay / Balanced",
            "tag_col": (146, 64, 14),
            "tag_bg": (254, 243, 199),
            "desc": "Chunk size is proportional to unassigned iterations / num_threads; starts large and shrinks to 'chunk'.",
            "best": "High iteration counts where workload decays or fine-tuning tail latency is needed.",
            "chunks": [
                [("T0", "0..7 (size 8)"), ("T1", "8..13 (size 6)"), ("T2", "14..18 (size 5)")],
                [("T3", "19..22 (size 4)"), ("T0", "23..25 (size 3)"), ("T1", "26..27 (size 2)")]
            ],
            "adv": "Combines low startup dispatch overhead with fine tail load balancing.",
            "dis": "Slightly higher math overhead per chunk calculation at runtime."
        }
    ]

    card_w = 360
    card_h = 535
    start_x = 35
    top_y = 74

    for idx, s in enumerate(sched_types):
        cx = start_x + idx * (card_w + 30)
        cy = top_y
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)

        # Header
        draw.text((cx + 15, cy + 22), s["name"], fill=NAVY, font=font_head, anchor="lm")
        # Tag
        tw = 215
        draw.rounded_rectangle([cx + 15, cy + 38, cx + 15 + tw, cy + 60], radius=4, fill=s["tag_bg"], outline=s["tag_col"], width=1)
        draw.text((cx + 15 + tw // 2, cy + 49), s["tag"], fill=s["tag_col"], font=font_badge, anchor="mm")

        # Description
        desc_lines = wrap_text_pixels(s["desc"], font_text, card_w - 30, draw)
        for l_idx, dl in enumerate(desc_lines[:3]):
            draw.text((cx + 15, cy + 72 + l_idx * 15), dl, fill=TEXT_DARK, font=font_text)

        # Work allocation timeline box
        draw.rounded_rectangle([cx + 12, cy + 120, cx + card_w - 12, cy + 252], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
        draw.text((cx + 20, cy + 134), "Iteration Chunk Allocation (N=32):", fill=NAVY_LIGHT, font=font_badge, anchor="lm")

        # Draw chunk blocks
        y_offset = cy + 152
        t_colors = {
            "T0": ((220, 252, 231), (22, 163, 74)),
            "T1": ((219, 234, 254), (37, 99, 235)),
            "T2": ((254, 243, 199), (217, 119, 6)),
            "T3": ((243, 232, 255), (147, 51, 234))
        }

        for row_idx, r_chunks in enumerate(s["chunks"]):
            x_curr = cx + 20
            ry = y_offset + row_idx * 44
            draw.text((cx + 20, ry), f"Pass {row_idx + 1}:", fill=TEXT_MUTED, font=font_text, anchor="lm")
            ry += 10
            for c_tid, c_label in r_chunks:
                bg, brd = t_colors[c_tid]
                bw = 70 if idx < 2 else 95
                draw.rounded_rectangle([x_curr, ry, x_curr + bw, ry + 24], radius=4, fill=bg, outline=brd, width=1)
                draw.text((x_curr + bw // 2, ry + 12), f"{c_tid}: {c_label}", fill=TEXT_DARK, font=get_font(10, bold=True), anchor="mm")
                x_curr += bw + 6

        # Best For Box (DEDICATED STYLED CALLOUT)
        draw.rounded_rectangle([cx + 12, cy + 262, cx + card_w - 12, cy + 342], radius=6, fill=(254, 252, 232), outline=(234, 179, 8), width=1)
        draw.text((cx + 20, cy + 276), "[*] Best Suited For:", fill=(146, 64, 14), font=font_badge, anchor="lm")
        best_lines = wrap_text_pixels(s["best"], font_text, card_w - 44, draw)
        for b_idx, bl in enumerate(best_lines[:3]):
            draw.text((cx + 20, cy + 296 + b_idx * 15), bl, fill=TEXT_DARK, font=font_text)

        # Advantage Box
        draw.rounded_rectangle([cx + 12, cy + 352, cx + card_w - 12, cy + 432], radius=6, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
        draw.text((cx + 20, cy + 366), "[+] Advantage:", fill=(22, 101, 52), font=font_badge, anchor="lm")
        adv_lines = wrap_text_pixels(s["adv"], font_text, card_w - 44, draw)
        for a_idx, al in enumerate(adv_lines[:3]):
            draw.text((cx + 20, cy + 386 + a_idx * 15), al, fill=TEXT_DARK, font=font_text)

        # Bottleneck Box
        draw.rounded_rectangle([cx + 12, cy + 442, cx + card_w - 12, cy + 522], radius=6, fill=CARD_BG_BAD, outline=CARD_BORDER_BAD, width=1)
        draw.text((cx + 20, cy + 456), "[-] Bottleneck:", fill=CRIMSON, font=font_badge, anchor="lm")
        dis_lines = wrap_text_pixels(s["dis"], font_text, card_w - 44, draw)
        for d_idx, dl in enumerate(dis_lines[:3]):
            draw.text((cx + 20, cy + 476 + d_idx * 15), dl, fill=TEXT_DARK, font=font_text)

    # Bottom summary comparison note
    draw.rounded_rectangle([35, 620, 1165, 650], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((W // 2, 635), "Design Rule: Use static for uniform loops; dynamic for heavy load-imbalance; guided to balance overhead & tail latency.", fill=NAVY, font=font_text, anchor="mm")

    img.save("extracted_images/lec15_loop_scheduling.png")
    print("Saved extracted_images/lec15_loop_scheduling.png")

# -------------------------------------------------------------
# 4. lec15_reduction_tree.png
# OpenMP reduction clause mechanics: local copies + tree reduction
# -------------------------------------------------------------
def create_reduction_tree():
    W, H = 1200, 620
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(17, bold=True)
    font_subhead = get_font(14, bold=False)
    font_badge = get_font(13, bold=True)
    font_text = get_font(13, bold=False)
    font_mono = get_font(13, bold=True)

    draw.text((W // 2, 26), "OpenMP Reduction Clause Architecture: reduction(+:sum)", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Eliminating loop-carried race conditions via thread-private accumulation and logarithmic tree reduction", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    left_w = 400
    right_w = 720
    top_y = 80
    h_box = 500

    # Left Box: Race condition
    draw.rounded_rectangle([35, top_y, 35 + left_w, top_y + h_box], radius=10, fill=CARD_BG_BAD, outline=CARD_BORDER_BAD, width=2)
    draw.text((35 + left_w // 2, top_y + 24), "Naive Parallel Loop (Data Race)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((35 + left_w // 2, top_y + 46), "Multiple threads write to shared 'sum'", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Code
    draw.rounded_rectangle([55, top_y + 70, 55 + left_w - 40, top_y + 190], radius=6, fill=(15, 23, 42), outline=LINE_COLOR, width=1)
    race_code = [
        "// NAIVE CODE: SEVERE BUG!",
        "int sum = 0;",
        "#pragma omp parallel for",
        "for (i = 0; i < N; i++) {",
        "    sum += A[i]; // RACE CONDITION!",
        "}"
    ]
    for idx, rc in enumerate(race_code):
        col = (252, 165, 165) if "BUG" in rc or "RACE" in rc else (248, 250, 252)
        draw.text((70, top_y + 85 + idx * 17), rc, fill=col, font=font_mono)

    # Diagram of 4 threads colliding on 1 memory address
    draw.ellipse([35 + left_w // 2 - 45, top_y + 260, 35 + left_w // 2 + 45, top_y + 350], fill=(254, 202, 202), outline=CRIMSON, width=3)
    draw.text((35 + left_w // 2, top_y + 295), "Shared Memory", fill=CRIMSON, font=font_badge, anchor="mm")
    draw.text((35 + left_w // 2, top_y + 315), "int sum = ???", fill=TEXT_DARK, font=font_mono, anchor="mm")

    threads_left = [
        ("T0", 75, top_y + 230),
        ("T1", 75, top_y + 390),
        ("T2", 390, top_y + 230),
        ("T3", 390, top_y + 390)
    ]
    for tname, tx, ty in threads_left:
        draw.ellipse([tx - 20, ty - 20, tx + 20, ty + 20], fill=(254, 226, 226), outline=CRIMSON, width=2)
        draw.text((tx, ty), tname, fill=CRIMSON, font=font_badge, anchor="mm")
        draw.line([(tx, ty), (35 + left_w // 2, top_y + 305)], fill=CRIMSON, width=2)

    draw.rounded_rectangle([55, top_y + 420, 55 + left_w - 40, top_y + 480], radius=6, fill=(255, 255, 255), outline=CRIMSON, width=1)
    draw.text((35 + left_w // 2, top_y + 440), "Concurrent Read-Modify-Write", fill=CRIMSON, font=font_badge, anchor="mm")
    draw.text((35 + left_w // 2, top_y + 460), "Causes lost updates & non-deterministic output!", fill=TEXT_DARK, font=font_text, anchor="mm")

    # Right Box: OpenMP Reduction Mechanism
    rx = 455
    draw.rounded_rectangle([rx, top_y, rx + right_w, top_y + h_box], radius=10, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=2)
    draw.text((rx + right_w // 2, top_y + 24), "OpenMP reduction(+:sum) Architecture", fill=(22, 101, 52), font=font_head, anchor="mm")
    draw.text((rx + right_w // 2, top_y + 46), "Phase 1: Local accumulation; Phase 2: Lock-free tree reduction", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Step 1: Thread-private copies
    draw.text((rx + 30, top_y + 75), "Phase 1: Thread-Private Local Copies Initialized to Identity (0)", fill=NAVY, font=font_badge, anchor="lm")
    t_boxes = [
        ("T0", "local_sum_0 = 0", "accumulates A[0..249]", 480),
        ("T1", "local_sum_1 = 0", "accumulates A[250..499]", 650),
        ("T2", "local_sum_2 = 0", "accumulates A[500..749]", 820),
        ("T3", "local_sum_3 = 0", "accumulates A[750..999]", 990)
    ]
    for tid, lvar, lacc, bx in t_boxes:
        draw.rounded_rectangle([bx, top_y + 95, bx + 155, top_y + 165], radius=6, fill=(255, 255, 255), outline=NAVY_LIGHT, width=2)
        draw.text((bx + 77, top_y + 115), f"{tid}: {lvar}", fill=NAVY, font=get_font(12, bold=True), anchor="mm")
        draw.text((bx + 77, top_y + 138), lacc, fill=TEXT_MUTED, font=get_font(11, bold=False), anchor="mm")

    # Arrows pointing down to tree reduction
    draw.text((rx + 30, top_y + 190), "Phase 2: Tree Reduction at Implicit Barrier (Logarithmic Depth)", fill=NAVY, font=font_badge, anchor="lm")

    # Tree reduction level 1
    # Pair (T0, T1) -> sum_01; Pair (T2, T3) -> sum_23
    draw.line([(557, top_y + 165), (630, top_y + 235)], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([(727, top_y + 165), (630, top_y + 235)], fill=HIGHLIGHT_BLUE, width=2)
    draw.rounded_rectangle([560, top_y + 235, 700, top_y + 285], radius=6, fill=(219, 234, 254), outline=(37, 99, 235), width=2)
    draw.text((630, top_y + 260), "sum_0 + sum_1", fill=(30, 64, 175), font=font_mono, anchor="mm")

    draw.line([(897, top_y + 165), (970, top_y + 235)], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([(1067, top_y + 165), (970, top_y + 235)], fill=HIGHLIGHT_BLUE, width=2)
    draw.rounded_rectangle([900, top_y + 235, 1040, top_y + 285], radius=6, fill=(219, 234, 254), outline=(37, 99, 235), width=2)
    draw.text((970, top_y + 260), "sum_2 + sum_3", fill=(30, 64, 175), font=font_mono, anchor="mm")

    # Tree reduction level 2
    draw.line([(630, top_y + 285), (800, top_y + 345)], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([(970, top_y + 285), (800, top_y + 345)], fill=HIGHLIGHT_BLUE, width=2)
    draw.rounded_rectangle([720, top_y + 345, 880, top_y + 400], radius=6, fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.text((800, top_y + 372), "(sum_01) + (sum_23)", fill=(21, 128, 61), font=font_mono, anchor="mm")

    # Commit to shared global sum
    draw.line([(800, top_y + 400), (800, top_y + 430)], fill=(22, 163, 74), width=3)
    draw.rounded_rectangle([680, top_y + 430, 920, top_y + 485], radius=8, fill=(255, 255, 255), outline=(22, 163, 74), width=3)
    draw.text((800, top_y + 448), "Global Shared: sum += total", fill=(21, 128, 61), font=font_head, anchor="mm")
    draw.text((800, top_y + 470), "Updated atomically by Master thread at Join", fill=TEXT_MUTED, font=font_text, anchor="mm")

    # Footer note
    draw.rounded_rectangle([35, 590, 1175, 615], radius=4, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((W // 2, 602), "Identity Elements: (+, -) -> 0; (* ) -> 1; (&) -> ~0; (|) -> 0; (max) -> -INF; (min) -> +INF", fill=NAVY, font=font_text, anchor="mm")

    img.save("extracted_images/lec15_reduction_tree.png")
    print("Saved extracted_images/lec15_reduction_tree.png")

# -------------------------------------------------------------
# 5. lec15_shared_vs_private.png
# Memory scoping: Shared address space vs Thread-Private stacks
# -------------------------------------------------------------
def create_shared_vs_private():
    W, H = 1200, 620
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(17, bold=True)
    font_subhead = get_font(14, bold=False)
    font_badge = get_font(13, bold=True)
    font_text = get_font(13, bold=False)
    font_mono = get_font(12, bold=True)

    draw.text((W // 2, 26), "OpenMP Data Environment: Shared vs. Private Scoping", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Understanding memory visibility, thread-private stacks, and data race prevention", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    # Global Shared Address Space Box
    draw.rounded_rectangle([40, 80, 1160, 240], radius=10, fill=(238, 242, 255), outline=(199, 210, 254), width=2)
    draw.text((600, 105), "Shared Address Space (Accessible by ALL Threads Simultaneously)", fill=NAVY, font=font_head, anchor="mm")
    draw.text((600, 128), "Global heap, static data, and variables declared before '#pragma omp parallel'", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    shared_vars = [
        ("double A[N]", "Global Array", (219, 234, 254), (37, 99, 235)),
        ("double B[N]", "Global Array", (219, 234, 254), (37, 99, 235)),
        ("double C[N]", "Global Array", (219, 234, 254), (37, 99, 235)),
        ("int k = 3", "Shared Scalar", (254, 243, 199), (217, 119, 6)),
        ("int N = 1000", "Shared Constant", (254, 243, 199), (217, 119, 6))
    ]
    sx_start = 75
    sb_w = 195
    for idx, (vname, vdesc, vbg, vborder) in enumerate(shared_vars):
        bx = sx_start + idx * (sb_w + 25)
        draw.rounded_rectangle([bx, 150, bx + sb_w, 220], radius=6, fill=vbg, outline=vborder, width=2)
        draw.text((bx + sb_w // 2, 175), vname, fill=TEXT_DARK, font=font_mono, anchor="mm")
        draw.text((bx + sb_w // 2, 200), vdesc, fill=TEXT_MUTED, font=font_text, anchor="mm")

    # 4 Thread-Private Boxes
    tp_y = 280
    tp_h = 240
    tp_w = 260
    gap = 25
    start_x = 45

    threads_private = [
        ("Thread 0", 0, "i = 0 ... 249", "tid = 0", (22, 163, 74), (240, 253, 244), (134, 239, 172)),
        ("Thread 1", 1, "i = 250 ... 499", "tid = 1", (37, 99, 235), (239, 246, 255), (191, 219, 254)),
        ("Thread 2", 2, "i = 500 ... 749", "tid = 2", (217, 119, 6), (254, 252, 232), (253, 224, 71)),
        ("Thread 3", 3, "i = 750 ... 999", "tid = 3", (147, 51, 234), (250, 245, 255), (233, 213, 255))
    ]

    for idx, (tname, tid, irange, tid_var, col, bg, border) in enumerate(threads_private):
        tx = start_x + idx * (tp_w + gap)
        draw.rounded_rectangle([tx, tp_y, tx + tp_w, tp_y + tp_h], radius=8, fill=bg, outline=border, width=2)

        draw.text((tx + tp_w // 2, tp_y + 22), tname, fill=col, font=font_head, anchor="mm")
        draw.text((tx + tp_w // 2, tp_y + 44), "Private Thread Stack Memory", fill=TEXT_MUTED, font=get_font(12, bold=False), anchor="mm")

        # Private variables inside stack
        draw.rounded_rectangle([tx + 15, tp_y + 65, tx + tp_w - 15, tp_y + 115], radius=6, fill=(255, 255, 255), outline=border, width=1)
        draw.text((tx + 25, tp_y + 82), "Loop Index: int i", fill=CRIMSON, font=font_badge, anchor="lm")
        draw.text((tx + 25, tp_y + 102), f"Range: {irange}", fill=TEXT_DARK, font=font_text, anchor="lm")

        draw.rounded_rectangle([tx + 15, tp_y + 125, tx + tp_w - 15, tp_y + 175], radius=6, fill=(255, 255, 255), outline=border, width=1)
        draw.text((tx + 25, tp_y + 142), "Thread ID: my_id", fill=col, font=font_badge, anchor="lm")
        draw.text((tx + 25, tp_y + 162), f"omp_get_thread_num() -> {tid}", fill=TEXT_DARK, font=font_text, anchor="lm")

        draw.rounded_rectangle([tx + 15, tp_y + 185, tx + tp_w - 15, tp_y + 225], radius=6, fill=(255, 255, 255), outline=border, width=1)
        draw.text((tx + tp_w // 2, tp_y + 205), "Local Registers & Cache", fill=TEXT_MUTED, font=font_text, anchor="mm")

        # Dotted read/write arrows between thread and shared space
        arr_x = tx + tp_w // 2
        for y_dot in range(240, tp_y, 6):
            draw.line([(arr_x, y_dot), (arr_x, y_dot + 3)], fill=col, width=2)
        draw.polygon([(arr_x - 4, 245), (arr_x + 4, 245), (arr_x, 240)], fill=col)

    # Scoping clause table / rules at bottom
    draw.rounded_rectangle([40, 540, 1160, 605], radius=8, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    rules = [
        "shared(var): One copy in global memory; all threads read/write (danger: data race)",
        "private(var): Each thread gets uninitialized stack copy; undefined at exit",
        "firstprivate(var): Private copy initialized with the master thread's value before parallel region",
        "default(none): Enforces explicit scoping of all variables; prevents accidental race conditions"
    ]
    for r_idx, r_text in enumerate(rules):
        col = NAVY if r_idx < 2 else CRIMSON if r_idx == 3 else TEXT_DARK
        draw.text((60, 555 + r_idx * 14), f"• {r_text}", fill=col, font=get_font(12, bold=(r_idx==3)))

    img.save("extracted_images/lec15_shared_vs_private.png")
    print("Saved extracted_images/lec15_shared_vs_private.png")

if __name__ == "__main__":
    create_fork_join_model()
    create_loop_worksharing()
    create_loop_scheduling()
    create_reduction_tree()
    create_shared_vs_private()
    print("All Lecture 15 diagrams created successfully!")
