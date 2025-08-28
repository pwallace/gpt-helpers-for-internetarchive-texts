#!/bin/python3

"""
--------------------------------------------------------------------------------
GPT-Summarizer: Automated Archival Transcript Summarizer
--------------------------------------------------------------------------------

DESCRIPTION:
This script batch-generates concise, neutral summaries for archival transcript files using OpenAI's GPT models. 
It is designed for archivists and librarians who need descriptive summaries for cataloging and finding aids.

HOW IT WORKS:
- Reads all `.txt` files from the `source` directory.
- For each transcript:
    - Loads the text and removes line breaks for better processing.
    - Splits the text into chunks based on the model's token limit.
    - Sends each chunk to GPT-3.5-turbo with a system prompt instructing the model to produce a neutral, professional summary.
    - Collects all chunk summaries, combines them, and sends the combined summary back to GPT for final revision.
    - Writes the final revised summary to the `output` directory, prefixed with `gpt_`.

PROMPT DESIGN:
- The system prompt instructs GPT to avoid value judgments, speculation, and sensitive information (e.g., emails, URLs).
- The summary should be under 200 words, focusing on succinctness, accuracy, readability, and completeness.

USAGE:
1. Place your transcript `.txt` files in the `source` directory.
2. Set your OpenAI API key as an environment variable: 
   export OPENAI_API_KEY="sk-..."
3. Install required Python packages:
   pip install openai tiktoken
4. Run the script:
   python gpt-summarizer.py
5. Summaries will be written to the `output` directory as `gpt_<original_filename>.txt`.

REQUIREMENTS:
- Python 3.7+
- Packages: openai, tiktoken
- OpenAI API key (set as environment variable OPENAI_API_KEY)

NOTES:
- The script uses GPT-3.5-turbo by default; you may change the model as needed.
- The script is designed for batch processing and will process all `.txt` files in the `source` directory.
- Summaries are revised for clarity and completeness before output.

--------------------------------------------------------------------------------
"""

import os
import tiktoken
import openai

client = openai.OpenAI(api_key="YOUR KEY")  # Replace with env var in production

# File setup
transcript_location = "source"
output_location = "output"

for transcript_file in os.listdir(transcript_location):
    if not transcript_file.endswith(".txt"):
        continue
    else:
        # Full path to the transcript file
        summary_outfile = os.path.join(output_location, "gpt_" + os.path.basename(transcript_file))
        # Full path to the source transcript file
        source_full_path = os.path.join(transcript_location, transcript_file)
        # Read the transcript file
        with open(source_full_path, "r") as f:
            long_text = f.read().replace("\n", " ")

        # Prompt setup
        system_content = (
            "You are an professional archivist creating descriptive summaries of archival documents for use in library catalogs and archival finding aids. Your job is neutral description not interpretation, so you avoid making any value judgments, inferences, or speculations. You never use racist or sexist language, even when the source text contains explicitly racist or sexist material.Describe and summarize the text in under 200 words; shorter responses are ok, and the goal should be a balance of succinctness, accuracy, readability, and completeness. NEVER include email addresses, phone numbers, or URLs."
        )

        global_content = (
            ""
        )

        # Tokenize
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoding.encode(long_text)
        system_tokens = encoding.encode(system_content)
        user_tokens = encoding.encode(global_content)

        max_tokens = 8192
        buffer_tokens = 500  # leave room for response
        chunk_size = max_tokens - len(system_tokens) - len(user_tokens) - buffer_tokens

        chunks = [
            encoding.decode(tokens[i:i + chunk_size])
            for i in range(0, len(tokens), chunk_size)
        ]

        # Prepare messages
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": global_content},
        ]

        responses = []

        for chunk in chunks:
            chunk_messages = messages + [{"role": "user", "content": chunk}]
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chunk_messages
            )
            summary = response.choices[0].message.content.strip()
            responses.append(summary)

# Combine summaries and write to output
        final_summary = "\n\n".join(responses)

        print("Summarized text for:", transcript_file)
        print("Revising summary...")
# Prepare revised messages for final summary
        revised_messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": final_summary},
        ]

        revised_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=revised_messages
        )
        revised_summary = revised_response.choices[0].message.content.strip()

    os.makedirs(output_location, exist_ok=True)
    with open(summary_outfile, "w") as f:
        f.write(revised_summary)

    print("DONE! Wrote summary to:", summary_outfile)
