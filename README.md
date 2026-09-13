# Personalizer

Write and edit prose in your own voice, with a profile learned from writing you actually produced.

Personalizer is a portable [Agent Skill](https://agentskills.io/specification) for Claude Code, Cursor, GitHub Copilot, Codex, and other hosts that support the format. It removes generic writing patterns, applies supported author habits, adjusts for the audience, and checks that the meaning and protected text survive. Your profile can preserve contractions, fragments, em dashes, rhetorical questions, or other habits that a generic editor might erase.

Without a profile, it still works as a neutral prose editor. It does not score authorship or promise to evade AI detectors.

## Install

Use an agent that can load `SKILL.md` and its supporting resources. The writing instructions have no provider, API, shell, or Python dependency. Saving a profile across sessions requires private persistent storage; the optional measurement helper requires Python 3.10 or newer and uses only the standard library.

With a supported Node.js/npm version available (the current CLI requires Node.js 22.20+), the [Skills CLI](https://github.com/vercel-labs/skills) installs the same package for the agents you select:

```sh
npx skills add https://github.com/KaramveerSidhu/personalizer/tree/v0.2.0 \
  --global --skill personalizer
```

To choose agents explicitly, append `--agent claude-code cursor github-copilot codex`, selecting only those you use. Omit `--global` for a project installation. Use `--copy` if you prefer copies to symlinks. The skill lives at the repository root; install the whole folder, including `references/`, `assets/`, and `scripts/`.

You can also clone the release into a skill directory your host supports:

| Host | Personal skill directory | Project skill directory | Explicit invocation |
| --- | --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/personalizer/` | `.claude/skills/personalizer/` | `/personalizer` |
| [Cursor](https://prod.cursor.com/help/customization/skills) | `~/.cursor/skills/personalizer/` | `.cursor/skills/personalizer/` | `/personalizer` |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | `~/.copilot/skills/personalizer/` | `.github/skills/personalizer/` | Natural-language request; `/personalizer` in [CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#skills-reference) and [VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills#_use-skills-as-slash-commands) |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `~/.agents/skills/personalizer/` | `.agents/skills/personalizer/` | `$personalizer` |

For example, a personal Claude Code installation:

```sh
mkdir -p "$HOME/.claude/skills"
git clone --branch v0.2.0 --depth 1 \
  https://github.com/KaramveerSidhu/personalizer.git \
  "$HOME/.claude/skills/personalizer"
```

Choose the corresponding path for another host. These are documented locations, not an exhaustive list of compatible agents. Discovery, invocation, and cloud support depend on the host. Local installations and local profiles do not automatically transfer to remote sessions. If the skill does not appear, follow the host's reload or restart guidance.

If already installed, update that installation instead of adding a duplicate within the same host. Existing Codex installations in `$CODEX_HOME/skills` or `~/.codex/skills` can keep their location. Codex's built-in installer also accepts the repository URL, the `v0.2.0` tag, root path `.`, and skill name `personalizer`.

For a Git clone, update from inside its directory:

```sh
git status --short
git fetch --tags origin
git switch --detach v0.2.0
```

Replace `v0.2.0` with the release you want. Review any local changes before switching. Profiles are stored separately, so updating the skill does not require recreating your profile.

`SKILL.md` and its resources are shared across hosts. `agents/openai.yaml` supplies optional Codex UI metadata; it is not required by the core skill. Supporting the standard does not imply that every host or model has been tested or will produce identical writing.

## Use it

```text
Use personalizer to make this sound like me: [draft]
Use personalizer to write a short project update using these facts: [facts]
Use personalizer to learn my voice from these samples: [your writing]
Use personalizer to update my voice profile with these new samples: [your writing]
Use personalizer to explain why this draft doesn't sound like me: [draft]
```

Use your host's explicit invocation syntax from the table when preferred. If it cannot discover skills, supply `SKILL.md` and the relevant bundled references through its supported context mechanism; persistent profiles and script execution still depend on available tools.

For calibration, supply genuine writing samples and identify their context. Several samples totaling roughly 500–2,000 words are useful; shorter samples are accepted with lower confidence. A tutorial, a quick message, and a report can show different habits. Personalizer records those differences instead of treating one sample as a rule for every channel.

Ordinary writing requests return the finished text. Diagnostics explain supported mismatches. Setup and update operations report the saved profile location and evidence coverage. Rewriting a draft does not silently update your profile.

## What changes, and what stays

The editing pass looks at inflated claims, repetitive structures, staged openings, filler, and unnecessary formatting. These are tendencies to examine, not forbidden words or punctuation.

For example, this **synthetic** draft:

> It is important to note that the pilot may reduce retries. This is not just a change; it is a transformative leap.

Can become:

> The pilot may reduce retries.

The qualification stays. A rewrite cannot invent a measured improvement or turn a possibility into a result.

Quotes, citations, URLs, numbers, dates, proper nouns, technical identifiers, code, Markdown link destinations, front matter, and data structures are protected unless you specifically authorize changes. The skill also checks attribution, uncertainty, conditions, and relationships. These are model instructions and audits, not a formal proof of preservation; review important writing before using it.

## Where your profile lives

Lookup order:

1. A profile you explicitly supply or name.
2. `<project-root>/.personalizer/voice-profile.md`.
3. `<project-root>/voice-profile.md`, when clearly intended as an author profile.
4. `<personalizer-home>/voice-profile.md`.

The shared personal directory is `~/.personalizer` by default. Configure `PERSONALIZER_HOME` as an absolute directory to use another location; the profile is `voice-profile.md` inside it. This is Personalizer's storage convention, separate from agent-specific skill directories. Agents using the same directory and filesystem permissions can reuse one profile without separate calibration.

New personal setup uses that shared location. Project or brand setup uses `.personalizer/voice-profile.md` in the chosen project. If private persistent storage is unavailable, setup returns a derived profile for you to save and supply later. It does not promise memory across sessions.

For existing Codex users, when no applicable shared profile is found and `PERSONALIZER_HOME` is unset, Codex can still read `$CODEX_HOME/personalizer/voice-profile.md` and then `~/.codex/personalizer/voice-profile.md`. Other hosts do not inspect these legacy directories unless you explicitly select a profile there. Existing-profile updates keep their selected path. To make a legacy profile available across agents, explicitly ask to move it to the shared location; the skill does not silently migrate or duplicate it.

An explicitly selected profile is exclusive. If it cannot be used, Personalizer explains the problem and works from current-session samples or neutral prose; it does not silently choose another author's profile. See [calibration guidance](references/voice-calibration.md) and the [generic profile template](assets/voice-profile.template.md) for the schema, confidence levels, and update rules.

## Privacy

Live profiles stay outside the installed skill and this repository. Calibration saves derived observations and aggregate evidence by default, without retaining raw samples, identifying source details, or verbatim sample sentences. Saving actual samples requires an explicit request.

The Python helper runs locally without network calls. Your host agent processes the supplied writing in its normal model session, so the complete workflow is not necessarily offline. The skill does not send samples to an additional analysis service.

Project profiles are kept out of Git using a local exclusion for their actual path. An ignore rule cannot protect a file already tracked in Git. Keep real profiles and samples out of issues, pull requests, examples, and test fixtures too.

## Measurement and checks

From a clone of this repository:

```sh
python3 scripts/analyze_voice.py --help
python3 scripts/analyze_voice.py path/to/your-sample.txt
python3 -B -m unittest discover -s tests -v
```

With no file argument, the helper reads stdin. It emits descriptive counts only, including sentence/paragraph lengths, punctuation, contractions, and person markers. It does not print source text or filenames or create a voice profile. Its English-oriented segmentation and Markdown cleanup are approximate; the JSON output explains the limitations.

[CI](.github/workflows/ci.yml) runs the helper tests on Python 3.10 and 3.14 and checks the package with the Agent Skills reference validator at a pinned upstream revision. Its validation-only dependencies are in [requirements-dev.txt](requirements-dev.txt); they are not required to use the skill or measurement helper. The reference validator requires Python 3.11 or newer.

To run format validation locally, use Python 3.11+ and Git from a clone named `personalizer`:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
skills-ref validate "$PWD"
```

Use your shell's virtual-environment activation command on other platforms. Pass the absolute skill directory to `skills-ref`: the reference validator checks that the folder name matches the skill's `name`.

The [synthetic evaluation pack](evals/README.md) provides separate manual checks for writing behavior, calibration, preservation, and profile selection. Passing unit tests does not establish that every model-generated rewrite matches an author. Model version, sample quality, register coverage, and the current request all affect the result.

## Contributing

Keep changes focused and preserve factual integrity and private-data boundaries. Run the unit tests and relevant synthetic scenarios for behavior changes. Use invented fixtures only, and describe which behavior you checked when opening a pull request. Broader language support and more repeatable voice-fit evaluations are useful areas for future work.

## Attribution and license

The cleanup foundation adapts [blader/humanizer](https://github.com/blader/humanizer). [shir-danishyar/humanize](https://github.com/shir-danishyar/humanize), formerly `Shirhussain/humanize`, inspired persistent calibration and register-aware application.

The profile schema, storage/update rules, measurement helper, and tests were independently implemented. The project uses the [MIT license](LICENSE.txt); [third-party notices](THIRD_PARTY_NOTICES.md) preserve upstream licenses and identify the revisions used. CI obtains the [Agent Skills reference validator](https://github.com/agentskills/agentskills/tree/main/skills-ref) separately and does not bundle it in this repository.
