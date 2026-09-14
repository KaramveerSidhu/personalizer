# Personalizer guide

[Back to the README](../README.md)

## Installation

Use a host that can load `SKILL.md` and its supporting resources. The writing instructions have no provider, API, shell, or Python dependency. Persistent profiles need private storage. The optional Python measurement helper requires Python 3.10+.

The [Skills CLI](https://github.com/vercel-labs/skills) requires a supported Node.js/npm installation (currently Node.js 22.20+). The README's short install command follows the repository's default branch. To install this exact release:

```sh
npx skills add https://github.com/KaramveerSidhu/personalizer/tree/v0.2.1 \
  --global --skill personalizer
```

Append `--agent claude-code cursor github-copilot codex` to choose agents explicitly, keeping only the names you use. Omit `--global` for a project installation. Use `--copy` if you prefer copies to symlinks. Install the whole package, including `references/`, `assets/`, and `scripts/`; the skill is at the repository root.

### Manual installation and invocation

These are documented locations, not an exhaustive list of compatible hosts:

| Host | Personal skill directory | Project skill directory | Invocation |
| --- | --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/personalizer/` | `.claude/skills/personalizer/` | `/personalizer` |
| [Cursor](https://prod.cursor.com/help/customization/skills) | `~/.cursor/skills/personalizer/` | `.cursor/skills/personalizer/` | `/personalizer` |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | `~/.copilot/skills/personalizer/` | `.github/skills/personalizer/` | Natural-language request; `/personalizer` in [CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#skills-reference) and [VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills#_use-skills-as-slash-commands) |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `~/.agents/skills/personalizer/` | `.agents/skills/personalizer/` | `$personalizer` |

For example, a personal Claude Code installation:

```sh
mkdir -p "$HOME/.claude/skills"
git clone --branch v0.2.1 --depth 1 \
  https://github.com/KaramveerSidhu/personalizer.git \
  "$HOME/.claude/skills/personalizer"
```

Choose the corresponding path for another host. Existing Codex installations in `$CODEX_HOME/skills` or `~/.codex/skills` can keep their location. Its built-in installer also accepts the repository URL, release tag, root path `.`, and skill name `personalizer`.

Discovery and explicit invocation depend on the host. If the skill does not appear, follow its reload or restart guidance. Hosts without skill discovery can use `SKILL.md` and the relevant bundled references supplied through their context mechanism. Local installations do not automatically transfer to remote sessions.

`agents/openai.yaml` is optional Codex UI metadata. Every host uses the same core skill and resources. Format compatibility and installer checks do not imply that every host application or model has been tested.

### Updating

Update using the method you installed with, and avoid duplicate installations within the same host.

For an installation tracked by the Skills CLI:

```sh
npx skills update personalizer --global
```

For a project installation, run from that project with `--project` instead. This targets Personalizer only. A release-pinned installation stays on its recorded tag. To move to a newer release, rerun the installation command with the desired tag.

To preserve specific agent targets or a `--copy` installation, rerun `skills add` with those options: the current updater re-detects agents and uses the default installation mode. If the CLI cannot find a tracked installation, rerun the appropriate install command or update your manual Git clone.

For a Git clone, from its directory:

```sh
git status --short
git fetch --tags origin
git switch --detach v0.2.1
```

Review local changes before switching, and replace the tag with the release you want. Updating the skill does not require rebuilding a separately stored profile.

## Voice profiles

### Setup and everyday use

Supply genuine writing and identify its context. Several samples totaling roughly 500–2,000 words are useful; smaller samples are accepted with lower confidence. A tutorial, quick message, and report can reveal different habits. Copied prompts, assistant output, quoted material, and drafts under repair are not automatically evidence of your voice.

```text
Use personalizer to learn my voice from these article samples: [your writing]
Use personalizer to write a project update using these facts: [facts]
Use personalizer to update my voice profile with these new samples: [your writing]
Use personalizer to explain why this draft doesn't sound like me: [draft]
```

Writing requests return the finished text. Diagnostics explain supported mismatches. Setup and updates report the saved path, sample coverage, and confidence. One-off style directions do not become permanent preferences unless you ask to remember them.

### Storage and selection

Lookup order:

1. A profile explicitly supplied or named by you.
2. `<project-root>/.personalizer/voice-profile.md`.
3. `<project-root>/voice-profile.md`, when clearly an author profile.
4. `<personalizer-home>/voice-profile.md`.

The shared personal directory defaults to `~/.personalizer`. Set `PERSONALIZER_HOME` to an absolute directory to use another location. This is separate from agent-specific skill installation paths; agents with access to the same directory can reuse a profile.

New personal setup uses that shared location. Project or brand setup uses `.personalizer/voice-profile.md` in the chosen project. Existing profiles are carefully updated at their selected path. The skill does not silently migrate or duplicate them.

An explicitly selected profile is exclusive. If it is unavailable or unsuitable, the skill reports the problem and uses genuine session samples or neutral prose. It does not silently select another author's profile. See [the skill's lookup rules](../SKILL.md#resolve-the-voice), [calibration guidance](../references/voice-calibration.md), and [profile template](../assets/voice-profile.template.md) for details.

### Existing Codex profiles

In Codex, when no applicable shared profile exists and `PERSONALIZER_HOME` is unset, legacy lookup checks `$CODEX_HOME/personalizer/voice-profile.md` when configured, then `~/.codex/personalizer/voice-profile.md`. Other hosts only inspect those locations if you explicitly choose a profile there.

To share a legacy profile across agents, explicitly ask to move it to the shared location. Your existing profile remains usable in Codex without migration.

### Privacy and limited hosts

Save derived observations, aggregate evidence, and confidence by default. Raw samples, verbatim sentences, personal names, and private source paths are not retained by default. Saving samples requires an explicit request and a separate private destination.

Profiles stay outside the installed skill. Project profiles use a local Git exclusion for their actual path; ignore rules cannot protect files already tracked. Never include real profiles or samples in issues, pull requests, or test fixtures.

Your host processes supplied writing in its normal model session. The skill does not send samples to an additional analysis service, and the Python helper makes no network calls. This does not make the entire workflow offline.

If private persistent storage is unavailable, setup returns a proposed profile for you to save and supply later. It does not promise future memory. Local profiles do not automatically sync to cloud sessions.

## Optional measurements

Run the helper from the installed skill or a repository clone:

```sh
python3 scripts/analyze_voice.py --help
python3 scripts/analyze_voice.py path/to/your-sample.txt
```

With no file arguments, it reads stdin. Files are treated as separate samples. Output is aggregate JSON: sentence and paragraph lengths, punctuation, contractions, and person markers. It does not print source text or filenames, create profiles, or judge voice quality.

The English-oriented segmentation and Markdown cleanup are approximate. Fenced and inline code, marked blockquotes, URL destinations, and front matter are excluded. Indented code, unmarked quotations, HTML, and complex Markdown need manual exclusion or in-context analysis. Read the JSON's `metadata.limitations` before interpreting measurements. For development checks, see [CONTRIBUTING.md](../CONTRIBUTING.md).
