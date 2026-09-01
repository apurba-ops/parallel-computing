import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('extracted_images', exist_ok=True)

# Colors
BG_COLOR = (255, 255, 255)
TEXT_DARK = (30, 41, 59)
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

# 1. lec11_multistage_schematic.png (Slide 2)
def create_multistage_schematic():
    W, H = 1000, 480
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(20, bold=True)
    font_body = get_font(16, bold=True)
    
    draw.text((100, 40), "Processors", fill=TEXT_DARK, font=font_title, anchor="mm")
    draw.text((500, 40), "Multistage interconnection network", fill=TEXT_DARK, font=font_title, anchor="mm")
    draw.text((900, 40), "Memory banks", fill=TEXT_DARK, font=font_title, anchor="mm")
    
    draw.rectangle([250, 80, 750, 420], outline=TEXT_MUTED, width=2)
    
    # Stage 1
    draw.rectangle([280, 100, 370, 400], fill=(241, 245, 249), outline=BOX_BORDER, width=2)
    draw.text((325, 250), "Stage 1", fill=TEXT_DARK, font=font_body, anchor="mm")
    
    # Stage 2
    draw.rectangle([410, 100, 500, 400], fill=(241, 245, 249), outline=BOX_BORDER, width=2)
    draw.text((455, 250), "Stage 2", fill=TEXT_DARK, font=font_body, anchor="mm")
    
    for x in [540, 570, 600]:
        draw.ellipse([x-3, 250-3, x+3, 250+3], fill=TEXT_DARK)
        
    # Stage n
    draw.rectangle([640, 100, 730, 400], fill=(241, 245, 249), outline=BOX_BORDER, width=2)
    draw.text((685, 250), "Stage n", fill=TEXT_DARK, font=font_body, anchor="mm")
    
    # Processors on left
    procs = [(130, "0"), (180, "1"), (360, "p-1")]
    for y, label in procs:
        draw.rectangle([70, y-18, 130, y+18], fill=BOX_BG, outline=BOX_BORDER, width=2)
        draw.text((100, y), label, fill=TEXT_DARK, font=font_body, anchor="mm")
        draw.line([130, y, 280, y], fill=LINE_COLOR, width=2)
        
    for y_dot in [250, 270, 290]:
        draw.ellipse([100-2, y_dot-2, 100+2, y_dot+2], fill=TEXT_MUTED)
        
    for y_link in [130, 160, 190, 340, 370]:
        draw.line([370, y_link, 410, y_link], fill=LINE_COLOR, width=2)
    for y_dot in [250, 270, 290]:
        draw.ellipse([390-2, y_dot-2, 390+2, y_dot+2], fill=TEXT_MUTED)
        
    for y_link in [130, 160, 190, 340, 370]:
        draw.line([600, y_link, 640, y_link], fill=LINE_COLOR, width=2)
        
    # Memory banks on right
    mems = [(130, "0"), (180, "1"), (360, "b-1")]
    for y, label in mems:
        draw.rectangle([870, y-18, 930, y+18], fill=BOX_BG, outline=BOX_BORDER, width=2)
        draw.text((900, y), label, fill=TEXT_DARK, font=font_body, anchor="mm")
        draw.line([730, y, 870, y], fill=LINE_COLOR, width=2)
        
    for y_dot in [250, 270, 290]:
        draw.ellipse([900-2, y_dot-2, 900+2, y_dot+2], fill=TEXT_MUTED)

    img.save("extracted_images/lec11_multistage_schematic.png", dpi=(300, 300))
    print("Saved lec11_multistage_schematic.png")

# 2. lec11_perfect_shuffle.png (Slide 4)
def create_perfect_shuffle():
    W, H = 900, 520
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_bold = get_font(17, bold=True)
    font_mono = get_font(16, bold=True)
    
    mapping = {
        0: (0, "000"),
        1: (2, "010"),
        2: (4, "100"),
        3: (6, "110"),
        4: (1, "001"),
        5: (3, "011"),
        6: (5, "101"),
        7: (7, "111")
    }
    
    y_start = 60
    y_gap = 50
    x_left = 340
    x_right = 540
    
    for i in range(8):
        y_in = y_start + i * y_gap
        bin_in = format(i, '03b')
        draw.text((x_left - 80, y_in), bin_in, fill=NAVY, font=font_mono, anchor="rm")
        draw.text((x_left - 30, y_in), str(i), fill=TEXT_DARK, font=font_bold, anchor="rm")
        
        out_idx, bin_out = mapping[i]
        y_out = y_start + out_idx * y_gap
        
        color = HIGHLIGHT_BLUE if i in [1, 2, 4] else (CRIMSON if i in [3, 5, 6] else LINE_COLOR)
        draw.line([x_left, y_in, x_right, y_out], fill=color, width=3)
        draw.ellipse([x_left-4, y_in-4, x_left+4, y_in+4], fill=color)
        draw.ellipse([x_right-4, y_out-4, x_right+4, y_out+4], fill=color)
        
    for j in range(8):
        y_out = y_start + j * y_gap
        bin_out = format(j, '03b')
        draw.text((x_right + 30, y_out), str(j), fill=TEXT_DARK, font=font_bold, anchor="lm")
        orig_i = [k for k, v in mapping.items() if v[0] == j][0]
        orig_bin = format(orig_i, '03b')
        draw.text((x_right + 70, y_out), f"{bin_out} = left_rotate({orig_bin})", fill=NAVY_LIGHT, font=font_mono, anchor="lm")
        
    img.save("extracted_images/lec11_perfect_shuffle.png", dpi=(300, 300))
    print("Saved lec11_perfect_shuffle.png")

# 3. lec11_switch_configurations.png (Slide 5)
def create_switch_configurations():
    W, H = 800, 360
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(18, bold=True)
    
    # (a) Pass-through
    cx1, cy1 = 220, 160
    draw.rectangle([cx1-50, cy1-60, cx1+50, cy1+60], fill=(248, 250, 252), outline=BOX_BORDER, width=3)
    y_t, y_b = cy1 - 30, cy1 + 30
    draw.line([cx1-90, y_t, cx1+90, y_t], fill=NAVY, width=4)
    draw.line([cx1-90, y_b, cx1+90, y_b], fill=NAVY, width=4)
    draw.text((cx1, 270), "(a) Pass-through", fill=TEXT_DARK, font=font_title, anchor="mm")
    
    # (b) Cross-over
    cx2, cy2 = 580, 160
    draw.rectangle([cx2-50, cy2-60, cx2+50, cy2+60], fill=(248, 250, 252), outline=BOX_BORDER, width=3)
    draw.line([cx2-90, y_t, cx2-50, y_t], fill=CRIMSON, width=4)
    draw.line([cx2-90, y_b, cx2-50, y_b], fill=CRIMSON, width=4)
    draw.line([cx2+50, y_t, cx2+90, y_t], fill=CRIMSON, width=4)
    draw.line([cx2+50, y_b, cx2+90, y_b], fill=CRIMSON, width=4)
    draw.line([cx2-50, y_t, cx2+50, y_b], fill=CRIMSON, width=4)
    draw.line([cx2-50, y_b, cx2+50, y_t], fill=CRIMSON, width=4)
    draw.text((cx2, 270), "(b) Cross-over", fill=TEXT_DARK, font=font_title, anchor="mm")
    
    img.save("extracted_images/lec11_switch_configurations.png", dpi=(300, 300))
    print("Saved lec11_switch_configurations.png")

# 4. lec11_omega_network_8x8.png (Slide 6)
def create_omega_network_8x8():
    W, H = 1000, 600
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_bold = get_font(15, bold=True)
    font_header = get_font(17, bold=True)
    
    shuffle = [0, 2, 4, 6, 1, 3, 5, 7]
    stages_x = [300, 520, 740]
    switch_w, switch_h = 60, 80
    switch_y = [100, 210, 320, 430]
    
    draw.text((120, 40), "Inputs", fill=TEXT_DARK, font=font_header, anchor="mm")
    draw.text((stages_x[0], 40), "Stage 0", fill=NAVY, font=font_header, anchor="mm")
    draw.text((stages_x[1], 40), "Stage 1", fill=NAVY, font=font_header, anchor="mm")
    draw.text((stages_x[2], 40), "Stage 2", fill=NAVY, font=font_header, anchor="mm")
    draw.text((900, 40), "Outputs", fill=TEXT_DARK, font=font_header, anchor="mm")
    
    input_y = []
    for k in range(4):
        input_y.append(switch_y[k] - 20)
        input_y.append(switch_y[k] + 20)
        
    for i in range(8):
        y_in = input_y[i]
        bin_i = format(i, '03b')
        draw.text((120, y_in), f"{bin_i} ({i})", fill=TEXT_DARK, font=font_bold, anchor="rm")
        
        dest_port = shuffle[i]
        dest_sw = dest_port // 2
        dest_is_lower = dest_port % 2
        y_dest = switch_y[dest_sw] + (20 if dest_is_lower else -20)
        
        draw.line([140, y_in, 180, y_in], fill=LINE_COLOR, width=2)
        draw.line([180, y_in, stages_x[0] - switch_w//2, y_dest], fill=LINE_COLOR, width=2)
        
    for s in range(3):
        sx = stages_x[s]
        for k in range(4):
            sy = switch_y[k]
            draw.rectangle([sx - switch_w//2, sy - switch_h//2, sx + switch_w//2, sy + switch_h//2],
                           fill=(241, 245, 249), outline=BOX_BORDER, width=2)
            draw.line([sx - 15, sy - 15, sx + 15, sy - 15], fill=TEXT_MUTED, width=1)
            draw.line([sx - 15, sy + 15, sx + 15, sy + 15], fill=TEXT_MUTED, width=1)
            
    for s_idx in range(2):
        for port in range(8):
            sw = port // 2
            is_lower = port % 2
            y_src = switch_y[sw] + (20 if is_lower else -20)
            x_src = stages_x[s_idx] + switch_w//2
            dest_port = shuffle[port]
            dest_sw = dest_port // 2
            dest_is_lower = dest_port % 2
            y_dest = switch_y[dest_sw] + (20 if dest_is_lower else -20)
            x_dest = stages_x[s_idx+1] - switch_w//2
            draw.line([x_src, y_src, x_src + 30, y_src], fill=LINE_COLOR, width=2)
            draw.line([x_src + 30, y_src, x_dest, y_dest], fill=LINE_COLOR, width=2)
        
    for i in range(8):
        sw = i // 2
        is_lower = i % 2
        y_out = switch_y[sw] + (20 if is_lower else -20)
        x_src = stages_x[2] + switch_w//2
        bin_i = format(i, '03b')
        draw.line([x_src, y_out, 860, y_out], fill=LINE_COLOR, width=2)
        draw.text((880, y_out), f"{bin_i} ({i})", fill=TEXT_DARK, font=font_bold, anchor="lm")
        
    img.save("extracted_images/lec11_omega_network_8x8.png", dpi=(300, 300))
    print("Saved lec11_omega_network_8x8.png")

# 5. lec11_omega_blocking.png (Slide 7)
def create_omega_blocking():
    W, H = 1000, 620
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_bold = get_font(15, bold=True)
    font_header = get_font(17, bold=True)
    font_ann = get_font(16, bold=True)
    
    shuffle = [0, 2, 4, 6, 1, 3, 5, 7]
    stages_x = [300, 520, 740]
    switch_w, switch_h = 60, 80
    switch_y = [100, 210, 320, 430]
    
    draw.text((120, 40), "Inputs", fill=TEXT_DARK, font=font_header, anchor="mm")
    draw.text((stages_x[0], 40), "Stage 0", fill=NAVY, font=font_header, anchor="mm")
    draw.text((stages_x[1], 40), "Stage 1", fill=NAVY, font=font_header, anchor="mm")
    draw.text((stages_x[2], 40), "Stage 2", fill=NAVY, font=font_header, anchor="mm")
    draw.text((900, 40), "Outputs", fill=TEXT_DARK, font=font_header, anchor="mm")
    
    input_y = []
    for k in range(4):
        input_y.append(switch_y[k] - 20)
        input_y.append(switch_y[k] + 20)
        
    for i in range(8):
        y_in = input_y[i]
        bin_i = format(i, '03b')
        draw.text((120, y_in), f"{bin_i}", fill=(148, 163, 184), font=font_bold, anchor="rm")
        dest_port = shuffle[i]
        dest_sw = dest_port // 2
        dest_is_lower = dest_port % 2
        y_dest = switch_y[dest_sw] + (20 if dest_is_lower else -20)
        draw.line([140, y_in, 180, y_in], fill=(226, 232, 240), width=2)
        draw.line([180, y_in, stages_x[0] - switch_w//2, y_dest], fill=(226, 232, 240), width=2)
        
    for s in range(3):
        sx = stages_x[s]
        for k in range(4):
            sy = switch_y[k]
            draw.rectangle([sx - switch_w//2, sy - switch_h//2, sx + switch_w//2, sy + switch_h//2],
                           fill=(248, 250, 252), outline=(203, 213, 225), width=2)
            
    for s_idx in range(2):
        for port in range(8):
            sw = port // 2
            is_lower = port % 2
            y_src = switch_y[sw] + (20 if is_lower else -20)
            x_src = stages_x[s_idx] + switch_w//2
            dest_port = shuffle[port]
            dest_sw = dest_port // 2
            dest_is_lower = dest_port % 2
            y_dest = switch_y[dest_sw] + (20 if dest_is_lower else -20)
            x_dest = stages_x[s_idx+1] - switch_w//2
            draw.line([x_src, y_src, x_src + 30, y_src], fill=(226, 232, 240), width=2)
            draw.line([x_src + 30, y_src, x_dest, y_dest], fill=(226, 232, 240), width=2)
            
    for i in range(8):
        sw = i // 2
        is_lower = i % 2
        y_out = switch_y[sw] + (20 if is_lower else -20)
        x_src = stages_x[2] + switch_w//2
        bin_i = format(i, '03b')
        draw.line([x_src, y_out, 860, y_out], fill=(226, 232, 240), width=2)
        draw.text((880, y_out), f"{bin_i}", fill=(148, 163, 184), font=font_bold, anchor="lm")

    # Path 1: 010 -> 111 (Blue)
    draw.text((120, input_y[2]), "010", fill=HIGHLIGHT_BLUE, font=font_bold, anchor="rm")
    draw.line([140, input_y[2], 180, input_y[2]], fill=HIGHLIGHT_BLUE, width=4)
    draw.line([180, input_y[2], stages_x[0]-switch_w//2, switch_y[2]-20], fill=HIGHLIGHT_BLUE, width=4)
    draw.line([stages_x[0]-switch_w//2, switch_y[2]-20, stages_x[0]+switch_w//2, switch_y[2]+20], fill=HIGHLIGHT_BLUE, width=4)
    
    # Path 2: 110 -> 100 (Orange)
    draw.text((120, input_y[6]), "110", fill=GOLD, font=font_bold, anchor="rm")
    draw.line([140, input_y[6], 180, input_y[6]], fill=GOLD, width=4)
    draw.line([180, input_y[6], stages_x[0]-switch_w//2, switch_y[2]+20], fill=GOLD, width=4)
    draw.line([stages_x[0]-switch_w//2, switch_y[2]+20, stages_x[0]+switch_w//2, switch_y[2]+20], fill=GOLD, width=4)
    
    # Collision Link A -> B
    draw.line([330, 340, 360, 340], fill=CRIMSON, width=5)
    draw.line([360, 340, 490, 230], fill=CRIMSON, width=5)
    
    draw.ellipse([330-6, 340-6, 330+6, 340+6], fill=CRIMSON)
    draw.text((315, 360), "A", fill=CRIMSON, font=font_ann, anchor="mm")
    
    draw.ellipse([490-6, 230-6, 490+6, 230+6], fill=CRIMSON)
    draw.text((475, 215), "B", fill=CRIMSON, font=font_ann, anchor="mm")
    
    # Box
    draw.rectangle([300, 530, 700, 590], fill=(254, 242, 242), outline=CRIMSON, width=2)
    draw.text((500, 560), "BLOCKING at Link AB: Both 010->111 and 110->100 require link AB!", fill=CRIMSON, font=font_bold, anchor="mm")
    
    img.save("extracted_images/lec11_omega_blocking.png", dpi=(300, 300))
    print("Saved lec11_omega_blocking.png")

# 6. lec11_prefix_sum_diagram.png (Slide 13)
def create_prefix_sum_diagram():
    W, H = 1000, 580
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_val = get_font(16, bold=True)
    font_lbl = get_font(15, bold=True)
    font_side = get_font(16, bold=True)
    
    stages_data = [
        ("Input Array (Initial)", [5, 20, 7, 13, 12, 25, 8, 16], 460),
        ("Iteration 1 (stride = 1)", [5, 25, 27, 20, 25, 37, 33, 24], 340),
        ("Iteration 2 (stride = 2)", [5, 25, 32, 45, 52, 57, 58, 61], 220),
        ("Iteration 3 (stride = 4, Final)", [5, 25, 32, 45, 57, 82, 90, 106], 100)
    ]
    
    box_w = 60
    box_h = 42
    start_x = 100
    gap_x = 65
    
    for stage_idx, (title, vals, y_pos) in enumerate(stages_data):
        draw.text((60, y_pos), f"k={3-stage_idx}" if stage_idx > 0 else "k=0", fill=NAVY, font=font_lbl, anchor="rm")
        
        for i, val in enumerate(vals):
            x = start_x + i * gap_x
            is_final_row = (stage_idx == 3)
            bg = (238, 242, 255) if is_final_row else BOX_BG
            border = HIGHLIGHT_BLUE if is_final_row else BOX_BORDER
            
            draw.rectangle([x, y_pos - box_h//2, x + box_w, y_pos + box_h//2], fill=bg, outline=border, width=2)
            draw.text((x + box_w//2, y_pos), str(val), fill=TEXT_DARK, font=font_val, anchor="mm")
            
    # Connect
    for i in range(8):
        x_dest = start_x + i * gap_x + box_w//2
        draw.line([x_dest, 460 - box_h//2, x_dest, 340 + box_h//2], fill=LINE_COLOR, width=2)
        if i >= 1:
            x_src = start_x + (i - 1) * gap_x + box_w//2
            draw.line([x_src, 460 - box_h//2, x_dest, 340 + box_h//2], fill=HIGHLIGHT_BLUE, width=2)
            
    for i in range(8):
        x_dest = start_x + i * gap_x + box_w//2
        draw.line([x_dest, 340 - box_h//2, x_dest, 220 + box_h//2], fill=LINE_COLOR, width=2)
        if i >= 2:
            x_src = start_x + (i - 2) * gap_x + box_w//2
            draw.line([x_src, 340 - box_h//2, x_dest, 220 + box_h//2], fill=HIGHLIGHT_BLUE, width=2)
            
    for i in range(8):
        x_dest = start_x + i * gap_x + box_w//2
        draw.line([x_dest, 220 - box_h//2, x_dest, 100 + box_h//2], fill=LINE_COLOR, width=2)
        if i >= 4:
            x_src = start_x + (i - 4) * gap_x + box_w//2
            draw.line([x_src, 220 - box_h//2, x_dest, 100 + box_h//2], fill=HIGHLIGHT_BLUE, width=2)

    draw.rectangle([660, 160, 960, 380], fill=(241, 245, 249), outline=NAVY, width=2)
    draw.text((810, 200), "CREW PRAM Algorithm", fill=NAVY, font=font_side, anchor="mm")
    draw.text((810, 250), "• Uses n/2 processors", fill=TEXT_DARK, font=font_lbl, anchor="mm")
    draw.text((810, 290), "• Time: O(log n) steps", fill=TEXT_DARK, font=font_lbl, anchor="mm")
    draw.text((810, 330), "• Stride doubles each round", fill=CRIMSON, font=font_lbl, anchor="mm")
    
    img.save("extracted_images/lec11_prefix_sum_diagram.png", dpi=(300, 300))
    print("Saved lec11_prefix_sum_diagram.png")

# 7. lec11_list_ranking_diagram.png (Slide 17)
def create_list_ranking_diagram():
    W, H = 1000, 600
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_bold = get_font(16, bold=True)
    font_sub = get_font(13)
    
    nodes = [
        {"idx": 3, "x": 160},
        {"idx": 4, "x": 300},
        {"idx": 6, "x": 440},
        {"idx": 1, "x": 580},
        {"idx": 0, "x": 720},
        {"idx": 5, "x": 860}
    ]
    
    stages = [
        ("(a) Initial State", [1, 1, 1, 1, 1, 0], 100, 1),
        ("(b) Iteration 1", [2, 2, 2, 2, 1, 0], 230, 2),
        ("(c) Iteration 2", [4, 4, 3, 2, 1, 0], 360, 4),
        ("(d) Iteration 3", [5, 4, 3, 2, 1, 0], 490, 8)
    ]
    
    box_w = 70
    box_h = 44
    
    for stage_idx, (title, dists, y_pos, stride) in enumerate(stages):
        draw.text((40, y_pos), title[:3], fill=NAVY, font=font_bold, anchor="lm")
        
        for i, node in enumerate(nodes):
            x = node["x"]
            if stage_idx == 0:
                draw.text((x + 20, y_pos - 32), f"Node {node['idx']}", fill=TEXT_MUTED, font=font_sub, anchor="mm")
                
            draw.rectangle([x, y_pos - box_h//2, x + 40, y_pos + box_h//2], fill=BOX_BG, outline=BOX_BORDER, width=2)
            draw.rectangle([x + 40, y_pos - box_h//2, x + 70, y_pos + box_h//2], fill=(241, 245, 249), outline=BOX_BORDER, width=2)
            
            draw.text((x + 20, y_pos), str(dists[i]), fill=TEXT_DARK, font=font_bold, anchor="mm")
            
            target_i = i + stride
            if target_i < len(nodes):
                target_x = nodes[target_i]["x"]
                if stride == 1:
                    draw.line([x + 55, y_pos, target_x, y_pos], fill=HIGHLIGHT_BLUE, width=2)
                    draw.polygon([(target_x, y_pos), (target_x - 6, y_pos - 4), (target_x - 6, y_pos + 4)], fill=HIGHLIGHT_BLUE)
                else:
                    arc_y = y_pos + 26
                    draw.line([x + 55, y_pos, x + 55, arc_y], fill=CRIMSON, width=2)
                    draw.line([x + 55, arc_y, target_x + 20, arc_y], fill=CRIMSON, width=2)
                    draw.line([target_x + 20, arc_y, target_x + 20, y_pos + box_h//2], fill=CRIMSON, width=2)
                    draw.polygon([(target_x + 20, y_pos + box_h//2), (target_x + 16, y_pos + box_h//2 + 6), (target_x + 24, y_pos + box_h//2 + 6)], fill=CRIMSON)
            else:
                draw.line([x + 44, y_pos + box_h//2 - 4, x + 66, y_pos - box_h//2 + 4], fill=TEXT_MUTED, width=2)
                
    img.save("extracted_images/lec11_list_ranking_diagram.png", dpi=(300, 300))
    print("Saved lec11_list_ranking_diagram.png")

if __name__ == "__main__":
    create_multistage_schematic()
    create_perfect_shuffle()
    create_switch_configurations()
    create_omega_network_8x8()
    create_omega_blocking()
    create_prefix_sum_diagram()
    create_list_ranking_diagram()
