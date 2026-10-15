"""Blur a whole image, or only the parts named on the command line.

Usage:
    python3 blur.py <input> <output> [--strength N] [--box x1,y1,x2,y2]...
                                     [--ellipse x1,y1,x2,y2]... [--info]

With no --box and no --ellipse the whole image is blurred. With them, only those
regions are blurred and the rest of the picture is untouched. Coordinates are pixels
of the original image, measured from the top-left corner.

--info prints the image's size and format and changes nothing.

Strength is a 0-100 scale. The radius matches the Blur Image Chrome extension:

    radius = (strength / 100) ** 1.5 * 0.05 * min(width, height)

At 100 the radius is 5% of the image's shorter side. The 1.5 power leaves more of the
scale in the low range, where most pictures are worked on.
"""

import sys

from PIL import Image, ImageDraw, ImageFilter

MAX_FRACTION = 0.05


def radius_for(strength, width, height):
    strength = max(0.0, min(100.0, float(strength)))
    return (strength / 100) ** 1.5 * MAX_FRACTION * min(width, height)


def parse_rect(text, width, height):
    parts = [p for p in text.replace(" ", "").split(",") if p != ""]
    if len(parts) != 4:
        sys.exit(f"bad region {text!r}: expected x1,y1,x2,y2")
    x1, y1, x2, y2 = (int(round(float(p))) for p in parts)
    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))
    x1 = max(0, min(width, x1))
    x2 = max(0, min(width, x2))
    y1 = max(0, min(height, y1))
    y2 = max(0, min(height, y2))
    if x2 - x1 < 1 or y2 - y1 < 1:
        sys.exit(f"region {text!r} is empty after clamping to the image")
    return x1, y1, x2, y2


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)

    src = args[0]
    img = Image.open(src)
    fmt = (img.format or "PNG").upper()
    width, height = img.size

    if "--info" in args:
        print(f"{width}x{height} format={fmt} mode={img.mode}")
        return

    if len(args) < 2:
        sys.exit("usage: blur.py <input> <output> [--strength N] [--box ...]")
    dst = args[1]

    strength = 30.0
    rects, ellipses = [], []
    rest = args[2:]
    i = 0
    while i < len(rest):
        flag = rest[i]
        if flag in ("--strength", "-s"):
            strength = float(rest[i + 1])
            i += 2
        elif flag == "--box":
            rects.append(parse_rect(rest[i + 1], width, height))
            i += 2
        elif flag == "--ellipse":
            ellipses.append(parse_rect(rest[i + 1], width, height))
            i += 2
        else:
            sys.exit(f"unknown option {flag!r}")

    if img.mode in ("P", "LA"):
        img = img.convert("RGBA")
    elif img.mode == "CMYK":
        img = img.convert("RGB")
    if fmt in ("JPEG", "JPG", "MPO") and img.mode != "RGB":
        img = img.convert("RGB")

    radius = radius_for(strength, width, height)
    blurred = img.filter(ImageFilter.GaussianBlur(radius))

    if rects or ellipses:
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        for box in rects:
            draw.rectangle(box, fill=255)
        for box in ellipses:
            draw.ellipse(box, fill=255)
        # Soften the mask edge so the blurred patch doesn't end in a hard line.
        mask = mask.filter(ImageFilter.GaussianBlur(max(1.0, radius / 3)))
        out = Image.composite(blurred, img, mask)
        where = f"{len(rects)} box(es), {len(ellipses)} ellipse(s)"
    else:
        out = blurred
        where = "whole image"

    if fmt in ("JPEG", "JPG", "MPO"):
        out.save(dst, "JPEG", quality=92)
        saved = "JPEG"
    elif fmt == "WEBP":
        out.save(dst, "WEBP", quality=92)
        saved = "WEBP"
    else:
        out.save(dst, "PNG")
        saved = "PNG"

    print(
        f"{width}x{height} strength={strength:g} radius={radius:.1f}px "
        f"blurred={where} saved={saved}"
    )


if __name__ == "__main__":
    main()
