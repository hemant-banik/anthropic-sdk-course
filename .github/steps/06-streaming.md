## 📘 Step 6 — Streaming responses

### Theory

`client.messages.create()` waits for the *entire* reply before returning
anything. For long answers that feels slow. `client.messages.stream()`
instead opens a streaming connection and hands you text chunks as Claude
generates them — use it as a context manager:

```python
with client.messages.stream(
    model="claude-opus-5",
    max_tokens=300,
    messages=[{"role": "user", "content": "Count from 1 to 5."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

    final_message = stream.get_final_message()
```

`stream.text_stream` yields plain-text chunks (skipping non-text event
plumbing) as they arrive — perfect for printing incrementally. After the
`with` block finishes (or via `stream.get_final_message()` inside it), you
can still access the complete assembled `Message` object, exactly like the
one `messages.create()` returns — same `.content`, `.usage`, `.stop_reason`.

**When to use this:** Chat UIs, CLIs, or any place a user is watching output
appear live rather than waiting on a spinner.

### 🏋️ Exercise

1. In this repo, create a new file at **`exercises/practice6_streaming.py`**
   with exactly this content:

   ```python
   import os
   from dotenv import load_dotenv
   from anthropic import Anthropic

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   client = Anthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )

   print("streaming:")
   full_text = ""
   with client.messages.stream(
       model="claude-opus-5",
       max_tokens=300,
       messages=[{"role": "user", "content": "Count from 1 to 5, one number per line."}],
   ) as stream:
       for text in stream.text_stream:
           print(text, end="", flush=True)
           full_text += text

       final_message = stream.get_final_message()

   print()  # newline after the streamed text
   print("stop_reason:", final_message.stop_reason)
   print("chars streamed:", len(full_text))
   ```

2. Run it locally:

   ```bash
   pip install anthropic python-dotenv
   python exercises/practice6_streaming.py
   ```

   ✅ **What should happen:** A `streaming:` line prints, then you see the
   count from 1 to 5 appear (each chunk printed as it arrives, no single
   giant block). Afterwards `stop_reason: end_turn` prints, followed by
   `chars streamed:` with a number greater than 0.

3. Commit and push your file to `main`:

   ```bash
   git add exercises/practice6_streaming.py
   git commit -m "Step 6: streaming responses"
   git push
   ```

4. Watch the **Actions** tab. The **"Step 6 — Streaming Responses"** check
   runs automatically. On success this issue closes and **Step 7** opens.
   If it fails, read the error in the Action's log, fix your file, and push
   again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice6_streaming.py`.
- Make sure you use `client.messages.stream(...)` (not `.create(...)`) as a
  **context manager** (`with ... as stream:`) — iterating `.text_stream`
  outside the `with` block will raise an error.
- `stream.get_final_message()` must be called **inside** the `with` block,
  before the connection closes.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
