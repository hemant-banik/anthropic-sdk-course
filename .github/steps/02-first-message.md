## 📘 Step 2 — Your first `messages.create()` call

### Theory

`messages.create()` is *the* call — every text generation, tool use, vision
request, and thinking request goes through it. The three **required**
parameters are:

| Parameter | Type | What it does |
|---|---|---|
| `model` | `str` | Which model to hit, e.g. `"claude-opus-5"` |
| `messages` | `list[dict]` | The conversation so far (user/assistant turns) |
| `max_tokens` | `int` | Hard ceiling on tokens Claude can generate this turn |

```python
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "What is 2 + 2?"}],
)
print(message.content[0].text)
```

**When to use this:** This is your bread-and-butter call for any
non-streaming, single-shot request.

### 🏋️ Exercise

1. Create **`exercises/practice_message.py`** with exactly this content:

   ```python
   from anthropic import Anthropic

   client = Anthropic()

   message = client.messages.create(
       model="claude-opus-5",
       max_tokens=100,
       messages=[{"role": "user", "content": "What is 2 + 2?"}],
   )
   print(message.content[0].text)
   ```

2. Run it locally:

   ```bash
   python exercises/practice_message.py
   ```

   ✅ **What should happen:** a short answer containing "4" prints. Notice
   this call only used the three required params: `model`, `max_tokens`,
   `messages`.

3. Commit and push:

   ```bash
   git add exercises/practice_message.py
   git commit -m "Step 2: first messages.create call"
   git push
   ```

4. The **"Step 2 — First Message"** check will run automatically. On success
   this issue closes and **Step 3** opens.

<details>
<summary>Having trouble?</summary>

- If you get a `TypeError` about a missing argument, double check you kept
  all three required params (`model`, `max_tokens`, `messages`).
- If you get an `AuthenticationError`, your `ANTHROPIC_API_KEY` secret is
  missing or wrong — check Settings → Secrets and variables → Actions.
- The grading check literally re-runs your script and reads what it prints
  to confirm a real reply came back — it's not just checking the file
  exists.

</details>
