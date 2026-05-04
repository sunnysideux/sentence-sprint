from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT / "app/src/main/java/com/sunnyapps/sentencebuilder/data/SentenceRepository.kt"
APP_IMAGE_DIR = ROOT / "app/src/main/res/drawable-nodpi"
PILOT_DIR = ROOT / "image_pilot"
RESOURCE_MAP = ROOT / "app/src/main/java/com/sunnyapps/sentencebuilder/ui/components/SentenceImageResources.kt"

PILOT_IDS = [
    "l1_01",
    "l1_03",
    "l1_04",
    "l1_06",
    "l1_08",
    "l2_01",
    "l3_01",
    "l4_09",
    "l5_03",
    "l5_10",
]

BATCH_IDS = {
    "01": ["l1_02", "l1_05", "l1_07", "l1_09", "l1_10", "l1_11", "l1_12", "l1_13", "l1_14", "l1_15"],
    "02": ["l1_16", "l1_17", "l1_18", "l1_19", "l1_20", "l1_21", "l1_22", "l1_23", "l1_24", "l1_25"],
    "03": ["l1_26", "l1_27", "l1_28", "l1_29", "l1_30", "l2_02", "l2_03", "l2_04", "l2_05", "l2_06"],
    "04": ["l2_07", "l2_08", "l2_09", "l2_10", "l2_11", "l2_12", "l2_13", "l2_14", "l2_15", "l2_16"],
    "05": ["l2_17", "l2_18", "l2_19", "l2_20", "l2_21", "l2_22", "l2_23", "l2_24", "l2_25", "l2_26"],
    "06": ["l2_27", "l2_28", "l2_29", "l2_30", "l3_02", "l3_03", "l3_04", "l3_05", "l3_06", "l3_07"],
    "07": ["l3_08", "l3_09", "l3_10", "l3_11", "l3_12", "l3_13", "l3_14", "l3_15", "l3_16", "l3_17"],
    "08": ["l3_18", "l3_19", "l3_20", "l3_21", "l3_22", "l3_23", "l3_24", "l3_25", "l3_26", "l3_27"],
    "09": ["l3_28", "l3_29", "l3_30", "l4_01", "l4_02", "l4_03", "l4_04", "l4_05", "l4_06", "l4_07"],
    "10": ["l4_08", "l4_10", "l4_11", "l4_12", "l4_13", "l4_14", "l4_15", "l4_16", "l4_17", "l4_18"],
    "11": ["l4_19", "l4_20", "l4_21", "l4_22", "l4_23", "l4_24", "l4_25", "l4_26", "l4_27", "l4_28"],
    "12": ["l4_29", "l4_30", "l5_01", "l5_02", "l5_04", "l5_05", "l5_06", "l5_07", "l5_08", "l5_09"],
    "13": ["l5_11", "l5_12", "l5_13", "l5_14", "l5_15", "l5_16", "l5_17", "l5_18", "l5_19", "l5_20"],
    "14": ["l5_21", "l5_22", "l5_23", "l5_24", "l5_25", "l5_26", "l5_27", "l5_28", "l5_29", "l5_30"],
}

CANVAS_SIZE = (1024, 576)
SAFE_COLORS = ["#f35b5b", "#3f8efc", "#2fb36d", "#ffbf3f", "#9b72e8", "#ff8c42"]


def sentence_ids() -> list[str]:
    text = REPOSITORY.read_text(encoding="utf-8")
    ids = re.findall(r'item\("(l\d+_\d+)"', text)
    if len(ids) != 150:
        raise SystemExit(f"Expected 150 sentence ids, found {len(ids)}")
    return ids


def sentence_lookup() -> dict[str, str]:
    text = REPOSITORY.read_text(encoding="utf-8")
    pairs = re.findall(r'item\("(l\d+_\d+)",\s*\d+,\s*"[^"]+",\s*"([^"]+)"', text)
    return dict(pairs)


def crayon_line(draw: ImageDraw.ImageDraw, points, fill: str, width: int = 5) -> None:
    draw.line(points, fill=fill, width=width, joint="curve")
    if width > 2:
        draw.line([(x + 1, y - 1) for x, y in points], fill=fill, width=max(1, width // 3))


def ellipse(draw: ImageDraw.ImageDraw, box, fill: str, outline: str = "#26334d", width: int = 4) -> None:
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def rounded(draw: ImageDraw.ImageDraw, box, radius: int, fill: str, outline: str = "#26334d", width: int = 4) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def add_crayon_texture(image: Image.Image, seed: int) -> Image.Image:
    draw = ImageDraw.Draw(image, "RGBA")
    for i in range(260):
        x = (seed * 17 + i * 37) % CANVAS_SIZE[0]
        y = (seed * 31 + i * 19) % CANVAS_SIZE[1]
        length = 18 + ((seed + i) % 42)
        color = (255, 255, 255, 18) if i % 2 else (60, 70, 90, 11)
        draw.line((x, y, x + length, y - length // 3), fill=color, width=2)
    return image.filter(ImageFilter.SMOOTH_MORE)


def base_scene(seed: int, outdoors: bool = False, night: bool = False) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", CANVAS_SIZE, "#fdf3d0" if not night else "#1d2b5f")
    draw = ImageDraw.Draw(image)
    if night:
        draw.rectangle((0, 0, 1024, 576), fill="#1d2b5f")
        for i in range(22):
            x = (seed * 23 + i * 43) % 960 + 20
            y = (seed * 29 + i * 31) % 220 + 20
            ellipse(draw, (x, y, x + 7, y + 7), "#ffe77a", "#ffe77a", 1)
    elif outdoors:
        draw.rectangle((0, 0, 1024, 340), fill="#cfefff")
        draw.rectangle((0, 340, 1024, 576), fill="#a9df83")
        ellipse(draw, (72, 42, 168, 138), "#ffd257", "#f5a524", 4)
        for cx in (720, 790, 860):
            ellipse(draw, (cx - 58, 70, cx + 58, 128), "#ffffff", "#d9e6ef", 3)
    else:
        draw.rectangle((0, 0, 1024, 576), fill="#fff0bd")
        draw.rectangle((0, 370, 1024, 576), fill="#ffd78d")
        rounded(draw, (60, 70, 220, 190), 10, "#b7e3ff", "#6ea9c8", 4)
        crayon_line(draw, [(70, 184), (210, 184)], "#6ea9c8", 4)
    return image, draw


def draw_person(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, shirt: str = "#3f8efc", adult: bool = False) -> None:
    skin = "#b9794f"
    head_r = int(42 * scale)
    body_h = int((128 if adult else 112) * scale)
    ellipse(draw, (x - head_r, y - body_h - head_r * 2, x + head_r, y - body_h), skin, "#26334d", 4)
    ellipse(draw, (x - 14 * scale, y - body_h - 52 * scale, x - 4 * scale, y - body_h - 42 * scale), "#26334d", "#26334d", 1)
    ellipse(draw, (x + 18 * scale, y - body_h - 52 * scale, x + 28 * scale, y - body_h - 42 * scale), "#26334d", "#26334d", 1)
    draw.arc((x - 18 * scale, y - body_h - 42 * scale, x + 28 * scale, y - body_h - 18 * scale), 0, 170, fill="#26334d", width=max(3, int(4 * scale)))
    draw.pieslice((x - head_r, y - body_h - head_r * 2 - 6 * scale, x + head_r, y - body_h - 24 * scale), 180, 360, fill="#2a1d18")
    rounded(draw, (x - 44 * scale, y - body_h, x + 44 * scale, y - 28 * scale), int(22 * scale), shirt, "#26334d", 4)
    crayon_line(draw, [(x - 28 * scale, y - 26 * scale), (x - 44 * scale, y + 50 * scale)], "#26334d", int(7 * scale))
    crayon_line(draw, [(x + 28 * scale, y - 26 * scale), (x + 44 * scale, y + 50 * scale)], "#26334d", int(7 * scale))


def draw_table(draw: ImageDraw.ImageDraw, x: int, y: int, w: int = 340, h: int = 40) -> None:
    rounded(draw, (x, y, x + w, y + h), 14, "#c98245", "#26334d", 4)
    crayon_line(draw, [(x + 40, y + h), (x + 18, y + 150)], "#7d4b2a", 10)
    crayon_line(draw, [(x + w - 40, y + h), (x + w - 18, y + 150)], "#7d4b2a", 10)


def draw_book(draw: ImageDraw.ImageDraw, x: int, y: int, color: str = "#3f8efc") -> None:
    rounded(draw, (x - 90, y - 34, x + 90, y + 34), 12, color, "#26334d", 4)
    crayon_line(draw, [(x, y - 30), (x, y + 30)], "#ffffff", 4)
    ellipse(draw, (x - 40, y - 16, x + 40, y + 16), "#8bdc7c", "#ffffff", 3)


def draw_plate_food(draw: ImageDraw.ImageDraw, x: int, y: int, food: str = "cake") -> None:
    ellipse(draw, (x - 90, y - 34, x + 90, y + 34), "#ffffff", "#26334d", 4)
    if food == "cake":
        rounded(draw, (x - 50, y - 62, x + 50, y + 8), 10, "#8b4b32", "#26334d", 4)
        rounded(draw, (x - 50, y - 62, x + 50, y - 42), 6, "#fff2d0", "#fff2d0", 1)
    else:
        ellipse(draw, (x - 50, y - 36, x + 50, y + 26), "#f7c56b", "#b36a2e", 4)


def draw_bag(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    rounded(draw, (x - 86, y - 108, x + 92, y + 72), 28, "#35a56d", "#26334d", 5)
    rounded(draw, (x - 40, y - 140, x + 40, y - 92), 22, "#2a7a52", "#26334d", 5)
    rounded(draw, (x - 58, y - 72, x + 62, y + 36), 22, "#3f8efc", "#26334d", 4)


def draw_sink(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    rounded(draw, (x - 175, y - 28, x + 175, y + 62), 30, "#d7edf6", "#26334d", 5)
    crayon_line(draw, [(x, y - 96), (x, y - 30)], "#6a7b8f", 12)
    crayon_line(draw, [(x, y - 96), (x + 56, y - 96)], "#6a7b8f", 12)
    for i in range(7):
        crayon_line(draw, [(x + 44 + i * 5, y - 82), (x + 35 + i * 8, y + 18)], "#4fb6ff", 4)
    for i in range(12):
        bx = x - 95 + i * 18
        by = y - 20 + (i % 3) * 15
        ellipse(draw, (bx, by, bx + 18, by + 18), "#ffffff", "#80cfff", 2)


def draw_animal(draw: ImageDraw.ImageDraw, kind: str, x: int, y: int, scale: float = 1.0) -> None:
    colors = {
        "cat": "#f08a35", "dog": "#c47a3d", "cow": "#f8f7f0", "monkey": "#9b6138",
        "bird": "#3f8efc", "fish": "#36b6b0", "rabbit": "#ffffff", "frog": "#67bb5b"
    }
    fill = colors.get(kind, "#f08a35")
    if kind == "bird":
        ellipse(draw, (x - 72 * scale, y - 42 * scale, x + 72 * scale, y + 42 * scale), fill, "#26334d", 4)
        draw.polygon([(x + 70 * scale, y - 10 * scale), (x + 112 * scale, y + 8 * scale), (x + 70 * scale, y + 26 * scale)], fill="#ffbf3f", outline="#26334d")
        ellipse(draw, (x + 28 * scale, y - 28 * scale, x + 42 * scale, y - 14 * scale), "#26334d", "#26334d", 1)
        return
    if kind == "fish":
        ellipse(draw, (x - 88 * scale, y - 50 * scale, x + 88 * scale, y + 50 * scale), fill, "#26334d", 4)
        draw.polygon([(x - 90 * scale, y), (x - 148 * scale, y - 55 * scale), (x - 148 * scale, y + 55 * scale)], fill="#ff8c42", outline="#26334d")
        ellipse(draw, (x + 34 * scale, y - 18 * scale, x + 50 * scale, y - 2 * scale), "#26334d", "#26334d", 1)
        return
    ellipse(draw, (x - 105 * scale, y - 48 * scale, x + 75 * scale, y + 58 * scale), fill, "#26334d", 5)
    ellipse(draw, (x + 48 * scale, y - 92 * scale, x + 138 * scale, y - 10 * scale), fill, "#26334d", 5)
    if kind in {"cat", "rabbit"}:
        draw.polygon([(x + 58 * scale, y - 84 * scale), (x + 78 * scale, y - 134 * scale), (x + 98 * scale, y - 82 * scale)], fill=fill, outline="#26334d")
        draw.polygon([(x + 100 * scale, y - 82 * scale), (x + 130 * scale, y - 130 * scale), (x + 128 * scale, y - 72 * scale)], fill=fill, outline="#26334d")
    ellipse(draw, (x + 86 * scale, y - 64 * scale, x + 100 * scale, y - 50 * scale), "#26334d", "#26334d", 1)
    crayon_line(draw, [(x - 72 * scale, y + 44 * scale), (x - 72 * scale, y + 112 * scale)], "#26334d", int(8 * scale))
    crayon_line(draw, [(x + 20 * scale, y + 44 * scale), (x + 20 * scale, y + 112 * scale)], "#26334d", int(8 * scale))
    draw.arc((x - 145 * scale, y - 70 * scale, x - 50 * scale, y + 30 * scale), 210, 350, fill="#26334d", width=max(4, int(8 * scale)))
    if kind == "cow":
        ellipse(draw, (x - 40 * scale, y - 20 * scale, x - 5 * scale, y + 14 * scale), "#26334d", "#26334d", 1)
        ellipse(draw, (x + 20 * scale, y + 6 * scale, x + 58 * scale, y + 42 * scale), "#26334d", "#26334d", 1)


def draw_tree(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    rounded(draw, (x - 36, y - 190, x + 36, y + 110), 18, "#8a552e", "#26334d", 4)
    for cx, cy, r in [(x - 70, y - 230, 78), (x, y - 270, 90), (x + 80, y - 222, 78)]:
        ellipse(draw, (cx - r, cy - r, cx + r, cy + r), "#42b365", "#267746", 4)


def draw_ball(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    ellipse(draw, (x - 60, y - 60, x + 60, y + 60), "#ffffff", "#26334d", 5)
    crayon_line(draw, [(x - 45, y), (x + 45, y)], "#26334d", 4)
    crayon_line(draw, [(x, y - 45), (x, y + 45)], "#26334d", 4)


def draw_chess(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    size = 176
    rounded(draw, (x - size // 2, y - size // 2, x + size // 2, y + size // 2), 12, "#ffffff", "#26334d", 5)
    cell = size // 4
    for row in range(4):
        for col in range(4):
            if (row + col) % 2 == 0:
                draw.rectangle((x - size // 2 + col * cell, y - size // 2 + row * cell, x - size // 2 + (col + 1) * cell, y - size // 2 + (row + 1) * cell), fill="#26334d")
    for px, py, color in [(-42, -18, "#f35b5b"), (42, 28, "#3f8efc"), (12, -58, "#ffbf3f")]:
        ellipse(draw, (x + px - 15, y + py - 15, x + px + 15, y + py + 15), color, "#26334d", 3)


def draw_flower_patch(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    for i, color in enumerate(SAFE_COLORS[:5]):
        stem_x = x + i * 42
        crayon_line(draw, [(stem_x, y + 85), (stem_x + 8, y + 12)], "#2fb36d", 5)
        ellipse(draw, (stem_x - 18, y - 8, stem_x + 24, y + 34), color, "#26334d", 3)
        ellipse(draw, (stem_x - 6, y + 4, stem_x + 12, y + 22), "#ffdf5d", "#26334d", 2)


def draw_lamp(draw: ImageDraw.ImageDraw, x: int, y: int, glowing: bool = True) -> None:
    if glowing:
        ellipse(draw, (x - 120, y - 130, x + 120, y + 110), "#fff0a0", "#fff0a0", 1)
    rounded(draw, (x - 50, y - 100, x + 50, y - 20), 15, "#ffbf3f", "#26334d", 5)
    crayon_line(draw, [(x, y - 20), (x, y + 70)], "#26334d", 9)
    crayon_line(draw, [(x - 70, y + 70), (x + 70, y + 70)], "#26334d", 9)


def draw_clock_face(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    ellipse(draw, (x - 96, y - 96, x + 96, y + 96), "#ffffff", "#26334d", 6)
    crayon_line(draw, [(x, y), (x, y - 58)], "#26334d", 6)
    crayon_line(draw, [(x, y), (x + 50, y + 24)], "#26334d", 6)
    for i in range(3):
        draw.arc((x - 150 - i * 20, y - 145 - i * 15, x + 150 + i * 20, y + 145 + i * 15), 315, 45, fill="#f35b5b", width=4)


def draw_house(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    rounded(draw, (x - 95, y - 55, x + 95, y + 90), 12, "#ffdf8b", "#26334d", 5)
    draw.polygon([(x - 120, y - 55), (x, y - 150), (x + 120, y - 55)], fill="#f35b5b", outline="#26334d")
    rounded(draw, (x - 25, y + 10, x + 25, y + 90), 8, "#8a552e", "#26334d", 4)
    rounded(draw, (x + 40, y - 25, x + 82, y + 20), 5, "#b7e3ff", "#26334d", 3)


def draw_bed(draw: ImageDraw.ImageDraw, x: int, y: int, with_person: bool = False) -> None:
    rounded(draw, (x - 190, y - 80, x + 190, y + 70), 24, "#80b7ff", "#26334d", 5)
    rounded(draw, (x - 170, y - 118, x - 55, y - 55), 18, "#ffffff", "#26334d", 4)
    crayon_line(draw, [(x - 185, y + 72), (x - 185, y + 125)], "#26334d", 9)
    crayon_line(draw, [(x + 185, y + 72), (x + 185, y + 125)], "#26334d", 9)
    if with_person:
        ellipse(draw, (x - 130, y - 145, x - 55, y - 70), "#b9794f", "#26334d", 4)
        draw.arc((x - 112, y - 102, x - 73, y - 75), 0, 180, fill="#26334d", width=4)


def draw_door(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    rounded(draw, (x - 75, y - 180, x + 75, y + 90), 16, "#a9683c", "#26334d", 5)
    ellipse(draw, (x + 38, y - 35, x + 56, y - 17), "#ffcf33", "#26334d", 2)


def draw_school(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    rounded(draw, (x - 170, y - 90, x + 170, y + 100), 12, "#ffd78d", "#26334d", 5)
    draw.polygon([(x - 200, y - 90), (x, y - 200), (x + 200, y - 90)], fill="#f35b5b", outline="#26334d")
    rounded(draw, (x - 30, y + 5, x + 30, y + 100), 8, "#8a552e", "#26334d", 4)
    for wx in (-110, 80):
        rounded(draw, (x + wx, y - 45, x + wx + 55, y + 10), 6, "#b7e3ff", "#26334d", 3)


def draw_simple_item(draw: ImageDraw.ImageDraw, kind: str, x: int, y: int) -> None:
    if kind == "bell":
        ellipse(draw, (x - 65, y - 75, x + 65, y + 55), "#ffbf3f", "#26334d", 5)
        ellipse(draw, (x - 20, y + 45, x + 20, y + 85), "#f35b5b", "#26334d", 4)
        for i in range(3):
            draw.arc((x - 120 - i * 25, y - 95, x + 120 + i * 25, y + 95), 320, 40, fill="#26334d", width=5)
    elif kind == "gate":
        for gx in (-70, 0, 70):
            crayon_line(draw, [(x + gx, y - 150), (x + gx, y + 90)], "#8a552e", 12)
        crayon_line(draw, [(x - 110, y - 55), (x + 110, y - 55)], "#8a552e", 10)
        crayon_line(draw, [(x - 110, y + 40), (x + 110, y + 40)], "#8a552e", 10)
    elif kind == "shoes":
        rounded(draw, (x - 120, y - 35, x - 15, y + 35), 24, "#3f8efc", "#26334d", 5)
        rounded(draw, (x + 15, y - 35, x + 120, y + 35), 24, "#3f8efc", "#26334d", 5)
    elif kind == "shelf":
        for row in range(3):
            crayon_line(draw, [(x - 130, y - 90 + row * 70), (x + 130, y - 90 + row * 70)], "#8a552e", 10)
            for col, color in enumerate(SAFE_COLORS[:4]):
                rounded(draw, (x - 110 + col * 55, y - 145 + row * 70, x - 70 + col * 55, y - 92 + row * 70), 5, color, "#26334d", 2)
    elif kind == "thermometer":
        rounded(draw, (x - 22, y - 150, x + 22, y + 70), 20, "#ffffff", "#26334d", 5)
        ellipse(draw, (x - 48, y + 44, x + 48, y + 140), "#f35b5b", "#26334d", 5)
        crayon_line(draw, [(x, y + 60), (x, y - 95)], "#f35b5b", 14)
    elif kind == "crayons":
        for i, color in enumerate(SAFE_COLORS):
            crayon_line(draw, [(x - 100 + i * 38, y + 70), (x - 78 + i * 38, y - 90)], color, 18)
    elif kind == "vegetables":
        for i, color in enumerate(["#2fb36d", "#ff8c42", "#f35b5b", "#9b72e8"]):
            ellipse(draw, (x - 100 + i * 58, y - 25, x - 45 + i * 58, y + 35), color, "#26334d", 4)
    elif kind == "money":
        for i in range(4):
            rounded(draw, (x - 130 + i * 45, y - 35 - i * 12, x - 20 + i * 45, y + 35 - i * 12), 8, "#7edc8b", "#26334d", 3)
            ellipse(draw, (x - 92 + i * 45, y - 13 - i * 12, x - 58 + i * 45, y + 21 - i * 12), "#e9ffd8", "#26334d", 2)
def draw_vehicle(draw: ImageDraw.ImageDraw, x: int, y: int, kind: str = "car") -> None:
    body = "#3f8efc" if kind != "bus" else "#ffbf3f"
    rounded(draw, (x - 160, y - 82, x + 160, y + 42), 30, body, "#26334d", 5)
    rounded(draw, (x - 80, y - 150, x + 90, y - 70), 28, "#b7e3ff", "#26334d", 5)
    ellipse(draw, (x - 110, y + 18, x - 50, y + 78), "#26334d", "#26334d", 1)
    ellipse(draw, (x + 54, y + 18, x + 114, y + 78), "#26334d", "#26334d", 1)


def draw_water_or_cloud(draw: ImageDraw.ImageDraw, x: int, y: int, kind: str) -> None:
    if kind in {"cloud", "clouds", "air"}:
        for dx in (-70, -20, 35, 88):
            ellipse(draw, (x + dx - 50, y - 32, x + dx + 50, y + 32), "#ffffff", "#d8e7f2", 4)
    elif kind == "rain":
        draw_water_or_cloud(draw, x, y - 80, "cloud")
        for i in range(10):
            crayon_line(draw, [(x - 130 + i * 28, y - 25), (x - 145 + i * 28, y + 35)], "#3f8efc", 5)
    else:
        for i in range(4):
            draw.arc((x - 170 + i * 80, y - 30, x - 70 + i * 80, y + 45), 0, 180, fill="#3f8efc", width=8)


def draw_science(draw: ImageDraw.ImageDraw, sentence: str) -> bool:
    lower = sentence.lower()
    if "earth moves around the sun" in lower:
        draw.rectangle((0, 0, 1024, 576), fill="#1d2b5f")
        ellipse(draw, (410, 170, 610, 370), "#ffcf33", "#f29b25", 8)
        ellipse(draw, (210, 330, 300, 420), "#3f8efc", "#26334d", 5)
        draw.arc((160, 90, 860, 500), 15, 340, fill="#ffffff", width=5)
        draw.polygon([(800, 174), (846, 184), (810, 214)], fill="#ffffff")
        return True
    if "heart pumps blood" in lower:
        ellipse(draw, (310, 155, 515, 360), "#f35b5b", "#26334d", 6)
        ellipse(draw, (470, 155, 675, 360), "#f35b5b", "#26334d", 6)
        draw.polygon([(280, 240), (705, 240), (500, 500)], fill="#f35b5b", outline="#26334d")
        for y, color in [(180, "#3f8efc"), (310, "#f35b5b")]:
            crayon_line(draw, [(90, y), (310, y), (500, 270), (850, y)], color, 14)
            draw.polygon([(850, y), (815, y - 20), (815, y + 20)], fill=color)
        return True
    if "plants need sunlight" in lower or "leaves make food" in lower or "seeds grow" in lower or "roots take water" in lower:
        draw_tree(draw, 500, 360)
        ellipse(draw, (80, 50, 200, 170), "#ffd257", "#f5a524", 5)
        for i in range(7):
            crayon_line(draw, [(180, 140 + i * 18), (390, 250 + i * 4)], "#ffd257", 4)
        draw_water_or_cloud(draw, 250, 430, "water")
        return True
    if "water changes into vapor" in lower or "ice melts" in lower:
        draw_water_or_cloud(draw, 350, 425, "water")
        ellipse(draw, (680, 320, 820, 460), "#cdefff", "#26334d", 5)
        for i in range(4):
            draw.arc((560 + i * 50, 120, 700 + i * 50, 300), 100, 260, fill="#7aa6bf", width=6)
        return True
    if "magnets attract" in lower:
        draw.arc((300, 170, 600, 470), 35, 325, fill="#f35b5b", width=50)
        rounded(draw, (690, 270, 780, 340), 12, "#9aa5b4", "#26334d", 5)
        rounded(draw, (800, 220, 890, 290), 12, "#9aa5b4", "#26334d", 5)
        for x in (620, 660):
            crayon_line(draw, [(x, 280), (700, 300)], "#26334d", 4)
        return True
    if "lungs" in lower:
        crayon_line(draw, [(512, 110), (512, 420)], "#6a7b8f", 14)
        ellipse(draw, (310, 195, 500, 445), "#ff9f9f", "#26334d", 6)
        ellipse(draw, (524, 195, 714, 445), "#ff9f9f", "#26334d", 6)
        for x in (405, 620):
            draw.arc((x - 60, 250, x + 60, 365), 200, 340, fill="#3f8efc", width=8)
        return True
    if "brain" in lower:
        for cx, cy in [(430, 250), (500, 210), (575, 250), (470, 320), (555, 325)]:
            ellipse(draw, (cx - 70, cy - 55, cx + 70, cy + 55), "#f8a6c2", "#26334d", 5)
        draw_person(draw, 180, 470, 0.8, "#3f8efc")
        return True
    if "rain comes" in lower:
        draw_water_or_cloud(draw, 520, 210, "rain")
        return True
    if "electricity" in lower or "light a bulb" in lower:
        ellipse(draw, (430, 145, 590, 305), "#ffe66d", "#26334d", 6)
        rounded(draw, (465, 300, 555, 380), 12, "#9aa5b4", "#26334d", 5)
        for i in range(8):
            crayon_line(draw, [(512, 220), (512 + (i - 4) * 65, 80 + (i % 3) * 45)], "#ffcf33", 6)
        return True
    if "shadow" in lower:
        ellipse(draw, (500, 410, 820, 470), "#808a99", "#808a99", 1)
        draw_person(draw, 430, 430, 1.0, "#3f8efc")
        ellipse(draw, (100, 60, 220, 180), "#ffd257", "#f5a524", 5)
        return True
    if "sound travels" in lower:
        draw_person(draw, 210, 420, 0.9, "#3f8efc")
        for i in range(5):
            draw.arc((285 + i * 65, 210 - i * 22, 485 + i * 90, 445 + i * 22), 300, 60, fill="#f35b5b", width=7)
        return True
    if "fish breathe" in lower:
        draw_animal(draw, "fish", 430, 310, 1.25)
        draw_water_or_cloud(draw, 520, 420, "water")
        return True
    if "birds have feathers" in lower:
        draw_animal(draw, "bird", 440, 300, 1.35)
        for i in range(5):
            crayon_line(draw, [(620, 220 + i * 28), (735, 200 + i * 18)], SAFE_COLORS[i % len(SAFE_COLORS)], 8)
        return True
    return False


def draw_preposition_scene(draw: ImageDraw.ImageDraw, sentence: str) -> bool:
    lower = sentence.lower()
    if "book is on the table" in lower:
        draw_table(draw, 300, 340, 440, 45)
        draw_book(draw, 520, 285, "#3f8efc")
        return True
    if "bag is beside the door" in lower:
        draw_bag(draw, 360, 360)
        draw_door(draw, 690, 330)
        return True
    if "school is near the park" in lower:
        draw_school(draw, 330, 355)
        draw_tree(draw, 760, 390)
        return True
    if "cat sleeps under the cot" in lower:
        draw_bed(draw, 560, 270)
        draw_animal(draw, "cat", 500, 430, 0.75)
        return True
    if "fan is above the bed" in lower:
        ellipse(draw, (470, 65, 555, 150), "#9aa5b4", "#26334d", 5)
        for pts in [[(512, 107), (380, 80)], [(512, 107), (648, 80)], [(512, 107), (512, 245)]]:
            crayon_line(draw, pts, "#6a7b8f", 16)
        draw_bed(draw, 520, 405)
        return True
    if "picture hangs on the wall" in lower:
        rounded(draw, (330, 120, 700, 360), 18, "#ffffff", "#26334d", 6)
        draw_house(draw, 515, 310)
        crayon_line(draw, [(515, 120), (515, 70)], "#26334d", 4)
        return True
    if "children sit in the classroom" in lower:
        for x in (310, 510, 710):
            draw_person(draw, x, 430, 0.8, SAFE_COLORS[(x // 100) % len(SAFE_COLORS)])
            draw_table(draw, x - 70, 400, 140, 24)
        return True
    if "bus stops near the school" in lower:
        draw_vehicle(draw, 310, 430, "bus")
        draw_school(draw, 720, 360)
        return True
    if "dog runs around the garden" in lower:
        draw_tree(draw, 720, 420)
        draw_animal(draw, "dog", 300, 420, 0.95)
        draw.arc((210, 205, 730, 500), 160, 330, fill="#3f8efc", width=8)
        return True
    if "toy car is behind the sofa" in lower:
        rounded(draw, (360, 250, 720, 430), 40, "#7aa6bf", "#26334d", 6)
        draw_vehicle(draw, 350, 450, "car")
        return True
    if "bottle is next to the lunch box" in lower:
        rounded(draw, (390, 240, 470, 430), 28, "#3f8efc", "#26334d", 5)
        rounded(draw, (550, 295, 730, 430), 24, "#ffbf3f", "#26334d", 5)
        return True
    if "birds fly over the field" in lower:
        draw_animal(draw, "bird", 330, 170, 0.85)
        draw_animal(draw, "bird", 560, 210, 0.75)
        for i in range(10):
            crayon_line(draw, [(120 + i * 85, 450), (160 + i * 85, 350)], "#2fb36d", 7)
        return True
    if "train moves through the tunnel" in lower:
        rounded(draw, (610, 210, 880, 500), 130, "#6a7b8f", "#26334d", 6)
        draw_vehicle(draw, 360, 420, "train")
        draw.arc((220, 230, 620, 510), 180, 330, fill="#3f8efc", width=7)
        return True
    if "cow stands near the tree" in lower:
        draw_animal(draw, "cow", 320, 420, 0.95)
        draw_tree(draw, 730, 410)
        return True
    if "mat lies outside the door" in lower:
        draw_door(draw, 500, 300)
        rounded(draw, (360, 455, 660, 520), 24, "#ff8c42", "#26334d", 5)
        return True
    if "kite flies above the houses" in lower:
        draw_house(draw, 320, 430)
        draw_house(draw, 650, 430)
        draw.polygon([(510, 105), (590, 185), (510, 265), (430, 185)], fill="#ffbf3f", outline="#26334d")
        crayon_line(draw, [(510, 265), (440, 350)], "#26334d", 4)
        return True
    if "bench is under the neem tree" in lower:
        draw_tree(draw, 520, 380)
        rounded(draw, (360, 420, 680, 470), 14, "#8a552e", "#26334d", 5)
        crayon_line(draw, [(390, 470), (370, 540)], "#8a552e", 10)
        crayon_line(draw, [(650, 470), (670, 540)], "#8a552e", 10)
        return True
    if "library is beside the office" in lower:
        draw_school(draw, 330, 370)
        draw_school(draw, 710, 370)
        return True
    if "shoes are below the rack" in lower:
        draw_simple_item(draw, "shelf", 520, 300)
        draw_simple_item(draw, "shoes", 520, 505)
        return True
    if "teacher walks across the room" in lower:
        draw_person(draw, 300, 450, 0.95, "#3f8efc", adult=True)
        crayon_line(draw, [(200, 480), (830, 480)], "#f35b5b", 8)
        draw.polygon([(830, 480), (790, 460), (790, 500)], fill="#f35b5b")
        return True
    if "river flows beside the village" in lower:
        draw_water_or_cloud(draw, 350, 440, "water")
        draw_house(draw, 710, 405)
        draw_house(draw, 840, 420)
        return True
    if "calendar is on the cupboard" in lower:
        rounded(draw, (350, 220, 700, 500), 18, "#c98245", "#26334d", 6)
        rounded(draw, (420, 130, 630, 260), 10, "#ffffff", "#26334d", 5)
        for i in range(3):
            crayon_line(draw, [(445, 170 + i * 28), (610, 170 + i * 28)], SAFE_COLORS[i], 3)
        return True
    if "puppy hides behind the curtain" in lower:
        rounded(draw, (480, 110, 735, 500), 20, "#9b72e8", "#26334d", 5)
        draw_animal(draw, "dog", 430, 430, 0.75)
        return True
    if "students gather near the flag" in lower:
        crayon_line(draw, [(720, 130), (720, 500)], "#26334d", 10)
        draw.polygon([(720, 140), (870, 190), (720, 240)], fill="#ff8c42", outline="#26334d")
        for x in (260, 380, 500):
            draw_person(draw, x, 455, 0.75, SAFE_COLORS[x % len(SAFE_COLORS)])
        return True
    if "moon appears above the trees" in lower:
        ellipse(draw, (460, 80, 570, 190), "#fff1a8", "#f5d46c", 5)
        draw_tree(draw, 350, 430)
        draw_tree(draw, 675, 430)
        return True
    if "under the chair" in lower:
        rounded(draw, (420, 210, 650, 250), 15, "#c98245", "#26334d", 5)
        for x in (450, 620):
            crayon_line(draw, [(x, 250), (x, 430)], "#7d4b2a", 11)
        draw_ball(draw, 535, 430)
        return True
    if "inside the box" in lower or "in the basket" in lower or "in the drawer" in lower:
        rounded(draw, (360, 265, 675, 465), 24, "#d79b55", "#26334d", 6)
        if "pencil" in lower:
            crayon_line(draw, [(465, 240), (610, 395)], "#ffbf3f", 18)
        elif "keys" in lower:
            ellipse(draw, (470, 310, 535, 375), "#ffcf33", "#26334d", 5)
            crayon_line(draw, [(535, 342), (630, 342)], "#ffcf33", 12)
        else:
            for x in (435, 505, 575):
                ellipse(draw, (x, 235, x + 70, 315), "#ffbf3f", "#26334d", 4)
        return True
    if "above" in lower or "over" in lower:
        if "fan" in lower:
            ellipse(draw, (470, 95, 555, 180), "#9aa5b4", "#26334d", 5)
            for pts in [[(512, 137), (380, 110)], [(512, 137), (648, 110)], [(512, 137), (512, 275)]]:
                crayon_line(draw, pts, "#6a7b8f", 16)
            rounded(draw, (340, 400, 690, 480), 24, "#b58a65", "#26334d", 5)
        else:
            draw_animal(draw, "bird" if "birds" in lower else "cat", 330, 220, 1.0)
            draw_tree(draw, 710, 390)
        return True
    if "beside" in lower or "next to" in lower or "near" in lower:
        draw_book(draw, 380, 340, "#ffbf3f")
        rounded(draw, (555, 210, 715, 450), 18, "#8a552e", "#26334d", 5)
        return True
    if "behind" in lower:
        rounded(draw, (440, 240, 720, 430), 28, "#7aa6bf", "#26334d", 5)
        if "puppy" in lower or "toy car" in lower:
            draw_animal(draw, "dog", 360, 390, 0.85)
        else:
            draw_vehicle(draw, 360, 390, "car")
        return True
    if "between" in lower:
        draw_person(draw, 340, 440, 0.9, "#f35b5b")
        draw_person(draw, 512, 440, 0.9, "#3f8efc")
        draw_person(draw, 680, 440, 0.9, "#2fb36d")
        return True
    return False


def draw_general_sentence(draw: ImageDraw.ImageDraw, sentence: str, seed: int) -> None:
    lower = sentence.lower()
    shirt = SAFE_COLORS[seed % len(SAFE_COLORS)]
    if "lamp" in lower:
        draw_lamp(draw, 520, 320, glowing=True)
    elif "clock" in lower:
        draw_clock_face(draw, 520, 275)
    elif "sun shines" in lower or "sun gives" in lower:
        ellipse(draw, (370, 115, 650, 395), "#ffd257", "#f5a524", 8)
        for i in range(12):
            import math
            a = i * 30
            x1 = 510 + math.cos(math.radians(a)) * 165
            y1 = 255 + math.sin(math.radians(a)) * 165
            x2 = 510 + math.cos(math.radians(a)) * 230
            y2 = 255 + math.sin(math.radians(a)) * 230
            crayon_line(draw, [(x1, y1), (x2, y2)], "#ffd257", 10)
    elif "kite" in lower:
        draw.polygon([(520, 105), (620, 205), (520, 305), (420, 205)], fill="#ffbf3f", outline="#26334d")
        crayon_line(draw, [(520, 305), (420, 430)], "#26334d", 4)
        for i in range(3):
            draw.arc((250 + i * 60, 120, 470 + i * 75, 300), 210, 330, fill="#3f8efc", width=6)
    elif "cat" in lower:
        draw_animal(draw, "cat", 300, 380, 1.15)
        if "mice" in lower:
            ellipse(draw, (650, 380, 720, 425), "#9aa5b4", "#26334d", 4)
            ellipse(draw, (760, 365, 830, 410), "#9aa5b4", "#26334d", 4)
            crayon_line(draw, [(435, 350), (615, 395)], "#f35b5b", 6)
    elif "dog" in lower or "puppy" in lower:
        draw_animal(draw, "dog", 300, 390, 1.1)
        if "car" in lower:
            draw_vehicle(draw, 700, 380, "car")
        if "barks" in lower:
            for i in range(3):
                draw.arc((480 + i * 45, 230 - i * 20, 650 + i * 65, 400 + i * 20), 300, 60, fill="#26334d", width=6)
    elif "cow" in lower:
        draw_animal(draw, "cow", 300, 390, 1.1)
        for i in range(9):
            crayon_line(draw, [(620 + i * 24, 430), (630 + i * 24, 350)], "#2fb36d", 6)
    elif "monkey" in lower:
        draw_tree(draw, 610, 380)
        draw_animal(draw, "monkey", 395, 300, 0.9)
        crayon_line(draw, [(455, 310), (565, 230)], "#9b6138", 10)
    elif "bird" in lower:
        draw_animal(draw, "bird", 430, 260, 1.2)
        for i in range(3):
            draw.arc((560 + i * 35, 160 - i * 20, 700 + i * 60, 310 + i * 15), 300, 60, fill="#f35b5b", width=6)
    elif "fish" in lower:
        draw_water_or_cloud(draw, 510, 420, "water")
        draw_animal(draw, "fish", 470, 300, 1.15)
    elif "rabbit" in lower:
        draw_animal(draw, "rabbit", 360, 390, 1.05)
        for i in range(3):
            draw.arc((500 + i * 52, 300 - i * 10, 660 + i * 52, 430), 210, 330, fill="#3f8efc", width=6)
    elif "frog" in lower:
        ellipse(draw, (320, 340, 500, 445), "#67bb5b", "#26334d", 5)
        ellipse(draw, (350, 285, 402, 337), "#67bb5b", "#26334d", 4)
        ellipse(draw, (425, 285, 477, 337), "#67bb5b", "#26334d", 4)
        for i in range(3):
            draw.arc((520 + i * 52, 250, 700 + i * 52, 435), 210, 330, fill="#3f8efc", width=6)
    else:
        draw_person(draw, 285, 455, 1.0, shirt)
        if "chess" in lower:
            draw_table(draw, 430, 355, 420, 45)
            draw_chess(draw, 620, 285)
            crayon_line(draw, [(335, 315), (500, 285)], "#b9794f", 10)
        elif any(word in lower for word in ["eat", "eats", "lunch", "dinner", "breakfast", "dal", "tea"]):
            draw_table(draw, 445, 370, 380, 45)
            draw_plate_food(draw, 620, 335, "cake" if "cake" in lower else "food")
            crayon_line(draw, [(330, 305), (540, 310)], "#b9794f", 10)
            if "share" in lower or "together" in lower or "family" in lower or "we " in lower:
                draw_person(draw, 760, 455, 0.85, "#ff8c42")
        elif "wash" in lower or "brush" in lower:
            draw_sink(draw, 620, 360)
            crayon_line(draw, [(330, 320), (550, 338)], "#b9794f", 12)
            if "brush" in lower or "teeth" in lower:
                ellipse(draw, (600, 220, 690, 310), "#ffffff", "#26334d", 4)
                crayon_line(draw, [(330, 290), (580, 260)], "#3f8efc", 10)
        elif any(word in lower for word in ["read", "reads", "lesson", "answer", "question"]):
            draw_book(draw, 600, 345, "#3f8efc")
            crayon_line(draw, [(330, 325), (535, 340)], "#b9794f", 10)
        elif any(word in lower for word in ["write", "draw", "paint", "homework", "crayons"]):
            draw_table(draw, 430, 360, 420, 45)
            draw_book(draw, 620, 325, "#ffffff")
            for i, color in enumerate(SAFE_COLORS[:4]):
                crayon_line(draw, [(720 + i * 24, 315), (745 + i * 24, 260)], color, 8)
        elif any(word in lower for word in ["pack", "bag"]):
            draw_bag(draw, 630, 360)
            draw_book(draw, 705, 230, "#ffbf3f")
            crayon_line(draw, [(330, 315), (560, 285)], "#b9794f", 10)
        elif "smiles" in lower or "laughs" in lower:
            draw.arc((240, 285, 330, 355), 0, 180, fill="#26334d", width=8)
            for i in range(3):
                draw.arc((430 + i * 60, 215 - i * 20, 600 + i * 70, 390 + i * 16), 300, 60, fill="#f35b5b", width=6)
        elif any(word in lower for word in ["play", "kicks", "football", "ball"]):
            draw_ball(draw, 660, 410)
            crayon_line(draw, [(330, 420), (585, 410)], "#26334d", 7)
        elif "clap" in lower:
            draw_person(draw, 500, 455, 0.9, "#ff8c42")
            draw_person(draw, 700, 455, 0.9, "#2fb36d")
            for x in (360, 560):
                ellipse(draw, (x, 265, x + 48, 335), "#b9794f", "#26334d", 4)
                ellipse(draw, (x + 45, 265, x + 93, 335), "#b9794f", "#26334d", 4)
        elif any(word in lower for word in ["water", "garden", "plants"]):
            for x in (600, 690, 780):
                draw_tree(draw, x, 430)
            draw_water_or_cloud(draw, 520, 360, "water")
        elif any(word in lower for word in ["bus", "car", "cycle", "train"]):
            draw_vehicle(draw, 680, 390, "bus" if "bus" in lower else "car")
        elif "vegetables" in lower:
            draw_table(draw, 430, 360, 420, 45)
            draw_simple_item(draw, "vegetables", 640, 315)
        elif "money" in lower:
            draw_table(draw, 430, 360, 420, 45)
            draw_simple_item(draw, "money", 640, 315)
        elif "temperature" in lower:
            draw_simple_item(draw, "thermometer", 650, 265)
        elif "gate" in lower:
            draw_simple_item(draw, "gate", 650, 330)
        elif "shoes" in lower:
            draw_simple_item(draw, "shoes", 650, 390)
        elif "crayons" in lower:
            draw_table(draw, 430, 360, 420, 45)
            draw_simple_item(draw, "crayons", 650, 310)
        elif "flowers" in lower or "house" in lower:
            draw_table(draw, 430, 360, 420, 45)
            rounded(draw, (560, 250, 730, 360), 12, "#ffffff", "#26334d", 5)
            if "house" in lower:
                draw_house(draw, 645, 350)
            else:
                draw_flower_patch(draw, 575, 260)
        elif "stories" in lower or "story" in lower:
            draw_person(draw, 620, 455, 1.0, "#ff8c42", adult=True)
            draw_book(draw, 500, 330, "#ffbf3f")
        elif "bed" in lower or "sleep" in lower or "wake up" in lower:
            draw_bed(draw, 620, 340, with_person=True)
        elif "sweep" in lower or "tidy" in lower or "clean" in lower:
            draw_table(draw, 540, 360, 260, 38)
            crayon_line(draw, [(620, 250), (760, 470)], "#8a552e", 12)
            for i in range(8):
                crayon_line(draw, [(710 + i * 12, 470), (735 + i * 12, 520)], "#c98245", 4)
        elif "shelf" in lower or "books on the shelf" in lower:
            draw_simple_item(draw, "shelf", 650, 320)
        elif "exercise" in lower or "runs" in lower or "walks" in lower or "rest" in lower:
            for i in range(3):
                draw.arc((400 + i * 55, 250 - i * 12, 560 + i * 70, 430), 210, 330, fill="#3f8efc", width=6)
        else:
            draw_book(draw, 620, 345, "#3f8efc")


def create_draft(sentence_id: str, sentence: str, out_path: Path) -> None:
    lower = sentence.lower()
    seed = sum((index + 1) * ord(char) for index, char in enumerate(sentence_id + sentence))
    outdoors = any(word in lower for word in ["tree", "garden", "park", "road", "field", "village", "sun", "moon", "kite", "river", "rain"])
    night = any(word in lower for word in ["moon", "stars", "night sky", "earth moves"])
    image, draw = base_scene(seed, outdoors=outdoors, night=night)
    handled = draw_science(draw, sentence)
    if not handled:
        handled = draw_preposition_scene(draw, sentence)
    if not handled:
        draw_general_sentence(draw, sentence, seed)
    add_crayon_texture(image, seed).save(out_path, "PNG", optimize=True)


def generate_missing_drafts(overwrite: bool = False) -> None:
    lookup = sentence_lookup()
    PILOT_DIR.mkdir(parents=True, exist_ok=True)
    generated = 0
    for sentence_id, sentence in lookup.items():
        out_path = PILOT_DIR / f"sentence_{sentence_id}.png"
        if out_path.exists() and not overwrite:
            continue
        if sentence_id in PILOT_IDS and out_path.exists():
            continue
        create_draft(sentence_id, sentence, out_path)
        generated += 1
    print(f"Generated {generated} crayon-style draft PNGs in {PILOT_DIR}.")


def missing_drafts() -> list[Path]:
    return [
        PILOT_DIR / f"sentence_{sentence_id}.png"
        for sentence_id in sentence_ids()
        if not (PILOT_DIR / f"sentence_{sentence_id}.png").is_file()
    ]


def write_resource_map(ids: list[str]) -> None:
    lines = [
        "package com.sunnyapps.sentencebuilder.ui.components",
        "",
        "import com.sunnyapps.sentencebuilder.R",
        "",
        "object SentenceImageResources {",
        "    private val resources = mapOf(",
    ]
    for index, sentence_id in enumerate(ids):
        res_name = f"sentence_{sentence_id}"
        comma = "," if index < len(ids) - 1 else ""
        lines.append(f'        "{res_name}" to R.drawable.{res_name}{comma}')
    lines += [
        "    )",
        "",
        "    fun idFor(imageResName: String): Int = resources[imageResName] ?: 0",
        "}",
    ]
    RESOURCE_MAP.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_app_images() -> None:
    missing = []
    for sentence_id in sentence_ids():
        image = APP_IMAGE_DIR / f"sentence_{sentence_id}.webp"
        if not image.is_file():
            missing.append(str(image))
    if missing:
        raise SystemExit("Missing sentence images:\n" + "\n".join(missing))
    print("All 150 app sentence images are present.")


def validate_drafts() -> None:
    if not PILOT_DIR.is_dir():
        raise SystemExit(
            "Missing image_pilot directory. The public GitHub package omits raw PNG drafts; "
            "restore image_pilot/ from the private art archive before running validate-drafts."
        )
    missing = missing_drafts()
    if missing:
        raise SystemExit("Missing sentence PNG drafts:\n" + "\n".join(str(path) for path in missing))
    print("All 150 PNG drafts are present.")


def convert_pilot() -> None:
    APP_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    missing = []
    for sentence_id in PILOT_IDS:
        source = PILOT_DIR / f"sentence_{sentence_id}.png"
        if not source.is_file():
            missing.append(str(source))
            continue
        target = APP_IMAGE_DIR / f"sentence_{sentence_id}.webp"
        with Image.open(source) as image:
            image.convert("RGB").save(target, "WEBP", quality=88, method=6)
    if missing:
        raise SystemExit("Missing pilot PNG drafts:\n" + "\n".join(missing))
    write_resource_map(sentence_ids())
    print(f"Converted {len(PILOT_IDS)} pilot images to app WebP resources.")


def convert_all() -> None:
    APP_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    validate_drafts()
    for sentence_id in sentence_ids():
        source = PILOT_DIR / f"sentence_{sentence_id}.png"
        target = APP_IMAGE_DIR / f"sentence_{sentence_id}.webp"
        with Image.open(source) as image:
            image.convert("RGB").save(target, "WEBP", quality=88, method=6)
    write_resource_map(sentence_ids())
    print("Converted all 150 approved PNG drafts to app WebP resources.")


def fit_on_game_canvas(image: Image.Image) -> Image.Image:
    source = image.convert("RGB")

    background_scale = max(CANVAS_SIZE[0] / source.width, CANVAS_SIZE[1] / source.height)
    background_size = (
        max(1, int(source.width * background_scale)),
        max(1, int(source.height * background_scale)),
    )
    background = source.resize(background_size, Image.Resampling.LANCZOS)
    left = max(0, (background.width - CANVAS_SIZE[0]) // 2)
    top = max(0, (background.height - CANVAS_SIZE[1]) // 2)
    background = background.crop((left, top, left + CANVAS_SIZE[0], top + CANVAS_SIZE[1]))
    background = background.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.blend(background, Image.new("RGB", CANVAS_SIZE, "#fff6dc"), 0.35)

    scale = min(CANVAS_SIZE[0] / source.width, CANVAS_SIZE[1] / source.height)
    size = (max(1, int(source.width * scale)), max(1, int(source.height * scale)))
    resized = source.resize(size, Image.Resampling.LANCZOS)
    x = (CANVAS_SIZE[0] - resized.width) // 2
    y = (CANVAS_SIZE[1] - resized.height) // 2
    canvas.paste(resized, (x, y))
    return canvas


def crop_batch_sheets() -> None:
    batch_dir = PILOT_DIR / "batch_sheets"
    PILOT_DIR.mkdir(parents=True, exist_ok=True)
    expected_ids = set(sentence_ids())
    batch_ids = {sentence_id for ids in BATCH_IDS.values() for sentence_id in ids}
    pilot_ids = set(PILOT_IDS)

    if batch_ids & pilot_ids:
        overlap = ", ".join(sorted(batch_ids & pilot_ids))
        raise SystemExit(f"Batch ids must not overwrite approved pilot images: {overlap}")
    if batch_ids | pilot_ids != expected_ids:
        missing = ", ".join(sorted(expected_ids - batch_ids - pilot_ids))
        extra = ", ".join(sorted((batch_ids | pilot_ids) - expected_ids))
        raise SystemExit(f"Batch id mismatch. Missing: {missing or 'none'} Extra: {extra or 'none'}")

    cropped = 0
    for batch_number, ids in BATCH_IDS.items():
        source = batch_dir / f"batch_{batch_number}.png"
        if not source.is_file():
            raise SystemExit(f"Missing batch sheet: {source}")

        with Image.open(source) as sheet:
            image = sheet.convert("RGB")
            columns = 2
            rows = 5
            cell_width = image.width // columns
            cell_height = image.height // rows
            if len(ids) != columns * rows:
                raise SystemExit(f"Batch {batch_number} expected {columns * rows} ids, found {len(ids)}")

            for index, sentence_id in enumerate(ids):
                col = index % columns
                row = index // columns
                left = col * cell_width
                top = row * cell_height
                right = image.width if col == columns - 1 else (col + 1) * cell_width
                bottom = image.height if row == rows - 1 else (row + 1) * cell_height
                draft = fit_on_game_canvas(image.crop((left, top, right, bottom)))
                draft.save(PILOT_DIR / f"sentence_{sentence_id}.png", "PNG", optimize=True)
                cropped += 1

    print(f"Cropped {cropped} generated batch images into {PILOT_DIR}.")


def create_contact_sheets() -> None:
    lookup = sentence_lookup()
    sheet_dir = PILOT_DIR / "contact_sheets"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    thumb_size = (256, 144)
    label_height = 24
    columns = 5
    for level in range(1, 6):
        ids = [sentence_id for sentence_id in sentence_ids() if sentence_id.startswith(f"l{level}_")]
        rows = 6
        sheet = Image.new("RGB", (columns * thumb_size[0], rows * (thumb_size[1] + label_height)), "#fff8ea")
        draw = ImageDraw.Draw(sheet)
        for index, sentence_id in enumerate(ids):
            source = PILOT_DIR / f"sentence_{sentence_id}.png"
            with Image.open(source) as image:
                thumb = image.convert("RGB")
                thumb.thumbnail(thumb_size)
                x = (index % columns) * thumb_size[0] + (thumb_size[0] - thumb.width) // 2
                y = (index // columns) * (thumb_size[1] + label_height)
                sheet.paste(thumb, (x, y))
                label = sentence_id
                draw.text(((index % columns) * thumb_size[0] + 8, y + thumb_size[1] + 5), label, fill="#243047")
        sheet.save(sheet_dir / f"level_{level}_contact_sheet.png", "PNG", optimize=True)
    print(f"Created level contact sheets in {sheet_dir}.")


def print_pilot_prompts() -> None:
    lookup = sentence_lookup()
    PILOT_DIR.mkdir(parents=True, exist_ok=True)
    for sentence_id in PILOT_IDS:
        sentence = lookup[sentence_id]
        print(f"{sentence_id}: {sentence}")
        print(
            "A crayon-style child drawing illustration for an educational sentence-building game. "
            f"Show this exact idea clearly: {sentence} "
            "Large clear subjects, one obvious action, simple classroom-friendly background, colorful wax crayon texture, "
            "drawn like a careful child made it but still easy to interpret for school-age learners. "
            "No text, no letters, no watermark, no logos, no brand names, no scary content, no clutter."
        )
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=[
            "validate",
            "validate-drafts",
            "missing-drafts",
            "generate-missing-drafts",
            "crop-batches",
            "convert-pilot",
            "convert-all",
            "contact-sheets",
            "pilot-prompts",
            "resource-map",
        ],
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.command == "validate":
        validate_app_images()
    elif args.command == "validate-drafts":
        validate_drafts()
    elif args.command == "missing-drafts":
        missing = missing_drafts()
        if missing:
            print("\n".join(str(path) for path in missing))
        else:
            print("No missing PNG drafts.")
    elif args.command == "generate-missing-drafts":
        generate_missing_drafts(overwrite=args.overwrite)
    elif args.command == "crop-batches":
        crop_batch_sheets()
    elif args.command == "convert-pilot":
        convert_pilot()
    elif args.command == "convert-all":
        convert_all()
    elif args.command == "contact-sheets":
        create_contact_sheets()
    elif args.command == "pilot-prompts":
        print_pilot_prompts()
    elif args.command == "resource-map":
        write_resource_map(sentence_ids())
        print("Regenerated sentence image resource map.")


if __name__ == "__main__":
    main()
