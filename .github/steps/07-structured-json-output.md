## 📘 Step 7 — Structured / JSON output

### Theory

The Messages API has no dedicated "JSON mode" — instead you **ask Claude in
the prompt** to reply with JSON only, then parse the text yourself with
Python's `json` module. Two things make this reliable:

1. Be explicit and specific in the instruction ("Respond with ONLY a JSON
   object, no other text, no markdown code fences").
2. Give Claude the exact shape you want, e.g. by showing field names.

```python
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=200,
    messages=[{
        "role": "user",
        "content": (
            "Respond with ONLY a JSON object (no markdown, no extra text) "
            "describing a fictional person with fields 'name' (string) and "
            "'age' (integer)."
        ),
    }],
)
raw_text = message.content[0].text
import json
data = json.loads(raw_text)
print(data["name"], data["age"])
```

**Why this can still fail:** Claude sometimes wraps JSON in ```` ```json ````
fences even when told not to. A common defensive trick is to strip fence
markers before parsing:

```python
cleaned = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
data = json.loads(cleaned)
```

**When to use this:** Any time your code needs to consume Claude's answer
programmatically (populate a form, feed another API, save to a database)
rather than just display it to a human.

### 🏋️ Exercise

1. In this repo, create a new file at
   **`exercises/practice7_json.py`** with exactly this content:

   ```python
   import json
   import os
   from dotenv import load_dotenv
   from anthropic import Anthropic

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   client = Anthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )

   message = client.messages.create(
       model="claude-opus-5",
       max_tokens=200,
       messages=[{
           "role": "user",
           "content": (
               "Respond with ONLY a JSON object (no markdown, no extra text) "
               "describing a fictional person with exactly two fields: "
               "'name' (string) and 'age' (integer)."
           ),
       }],
   )

   raw_text = message.content[0].text
   cleaned = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
   data = json.loads(cleaned)

   print("raw:", raw_text)
   print("parsed name:", data["name"])
   print("parsed age:", data["age"])
   print("age type:", type(data["age"]).__name__)
   ```

2. Run it locally:

   ```bash
   pip install anthropic python-dotenv
   python exercises/practice7_json.py
   ```

   ✅ **What should happen:** A `raw:` line prints Claude's raw text, then
   `parsed name:` and `parsed age:` print the extracted fields, and
   `age type: int` confirms `json.loads()` correctly typed the age as an
   integer (not a string).

3. Commit and push your file to `main`:

   ```bash
   git add exercises/practice7_json.py
   git commit -m "Step 7: structured JSON output"
   git push
   ```

4. Watch the **Actions** tab. The **"Step 7 — Structured JSON Output"**
   check runs automatically. On success this issue closes and **Step 8**
   opens. If it fails, read the error in the Action's log, fix your file,
   and push again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice7_json.py`.
- If `json.loads()` raises an error, print `raw_text` first to see exactly
  what Claude returned — it may still be wrapped in ```` ``` ```` fences the
  `.removeprefix()`/`.removesuffix()` calls didn't catch (they only strip
  from the very start/end of the string, so extra whitespace or newlines
  around the fences can trip this up — call `.strip()` again if needed).
- Make sure your prompt tells Claude the **exact field names** you expect
  (`name`, `age`) — vague prompts produce inconsistent JSON shapes.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
