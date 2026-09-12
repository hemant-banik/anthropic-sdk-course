## 📘 Step 12 — Prompt caching

### Theory

If you send the same large system prompt or reference document on many
requests, prompt caching lets Claude skip re-processing it. Mark the block
you want cached with `"cache_control": {"type": "ephemeral"}`:

```python
long_context = "..." * 2000  # imagine a large document or system prompt

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=200,
    system=[
        {
            "type": "text",
            "text": long_context,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": "Summarize the above in one sentence."}],
)

usage = response.usage
print(usage.cache_creation_input_tokens, usage.cache_read_input_tokens)
```

The first request **writes** to the cache (`cache_creation_input_tokens` is
nonzero). A second, identical request within the cache's TTL (5 minutes by
default) **reads** from the cache instead (`cache_read_input_tokens` is
nonzero, and the request is cheaper/faster). Only blocks marked with
`cache_control` are cached — everything after the last cached block is
processed fresh each time.

**When to use this:** Long system prompts, large reference documents, big
few-shot example sets, or any content reused across many requests in a
short window — cut latency and cost by not reprocessing it every time.

### 🏋️ Exercise

1. In this repo, create a new file at **`exercises/practice12_caching.py`**
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

   # A long block of repeated text to make caching worthwhile.
   long_context = "The quick brown fox jumps over the lazy dog. " * 400

   system_blocks = [
       {
           "type": "text",
           "text": long_context,
           "cache_control": {"type": "ephemeral"},
       }
   ]

   # First call: writes to the cache.
   first = client.messages.create(
       model="claude-opus-5",
       max_tokens=100,
       system=system_blocks,
       messages=[{"role": "user", "content": "In one short sentence, what animal is mentioned above?"}],
   )
   print("first cache_creation_input_tokens:", first.usage.cache_creation_input_tokens)
   print("first cache_read_input_tokens:", first.usage.cache_read_input_tokens)

   # Second call with the identical cached block: reads from the cache.
   second = client.messages.create(
       model="claude-opus-5",
       max_tokens=100,
       system=system_blocks,
       messages=[{"role": "user", "content": "In one short sentence, what animal is mentioned above?"}],
   )
   print("second cache_creation_input_tokens:", second.usage.cache_creation_input_tokens)
   print("second cache_read_input_tokens:", second.usage.cache_read_input_tokens)
   ```

2. Run it locally:

   ```bash
   pip install anthropic python-dotenv
   python exercises/practice12_caching.py
   ```

   ✅ **What should happen:** The first call prints a nonzero
   `first cache_creation_input_tokens` (writing the cache). The second call
   prints a nonzero `second cache_read_input_tokens` (reading from the
   cache instead of reprocessing).

3. Commit and push your file to `main`:

   ```bash
   git add exercises/practice12_caching.py
   git commit -m "Step 12: prompt caching"
   git push
   ```

4. Watch the **Actions** tab. The **"Step 12 — Prompt Caching"** check runs
   automatically. On success this issue closes and **Step 13** (token
   counting) opens. If it fails, read the error in the Action's log, fix
   your file, and push again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice12_caching.py`.
- `cache_control` must be attached to the **system block dict itself**, not
  passed as a separate top-level argument.
- The two calls must use the **exact same** cached content — even a single
  character difference invalidates the cache and both calls will show
  `cache_creation_input_tokens` instead of a cache read on the second call.
- Caches expire after a few minutes of inactivity — if you're debugging by
  running the script slowly line-by-line, run it as a whole script instead.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
