# Personalizer

**Write and edit in your own voice.**

Personalizer learns from samples of your writing, then helps your agent draft and edit in that voice. It pays attention to rhythm, wording, punctuation, and how your tone changes between an email, a post, and an article.

Works with Claude Code, Cursor, GitHub Copilot, Codex, and other [Agent Skills](https://agentskills.io/specification)-compatible hosts.

[![Checks](https://github.com/KaramveerSidhu/personalizer/actions/workflows/ci.yml/badge.svg)](https://github.com/KaramveerSidhu/personalizer/actions/workflows/ci.yml)
[Guide](docs/guide.md) · [Releases](https://github.com/KaramveerSidhu/personalizer/releases) · [MIT license](LICENSE.txt)

## Quick start

**1. Install** with the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add KaramveerSidhu/personalizer --global --skill personalizer
```

Select the agents you use. For an exact release, manual installation, or an update, see the [installation guide](docs/guide.md#installation).

**2. Teach it your voice.** Paste writing you actually produced and say what kind of writing it is:

```text
Use personalizer to learn my voice from these samples.
These are emails I wrote to teammates: [your samples]
```

Several samples totaling roughly 500–2,000 words are a useful starting point. Shorter samples work with lower confidence. Setup creates a reusable voice profile; it does not save your raw samples by default.

**3. Use it on a draft:**

```text
Use personalizer to rewrite this teammate email in my voice: [draft]
```

You can also ask it to write from supplied facts, update your profile with new samples, or explain why a draft does not sound like you. Without a usable profile, it can edit in a neutral voice.

## An example

This fictional profile favors plain wording, natural contractions, short paragraphs, and direct, polite requests.

**Before**

> I wanted to reach out to let you know that the guide is ready for review. We would greatly appreciate it if you could take a look at the last paragraph before noon. Your feedback will help us decide whether to send it today.

**With that profile**

> The guide’s ready for review.
>
> Could you look over the last paragraph before noon? Your feedback will help us decide whether to send it today.

The request, timing, and uncertainty stay intact. Another profile may call for a different rhythm or level of formality. This example uses invented material; no personal writing is bundled.

## What it does

- **Learns your writing habits.** Builds a profile from genuine samples, with evidence, confidence, and differences between channels.
- **Applies your voice.** Drafts and rewrites using those observations, while keeping facts, quotations, links, numbers, and code intact unless you authorize changes.
- **Improves with your feedback.** Merges new evidence when asked. Ordinary rewrites do not silently change the profile.
- **Explains mismatches.** Diagnoses where a draft differs from the profile without inventing an authorship score.

## Your profile stays separate

New personal profiles default to `~/.personalizer/voice-profile.md`. Local agents with access to the same profile can reuse it. You can also choose a project profile or configure another location with `PERSONALIZER_HOME`; see the [profile guide](docs/guide.md#voice-profiles).

Calibration stores derived observations and aggregate evidence by default. Your host still processes supplied writing in its normal model session. Local profiles do not automatically sync to cloud sessions, and hosts without persistent storage return a profile for you to save.

The skill provides instructions and audits, not a guarantee that every rewrite will be perfect. Review important writing. It does not promise AI-detector evasion. The optional Python helper uses approximate English-oriented measurements; voice quality depends on the model and the samples supplied.

## Development and attribution

[Contributor instructions](CONTRIBUTING.md) cover the helper tests, standard format validation, and [synthetic behavior checks](evals/README.md). The writing skill needs no Python installation; the optional measurement helper requires Python 3.10+.

The cleanup foundation adapts [Humanizer](https://github.com/blader/humanizer). [Humanize](https://github.com/shir-danishyar/humanize) inspired persistent calibration and channel-aware application. The profile schema, storage rules, voice-matching guidance, helper, and tests were independently implemented. See the [MIT license](LICENSE.txt) and [third-party notices](THIRD_PARTY_NOTICES.md).
