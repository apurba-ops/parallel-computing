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
        bbox = draw.textbbox((0, 0), test_line, font=font)
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
# 1. lec18_processes_vs_processors.png
# Processes vs Processors: Virtualization Hierarchy & Binding
# -------------------------------------------------------------
def create_processes_vs_processors():
    SCALE = 2
    BASE_W, BASE_H = 1240, 580
    W, H = BASE_W * SCALE, BASE_H * SCALE

    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts scaled up for maximum legibility
    font_head = get_font(21 * SCALE, bold=True)
    font_subhead = get_font(13 * SCALE, bold=False)
    font_card_title = get_font(15 * SCALE, bold=True)
    font_card_body = get_font(13 * SCALE, bold=False)
    font_arrow = get_font(12 * SCALE, bold=True)
    font_bullet = get_font(13 * SCALE, bold=False)
    font_bullet_bold = get_font(13 * SCALE, bold=True)

    margin_x = 18 * SCALE
    margin_y = 14 * SCALE
    gap_x = 18 * SCALE
    p_w = (W - 2 * margin_x - gap_x) // 2
    p_h = H - 2 * margin_y

    lx = margin_x
    ly = margin_y
    rx = lx + p_w + gap_x
    ry = margin_y

    # =========================================================================
    # LEFT PANEL: The 4-Tier Mapping Hierarchy
    # =========================================================================
    draw.rounded_rectangle([lx, ly, lx + p_w, ly + p_h], radius=12 * SCALE, fill=BOX_BG, outline=BOX_BORDER, width=2 * SCALE)
    draw.text((lx + p_w // 2, ly + 26 * SCALE), "The 4-Tier Mapping Hierarchy", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((lx + p_w // 2, ly + 50 * SCALE), "Algorithmic Tasks  →  Virtual Processes  →  OS Scheduler  →  Hardware Processors", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    layers = [
        ("Tier 1: Algorithmic Tasks", "Fine-grained logical concurrency (k >> p): T1, T2, ..., Tk", (239, 246, 255), HIGHLIGHT_BLUE),
        ("Tier 2: Virtual Processes / Threads", "Programming Model Abstraction: MPI Ranks (0..p-1), OpenMP / POSIX Threads", (254, 243, 199), GOLD),
        ("Tier 3: OS Kernel Dispatcher & Runtime", "Thread pool, run-queues, context switching, CPU core affinity", (241, 245, 249), LINE_COLOR),
        ("Tier 4: Physical Hardware Processors", "Physical CPU Cores, SMT Hardware Threads, Sockets, NUMA Nodes", (240, 253, 244), HIGHLIGHT_GREEN)
    ]

    arrow_labels = [
        "Mapping Scheme (Static / Dynamic)",
        "OS Thread Scheduling & Runtime",
        "Hardware Dispatch & Core Affinity"
    ]

    tier_y = ly + 70 * SCALE
    tier_h = 58 * SCALE
    tier_w = p_w - 36 * SCALE
    tier_x = lx + 18 * SCALE

    for i, (title, desc, bg, col) in enumerate(layers):
        draw.rounded_rectangle([tier_x, tier_y, tier_x + tier_w, tier_y + tier_h], radius=8 * SCALE, fill=bg, outline=col, width=2 * SCALE)
        draw.text((tier_x + 18 * SCALE, tier_y + 18 * SCALE), title, fill=col if col != LINE_COLOR else NAVY, font=font_card_title, anchor="lm")
        draw.text((tier_x + 18 * SCALE, tier_y + 40 * SCALE), desc, fill=TEXT_DARK, font=font_card_body, anchor="lm")

        if i < 3:
            arrow_gap = 24 * SCALE
            arrow_top = tier_y + tier_h
            arrow_bot = arrow_top + arrow_gap
            draw_arrow(draw, tier_x + tier_w // 2, arrow_top, tier_x + tier_w // 2, arrow_bot, color=CRIMSON, width=2 * SCALE, arrow_len=8 * SCALE)
            draw.text((tier_x + tier_w // 2 + 14 * SCALE, arrow_top + arrow_gap // 2), arrow_labels[i], fill=CRIMSON, font=font_arrow, anchor="lm")
            tier_y += tier_h + arrow_gap

    # Left Panel Bottom Callout: Key Principle
    callout_y = tier_y + tier_h + 16 * SCALE
    callout_h = (ly + p_h - 16 * SCALE) - callout_y
    draw.rounded_rectangle([tier_x, callout_y, tier_x + tier_w, callout_y + callout_h], radius=8 * SCALE, fill=(255, 255, 255), outline=BOX_BORDER, width=1 * SCALE)
    
    cp_title = "Key Architectural Principle (Foster's PCAM Methodology):"
    draw.text((tier_x + 16 * SCALE, callout_y + 16 * SCALE), cp_title, fill=CRIMSON, font=font_card_title, anchor="lt")
    
    cp_bullets = [
        ("• Typical APIs (MPI, Pthreads, OpenMP) map to virtual processes, not bare-metal hardware.", False),
        ("• Decoupling enables identical binaries to scale from laptops to 10,000-node supercomputers.", True),
        ("• Eliminates architecture lock-in and hides core topology disparities across platforms.", False)
    ]
    by = callout_y + 38 * SCALE
    for text_line, is_bold in cp_bullets:
        draw.text((tier_x + 16 * SCALE, by), text_line, fill=NAVY if is_bold else TEXT_DARK, font=font_bullet_bold if is_bold else font_bullet, anchor="lt")
        by += 21 * SCALE

    # =========================================================================
    # RIGHT PANEL: Architectural & Algorithmic Rationale
    # =========================================================================
    draw.rounded_rectangle([rx, ry, rx + p_w, ry + p_h], radius=12 * SCALE, fill=BOX_BG, outline=BOX_BORDER, width=2 * SCALE)
    draw.text((rx + p_w // 2, ry + 26 * SCALE), "Architectural & Algorithmic Rationale", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, ry + 50 * SCALE), "Why separating processes from processors is essential in HPC system design", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    rationales = [
        ("1. Decoupling Concurrency from Hardware", 
         "Algorithmic tasks far exceed cores (k >> p). Targeting virtual processes allows seamless execution on a 4-core desktop or a 10,000-node cluster without altering source code."),

        ("2. Platform Portability & Standard APIs", 
         "Standard APIs (MPI ranks, OpenMP threads, Pthreads) define execution on processes, ensuring seamless portability across Intel, AMD, ARM, and heterogeneous accelerators."),

        ("3. Dynamic Latency Hiding (Over-Subscription)", 
         "Running multiple processes/threads per core lets the runtime scheduler switch to ready tasks when others stall on high-latency memory accesses or network transfers."),

        ("4. OS Isolation, Memory Safety & NUMA Pinning", 
         "Private virtual address spaces isolate processes from memory corruption, while OS affinity (taskset, numactl) pins processes to local NUMA nodes for peak bandwidth.")
    ]

    card_y = ry + 70 * SCALE
    card_w = p_w - 36 * SCALE
    card_x = rx + 18 * SCALE
    card_h = 70 * SCALE
    card_gap = 10 * SCALE

    for title, desc in rationales:
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=6 * SCALE, fill=(255, 255, 255), outline=BOX_BORDER, width=1 * SCALE)
        draw.text((card_x + 16 * SCALE, card_y + 12 * SCALE), title, fill=NAVY, font=font_card_title, anchor="lt")
        
        # Word wrap description to strictly fit card width
        wrapped = wrap_text(draw, desc, font_card_body, card_w - 32 * SCALE)
        desc_y = card_y + 32 * SCALE
        for line in wrapped:
            draw.text((card_x + 16 * SCALE, desc_y), line, fill=TEXT_DARK, font=font_card_body, anchor="lt")
            desc_y += 18 * SCALE
            
        card_y += card_h + card_gap

    # Right Panel Bottom Callout: Takeaway Banner
    tb_y = card_y + 6 * SCALE
    tb_h = (ry + p_h - 16 * SCALE) - tb_y
    draw.rounded_rectangle([card_x, tb_y, card_x + card_w, tb_y + tb_h], radius=8 * SCALE, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1 * SCALE)
    
    # Draw checkmark circle icon
    icon_cx = card_x + 24 * SCALE
    icon_cy = tb_y + 24 * SCALE
    icon_r = 9 * SCALE
    draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r], fill=HIGHLIGHT_GREEN)
    chk_p1 = (icon_cx - 4 * SCALE, icon_cy)
    chk_p2 = (icon_cx - 1 * SCALE, icon_cy + 4 * SCALE)
    chk_p3 = (icon_cx + 5 * SCALE, icon_cy - 4 * SCALE)
    draw.line([chk_p1, chk_p2, chk_p3], fill=(255, 255, 255), width=2 * SCALE)

    tb_title = "Core Takeaway for Parallel Algorithm Design:"
    draw.text((icon_cx + icon_r + 8 * SCALE, tb_y + 16 * SCALE), tb_title, fill=HIGHLIGHT_GREEN, font=font_card_title, anchor="lt")
    
    tb_bullets = [
        ("• Algorithm design specifies Task -> Process mapping (optimizing load balance & locality).", False),
        ("• The system runtime & OS handle Process -> Processor mapping (core dispatch & scheduling).", False),
        ("• This two-stage separation is the foundation of portable, high-performance computing!", True)
    ]
    tby = tb_y + 38 * SCALE
    for bullet, is_bold in tb_bullets:
        draw.text((card_x + 16 * SCALE, tby), bullet, fill=NAVY if is_bold else TEXT_DARK, font=font_bullet_bold if is_bold else font_bullet, anchor="lt")
        tby += 21 * SCALE

    # Resize cleanly to target dimensions with Lanczos
    final_img = img.resize((BASE_W, BASE_H), Image.Resampling.LANCZOS)
    final_img.save("extracted_images/lec18_processes_vs_processors.png", dpi=(300, 300))
    print("Saved lec18_processes_vs_processors.png")

# -------------------------------------------------------------
# 2. lec18_mapping_tradeoff_idling_comm.png
# Dual Objectives of Mapping: Minimizing Idling vs Communication
# -------------------------------------------------------------
def create_mapping_tradeoff_idling_comm():
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

    draw.text((W // 2, 28), "The Dual Objectives of Process Mapping: Idling vs. Communication", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "An optimal mapping balances Task Dependency Graphs (Load Balancing) and Task Interaction Graphs (Locality)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Objective 1: Minimizing Idling (Load Balance)
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Objective 1: Minimum Idling & Load Balance", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Governed by Task Dependency Graph (DAG) (Slide 4, 6)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Replicate Database Query Mapping (Slide 7)
    # Level 1: 4 tasks (Task 1, 2, 3, 4) mapped to P0, P1, P2, P3
    # Level 2: 2 tasks (Task 5, 6) mapped to P0, P2
    # Level 3: 1 task (Task 7) mapped to P0
    ox = 80
    oy = 180

    # Nodes Level 1
    l1_tasks = [("Task 4", "10", "P3"), ("Task 3", "10", "P2"), ("Task 2", "10", "P1"), ("Task 1", "10", "P0")]
    l1_xs = [ox + 60, ox + 180, ox + 300, ox + 420]
    r_node = 24

    for i, (tname, wt, proc) in enumerate(l1_tasks):
        cx = l1_xs[i]
        draw.ellipse([cx - r_node, oy - r_node, cx + r_node, oy + r_node], fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
        draw.text((cx, oy - 6), wt, fill=NAVY, font=font_mono, anchor="mm")
        draw.text((cx, oy - r_node - 14), tname, fill=TEXT_MUTED, font=font_badge, anchor="mm")
        draw.text((cx + r_node + 12, oy + 4), proc, fill=CRIMSON, font=font_badge, anchor="lm")

    # Level 2 Nodes: Task 6 (weight 9, proc P2) from Tasks 4,3 and Task 5 (weight 6, proc P0) from Tasks 2,1
    oy2 = 280
    cx_t6 = (l1_xs[0] + l1_xs[1]) // 2
    cx_t5 = (l1_xs[2] + l1_xs[3]) // 2

    # Task 6
    draw.ellipse([cx_t6 - r_node, oy2 - r_node, cx_t6 + r_node, oy2 + r_node], fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((cx_t6, oy2 - 6), "9", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((cx_t6 + r_node + 12, oy2 + 4), "P2", fill=CRIMSON, font=font_badge, anchor="lm")
    draw.text((cx_t6 + r_node + 35, oy2 - 6), "Task 6", fill=TEXT_MUTED, font=font_badge, anchor="lm")
    draw_arrow(draw, l1_xs[0], oy + r_node, cx_t6 - 10, oy2 - r_node, color=LINE_COLOR, width=2)
    draw_arrow(draw, l1_xs[1], oy + r_node, cx_t6 + 10, oy2 - r_node, color=LINE_COLOR, width=2)

    # Task 5
    draw.ellipse([cx_t5 - r_node, oy2 - r_node, cx_t5 + r_node, oy2 + r_node], fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((cx_t5, oy2 - 6), "6", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((cx_t5 - r_node - 12, oy2 + 4), "P0", fill=CRIMSON, font=font_badge, anchor="rm")
    draw.text((cx_t5 + r_node + 12, oy2 - 6), "Task 5", fill=TEXT_MUTED, font=font_badge, anchor="lm")
    draw_arrow(draw, l1_xs[2], oy + r_node, cx_t5 - 10, oy2 - r_node, color=LINE_COLOR, width=2)
    draw_arrow(draw, l1_xs[3], oy + r_node, cx_t5 + 10, oy2 - r_node, color=LINE_COLOR, width=2)

    # Level 3 Node: Task 7 (weight 8, proc P0)
    oy3 = 380
    cx_t7 = (cx_t6 + cx_t5) // 2
    draw.ellipse([cx_t7 - r_node, oy3 - r_node, cx_t7 + r_node, oy3 + r_node], fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=2)
    draw.text((cx_t7, oy3 - 6), "8", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((cx_t7 - r_node - 12, oy3 + 4), "P0", fill=CRIMSON, font=font_badge, anchor="rm")
    draw.text((cx_t7 + r_node + 12, oy3 - 6), "Task 7", fill=TEXT_MUTED, font=font_badge, anchor="lm")
    draw_arrow(draw, cx_t6, oy2 + r_node, cx_t7 - 10, oy3 - r_node, color=LINE_COLOR, width=2)
    draw_arrow(draw, cx_t5, oy2 + r_node, cx_t7 + 10, oy3 - r_node, color=LINE_COLOR, width=2)

    # Callout card for Level-by-Level mapping
    draw.rounded_rectangle([60, 440, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 455), "Mapping Rules for Minimum Idling:", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([75, 475, 40 + p_w - 35, 475], fill=BOX_BORDER, width=1)

    idling_rules = [
        ("Level-Based Allocation:", "View DAG in topological levels. Tasks at same level run concurrently."),
        ("Disjoint Assignment:", "Map independent concurrent tasks to different physical processes (P0..P3)."),
        ("Critical Path Priority:", "Assign critical path tasks to available processes immediately."),
        ("Process Reuse:", "P0 computes Task 1, then Task 5, then Task 7, eliminating inter-node transfer.")
    ]
    iy = 485
    for rtitle, rdesc in idling_rules:
        draw.text((75, iy), f"• {rtitle}", fill=CRIMSON, font=font_badge, anchor="lt")
        draw.text((230, iy), rdesc, fill=TEXT_DARK, font=font_text, anchor="lt")
        iy += 28

    # RIGHT PANEL: Objective 2: Minimizing Interaction (Communication)
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "Objective 2: Minimum Communication", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Governed by Task Interaction Graph (Spatial Locality) (Slide 4, 6)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Spatial cluster diagram
    # Two clusters of densely interacting tasks
    cx1, cy1 = rx + 150, 260
    cx2, cy2 = rx + 430, 260
    clust_r = 100

    # Cluster 1 (Process 0)
    draw.ellipse([cx1 - clust_r, cy1 - clust_r, cx1 + clust_r, cy1 + clust_r], fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
    draw.text((cx1, cy1 - clust_r + 20), "Process 0 Domain", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="mm")
    # Internal tasks
    p0_tasks = [ (cx1 - 40, cy1 - 20, "T1"), (cx1 + 40, cy1 - 20, "T2"), (cx1, cy1 + 40, "T3") ]
    for tx, ty, tname in p0_tasks:
        draw.ellipse([tx - 18, ty - 18, tx + 18, ty + 18], fill=(255, 255, 255), outline=NAVY, width=2)
        draw.text((tx, ty), tname, fill=NAVY, font=font_mono, anchor="mm")
    # Dense internal edges
    draw.line([p0_tasks[0][0], p0_tasks[0][1], p0_tasks[1][0], p0_tasks[1][1]], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([p0_tasks[0][0], p0_tasks[0][1], p0_tasks[2][0], p0_tasks[2][1]], fill=HIGHLIGHT_BLUE, width=2)
    draw.line([p0_tasks[1][0], p0_tasks[1][1], p0_tasks[2][0], p0_tasks[2][1]], fill=HIGHLIGHT_BLUE, width=2)
    draw.text((cx1, cy1), "Dense Local\nMemory Access", fill=HIGHLIGHT_GREEN, font=get_font(11, bold=True), anchor="mm")

    # Cluster 2 (Process 1)
    draw.ellipse([cx2 - clust_r, cy2 - clust_r, cx2 + clust_r, cy2 + clust_r], fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((cx2, cy2 - clust_r + 20), "Process 1 Domain", fill=GOLD, font=font_badge, anchor="mm")
    p1_tasks = [ (cx2 - 40, cy2 - 20, "T4"), (cx2 + 40, cy2 - 20, "T5"), (cx2, cy2 + 40, "T6") ]
    for tx, ty, tname in p1_tasks:
        draw.ellipse([tx - 18, ty - 18, tx + 18, ty + 18], fill=(255, 255, 255), outline=NAVY, width=2)
        draw.text((tx, ty), tname, fill=NAVY, font=font_mono, anchor="mm")
    # Dense internal edges
    draw.line([p1_tasks[0][0], p1_tasks[0][1], p1_tasks[1][0], p1_tasks[1][1]], fill=GOLD, width=2)
    draw.line([p1_tasks[0][0], p1_tasks[0][1], p1_tasks[2][0], p1_tasks[2][1]], fill=GOLD, width=2)
    draw.line([p1_tasks[1][0], p1_tasks[1][1], p1_tasks[2][0], p1_tasks[2][1]], fill=GOLD, width=2)
    draw.text((cx2, cy2), "Dense Local\nMemory Access", fill=HIGHLIGHT_GREEN, font=get_font(11, bold=True), anchor="mm")

    # Sparse inter-process edge between T2 and T4
    draw.line([p0_tasks[1][0], p0_tasks[1][1], p1_tasks[0][0], p1_tasks[0][1]], fill=CRIMSON, width=3)
    draw.text(((p0_tasks[1][0] + p1_tasks[0][0]) // 2, cy1 - 35), "Sparse Inter-Process\nNetwork Message", fill=CRIMSON, font=get_font(11, bold=True), anchor="mm")

    # Comparison summary card
    draw.rounded_rectangle([rx + 20, 440, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((rx + 35, 455), "The Fundamental Mapping Trade-off:", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([rx + 35, 475, rx + p_w - 35, 475], fill=BOX_BORDER, width=1)

    tradeoff_rows = [
        ("The Conflict:", "Spreading tasks across processes maximizes load balance but multiplies network communication overhead."),
        ("Clustering Tasks:", "Mapping tasks with dense interactions to the same process converts network latency into sub-nanosecond L1/L2 cache hits!"),
        ("The Pareto Optimum:", "An optimal mapping algorithm places tightly coupled tasks on the same core/socket, while balancing work evenly across cores.")
    ]
    ty_off = 485
    for rtitle, rdesc in tradeoff_rows:
        draw.text((rx + 35, ty_off), f"✓ {rtitle}", fill=CRIMSON, font=font_badge, anchor="lt")
        words = rdesc.split(" ")
        l1 = " ".join(words[:11])
        l2 = " ".join(words[11:])
        draw.text((rx + 175, ty_off), l1, fill=TEXT_DARK, font=font_text, anchor="lt")
        if l2:
            draw.text((rx + 175, ty_off + 18), l2, fill=TEXT_DARK, font=font_text, anchor="lt")
            ty_off += 18
        ty_off += 24

    img.save("extracted_images/lec18_mapping_tradeoff_idling_comm.png")
    print("Saved lec18_mapping_tradeoff_idling_comm.png")

# -------------------------------------------------------------
# 3. lec18_data_partitioning_1d_2d.png
# Static Mapping via Data Partitioning: 1-D vs 2-D Distributions
# -------------------------------------------------------------
def create_data_partitioning_1d_2d():
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

    draw.text((W // 2, 28), "Static Mapping via Data Partitioning: 1-D vs. 2-D Matrix Distributions", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Replicating Slide 37: 1-D Block (Row/Col) vs. 2-D Checkerboard with Communication Volume Analysis", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: 1-D Block Distributions (Slide 37)
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "1-D Block Distributions (p = 8 Processes)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Row-wise Distribution (Left) vs. Column-wise Distribution (Right)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Row-wise matrix
    ox_row = 80
    oy_grid = 175
    gw = 200
    gh = 220
    row_h = gh // 8

    draw.text((ox_row + gw // 2, oy_grid - 15), "Row-wise Distribution", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(8):
        y1 = oy_grid + r * row_h
        y2 = y1 + row_h
        bg = (239, 246, 255) if r % 2 == 0 else (255, 255, 255)
        draw.rectangle([ox_row, y1, ox_row + gw, y2], fill=bg, outline=LINE_COLOR, width=1)
        draw.text((ox_row + gw // 2, y1 + row_h // 2), f"P{r}", fill=NAVY, font=font_mono, anchor="mm")

    # Column-wise matrix
    ox_col = 350
    col_w = gw // 8
    draw.text((ox_col + gw // 2, oy_grid - 15), "Column-wise Distribution", fill=NAVY, font=font_badge, anchor="mm")
    for c in range(8):
        x1 = ox_col + c * col_w
        x2 = x1 + col_w
        bg = (239, 246, 255) if c % 2 == 0 else (255, 255, 255)
        draw.rectangle([x1, oy_grid, x2, oy_grid + gh], fill=bg, outline=LINE_COLOR, width=1)
        draw.text((x1 + col_w // 2, oy_grid + gh // 2), f"P{c}", fill=NAVY, font=font_mono, anchor="mm")

    # 1D Analysis card
    draw.rounded_rectangle([60, 430, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 445), "1-D Distribution Characteristics & Limitations:", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([75, 465, 40 + p_w - 35, 465], fill=BOX_BORDER, width=1)

    c1_notes = [
        ("Simplicity", "Trivially maps to contiguous memory in row-major (C) or col-major (Fortran)."),
        ("Scalability Bound", "Maximum number of processors is strictly bounded by p ≤ n."),
        ("Boundary Overhead", "Each process shares a 2n-element boundary with nearest neighbors."),
        ("LU Work Imbalance", "In triangular elimination, early rows/cols finish early, idling processes.")
    ]
    ny = 475
    for lbl, desc in c1_notes:
        draw.text((75, ny), f"• {lbl}:", fill=CRIMSON, font=font_badge, anchor="lt")
        bbox = draw.textbbox((75, ny), f"• {lbl}:", font=font_badge)
        draw.text((bbox[2] + 8, ny), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 28

    # RIGHT PANEL: 2-D Checkerboard Block Distribution
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "2-D Checkerboard (Square Grid) Distribution", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "p = 16 Processes arranged in a 4×4 Process Mesh (P_i,j)", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 4x4 Process grid
    gx = rx + (p_w - 240) // 2
    gy = 175
    cell_s = 60

    draw.text((gx + 120, gy - 15), "2-D Checkerboard Grid (4×4)", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(4):
        for c in range(4):
            x1 = gx + c * cell_s
            y1 = gy + r * cell_s
            p_id = r * 4 + c
            bg = (240, 253, 244) if (r + c) % 2 == 0 else (255, 255, 255)
            draw.rectangle([x1, y1, x1 + cell_s, y1 + cell_s], fill=bg, outline=LINE_COLOR, width=1)
            draw.text((x1 + cell_s // 2, y1 + cell_s // 2), f"P{p_id}", fill=NAVY, font=font_mono, anchor="mm")

    # Mathematical Surface-to-Volume comparison card
    draw.rounded_rectangle([rx + 20, 430, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((rx + 35, 445), "Communication Surface-to-Volume Advantage (Grama Sec 3.4.1):", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")
    draw.line([rx + 35, 465, rx + p_w - 35, 465], fill=BOX_BORDER, width=1)

    c2_notes = [
        ("Processor Scaling", "Supports up to p ≤ n^2 processors for massive supercomputers."),
        ("1-D Boundary Perimeter", "Perimeter = 2n elements. Communication overhead = O(n)."),
        ("2-D Boundary Perimeter", "Perimeter = 4(n/√p). Communication overhead = O(n/√p)."),
        ("Asymptotic Reduction", "Communication is reduced by an asymptotic factor of √p!"),
        ("Standard in ScaLAPACK", "Employed by state-of-the-art supercomputing dense solvers.")
    ]
    ny = 475
    for lbl, desc in c2_notes:
        draw.text((rx + 35, ny), f"• {lbl}:", fill=NAVY, font=font_badge, anchor="lt")
        bbox = draw.textbbox((rx + 35, ny), f"• {lbl}:", font=font_badge)
        draw.text((bbox[2] + 8, ny), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        ny += 28

    img.save("extracted_images/lec18_data_partitioning_1d_2d.png")
    print("Saved lec18_data_partitioning_1d_2d.png")

# -------------------------------------------------------------
# 4. lec18_sparse_graph_partitioning.png
# Mapping via Task Graph Partitioning: Sparse Matrix-Vector Multiplication
# -------------------------------------------------------------
def create_sparse_graph_partitioning():
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

    draw.text((W // 2, 28), "Mapping via Task Graph Partitioning: Sparse Matrix-Vector Multiplication", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Replicating Slide 38: Mapping Sparse Matrix non-zeros onto an Interaction Graph partitioned across 3 Processes", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Sparse Matrix A & Vector b Partitioning (Slide 38 right)
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Sparse Matrix A (12×12) & Process Partitioning", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Non-zero entries induce required vector elements b[j]", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 12x12 grid with dots
    ox = 90
    oy = 175
    cell = 20
    n = 12

    # Draw matrix frame
    draw.text((ox + n * cell // 2, oy - 15), "Matrix A (12×12)", fill=NAVY, font=font_badge, anchor="mm")
    # Column indices
    for c in range(n):
        draw.text((ox + c * cell + cell // 2, oy - 4), str(c), fill=TEXT_MUTED, font=get_font(10), anchor="mm")

    # Sparse dots pattern (from Slide 38)
    sparse_entries = {
        0: [0, 1, 4, 5],
        1: [0, 1, 5, 6],
        2: [1, 2, 6, 7],
        3: [2, 3, 7],
        4: [0, 4, 5, 8, 9],
        5: [0, 1, 4, 5, 6, 9, 10],
        6: [1, 2, 5, 6, 7, 10, 11],
        7: [2, 3, 6, 7, 11],
        8: [4, 8, 9],
        9: [4, 5, 8, 9, 10],
        10: [5, 6, 9, 10, 11],
        11: [6, 7, 10, 11]
    }

    # Process rows assignment: Process 0 (rows 0-3), Process 1 (rows 4-7), Process 2 (rows 8-11)
    p_row_colors = [
        (239, 246, 255), (239, 246, 255), (239, 246, 255), (239, 246, 255),
        (254, 243, 199), (254, 243, 199), (254, 243, 199), (254, 243, 199),
        (240, 253, 244), (240, 253, 244), (240, 253, 244), (240, 253, 244)
    ]

    for r in range(n):
        draw.rectangle([ox, oy + r * cell, ox + n * cell, oy + (r + 1) * cell], fill=p_row_colors[r], outline=BOX_BORDER)
        for c in range(n):
            if c in sparse_entries.get(r, []):
                # draw black dot
                draw.ellipse([ox + c * cell + 4, oy + r * cell + 4, ox + (c + 1) * cell - 4, oy + (r + 1) * cell - 4], fill=TEXT_DARK)

    # Process bracket labels on left
    draw.text((ox - 12, oy + 2 * cell), "Process 0", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="rm")
    draw.text((ox - 12, oy + 6 * cell), "Process 1", fill=GOLD, font=font_badge, anchor="rm")
    draw.text((ox - 12, oy + 10 * cell), "Process 2", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="rm")

    # Vector b column on right
    bx = ox + n * cell + 25
    draw.text((bx + 12, oy - 15), "b", fill=NAVY, font=font_badge, anchor="mm")
    for r in range(n):
        draw.rectangle([bx, oy + r * cell, bx + 24, oy + (r + 1) * cell], fill=(255, 255, 255), outline=LINE_COLOR)

    # Communication requirement labels from Slide 38
    comm_y = oy + n * cell + 20
    draw.rounded_rectangle([60, comm_y, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, comm_y + 15), "Required Elements from Vector b (Slide 38):", fill=NAVY, font=font_badge, anchor="lt")

    c_reqs = [
        ("Process 0 requires b-elements:", "C0 = {4, 5, 6, 7, 8} from remote nodes."),
        ("Process 1 requires b-elements:", "C1 = {0, 1, 2, 3, 8, 9, 10, 11} from remote nodes."),
        ("Process 2 requires b-elements:", "C2 = {0, 4, 5, 6} from remote nodes."),
        ("Sparse Irregularity:", "Dense blocks fail! Highly uneven communication across processes.")
    ]
    ry_c = comm_y + 40
    for lbl, desc in c_reqs:
        draw.text((75, ry_c), f"• {lbl}", fill=CRIMSON, font=font_badge, anchor="lt")
        bbox = draw.textbbox((75, ry_c), f"• {lbl}", font=font_badge)
        draw.text((bbox[2] + 8, ry_c), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        ry_c += 26

    # RIGHT PANEL: Graph Partitioning Formulation (Slide 38 left)
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "Isomorphic Graph Partitioning (k = 3)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Vertices = Tasks (Rows), Edges = Interactions, Cut = Communication", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Draw graph with 12 vertices in 3 partitioned clusters
    # Cluster 0 (Process 0): Vertices 0, 4, 8, 1
    # Cluster 1 (Process 1): Vertices 2, 3, 6, 7
    # Cluster 2 (Process 2): Vertices 5, 9, 10, 11
    coords = {
        0: (rx + 110, 210), 1: (rx + 190, 210), 4: (rx + 100, 290), 8: (rx + 180, 290),
        2: (rx + 330, 210), 3: (rx + 420, 210), 6: (rx + 340, 290), 7: (rx + 430, 290),
        5: (rx + 230, 360), 9: (rx + 220, 420), 10: (rx + 310, 420), 11: (rx + 400, 420)
    }

    # Draw edges between nodes (sample interactions)
    edges = [
        (0, 1), (0, 4), (1, 4), (1, 5), (4, 8), (4, 5), (8, 9),
        (2, 3), (2, 6), (3, 7), (6, 7), (6, 10), (7, 11),
        (5, 6), (5, 9), (5, 10), (9, 10), (10, 11)
    ]
    for u, v in edges:
        is_cut = (u in [0,1,4,8] and v not in [0,1,4,8]) or (u in [2,3,6,7] and v not in [2,3,6,7])
        col = CRIMSON if is_cut else BOX_BORDER
        w_edge = 2 if is_cut else 1
        draw.line([coords[u][0], coords[u][1], coords[v][0], coords[v][1]], fill=col, width=w_edge)

    # Draw node circles
    for node_id, (nx, ny) in coords.items():
        if node_id in [0, 1, 4, 8]:
            fill_c = (239, 246, 255)
            border_c = HIGHLIGHT_BLUE
        elif node_id in [2, 3, 6, 7]:
            fill_c = (254, 243, 199)
            border_c = GOLD
        else:
            fill_c = (240, 253, 244)
            border_c = HIGHLIGHT_GREEN

        draw.ellipse([nx - 14, ny - 14, nx + 14, ny + 14], fill=fill_c, outline=border_c, width=2)
        draw.text((nx, ny), str(node_id), fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Dotted boundary lines around partitions
    draw.text((rx + 70, 185), "Process 0", fill=HIGHLIGHT_BLUE, font=font_badge, anchor="lm")
    draw.text((rx + 410, 185), "Process 1", fill=GOLD, font=font_badge, anchor="lm")
    draw.text((rx + 220, 460), "Process 2", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lm")

    # Min-Cut card at bottom
    draw.rounded_rectangle([rx + 20, 480, rx + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((rx + 35, 495), "Min-Cut Graph Partitioning Objective:", fill=NAVY, font=font_badge, anchor="lt")
    draw.line([rx + 35, 515, rx + p_w - 35, 515], fill=BOX_BORDER, width=1)

    mincut_bullets = [
        ("Vertex Balance", "Each partition receives ~|V|/k vertices (uniform computational load)."),
        ("Min-Cut Edges", "Minimize number of cross-partition edges to minimize network volume."),
        ("NP-Hard Problem", "Optimal k-way min-cut is NP-hard; solved via METIS or Scotch libraries.")
    ]
    my_off = 525
    for lbl, desc in mincut_bullets:
        draw.text((rx + 35, my_off), f"• {lbl}:", fill=CRIMSON, font=font_badge, anchor="lt")
        bbox = draw.textbbox((rx + 35, my_off), f"• {lbl}:", font=font_badge)
        draw.text((bbox[2] + 8, my_off), desc, fill=TEXT_DARK, font=font_text, anchor="lt")
        my_off += 26

    img.save("extracted_images/lec18_sparse_graph_partitioning.png")
    print("Saved lec18_sparse_graph_partitioning.png")

# -------------------------------------------------------------
# 5. lec18_hierarchical_mapping_tree.png
# Hierarchical Process Mapping: Multi-Level Architecture for Tree Algorithms
# -------------------------------------------------------------
def create_hierarchical_mapping_tree():
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

    draw.text((W // 2, 28), "Hierarchical Process Mapping: Multi-Level Architecture for Tree Algorithms", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Replicating Slide 39 & 40: Task Partitioning at Top Level with Data Partitioning within Processor Subsets", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: The Multi-Level Tree Allocation (Slide 40)
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Hierarchical Process Group Tree (Slide 40)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "p = 8 Processors subdivided into recursive teams", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Draw Tree from Slide 40
    # Level 0 (Root): All 8 processors [P0 P1 P4 P5 / P2 P3 P6 P7]
    cx_root = 40 + p_w // 2
    cy_root = 180
    rw, rh = 160, 44
    draw.rounded_rectangle([cx_root - rw // 2, cy_root - rh // 2, cx_root + rw // 2, cy_root + rh // 2], radius=6, fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
    draw.text((cx_root, cy_root - 10), "P0  P1  P4  P5", fill=NAVY, font=font_mono, anchor="mm")
    draw.line([cx_root - rw // 2 + 10, cy_root, cx_root + rw // 2 - 10, cy_root], fill=HIGHLIGHT_BLUE, width=1)
    draw.text((cx_root, cy_root + 10), "P2  P3  P6  P7", fill=NAVY, font=font_mono, anchor="mm")
    draw.text((cx_root - rw // 2 - 12, cy_root), "Team 8", fill=CRIMSON, font=font_badge, anchor="rm")

    # Level 1: Left [P0 P1 / P2 P3] and Right [P4 P5 / P6 P7]
    cy_l1 = 280
    cx_left = cx_root - 140
    cx_right = cx_root + 140
    rw1, rh1 = 110, 40

    draw_arrow(draw, cx_root - 30, cy_root + rh // 2, cx_left, cy_l1 - rh1 // 2, color=LINE_COLOR, width=2)
    draw_arrow(draw, cx_root + 30, cy_root + rh // 2, cx_right, cy_l1 - rh1 // 2, color=LINE_COLOR, width=2)

    # Left Team
    draw.rounded_rectangle([cx_left - rw1 // 2, cy_l1 - rh1 // 2, cx_left + rw1 // 2, cy_l1 + rh1 // 2], radius=6, fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((cx_left, cy_l1 - 9), "P0   P1", fill=NAVY, font=font_mono, anchor="mm")
    draw.line([cx_left - rw1 // 2 + 8, cy_l1, cx_left + rw1 // 2 - 8, cy_l1], fill=GOLD, width=1)
    draw.text((cx_left, cy_l1 + 9), "P2   P3", fill=NAVY, font=font_mono, anchor="mm")

    # Right Team
    draw.rounded_rectangle([cx_right - rw1 // 2, cy_l1 - rh1 // 2, cx_right + rw1 // 2, cy_l1 + rh1 // 2], radius=6, fill=(254, 243, 199), outline=GOLD, width=2)
    draw.text((cx_right, cy_l1 - 9), "P4   P5", fill=NAVY, font=font_mono, anchor="mm")
    draw.line([cx_right - rw1 // 2 + 8, cy_l1, cx_right + rw1 // 2 - 8, cy_l1], fill=GOLD, width=1)
    draw.text((cx_right, cy_l1 + 9), "P6   P7", fill=NAVY, font=font_mono, anchor="mm")

    # Level 2: 4 pairs of 2: [P0 P1], [P2 P3], [P4 P5], [P6 P7]
    cy_l2 = 370
    l2_xs = [cx_left - 70, cx_left + 70, cx_right - 70, cx_right + 70]
    l2_labels = ["P0  P1", "P2  P3", "P4  P5", "P6  P7"]
    rw2, rh2 = 76, 26

    draw_arrow(draw, cx_left - 20, cy_l1 + rh1 // 2, l2_xs[0], cy_l2 - rh2 // 2, color=LINE_COLOR, width=2)
    draw_arrow(draw, cx_left + 20, cy_l1 + rh1 // 2, l2_xs[1], cy_l2 - rh2 // 2, color=LINE_COLOR, width=2)
    draw_arrow(draw, cx_right - 20, cy_l1 + rh1 // 2, l2_xs[2], cy_l2 - rh2 // 2, color=LINE_COLOR, width=2)
    draw_arrow(draw, cx_right + 20, cy_l1 + rh1 // 2, l2_xs[3], cy_l2 - rh2 // 2, color=LINE_COLOR, width=2)

    for i, lx in enumerate(l2_xs):
        draw.rounded_rectangle([lx - rw2 // 2, cy_l2 - rh2 // 2, lx + rw2 // 2, cy_l2 + rh2 // 2], radius=4, fill=(240, 253, 244), outline=HIGHLIGHT_GREEN, width=1)
        draw.text((lx, cy_l2), l2_labels[i], fill=NAVY, font=font_mono, anchor="mm")

    # Level 3: Individual 8 processors: P0, P1, P2, P3, P4, P5, P6, P7
    cy_l3 = 450
    rw3 = 34
    for i in range(8):
        parent_x = l2_xs[i // 2]
        off = -18 if i % 2 == 0 else 18
        px = parent_x + off
        draw_arrow(draw, parent_x, cy_l2 + rh2 // 2, px, cy_l3 - 12, color=LINE_COLOR, width=1)
        draw.rounded_rectangle([px - rw3 // 2, cy_l3 - 12, px + rw3 // 2, cy_l3 + 12], radius=4, fill=(255, 255, 255), outline=CRIMSON, width=1)
        draw.text((px, cy_l3), f"P{i}", fill=CRIMSON, font=font_mono, anchor="mm")

    # Callout at bottom left
    draw.rounded_rectangle([60, 495, 40 + p_w - 20, 80 + p_h - 20], radius=8, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((75, 510), "Hierarchical Mapping Mechanics (Slide 39):", fill=NAVY, font=font_badge, anchor="lt")
    draw.text((75, 532), "• Top Level: Task mapping cannot use large p -> Use Data Partitioning within group.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((75, 554), "• Intermediate: Recursive bisection splits processor groups symmetrically.", fill=TEXT_DARK, font=font_text, anchor="lt")
    draw.text((75, 576), "• Leaf Level: 1 processor per task -> Zero inter-process communication!", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")

    # RIGHT PANEL: Benefits, Use Cases & Algorithmic Impact
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "Why Hierarchical Mapping is Essential", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Solving the scalability dilemma of binary tree algorithms", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    h_cards = [
        ("1. Eliminates Upper-Level Processor Idling",
         "In standard Quicksort or Tree reductions, the root step has concurrency = 1, leaving p-1 processors idle. "
         "Hierarchical mapping engages ALL p processors to partition data cooperatively."),

        ("2. Congruence with Physical Hardware Topology",
         "Modern supercomputers are hierarchical (SMT cores, NUMA sockets, InfiniBand network racks). "
         "Hierarchical mapping aligns algorithmic subproblems with physical NUMA and rack boundaries!"),

        ("3. Eliminates Cross-Network Traffic at Leaves",
         "Once subproblems are small enough to fit within local processor cache (L2/L3), tasks transition to pure sequential execution with 100% cache locality and zero network messaging."),

        ("4. Applicable Algorithm Classes",
         "Hierarchical Barnes-Hut N-body simulation, Fast Multipole Method (FMM), Adaptive Mesh Refinement (AMR), and Multilevel Graph Partitioners (METIS/Scotch).")
    ]

    ry_r = 165
    for title, desc in h_cards:
        draw.rounded_rectangle([rx + 20, ry_r, rx + p_w - 20, ry_r + 96], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
        draw.text((rx + 35, ry_r + 14), title, fill=NAVY, font=font_badge, anchor="lt")
        wrapped = wrap_text(draw, desc, font_text, p_w - 70)
        ty = ry_r + 36
        for line in wrapped[:3]:
            draw.text((rx + 35, ty), line, fill=TEXT_DARK, font=font_text, anchor="lt")
            ty += 18
        ry_r += 108

    draw.rounded_rectangle([rx + 20, 580, rx + p_w - 20, 80 + p_h - 20], radius=6, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((rx + 35, 595), "• Result: Converts an O(n) span bottleneck into an O(log^2 n) span parallel algorithm!", fill=HIGHLIGHT_GREEN, font=font_badge, anchor="lt")

    img.save("extracted_images/lec18_hierarchical_mapping_tree.png")
    print("Saved lec18_hierarchical_mapping_tree.png")

# -------------------------------------------------------------
# 6. lec18_dynamic_mapping_work_stealing.png
# Dynamic Load Balancing: Centralized Master-Worker vs Work Stealing
# -------------------------------------------------------------
def create_dynamic_mapping_work_stealing():
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

    draw.text((W // 2, 28), "Dynamic Load Balancing: Centralized Master-Worker vs. Work Stealing", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Comparing Global Queue Serialization with Decentralized Lock-Free Double-Ended Work Stealing", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Centralized Master-Worker Scheme
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 110), "Scheme A: Centralized Master-Worker Queue", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 134), "Global queue on master process with worker dispatch", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # Master node & Queue
    mx = 40 + p_w // 2
    my = 180
    draw.rounded_rectangle([mx - 150, my, mx + 150, my + 50], radius=6, fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
    draw.text((mx, my + 16), "Master Process (P0)", fill=NAVY, font=font_badge, anchor="mm")
    draw.text((mx, my + 34), "Global Work Pool / Priority Task Queue", fill=CRIMSON, font=font_mono, anchor="mm")

    # 4 Workers below
    wy = 310
    w_xs = [80, 200, 320, 440]
    for i in range(4):
        wx = w_xs[i]
        draw.rounded_rectangle([wx, wy, wx + 80, wy + 50], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=2)
        draw.text((wx + 40, wy + 16), f"Worker {i+1}", fill=NAVY, font=font_badge, anchor="mm")
        draw.text((wx + 40, wy + 34), f"Task Chunk", fill=TEXT_MUTED, font=get_font(11), anchor="mm")

        # Two-way arrows between master and workers
        draw_arrow(draw, mx - 80 + i * 50, my + 50, wx + 40, wy, color=HIGHLIGHT_BLUE, width=2)

    # Master-Worker bottlenecks card
    card_y1 = 395
    card_y2 = 80 + p_h - 15  # 635
    lx1 = 60
    lx2 = 40 + p_w - 20      # 600
    draw.rounded_rectangle([lx1, card_y1, lx2, card_y2], radius=8, fill=(254, 242, 242), outline=CARD_BORDER_BAD, width=1)
    draw.text((lx1 + 16, card_y1 + 12), "Bottlenecks of Centralized Queue (Grama Sec 3.5.2):", fill=CRIMSON, font=get_font(14, bold=True), anchor="lt")
    draw.line([lx1 + 16, card_y1 + 32, lx2 - 16, card_y1 + 32], fill=BOX_BORDER, width=1)

    mw_flaws = [
        ("Central Lock Contention", "As p > 32, lock contention on global queue serializes task dispatch."),
        ("Single Point of Failure", "Master process crash or network stall halts the entire supercomputing job."),
        ("Chunking Dilemma", "Large chunks cause tail load imbalance; small chunks flood network with RPCs."),
        ("Guided Self-Scheduling Mitigation", "Heuristic mitigates contention by shrinking chunk size: K_t = ceil(R_t / p).")
    ]
    my_off = card_y1 + 38
    for lbl, desc in mw_flaws:
        draw.text((lx1 + 16, my_off), f"• {lbl}:", fill=NAVY, font=get_font(13, bold=True), anchor="lt")
        draw.text((lx1 + 30, my_off + 17), desc, fill=TEXT_DARK, font=get_font(12, bold=False), anchor="lt")
        my_off += 48

    # RIGHT PANEL: Distributed Work Stealing (Cilk / Intel TBB)
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 110), "Scheme B: Distributed Work Stealing (Cilk/TBB)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 134), "Local Deques: Workers push/pop bottom; Idle thieves steal top", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    # 3 Worker deques side by side
    dq_xs = [rx + 70, rx + 240, rx + 410]
    dq_y = 180
    dq_w = 110
    dq_h = 160

    # Worker 1 (Busy)
    draw.rounded_rectangle([dq_xs[0], dq_y, dq_xs[0] + dq_w, dq_y + dq_h], radius=6, fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
    draw.text((dq_xs[0] + dq_w // 2, dq_y + 16), "Worker 1 Deque", fill=NAVY, font=font_badge, anchor="mm")
    # tasks inside
    for t_idx, t_name in enumerate(["Task 10 (Coarse)", "Task 11", "Task 12 (Fine)"]):
        ty = dq_y + 40 + t_idx * 35
        draw.rectangle([dq_xs[0] + 8, ty, dq_xs[0] + dq_w - 8, ty + 26], fill=(255, 255, 255), outline=BOX_BORDER)
        draw.text((dq_xs[0] + dq_w // 2, ty + 13), t_name, fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Worker 2 (Busy)
    draw.rounded_rectangle([dq_xs[1], dq_y, dq_xs[1] + dq_w, dq_y + dq_h], radius=6, fill=(239, 246, 255), outline=HIGHLIGHT_BLUE, width=2)
    draw.text((dq_xs[1] + dq_w // 2, dq_y + 16), "Worker 2 Deque", fill=NAVY, font=font_badge, anchor="mm")
    for t_idx, t_name in enumerate(["Task 20 (Coarse)", "Task 21", "Task 22 (Fine)"]):
        ty = dq_y + 40 + t_idx * 35
        draw.rectangle([dq_xs[1] + 8, ty, dq_xs[1] + dq_w - 8, ty + 26], fill=(255, 255, 255), outline=BOX_BORDER)
        draw.text((dq_xs[1] + dq_w // 2, ty + 13), t_name, fill=TEXT_DARK, font=font_mono, anchor="mm")

    # Worker 3 (IDLE / Thief)
    draw.rounded_rectangle([dq_xs[2], dq_y, dq_xs[2] + dq_w, dq_y + dq_h], radius=6, fill=(254, 242, 242), outline=HIGHLIGHT_RED, width=2)
    draw.text((dq_xs[2] + dq_w // 2, dq_y + 16), "Worker 3 (IDLE)", fill=CRIMSON, font=font_badge, anchor="mm")
    draw.text((dq_xs[2] + dq_w // 2, dq_y + 70), "[ DEQUE EMPTY ]", fill=TEXT_MUTED, font=font_mono, anchor="mm")
    draw.text((dq_xs[2] + dq_w // 2, dq_y + 110), "Acts as Thief!", fill=CRIMSON, font=font_badge, anchor="mm")

    # Steal Arrow from Worker 3 to Worker 2 top
    draw_arrow(draw, dq_xs[2], dq_y + 110, dq_xs[1] + dq_w, dq_y + 55, color=CRIMSON, width=3)
    draw.text((dq_xs[1] + dq_w + 30, dq_y + 75), "Steals Top Task\n(Coarsest Grain)", fill=CRIMSON, font=get_font(11, bold=True), anchor="mm")

    # Bottom work stealing benefits card
    rx1 = rx + 20           # 680
    rx2 = rx + p_w - 20     # 1220
    draw.rounded_rectangle([rx1, card_y1, rx2, card_y2], radius=8, fill=(240, 253, 244), outline=CARD_BORDER_GOOD, width=1)
    draw.text((rx1 + 16, card_y1 + 12), "Why Work Stealing is Optimal (Blumofe & Leiserson 1999):", fill=(16, 120, 70), font=get_font(14, bold=True), anchor="lt")
    draw.line([rx1 + 16, card_y1 + 32, rx2 - 16, card_y1 + 32], fill=BOX_BORDER, width=1)

    ws_perks = [
        ("Zero Central Bottleneck", "Workers execute on local deques; zero cross-thread locking when busy."),
        ("LIFO Bottom Local Execution", "Worker pushes/pops at bottom (stack order) -> 100% warm L1/L2 cache reuse!"),
        ("FIFO Remote Stealing at Top", "Thieves steal from TOP -> Obtains highest subtrees (largest work granularity)."),
        ("Provably Optimal Communication Bound", "Total communication is bounded by O(p · L), independent of total work W!")
    ]
    wy_off = card_y1 + 38
    for lbl, desc in ws_perks:
        draw.text((rx1 + 16, wy_off), f"✓ {lbl}:", fill=NAVY, font=get_font(13, bold=True), anchor="lt")
        draw.text((rx1 + 30, wy_off + 17), desc, fill=TEXT_DARK, font=get_font(12, bold=False), anchor="lt")
        wy_off += 48

    img.save("extracted_images/lec18_dynamic_mapping_work_stealing.png")
    print("Saved lec18_dynamic_mapping_work_stealing.png")

# -------------------------------------------------------------
# 7. lec18_task_interaction_taxonomy.png
# Taxonomy of Tasks & Task Interaction Characteristics
# -------------------------------------------------------------
def create_task_interaction_taxonomy():
    W, H = SLIDE_W, SLIDE_H
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(21, bold=True)
    font_subhead = get_font(15, bold=False)
    font_badge = get_font(15.5, bold=True)
    font_lbl = get_font(14, bold=True)
    font_text = get_font(13.5, bold=False)

    draw.text((W // 2, 28), "Taxonomy of Tasks & Task Interaction Characteristics", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 56), "Replicating Slide 2 Overview: Task Generation, Granularity, Context & Task Interaction Profiles", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    p_w = 580
    p_h = 570

    # LEFT PANEL: Characteristics of Tasks (Slide 2)
    draw.rounded_rectangle([40, 80, 40 + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((40 + p_w // 2, 108), "Characteristics of Tasks (Grama Sec 3.3.1)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((40 + p_w // 2, 132), "Task Generation, Granularity, Sizes & Context Memory", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    task_tax = [
        ("1. Task Generation: Static vs. Dynamic", [
            ("Static", "All tasks known before run (e.g., Matrix Multiply, FFT) -> Static mapping."),
            ("Dynamic", "Tasks created at runtime (e.g., Quicksort recursion) -> Dynamic queues.")
        ]),
        ("2. Task Sizes: Uniform vs. Non-Uniform", [
            ("Uniform", "Identical compute time (e.g., dense dot products) -> Block mapping."),
            ("Non-Uniform", "Durations vary wildly (e.g., Mandelbrot, sparse rows) -> Load balancing.")
        ]),
        ("3. Knowledge of Task Sizes: Known vs. Unknown", [
            ("Known", "Predictable cost a priori -> Enables heuristic load balancing."),
            ("Unknown", "Cost unpredictable (e.g., branch-and-bound, SAT) -> Work stealing.")
        ]),
        ("4. Task Context & Data Footprint Size", [
            ("Small Context", "Minimal memory footprint -> Low overhead to migrate tasks."),
            ("Large Context", "Heavy memory footprint -> Bound to local RAM (no migration).")
        ])
    ]

    card_w = p_w - 40
    avail_w = card_w - 28
    box_h = 116
    ty = 152
    for title, items in task_tax:
        bx1 = 60
        bx2 = bx1 + card_w
        draw.rounded_rectangle([bx1, ty, bx2, ty + box_h], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
        draw.text((bx1 + 14, ty + 10), title, fill=NAVY, font=font_badge, anchor="lt")
        draw.line([bx1 + 14, ty + 32, bx2 - 14, ty + 32], fill=(226, 232, 240), width=1)
        
        cy = ty + 40
        for lbl, desc in items:
            prefix = f"• {lbl}: "
            pb = font_lbl.getbbox(prefix)
            pw = pb[2] - pb[0]
            draw.text((bx1 + 14, cy), prefix, fill=CRIMSON, font=font_lbl, anchor="lt")
            
            lines = wrap_text_multi(draw, desc, font_text, avail_w - pw, avail_w - 18)
            draw.text((bx1 + 14 + pw, cy), lines[0], fill=TEXT_DARK, font=font_text, anchor="lt")
            if len(lines) > 1:
                draw.text((bx1 + 24, cy + 20), lines[1], fill=TEXT_DARK, font=font_text, anchor="lt")
                cy += 40
            else:
                cy += 24
        ty += box_h + 10

    # RIGHT PANEL: Characteristics of Task Interactions (Slide 2)
    rx = 40 + p_w + 40
    draw.rounded_rectangle([rx, 80, rx + p_w, 80 + p_h], radius=10, fill=BOX_BG, outline=BOX_BORDER, width=2)
    draw.text((rx + p_w // 2, 108), "Characteristics of Interactions (Grama Sec 3.3.2)", fill=CRIMSON, font=font_head, anchor="mm")
    draw.text((rx + p_w // 2, 132), "Timing, Topologies, Read/Write Semantics & Coordination", fill=TEXT_MUTED, font=font_subhead, anchor="mm")

    inter_tax = [
        ("1. Static vs. Dynamic Interactions", [
            ("Static", "Communication partners & timing fixed in advance (e.g., Stencil halo)."),
            ("Dynamic", "Partners determined at runtime by data (e.g., N-body collisions).")
        ]),
        ("2. Regular vs. Irregular Interaction Topology", [
            ("Regular", "Structured communication graphs (e.g., 2D mesh, rings, trees)."),
            ("Irregular", "Arbitrary unstructured graphs (e.g., sparse meshes) -> Min-cut.")
        ]),
        ("3. Read-Only vs. Read-Write Data Sharing", [
            ("Read-Only", "Concurrent read access to inputs -> Lock-free, enables replication."),
            ("Read-Write", "Shared variable mutation across tasks -> Requires locks / atomics.")
        ]),
        ("4. One-Sided vs. Two-Sided Coordination", [
            ("Two-Sided", "Cooperative participation (sender: MPI_Send, receiver: MPI_Recv)."),
            ("One-Sided", "Remote Memory Access (RMA) -> Direct MPI_Put/Get without receiver.")
        ])
    ]

    ry = 152
    for title, items in inter_tax:
        bx1 = rx + 20
        bx2 = bx1 + card_w
        draw.rounded_rectangle([bx1, ry, bx2, ry + box_h], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
        draw.text((bx1 + 14, ry + 10), title, fill=CRIMSON, font=font_badge, anchor="lt")
        draw.line([bx1 + 14, ry + 32, bx2 - 14, ry + 32], fill=(226, 232, 240), width=1)
        
        cy = ry + 40
        for lbl, desc in items:
            prefix = f"• {lbl}: "
            pb = font_lbl.getbbox(prefix)
            pw = pb[2] - pb[0]
            draw.text((bx1 + 14, cy), prefix, fill=NAVY, font=font_lbl, anchor="lt")
            
            lines = wrap_text_multi(draw, desc, font_text, avail_w - pw, avail_w - 18)
            draw.text((bx1 + 14 + pw, cy), lines[0], fill=TEXT_DARK, font=font_text, anchor="lt")
            if len(lines) > 1:
                draw.text((bx1 + 24, cy + 20), lines[1], fill=TEXT_DARK, font=font_text, anchor="lt")
                cy += 40
            else:
                cy += 24
        ry += box_h + 10

    img.save("extracted_images/lec18_task_interaction_taxonomy.png")
    print("Saved lec18_task_interaction_taxonomy.png")

if __name__ == "__main__":
    create_processes_vs_processors()
    create_mapping_tradeoff_idling_comm()
    create_data_partitioning_1d_2d()
    create_sparse_graph_partitioning()
    create_hierarchical_mapping_tree()
    create_dynamic_mapping_work_stealing()
    create_task_interaction_taxonomy()
    print("All Lecture 18 images generated successfully!")
