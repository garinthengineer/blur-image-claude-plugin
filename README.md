# Blur Image

Blur a photo or a screenshot without leaving the conversation.

## Use it

Attach an image and say what to blur. Ask for the whole picture and you get the whole
picture blurred; name a face, a license plate, an address, a message or a line of text
and only that part is blurred, with the rest left readable. Say "lighter" or "stronger"
and Claude redoes it. You get the file back in the format you sent — PNG, JPEG or
WebP — ready to download.

Claude places the blur by looking at the picture, so the edges land where it judges
them to be. To set the strength on a slider and pick the spots with your mouse, use the
[Blur Image extension for Chrome](https://chromewebstore.google.com/detail/blur-image/khgdjngglcdkgfnnoneopelpiaebkdkh).
It blurs rectangles, ellipses and freehand shapes, shows the result as you drag, adds
highlight frames and arrows, and runs on your own computer. The same editor is on the
web at [blurimage.tech](https://blurimage.tech).

## Data

The image you attach goes to Claude, the way any file you upload to a conversation does,
and the blur runs in Claude's own sandbox with Pillow. The plugin sends nothing anywhere
else, stores nothing, and has no server, no account and no API key. The Chrome extension
processes files on your computer and has no network access at all.

## What's inside

- `skills/blur-image/SKILL.md` — when Claude uses the skill and how
- `skills/blur-image/scripts/blur.py` — the blur itself: Pillow's Gaussian blur over the
  whole image or over the rectangles and ellipses it is given, with the same radius
  formula as the Chrome extension

## License

MIT. See [LICENSE](LICENSE).
