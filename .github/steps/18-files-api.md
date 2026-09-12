## 📘 Step 18 — Upload once, reference by ID

### Theory

Upload a file once, get a `file_id` back, and reference it in as many
`messages.create()` calls as you want — no more re-sending base64 on every
request.

```python
# Upload
with open("/path/to/document.pdf", "rb") as f:
    uploaded = client.files.upload(file=("document.pdf", f, "application/pdf"))

file_id = uploaded.id
print(file_id)   # "file_011CNha8iCJcU1wXNR6q4V8w"

# Reference it in a message — document block, using {"type": "file", "file_id": ...}
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Summarize this document."},
                {"type": "document", "source": {"type": "file", "file_id": file_id}},
            ],
        }
    ],
)

# Manage files
client.files.list()
client.files.retrieve_metadata(file_id)
client.files.delete(file_id)
```

Images use the same pattern with
`{"type": "image", "source": {"type": "file", "file_id": ...}}`. Limits:
500MB per file, 1TB per organization; Files API operations themselves are
free (you only pay input-token cost when the file content is actually used
in a Messages request).

**When to use this:** Any file you'll reference more than once — a
reference PDF for repeated Q&A, a logo image reused across many generation
calls, or datasets fed into the code execution tool (Step 19). Skips the
base64-encoding overhead and keeps request payloads small.

> **⚠️ Note on this project's gateway:** the Files API endpoints
> (`client.files.upload`, `.list`, `.retrieve_metadata`, `.delete`) are part
> of the standard `anthropic` SDK surface and are used exactly as documented
> above. If your gateway/base_url doesn't proxy the Files API the same way
> it proxies `messages.create()`, you may see a 404 or "not supported"
> error from `files.upload()` — if that happens, note it in your PR/issue
> comment and the checker will still validate your *code pattern* is
> correct (upload → get file_id → reference in a document block), even if
> the live call needs a direct `ANTHROPIC_API_KEY` fallback instead of the
> gateway. This is the one step where the closest available real pattern is
> used, per the course notes.

### 🏋️ Exercise

1. Create a new file at `exercises/practice18_files_api.py`.

2. Set up the client exactly like previous steps (`load_dotenv()`,
   `ICA_API_KEY`, `base_url=`).

3. Write a small local text file, upload it with `client.files.upload()`,
   and print its ID:

```python
with open("upload_notes.txt", "w") as f:
    f.write("Claude is an AI model made by Anthropic. It can read text, images, and PDFs.")

with open("upload_notes.txt", "rb") as f:
    uploaded = client.files.upload(file=("upload_notes.txt", f, "text/plain"))

print("file_id:", uploaded.id)
```

4. Reference `uploaded.id` in a `messages.create()` call using a
   `document` content block, and print Claude's summary:

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=200,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Summarize this document in one sentence."},
            {"type": "document", "source": {"type": "file", "file_id": uploaded.id}},
        ],
    }],
)
print("summary:", response.content[0].text)
```

✅ What should happen: you'll see a `file_id:` line starting with `file_`,
followed by a `summary:` line containing a one-sentence description that
reflects the uploaded file's content (mentioning Claude/Anthropic).

5. Run it with `python exercises/practice18_files_api.py`.

✅ What should happen: both lines print with no errors. This proves the
file was uploaded, referenced by ID (not re-pasted as text), and Claude
successfully read it.

6. Commit and push your file to `main`. The workflow will run the
   checker, comment on this issue, and open Step 19.

<details>
<summary>Having trouble?</summary>

- If `client.files.upload()` raises a 404 or "not supported" error on this
  project's gateway, that's a known limitation noted above — try again with
  a direct `anthropic.Anthropic()` client (no `base_url=` override) using
  your own `ANTHROPIC_API_KEY` if you have one, or ask in the course
  discussion for the current gateway status.
- If the `file_id:` line is missing, double check you printed
  `uploaded.id` (not `uploaded` itself).
- If `summary:` doesn't reflect the file content, make sure the
  `document` content block's `source` dict uses `"type": "file"` and
  `"file_id": uploaded.id` exactly — a typo here silently falls back to an
  empty/invalid reference.
- Keep `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in your client setup
  — the checker verifies your script still uses this project's real client
  pattern.

</details>
