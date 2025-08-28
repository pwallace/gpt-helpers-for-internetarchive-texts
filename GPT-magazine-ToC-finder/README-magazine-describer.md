# README-magazine-describer

## magazine-toc-describer.py

### DESCRIPTION
This script automates the extraction of a magazine's table of contents from scanned images hosted on the Internet Archive. For each magazine identifier provided, the script locates the correct archive file, downloads the first three pages as JPEG previews, and uses the OpenAI GPT-4o API to attempt to transcribe the table of contents. If successful, the table of contents is saved as a text file.

---

### USAGE

1. Prepare a plaintext file (e.g., `identifiers.txt`) containing one Internet Archive identifier per line.
2. Ensure you have an OpenAI API key set in the environment variable `OPENAI_API_KEY`.
3. Install required Python libraries:
    - `requests`
    - `openai`
    - `base64`
4. Run the script:
    ```bash
    python magazine-toc-describer.py identifiers.txt
    ```

---

### PROCESS OVERVIEW

For each identifier in the input file:
- The script queries the Internet Archive metadata API to list files for the item.
- It searches for a file ending in `_jp2.zip` (preferred) or `_images.zip` (fallback).
- The script determines the base filename from the archive file name.
- For each of the first three pages (`_0001`, `_0002`, `_0003`), it constructs a direct JPEG preview URL and downloads the image.
- The downloaded image is sent to GPT-4o with a prompt to extract the table of contents.
- If GPT-4o returns a valid table of contents, it is saved as `{identifier}_toc.txt`.
- If no table of contents is detected after all three pages, a warning is printed and no output file is created.

---

### EXPECTED OUTPUT

- For each magazine where a table of contents is detected, a file named `{identifier}_toc.txt` will be created in the current directory.
- The file contains a hyphen-bulleted list headed by "TABLE OF CONTENTS", with section/article titles and short descriptions as extracted by GPT-4o.

---

### EXPECTED ISSUES / BUGS

- If the Internet Archive item does not contain a `_jp2.zip` or `_images.zip` file, the script will skip that identifier.
- If the preview JPEG for a page cannot be downloaded (e.g., missing or network error), the script will skip that page and try the next.
- If GPT-4o fails to detect a table of contents on all three pages, no output file will be created for that identifier.
- The script does not handle rate limiting or API quota errors from OpenAI or Internet Archive.
- The script assumes the first three pages (`_0001`, `_0002`, `_0003`) are the most likely to contain the table of contents; magazines with TOC on later pages will not be processed.
- The script does not retry failed downloads or API calls.
- The script does not validate the format of the returned table of contents beyond checking for "NO TOC DETECTED".
- The script does not support batch parallelization; items are processed sequentially.
- If the OpenAI API key is missing or invalid, the script will fail.
- If the Internet Archive identifier is invalid or the item is not public, the script will fail for that identifier.

---

### TROUBLESHOOTING

- Ensure your identifiers file contains valid Internet Archive item identifiers, one per line.
- Make sure your OpenAI API key is set in the environment variable `OPENAI_API_KEY`.
- Check your network connection if downloads fail.
- Review warnings printed by the script for skipped items or pages.
- If you encounter API errors, check your OpenAI usage limits and credentials.

---

### CONTACT / SUPPORT

For bug reports or feature requests, contact the script author or project.
