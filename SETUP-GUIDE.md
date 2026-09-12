# SETUP GUIDE — How to stand up this course yourself

This guide is for **you** (the course author), not the learner. It walks
through turning this scaffold into a live, working GitHub course.

---

## 1. Create the GitHub repo

You have two options:

**Option A — Push as a normal repo (fastest way to test it yourself):**

```bash
cd /workspace/anthropic-sdk-course
git init
git add .
git commit -m "Scaffold: Anthropic Python SDK course (steps 1-3 PoC)"
gh repo create YOUR-USERNAME/anthropic-sdk-course --public --source=. --remote=origin --push
```

(Install the `gh` CLI first if you don't have it: https://cli.github.com/,
then run `gh auth login` once.)

**Option B — Make it a real "Use this template" course (for other learners):**

1. Push the repo as above.
2. Go to the repo on GitHub → **Settings** → check **"Template repository"**.
3. Share the URL. Anyone can now click **"Use this template"** to get their
   own independent copy with a clean Actions history.

---

## 2. Enable Actions

New repos usually have Actions enabled by default, but double check:

- Go to **Settings → Actions → General**.
- Under "Actions permissions," choose **"Allow all actions and reusable
  workflows"** (or at least allow `actions/checkout`, `actions/setup-python`,
  and the built-in `gh` CLI usage — those are all this course needs).
- Under "Workflow permissions" (same page, scroll down), select **"Read and
  write permissions"**. The workflows need to create issues, comment, close
  issues, and enable/disable other workflows — this requires write access.

---

## 3. Add your API key as a secret

Steps 2 and 3 make **real calls to the Anthropic API through this project's
IBM gateway** (`base_url="https://api.servicesessentials.ibm.com"`), both
when you (the learner) run the script locally AND when the GitHub Action
re-runs it to grade you. The client is constructed with `python-dotenv` +
`ICA_API_KEY` + that custom `base_url` — not the plain `Anthropic()` default.
That means the key needs to exist in two places:

1. **Your local `.env` file**, for testing: copy `.env.example` to `.env`
   and set `ICA_API_KEY=<your real key>`. The exercises call
   `load_dotenv()` to read it — `.env` is git-ignored, so it never gets
   committed.
2. **The repo's Actions secrets**, for grading:
   - Go to **Settings → Secrets and variables → Actions → New repository
     secret**.
   - Name: `ICA_API_KEY`
   - Value: your real key.
   - Click **Add secret**.

> 🌐 **Why `base_url`?** Passing `base_url=` points the SDK at a proxy/
> gateway in front of Anthropic's API instead of hitting `api.anthropic.com`
> directly. The SDK's request/response shapes stay identical — only the
> network destination changes. Useful when an org routes model traffic
> through an internal gateway for logging, cost tracking, or access control.

> 💰 **Cost note:** Steps 2 and 3 each make one small `messages.create()`
> call with `max_tokens=100`. This is a trivial cost per learner run
> (fractions of a cent), but if you expect many learners, keep an eye on
> your usage dashboard.

---

## 4. Kick off the course

The course starts itself automatically the first time something is pushed
to `main` — which happens the moment you push your initial commit (see
step 1 above). Workflow `Step 0 - Start Course` runs, and within a few
seconds you should see a new **Issue** appear titled "Step 1: Install the
SDK & create a client."

If nothing appears after ~30 seconds:

- Go to the **Actions** tab and check whether "Step 0 - Start Course" ran
  and what its logs say.
- Most common cause: workflow permissions weren't set to "Read and write"
  (see step 2 above) — the job will fail with a 403 when it tries to
  create the issue.

---

## 5. Test the flow yourself, as a learner would

1. Open the Step 1 issue that got created.
2. Follow its instructions exactly: create `exercises/practice1.py` locally
   with the given content, run it, then:

   ```bash
   git add exercises/practice1.py
   git commit -m "Step 1: install SDK and create client"
   git push
   ```

3. Watch the **Actions** tab — `Step 1 - Install SDK` should trigger within
   a couple seconds of the push landing on GitHub.
4. When it finishes (green check), refresh the Step 1 issue. You should see
   a ✅ comment, and the issue should be **closed**. A brand new **Step 2**
   issue should have opened automatically.
5. Repeat for Step 2 (`exercises/practice_message.py`) and Step 3
   (`exercises/practice_inspect.py`).
6. After Step 3 passes, a final **"🎉 Course complete!"** issue opens.

If a check fails, the workflow run will show a red ❌ in the Actions tab,
and (if the bot could figure out which issue to comment on) you'll see a
comment pointing you at the failed run's logs. Fix the file, push again —
the same workflow re-triggers on the next push to that file.

---

## 6. Extending to more sections

This scaffold wires up Sections 1-2 of the 21-section reference material
(3 exercises total) as a working proof of concept. To add Section 3
onward, for each new step:

1. Add `.github/steps/0N-<slug>.md` with theory + exercise, adapted from
   the matching section in `Anthropic-Python-SDK-Reference.md`.
2. Add `.github/scripts/check_stepN.py` — a small script that runs the
   learner's file and checks stdout/behavior.
3. Add `.github/workflows/0N-check-stepN.yml`, copying the pattern from
   `02-check-step2.yml` or `03-check-step3.yml` (update file paths, issue
   labels, step numbers, and workflow names to enable/disable).
4. Update the previous step's workflow to open the new issue and enable
   the new workflow, instead of the course-complete issue.

See `COURSE-ARCHITECTURE.md` for the full design rationale and diagrams.
