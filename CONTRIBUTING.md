# Contributing

Thank you for helping. This is a safety-critical project, so the contribution rules are stricter
than usual and a few of them are unusual. Read all of this before your first commit.

---

## Read before your first commit: version control deanonymises you

**`git log` is a permanent, public, globally indexed list of contributors' real names and email
addresses.** Whatever name and email your `git config` holds will be attached to every commit,
forever, in every fork and mirror. If that is a safety problem for you:

- Set a dedicated identity for this repo *before* you commit:
  ```
  git config user.name  "a name you are comfortable publishing"
  git config user.email "an address you are comfortable publishing"
  ```
- Consider GitHub's `noreply` email and its email-privacy setting.
- If you cannot contribute safely, **do not.** Open an issue anonymously, or ask an advocacy
  organisation to relay it. Your safety is worth more than a pull request.

---

## The cover identity never enters the repository

The disguise is defeated by a search engine, not an attacker (`docs/THE_APP_v1_5.md`, Part I).
So, without exception:

- **No candidate cover name, package, icon or domain** in code, config, tests, fixtures,
  screenshots, issues, PR titles, or commit messages. The placeholders stay placeholders.
- **No screenshot of the cover UI**, anywhere, including in this repo and in issues.
- **Read your commit messages before you push.** No gate catches `fix decoy PIN timing`; a human
  writing the log carefully does. That phrase is the whole product in four words.
- **Never type the cover identity into a hosted agent or any third-party tool.** A prompt is a
  record. This is easy, because per the above it is not in the repo for you to copy either.
- **No signing material committed** — `*.keystore`, `*.jks`, `*.p12`, `*.mobileprovision`.

---

## The gates are the law

Every change must pass the gates. They **fail** the build; they do not warn.

```
make hooks        # do this once — installs the pre-commit hook
make gates-fast   # runs on every commit, <5s
make gates        # run the full set before you open a PR
```

If a gate blocks you, it is telling you which promise the change breaks — the trace to the
requirement is in the failure message. **The answer is almost never "edit the gate."**

### The dependency allowlist is protected on purpose

Adding a line to `gates/allowed-deps.txt` is a human decision that needs a reason in the commit
message. That friction is the point (S8: *no third-party SDKs*). If an agent can widen the
allowlist to make its own build pass, the gate does nothing.

---

## The blocklist of "helpful" defaults

Every item below is something a good engineer adds unasked. Here, each one gets someone hurt.
Do not add:

```
⛔ crash reporting, error tracking, Sentry, Crashlytics — of any kind
⛔ analytics, telemetry, "anonymous" usage metrics, A/B infrastructure
⛔ any network client, any HTTP library, any retrofit/ktor/URLSession call
⛔ logging that survives release builds
⛔ persistence "so the user doesn't lose progress" in the training tier — it is meant to be lost
⛔ a splash screen, an onboarding carousel, a rating prompt, a changelog dialog
⛔ biometric unlock — compellable, so this is not a preference
⛔ a wrong-entry state of any kind: no shake, no toast, no counter, no lockout
⛔ deep links, share sheets, app shortcuts, widgets, notification channels
⛔ a dependency added to save an afternoon
```

## What a machine must not touch

- **The threat model itself.** Never generated, never refactored by a machine.
- **The entry sequence, the decoy tier, the panic wipe.** Key-before-data ordering
  (`docs/THE_APP_v1_4.md`, Part VI) is exactly what a "tidier" refactor quietly inverts.
- **Every string that ships.** A human reads all of them.

## The tests you cannot automate

Two things the gates cannot check, and a person must:

1. **The five-minute hostile test** — a suspicious, technical person with the phone in their
   hand. Fast entry, convincing cover, plausible decoy. A machine cannot run this.
2. **The advocate review** (`docs/THE_APP.md`, Part VII). Non-negotiable before launch.

---

*Compile the promise or lose it. Check the artefact, never the source.*

**P = 12 · χ = 2 · always.**
