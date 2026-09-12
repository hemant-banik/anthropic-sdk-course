## 📘 Step 4 — Message roles & multi-turn conversations

### Theory

Every call to `client.messages.create()` takes a `messages` list — each item
is a dict with a `role` (`"user"` or `"assistant"`) and `content`. The API
itself is **stateless**: it has no memory between calls. Multi-turn
conversation is just *you* re-sending the whole history each time, with the
latest assistant reply appended as a `"role": "assistant"` message before
you append the next user turn.

```python
messages = [{"role": "user", "content": "My name is Zara. Remember that."}]

first = client.messages.create(
    model="claude-opus-5",
    max_tokens=200,
    messages=messages,
)
print(first.content[0].text)

# Append the assistant's reply, then the next user turn, before calling again
messages.append({"role": "assistant", "content": first.content})
messages.append({"role": "user", "content": "What is my name?"})

second = client.messages.create(
    model="claude-opus-5",
    max_tokens=200,
    messages=messages,
)
print(second.content[0].text)
```

**Why append `first.content` (not `first.content[0].text`)?** The
`assistant` message you feed back in must match the *shape* the API itself
returns — a list of content blocks — not a plain string. Passing the raw
`response.content` list back in is the simplest way to guarantee that shape
stays correct, even for multi-block responses (e.g. later, tool use or
extended thinking add extra block types to that same list).

**When to use this:** Any chatbot, agent loop, or follow-up-question flow.
The context window is what the model actually "remembers" — if you truncate
or forget to include earlier turns, the model has no memory of them at all.

### 🏋️ Exercise

1. In this repo, create a new file at **`exercises/practice4_multiturn.py`**
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

   messages = [{"role": "user", "content": "My name is Zara. Remember that."}]

   first = client.messages.create(
       model="claude-opus-5",
       max_tokens=200,
       messages=messages,
   )
   print("Turn 1:", first.content[0].text)

   messages.append({"role": "assistant", "content": first.content})
   messages.append({"role": "user", "content": "What is my name?"})

   second = client.messages.create(
       model="claude-opus-5",
       max_tokens=200,
       messages=messages,
   )
   print("Turn 2:", second.content[0].text)

   messages.append({"role": "assistant", "content": second.content})
   print("Messages in list:", len(messages))
   ```

2. Run it locally to make sure it works:

   ```bash
   pip install anthropic python-dotenv
   python exercises/practice4_multiturn.py
   ```

   ✅ **What should happen:** `Turn 1:` prints a line acknowledging the name
   Zara. `Turn 2:` prints an answer that correctly says the name is **Zara**
   — even though you never repeated the name in the second question, Claude
   remembers it because the full history was resent. Finally `Messages in
   list: 4` prints (user, assistant, user, assistant).

3. Commit and push your file to `main`:

   ```bash
   git add exercises/practice4_multiturn.py
   git commit -m "Step 4: message roles and multi-turn conversation"
   git push
   ```

4. Watch the **Actions** tab. The **"Step 4 — Message Roles & Multi-turn"**
   check runs automatically. On success this issue closes and **Step 5**
   opens. If it fails, read the error in the Action's log, fix your file,
   and push again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice4_multiturn.py`.
- Make sure you append `first.content` (the list of content blocks), **not**
  `first.content[0].text` (a plain string) — the checker and the API both
  expect the assistant turn to be the same shape the API returned.
- If Turn 2 doesn't mention "Zara", make sure `messages` actually contains
  all four entries in order before the second `client.messages.create()`
  call — if you forgot to `.append()` before calling again, Claude never
  sees the earlier turn.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
