import numpy as np
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    try:
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

def generate_randomized_block_cyclic_figure(output_path="extracted_images/lec19_randomized_block_cyclic.png"):
    W, H = 1280, 680
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
    font_axis = get_font(9, bold=True)
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
                # Nonzero cell: dark slate/navy
                draw.rectangle([cx, cy, cx + cs, cy + cs], fill=(71, 85, 105), outline=(148, 163, 184), width=1)
            else:
                # Zero cell: white
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
            
            # Label
            draw.text((cx + bs // 2, cy + bs // 2 - 9), f"P_{{{pid}}}", fill=txt_col, font=font_mono, anchor="mm")
            
            # Count label
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

    # Footnote citation inside card
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
                # Permuted nonzero cell: bright sky blue / azure
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

            # All processes are well-balanced (4 to 7 nonzeros)
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

    # Footnote citation inside card
    draw.text((x_right + 24, card_y + card_h - 24), "Citation: Grama, Gupta, Karypis, Kumar — Introduction to Parallel Computing (2nd Ed.), Fig. 3.33 (p. 130)", fill=(156, 163, 175), font=get_font(9.5, bold=False), anchor="lb")

    img.save(output_path, dpi=(150, 150))
    print(f"Successfully generated {output_path} ({W}x{H})")

if __name__ == "__main__":
    generate_randomized_block_cyclic_figure()
