## 📘 Step 8 — Tool use

### Theory

Tool use lets Claude call functions *you* define. You describe each tool
with a JSON Schema, Claude decides when to use one, replies with a
`tool_use` content block instead of (or alongside) text, and you send the
result back so Claude can finish its answer. One round-trip looks like:

```python
tools = [{
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "City name"}},
        "required": ["city"],
    },
}]

message = client.messages.create(
    model="claude-opus-5",
    max_tokens=300,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
)

if message.stop_reason == "tool_use":
    tool_use_block = next(b for b in message.content if b.type == "tool_use")
    # Run your real function here — this example hardcodes a result.
    result = "18°C, partly cloudy"

    follow_up = client.messages.create(
        model="claude-opus-5",
        max_tokens=300,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in Paris?"},
            {"role": "assistant", "content": message.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": result,
                }],
            },
        ],
    )
    print(follow_up.content[0].text)
```

Key pieces: `tool_use_block.name`, `tool_use_block.input` (a dict matching
your schema) tell you *what* Claude wants to call and *with what
arguments*. The `tool_result` block's `tool_use_id` **must match** the
`tool_use` block's `id` so Claude knows which call the result answers.

### 🏋️ Exercise

1. In this repo, create a new file at **`exercises/practice8_tools.py`**
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

   tools = [{
       "name": "get_weather",
       "description": "Get the current weather for a city.",
       "input_schema": {
           "type": "object",
           "properties": {"city": {"type": "string", "description": "City name"}},
           "required": ["city"],
       },
   }]

   user_question = "What's the weather in Paris?"

   message = client.messages.create(
       model="claude-opus-5",
       max_tokens=300,
       tools=tools,
       messages=[{"role": "user", "content": user_question}],
   )

   print("stop_reason:", message.stop_reason)

   if message.stop_reason == "tool_use":
       tool_use_block = next(b for b in message.content if b.type == "tool_use")
       print("tool name:", tool_use_block.name)
       print("tool input:", tool_use_block.input)

       # A real integration would call a weather API here. We hardcode a result.
       result = "18°C, partly cloudy"

       follow_up = client.messages.create(
           model="claude-opus-5",
           max_tokens=300,
           tools=tools,
           messages=[
               {"role": "user", "content": user_question},
               {"role": "assistant", "content": message.content},
               {
                   "role": "user",
                   "content": [{
                       "type": "tool_result",
                       "tool_use_id": tool_use_block.id,
                       "content": result,
                   }],
               },
           ],
       )
       print("final answer:", follow_up.content[0].text)
   ```

2. Run it locally:

   ```bash
   pip install anthropic python-dotenv
   python exercises/practice8_tools.py
   ```

   ✅ **What should happen:** `stop_reason: tool_use` prints, followed by
   `tool name: get_weather` and `tool input:` showing a dict with a `city`
   key. Then `final answer:` prints Claude's reply incorporating the
   `18°C, partly cloudy` result you supplied.

3. Commit and push your file to `main`:

   ```bash
   git add exercises/practice8_tools.py
   git commit -m "Step 8: tool use"
   git push
   ```

4. Watch the **Actions** tab. The **"Step 8 — Tool Use"** check runs
   automatically. On success this issue closes and **Step 9** opens. If it
   fails, read the error in the Action's log, fix your file, and push
   again.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice8_tools.py`.
- If `stop_reason` isn't `tool_use`, Claude decided not to call the tool —
  make sure the `user_question` is clearly about weather so Claude has a
  reason to use `get_weather`.
- The `tool_use_id` in your `tool_result` block **must exactly match** the
  `id` attribute of the `tool_use` block Claude returned — copy it from
  `tool_use_block.id`, don't hardcode a string.
- The second `messages.create()` call must include the **same `tools=`**
  list you passed the first time.
- The checker looks for `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in
  your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure it's set as
  a repo secret (Settings → Secrets and variables → Actions).

</details>
