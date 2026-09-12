## 📘 Step 13 — Count tokens before you spend them

### Theory

`client.messages.count_tokens()` tells you exactly how many input tokens a
request *would* use — without generating any output and without spending
output tokens. Same request shape as `messages.create()`, minus
`max_tokens`. Same client setup as every previous step — load `.env`, read
`ICA_API_KEY`, point at the gateway `base_url`:

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

count = client.messages.count_tokens(
    model="claude-opus-5",
    messages=[{"role": "user", "content": "Hello, world"}],
)
print(count.input_tokens)   # e.g. 10
```

**What to expect:** a small integer — the exact input token count for that
message, with zero completion tokens spent, since `count_tokens` never
actually generates a response.

**When to use this:** budget-checking before an expensive request
(especially with big documents or long conversation history), trimming
context to fit a window, or estimating cost for a batch job before
submitting it. It's free and fast — always cheaper than discovering you
blew your context window mid-request.

### 🏋️ Exercise

1. Create **`exercises/practice13_token_counting.py`** with exactly this
   content:

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

   short_count = client.messages.count_tokens(
       model="claude-opus-5",
       messages=[{"role": "user", "content": "Hi"}],
   )
   long_count = client.messages.count_tokens(
       model="claude-opus-5",
       messages=[{
           "role": "user",
           "content": (
               "Please write a detailed, three-paragraph explanation of how "
               "photosynthesis works, including the role of chlorophyll and "
               "sunlight."
           ),
       }],
   )
   print("short_tokens:", short_count.input_tokens)
   print("long_tokens:", long_count.input_tokens)
   ```

   ✅ **What should happen:** nothing yet — you're just creating the file.

2. Run it locally (make sure `.env` still has your `ICA_API_KEY`):

   ```bash
   python exercises/practice13_token_counting.py
   ```

   ✅ **What should happen:** two lines print. `short_tokens` should be a
   small number (roughly 1–5), and `long_tokens` should be noticeably
   larger (several dozen) — confirming the count scales with text length.

3. Commit and push:

   ```bash
   git add exercises/practice13_token_counting.py
   git commit -m "Step 13: count tokens before sending a request"
   git push
   ```

4. The **"Step 13 - Token Counting"** check runs automatically. On success
   this issue closes and **Step 14** (Batch API) opens automatically.

<details>
<summary>Having trouble?</summary>

- `count_tokens()` takes the same `model=` and `messages=` shape as
  `messages.create()`, but **no** `max_tokens` — leaving it out (or adding
  it) shouldn't error, but the exercise above deliberately omits it since
  it isn't needed for counting.
- If `long_tokens` isn't bigger than `short_tokens`, double check you
  didn't swap the two message contents.
- Keep both `print("short_tokens": ...)` and `print("long_tokens": ...)`
  lines exactly as labeled — the checker looks for both labels in your
  script's stdout.
- Keep `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in your client setup
  — the checker verifies your script still uses this project's real client
  pattern, not the plain `Anthropic()` default.

</details>
