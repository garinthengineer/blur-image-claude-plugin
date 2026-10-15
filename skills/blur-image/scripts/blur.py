"""Blur a whole image.

Usage: python3 blur.py <input> <output> [strength]

Strength is a 0-100 scale. The radius matches the Blur Image Chrome extension:

    radius = (strength / 100) ** 1.5 * 0.05 * min(width, height)

At 100 the radius is 5% of the image's shorter side. The 1.5 power leaves more
of the scale in the low range, where most pictures are worked on.
"""

import sys

from PIL import Image, ImageFilter

MAX_FRACTION = 0.05


def radius_for(strength, width, height):
    strength = max(0.0, min(100.0, float(strength)))
    return (strength / 100) ** 1.5 * MAX_FRACTION * min(width, height)


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: blur.py <input> <output> [strength]")

    src, dst = sys.argv[1], sys.argv[2]
    strength = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0

    img = Image.open(src)
    fmt = (img.format or "PNG").upper()
    width, height = img.size
    radius = radius_for(strength, width, height)

    if img.mode in ("P", "CMYK", "LA"):
        img = img.convert("RGBA" if img.mode in ("P", "LA") else "RGB")
    if fmt in ("JPEG", "JPG", "MPO") and img.mode != "RGB":
        img = img.convert("RGB")

    out = img.filter(ImageFilter.GaussianBlur(radius))

    if fmt in ("JPEG", "JPG", "MPO"):
        out.save(dst, "JPEG", quality=92)
        saved = "JPEG"
    elif fmt == "WEBP":
        out.save(dst, "WEBP", quality=92)
        saved = "WEBP"
    else:
        out.save(dst, "PNG")
        saved = "PNG"

    print(f"{width}x{height} strength={strength:g} radius={radius:.1f}px saved={saved}")


if __name__ == "__main__":
    main()
