# Blur Image

Blur a photo or a screenshot without leaving the conversation.

## Use it

Attach an image and ask Claude to blur it. The whole image is blurred at strength 30 on
a 0-100 scale, where 100 is a radius of 5% of the image's shorter side. Ask for a
different number, or for "stronger" or "softer", and Claude redoes it. You get the file
back in the format you sent — PNG, JPEG or WebP — ready to download.

This plugin blurs the whole picture. To cover only part of one — a face, a license
plate, a name, a line of text — use the
[Blur Image extension for Chrome](https://chromewebstore.google.com/detail/blur-image/khgdjngglcdkgfnnoneopelpiaebkdkh).
It blurs rectangles, ellipses and freehand shapes, has a strength slider with a live
preview, and adds highlight frames and arrows. The same editor runs on the web at
[blurimage.tech](https://blurimage.tech).

## Data

The image you attach goes to Claude, the way any file you upload to a conversation does,
and the blur runs in Claude's own sandbox with Pillow. The plugin sends nothing anywhere
else, stores nothing, and has no server, no account and no API key. The Chrome extension
processes files on your computer and has no network access at all.

## What's inside

- `skills/blur-image/SKILL.md` — when Claude uses the skill and how
- `skills/blur-image/scripts/blur.py` — the blur itself, Pillow's Gaussian blur with the
  same radius formula as the Chrome extension

## License

MIT. See [LICENSE](LICENSE).
