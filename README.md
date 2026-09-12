# Introduction to the Anthropic Python SDK

_A self-paced, GitHub-native course. Modeled on [github.com/skills](https://github.com/skills)._

In this course you'll learn the Anthropic Python SDK by actually using it —
one small exercise at a time, inside your own GitHub repo. A bot opens an
issue with a short lesson, you write a few lines of Python and push, and a
GitHub Action checks your work and unlocks the next issue. No videos, no
slides — just you, your editor, and real API calls.

**What you'll learn in this proof-of-concept (3 steps):**

1. Install the SDK and create an `Anthropic` client (env var vs explicit key).
2. Make your first `messages.create()` call.
3. Inspect the full response object (`id`, `model`, `stop_reason`, `usage`).

The full course (see [`COURSE-ARCHITECTURE.md`](COURSE-ARCHITECTURE.md)) is
designed to extend this same pattern across all 21 topics of the Anthropic
SDK — streaming, tool use, vision, prompt caching, batches, async, error
handling, and more — but this repo currently wires up the **first 3 steps**
as a working demonstration.

---

## 🚀 Start the course

1. Click **[Use this template](../../generate)** above (or the green
   "Use this template" button on the repo page) to create **your own private
   copy** of this course. Do not fork it — "Use this template" gives you a
   clean repo with no shared history, exactly like github/skills courses.
2. In your new repo, go to **Settings → Actions → General** and confirm
   "Allow all actions and reusable workflows" is selected, then click
   **Save**. (Template copies sometimes start with Actions disabled.)
3. Go to **Settings → Secrets and variables → Actions → New repository
   secret** and add:
   - Name: `ANTHROPIC_API_KEY`
   - Value: your key from [console.anthropic.com](https://console.anthropic.com/settings/keys)

   > 💸 **Cost note:** Steps 2 and 3 make real calls to the Anthropic API —
   > both when you run your script locally, and again in CI when the grading
   > workflow re-runs your script to check it. Each run costs a small
   > fraction of a cent with a short-output model. Budget accordingly if you
   > run the course many times.
4. Go to the **Issues** tab. Within about 20–30 seconds of creating your
   repo, **Issue #1: "📘 Step 1 — Install the SDK & create a client"** should
   appear automatically. If it doesn't show up after a minute, go to the
   **Actions** tab and manually run the **"Step 0 — Start Course"** workflow
   once (`Run workflow` button).
5. Follow the instructions in the issue. When you're done, `git add`,
   `git commit`, `git push` your work to `main`.
6. Watch the **Actions** tab — a check will run automatically. If it passes,
   within a few seconds the issue closes with a ✅ comment and the next issue
   opens. If it fails, read the failure output in the Action's log, fix your
   code, and push again — you can retry as many times as you want.
7. Repeat until you see **"🎉 Course complete"**.

---

## 📂 Where your work goes

All exercise code lives in the `exercises/` folder in **your own repo**. Each
step tells you exactly what filename to create there (e.g.
`exercises/practice1.py`). Don't rename these — the grading workflows look
for these exact paths.

---

## 🧩 How this works (for the curious)

Short version: each step is one GitHub Actions workflow that's triggered when
you push the expected exercise file. It runs a small Python checker against
your code, and if it's correct, uses the GitHub CLI to comment + close the
current issue and open the next one. Full breakdown, including why it's
built this way, is in [`COURSE-ARCHITECTURE.md`](COURSE-ARCHITECTURE.md).

If you're the person setting this course up for others (publishing it as a
template repo, wiring up secrets, testing the whole flow yourself first), see
[`SETUP-GUIDE.md`](SETUP-GUIDE.md).

---

## Requirements

- Python 3.10+ (matches the SDK's minimum supported version)
- A GitHub account with Actions enabled
- An Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

## Source material

This course's lesson content is adapted from a comprehensive internal
reference doc covering all 21 areas of the Anthropic Python SDK (installation
through Bedrock/Vertex variants). The exercises you'll do here are pulled and
lightly adapted from that same reference so what you practice here matches
real study material 1:1.
