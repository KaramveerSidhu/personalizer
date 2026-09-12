# Personalizer

Write and edit prose in your own voice, with a profile learned from writing you actually produced.

Personalizer is a local Codex skill. It removes generic writing patterns, applies supported author habits, adjusts for the audience, and checks that the meaning and protected text survive. Your profile can preserve contractions, fragments, em dashes, rhetorical questions, or other habits that a generic editor might erase.

Without a profile, it still works as a neutral prose editor. It does not score authorship or promise to evade AI detectors.

## Install

You need Codex with local skill support. The optional measurement helper requires Python 3.10 or newer and uses only the standard library.

Ask Codex's built-in installer:

```text
$skill-installer install https://github.com/KaramveerSidhu/personalizer at tag v0.1.0. The skill is at the repository root; name it personalizer.
```

Or clone the release into the user skill location documented by [Codex](https://learn.chatgpt.com/docs/build-skills):

```sh
mkdir -p "$HOME/.agents/skills"
git clone --branch v0.1.0 --depth 1 \
  https://github.com/KaramveerSidhu/personalizer.git \
  "$HOME/.agents/skills/personalizer"
```

If you already have Personalizer installed, update that installation instead of adding a second copy. Some Codex setups and the built-in installer use `$CODEX_HOME/skills` or `~/.codex/skills`. Keep the location your installation uses. Codex discovers skill changes automatically; restart it if the skill does not appear.

For a Git clone, update from inside its directory:

```sh
git status --short
git fetch --tags origin
git switch --detach v0.1.0
```

Replace `v0.1.0` with the release you want. Review any local changes before switching. Profiles are stored separately, so updating the skill does not require recreating your profile.

## Use it

```text
$personalizer make this sound like me: [draft]
$personalizer write a short project update using these facts: [facts]
$personalizer setup — learn my voice from these samples: [your writing]
$personalizer update my voice profile with these new samples: [your writing]
$personalizer why doesn't this draft sound like me? [draft]
```

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
4. `$CODEX_HOME/personalizer/voice-profile.md`, when `CODEX_HOME` is set.
5. `~/.codex/personalizer/voice-profile.md`.

New personal setup uses the configured global location, with the last path as the default. Project or brand setup uses `.personalizer/voice-profile.md` in the chosen project.

An explicitly selected profile is exclusive. If it cannot be used, Personalizer explains the problem and works from current-session samples or neutral prose; it does not silently choose another author's profile. See [calibration guidance](references/voice-calibration.md) and the [generic profile template](assets/voice-profile.template.md) for the schema, confidence levels, and update rules.

## Privacy

Live profiles stay outside the installed skill and this repository. Calibration saves derived observations and aggregate evidence by default, without retaining raw samples, identifying source details, or verbatim sample sentences. Saving actual samples requires an explicit request.

The Python helper runs locally without network calls. Codex processes the supplied writing in its normal model session, so the complete workflow is not an offline system. The skill does not send samples to an additional analysis service.

Project profiles are kept out of Git using a local exclusion for their actual path. An ignore rule cannot protect a file already tracked in Git. Keep real profiles and samples out of issues, pull requests, examples, and test fixtures too.

## Measurement and checks

From a clone of this repository:

```sh
python3 scripts/analyze_voice.py --help
python3 scripts/analyze_voice.py path/to/your-sample.txt
python3 -B -m unittest discover -s tests -v
```

With no file argument, the helper reads stdin. It emits descriptive counts only, including sentence/paragraph lengths, punctuation, contractions, and person markers. It does not print source text or filenames or create a voice profile. Its English-oriented segmentation and Markdown cleanup are approximate; the JSON output explains the limitations.

[CI](.github/workflows/ci.yml) runs the helper tests and the official OpenAI Skill Creator validator at a pinned upstream revision. PyYAML in [requirements-dev.txt](requirements-dev.txt) is a validation-only dependency; it is not required to use the measurement helper.

The [synthetic evaluation pack](evals/README.md) provides separate manual checks for writing behavior, calibration, preservation, and profile selection. Passing unit tests does not establish that every model-generated rewrite matches an author. Model version, sample quality, register coverage, and the current request all affect the result.

## Contributing

Keep changes focused and preserve factual integrity and private-data boundaries. Run the unit tests and relevant synthetic scenarios for behavior changes. Use invented fixtures only, and describe which behavior you checked when opening a pull request. Broader language support and more repeatable voice-fit evaluations are useful areas for future work.

## Attribution and license

The cleanup foundation adapts [blader/humanizer](https://github.com/blader/humanizer). [shir-danishyar/humanize](https://github.com/shir-danishyar/humanize), formerly `Shirhussain/humanize`, inspired persistent calibration and register-aware application.

The profile schema, storage/update rules, measurement helper, and tests were independently implemented. The project uses the [MIT license](LICENSE.txt); [third-party notices](THIRD_PARTY_NOTICES.md) preserve upstream licenses and identify the revisions used. CI obtains the OpenAI validator separately and does not bundle it in this repository.
