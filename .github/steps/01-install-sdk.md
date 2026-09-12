## 📘 Step 1 — Install the SDK & create a client

### Theory

The Anthropic Python SDK is one `pip install` away. You get a `client`
object and every API call hangs off of it.

```bash
pip install anthropic
```

```python
import os
from anthropic import Anthropic

# Option A — implicit: reads ANTHROPIC_API_KEY from the environment.
# This is the default, so you can omit api_key entirely.
client = Anthropic()

# Option B — explicit: pass the key yourself (e.g., pulled from a secrets manager)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
```

**When to use which:** Prefer the env var (`ANTHROPIC_API_KEY`) in real
projects so you never hardcode secrets in source. Pass `api_key=` explicitly
only when the key comes from something other than an env var (Vault, a
config service, multi-tenant key-per-user setups).

Requires **Python 3.10+**.

### 🏋️ Exercise

1. In this repo, create a new file at **`exercises/practice1.py`** with
   exactly this content:

   ```python
   import anthropic
   from anthropic import Anthropic

   print("SDK version:", anthropic.__version__)

   client = Anthropic()
   print("Client type:", type(client).__name__)
   ```

2. Run it locally to make sure it works:

   ```bash
   pip install anthropic
   export ANTHROPIC_API_KEY=sk-ant-...   # your real key
   python exercises/practice1.py
   ```

   ✅ **What should happen:** two lines print — `SDK version: 0.x.y` and
   `Client type: Anthropic`. No exceptions.

3. Commit and push your file to `main`:

   ```bash
   git add exercises/practice1.py
   git commit -m "Step 1: install SDK and create client"
   git push
   ```

4. Watch the **Actions** tab. A check called **"Step 1 — Install SDK"** will
   run automatically. If it passes, this issue will close and **Step 2**
   will open within a few seconds. If it fails, read the error in the
   Action's log — fix your file and push again. You can retry as many times
   as you need.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice1.py` (the
  checker looks for that exact path).
- If the check fails with an import error, confirm you didn't accidentally
  add a typo to `import anthropic`.
- If the check fails complaining about `ANTHROPIC_API_KEY`, make sure you
  added it as a repo secret (Settings → Secrets and variables → Actions) —
  the CI checker needs it too, not just your local shell.

</details>
