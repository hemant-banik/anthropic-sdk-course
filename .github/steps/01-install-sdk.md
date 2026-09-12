## 📘 Step 1 — Install the SDK & create a client

### Theory

The Anthropic Python SDK is one `pip install` away. You get a `client`
object and every API call hangs off of it.

```bash
pip install anthropic
```

**Option A — the SDK's default/direct pattern.** Good to know for general
SDK knowledge: this talks directly to Anthropic's own servers.

```python
import os
from anthropic import Anthropic

# Implicit: reads ANTHROPIC_API_KEY from the environment. This is the
# default, so you can omit api_key entirely.
client = Anthropic()

# Or explicit: pass the key yourself.
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
```

**Option B — this project's actual pattern.** This course routes requests
through a custom gateway (an IBM `base_url`) instead of Anthropic's default
endpoint, and loads the key from a local `.env` file via `python-dotenv`
instead of a bare shell env var. This is the pattern you'll actually use in
the exercises below:

```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()  # reads the .env file in the repo root into the environment
config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

client = Anthropic(
    api_key=config["ICA_API_KEY"],
    base_url="https://api.servicesessentials.ibm.com",
)
```

**Why `base_url`?** Passing `base_url=` points the SDK at a proxy/gateway
in front of Anthropic's API instead of hitting `api.anthropic.com` directly.
The SDK's request/response shapes stay identical — only the network
destination changes. This is common in organizations that route model
traffic through an internal gateway for logging, cost tracking, or access
control.

**When to use which:** Option A is what you'll see in most public docs and
tutorials. Option B is what this course (and this project) actually uses —
prefer it here since it matches the real setup you'll be checked against.

Requires **Python 3.10+**.

### 🏋️ Exercise

1. Create a `.env` file in the repo root (copy `.env.example` — it is
   already git-ignored, so it will never get committed) and put your real
   key in it:

   ```bash
   cp .env.example .env
   # then edit .env and set ICA_API_KEY=<your real key>
   ```

2. In this repo, create a new file at **`exercises/practice1.py`** with
   exactly this content:

   ```python
   import os
   import anthropic
   from dotenv import load_dotenv
   from anthropic import Anthropic

   load_dotenv()
   config = {"ICA_API_KEY": os.environ.get("ICA_API_KEY")}

   print("SDK version:", anthropic.__version__)

   client = Anthropic(
       api_key=config["ICA_API_KEY"],
       base_url="https://api.servicesessentials.ibm.com",
   )
   print("Client type:", type(client).__name__)
   ```

3. Run it locally to make sure it works:

   ```bash
   pip install anthropic python-dotenv
   python exercises/practice1.py
   ```

   ✅ **What should happen:** two lines print — `SDK version: 0.x.y` and
   `Client type: Anthropic`. No exceptions.

4. Commit and push your file to `main`:

   ```bash
   git add exercises/practice1.py
   git commit -m "Step 1: install SDK and create client"
   git push
   ```

   > Don't `git add .env` — it's already covered by `.gitignore` and should
   > never be committed. Only `.env.example` (with a placeholder value)
   > lives in the repo.

5. Watch the **Actions** tab. A check called **"Step 1 — Install SDK"** will
   run automatically. If it passes, this issue will close and **Step 2**
   will open within a few seconds. If it fails, read the error in the
   Action's log — fix your file and push again. You can retry as many times
   as you need.

<details>
<summary>Having trouble?</summary>

- Double-check the file path is exactly `exercises/practice1.py` (the
  checker looks for that exact path).
- If the check fails with an import error, confirm you didn't accidentally
  add a typo to `import anthropic` or forget `from dotenv import load_dotenv`.
- The checker looks for `load_dotenv()`, a reference to `ICA_API_KEY`, and a
  `base_url=` argument in your script — make sure all three are present.
- If the check fails complaining about `ICA_API_KEY`, make sure you added it
  as a repo secret (Settings → Secrets and variables → Actions) — the CI
  checker needs it too, not just your local `.env`.

</details>
