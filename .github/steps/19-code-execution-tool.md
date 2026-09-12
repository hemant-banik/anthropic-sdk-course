## 📘 Step 19 — Code execution tool (server-side sandbox)

### Theory

The code execution tool lets Claude write and run
**real Python code** inside an Anthropic-managed sandbox — no code runs on
your machine, and you get the actual results (not a guess) back in the
same response.

A server-side tool is different from a client-side tool (like the
`custom` function tools from earlier steps): Claude doesn't ask *you* to
run anything. Instead, Anthropic's infrastructure runs the code and feeds
the result straight back into Claude's reasoning, all within one
`messages.create()` call.

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Use code execution to find the mean and stdev of [1,2,3,4,5,6,7,8,9,10]"}
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

The response interleaves `server_tool_use` blocks (what Claude ran) with
`bash_code_execution_tool_result` / `text_editor_code_execution_tool_result`
blocks (what happened), plus a top-level `response.container.id` you can
reuse across requests to persist files and variables in the same sandbox.

**Sandbox specs:** Python 3.11, Linux/x86_64, 5 GiB RAM, no internet
access, pandas/numpy/matplotlib/scipy/pillow etc. pre-installed. Billed by
execution time (1,550 free hours/month per org, then $0.05/hour) — and
it's free entirely when paired with the web search or web fetch tools.

**When to use this:** Data analysis, chart generation, precise math Claude
shouldn't "guess" at, file format conversions — anything where you want
Claude to actually *run* code rather than just describe what code would do.

⚠️ **Exact type string matters.** The reference doc for this SDK version
specifies `"type": "code_execution_20250825"` — copy it exactly. A stale
or misspelled version string will be rejected by the API.

### 🏋️ Exercise

1. Create a file called `exercises/practice19_code_execution.py`
   in this repo with the following content:

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ICA_API_KEY"),
    base_url="https://api.servicesessentials.ibm.com",
)

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Use code execution to find the mean of [1,2,3,4,5,6,7,8,9,10]. State the mean clearly in your final sentence."}
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

for block in response.content:
    if block.type == "text":
        print("answer:", block.text)
```

✅ **What should happen:** the script prints one line starting with
`answer:` whose text clearly states the mean is `5.5` (Claude computed
this by actually running Python in the sandbox, not by guessing).

2. Run it locally to confirm it works:

```bash
python exercises/practice19_code_execution.py
```

✅ **What should happen:** no errors, and the printed answer mentions
`5.5` as the mean.

3. Commit and push your file to the `main` branch:

```bash
git add exercises/practice19_code_execution.py
git commit -m "Complete step 19: code execution tool"
git push
```

✅ **What should happen:** pushing triggers the "Step 19 - Code Execution
Tool" GitHub Actions workflow. Watch the **Actions** tab — a green
checkmark means this issue will auto-close and Step 20 will open
automatically.

<details>
<summary>Having trouble?</summary>

- If you see an error mentioning an unrecognized tool type, double-check
  you spelled `code_execution_20250825` exactly — no typos, no extra
  spaces, correct date suffix.
- If `response.content` has no `text` blocks, check for a
  `server_tool_use` or tool-result block instead — Claude sometimes
  returns tool activity before its final text summary; the loop above
  only prints `text` blocks, so make sure `max_tokens` is high enough
  (4096) for Claude to finish its explanation after running code.
- The sandbox has **no internet access** — this exercise doesn't need it,
  but don't expect `requests.get()`-style code inside code execution to
  work.
- Keep `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in your client
  setup — the checker verifies your script still uses this project's real
  client pattern.

</details>
