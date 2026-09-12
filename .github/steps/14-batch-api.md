## 📘 Step 14 — Batch API: create, poll, retrieve results

### Theory

The Message Batches API processes many requests asynchronously at 50% of
standard pricing, with most batches finishing in minutes (hard cap: 24
hours). Same client setup as every previous step:

```python
import os, time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

client = Anthropic(
    api_key=config["ICA_API_KEY"],
    base_url="https://api.servicesessentials.ibm.com",
)

# 1. Create a batch of independent requests, each with a unique custom_id
message_batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-opus-5",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "Hello, world"}],
            },
        },
    ]
)
print(message_batch.id, message_batch.processing_status)   # in_progress

# 2. Poll for completion with a short, bounded loop (batches usually finish
#    within minutes — no need for a long-running `while True: sleep(60)`)
for attempt in range(30):
    batch = client.messages.batches.retrieve(message_batch.id)
    if batch.processing_status == "ended":
        break
    time.sleep(10)

# 3. Stream results (memory-efficient, one result at a time)
for result in client.messages.batches.results(message_batch.id):
    if result.result.type == "succeeded":
        print(result.custom_id, "->", result.result.message.content[0].text)
    elif result.result.type == "errored":
        print(result.custom_id, "failed:", result.result.error)
```

Limits: 100,000 requests or 256MB per batch. Results are downloadable for 29
days. `max_tokens: 0` and `stream: true` are **not** supported inside a
batch request.

**What to expect:** the batch ID starts with `msgbatch_`, its status is
`in_progress` right away, then transitions to `ended` once processing
finishes. Results are matched back to your requests by `custom_id` — order
isn't guaranteed.

**When to use this:** bulk content generation, large-scale evals, offline
document processing, content moderation sweeps — anything where you don't
need an answer in real time and can wait for a big cost discount.

### 🏋️ Exercise

1. Create **`exercises/practice14_batch_api.py`** with exactly this
   content:

   ```python
   import os
   import time
   from dotenv import load_dotenv
   from anthropic import Anthropic

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   client = Anthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )

   message_batch = client.messages.batches.create(requests=[
       {
           "custom_id": "capital-question",
           "params": {
               "model": "claude-opus-5",
               "max_tokens": 50,
               "messages": [{"role": "user", "content": "What is the capital of France? One word."}],
           },
       },
       {
           "custom_id": "math-question",
           "params": {
               "model": "claude-opus-5",
               "max_tokens": 50,
               "messages": [{"role": "user", "content": "What is 7 times 6? Just the number."}],
           },
       },
   ])
   print("batch_id:", message_batch.id)
   print("initial_status:", message_batch.processing_status)

   # Short, bounded polling loop — batches usually finish within minutes
   for attempt in range(30):
       batch = client.messages.batches.retrieve(message_batch.id)
       print(f"poll_attempt_{attempt + 1}:", batch.processing_status)
       if batch.processing_status == "ended":
           break
       time.sleep(10)

   succeeded, errored = 0, 0
   for result in client.messages.batches.results(message_batch.id):
       if result.result.type == "succeeded":
           succeeded += 1
           print(result.custom_id, "SUCCEEDED ->", result.result.message.content[0].text)
       elif result.result.type == "errored":
           errored += 1
           print(result.custom_id, "ERRORED ->", result.result.error)

   print("succeeded:", succeeded)
   print("errored:", errored)
   ```

   ✅ **What should happen:** nothing yet — you're just creating the file.

2. Run it locally (make sure `.env` still has your `ICA_API_KEY`):

   ```bash
   python exercises/practice14_batch_api.py
   ```

   ✅ **What should happen:** `batch_id:` prints an ID starting with
   `msgbatch_`, `initial_status:` usually prints `in_progress`, several
   `poll_attempt_N:` lines print while the batch finishes, and finally you
   see both `capital-question SUCCEEDED -> ...` and `math-question
   SUCCEEDED -> ...` lines, ending with `succeeded: 2` and `errored: 0`.
   This can take a few minutes — that's expected for an async batch job.

3. Commit and push:

   ```bash
   git add exercises/practice14_batch_api.py
   git commit -m "Step 14: batch API - create, poll, retrieve results"
   git push
   ```

4. The **"Step 14 - Batch API"** check runs automatically. On success this
   issue closes and **Step 15** (Async client) opens automatically.

<details>
<summary>Having trouble?</summary>

- The polling loop is intentionally *bounded* (30 attempts × 10s = 5
  minutes max) rather than an unbounded `while True` — this keeps both
  your local run and the CI check from hanging forever if something goes
  wrong.
- Results come back matched by `custom_id`, not in submission order — that
  is why each request needs a unique `custom_id` and why you should match
  on it rather than assuming array order.
- If `errored:` is greater than 0, double-check both requests' `params`
  match the shape shown above exactly (valid `model`, non-zero
  `max_tokens`, a `messages` list).
- Keep `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in your client setup
  — the checker verifies your script still uses this project's real client
  pattern, not the plain `Anthropic()` default.
- CI runners can be slow — the checker gives the script several minutes to
  finish polling before timing out.

</details>
