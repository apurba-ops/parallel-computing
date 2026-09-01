import os
import math
from PIL import Image, ImageDraw, ImageFont

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

def draw_arrow_curve(draw, start_pt, end_pt, color, width=4, curve_drop=0):
    x1, y1 = start_pt
    x2, y2 = end_pt
    
    if curve_drop == 0:
        # Straight horizontal arrow
        draw.line([x1, y1, x2, y2], fill=color, width=width)
        angle = 0.0
    else:
        # Smooth quadratic curve through control point below
        cx = (x1 + x2) / 2.0
        cy = max(y1, y2) + curve_drop
        
        num_pts = 60
        pts = []
        for i in range(num_pts + 1):
            t = i / float(num_pts)
            bx = (1 - t)**2 * x1 + 2 * (1 - t) * t * cx + t**2 * x2
            by = (1 - t)**2 * y1 + 2 * (1 - t) * t * cy + t**2 * y2
            pts.append((bx, by))
            
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=width)
            
        dx = x2 - cx
        dy = y2 - cy
        angle = math.atan2(dy, dx)
        
    # Draw sharp arrowhead
    arrow_len = 16
    arrow_angle = math.pi / 7.0
    p1 = (x2 - arrow_len * math.cos(angle - arrow_angle), y2 - arrow_len * math.sin(angle - arrow_angle))
    p2 = (x2 - arrow_len * math.cos(angle + arrow_angle), y2 - arrow_len * math.sin(angle + arrow_angle))
    
    draw.polygon([(x2, y2), p1, p2], fill=color)

def generate_perfect_slide17():
    SCALE = 3  # 3x supersampling for ultra crispness
    W = 1200 * SCALE
    H = 760 * SCALE
    
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_stage = get_font(25 * SCALE, bold=False)
    font_idx = get_font(23 * SCALE, bold=False)
    font_val = get_font(26 * SCALE, bold=False)
    
    # Palette matching academic textbook / slide illustration
    TEXT_BLACK = (20, 25, 35)
    LABEL_GRAY = (90, 100, 115)
    BOX_BORDER = (80, 90, 105)
    BOX_BG_VAL = (245, 247, 250)
    BOX_BG_PTR = (235, 238, 243)
    LINE_GRAY = (140, 150, 165)
    ARROW_COLOR = (45, 55, 72)
    SLASH_COLOR = (100, 110, 125)
    
    node_indices = [3, 4, 6, 1, 0, 5]
    num_nodes = len(node_indices)
    
    # Dimensions
    node_w = 96 * SCALE
    node_h = 58 * SCALE
    val_w = 54 * SCALE
    ptr_w = 42 * SCALE
    
    start_x = 175 * SCALE
    gap_x = 165 * SCALE
    node_x_coords = [start_x + i * gap_x for i in range(num_nodes)]
    
    # 4 rows corresponding to iterations (a), (b), (c), (d)
    rows_data = [
        ("(a)", [1, 1, 1, 1, 1, 0], 100 * SCALE, {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}, 0),
        ("(b)", [2, 2, 2, 2, 1, 0], 270 * SCALE, {0: 2, 1: 3, 2: 4, 3: 5}, 42 * SCALE),
        ("(c)", [4, 4, 3, 2, 1, 0], 450 * SCALE, {0: 4, 1: 5}, 58 * SCALE),
        ("(d)", [5, 4, 3, 2, 1, 0], 630 * SCALE, {}, 0)
    ]
    
    for row_label, vals, cy, pointer_targets, curve_base_depth in rows_data:
        # Row label on far left
        draw.text((70 * SCALE, cy), row_label, fill=LABEL_GRAY, font=font_stage, anchor="mm")
        
        for i, idx in enumerate(node_indices):
            nx = node_x_coords[i]
            val = vals[i]
            
            # Node ID above the cell
            draw.text((nx + node_w / 2, cy - node_h / 2 - 18 * SCALE), str(idx), fill=LABEL_GRAY, font=font_idx, anchor="mm")
            
            # Outer Box
            bx1, by1 = nx, cy - node_h / 2
            bx2, by2 = nx + node_w, cy + node_h / 2
            
            # Value cell (left)
            draw.rectangle([bx1, by1, bx1 + val_w, by2], fill=BOX_BG_VAL, outline=BOX_BORDER, width=2 * SCALE)
            draw.text((bx1 + val_w / 2, cy), str(val), fill=TEXT_BLACK, font=font_val, anchor="mm")
            
            # Pointer cell (right)
            draw.rectangle([bx1 + val_w, by1, bx2, by2], fill=BOX_BG_PTR, outline=BOX_BORDER, width=2 * SCALE)
            
            # Pointer logic
            if i in pointer_targets:
                target_node_idx = pointer_targets[i]
                target_x = node_x_coords[target_node_idx]
                
                start_pt = (bx1 + val_w + ptr_w / 2, cy)
                
                hop_dist = target_node_idx - i
                if hop_dist == 1:
                    # Straight horizontal arrow
                    end_pt = (target_x - 3 * SCALE, cy)
                    draw_arrow_curve(draw, start_pt, end_pt, ARROW_COLOR, width=2 * SCALE + 2, curve_drop=0)
                else:
                    # Curved arc below
                    # Start point slightly below center of pointer box
                    s_pt = (start_pt[0], cy + 10 * SCALE)
                    # End point at bottom-left of target box
                    e_pt = (target_x + 8 * SCALE, cy + node_h / 2 + 1 * SCALE)
                    
                    # Stagger depths so parallel arcs are cleanly separated
                    c_drop = curve_base_depth + (hop_dist - 2) * (18 * SCALE)
                    draw_arrow_curve(draw, s_pt, e_pt, ARROW_COLOR, width=2 * SCALE + 2, curve_drop=c_drop)
            else:
                # Slash in pointer box
                pad_x = 9 * SCALE
                pad_y = 7 * SCALE
                draw.line([bx1 + val_w + pad_x, by2 - pad_y, bx2 - pad_x, by1 + pad_y], fill=SLASH_COLOR, width=2 * SCALE + 1)
                
    # High-quality resize to target presentation dimensions
    final_img = img.resize((1200, 760), Image.Resampling.LANCZOS)
    final_img.save("extracted_images/lec11_list_ranking_diagram.png", dpi=(300, 300))
    print("Regenerated high-DPI slide 17 image successfully.")

if __name__ == "__main__":
    generate_perfect_slide17()
