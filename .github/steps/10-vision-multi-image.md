## 📘 Step 10 — Vision: multiple images in one request

### Theory

You already sent one base64 image in Step 5. Claude can also compare
**multiple images in a single message** — just add more `image` content
blocks to the same `content` list, in the order you want Claude to consider
them:

```python
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image1_b64}},
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image2_b64}},
                {"type": "text", "text": "What color is the first image, and what color is the second?"},
            ],
        }
    ],
)
```

Claude sees the images in the order the blocks appear in `content`, so
mention "first image" / "second image" in your text block to disambiguate
which is which. This is how you'd build a "compare these two screenshots"
or "which of these products matches" feature.

**When to use this:** Comparing before/after images, matching a reference
photo against candidates, or asking Claude to reconcile info spread across
several images.

### 🏋️ Exercise

1. In this repo, create a new file at
   **`exercises/practice10_vision.py`** with exactly this content:

   ```python
   import base64
   import io
   import os

   from dotenv import load_dotenv
   from PIL import Image
   from anthropic import Anthropic

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   client = Anthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )


   def make_image_b64(color):
       img = Image.new("RGB", (32, 32), color=color)
       buf = io.BytesIO()
       img.save(buf, format="PNG")
       return base64.standard_b64encode(buf.getvalue()).decode("utf-8")


   image1_b64 = make_image_b64((220, 20, 20))   # red
   image2_b64 = make_image_b64((20, 80, 220))   # blue

   message = client.messages.create(
       model="claude-opus-5",
       max_tokens=300,
       messages=[
           {
               "role": "user",
               "content": [
                   {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image1_b64}},
                   {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image2_b64}},
                   {"type": "text", "text": "What color is the first image, and what color is the second? Answer in the form 'first: <color>, second: <color>'."},
               ],
           }
       ],
   )

   print("answer:", message.content[0].text)
   ```

2. Run it locally:

   ```bash
   pip install anthropic python-dotenv pillow
   python exercises/practice10_vision.py
   ```

   ✅ **What should happen:** An `answer:` line prints, mentioning **red**
   for the first image and **blue** for the second.

3. Commit and push your file to `main`:

   ```bash
   git add exercises/practice10_vision.py
   git commit -m "Step 10: vision with multiple images"
   git push
   ```

4. Watch the **Actions** tab. The **"Step 10 — Vision Multiple Images"**
   check runs automatically. On success this issue closes and **Step 11**
   opens. If it fails, read the error in the Action's log, fix your file,
   and push again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice10_vision.py`.
- Make sure both `image` content blocks come **before** the `text` block in
  the `content` list, and in the order red-then-blue — the checker expects
  Claude to say "first" = red and "second" = blue.
- If `pillow` isn't installed you'll get `ModuleNotFoundError: No module
  named 'PIL'` — install it with `pip install pillow`.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
