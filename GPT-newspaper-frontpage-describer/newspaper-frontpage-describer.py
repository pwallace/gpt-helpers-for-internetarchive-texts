'''
newspaper-frontpage-describer.py

This script reads a plaintext file containing one Internet Archive identifier per line, finds the correct .jp2.zip or .images.zip file for each item, downloads the front page JPG preview, and sends it to GPT-4o for description and summary.

Process:
- For each identifier:
    - Uses the Internet Archive metadata API to list files in the item.
    - Finds the .jp2.zip or .images.zip file and extracts the base filename.
    - Constructs the preview JPG URL for the front page.
    - Downloads the JPG.
    - Sends the JPG to GPT-4o for description and summary.
    - Saves the summary to {identifier}_summary.txt.

Usage:
    python newspaper-frontpage-describer.py identifiers.txt

Requirements:
- OpenAI API key (set as environment variable OPENAI_API_KEY)
- requests, Pillow, openai, base64 Python libraries
'''

import sys
import os
import requests
import tempfile
from PIL import Image
import openai
import base64

def get_jp2_or_images_zip_filename(identifier):
    # Use IA metadata API to list files
    meta_url = f"https://archive.org/metadata/{identifier}"
    r = requests.get(meta_url)
    if r.status_code != 200:
        print(f"    Failed to get metadata for {identifier}")
        return None, None
    meta = r.json()
    files = meta.get("files", [])
    for f in files:
        name = f.get("name", "")
        if name.endswith("_jp2.zip"):
            return name, "jp2"
    for f in files:
        name = f.get("name", "")
        if name.endswith("_images.zip"):
            return name, "images"
    return None, None

def get_base_filename(zipname, ziptype):
    if ziptype == "jp2" and zipname.endswith("_jp2.zip"):
        return zipname[:-8]
    if ziptype == "images" and zipname.endswith("_images.zip"):
        return zipname[:-10]
    return None

def download_frontpage_jpg(identifier, base_filename, ziptype, work_dir):
    if ziptype == "jp2":
        zipname = f"{base_filename}_jp2.zip"
        jp2dir = f"{base_filename}_jp2"
        jp2file = f"{base_filename}_0000.jp2"
        jp2_path = f"{jp2dir}%2F{jp2file}&ext=jpg"
        jpg_url = f"https://archive.org/download/{identifier}/{zipname}/{jp2_path}"
    elif ziptype == "images":
        zipname = f"{base_filename}_images.zip"
        imagesdir = f"{base_filename}_images"
        tiffile = f"{base_filename}_0000.tif"
        tif_path = f"{imagesdir}%2F{tiffile}&ext=jpg"
        jpg_url = f"https://archive.org/download/{identifier}/{zipname}/{tif_path}"
    else:
        return None
    jpg_path = os.path.join(work_dir, f"{base_filename}_0000.jpg")
    print(f"  Downloading {jpg_url} ...")
    r = requests.get(jpg_url, stream=True)
    if r.status_code != 200:
        print(f"    Failed to download {jpg_url}")
        return None
    with open(jpg_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return jpg_path

def get_summary_from_image(image_path):
    api_key = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI(api_key="OPENAI_API_KEY")
    prompt = (
        "Extract all headlines from this newspaper front page. For each headline, provide a 1-2 sentence summary of its content, separated from the headline by a colon. "
        "For headline images, use 'image:' followed by a caption summary or description. "
        "Also list titles for any other articles or sections mentioned in a table of contents, 'in this issue', or similar elements, using the same format. "
        "Do not include page numbers, volume, issue numbers, cover price, or other trivial metadata. "
        "Do not use markdown, bullet points, or any formatting marks. "
        "Do not identify the publication or its type. "
        "Respond only with the requested output."
    )
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please describe and summarize the contents of this newspaper front page."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: python newspaper-frontpage-describer.py identifiers.txt")
        sys.exit(1)

    identifiers_file = sys.argv[1]
    if not os.path.isfile(identifiers_file):
        print(f"Error: File '{identifiers_file}' not found.")
        sys.exit(1)

    with open(identifiers_file, "r") as f:
        identifiers = [line.strip() for line in f if line.strip()]

    print(f"Processing {len(identifiers)} identifiers from '{identifiers_file}' ...")
    for idx, identifier in enumerate(identifiers):
        print(f"\n[{idx+1}/{len(identifiers)}] Processing identifier: {identifier}")
        zipname, ziptype = get_jp2_or_images_zip_filename(identifier)
        if not zipname or not ziptype:
            print(f"  Skipping {identifier}: No _jp2.zip or _images.zip file found.")
            continue
        base_filename = get_base_filename(zipname, ziptype)
        if not base_filename:
            print(f"  Skipping {identifier}: Could not determine base filename.")
            continue
        with tempfile.TemporaryDirectory() as work_dir:
            jpg_path = download_frontpage_jpg(identifier, base_filename, ziptype, work_dir)
            if not jpg_path:
                print(f"  Skipping {identifier} due to download error.")
                continue
            print(f"  Sending front page image to GPT-4o for summary ...")
            summary = get_summary_from_image(jpg_path)
            output_file = f"{identifier}_summary.txt"
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(summary)
            print(f"  Summary saved to '{output_file}'")
    print("\nProcessing complete.")
