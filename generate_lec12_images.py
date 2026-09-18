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
BOX_BORDER = (71, 85, 105)
LINE_COLOR = (51, 65, 85)
HIGHLIGHT_BLUE = (37, 99, 235)
HIGHLIGHT_RED = (220, 38, 38)
HIGHLIGHT_GREEN = (16, 185, 129)

COLOR_COMP = (30, 41, 59)         # Dark slate/black for essential/excess computation
COLOR_COMM = (148, 163, 184)      # Medium slate for communication
COLOR_IDLE = (255, 255, 255)      # White with border for idling

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
# 1. lec12_overhead_breakdown.png (Slide 4: Overhead Gantt Chart)
# -------------------------------------------------------------
def create_overhead_breakdown():
    W, H = 1000, 520
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(20, bold=True)
    font_label = get_font(15, bold=True)
    font_sm = get_font(13, bold=False)

    # Title & Axes
    draw.text((W // 2, 30), "Overhead Breakdown Across Processors (P0 – P7)", fill=NAVY, font=font_title, anchor="mm")

    x_start = 120
    x_end = 880
    bar_w = x_end - x_start

    # Draw Execution Time axis arrow
    y_axis = 75
    draw.text((x_start + bar_w // 2, y_axis - 15), "Execution Time (Tp)  ──►", fill=TEXT_DARK, font=font_label, anchor="mm")
    draw.line([x_start, y_axis, x_end, y_axis], fill=LINE_COLOR, width=2)
    draw.polygon([(x_end, y_axis - 5), (x_end + 10, y_axis), (x_end, y_axis + 5)], fill=LINE_COLOR)

    # Processors P0 to P7
    # Segments: list of (type, width_ratio)
    # type: 'comp', 'comm', 'idle'
    proc_segments = [
        # P0
        [('comp', 0.35), ('comm', 0.12), ('comp', 0.28), ('comm', 0.10), ('comp', 0.15)],
        # P1
        [('comp', 0.20), ('comm', 0.15), ('comp', 0.15), ('comm', 0.10), ('idle', 0.20), ('comp', 0.20)],
        # P2
        [('comp', 0.28), ('comm', 0.08), ('idle', 0.18), ('comp', 0.22), ('comm', 0.09), ('comp', 0.15)],
        # P3
        [('comp', 0.40), ('idle', 0.15), ('comp', 0.15), ('comm', 0.12), ('idle', 0.08), ('comp', 0.10)],
        # P4
        [('comp', 0.32), ('comm', 0.10), ('idle', 0.12), ('comp', 0.26), ('comm', 0.05), ('comp', 0.15)],
        # P5
        [('comp', 0.35), ('comm', 0.05), ('idle', 0.25), ('comp', 0.18), ('comm', 0.05), ('comp', 0.12)],
        # P6
        [('comp', 0.52), ('idle', 0.15), ('comp', 0.15), ('comm', 0.08), ('comp', 0.10)],
        # P7
        [('comp', 0.48), ('comm', 0.08), ('idle', 0.18), ('comp', 0.16), ('idle', 0.10)],
    ]

    y_bar_start = 100
    bar_height = 32
    y_gap = 42

    for i, segs in enumerate(proc_segments):
        y = y_bar_start + i * y_gap
        # Processor label
        draw.text((x_start - 25, y + bar_height // 2), f"P{i}", fill=NAVY, font=font_label, anchor="mm")

        # Draw segments
        cur_x = x_start
        for stype, ratio in segs:
            seg_w = ratio * bar_w
            x1 = cur_x
            x2 = cur_x + seg_w
            cur_x = x2

            if stype == 'comp':
                fill_col = COLOR_COMP
                draw.rectangle([x1, y, x2, y + bar_height], fill=fill_col, outline=LINE_COLOR, width=1)
            elif stype == 'comm':
                fill_col = COLOR_COMM
                draw.rectangle([x1, y, x2, y + bar_height], fill=fill_col, outline=LINE_COLOR, width=1)
            else: # idle
                fill_col = COLOR_IDLE
                draw.rectangle([x1, y, x2, y + bar_height], fill=fill_col, outline=BOX_BORDER, width=1)
                # subtle hatch/dot
                draw.line([x1, y, x2, y + bar_height], fill=(226, 232, 240), width=1)

    # Vertical finish line at Tp
    draw.line([x_end, y_bar_start - 5, x_end, y_bar_start + 8 * y_gap - 10], fill=CRIMSON, width=2)
    draw.text((x_end, y_bar_start + 8 * y_gap), "Tp (Wall Clock Time)", fill=CRIMSON, font=font_label, anchor="mm")

    # Legend at bottom
    y_leg = 465
    draw.rectangle([200, y_leg - 10, 800, y_leg + 25], fill=(241, 245, 249), outline=BOX_BORDER, width=1)

    # Comp
    draw.rectangle([220, y_leg, 245, y_leg + 16], fill=COLOR_COMP, outline=LINE_COLOR, width=1)
    draw.text((255, y_leg + 8), "Essential / Excess Computation", fill=TEXT_DARK, font=font_sm, anchor="lm")

    # Comm
    draw.rectangle([450, y_leg, 475, y_leg + 16], fill=COLOR_COMM, outline=LINE_COLOR, width=1)
    draw.text((485, y_leg + 8), "Interprocessor Communication", fill=TEXT_DARK, font=font_sm, anchor="lm")

    # Idle
    draw.rectangle([680, y_leg, 705, y_leg + 16], fill=COLOR_IDLE, outline=BOX_BORDER, width=1)
    draw.line([680, y_leg, 705, y_leg + 16], fill=(203, 213, 225), width=1)
    draw.text((715, y_leg + 8), "Idling", fill=TEXT_DARK, font=font_sm, anchor="lm")

    img.save("extracted_images/lec12_overhead_breakdown.png", dpi=(300, 300))
    print("Saved lec12_overhead_breakdown.png")

# -------------------------------------------------------------
# 2. lec12_tree_addition.png (Slide 10: 16-element tree reduction)
# -------------------------------------------------------------
def create_tree_addition():
    W, H = 1100, 680
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(18, bold=True)
    font_step = get_font(14, bold=True)
    font_node = get_font(13, bold=True)
    font_sum = get_font(12, bold=True)

    draw.text((W // 2, 25), "Tree-Structured Reduction for Adding 16 Numbers on 16 Processors", fill=NAVY, font=font_title, anchor="mm")

    n_procs = 16
    x_left = 140
    x_right = 1040
    dx = (x_right - x_left) / (n_procs - 1)

    steps = [
        ("(a) Step 1 (stride 1): Odd ranks send to even neighbors", 1, 95),
        ("(b) Step 2 (stride 2): Active ranks send to distance 2", 2, 215),
        ("(c) Step 3 (stride 4): Active ranks send to distance 4", 4, 335),
        ("(d) Step 4 (stride 8): Rank 8 sends to Rank 0", 8, 455),
        ("(e) Final State: Sum accumulated at Processing Element 0", 0, 575)
    ]

    def get_proc_x(rank):
        return int(x_left + rank * dx)

    # Draw each step
    for step_idx, (title, stride, y_base) in enumerate(steps):
        draw.text((60, y_base - 22), title, fill=NAVY_LIGHT, font=font_step, anchor="lm")

        # Draw processors 0..15
        for p in range(n_procs):
            px = get_proc_x(p)
            r = 14

            # Highlight active processors
            is_active = (stride == 0 and p == 0) or (stride > 0 and (p % stride == 0))
            if is_active:
                fill_c = (239, 246, 255)
                outline_c = HIGHLIGHT_BLUE
            else:
                fill_c = (248, 250, 252)
                outline_c = TEXT_MUTED

            draw.ellipse([px - r, y_base - r, px + r, y_base + r], fill=fill_c, outline=outline_c, width=2)
            draw.text((px, y_base), str(p), fill=TEXT_DARK, font=font_node, anchor="mm")

            # Label partial sum above active nodes
            if step_idx == 0:
                draw.text((px, y_base - 22), f"{p}", fill=TEXT_MUTED, font=font_sum, anchor="mm")
            elif step_idx == 1:
                if p % 2 == 0:
                    draw.text((px, y_base - 22), f"Σ_{p}^{p+1}", fill=CRIMSON, font=font_sum, anchor="mm")
            elif step_idx == 2:
                if p % 4 == 0:
                    draw.text((px, y_base - 22), f"Σ_{p}^{p+3}", fill=CRIMSON, font=font_sum, anchor="mm")
            elif step_idx == 3:
                if p % 8 == 0:
                    draw.text((px, y_base - 22), f"Σ_{p}^{p+7}", fill=CRIMSON, font=font_sum, anchor="mm")
            elif step_idx == 4:
                if p == 0:
                    draw.text((px, y_base - 22), "Σ_0^15 (Total Sum)", fill=CRIMSON, font=font_title, anchor="mm")

        # Draw curved arrows for communication
        if stride > 0:
            for src in range(stride, n_procs, stride * 2):
                dst = src - stride
                x_src = get_proc_x(src)
                x_dst = get_proc_x(dst)
                y_node = y_base

                # Draw curved arc underneath
                arc_h = min(22 + stride * 4, 45)
                mid_x = (x_src + x_dst) / 2
                mid_y = y_node + arc_h

                # Approximate arc with line segments
                pts = []
                for t in range(21):
                    param = t / 20.0
                    # quadratic bezier
                    bx = (1 - param)**2 * x_src + 2 * (1 - param) * param * mid_x + param**2 * x_dst
                    by = (1 - param)**2 * (y_node + 14) + 2 * (1 - param) * param * mid_y + param**2 * (y_node + 14)
                    pts.append((bx, by))

                for k in range(len(pts) - 1):
                    draw.line([pts[k], pts[k+1]], fill=HIGHLIGHT_BLUE, width=2)

                # Arrow head at dst
                ax = x_dst
                ay = y_node + 14
                draw.polygon([(ax, ay), (ax + 6, ay + 7), (ax + 2, ay + 10)], fill=HIGHLIGHT_BLUE)

    img.save("extracted_images/lec12_tree_addition.png", dpi=(300, 300))
    print("Saved lec12_tree_addition.png")

# -------------------------------------------------------------
# 3. lec12_circuit_model_sum.png (Slide 18: Circuit Binary Tree)
# -------------------------------------------------------------
def create_circuit_model_sum():
    W, H = 1000, 580
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(20, bold=True)
    font_head = get_font(16, bold=True)
    font_bold = get_font(15, bold=True)
    font_sm = get_font(13, bold=False)

    draw.text((W // 2, 30), "Circuit Model: Binary Tree Adder for n = 16 Inputs", fill=NAVY, font=font_title, anchor="mm")

    # Table columns: Left = Depth, Right = Work
    draw.text((120, 75), "Depth", fill=NAVY, font=font_head, anchor="mm")
    draw.text((880, 75), "Work (Adders)", fill=NAVY, font=font_head, anchor="mm")

    # Levels
    levels = [
        (1, 8, 140, "8 adders"),
        (2, 4, 230, "4 adders"),
        (3, 2, 320, "2 adders"),
        (4, 1, 410, "1 adder")
    ]

    # Node positions per level
    node_positions = {}
    box_w, box_h = 32, 32

    for lvl, count, y_pos, desc in levels:
        draw.text((120, y_pos), "1", fill=TEXT_DARK, font=font_bold, anchor="mm")
        draw.text((880, y_pos), str(count), fill=TEXT_DARK, font=font_bold, anchor="mm")

        # spread count nodes horizontally between 220 and 780
        x_min = 220
        x_max = 780
        span = x_max - x_min
        dx = span / (count)
        positions = []
        for j in range(count):
            x = x_min + dx * (j + 0.5)
            positions.append((x, y_pos))
        node_positions[lvl] = positions

    # Draw inputs entering Level 1
    lvl1_positions = node_positions[1]
    for j, (nx, ny) in enumerate(lvl1_positions):
        # 2 inputs per adder
        in1_x = nx - 14
        in2_x = nx + 14
        draw.line([in1_x, ny - 30, nx - 6, ny - box_h // 2], fill=LINE_COLOR, width=2)
        draw.line([in2_x, ny - 30, nx + 6, ny - box_h // 2], fill=LINE_COLOR, width=2)

    # Draw inter-level edges
    for lvl in [1, 2, 3]:
        src_positions = node_positions[lvl]
        dst_positions = node_positions[lvl + 1]
        for j, (sx, sy) in enumerate(src_positions):
            dst_node = dst_positions[j // 2]
            dx_dst, dy_dst = dst_node
            offset = -6 if (j % 2 == 0) else 6
            draw.line([sx, sy + box_h // 2, dx_dst + offset, dy_dst - box_h // 2], fill=LINE_COLOR, width=2)

    # Draw nodes
    for lvl, positions in node_positions.items():
        for nx, ny in positions:
            draw.rectangle([nx - box_w // 2, ny - box_h // 2, nx + box_w // 2, ny + box_h // 2],
                           fill=(241, 245, 249), outline=NAVY, width=2)
            draw.text((nx, ny - 1), "+", fill=NAVY, font=font_bold, anchor="mm")

    # Draw output edge from root
    root_x, root_y = node_positions[4][0]
    draw.line([root_x, root_y + box_h // 2, root_x, root_y + box_h // 2 + 35], fill=CRIMSON, width=3)
    draw.polygon([(root_x, root_y + box_h // 2 + 45), (root_x - 6, root_y + box_h // 2 + 33), (root_x + 6, root_y + box_h // 2 + 33)], fill=CRIMSON)
    draw.text((root_x, root_y + box_h // 2 + 55), "Output (Final Sum)", fill=CRIMSON, font=font_bold, anchor="mm")

    # Divider line
    draw.line([80, 465, 920, 465], fill=BOX_BORDER, width=1)

    # Totals
    draw.text((120, 490), "Total Depth: 4", fill=CRIMSON, font=font_bold, anchor="mm")
    draw.text((880, 490), "Total Work: 15", fill=CRIMSON, font=font_bold, anchor="mm")
    draw.text((W // 2, 490), "General Case:  W(n) = n - 1 = Θ(n)   |   D(n) = log₂ n = Θ(log n)", fill=NAVY, font=font_bold, anchor="mm")
    draw.text((W // 2, 525), "Parallelism: P = W / D = (n - 1) / log₂ n  •  Algorithm is Work-Efficient (matches sequential O(n))", fill=TEXT_DARK, font=font_sm, anchor="mm")

    img.save("extracted_images/lec12_circuit_model_sum.png", dpi=(300, 300))
    print("Saved lec12_circuit_model_sum.png")

# -------------------------------------------------------------
# 4. lec12_superlinear_cache.png (Slide 19-20: Example 5.3 Cache Effects)
# -------------------------------------------------------------
def create_superlinear_cache():
    W, H = 1050, 560
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(20, bold=True)
    font_head = get_font(16, bold=True)
    font_bold = get_font(14, bold=True)
    font_body = get_font(13, bold=False)
    font_mono = get_font(13, bold=True)

    draw.text((W // 2, 30), "Hardware Superlinear Speedup: Cache Hierarchy Effects (Example 5.3)", fill=NAVY, font=font_title, anchor="mm")

    # Left: Single Processor
    draw.rectangle([50, 70, 480, 440], fill=(248, 250, 252), outline=BOX_BORDER, width=2)
    draw.rectangle([50, 70, 480, 110], fill=NAVY, outline=NAVY, width=1)
    draw.text((265, 90), "Single Processor (p = 1)", fill=(255, 255, 255), font=font_head, anchor="mm")

    # Working set box
    draw.rectangle([80, 125, 450, 160], fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((265, 142), "Working Set: M  (Exceeds Cache Capacity)", fill=TEXT_DARK, font=font_bold, anchor="mm")

    # Cache box
    draw.rectangle([80, 180, 450, 245], fill=(220, 252, 231), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((265, 200), "L1/L2 Cache: 64 KB", fill=TEXT_DARK, font=font_bold, anchor="mm")
    draw.text((265, 225), "Hit Ratio: h₁ = 80%  (Latency = 2 ns)", fill=TEXT_DARK, font=font_mono, anchor="mm")

    # DRAM box
    draw.rectangle([80, 265, 450, 330], fill=(254, 226, 226), outline=HIGHLIGHT_RED, width=2)
    draw.text((265, 285), "DRAM Main Memory", fill=TEXT_DARK, font=font_bold, anchor="mm")
    draw.text((265, 310), "Miss Ratio: 20%  (Latency = 100 ns)", fill=CRIMSON, font=font_mono, anchor="mm")

    # Single proc latency calculation
    draw.rectangle([80, 350, 450, 420], fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((265, 370), "Average Access Time (t_seq):", fill=NAVY, font=font_bold, anchor="mm")
    draw.text((265, 395), "t_seq = 0.8(2) + 0.2(100) = 21.6 ns", fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Right: Two Processors
    draw.rectangle([520, 70, 1000, 440], fill=(248, 250, 252), outline=BOX_BORDER, width=2)
    draw.rectangle([520, 70, 1000, 110], fill=NAVY_LIGHT, outline=NAVY_LIGHT, width=1)
    draw.text((760, 90), "Two Processors (p = 2)", fill=(255, 255, 255), font=font_head, anchor="mm")

    # Partitioned Working set box
    draw.rectangle([550, 125, 970, 160], fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((760, 142), "Partitioned Working Set: M/2 per Proc (Fits Cache!)", fill=TEXT_DARK, font=font_bold, anchor="mm")

    # Aggregate Cache box
    draw.rectangle([550, 180, 970, 245], fill=(220, 252, 231), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((760, 200), "Aggregate Cache: 2 × 64 KB = 128 KB", fill=TEXT_DARK, font=font_bold, anchor="mm")
    draw.text((760, 225), "Hit Ratio climbs to: h₂ = 90%  (Latency = 2 ns)", fill=HIGHLIGHT_GREEN, font=font_mono, anchor="mm")

    # DRAM Partition
    draw.rectangle([550, 265, 970, 330], fill=(254, 226, 226), outline=HIGHLIGHT_RED, width=2)
    draw.text((760, 285), "Local DRAM: 8% (100 ns)  |  Remote DRAM: 2% (400 ns)", fill=TEXT_DARK, font=font_mono, anchor="mm")
    draw.text((760, 310), "Interconnect penalty on remote misses", fill=TEXT_MUTED, font=font_body, anchor="mm")

    # Two proc latency calculation
    draw.rectangle([550, 350, 970, 420], fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((760, 370), "Average Access Time (t_par):", fill=NAVY, font=font_bold, anchor="mm")
    draw.text((760, 395), "t_par = 0.9(2) + 0.08(100) + 0.02(400) = 17.8 ns", fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Bottom Banner: Speedup Calculation
    draw.rectangle([50, 460, 1000, 530], fill=(241, 245, 249), outline=CRIMSON, width=2)
    draw.text((W // 2, 480), "Ts = N × 21.6 ns    |    Tp = (N / 2) × 17.8 ns = N × 8.9 ns", fill=NAVY, font=font_bold, anchor="mm")
    draw.text((W // 2, 508), "Speedup S = Ts / Tp = 21.6 / 8.9 ≈ 2.43 > 2.0  (Superlinear Speedup!)", fill=CRIMSON, font=font_head, anchor="mm")

    img.save("extracted_images/lec12_superlinear_cache.png", dpi=(300, 300))
    print("Saved lec12_superlinear_cache.png")

if __name__ == "__main__":
    create_overhead_breakdown()
    create_tree_addition()
    create_circuit_model_sum()
    create_superlinear_cache()
    print("All Lecture 12 images generated successfully!")
