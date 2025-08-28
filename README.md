# GPT-supported Helper Scripts for Internet Archive texts

Two Python tools for extracting and summarizing content from digitized magazine and newspaper text files.  

Below is a description of each script and its usage.

---

## 1. GPT-magazine-ToC-finder

**Script:** `magazine-toc-describer.py`

**Purpose:**  
Automates the extraction and transcription of tables of contents (ToC) from digitized magazine issues hosted on the Internet Archive.  
For each issue, the script downloads the first magazine page preview image and uses GPT-4o to identify and transcribe the ToC.

**Process:**

- Reads a plaintext file containing one Internet Archive identifier per line.
- For each identifier:
    - Uses the Internet Archive metadata API to list files in the item.
    - Finds the `.jp2.zip` or `.images.zip` file and extracts the base filename.
    - Constructs the preview JPG URL for page `_0001`, then `_0002`, then `_0003` if needed.
    - Downloads the JPG.
    - Sends the JPG to GPT-4o for table of contents extraction.
    - If a valid table of contents is detected, outputs it as a hyphen-bulleted list with the header `TABLE OF CONTENTS` and saves it to `{identifier}_toc.txt`.
    - If no table of contents is detected after all attempts, prints a warning and does not create an output file.

**Usage:**

```bash
python magazine-toc-describer.py identifiers.txt
```

- `identifiers.txt`: Plaintext file with one Internet Archive identifier per line.

**Requirements:**

- OpenAI API key (set as environment variable `OPENAI_API_KEY`)
- Python libraries: `requests`, `Pillow`, `openai`, `base64`

**Typical Workflow:**

1. Prepare a text file listing the Internet Archive identifiers for your magazine issues.
2. Ensure your OpenAI API key is set in your environment.
3. Run the script to extract and transcribe tables of contents.
4. Review the `{identifier}_toc.txt` files for accuracy and completeness.

**Supporting Files:**

- `README-magazine-describer.md`: Additional documentation and tips.
- `SAMPLE-INPUT_middmag.txt`: Example input file (identifiers list).
- `SAMPLE-OUTPUT_middleburyNewspapers_Newsletter_1985_V59N03.txt`: Example output file.

---

## 2. GPT-newspaper-frontpage-describer

**Script:** `newspaper-frontpage-describer.py`

**Purpose:**  
Automates the extraction and summarization of front page articles from digitized newspaper issues hosted on the Internet Archive.  
For each issue, the script downloads the front page preview image and uses GPT-4o to generate a description and summary.

**Process:**

- Reads a plaintext file containing one Internet Archive identifier per line.
- For each identifier:
    - Uses the Internet Archive metadata API to list files in the item.
    - Finds the `.jp2.zip` or `.images.zip` file and extracts the base filename.
    - Constructs the preview JPG URL for the front page.
    - Downloads the JPG.
    - Sends the JPG to GPT-4o for description and summary.
    - Saves the summary to `{identifier}_summary.txt`.

**Usage:**

```bash
python newspaper-frontpage-describer.py identifiers.txt
```

- `identifiers.txt`: Plaintext file with one Internet Archive identifier per line.

**Requirements:**

- OpenAI API key (set as environment variable `OPENAI_API_KEY`)
- Python libraries: `requests`, `Pillow`, `openai`, `base64`

**Typical Workflow:**

1. Prepare a text file listing the Internet Archive identifiers for your newspaper issues.
2. Ensure your OpenAI API key is set in your environment.
3. Run the script to extract and summarize front page content.
4. Review the `{identifier}_summary.txt` files for clarity and completeness.

**Supporting Files:**

- `README-newspaper-frontpage-describer.md`: Additional documentation and tips.
- `SAMPLE-INPUT_campus-issues.txt`: Example input file (identifiers list).
- `SAMPLE-OUTPUT_middleburyNewspapers_2019-05-02.txt`: Example output file.

---

## General Notes

- Both scripts require **Python 3**.
- Input files should be plain text, UTF-8 encoded.
- Output files are written in plain text format.
- For best results, review the README files and comments in each script for additional options or configuration.

---

## Questions?

For help with a specific script, consult the README files or script comments for details.
