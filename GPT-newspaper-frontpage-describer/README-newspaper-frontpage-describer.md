# README-newspaper-frontpage-describer

## newspaper-frontpage-describer.py

### DESCRIPTION
This script automates the extraction and summarization of newspaper front pages from items hosted on the Internet Archive. For each identifier provided, the script locates the correct archive file, downloads the front page as a JPEG preview, and uses the OpenAI GPT-4o API to generate a concise summary of the headlines and main content. The summary is saved as a text file for each item.

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
    python newspaper-frontpage-describer.py identifiers.txt
    ```

---

### PROCESS OVERVIEW

For each identifier in the input file:
- The script queries the Internet Archive metadata API to list files for the item.
- It searches for a file ending in `_jp2.zip` (preferred) or `_images.zip` (fallback).
- The script determines the base filename from the archive file name.
- It constructs a direct JPEG preview URL for the front page (`_0000`).
- The JPEG image is downloaded.
- The image is sent to GPT-4o with a prompt to extract all headlines, provide a 1-2 sentence summary for each, and describe headline images and other sections.
- The summary is saved as `{identifier}_summary.txt` in the current directory.

---

### EXPECTED OUTPUT

- For each newspaper, a file named `{identifier}_summary.txt` will be created in the current directory.
- The file contains a list of headlines and summaries, formatted as `headline:summary` or `image:caption`, with no markdown or formatting marks.

---

### EXPECTED ISSUES / BUGS

- If the Internet Archive item does not contain a `_jp2.zip` or `_images.zip` file, the script will skip that identifier.
- If the preview JPEG for the front page cannot be downloaded (e.g., missing or network error), the script will skip that identifier.
- If GPT-4o fails to return a valid summary, the output file may be empty or incomplete.
- The script does not handle rate limiting or API quota errors from OpenAI or Internet Archive.
- The script assumes the front page (`_0000`) contains the main headlines; newspapers with front matter on later pages will not be processed.
- The script does not retry failed downloads or API calls.
- The script does not validate the format of the returned summary beyond saving the output.
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

For bug reports or feature requests, contact the script author or maintainer.