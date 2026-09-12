## 📘 Step 21 — Bedrock and Vertex client variants (FINAL STEP)

Welcome to the final step of the course! This one is different from the
rest: you're not required to have AWS or GCP credentials. It's a
**conceptual/comparison** exercise about the SDK's cloud-partner client
variants.

### Theory

Same SDK, different backend — swap the client class when Claude is
deployed through a cloud partner instead of the direct Claude API.

```python
# AWS Bedrock
from anthropic import AnthropicBedrock

client = AnthropicBedrock(
    aws_access_key="<access key>",
    aws_secret_key="<secret key>",
    aws_region="us-west-2",
)
message = client.messages.create(
    model="global.anthropic.claude-opus-4-6-v1",   # note the AWS-flavored model ID
    max_tokens=256,
    messages=[{"role": "user", "content": "Hello, world"}],
)
```

```python
# Google Cloud Vertex / Agent Platform
from anthropic import AnthropicVertex

client = AnthropicVertex(project_id="MY_PROJECT_ID", region="global")
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hey Claude!"}],
)
```

`messages.create()` and friends work identically once the client is
constructed — same params, same response shape. What differs:
authentication (AWS creds/`boto3` session vs. `gcloud auth
application-default login`), model ID format (Bedrock prepends
`anthropic.` and sometimes a region prefix like `us.` or `global.`), and
feature parity (some newer features — e.g. server-side tools, Files API —
lag behind on partner platforms).

**When to use which:**
- **`Anthropic`** (direct) — the default choice for most projects; talks
  straight to the Anthropic API with an Anthropic API key.
- **`AnthropicBedrock`** — you already run infrastructure on AWS and want
  Claude billed/governed through your existing AWS account (IAM, VPC,
  compliance boundary) instead of a separate Anthropic API key
  relationship. Install with `pip install "anthropic[bedrock]"`.
- **`AnthropicVertex`** — same idea, but for Google Cloud: you want Claude
  billed/governed through an existing GCP project via Vertex AI, using
  `gcloud` application-default credentials instead of an Anthropic API
  key. Install with `pip install "anthropic[vertex]"`.

> **Note on assumptions:** this step does not make a live call to the
> direct Anthropic API through this project's usual `ICA_API_KEY` /
> gateway pattern — it's a static, text-based exercise. There's no
> "correct" live response to check because most learners won't have real
> AWS or GCP credentials. Instead, the checker verifies your script
> demonstrates both client constructions correctly and explains, in a
> comment, when you'd reach for each one.

### 🏋️ Exercise

1. Create a file called
   `exercises/practice21_bedrock_vertex.py` in this repo. It should:
   - Import `AnthropicBedrock` and `AnthropicVertex` from `anthropic`.
   - Construct one instance of each (fake/placeholder credentials are fine
     — building the client object never makes a network call).
   - Include a comment explaining when you'd use each one.

Example:

```python
from anthropic import AnthropicBedrock, AnthropicVertex

# --- AWS Bedrock ---
# Use AnthropicBedrock when your team already runs infrastructure on AWS
# and wants Claude usage billed/governed through that existing AWS account
# (IAM roles, VPC boundaries, AWS cost reporting) rather than a separate
# Anthropic API key. Auth comes from AWS credentials (access key/secret
# key or an IAM role), not an Anthropic API key.
bedrock_client = AnthropicBedrock(
    aws_access_key="fake-access-key-for-practice",
    aws_secret_key="fake-secret-key-for-practice",
    aws_region="us-west-2",
)

# --- Google Cloud Vertex AI ---
# Use AnthropicVertex when your team already runs infrastructure on GCP
# and wants Claude usage billed/governed through that existing GCP project
# via Vertex AI, using gcloud application-default credentials instead of
# an Anthropic API key.
vertex_client = AnthropicVertex(
    project_id="fake-project-for-practice",
    region="global",
)

print("Bedrock client:", type(bedrock_client).__name__)
print("Vertex client:", type(vertex_client).__name__)
print("Same .messages.create(...) call shape works on both — only the constructor differs.")
```

✅ **What should happen:** running the script prints the two client class
names with no errors (constructing these clients never talks to AWS/GCP —
that only happens on `.messages.create()`, which this exercise
deliberately skips since most learners won't have real cloud creds).

2. Run it locally to confirm it works:

```bash
python exercises/practice21_bedrock_vertex.py
```

✅ **What should happen:** two lines printing `AnthropicBedrock` and
`AnthropicVertex`, plus the reminder line — no exceptions, no network
calls.

3. Commit and push your file to the `main` branch:

```bash
git add exercises/practice21_bedrock_vertex.py
git commit -m "Complete step 21: Bedrock and Vertex client variants"
git push
```

✅ **What should happen:** pushing triggers the "Step 21 - Bedrock and
Vertex Clients" GitHub Actions workflow. A green checkmark closes this
issue and opens the final **🎉 Course complete!** issue — congratulations,
you'll have finished all 21 sections of the SDK reference!

<details>
<summary>Having trouble?</summary>

- This is the one step in the course with **no live API call required** —
  the checker only inspects your script's source text, it does not run
  it against a real endpoint.
- Make sure your script contains the literal class names `AnthropicBedrock`
  and `AnthropicVertex` (not just `Bedrock`/`Vertex` abbreviations).
- Make sure you have an actual explanatory comment (a `#` line) near each
  client construction — not just the import statement — describing when
  you'd pick that variant. The checker looks for a `#` comment containing
  words like "use" and "when" near each class name.
- You do NOT need real AWS or GCP credentials to complete this exercise —
  fake placeholder strings are correct and expected, since constructing a
  client object never makes a network call.

</details>
