## 📘 Step 15 — Async Client: `AsyncAnthropic`

### Theory

Every sync method has an async twin under `AsyncAnthropic`, with identical
parameters — just `await` the call. This project's client setup stays the
same, just with the async class and an `asyncio.run(main())` entry point:

```python
import os
import asyncio
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

load_dotenv()
config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

client = AsyncAnthropic(
    api_key=config["ICA_API_KEY"],
    base_url="https://api.servicesessentials.ibm.com",
)

async def main() -> None:
    message = await client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, Claude"}],
    )
    print(message.content[0].text)

asyncio.run(main())
```

**When to use this:** any FastAPI/async web service, or when you're firing
off many independent Claude calls concurrently (e.g. processing 50
documents at once) and don't want to block on each one sequentially.
Firing several requests with `asyncio.gather` lets them run concurrently,
so the whole batch finishes in roughly the time of ONE request instead of
N sequential ones.

### 🏋️ Exercise

1. Create **`exercises/practice15_async_client.py`** with exactly this
   content:

   ```python
   import os
   import asyncio
   from dotenv import load_dotenv
   from anthropic import AsyncAnthropic

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   client = AsyncAnthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )

   async def ask(question: str) -> str:
       message = await client.messages.create(
           model="claude-opus-5",
           max_tokens=50,
           messages=[{"role": "user", "content": question}],
       )
       return message.content[0].text

   async def main() -> None:
       results = await asyncio.gather(
           ask("What is the capital of Italy? One word."),
           ask("What is 9 times 9? Just the number."),
       )
       print("answer_1:", results[0])
       print("answer_2:", results[1])

   asyncio.run(main())
   ```

   ✅ **What should happen:** nothing yet — you're just creating the file.

2. Run it locally (make sure `.env` still has your `ICA_API_KEY`):

   ```bash
   python exercises/practice15_async_client.py
   ```

   ✅ **What should happen:** two printed lines, `answer_1: Rome` (or
   similar) and `answer_2: 81` — both requests ran concurrently via
   `asyncio.gather` rather than one after another.

3. Commit and push:

   ```bash
   git add exercises/practice15_async_client.py
   git commit -m "Step 15: async client with AsyncAnthropic"
   git push
   ```

4. The **"Step 15 - Async Client"** check runs automatically. On success
   this issue closes and **Step 16** (Error handling) opens automatically.

<details>
<summary>Having trouble?</summary>

- `AsyncAnthropic` methods must be awaited — forgetting `await` gives you a
  coroutine object instead of a real response, and `message.content` will
  fail with an `AttributeError`.
- `asyncio.run(main())` must wrap an `async def main()` — you can't `await`
  at the top level of a plain script outside a coroutine.
- If both answers seem to run one after another rather than concurrently,
  double check you used `asyncio.gather(...)` and not two separate
  sequential `await ask(...)` calls.
- Keep `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in your client setup
  — the checker verifies your script still uses this project's real client
  pattern, not the plain `AsyncAnthropic()` default.

</details>
