#!/usr/bin/env python3
import argparse
import os
import sys
from PIL import Image, ExifTags

def get_exif_dict(img):
    exif = img._getexif()
    if exif is None:
        return None
    return {ExifTags.TAGS.get(tag, tag): value for tag, value in exif.items()}

def show_images(files):
    for f in files:
        try:
            with Image.open(f) as img:
                print(f"File: {f}")
                print(f"  Format: {img.format}")
                print(f"  Size: {img.size[0]}x{img.size[1]}")
                print(f"  Mode: {img.mode}")
                exif = get_exif_dict(img)
                if exif:
                    print("  EXIF:")
                    for tag, value in exif.items():
                        print(f"    {tag}: {value}")
                else:
                    print("  EXIF: No EXIF data")
                print(f"  Info: {img.info}")
                print()
        except Exception as e:
            print(f"Error processing {f}: {e}", file=sys.stderr)
            sys.exit(1)

def strip_images(files, output_path=None, output_dir=None):
    if len(files) == 1:
        if output_path:
            out_path = output_path
        else:
            base, ext = os.path.splitext(files[0])
            out_path = f"{base}_stripped{ext}"
    else:
        if not output_dir:
            print("Error: --out-dir required for multiple files", file=sys.stderr)
            sys.exit(1)
        os.makedirs(output_dir, exist_ok=True)
        out_paths = []
        for f in files:
            base = os.path.basename(f)
            name, ext = os.path.splitext(base)
            out_paths.append(os.path.join(output_dir, f"{name}_stripped{ext}"))
        for f, out_path in zip(files, out_paths):
            try:
                with Image.open(f) as img:
                    data = list(img.getdata())
                    new_img = Image.new(img.mode, img.size)
                    new_img.putdata(data)
                    new_img.save(out_path, format=img.format)
                    print(f"{f} -> {out_path}")
            except Exception as e:
                print(f"Error processing {f}: {e}", file=sys.stderr)
                sys.exit(1)
        return

    try:
        with Image.open(files[0]) as img:
            data = list(img.getdata())
            new_img = Image.new(img.mode, img.size)
            new_img.putdata(data)
            new_img.save(out_path, format=img.format)
            print(f"{files[0]} -> {out_path}")
    except Exception as e:
        print(f"Error processing {files[0]}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Metadata manipulation tool for images")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show_parser = subparsers.add_parser("show", help="Display image metadata")
    show_parser.add_argument("files", nargs="+", help="Image files to process")

    strip_parser = subparsers.add_parser("strip", help="Remove metadata from images")
    strip_parser.add_argument("files", nargs="+", help="Image files to process")
    strip_parser.add_argument("-o", "--output", dest="output_path", help="Output file (single input only)")
    strip_parser.add_argument("--out-dir", dest="output_dir", help="Output directory (multiple inputs)")

    args = parser.parse_args()

    if args.command == "show":
        show_images(args.files)
    elif args.command == "strip":
        strip_images(args.files, args.output_path, args.output_dir)

if __name__ == "__main__":
    main()
