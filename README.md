# MetaDrop

by Dr. Brent Allen Jensen

See the metadata hiding in your images — and strip it before you
share them. EXIF data can carry camera models, timestamps, and GPS
coordinates; MetaDrop shows it in plain language and writes clean
copies with it removed.

## Quickstart

```bash
pip install -r requirements.txt        # just `Pillow`

python3 metadrop.py show photo.jpg
python3 metadrop.py show a.jpg b.png
python3 metadrop.py strip photo.jpg                  # writes photo_stripped.jpg
python3 metadrop.py strip photo.jpg -o clean.jpg
python3 metadrop.py strip a.jpg b.jpg --out-dir clean/
```

## Commands

| Command | What it does |
|---|---|
| `show` | Print format, dimensions, mode, EXIF tags (human-readable names), and other embedded info |
| `strip` | Write copies rebuilt from pixel data only — EXIF and info metadata gone |

Originals are never modified. Stripped files keep the source format
(JPEG, PNG, WebP, …) and gain a `_stripped` suffix unless you name the
output yourself.

## Requirements

- Python 3.10+, `Pillow`

## Notes

- Stripping rebuilds the image from its pixels, so ancillary extras
  (thumbnails, color-profile chunks, text chunks) are dropped along
  with EXIF. For animated images only the first frame is kept.
- `show` reports "No EXIF data" for images that carry none — that is
  the answer, not an error.

## Support this work

If this tool saved you time or taught you something, donations keep the work going:

- BTC: 15McijPo79Zx58NGyEf2PvaPtGqGmpztWn
- ETH: 0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B

## License

MIT — see [LICENSE](LICENSE).
