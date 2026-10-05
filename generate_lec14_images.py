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
# 1. lec14_process_mapping_impact.png
# (a) 4x4 Physical Mesh (Processors 1..16)
# (b) 4x4 Process Graph (Processes a..p)
# (c) Identity / Good Mapping (Dilation=1, Congestion=1)
# (d) Scrambled / Bad Mapping (Multi-hop routing, Link Contention)
# -------------------------------------------------------------
def create_process_mapping_impact():
    W, H = 1200, 640
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_subhead = get_font(14, bold=False)
    font_node = get_font(15, bold=True)
    font_badge = get_font(14, bold=True)
    font_notes = get_font(14, bold=False)

    # Title & Subtitle
    draw.text((W // 2, 26), "Impact of Process-to-Processor Mapping", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Mapping logical communication graphs onto physical hardware topologies dictates performance", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    panel_w = 265
    panel_h = 535
    gap = 20
    start_x = 35
    top_y = 80

    panels = [
        {"title": "(a) Physical 4x4 Mesh", "sub": "16 Physical Processors (1-16)", "bg": BOX_BG, "border": BOX_BORDER, "type": "phys"},
        {"title": "(b) Logical Process Graph", "sub": "16 Interacting Tasks (a-p)", "bg": BOX_BG, "border": BOX_BORDER, "type": "proc"},
        {"title": "(c) Optimal Mapping", "sub": "Identity Embedding (D=1, C=1)", "bg": CARD_BG_GOOD, "border": CARD_BORDER_GOOD, "type": "opt"},
        {"title": "(d) Poor / Scrambled", "sub": "Uncoordinated (High D & C)", "bg": CARD_BG_BAD, "border": CARD_BORDER_BAD, "type": "bad"}
    ]

    grid_size = 4
    spacing = 48

    for idx, p in enumerate(panels):
        px = start_x + idx * (panel_w + gap)
        py = top_y
        draw.rounded_rectangle([px, py, px + panel_w, py + panel_h], radius=8, fill=p["bg"], outline=p["border"], width=2)
        draw.text((px + panel_w // 2, py + 24), p["title"], fill=NAVY if idx < 3 else CRIMSON, font=font_head, anchor="mm")
        draw.text((px + panel_w // 2, py + 46), p["sub"], fill=TEXT_MUTED, font=font_subhead, anchor="mm")

        gx_start = px + (panel_w - (grid_size - 1) * spacing) // 2
        gy_start = py + 80

        for r in range(grid_size):
            for c in range(grid_size):
                x = gx_start + c * spacing
                y = gy_start + r * spacing
                if c < grid_size - 1:
                    edge_col = (148, 163, 184) if p["type"] != "bad" else (203, 213, 225)
                    edge_w = 2 if p["type"] != "bad" else 1
                    draw.line([(x, y), (x + spacing, y)], fill=edge_col, width=edge_w)
                if r < grid_size - 1:
                    edge_col = (148, 163, 184) if p["type"] != "bad" else (203, 213, 225)
                    edge_w = 2 if p["type"] != "bad" else 1
                    draw.line([(x, y), (x, y + spacing)], fill=edge_col, width=edge_w)

        scrambled = [
            'k', 'h', 'm', 'i',
            'j', 'p', 'o', 'b',
            'd', 'e', 'a', 'n',
            'c', 'l', 'g', 'f'
        ]

        for r in range(grid_size):
            for c in range(grid_size):
                x = gx_start + c * spacing
                y = gy_start + r * spacing
                node_idx = r * 4 + c

                if p["type"] == "phys":
                    draw.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(224, 231, 255), outline=NAVY_LIGHT, width=2)
                    draw.text((x, y), str(node_idx + 1), fill=NAVY, font=font_node, anchor="mm")
                elif p["type"] == "proc":
                    char = chr(ord('a') + node_idx)
                    draw.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(254, 240, 138), outline=(202, 138, 4), width=2)
                    draw.text((x, y), char, fill=(113, 63, 18), font=font_node, anchor="mm")
                elif p["type"] == "opt":
                    char = chr(ord('a') + node_idx)
                    draw.ellipse([x - 17, y - 17, x + 17, y + 17], fill=(220, 252, 231), outline=(22, 163, 74), width=2)
                    draw.text((x - 5, y - 5), str(node_idx + 1), fill=(21, 128, 61), font=get_font(12, bold=True), anchor="mm")
                    draw.text((x + 5, y + 4), char, fill=NAVY, font=get_font(14, bold=True), anchor="mm")
                elif p["type"] == "bad":
                    char = scrambled[node_idx]
                    draw.ellipse([x - 17, y - 17, x + 17, y + 17], fill=(254, 226, 226), outline=(220, 38, 38), width=2)
                    draw.text((x - 5, y - 5), str(node_idx + 1), fill=TEXT_MUTED, font=get_font(12, bold=True), anchor="mm")
                    draw.text((x + 5, y + 4), char, fill=CRIMSON, font=get_font(14, bold=True), anchor="mm")

        if p["type"] == "bad":
            xa = gx_start + 2 * spacing
            ya = gy_start + 2 * spacing
            xb = gx_start + 3 * spacing
            yb = gy_start + 1 * spacing
            x_mid = gx_start + 2 * spacing
            y_mid = gy_start + 1 * spacing
            draw.line([(xa, ya), (x_mid, y_mid)], fill=CRIMSON, width=3)
            draw.line([(x_mid, y_mid), (xb, yb)], fill=CRIMSON, width=3)
            draw.text((x_mid - 44, (ya + y_mid) // 2 - 8), "2 hops", fill=CRIMSON, font=font_badge)

        bx1, by1, bx2, by2 = px + 10, py + 285, px + panel_w - 10, py + panel_h - 15
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=(255, 255, 255), outline=p["border"], width=1)

        if p["type"] == "phys":
            notes = [
                "• 2D Mesh Interconnect",
                "• 16 Compute Cores",
                "• Nearest-neighbor links",
                "• Bisection width B = 4",
                "• Diameter = 6 hops"
            ]
        elif p["type"] == "proc":
            notes = [
                "• Computational tasks",
                "• 2D stencil pattern",
                "• (u, v) interact heavily",
                "• Balanced workload",
                "• 24 communication edges"
            ]
        elif p["type"] == "opt":
            notes = [
                "• Task 'k' mapped to P_k",
                "• Dilation = 1 (1 hop)",
                "• Congestion = 1 (no share)",
                "• Zero queuing stalls",
                "• Peak throughput"
            ]
        else:
            notes = [
                "• Random core allocation",
                "• (a, b) needs 2 hops",
                "• High Dilation (4-5 hops)",
                "• High Link Congestion",
                "• Severe contention!"
            ]

        ny = by1 + 18
        for note in notes:
            col = NAVY if p["type"] != "bad" else (185, 28, 28)
            draw.text((bx1 + 14, ny), note, fill=col, font=font_notes)
            ny += 38

    img.save("extracted_images/lec14_process_mapping_impact.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_process_mapping_impact.png")

# -------------------------------------------------------------
# 2. lec14_graph_embedding_metrics.png
# Formal Graph Embedding Metrics & Visual Intuition
# -------------------------------------------------------------
def create_graph_embedding_metrics():
    W, H = 1140, 560
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_bold = get_font(16, bold=True)
    font_sm = get_font(14, bold=False)
    font_math = get_font(15, bold=True)

    draw.text((W // 2, 26), "Graph Embedding Fundamentals: Core Metrics", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Mapping Guest Graph G(V, E) into Host Graph G'(V', E') via embedding function phi", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    lx1, ly1, lx2, ly2 = 40, 80, 530, 530
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((lx1 + lx2) // 2, ly1 + 22), "Embedding Function: phi: G -> G'", fill=NAVY, font=font_head, anchor="mm")

    # Guest Graph Box
    draw.rounded_rectangle([lx1 + 15, ly1 + 45, lx1 + 215, ly1 + 205], radius=6, fill=(254, 240, 138), outline=(202, 138, 4), width=1)
    draw.text((lx1 + 115, ly1 + 68), "Guest Graph G(V, E)", fill=(113, 63, 18), font=font_bold, anchor="mm")
    draw.text((lx1 + 115, ly1 + 88), "(Logical Algorithm)", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    gnodes = [(lx1 + 55, ly1 + 125), (lx1 + 175, ly1 + 125), (lx1 + 55, ly1 + 175), (lx1 + 175, ly1 + 175)]
    glabels = ["u", "v", "w", "z"]
    draw.line([gnodes[0], gnodes[1]], fill=(180, 83, 9), width=3)
    draw.line([gnodes[0], gnodes[2]], fill=(180, 83, 9), width=2)
    draw.line([gnodes[1], gnodes[3]], fill=(180, 83, 9), width=2)
    draw.line([gnodes[2], gnodes[3]], fill=(180, 83, 9), width=2)
    draw.line([gnodes[0], gnodes[3]], fill=CRIMSON, width=3)

    for pt, lbl in zip(gnodes, glabels):
        draw.ellipse([pt[0]-15, pt[1]-15, pt[0]+15, pt[1]+15], fill=(254, 249, 195), outline=(161, 98, 7), width=2)
        draw.text(pt, lbl, fill=(113, 63, 18), font=font_bold, anchor="mm")

    draw.text((lx1 + 115, ly1 + 135), "e = (u,v)", fill=(180, 83, 9), font=get_font(13, bold=True), anchor="mm")

    # Mapping Arrow
    draw.line([(lx1 + 225, ly1 + 125), (lx1 + 265, ly1 + 125)], fill=NAVY_LIGHT, width=3)
    draw.polygon([(lx1 + 265, ly1 + 118), (lx1 + 277, ly1 + 125), (lx1 + 265, ly1 + 132)], fill=NAVY_LIGHT)
    draw.text((lx1 + 248, ly1 + 108), "phi", fill=NAVY, font=font_bold, anchor="mm")

    # Host Graph Box
    draw.rounded_rectangle([lx1 + 285, ly1 + 45, lx2 - 15, ly1 + 205], radius=6, fill=(224, 231, 255), outline=NAVY_LIGHT, width=1)
    draw.text((lx1 + 390, ly1 + 68), "Host Graph G'(V', E')", fill=NAVY, font=font_bold, anchor="mm")
    draw.text((lx1 + 390, ly1 + 88), "(Hardware System)", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    hnodes = [(lx1 + 315, ly1 + 125), (lx1 + 365, ly1 + 125), (lx1 + 415, ly1 + 125), (lx1 + 465, ly1 + 125),
              (lx1 + 315, ly1 + 175), (lx1 + 365, ly1 + 175), (lx1 + 415, ly1 + 175), (lx1 + 465, ly1 + 175)]
    for i in range(3):
        draw.line([hnodes[i], hnodes[i+1]], fill=(148, 163, 184), width=2)
        draw.line([hnodes[i+4], hnodes[i+5]], fill=(148, 163, 184), width=2)
    for i in range(4):
        draw.line([hnodes[i], hnodes[i+4]], fill=(148, 163, 184), width=2)

    draw.line([hnodes[0], hnodes[1]], fill=HIGHLIGHT_BLUE, width=4)
    draw.line([hnodes[1], hnodes[2]], fill=HIGHLIGHT_BLUE, width=4)
    draw.line([(hnodes[0][0], hnodes[0][1]+3), (hnodes[1][0], hnodes[1][1]+3)], fill=CRIMSON, width=3)

    for idx, pt in enumerate(hnodes):
        draw.ellipse([pt[0]-13, pt[1]-13, pt[0]+13, pt[1]+13], fill=(238, 242, 255), outline=NAVY, width=2)
        draw.text(pt, str(idx), fill=NAVY, font=get_font(12, bold=True), anchor="mm")

    # Bottom visual annotations
    draw.rounded_rectangle([lx1 + 15, ly1 + 225, lx2 - 15, ly2 - 15], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((lx1 + 30, ly1 + 245), "Key Visual Observations:", fill=NAVY, font=font_bold)
    draw.text((lx1 + 30, ly1 + 278), "1. Dilation = 2: Guest edge (u, v) maps to 2 physical links (h0-h1-h2).", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 30, ly1 + 312), "2. Congestion = 2: Physical link (h0-h1) carries 2 guest paths (blue & red).", fill=CRIMSON, font=font_sm)
    draw.text((lx1 + 30, ly1 + 346), "3. Expansion = |V'| / |V| = 8 / 4 = 2.0 (Host has 2x nodes of Guest).", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 30, ly1 + 380), "4. Load = 1: At most 1 guest process mapped to each processor node.", fill=TEXT_DARK, font=font_sm)

    # Right: Mathematical Metrics & Formulas
    rx1, ry1, rx2, ry2 = 550, 80, 1100, 530
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((rx1 + rx2) // 2, ry1 + 22), "Mathematical Metrics & Physical Impact", fill=NAVY, font=font_head, anchor="mm")

    metric_boxes = [
        {"title": "1. Dilation (D) • Latency Overhead",
         "formula": "D = max |phi_E(e)|",
         "desc1": "Maximum physical hops traversed by any logical message edge.",
         "desc2": "Directly multiplies packet transfer time in Store-and-Forward networks.",
         "col": HIGHLIGHT_BLUE, "bg": (239, 246, 255), "border": (191, 219, 254)},
        {"title": "2. Congestion (C) • Bandwidth Bottleneck",
         "formula": "C = max |paths(e')|",
         "desc1": "Maximum number of logical paths sharing any single physical link.",
         "desc2": "Bottlenecks throughput: effective channel bandwidth throttles to B / C.",
         "col": CRIMSON, "bg": (254, 242, 242), "border": (254, 202, 202)},
        {"title": "3. Expansion (X) & Load (L)",
         "formula": "X = |V'| / |V|,  L = max |phi_V^-1|",
         "desc1": "Expansion measures hardware resource utilization efficiency.",
         "desc2": "Load measures process oversubscription per processor node.",
         "col": (180, 83, 9), "bg": (254, 252, 232), "border": (254, 240, 138)},
        {"title": "4. Leighton's Bisection Lower Bound Theorem",
         "formula": "C >= B(G) / B(G')",
         "desc1": "Any bisection of host graph severs at most B(G') physical links,",
         "desc2": "which must carry all B(G) crossing paths => Congestion C >= B(G)/B(G').",
         "col": (21, 128, 61), "bg": (240, 253, 244), "border": (187, 247, 208)}
    ]

    my = ry1 + 45
    card_h = 92
    for m in metric_boxes:
        draw.rounded_rectangle([rx1 + 16, my, rx2 - 16, my + card_h], radius=6, fill=m["bg"], outline=m["border"], width=1)
        draw.text((rx1 + 26, my + 14), m["title"], fill=m["col"], font=font_bold)
        draw.text((rx2 - 25, my + 14), m["formula"], fill=NAVY, font=font_math, anchor="ra")
        draw.text((rx1 + 26, my + 42), m["desc1"], fill=TEXT_DARK, font=font_sm)
        draw.text((rx1 + 26, my + 64), m["desc2"], fill=TEXT_MUTED, font=font_sm)
        my += card_h + 12

    img.save("extracted_images/lec14_graph_embedding_metrics.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_graph_embedding_metrics.png")

# -------------------------------------------------------------
# 3. lec14_gray_code_hypercube.png
# Binary Reflected Gray Code (RGC) Table & 3D Hypercube Ring Embedding
# -------------------------------------------------------------
def create_gray_code_hypercube():
    W, H = 1140, 560
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_bold = get_font(16, bold=True)
    font_sm = get_font(14, bold=False)
    font_mono = get_font(16, bold=True)

    draw.text((W // 2, 26), "Binary Reflected Gray Code & Hypercube Ring Embedding", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Successive elements differ in exactly 1 bit, mapping ring adjacency to direct hypercube edges", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    lx1, ly1, lx2, ly2 = 40, 80, 550, 530
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((lx1 + lx2) // 2, ly1 + 22), "1. Binary Reflected Gray Code (RGC) Construction", fill=NAVY, font=font_head, anchor="mm")

    col_x = [lx1 + 25, lx1 + 95, lx1 + 185, lx1 + 300, lx1 + 415]
    headers = ["1-bit", "2-bit", "3-bit RGC", "Ring Node", "Cube Node"]
    for i, h in enumerate(headers):
        draw.text((col_x[i], ly1 + 48), h, fill=NAVY, font=font_bold)

    rgc_3bit = ["000", "001", "011", "010", "110", "111", "101", "100"]
    cube_int = [0, 1, 3, 2, 6, 7, 5, 4]

    row_y_start = ly1 + 78
    row_h = 34
    for r in range(8):
        ry = row_y_start + r * row_h
        row_bg = (255, 255, 255) if r % 2 == 0 else (241, 245, 249)
        draw.rounded_rectangle([lx1 + 15, ry, lx2 - 15, ry + row_h - 4], radius=4, fill=row_bg, outline=None)

        if r < 2:
            draw.text((col_x[0] + 12, ry + 6), str(r), fill=TEXT_DARK, font=font_mono)
        if r < 4:
            b2 = ["00", "01", "11", "10"][r]
            draw.text((col_x[1] + 12, ry + 6), b2, fill=TEXT_DARK, font=font_mono)

        draw.text((col_x[2] + 18, ry + 6), rgc_3bit[r], fill=HIGHLIGHT_BLUE, font=font_mono)
        draw.text((col_x[3] + 20, ry + 6), f"Node {r}", fill=NAVY, font=font_bold)
        draw.text((col_x[4] + 20, ry + 6), f"P_{cube_int[r]}", fill=CRIMSON, font=font_bold)

    # Dashed reflection line on left side
    ref_y = row_y_start + 4 * row_h - 2
    for x in range(lx1 + 20, lx2 - 20, 8):
        draw.line([(x, ref_y), (x + 4, ref_y)], fill=GOLD, width=2)
    draw.text((col_x[0] + 5, ref_y - 16), "Prepend 0 ^", fill=(180, 83, 9), font=get_font(11, bold=True))
    draw.text((col_x[0] + 5, ref_y + 4), "Prepend 1 v", fill=CRIMSON, font=get_font(11, bold=True))

    draw.rounded_rectangle([lx1 + 15, ly2 - 80, lx2 - 15, ly2 - 15], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx1 + 25, ly2 - 70), "Gray Code Recurrence: G(0, 1) = 0,  G(1, 1) = 1", fill=NAVY, font=font_bold)
    draw.text((lx1 + 25, ly2 - 42), "G(i, x+1) = G(i, x) if i < 2^x  else  2^x + G(2^{x+1} - 1 - i, x)", fill=HIGHLIGHT_BLUE, font=get_font(14, bold=True))

    # Right Panel: 3D Hypercube Hamiltonian Cycle Ring Embedding
    rx1, ry1, rx2, ry2 = 570, 80, 1100, 530
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((rx1 + rx2) // 2, ry1 + 22), "2. Ring Embedded in 3-D Hypercube (Q3)", fill=NAVY, font=font_head, anchor="mm")
    draw.text(((rx1 + rx2) // 2, ry1 + 44), "Hamiltonian Cycle: Congestion = 1, Dilation = 1, Expansion = 1", fill=(21, 128, 61), font=font_bold, anchor="mm")

    cx = (rx1 + rx2) // 2
    cy = ry1 + 240

    f_bl = (cx - 100, cy + 60)
    f_br = (cx + 50, cy + 60)
    f_tr = (cx + 50, cy - 70)
    f_tl = (cx - 100, cy - 70)

    dx, dy = 70, -55
    b_bl = (f_bl[0] + dx, f_bl[1] + dy)
    b_br = (f_br[0] + dx, f_br[1] + dy)
    b_tr = (f_tr[0] + dx, f_tr[1] + dy)
    b_tl = (f_tl[0] + dx, f_tl[1] + dy)

    cube_all_edges = [
        (f_bl, f_br), (f_br, f_tr), (f_tr, f_tl), (f_tl, f_bl),
        (b_bl, b_br), (b_br, b_tr), (b_tr, b_tl), (b_tl, b_bl),
        (f_bl, b_bl), (f_br, b_br), (f_tr, b_tr), (f_tl, b_tl)
    ]
    for p1, p2 in cube_all_edges:
        draw.line([p1, p2], fill=(203, 213, 225), width=2)

    ring_cycle = [
        (f_bl, f_br), (f_br, f_tr), (f_tr, f_tl), (f_tl, b_tl),
        (b_tl, b_tr), (b_tr, b_br), (b_br, b_bl), (b_bl, f_bl)
    ]
    for p1, p2 in ring_cycle:
        draw.line([p1, p2], fill=HIGHLIGHT_BLUE, width=4)

    cube_nodes = [
        (f_bl, "000 (0)", (239, 246, 255), NAVY),
        (f_br, "001 (1)", (239, 246, 255), NAVY),
        (f_tr, "011 (3)", (239, 246, 255), NAVY),
        (f_tl, "010 (2)", (239, 246, 255), NAVY),
        (b_bl, "100 (4)", (254, 242, 242), CRIMSON),
        (b_br, "101 (5)", (254, 242, 242), CRIMSON),
        (b_tr, "111 (7)", (254, 242, 242), CRIMSON),
        (b_tl, "110 (6)", (254, 242, 242), CRIMSON)
    ]
    for pt, lbl, bg, fg in cube_nodes:
        draw.ellipse([pt[0]-18, pt[1]-18, pt[0]+18, pt[1]+18], fill=bg, outline=fg, width=2)
        draw.text(pt, lbl.split()[0], fill=fg, font=get_font(12, bold=True), anchor="mm")

    # Bottom takeaway in 2 clean lines
    draw.rounded_rectangle([rx1 + 15, ly2 - 80, rx2 - 15, ly2 - 15], radius=6, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((rx1 + 25, ly2 - 70), "Key Takeaway: Hamiltonian Cycle in Hypercube", fill=(21, 128, 61), font=font_bold)
    draw.text((rx1 + 25, ly2 - 46), "Every ring neighbor is separated by Hamming distance = 1.", fill=TEXT_DARK, font=font_sm)
    draw.text((rx1 + 25, ly2 - 28), "Congestion = 1, Dilation = 1, Expansion = 1. Complete hardware efficiency!", fill=(21, 128, 61), font=get_font(13, bold=True))

    img.save("extracted_images/lec14_gray_code_hypercube.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_gray_code_hypercube.png")

# -------------------------------------------------------------
# 4. lec14_mesh_into_hypercube.png
# Embedding 2D Mesh into Hypercube via Gray Code Concatenation
# -------------------------------------------------------------
def create_mesh_into_hypercube():
    W, H = 1140, 560
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_bold = get_font(16, bold=True)
    font_sm = get_font(14, bold=False)

    draw.text((W // 2, 26), "Embedding a 2D Mesh into a Hypercube", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Mapping node (i, j) to G(i, r) || G(j, s) achieves Congestion = 1, Dilation = 1, Expansion = 1", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    lx1, ly1, lx2, ly2 = 40, 80, 530, 530
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((lx1 + lx2) // 2, ly1 + 22), "1. Example: 2 x 4 Mesh into 3-D Hypercube", fill=NAVY, font=font_head, anchor="mm")
    draw.text(((lx1 + lx2) // 2, ly1 + 44), "r = 1 (1-bit row Gray code),  s = 2 (2-bit col Gray code)", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    m_spacing_x = 95
    m_spacing_y = 95
    m_start_x = lx1 + 55
    m_start_y = ly1 + 82

    mesh_2x4 = [
        [("(0,0)", "0 00"), ("(0,1)", "0 01"), ("(0,2)", "0 11"), ("(0,3)", "0 10")],
        [("(1,0)", "1 00"), ("(1,1)", "1 01"), ("(1,2)", "1 11"), ("(1,3)", "1 10")]
    ]

    for r in range(2):
        for c in range(4):
            x = m_start_x + c * m_spacing_x
            y = m_start_y + r * m_spacing_y
            if c < 3:
                draw.line([(x, y), (x + m_spacing_x, y)], fill=NAVY_LIGHT, width=2)
            if r < 1:
                draw.line([(x, y), (x, y + m_spacing_y)], fill=NAVY_LIGHT, width=2)

    for r in range(2):
        for c in range(4):
            x = m_start_x + c * m_spacing_x
            y = m_start_y + r * m_spacing_y
            coord_str, code_str = mesh_2x4[r][c]
            draw.ellipse([x - 24, y - 24, x + 24, y + 24], fill=(255, 255, 255), outline=NAVY, width=2)
            draw.text((x, y - 7), coord_str, fill=NAVY, font=get_font(12, bold=True), anchor="mm")
            draw.text((x, y + 8), code_str, fill=CRIMSON, font=get_font(12, bold=True), anchor="mm")

    draw.rounded_rectangle([lx1 + 15, ly1 + 235, lx2 - 15, ly2 - 15], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((lx1 + 25, ly1 + 252), "Neighbor Hamming Distance Analysis:", fill=NAVY, font=font_bold)
    draw.text((lx1 + 25, ly1 + 280), "• Horizontal Neighbors: (0,0) [0 00] and (0,1) [0 01]", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 40, ly1 + 302), "Row bit '0' is identical; col Gray code differs by 1 bit -> H = 1", fill=HIGHLIGHT_BLUE, font=font_sm)
    draw.text((lx1 + 25, ly1 + 332), "• Vertical Neighbors: (0,1) [0 01] and (1,1) [1 01]", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 40, ly1 + 354), "Col bits '01' are identical; row Gray code differs by 1 bit -> H = 1", fill=HIGHLIGHT_BLUE, font=font_sm)
    draw.text((lx1 + 25, ly1 + 384), "• Torus Wraparound: (0,3) [0 10] and (0,0) [0 00] differ by 1 bit!", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 25, ly1 + 414), "=> All 2x4 mesh & torus edges map to direct hypercube links!", fill=(21, 128, 61), font=font_bold)

    # Right: 4x4 Mesh into 4-D Hypercube (16 nodes)
    rx1, ry1, rx2, ry2 = 550, 80, 1100, 530
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((rx1 + rx2) // 2, ry1 + 22), "2. 4 x 4 Mesh into 4-D Hypercube (Q4)", fill=NAVY, font=font_head, anchor="mm")
    draw.text(((rx1 + rx2) // 2, ry1 + 44), "r = 2, s = 2: Node (i, j) -> G(i, 2) || G(j, 2)", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    g4_spacing = 56
    g4_x0 = rx1 + 105
    g4_y0 = ry1 + 95
    gray_2b = ["00", "01", "11", "10"]

    for c in range(4):
        draw.text((g4_x0 + c * g4_spacing, g4_y0 - 24), f"c={c} [{gray_2b[c]}]", fill=HIGHLIGHT_BLUE, font=get_font(12, bold=True), anchor="mm")
    for r in range(4):
        draw.text((g4_x0 - 62, g4_y0 + r * g4_spacing), f"r={r} [{gray_2b[r]}]", fill=CRIMSON, font=get_font(12, bold=True), anchor="mm")

    for r in range(4):
        for c in range(4):
            x = g4_x0 + c * g4_spacing
            y = g4_y0 + r * g4_spacing
            if c < 3:
                draw.line([(x, y), (x + g4_spacing, y)], fill=(148, 163, 184), width=1)
            if r < 3:
                draw.line([(x, y), (x, y + g4_spacing)], fill=(148, 163, 184), width=1)

    for r in range(4):
        for c in range(4):
            x = g4_x0 + c * g4_spacing
            y = g4_y0 + r * g4_spacing
            label = f"{gray_2b[r]} {gray_2b[c]}"
            draw.ellipse([x - 19, y - 19, x + 19, y + 19], fill=(255, 255, 255), outline=NAVY, width=2)
            draw.text((x, y - 5), f"({r},{c})", fill=NAVY, font=get_font(10, bold=True), anchor="mm")
            draw.text((x, y + 6), label, fill=CRIMSON, font=get_font(9, bold=True), anchor="mm")

    m_card_top = ly1 + 295
    draw.rounded_rectangle([rx1 + 15, m_card_top, rx2 - 15, ly2 - 15], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((rx1 + 25, m_card_top + 12), "Row & Column Invariance Properties:", fill=NAVY, font=font_bold)
    draw.text((rx1 + 25, m_card_top + 36), "1. Row Invariance: Processors in row r share identical 2 MSBs.", fill=CRIMSON, font=font_sm)
    draw.text((rx1 + 25, m_card_top + 60), "2. Column Invariance: Processors in col c share identical 2 LSBs.", fill=HIGHLIGHT_BLUE, font=font_sm)
    draw.text((rx1 + 25, m_card_top + 84), "• Generalization: k-D Torus of size 2^{d1} x ... x 2^{dk} embeds into a", fill=TEXT_DARK, font=font_sm)
    draw.text((rx1 + 40, m_card_top + 106), "(sum d_i)-D Hypercube with D = 1, C = 1, X = 1.", fill=(21, 128, 61), font=font_bold)

    img.save("extracted_images/lec14_mesh_into_hypercube.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_mesh_into_hypercube.png")

# -------------------------------------------------------------
# 5. lec14_mesh_linear_array_embedding.png
# Linear Array to Mesh (Snake) vs Inverted Mesh to Linear Array (Congestion=5)
# -------------------------------------------------------------
def create_mesh_linear_array_embedding():
    W, H = 1140, 560
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_bold = get_font(16, bold=True)
    font_sm = get_font(14, bold=False)

    draw.text((W // 2, 26), "Embedding Between 2D Mesh and Linear Array", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Forward Mapping (Congestion 1) vs. Inverted Mapping Bottlenecks (Congestion 5)", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    lx1, ly1, lx2, ly2 = 40, 80, 480, 530
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((lx1 + lx2) // 2, ly1 + 22), "(a) Linear Array into 2D Mesh", fill=NAVY, font=font_head, anchor="mm")
    draw.text(((lx1 + lx2) // 2, ly1 + 44), "Serpentine / Snake-like embedding (C = 1, D = 1)", fill=TEXT_MUTED, font=font_sm, anchor="mm")

    spacing = 62
    sx0 = lx1 + 80
    sy0 = ly1 + 75
    snake_coords = [
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 3), (1, 2), (1, 1), (1, 0),
        (2, 0), (2, 1), (2, 2), (2, 3),
        (3, 3), (3, 2), (3, 1), (3, 0)
    ]
    for i in range(15):
        r1, c1 = snake_coords[i]
        r2, c2 = snake_coords[i+1]
        draw.line([(sx0 + c1 * spacing, sy0 + r1 * spacing), (sx0 + c2 * spacing, sy0 + r2 * spacing)], fill=NAVY_LIGHT, width=4)

    for i in range(16):
        r, c = snake_coords[i]
        x = sx0 + c * spacing
        y = sy0 + r * spacing
        draw.ellipse([x - 17, y - 17, x + 17, y + 17], fill=(255, 255, 255), outline=NAVY, width=2)
        draw.text((x, y), str(i), fill=NAVY, font=get_font(13, bold=True), anchor="mm")

    draw.rounded_rectangle([lx1 + 15, ly2 - 145, lx2 - 15, ly2 - 15], radius=6, fill=CARD_BG_GOOD, outline=CARD_BORDER_GOOD, width=1)
    draw.text((lx1 + 25, ly2 - 130), "Forward Mapping Metrics (Linear -> Mesh):", fill=(21, 128, 61), font=font_bold)
    draw.text((lx1 + 25, ly2 - 100), "• Dilation = 1 (Every linear link is an adjacent mesh edge)", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 25, ly2 - 72), "• Congestion = 1 (At most 1 linear link per mesh channel)", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 25, ly2 - 44), "• Expansion = 1 (16 linear nodes in 16 mesh nodes)", fill=TEXT_DARK, font=font_sm)

    # Right Panel: Inverting Mapping
    rx1, ry1, rx2, ry2 = 500, 80, 1100, 530
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((rx1 + rx2) // 2, ry1 + 22), "(b) Inverting Mapping: 2D Mesh into Linear Array", fill=NAVY, font=font_head, anchor="mm")
    draw.text(((rx1 + rx2) // 2, ry1 + 44), "High Dilation (up to 7) & Severe Link Congestion (Congestion = 5)", fill=CRIMSON, font=font_bold, anchor="mm")

    lin_y = ry1 + 240
    lin_spacing = 35
    lin_x0 = rx1 + 35

    draw.line([(lin_x0, lin_y), (lin_x0 + 15 * lin_spacing, lin_y)], fill=NAVY_LIGHT, width=4)

    arcs = [
        (0, 7, 65), (8, 15, 65),
        (1, 6, 50), (6, 9, 36), (9, 14, 50),
        (2, 5, 32), (5, 10, 50), (10, 13, 32),
        (4, 11, 65)
    ]
    for u, v, arc_h in arcs:
        x_u = lin_x0 + u * lin_spacing
        x_v = lin_x0 + v * lin_spacing
        pts = []
        for s in range(31):
            t = s / 30
            px = x_u + t * (x_v - x_u)
            py = lin_y - math.sin(t * math.pi) * arc_h * 2.0
            pts.append((px, py))
        draw.line(pts, fill=CRIMSON, width=2)

    cut_positions = [
        (lin_x0 + 3.5 * lin_spacing, "Cut 1"),
        (lin_x0 + 7.5 * lin_spacing, "Bisection Cut (C = 5)"),
        (lin_x0 + 11.5 * lin_spacing, "Cut 3")
    ]
    for cx_val, cut_lbl in cut_positions:
        for y in range(ry1 + 75, lin_y + 35, 6):
            draw.line([(cx_val, y), (cx_val, y + 3)], fill=(148, 163, 184), width=1)
        if "Bisection" in cut_lbl:
            draw.text((cx_val, ry1 + 68), cut_lbl, fill=CRIMSON, font=get_font(13, bold=True), anchor="mm")

    for idx in range(16):
        x = lin_x0 + idx * lin_spacing
        draw.ellipse([x - 12, lin_y - 12, x + 12, lin_y + 12], fill=(255, 255, 255), outline=NAVY, width=2)
        draw.text((x, lin_y), str(idx), fill=NAVY, font=get_font(11, bold=True), anchor="mm")

    draw.text((lin_x0 + 7.5 * lin_spacing, lin_y + 26), "▲ Peak: 5 paths across link 7-8", fill=CRIMSON, font=get_font(14, bold=True), anchor="mm")

    bx1, by1, bx2, by2 = rx1 + 15, ly2 - 165, rx2 - 15, ly2 - 15
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=CARD_BG_BAD, outline=CARD_BORDER_BAD, width=1)
    draw.text((bx1 + 14, by1 + 12), "Why Inverted Mapping Suffers Congestion = 5 & Dilation = 7:", fill=CRIMSON, font=font_bold)
    draw.text((bx1 + 14, by1 + 38), "• Dilation D = 2k - 1 = 2(4) - 1 = 7 hops (e.g. edge (0, 7) stretches 7 links).", fill=TEXT_DARK, font=font_sm)
    draw.text((bx1 + 14, by1 + 66), "• Congestion C = 5 on central link (nodes 7 to 8):", fill=CRIMSON, font=font_bold)
    draw.text((bx1 + 28, by1 + 90), "1 backbone link + edges (6,9), (5,10), (4,11), and (0,7)/(8,15) = 5 paths!", fill=TEXT_DARK, font=font_sm)
    draw.text((bx1 + 14, by1 + 118), "• Bisection lower bound: Mesh B = 4, Linear B = 1 => C >= 4/1 = 4 (Snake hits 5).", fill=TEXT_MUTED, font=font_sm)

    img.save("extracted_images/lec14_mesh_linear_array_embedding.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_mesh_linear_array_embedding.png")

# -------------------------------------------------------------
# 6. lec14_hypercube_into_mesh_bisection.png
# Embedding a Hypercube into a 2D Mesh & Bisection Bandwidth Lower Bound
# -------------------------------------------------------------
def create_hypercube_into_mesh_bisection():
    W, H = 1140, 560
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_sub = get_font(16, bold=False)
    font_head = get_font(18, bold=True)
    font_bold = get_font(16, bold=True)
    font_sm = get_font(14, bold=False)
    font_math = get_font(15, bold=True)

    draw.text((W // 2, 26), "Embedding a Hypercube into a 2-D Mesh: Bisection Lower Bound", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Proving why high-dimensional networks suffer unavoidable Congestion >= sqrt(p) / 4 when mapped to 2D silicon", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    lx1, ly1, lx2, ly2 = 40, 80, 530, 530
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((lx1 + lx2) // 2, ly1 + 22), "1. Network Bisection Bandwidth Comparison", fill=NAVY, font=font_head, anchor="mm")

    # Hypercube Bisection Box
    draw.rounded_rectangle([lx1 + 15, ly1 + 45, lx2 - 15, ly1 + 185], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx1 + 25, ly1 + 65), "p-Node Hypercube (Q_d, d = log2 p)", fill=NAVY, font=font_bold)
    draw.text((lx1 + 25, ly1 + 92), "• Bisection Width B(Q_d) = p / 2", fill=HIGHLIGHT_BLUE, font=font_math)
    draw.text((lx1 + 25, ly1 + 118), "• A balanced partition separates p/2 nodes on each side.", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 25, ly1 + 142), "• For p = 64 nodes: Bisection Width = 32 links.", fill=CRIMSON, font=font_bold)

    # 2D Mesh Bisection Box
    draw.rounded_rectangle([lx1 + 15, ly1 + 200, lx2 - 15, ly1 + 340], radius=6, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((lx1 + 25, ly1 + 220), "p-Node 2-D Mesh (sqrt(p) x sqrt(p))", fill=CRIMSON, font=font_bold)
    draw.text((lx1 + 25, ly1 + 248), "• Bisection Width B(Mesh) = sqrt(p)  (or 2*sqrt(p) for Torus)", fill=CRIMSON, font=font_math)
    draw.text((lx1 + 25, ly1 + 274), "• 2D cross-section limits physical bisection channels.", fill=TEXT_DARK, font=font_sm)
    draw.text((lx1 + 25, ly1 + 298), "• For p = 64 nodes: Bisection Width = only 8 links! (4x deficit)", fill=NAVY, font=font_bold)

    # Theoretical Bound Banner
    draw.rounded_rectangle([lx1 + 15, ly1 + 355, lx2 - 15, ly2 - 15], radius=6, fill=CARD_BG_BAD, outline=CARD_BORDER_BAD, width=1)
    draw.text(((lx1 + lx2) // 2, ly1 + 375), "Congestion Lower Bound: C >= B(Q_d) / B(Mesh)", fill=CRIMSON, font=font_bold, anchor="mm")
    draw.text(((lx1 + lx2) // 2, ly1 + 402), "C >= (p / 2) / (2 * sqrt(p)) = sqrt(p) / 4", fill=NAVY, font=font_math, anchor="mm")

    # Right Panel: Architectural Scaling & Physical Realization
    rx1, ry1, rx2, ry2 = 550, 80, 1100, 530
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)
    draw.text(((rx1 + rx2) // 2, ry1 + 22), "2. Numerical Scaling & Physical Wireability", fill=NAVY, font=font_head, anchor="mm")

    # Scaling Table
    table_x = [rx1 + 25, rx1 + 120, rx1 + 225, rx1 + 325, rx1 + 435]
    table_headers = ["Nodes p", "Cube B", "Mesh B", "Congestion C", "Dilation D"]
    for i, th in enumerate(table_headers):
        draw.text((table_x[i], ry1 + 52), th, fill=NAVY, font=get_font(15, bold=True))

    data = [
        ("16", "8", "4", "2", "3"),
        ("64", "32", "8", "4", "7"),
        ("256", "128", "16", "8", "15"),
        ("1,024", "512", "32", "16", "31"),
        ("4,096", "2,048", "64", "32", "63"),
        ("65,536", "32,768", "256", "128", "255")
    ]

    ty0 = ry1 + 78
    for r_idx, row in enumerate(data):
        ty = ty0 + r_idx * 30
        row_bg = (255, 255, 255) if r_idx % 2 == 0 else (241, 245, 249)
        draw.rounded_rectangle([rx1 + 15, ty, rx2 - 15, ty + 26], radius=4, fill=row_bg, outline=None)
        draw.text((table_x[0] + 5, ty + 4), row[0], fill=TEXT_DARK, font=font_sm)
        draw.text((table_x[1] + 10, ty + 4), row[1], fill=HIGHLIGHT_BLUE, font=font_sm)
        draw.text((table_x[2] + 10, ty + 4), row[2], fill=CRIMSON, font=font_sm)
        draw.text((table_x[3] + 20, ty + 4), row[3], fill=CRIMSON, font=font_bold)
        draw.text((table_x[4] + 20, ty + 4), row[4], fill=NAVY, font=font_bold)

    # Architectural Takeaway Box (adjusted padding so text fits perfectly inside)
    card_top = ry1 + 262
    draw.rounded_rectangle([rx1 + 15, card_top, rx2 - 15, ly2 - 15], radius=6, fill=(255, 255, 255), outline=BOX_BORDER, width=1)
    draw.text((rx1 + 25, card_top + 10), "Why Supercomputers Abandoned Physical Hypercubes:", fill=NAVY, font=font_bold)
    draw.text((rx1 + 25, card_top + 32), "• Physical Packaging: Chips, boards, and server racks are 3D.", fill=TEXT_DARK, font=font_sm)
    draw.text((rx1 + 25, card_top + 52), "• Wire Volume: Hypercube wiring density explodes as O(p log p).", fill=TEXT_DARK, font=font_sm)
    draw.text((rx1 + 25, card_top + 72), "• Congestion Collapse: Laying out a 64k-node hypercube on 2D mesh", fill=CRIMSON, font=font_sm)
    draw.text((rx1 + 38, card_top + 92), "forces 128 logical channels through each physical bisection link!", fill=CRIMSON, font=font_bold)
    draw.text((rx1 + 25, card_top + 114), "• Modern Consensus: Machines like Fugaku and TPU pods adopt 3D/6D Torus", fill=TEXT_DARK, font=font_sm)
    draw.text((rx1 + 38, card_top + 134), "or Dragonfly topologies optimized for physical wire limits.", fill=(21, 128, 61), font=font_bold)

    img.save("extracted_images/lec14_hypercube_into_mesh_bisection.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_hypercube_into_mesh_bisection.png")

# -------------------------------------------------------------
# 7a. lec14_routing_store_and_forward.png
# Detailed Store-and-Forward Routing timeline & buffer model (Large Fonts, Disjoint Columns)
# -------------------------------------------------------------
def create_routing_store_and_forward():
    W, H = 1140, 530
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(22, bold=True)
    font_bold = get_font(20, bold=True)
    font_sm = get_font(16, bold=False)
    font_mono = get_font(18, bold=True)
    font_badge = get_font(17, bold=True)
    font_sum_bold = get_font(18, bold=True)
    font_sum_sm = get_font(15, bold=False)
    font_link = get_font(16, bold=True)

    draw.text((W // 2, 26), "Store-and-Forward (SAF) Routing: Step-by-Step Packet Serialization", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Each intermediate router must receive and buffer the 100% complete packet before forwarding", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    lx1, ly1, lx2, ly2 = 35, 78, 1105, 505
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)

    # 4 Router columns on right half
    rx = [430, 620, 810, 1000]
    ry = 130

    for i in range(3):
        draw.line([(rx[i] + 30, ry), (rx[i+1] - 30, ry)], fill=(148, 163, 184), width=4)
        draw.text(((rx[i] + rx[i+1]) // 2, ry - 20), f"Link {i+1}", fill=TEXT_MUTED, font=font_link, anchor="mm")

    for i, x in enumerate(rx):
        draw.ellipse([x - 28, ry - 28, x + 28, ry + 28], fill=(241, 245, 249), outline=NAVY, width=2)
        draw.text((x, ry), f"R{i}", fill=NAVY, font=font_head, anchor="mm")
        for gy in range(ry + 34, 410, 8):
            draw.line([(x, gy), (x, gy + 4)], fill=(226, 232, 240), width=1)

    steps = [
        {
            "step": "Step 1 (t = 0 -> T_trans):",
            "desc1": "R0 transmits entire packet to R1.",
            "desc2": "R1 buffers all m words in local RAM.",
            "col": CRIMSON,
            "y": 210,
            "packet_link": 0,
            "buffer_link": 1,
            "buf_text": "R1 Buffers m words",
            "idle_links": [2]
        },
        {
            "step": "Step 2 (t = T_trans -> 2*T_trans):",
            "desc1": "R1 decodes header, sends to R2.",
            "desc2": "R2 buffers all m words in local RAM.",
            "col": (180, 83, 9),
            "y": 285,
            "packet_link": 1,
            "buffer_link": 2,
            "buf_text": "R2 Buffers m words",
            "idle_links": [0]
        },
        {
            "step": "Step 3 (t = 2*T_trans -> 3*T_trans):",
            "desc1": "R2 forwards entire packet to R3.",
            "desc2": "R3 (Destination) receives full payload.",
            "col": (21, 128, 61),
            "y": 360,
            "packet_link": 2,
            "buffer_link": None,
            "buf_text": None,
            "idle_links": [0, 1]
        }
    ]

    for s in steps:
        sy = s["y"]
        # Left column descriptions (x: 55..400)
        draw.text((lx1 + 25, sy - 20), s["step"], fill=s["col"], font=font_bold)
        draw.text((lx1 + 25, sy + 4), s["desc1"], fill=TEXT_DARK, font=font_sm)
        draw.text((lx1 + 25, sy + 26), s["desc2"], fill=TEXT_MUTED, font=font_sm)

        # 1. Active transmitting packet link
        pli = s["packet_link"]
        px_start = rx[pli] + 12
        px_end = rx[pli+1] - 12
        draw.rounded_rectangle([px_start, sy - 18, px_end, sy + 18], radius=6, fill=(254, 226, 226) if s["col"] == CRIMSON else ((254, 243, 199) if s["col"] == (180, 83, 9) else (220, 252, 231)), outline=s["col"], width=2)
        draw.text(((px_start + px_end) // 2, sy), "Full Packet (m)  ->", fill=s["col"], font=font_mono, anchor="mm")

        # 2. Buffer badge at receiving router (placed inside the next link's span, perfectly non-overlapping!)
        if s["buffer_link"] is not None:
            bli = s["buffer_link"]
            bx_start = rx[bli] + 10
            bx_end = rx[bli+1] - 10
            draw.rounded_rectangle([bx_start, sy - 18, bx_end, sy + 18], radius=6, fill=(254, 242, 242) if s["col"] == CRIMSON else (254, 252, 232), outline=s["col"], width=1)
            draw.text(((bx_start + bx_end) // 2, sy), s["buf_text"], fill=s["col"], font=font_badge, anchor="mm")
        elif s["step"].startswith("Step 3"):
            # Destination R3 received badge
            draw.rounded_rectangle([rx[3] + 8, sy - 18, rx[3] + 100, sy + 18], radius=6, fill=(220, 252, 231), outline=(21, 128, 61), width=2)
            draw.text((rx[3] + 54, sy), "Received!", fill=(21, 128, 61), font=font_badge, anchor="mm")

        # 3. Idle links
        for ili in s["idle_links"]:
            ix_start = rx[ili] + 12
            ix_end = rx[ili+1] - 12
            draw.line([(ix_start + 10, sy), (ix_end - 10, sy)], fill=(203, 213, 225), width=2)
            draw.text(((ix_start + ix_end) // 2, sy - 10), "Idle", fill=(148, 163, 184), font=get_font(16, bold=False), anchor="mm")

    # Bottom summary box
    by1, by2 = 425, 498
    draw.rounded_rectangle([lx1 + 15, by1, lx2 - 15, by2], radius=6, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((lx1 + 25, by1 + 10), "Latency Penalty: T_comm = t_s + l * (m * t_w + t_h) — Transmission time multiplies at EVERY hop!", fill=CRIMSON, font=font_sum_bold)
    draw.text((lx1 + 25, by1 + 36), "For l = 3 hops: total transfer takes 3 * (m * t_w). Huge memory footprint: each router needs >= m words buffer.", fill=TEXT_DARK, font=font_sum_sm)

    img.save("extracted_images/lec14_routing_store_and_forward.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_routing_store_and_forward.png")

# -------------------------------------------------------------
# 7b. lec14_routing_cut_through.png
# Detailed Virtual Cut-Through Routing pipeline & blocking (Large Fonts, Disjoint)
# -------------------------------------------------------------
def create_routing_cut_through():
    W, H = 1140, 530
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(22, bold=True)
    font_case = get_font(20, bold=True)
    font_sm = get_font(16, bold=False)
    font_flit = get_font(17, bold=True)
    font_sum_bold = get_font(18, bold=True)
    font_sum_sm = get_font(15, bold=False)
    font_link = get_font(16, bold=True)

    draw.text((W // 2, 26), "Virtual Cut-Through (VCT) Routing: Pipelined Streaming & Full-Packet Buffering", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Kermani & Kleinrock (1979): Header initiates immediate cut-through; entire packet absorbed if blocked", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    lx1, ly1, lx2, ly2 = 35, 78, 1105, 505
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)

    rx = [160, 420, 680, 940]
    ry = 130
    for i in range(3):
        draw.line([(rx[i] + 30, ry), (rx[i+1] - 30, ry)], fill=(148, 163, 184), width=4)
        draw.text(((rx[i] + rx[i+1]) // 2, ry - 20), f"Link {i+1}", fill=TEXT_MUTED, font=font_link, anchor="mm")

    for i, x in enumerate(rx):
        draw.ellipse([x - 28, ry - 28, x + 28, ry + 28], fill=(241, 245, 249), outline=NAVY, width=2)
        draw.text((x, ry), f"R{i}", fill=NAVY, font=font_head, anchor="mm")

    # Case A: Uncongested Cut-Through
    draw.text((lx1 + 25, 180), "Case A: Uncongested Path — Immediate Flit Streaming Across Links", fill=(21, 128, 61), font=font_case)
    draw.text((lx1 + 25, 210), "As soon as Header arrives and output link is free, flits stream directly through routers without buffering:", fill=TEXT_DARK, font=font_sm)

    vct_flits = [
        ("Tail", 180, (253, 224, 71), (113, 63, 18)),
        ("Body 2", 300, (250, 204, 21), (113, 63, 18)),
        ("Body 1", 420, (234, 179, 8), (113, 63, 18)),
        ("Head ->", 540, (202, 138, 4), (255, 255, 255))
    ]
    for lbl, fx, bg, fg in vct_flits:
        draw.rounded_rectangle([fx, 240, fx + 105, 280], radius=6, fill=bg, outline=(180, 83, 9), width=2)
        draw.text((fx + 52, 260), lbl, fill=fg, font=font_flit, anchor="mm")

    draw.text((680, 260), "Pipelined: T_comm = t_s + l * t_h + m * t_w", fill=NAVY, font=get_font(19, bold=True), anchor="lm")

    # Case B: Blocked Channel
    draw.text((lx1 + 25, 305), "Case B: Output Link Blocked at Router R2 (Contention / Busy Resource)", fill=CRIMSON, font=font_case)
    draw.text((lx1 + 25, 335), "Because Link 3 is occupied, R2 CANNOT cut through. R2 buffers the ENTIRE packet in local RAM:", fill=TEXT_DARK, font=font_sm)

    draw.rounded_rectangle([180, 365, 490, 410], radius=6, fill=(254, 226, 226), outline=CRIMSON, width=2)
    draw.text((335, 387), "Absorbed into R2 Buffer (m words)", fill=CRIMSON, font=font_flit, anchor="mm")

    draw.line([(510, 387), (565, 387)], fill=CRIMSON, width=3)
    draw.text((575, 387), "[Link 3 Blocked / Busy]", fill=CRIMSON, font=get_font(18, bold=True), anchor="lm")
    draw.text((820, 387), "(Links 1 & 2 Released!)", fill=(21, 128, 61), font=get_font(17, bold=True), anchor="lm")

    # Bottom summary box
    by1, by2 = 430, 495
    draw.rounded_rectangle([lx1 + 15, by1, lx2 - 15, by2], radius=6, fill=(254, 252, 232), outline=(254, 240, 138), width=1)
    draw.text((lx1 + 25, by1 + 10), "Key Trade-off: Fast pipelining when open, BUT routers still require full-packet buffers (m words)!", fill=(180, 83, 9), font=font_sum_bold)
    draw.text((lx1 + 25, by1 + 34), "Buffer capacity of m words per port limits scalability in dense on-chip Networks-on-Chip (NoCs).", fill=TEXT_MUTED, font=font_sum_sm)

    img.save("extracted_images/lec14_routing_cut_through.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_routing_cut_through.png")

# -------------------------------------------------------------
# 7c. lec14_routing_wormhole.png
# Detailed Wormhole Routing flit train & in-place stalling (Large Fonts, Disjoint)
# -------------------------------------------------------------
def create_routing_wormhole():
    W, H = 1140, 530
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_sub = get_font(17, bold=False)
    font_head = get_font(22, bold=True)
    font_case = get_font(20, bold=True)
    font_sm = get_font(16, bold=False)
    font_flit = get_font(17, bold=True)
    font_sum_bold = get_font(18, bold=True)
    font_sum_sm = get_font(15, bold=False)
    font_link = get_font(16, bold=True)

    draw.text((W // 2, 26), "Wormhole Routing: Flit-Level Flow Control & In-Place Link Stalling", fill=NAVY, font=font_title, anchor="mm")
    draw.text((W // 2, 54), "Dally & Seitz (1986): Packet decomposed into tiny flits; Header reserves path, Body streams, Tail releases", fill=TEXT_MUTED, font=font_sub, anchor="mm")

    lx1, ly1, lx2, ly2 = 35, 78, 1105, 505
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=BOX_BG, outline=BOX_BORDER, width=1)

    rx = [160, 420, 680, 940]
    ry = 130
    for i in range(3):
        draw.line([(rx[i] + 30, ry), (rx[i+1] - 30, ry)], fill=(148, 163, 184), width=4)
        draw.text(((rx[i] + rx[i+1]) // 2, ry - 20), f"Link {i+1}", fill=TEXT_MUTED, font=font_link, anchor="mm")

    for i, x in enumerate(rx):
        draw.ellipse([x - 28, ry - 28, x + 28, ry + 28], fill=(241, 245, 249), outline=NAVY, width=2)
        draw.text((x, ry), f"R{i}", fill=NAVY, font=font_head, anchor="mm")

    # Case A: Flit Train Propagation
    draw.text((lx1 + 25, 180), "1. Flit Decomposition & Active Pipelined Streaming (Unblocked)", fill=(21, 128, 61), font=font_case)
    draw.text((lx1 + 25, 210), "Packet = [Head Flit] (sets switch) + [Body Flits] (payload) + [Tail Flit] (releases channel). Tiny 1-flit buffers:", fill=TEXT_DARK, font=font_sm)

    wh_flits = [
        ("Tail Flit", 140, (220, 252, 231), (22, 101, 52)),
        ("Body Flit 2", 270, (187, 247, 208), (22, 101, 52)),
        ("Body Flit 1", 400, (134, 239, 172), (22, 101, 52)),
        ("Head Flit ->", 530, (34, 197, 94), (255, 255, 255))
    ]
    for lbl, fx, bg, fg in wh_flits:
        draw.rounded_rectangle([fx, 240, fx + 120, 280], radius=6, fill=bg, outline=(34, 197, 94), width=2)
        draw.text((fx + 60, 260), lbl, fill=fg, font=font_flit, anchor="mm")

    draw.text((680, 260), "Pipelined: T_comm = t_s + l * t_h + m * t_w", fill=(21, 128, 61), font=get_font(19, bold=True), anchor="lm")

    # Case B: Blocked State - The Frozen Worm
    draw.text((lx1 + 25, 305), "2. The Blocked State: Flits Freeze In-Place Across Multiple Intermediate Links!", fill=CRIMSON, font=font_case)
    draw.text((lx1 + 25, 335), "If Head Flit is blocked at Router R2, body flits stop immediately in their current flit buffers across links:", fill=TEXT_DARK, font=font_sm)

    frozen_flits = [
        ("Tail (at R0)", 110, (254, 226, 226), CRIMSON),
        ("Body 2 (Link 1)", 260, (254, 202, 202), CRIMSON),
        ("Body 1 (at R1)", 420, (254, 202, 202), CRIMSON),
        ("Head (Blocked R2)", 580, (220, 38, 38), (255, 255, 255))
    ]
    for lbl, fx, bg, fg in frozen_flits:
        draw.rounded_rectangle([fx, 365, fx + 150, 405], radius=6, fill=bg, outline=CRIMSON, width=2)
        draw.text((fx + 75, 385), lbl, fill=fg, font=get_font(15, bold=True), anchor="mm")

    draw.text((755, 385), "[HOLD] Wires stay held! (HOL blocking)", fill=CRIMSON, font=get_font(17, bold=True), anchor="lm")

    # Bottom summary box
    by1, by2 = 430, 495
    draw.rounded_rectangle([lx1 + 15, by1, lx2 - 15, by2], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.text((lx1 + 25, by1 + 10), "Key Advantage: Tiny buffer footprint per router (only 1-4 flits)! Enables dense multicore NoCs.", fill=(21, 128, 61), font=font_sum_bold)
    draw.text((lx1 + 25, by1 + 34), "Challenge: Stalled worms hold physical wires and cause deadlocks. Solution: Virtual Channels (VCs).", fill=TEXT_MUTED, font=font_sum_sm)

    img.save("extracted_images/lec14_routing_wormhole.png", dpi=(300, 300))
    print("Generated extracted_images/lec14_routing_wormhole.png")

if __name__ == '__main__':
    create_process_mapping_impact()
    create_graph_embedding_metrics()
    create_gray_code_hypercube()
    create_mesh_into_hypercube()
    create_mesh_linear_array_embedding()
    create_hypercube_into_mesh_bisection()
    create_routing_store_and_forward()
    create_routing_cut_through()
    create_routing_wormhole()
    print("All Lecture 14 diagrams generated successfully with elevated font sizes!")
