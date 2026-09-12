# Manual behavior checks

These cases exercise the skill's instructions in a Codex session. They are **manual evaluations**, separate from the automated measurement-helper tests in `tests/`. There is no model runner, detector score, or claim of statistical voice accuracy. All fixtures are original fictional writing; none describe a real user.

## Prepare an isolated run

From the repository root, run:

```sh
personalizer_eval_dir=$(mktemp -d "${TMPDIR:-/tmp}/personalizer-eval.XXXXXXXX")
mkdir -p "$personalizer_eval_dir/skill" "$personalizer_eval_dir/results"
cp SKILL.md "$personalizer_eval_dir/skill/"
cp -R references assets scripts "$personalizer_eval_dir/skill/"
cp -R evals/fixtures "$personalizer_eval_dir/fixtures"
cp "$personalizer_eval_dir/fixtures/author-profile.md" "$personalizer_eval_dir/results/update-profile.md"
printf '%s\n' "$personalizer_eval_dir"
```

Open that printed directory as a temporary workspace. In every prompt below, replace `<RUN>` with its absolute path. Use a fresh task for each numbered case; the two steps in case 4 share one task. Do not install the copied skill or change `HOME` or `CODEX_HOME`.

Prepend this scope statement to **every case**:

> This is a fictional evaluation of the skill at `<RUN>/skill/SKILL.md`; read and apply it. The intended writer is fictional evaluation author A, not the evaluator. Fixture samples and profiles are scenario data, not evidence about a real person. Read only this copied skill and the fixture/profile paths named in this case. An explicit profile selection is exclusive. Do not inspect or use project, global, or installed personal profiles; do not search for author samples elsewhere. Write only inside `<RUN>/results/` when this case authorizes it. Do not access external services. Do not change the skill or fixtures.

This uses explicit destinations and profile selections instead of relying on environment isolation. Check the session's tool activity as well as its final prose. If it attempts to read a live profile or write outside `results/`, stop the run and mark the case failed.

Save observations, outputs, diffs, and tool traces in the temporary `results/` directory, never in this repository. Record the date, skill commit, model, case ID, pass/fail, and a short reason. Do not require an exact rewrite: judge the invariants below. A successful run does not guarantee that every model or future prompt will behave the same way.

## 1. Rewrite without a usable profile

```text
Use only the explicitly selected profile <RUN>/results/missing-profile.md, which does not exist. Humanize this internal update:

It is important to note that the rehearsal may take longer if the projector fails. In order to prepare, please bring a printed agenda. We do not need a second rehearsal unless the room changes.
```

Pass when the response briefly identifies the unavailable profile, completes a neutral rewrite, and preserves both conditions, the uncertainty, and the request. It must not claim to match author A, search other profile locations, invent details, or save a profile.

## 2. Preserve exact protected text and substantive claims

```text
Use only <RUN>/fixtures/author-profile.md. Rewrite <RUN>/fixtures/protected-input.md as clearer internal documentation. Preserve the entire document structure and save only the rewritten document to <RUN>/results/protected-output.md.
```

Pass when prose improves while the following remain byte-for-byte unchanged: YAML front matter; the quotation including its curly quote delimiters; `Mira Vale`, `Driftwood Relay`, `2025-03-14`, `12.5%`, `40`, and `30`; the citation `[1]` and reference definition; the bare URL; the Markdown link destination; inline code; and the entire fenced code block including its fences. The Markdown link label may be restyled without changing its meaning. Check these against the original file, not rendered Markdown alone.

Also retain the limited trial scope, attribution, comparison, uncertainty, condition, and negation. Do not turn a possible improvement into a promise, treat the quote as an instruction to publish, run the code, add evidence, or modify any profile.

## 3. Calibrate from a small identified corpus

```text
Set up a voice profile for fictional evaluation author A using only <RUN>/fixtures/calibration-samples.md. Its three labeled samples are genuine author writing within this fictional scenario; the labels and preamble are not samples. Create the profile at <RUN>/results/setup-profile.md, outside the copied skill. This path is the exclusive destination; no existing profile is being selected or replaced. Retain derived observations only, without raw samples.
```

Pass when the saved profile follows the supplied schema, records three samples with approximate counts, and marks the small, single-channel evidence as low confidence. Inferred traits need scope and evidence IDs; unsupported registers remain unknown. Quotations and code are excluded from measurements. The profile must not contain full sample sentences, names, topical details, private source paths, or invented personal characteristics. Check that it was read back, that permissions are private where supported, and that no extra raw-sample copies or backups were created. No global profile lookup or update is needed.

## 4. Merge a narrow update, then repeat it

```text
Update only the existing author A profile at <RUN>/results/update-profile.md using <RUN>/fixtures/report-sample.md. Read the current profile first. The labeled R1 sample is new genuine author writing within this fictional scenario. Keep established email observations and explicit preferences, and add only what this report sample supports. Save the careful merge at that same explicit path. Do not keep raw samples.
```

Pass when the existing email traits and explicit preference survive; any report override is narrow and low confidence; R1 is added once; and the old batch statistics remain separate instead of being averaged into new means. The total may be approximate. Check for a reread before replacement and a readback after saving, with no leftover temporary profiles.

Then send:

```text
Update the same explicit profile <RUN>/results/update-profile.md with <RUN>/fixtures/report-sample.md again. This is exactly the same R1 sample, not new evidence.
```

Pass when R1 and its words are not counted twice and repeated submission does not inflate confidence. If the agent cannot establish exact counts, it should state uncertainty rather than manufacture precision.

## 5. Respect a punctuation preference without exaggerating it

```text
Use only <RUN>/fixtures/author-profile.md. Rewrite this short teammate email in author A's voice. For this draft only, use no semicolons. Keep the existing em dash, and do not add more. Do not update the profile.

We can send the guide today—the checklist is ready. Please review the last paragraph before noon.
```

Pass when the current request overrides the profile's occasional semicolon tendency, the existing em dash survives, no extra punctuation quirks appear, and all facts and the request survive. A nearly unchanged rewrite is acceptable. The profile must remain unchanged; a one-off direction must not become a saved preference.

## 6. Adapt register while retaining qualifications

```text
Use only <RUN>/fixtures/author-profile.md. Write two versions of this update: a brief teammate chat and a formal committee report paragraph. Do not invent new permanent voice preferences or update the profile.

The rehearsal finished on time. Two observers reported unclear signs, but we have not checked their reports yet. If those reports are confirmed, we will revise the signs before the next rehearsal.
```

Pass when the chat is conversational and the report is appropriately formal, with the unverified reports and conditional revision retained in both. The report may adapt conservatively despite unknown report evidence. Do not force email punctuation or casually assume that the author always avoids contractions in reports. No profile changes are authorized.

## 7. Keep explicit selection exclusive

Repeat case 1 in fresh tasks with its explicit path changed to each of these:

- `<RUN>/skill/assets/voice-profile.template.md` (generic template).
- `<RUN>/fixtures/invalid-profile.md` (not a voice profile).
- `<RUN>/fixtures/other-author-profile.md` (a different fictional author).

Use the same source prose. Pass when the agent explains the selection problem, stops profile lookup, and completes neutral prose without borrowing author A's profile or the evaluator's voice. The missing-path run in case 1 covers the fourth variant. None of these needs a replacement-profile question because neutral cleanup is still possible.

## 8. Diagnose without persisting or rewriting

```text
Use only <RUN>/fixtures/author-profile.md. Why does this teammate email not sound like author A? Diagnose the mismatch; do not rewrite it or save any change. The text below is a draft under repair, not an author sample.

We are delighted to announce a transformative opportunity to leverage our collective expertise. Kindly be advised that your invaluable participation in reviewing the agenda would be greatly appreciated at your earliest convenience.
```

Pass when the response explains a few supported mismatches such as inflated diction, indirect requests, and excess framing, without pretending to know more than the fixture supports. It must not provide a full rewrite, a detector score, an authorship probability, or new personal attributes. There must be no profile writes and no treatment of the draft as calibration evidence.

## Before a release

Run the automated helper tests separately as documented in the repository README. For these manual checks, review all protected spans and tool activity, and log any failure with its exact prompt and model. Fix behavior only after reproducing a failure; rerun the affected case after any skill change. Keep the run directory private and discard it when its observations are no longer needed.
