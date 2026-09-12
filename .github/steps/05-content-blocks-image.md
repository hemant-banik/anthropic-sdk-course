## 📘 Step 5 — Content blocks: text + image input (base64)

### Theory

A message's `content` can be a plain string (shorthand for a single text
block) **or** a list of typed content block dicts. Mixing types — an image
plus a question, in the same turn — is the whole point of multimodal
messages. An image block looks like this:

```python
{
    "type": "image",
    "source": {
        "type": "base64",
        "media_type": "image/png",   # image/jpeg, image/png, image/gif, image/webp
        "data": "<base64-encoded-bytes>",
    },
}
```

Put it in the same `content` list alongside a `{"type": "text", "text": ...}`
block:

```python
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=200,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": "What color is this image? Answer in one word."},
        ],
    }],
)
```

**Why does image come before text?** Block **order matters** — Claude reads
top-to-bottom, so put images/documents *before* the text that asks about
them for the best results.

**When to use this:** Anytime you need to show Claude a picture — screenshots,
diagrams, photos, scanned documents — instead of only describing it in words.

### 🏋️ Exercise

1. Install `pillow` (used only to generate a tiny test image locally —
   it is **not** part of the `anthropic` SDK):

   ```bash
   pip install anthropic python-dotenv pillow
   ```

2. In this repo, create a new file at
   **`exercises/practice5_image.py`** with exactly this content:

   ```python
   import base64
   import os
   from io import BytesIO

   from dotenv import load_dotenv
   from PIL import Image
   from anthropic import Anthropic

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   client = Anthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )

   # Generate a small solid-red test image in memory (no file needed)
   img = Image.new("RGB", (100, 100), color="red")
   buffer = BytesIO()
   img.save(buffer, format="PNG")
   image_data = base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

   message = client.messages.create(
       model="claude-opus-5",
       max_tokens=200,
       messages=[{
           "role": "user",
           "content": [
               {
                   "type": "image",
                   "source": {
                       "type": "base64",
                       "media_type": "image/png",
                       "data": image_data,
                   },
               },
               {"type": "text", "text": "What color is this image? Answer in one word."},
           ],
       }],
   )
   print("color:", message.content[0].text)
   ```

3. Run it locally:

   ```bash
   python exercises/practice5_image.py
   ```

   ✅ **What should happen:** A line `color:` prints, followed by Claude's
   answer, which should contain the word **"red"** — confirming the base64
   image block was encoded and understood correctly.

4. Commit and push your file to `main`:

   ```bash
   git add exercises/practice5_image.py
   git commit -m "Step 5: content blocks - text and image input"
   git push
   ```

5. Watch the **Actions** tab. The **"Step 5 — Content Blocks & Image Input"**
   check runs automatically. On success this issue closes and **Step 6**
   opens. If it fails, read the error in the Action's log, fix your file,
   and push again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice5_image.py`.
- Make sure the image block comes **before** the text block in the
  `content` list — this matches the doc's recommended order.
- `media_type` must exactly match the format you saved with — `PNG` format
  pairs with `"image/png"`.
- Make sure you `base64.standard_b64encode(...).decode("utf-8")` — the API
  needs a plain string, not raw bytes.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
