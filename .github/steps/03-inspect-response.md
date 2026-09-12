## 📘 Step 3 — Inspect the full response object

### Theory

`messages.create()` doesn't just return text — it returns a `Message` object
with useful metadata:

```python
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Name one planet."}],
)
print("id:", message.id)
print("model:", message.model)
print("role:", message.role)
print("stop_reason:", message.stop_reason)
print("usage:", message.usage)
print("text:", message.content[0].text)
```

**What to expect:** `id` starts with `msg_`, `role` is `assistant`,
`stop_reason` is usually `end_turn`, and `usage` shows an object with
`input_tokens` and `output_tokens`.

### 🏋️ Exercise

1. Create **`exercises/practice_inspect.py`** with exactly this content:

   ```python
   from anthropic import Anthropic

   client = Anthropic()

   message = client.messages.create(
       model="claude-opus-5",
       max_tokens=100,
       messages=[{"role": "user", "content": "Name one planet."}],
   )
   print("id:", message.id)
   print("model:", message.model)
   print("role:", message.role)
   print("stop_reason:", message.stop_reason)
   print("usage:", message.usage)
   print("text:", message.content[0].text)
   ```

2. Run it locally:

   ```bash
   python exercises/practice_inspect.py
   ```

   ✅ **What should happen:** six lines print. `id` starts with `msg_`,
   `role` is `assistant`, `stop_reason` prints (usually `end_turn`), `usage`
   shows token counts, and `text` contains a planet name.

3. Commit and push:

   ```bash
   git add exercises/practice_inspect.py
   git commit -m "Step 3: inspect the response object"
   git push
   ```

4. The **"Step 3 — Inspect Response"** check runs automatically. On success
   this issue closes and you'll see the final **"🎉 Course complete"** issue
   open — you've completed this proof-of-concept course!

<details>
<summary>Having trouble?</summary>

- If `message.id` doesn't start with `msg_`, something's wrong with the
  response — check for typos in your field access (`message.id`, not
  `message["id"]` — this is an object, not a dict).
- Keep all six `print(...)` lines — the checker looks for each label
  (`id:`, `model:`, `role:`, `stop_reason:`, `usage:`, `text:`) in your
  script's output.

</details>
