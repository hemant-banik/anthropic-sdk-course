## 📘 Step 20 — Web search tool (server-side)

### Theory

Like code execution, web search is a **server-side
tool** — Claude searches the live web itself and returns cited results,
all within one `messages.create()` call. No scraping code on your end.

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What's the weather in NYC right now?"}],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
)
print(response.content)   # includes server_tool_use, web_search_tool_result, and cited text blocks
```

Optional tool-definition fields:
- `max_uses` — cap how many searches Claude can make per request.
- `allowed_domains` / `blocked_domains` — mutually exclusive allow/deny lists.
- `user_location` — localize results by city/region/country/timezone.

```python
tools = [{
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": ["wikipedia.org"],
    "user_location": {"type": "approximate", "city": "San Francisco", "country": "US"},
}]
```

Every search result carries `encrypted_content` — pass it back
**unmodified** on later turns to preserve multi-turn search context.
Priced at **$10 per 1,000 searches**, on top of the normal token cost of
ingested results.

**When to use this:** Current events, live prices/scores/stats, anything
about a person/company/product that could have changed since training —
basically "Claude, go check the internet" moments. Always ships with
citations built in.

⚠️ **Exact type string matters.** The reference doc for this SDK version
specifies `"type": "web_search_20250305"` — copy it exactly. A typo (like
`web_search_20305`) causes a validation error, not a silent failure.

### 🏋️ Exercise

1. Create a file called `exercises/practice20_web_search.py` in
   this repo with the following content:

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
    max_tokens=1024,
    messages=[{"role": "user", "content": "Use web search to tell me who Claude Shannon was, in one or two sentences."}],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 3}],
)

block_types = [block.type for block in response.content]
print("block_types:", block_types)

for block in response.content:
    if block.type == "text":
        print("answer:", block.text)
```

✅ **What should happen:** the script prints a `block_types:` line
showing a mix of tool/result block types (something like
`['server_tool_use', 'web_search_tool_result', 'text']`), followed by an
`answer:` line where Claude explains who Claude Shannon was (the "father
of information theory").

2. Run it locally to confirm it works:

```bash
python exercises/practice20_web_search.py
```

✅ **What should happen:** no errors, `block_types:` lists at least one
tool-related block type plus `text`, and the answer mentions Shannon /
information theory.

3. Commit and push your file to the `main` branch:

```bash
git add exercises/practice20_web_search.py
git commit -m "Complete step 20: web search tool"
git push
```

✅ **What should happen:** pushing triggers the "Step 20 - Web Search
Tool" GitHub Actions workflow. Watch the **Actions** tab — a green
checkmark means this issue will auto-close and Step 21 (the final step!)
will open automatically.

<details>
<summary>Having trouble?</summary>

- Double-check the tool type string is exactly `web_search_20250305` — a
  single-digit typo (like `web_search_20305`) triggers a validation error
  from the API rather than a graceful fallback.
- If `block_types` only shows `['text']` with no tool blocks, Claude may
  have decided it already knew the answer without searching — try making
  the prompt more explicitly time-sensitive or explicitly say "search the
  web" to nudge it toward using the tool.
- Web search is billed per search ($10/1,000), separate from token costs
  — this exercise uses `max_uses: 3` to keep costs minimal.
- Keep `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in your client
  setup — the checker verifies your script still uses this project's real
  client pattern.

</details>
