from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT / "app/src/main/java/com/sunnyapps/sentencebuilder/data/SentenceRepository.kt"
OUT_DIR = ROOT / "app/src/main/res/drawable-nodpi"
RESOURCE_MAP = ROOT / "app/src/main/java/com/sunnyapps/sentencebuilder/ui/components/SentenceImageResources.kt"

WIDTH = 640
HEIGHT = 360


def parse_sentences() -> list[tuple[str, str]]:
    text = REPOSITORY.read_text(encoding="utf-8")
    return re.findall(r'item\("(l\d+_\d+)",\s*\d+,\s*"[^"]+",\s*"([^"]+)"', text)


def ellipse(draw: ImageDraw.ImageDraw, cx: float, cy: float, rx: float, ry: float, fill, outline=None, width=1):
    draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=fill, outline=outline, width=width)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_person(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, shirt="#4D8BFF", child=True):
    skin = "#8D5A3B"
    h = 78 if child else 96
    ellipse(draw, x, y - h * scale, 18 * scale, 18 * scale, skin, "#5A3527", 2)
    draw.arc((x - 10 * scale, y - (h + 4) * scale, x + 10 * scale, y - (h - 10) * scale), 0, 180, fill="#243047", width=max(2, int(3 * scale)))
    rounded(draw, (x - 20 * scale, y - 58 * scale, x + 20 * scale, y - 12 * scale), 12 * scale, shirt, "#243047", 2)
    draw.line((x - 16 * scale, y - 12 * scale, x - 28 * scale, y + 18 * scale), fill="#243047", width=max(2, int(4 * scale)))
    draw.line((x + 16 * scale, y - 12 * scale, x + 28 * scale, y + 18 * scale), fill="#243047", width=max(2, int(4 * scale)))
    draw.line((x - 18 * scale, y - 45 * scale, x - 46 * scale, y - 34 * scale), fill=skin, width=max(2, int(5 * scale)))
    draw.line((x + 18 * scale, y - 45 * scale, x + 46 * scale, y - 34 * scale), fill=skin, width=max(2, int(5 * scale)))


def draw_animal(draw: ImageDraw.ImageDraw, kind: str, x: int, y: int, scale: float = 1.0):
    colors = {
        "cat": "#F6A85D", "dog": "#B57A4D", "cow": "#F5F1E8", "monkey": "#9B6A43",
        "bird": "#57A6FF", "fish": "#4DB6AC", "rabbit": "#FFFFFF", "frog": "#69B96B",
        "puppy": "#C98B5A"
    }
    fill = colors.get(kind, "#F6A85D")
    outline = "#243047"
    if kind == "bird":
        ellipse(draw, x, y, 34 * scale, 24 * scale, fill, outline, 2)
        draw.polygon([(x + 32 * scale, y - 4 * scale), (x + 52 * scale, y + 6 * scale), (x + 32 * scale, y + 14 * scale)], fill="#FFC857", outline=outline)
        ellipse(draw, x + 12 * scale, y - 10 * scale, 4 * scale, 4 * scale, outline)
        draw.arc((x - 8 * scale, y - 38 * scale, x + 54 * scale, y + 8 * scale), 195, 315, fill=outline, width=3)
        return
    if kind == "fish":
        ellipse(draw, x, y, 42 * scale, 24 * scale, fill, outline, 2)
        draw.polygon([(x - 42 * scale, y), (x - 72 * scale, y - 24 * scale), (x - 72 * scale, y + 24 * scale)], fill="#FF7A6B", outline=outline)
        ellipse(draw, x + 20 * scale, y - 6 * scale, 4 * scale, 4 * scale, outline)
        return
    if kind == "frog":
        ellipse(draw, x, y, 40 * scale, 26 * scale, fill, outline, 2)
        ellipse(draw, x - 18 * scale, y - 22 * scale, 10 * scale, 10 * scale, fill, outline, 2)
        ellipse(draw, x + 18 * scale, y - 22 * scale, 10 * scale, 10 * scale, fill, outline, 2)
        draw.arc((x - 18 * scale, y - 2 * scale, x + 18 * scale, y + 18 * scale), 10, 170, fill=outline, width=2)
        return
    ellipse(draw, x, y, 48 * scale, 26 * scale, fill, outline, 2)
    ellipse(draw, x + 46 * scale, y - 20 * scale, 24 * scale, 24 * scale, fill, outline, 2)
    if kind in {"cat", "rabbit"}:
        draw.polygon([(x + 30 * scale, y - 42 * scale), (x + 42 * scale, y - 66 * scale), (x + 52 * scale, y - 38 * scale)], fill=fill, outline=outline)
        draw.polygon([(x + 54 * scale, y - 38 * scale), (x + 74 * scale, y - 62 * scale), (x + 72 * scale, y - 30 * scale)], fill=fill, outline=outline)
    ellipse(draw, x + 54 * scale, y - 24 * scale, 4 * scale, 4 * scale, outline)
    for dx in (-28, 10):
        draw.line((x + dx * scale, y + 18 * scale, x + dx * scale, y + 48 * scale), fill=outline, width=max(2, int(4 * scale)))
    draw.arc((x - 70 * scale, y - 35 * scale, x - 22 * scale, y + 15 * scale), 210, 350, fill=outline, width=max(2, int(5 * scale)))
    if kind == "cow":
        ellipse(draw, x - 8 * scale, y - 6 * scale, 10 * scale, 8 * scale, "#243047")
        ellipse(draw, x + 20 * scale, y + 4 * scale, 12 * scale, 10 * scale, "#243047")


def draw_object(draw: ImageDraw.ImageDraw, name: str, x: int, y: int, scale: float = 1.0):
    outline = "#243047"
    if name in {"cake", "dal", "dinner", "breakfast", "lunch", "tea", "food"}:
        rounded(draw, (x - 42 * scale, y - 20 * scale, x + 42 * scale, y + 20 * scale), 10 * scale, "#F9D08A", outline, 2)
        ellipse(draw, x, y - 20 * scale, 42 * scale, 10 * scale, "#FFB3C7", outline, 2)
    elif name in {"chess"}:
        rounded(draw, (x - 46 * scale, y - 34 * scale, x + 46 * scale, y + 34 * scale), 8 * scale, "#FFFFFF", outline, 2)
        cell = 23 * scale
        for row in range(4):
            for col in range(4):
                if (row + col) % 2 == 0:
                    draw.rectangle((x - 46 * scale + col * cell, y - 34 * scale + row * cell, x - 46 * scale + (col + 1) * cell, y - 34 * scale + (row + 1) * cell), fill="#243047")
    elif name in {"mice", "mouse"}:
        for i in range(2):
            ellipse(draw, x + i * 44 * scale, y, 22 * scale, 12 * scale, "#B8BDC9", outline, 2)
            ellipse(draw, x - 12 * scale + i * 44 * scale, y - 12 * scale, 7 * scale, 7 * scale, "#B8BDC9", outline, 2)
            draw.arc((x + 12 * scale + i * 44 * scale, y - 2 * scale, x + 46 * scale + i * 44 * scale, y + 30 * scale), 190, 340, fill=outline, width=2)
    elif name in {"hands"}:
        ellipse(draw, x - 24 * scale, y, 18 * scale, 24 * scale, "#8D5A3B", outline, 2)
        ellipse(draw, x + 24 * scale, y, 18 * scale, 24 * scale, "#8D5A3B", outline, 2)
        for bx in (-54, 54):
            ellipse(draw, x + bx * scale, y - 36 * scale, 9 * scale, 9 * scale, "#82DDF0")
    elif name in {"books", "book", "lesson", "notebook", "timetable", "letters", "question"}:
        for i, color in enumerate(["#4D8BFF", "#FFC857", "#FF7A6B"]):
            rounded(draw, (x - 48 * scale, y - (20 - i * 14) * scale, x + 48 * scale, y + (4 + i * 14) * scale), 6 * scale, color, outline, 2)
    elif name in {"car", "bus", "train", "cycle"}:
        body = "#FF7A6B" if name != "bus" else "#FFC857"
        rounded(draw, (x - 66 * scale, y - 30 * scale, x + 66 * scale, y + 18 * scale), 14 * scale, body, outline, 2)
        rounded(draw, (x - 34 * scale, y - 58 * scale, x + 38 * scale, y - 24 * scale), 12 * scale, "#EAF3FF", outline, 2)
        ellipse(draw, x - 40 * scale, y + 20 * scale, 14 * scale, 14 * scale, "#243047")
        ellipse(draw, x + 42 * scale, y + 20 * scale, 14 * scale, 14 * scale, "#243047")
    elif name in {"grass", "plants", "plant", "flowers", "garden", "tree", "rice", "roots", "soil", "seeds", "leaves"}:
        for i in range(7):
            bx = x - 70 * scale + i * 22 * scale
            draw.line((bx, y + 28 * scale, bx + 8 * scale, y - 18 * scale), fill="#3BAA77", width=max(2, int(4 * scale)))
        if name in {"tree", "plants", "plant", "flowers", "garden", "leaves"}:
            draw.rectangle((x - 8 * scale, y - 62 * scale, x + 8 * scale, y + 28 * scale), fill="#8B5A2B")
            ellipse(draw, x, y - 88 * scale, 45 * scale, 38 * scale, "#3BAA77", outline, 2)
            if name == "flowers":
                for dx in (-32, 0, 32):
                    ellipse(draw, x + dx * scale, y - 12 * scale, 10 * scale, 10 * scale, "#FF7A6B")
    elif name in {"ball", "football"}:
        ellipse(draw, x, y, 34 * scale, 34 * scale, "#FFFFFF", outline, 3)
        draw.line((x - 25 * scale, y, x + 25 * scale, y), fill=outline, width=2)
        draw.line((x, y - 25 * scale, x, y + 25 * scale), fill=outline, width=2)
    elif name in {"sun", "sunlight", "heat", "light"}:
        ellipse(draw, x, y, 34 * scale, 34 * scale, "#FFC857", outline, 2)
        for angle in range(0, 360, 45):
            import math
            x1 = x + math.cos(math.radians(angle)) * 46 * scale
            y1 = y + math.sin(math.radians(angle)) * 46 * scale
            x2 = x + math.cos(math.radians(angle)) * 62 * scale
            y2 = y + math.sin(math.radians(angle)) * 62 * scale
            draw.line((x1, y1, x2, y2), fill="#FFC857", width=max(2, int(5 * scale)))
    elif name in {"moon"}:
        ellipse(draw, x, y, 38 * scale, 38 * scale, "#F3F1D1", outline, 2)
        ellipse(draw, x + 16 * scale, y - 8 * scale, 34 * scale, 34 * scale, "#96BFEA")
    elif name in {"water", "river", "rain", "vapor", "clouds", "air"}:
        if name == "rain":
            for i in range(8):
                draw.line((x - 70 * scale + i * 20 * scale, y - 40 * scale, x - 76 * scale + i * 20 * scale, y - 18 * scale), fill="#4D8BFF", width=3)
        elif name == "clouds" or name == "air":
            for dx in (-30, 0, 30):
                ellipse(draw, x + dx * scale, y, 30 * scale, 20 * scale, "#FFFFFF", outline, 2)
        else:
            draw.arc((x - 80 * scale, y - 10 * scale, x - 20 * scale, y + 30 * scale), 0, 180, fill="#4D8BFF", width=6)
            draw.arc((x - 20 * scale, y - 10 * scale, x + 40 * scale, y + 30 * scale), 0, 180, fill="#4D8BFF", width=6)
    elif name in {"bulb", "electricity"}:
        ellipse(draw, x, y - 20 * scale, 30 * scale, 30 * scale, "#FFE66D", outline, 2)
        rounded(draw, (x - 16 * scale, y + 8 * scale, x + 16 * scale, y + 34 * scale), 5 * scale, "#8A96A8", outline, 2)
        for dx in (-60, -42, 42, 60):
            draw.line((x + dx * scale, y - 26 * scale, x + (dx * 0.75) * scale, y - 10 * scale), fill="#FFC857", width=4)
    elif name in {"magnet", "magnets", "iron"}:
        draw.arc((x - 45 * scale, y - 50 * scale, x + 45 * scale, y + 50 * scale), 30, 330, fill="#FF7A6B", width=max(8, int(16 * scale)))
        for dx in (-70, 70):
            rounded(draw, (x + dx * scale - 18 * scale, y - 12 * scale, x + dx * scale + 18 * scale, y + 12 * scale), 4 * scale, "#8A96A8", outline, 2)
    elif name in {"clock", "temperature", "thermometer"}:
        if name == "thermometer" or name == "temperature":
            rounded(draw, (x - 10 * scale, y - 70 * scale, x + 10 * scale, y + 24 * scale), 9 * scale, "#FFFFFF", outline, 2)
            ellipse(draw, x, y + 28 * scale, 22 * scale, 22 * scale, "#FF7A6B", outline, 2)
            draw.line((x, y + 20 * scale, x, y - 48 * scale), fill="#FF7A6B", width=max(3, int(7 * scale)))
        else:
            ellipse(draw, x, y, 42 * scale, 42 * scale, "#FFFFFF", outline, 3)
            draw.line((x, y, x, y - 26 * scale), fill=outline, width=3)
            draw.line((x, y, x + 20 * scale, y + 10 * scale), fill=outline, width=3)
    elif name in {"heart", "lungs", "brain", "body", "blood", "healthy", "health"}:
        ellipse(draw, x - 18 * scale, y - 15 * scale, 22 * scale, 22 * scale, "#FF7A6B", outline, 2)
        ellipse(draw, x + 18 * scale, y - 15 * scale, 22 * scale, 22 * scale, "#FF7A6B", outline, 2)
        draw.polygon([(x - 40 * scale, y - 4 * scale), (x + 40 * scale, y - 4 * scale), (x, y + 54 * scale)], fill="#FF7A6B", outline=outline)
    elif name in {"kite"}:
        draw.polygon([(x, y - 58 * scale), (x + 48 * scale, y), (x, y + 58 * scale), (x - 48 * scale, y)], fill="#FFC857", outline=outline)
        draw.line((x, y + 58 * scale, x - 50 * scale, y + 96 * scale), fill=outline, width=2)
    elif name in {"shadow"}:
        ellipse(draw, x, y + 34 * scale, 70 * scale, 16 * scale, "#8A96A8")
        rounded(draw, (x - 22 * scale, y - 60 * scale, x + 22 * scale, y + 22 * scale), 8 * scale, "#4D8BFF", outline, 2)
    else:
        rounded(draw, (x - 48 * scale, y - 34 * scale, x + 48 * scale, y + 34 * scale), 14 * scale, "#FFFFFF", outline, 2)
        ellipse(draw, x, y, 18 * scale, 18 * scale, "#FFC857", outline, 2)


SUBJECTS: dict[str, Callable[[ImageDraw.ImageDraw, int, int, float], None]] = {
    "cat": lambda d, x, y, s: draw_animal(d, "cat", x, y, s),
    "dog": lambda d, x, y, s: draw_animal(d, "dog", x, y, s),
    "puppy": lambda d, x, y, s: draw_animal(d, "puppy", x, y, s),
    "cow": lambda d, x, y, s: draw_animal(d, "cow", x, y, s),
    "cows": lambda d, x, y, s: draw_animal(d, "cow", x, y, s),
    "monkey": lambda d, x, y, s: draw_animal(d, "monkey", x, y, s),
    "bird": lambda d, x, y, s: draw_animal(d, "bird", x, y, s),
    "birds": lambda d, x, y, s: draw_animal(d, "bird", x, y, s),
    "fish": lambda d, x, y, s: draw_animal(d, "fish", x, y, s),
    "rabbit": lambda d, x, y, s: draw_animal(d, "rabbit", x, y, s),
    "frog": lambda d, x, y, s: draw_animal(d, "frog", x, y, s),
}


OBJECT_KEYWORDS = [
    "cake", "chess", "mice", "hands", "books", "book", "car", "grass", "tree", "flowers",
    "ball", "football", "sun", "sunlight", "kite", "rice", "plants", "plant", "water",
    "bus", "cycle", "tea", "dinner", "lunch", "breakfast", "notebook", "lesson", "garden",
    "moon", "clouds", "rain", "vapor", "air", "magnet", "magnets", "iron", "seeds",
    "roots", "soil", "leaves", "heart", "lungs", "brain", "blood", "temperature",
    "thermometer", "bulb", "electricity", "shadow", "river", "healthy", "health", "clock",
    "letters", "question", "food", "light", "heat"
]


def draw_scene(sentence_id: str, sentence: str, out_path: Path):
    tokens = set(re.findall(r"[a-z]+", sentence.lower()))
    seed = sum((index + 1) * ord(char) for index, char in enumerate(sentence_id + sentence))
    palette = ["#4D8BFF", "#3BAA77", "#FFC857", "#FF7A6B", "#8A7CFF", "#69D2E7"]
    image = Image.new("RGB", (WIDTH, HEIGHT), "#EAF3FF")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 225, WIDTH, HEIGHT), fill="#FFF8EA")
    ellipse(draw, 76, 66, 44, 44, "#FFC857")
    for cx, cy in [(510, 78), (550, 72), (590, 82)]:
        ellipse(draw, cx, cy, 35, 22, "#FFFFFF", "#DDE7F2", 2)
    for i in range(7):
        draw.line((28 + i * 28, 285, 38 + i * 28, 245), fill="#3BAA77", width=4)
    # Sentence-specific, non-text classroom decoration keeps each offline image unique.
    for i in range(5):
        color = palette[(seed + i) % len(palette)]
        x = 388 + i * 42
        y = 24 + ((seed >> (i * 2)) % 28)
        if (seed + i) % 2 == 0:
            ellipse(draw, x, y, 10 + ((seed + i) % 5), 10 + ((seed + i) % 5), color)
        else:
            draw.polygon([(x, y - 13), (x + 14, y + 10), (x - 14, y + 10)], fill=color)

    subject_key = next((key for key in SUBJECTS if key in tokens), None)
    person_words = {"ram", "he", "ravi", "she", "sister", "baby", "anu", "teacher", "friend", "children", "meena", "boy", "grandma", "mother", "father", "class", "uncle", "shopkeeper", "driver", "family", "aunt", "nurse", "postman", "guard", "cousin", "girl", "students", "doctor", "farmer", "grandfather", "grandmother", "brother"}
    has_person = bool(tokens & person_words)

    if subject_key:
        SUBJECTS[subject_key](draw, 190, 250, 1.25)
        if "climbs" in tokens or "tree" in tokens:
            draw_object(draw, "tree", 420, 245, 1.15)
    elif has_person:
        draw_person(draw, 185, 280, 1.15, shirt=palette[seed % len(palette)], child=not bool(tokens & {"mother", "father", "uncle", "aunt", "teacher", "doctor", "farmer", "grandfather", "grandmother", "shopkeeper", "driver", "nurse", "postman", "guard"}))
        if "children" in tokens or "students" in tokens or "class" in tokens or "we" in tokens:
            draw_person(draw, 105, 285, 0.9, shirt=palette[(seed + 2) % len(palette)])
            draw_person(draw, 265, 285, 0.9, shirt=palette[(seed + 4) % len(palette)])
    else:
        # Science and place sentences often have object subjects.
        subject_object = next((word for word in OBJECT_KEYWORDS if word in tokens), "book")
        draw_object(draw, subject_object, 180, 230, 1.35)

    objects = [word for word in OBJECT_KEYWORDS if word in tokens]
    primary_subject_object = subject_key or None
    objects = [word for word in objects if word != primary_subject_object]
    if not objects:
        objects = ["book"]

    positions = [(430, 238), (520, 260), (365, 300)]
    for index, obj in enumerate(objects[:3]):
        draw_object(draw, obj, positions[index][0], positions[index][1], 0.95 if index else 1.1)

    # Visual action cues: motion, sound, or interaction lines.
    if tokens & {"plays", "runs", "hops", "jumps", "flies", "climbs", "kicks", "moves", "walks", "rides"}:
        for i in range(3):
            draw.arc((80 + i * 28, 120 + i * 18, 180 + i * 28, 190 + i * 18), 200, 315, fill="#4D8BFF", width=4)
    if tokens & {"sings", "barks", "rings", "laughs", "clap", "claps", "tells"}:
        for i in range(3):
            draw.arc((270 + i * 20, 120 - i * 15, 350 + i * 38, 205 + i * 12), 290, 60, fill="#FF7A6B", width=4)
    if tokens & {"reads", "writes", "draws", "paints", "answer", "practices"}:
        draw_object(draw, "book", 405, 285, 0.8)

    image.save(out_path, "WEBP", quality=82, method=6)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sentences = parse_sentences()
    if len(sentences) != 150:
        raise SystemExit(f"Expected 150 sentences, found {len(sentences)}")
    for sentence_id, sentence in sentences:
        draw_scene(sentence_id, sentence, OUT_DIR / f"sentence_{sentence_id}.webp")
    write_resource_map([sentence_id for sentence_id, _ in sentences])
    print(f"Generated {len(sentences)} images in {OUT_DIR}")


def write_resource_map(sentence_ids: list[str]):
    lines = [
        "package com.sunnyapps.sentencebuilder.ui.components",
        "",
        "import com.sunnyapps.sentencebuilder.R",
        "",
        "object SentenceImageResources {",
        "    private val resources = mapOf(",
    ]
    for index, sentence_id in enumerate(sentence_ids):
        res_name = f"sentence_{sentence_id}"
        comma = "," if index < len(sentence_ids) - 1 else ""
        lines.append(f'        "{res_name}" to R.drawable.{res_name}{comma}')
    lines += [
        "    )",
        "",
        "    fun idFor(imageResName: String): Int = resources[imageResName] ?: 0",
        "}",
    ]
    RESOURCE_MAP.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
