## 📘 Step 17 — Compare models: same call, different model string

### Theory

Model IDs follow the pattern `claude-{name}-{major}[-{minor}]`. Always check
[docs.claude.com/en/docs/about-claude/models/overview](https://docs.claude.com/en/docs/about-claude/models/overview)
for the live table since names/pricing change.

| Family | Example model ID | Best for |
|---|---|---|
| Opus | `claude-opus-5` | Complex agentic coding, enterprise-grade reasoning |
| Sonnet | `claude-sonnet-5` | Best balance of speed and intelligence — default workhorse |
| Haiku | `claude-haiku-4-5` | Fastest, near-frontier intelligence, cost-sensitive high-volume tasks |

Swapping models is just a string change:

```python
message = client.messages.create(
    model="claude-sonnet-5",   # <- just a string, swap freely
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hi"}],
)
```

**When to use this:** Pick Opus when quality/reasoning depth matters most and
cost is secondary; Sonnet for the default "just build the thing" choice;
Haiku for high-throughput, latency-sensitive, or budget-constrained
workloads. Model IDs are **pinned** — the underlying model behind a given ID
never silently changes, so upgrading is always an explicit code change.

### 🏋️ Exercise

1. Create a new file at `exercises/practice17_models_available.py`.

2. Set up the client exactly like previous steps (`load_dotenv()`,
`ICA_API_KEY`, `base_url=`).

3. Loop over at least 2-3 different model name strings — for example
`"claude-opus-5"`, `"claude-sonnet-5"`, `"claude-haiku-4-5"` — and for each
one call `client.messages.create()` with the same prompt (e.g. "In one
sentence, what is your name/model family?"). Print two labeled lines per
model:

```python
print("model:", message.model)
print("stop_reason:", message.stop_reason)
```

Your full loop should look like this:

```python
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ["ICA_API_KEY"],
    base_url="https://api.servicesessentials.ibm.com",
)

prompt = "In one sentence, what is your name/model family?"

for model_name in ["claude-opus-5", "claude-sonnet-5", "claude-haiku-4-5"]:
    message = client.messages.create(
        model=model_name,
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    print("model:", message.model)
    print("stop_reason:", message.stop_reason)
```

✅ What should happen: for each model in your loop, you get one `model:` line
and one `stop_reason:` line — six lines total for three models. The `model:`
values should differ across lines (proving you actually hit different
models, not the same one three times), and `stop_reason` will almost always
be `end_turn` for a short, complete answer.

4. Run it with `python exercises/practice17_models_available.py`.

✅ What should happen: all model calls succeed with no errors, and you can
visually compare which model IDs came back. This is the exact defensive
pattern real apps use before committing to a specific model in production.

5. Commit and push your file to `main`. The workflow will run the
   checker, verify at least two distinct models were used, comment on this
   issue, and open Step 18.

<details>
<summary>Having trouble?</summary>

- If the checker says "expected 2 lines starting with 'model:'", make sure
  you print the label exactly as `model:` (lowercase, colon, one space) —
  the checker parses stdout with a regex looking for that exact prefix.
- If it says "expected 2 DIFFERENT model names", double check you're not
  accidentally calling the same model string in every loop iteration.
- If a model name causes an error, verify the spelling matches the table
  above exactly — model strings are case-sensitive and don't tolerate typos.
- Keep `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in your client setup
  — the checker verifies your script still uses this project's real client
  pattern.

</details>
