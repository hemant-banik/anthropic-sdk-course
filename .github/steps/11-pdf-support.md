## 📘 Step 11 — PDF support

### Theory

PDFs use the same `document` content block that citations use, provided as
base64, a URL, or a Files API `file_id`. Claude treats a PDF as *both*
extracted text and page-images, so it can read charts and diagrams inside
it, not just raw text:

```python
import base64

with open("test_doc.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=200,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data,
                    },
                },
                {"type": "text", "text": "What is the secret code mentioned in this document?"},
            ],
        }
    ],
)
```

Block **order matters** — put the document block *before* the text that
asks about it, same as with images.

**When to use this:** Financial report analysis, legal document review,
"chat with a PDF" flows. For PDFs you'll reuse across many requests,
prefer uploading once via the Files API instead of re-sending base64 data
every time.

### 🏋️ Exercise

1. Make sure `reportlab` is installed (used only to generate a tiny test
   PDF locally — it's not part of the Anthropic SDK):

   ```bash
   pip install reportlab
   ```

2. In this repo, create a new file at **`exercises/practice11_pdf.py`**
   with exactly this content:

   ```python
   import base64
   import os

   from dotenv import load_dotenv
   from anthropic import Anthropic
   from reportlab.pdfgen import canvas

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   client = Anthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )

   # Generate a one-page PDF containing a made-up "secret code"
   pdf_path = "test_doc.pdf"
   c = canvas.Canvas(pdf_path)
   c.drawString(100, 700, "The secret code is 4471.")
   c.save()
   print("pdf created:", os.path.exists(pdf_path))

   with open(pdf_path, "rb") as f:
       pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

   response = client.messages.create(
       model="claude-opus-5",
       max_tokens=200,
       messages=[
           {
               "role": "user",
               "content": [
                   {
                       "type": "document",
                       "source": {
                           "type": "base64",
                           "media_type": "application/pdf",
                           "data": pdf_data,
                       },
                   },
                   {"type": "text", "text": "What is the secret code mentioned in this document? Reply with just the number."},
               ],
           }
       ],
   )
   answer = response.content[0].text
   print("answer:", answer)
   ```

3. Run it locally:

   ```bash
   pip install anthropic python-dotenv reportlab
   python exercises/practice11_pdf.py
   ```

   ✅ **What should happen:** `pdf created: True` prints, then `answer:`
   followed by Claude's reply containing `4471` — the code it read straight
   out of the PDF text.

4. Commit and push your file (you don't need to commit `test_doc.pdf`
   itself — it's generated fresh each run):

   ```bash
   git add exercises/practice11_pdf.py
   git commit -m "Step 11: PDF support"
   git push
   ```

5. Watch the **Actions** tab. The **"Step 11 — PDF Support"** check runs
   automatically. On success this issue closes and **Step 12** opens. If it
   fails, read the error in the Action's log, fix your file, and push
   again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice11_pdf.py`.
- If you get `ModuleNotFoundError: No module named 'reportlab'`, run
  `pip install reportlab`.
- The document content block needs `"type": "document"` with a `"source"`
  dict containing `"type": "base64"`, `"media_type": "application/pdf"`,
  and `"data"` — check every key is spelled exactly right.
- Put the document block **before** the text block in the `content` list,
  same ordering rule as images.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
