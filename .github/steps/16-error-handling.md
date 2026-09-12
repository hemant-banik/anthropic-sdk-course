## 📘 Step 16 — Error Handling: `APIError`, `RateLimitError`, `APIStatusError`

### Theory

Anthropic errors are subclasses of `anthropic.APIError`, split by HTTP
status code so you can branch on what actually happened:

| Status | Exception |
|---|---|
| 400 | `BadRequestError` |
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 422 | `UnprocessableEntityError` |
| 429 | `RateLimitError` |
| ≥500 | `InternalServerError` |
| N/A (network) | `APIConnectionError` |
| N/A (timeout) | `APITimeoutError` |

```python
import anthropic

try:
    message = client.messages.create(
        model="claude-opus-5", max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, Claude"}],
    )
except anthropic.APIConnectionError as e:
    print("Could not reach the server:", e.__cause__)
except anthropic.RateLimitError as e:
    print("429 — back off and retry later")
except anthropic.APIStatusError as e:
    print("Non-2xx response:", e.status_code, e.response)
```

**When to use this:** every production integration. Always at least catch
`RateLimitError` (back off) and `APIConnectionError` (transient network)
separately from `APIStatusError` (something's actually wrong with your
request). `NotFoundError` and `BadRequestError` are both subclasses of
`APIStatusError`, which is itself a subclass of `APIError` — so a broad
`except anthropic.APIError` catches everything the SDK can raise.

### 🏋️ Exercise

1. Create **`exercises/practice16_error_handling.py`** with exactly this
   content. It deliberately sends an invalid model name to trigger a real
   `NotFoundError` from the API, then catches it and prints the exception
   type and message:

   ```python
   import os
   import anthropic
   from dotenv import load_dotenv

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   client = anthropic.Anthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )

   try:
       client.messages.create(
           model="claude-does-not-exist-9000",
           max_tokens=100,
           messages=[{"role": "user", "content": "Hi"}],
       )
       print("No error was raised — this should not happen!")
   except anthropic.APIStatusError as e:
       print("error_type:", type(e).__name__)
       print("error_message:", str(e))
   ```

   ✅ **What should happen:** nothing yet — you're just creating the file.

2. Run it locally:

   ```bash
   python exercises/practice16_error_handling.py
   ```

   ✅ **What should happen:** two lines print — `error_type: NotFoundError`
   (a subclass of `APIStatusError`) and `error_message:` followed by the
   API's error text. No raw traceback should leak to your terminal —
   the `except` block caught it cleanly.

3. Commit and push:

   ```bash
   git add exercises/practice16_error_handling.py
   git commit -m "Step 16: error handling with APIStatusError"
   git push
   ```

4. The **"Step 16 - Error Handling"** check runs automatically. On success
   this issue closes and **Step 17** (Models available) opens
   automatically.

<details>
<summary>Having trouble?</summary>

- If nothing gets caught and you see `"No error was raised"`, double check
  the model string is actually invalid (`claude-does-not-exist-9000`) and
  that you didn't accidentally fix the typo.
- `anthropic.NotFoundError` is itself an `anthropic.APIStatusError`, which
  is itself an `anthropic.APIError` — catching the parent class is fine
  and is what this exercise does deliberately, since the exact status code
  a gateway returns for an unknown model can vary.
- If you get an `AuthenticationError` instead, your `ICA_API_KEY` isn't
  being loaded correctly — check your `.env` file and `load_dotenv()`.
- Keep `load_dotenv()`, `ICA_API_KEY`, and `base_url=` in your client setup
  — the checker verifies your script still uses this project's real client
  pattern.

</details>
