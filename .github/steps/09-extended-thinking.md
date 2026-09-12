## 📘 Step 9 — Extended thinking

### Theory

Extended thinking lets Claude reason step-by-step in a separate `thinking`
content block before writing its final answer — useful for math, logic, and
multi-step planning. Enable it with the `thinking` parameter and a
`budget_tokens` (how many tokens Claude may spend thinking):

```python
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=2000,
    thinking={"type": "enabled", "budget_tokens": 1024},
    messages=[{"role": "user", "content": "What is 27 * 34? Think it through."}],
)

for block in message.content:
    if block.type == "thinking":
        print("thinking:", block.thinking[:200])
    elif block.type == "text":
        print("answer:", block.text)
```

Rules to know: `budget_tokens` must be **less than** `max_tokens` (the
thinking budget is a subset of the total token budget), and Claude's
response can contain **both** a `thinking` block and a `text` block — you
must check `block.type` to tell them apart when iterating `message.content`.
Thinking blocks also have a `signature` field for verification but that's
out of scope here.

**When to use this:** Hard reasoning tasks where you want visibility into
*how* Claude got its answer, or where letting it "think out loud" first
measurably improves final-answer quality.

### 🏋️ Exercise

1. In this repo, create a new file at
   **`exercises/practice9_thinking.py`** with exactly this content:

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

   message = client.messages.create(
       model="claude-opus-5",
       max_tokens=2000,
       thinking={"type": "enabled", "budget_tokens": 1024},
       messages=[{"role": "user", "content": "What is 27 * 34? Think it through step by step."}],
   )

   thinking_text = ""
   answer_text = ""
   for block in message.content:
       if block.type == "thinking":
           thinking_text = block.thinking
       elif block.type == "text":
           answer_text = block.text

   print("has thinking block:", bool(thinking_text))
   print("thinking length:", len(thinking_text))
   print("answer:", answer_text)
   ```

2. Run it locally:

   ```bash
   pip install anthropic python-dotenv
   python exercises/practice9_thinking.py
   ```

   ✅ **What should happen:** `has thinking block: True` prints, followed by
   `thinking length:` with a number greater than 0, and `answer:` with
   Claude's final reply containing the correct product, `918`.

3. Commit and push your file to `main`:

   ```bash
   git add exercises/practice9_thinking.py
   git commit -m "Step 9: extended thinking"
   git push
   ```

4. Watch the **Actions** tab. The **"Step 9 — Extended Thinking"** check
   runs automatically. On success this issue closes and **Step 10** opens.
   If it fails, read the error in the Action's log, fix your file, and push
   again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice9_thinking.py`.
- `budget_tokens` must be **strictly less than** `max_tokens` — if you get a
  400 error about token budgets, raise `max_tokens` or lower `budget_tokens`.
- Remember `message.content` is a **list of blocks** — you must loop over it
  and check `block.type` (`"thinking"` vs `"text"`); don't assume index `0`
  is always the text block when thinking is enabled.
- If `answer:` doesn't contain `918`, try rerunning — extended thinking
  greatly reduces arithmetic mistakes but ensure your prompt still asks for
  the multiplication clearly.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
