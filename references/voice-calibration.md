# Learn and maintain a private profile

## Evidence and consent

Setup needs genuine author samples or explicit preferences. Ask for samples if none are supplied; never use a copied ChatGPT prompt, assistant output, third-party quotation, or draft under repair as presumed author evidence. Exclude quoted material and code from measurements. For mixed authorship, use identified genuine portions or ask one focused question. Do not mine unrelated files, messages, or prior conversations for samples.

Several samples across relevant channels, roughly 500–2,000 words or more in total, help expose stable patterns. Accept smaller samples and mark inference confidence low. One chat message can support a provisional chat observation, not a general rule about all writing. More words in one sample do not establish cross-context consistency.

Record writing behavior only. Do not infer personality, identity, demographics, education, politics, health, or psychological attributes. Distinguish how certainty is expressed from what the author believes. Explicit dislikes or preferences can be recorded as user-stated directions without pretending samples demonstrated them.

## Profile storage

Use the lookup and `<personalizer-home>` definition in SKILL.md. For new personal/global setup, use `<personalizer-home>/voice-profile.md` (normally `~/.personalizer/voice-profile.md`). For project-specific author or brand setup, use `<project-root>/.personalizer/voice-profile.md`. Follow an explicitly chosen safe profile destination outside the installed skill. Before treating setup as new, resolve the applicable existing profile; an existing profile needs a careful update, not an automatic second copy. Do not turn an unrelated file named `voice-profile.md` into this schema.

Use the host's private, persistent file tools when available. A temporary cloud workspace is not automatically persistent storage. Without suitable storage, return the derived profile in the conversation for the user to save or supply next time, and state that it has not been saved persistently. Do not require a shell or Python for writing or calibration; if file tools cannot perform the Git protections below, use a private location outside the repository or return the proposed profile.

Create parent directories as needed. Keep profile files private where supported (directory mode 700, file mode 600). Before writing in Git, check whether the actual destination is tracked or ignored. For an untracked profile, add a local exclusion for its actual repository-relative path or private directory in the file resolved by `git rev-parse --git-path info/exclude`, preserving existing rules. The default locations use `/.personalizer/` and `/voice-profile.md`; a custom path needs its own rule. Escape Git pattern metacharacters in literal filenames and verify coverage with `git check-ignore -- <destination>` before saving. Never stage samples or a live profile. If already tracked, do not claim an ignore rule protects it; prepare the update in a private global location and explain the tracked-path issue without altering Git history.

Store derived observations, approximate counts, anonymized sample IDs, channels, dates, and confidence. **Do not retain raw samples, verbatim sample sentences, personal names, private source paths, or topical details by default**, even in an evidence section or backup. Harmless transition words and a phrase the user explicitly asks to preserve are acceptable. Persisting actual samples needs an explicit request and a private destination separate from the skill. Do not write pasted samples into temporary files just to run analysis; use stdin if safely available or reason over the text in context.

The helper performs local computation and makes no network calls. The host agent still processes supplied writing in its normal model session; do not claim the whole workflow is offline. Do not upload samples to another analysis service.

## Build the profile

Use [voice-profile.template.md](../assets/voice-profile.template.md) as the schema. Replace generic prompts with observations or `unknown`; remove empty table rows. Capture:

- Purpose/scope, language, sample count, approximate analyzed words, last update, overall confidence and its limits.
- Core voice: formality, warmth/directness, compression, perspective, certainty/hedging.
- Sentence/paragraph rhythm: length mix and variance, fragments, complexity, paragraph lengths and opening/closing habits.
- Syntax, diction, punctuation, formatting, rhetorical habits, preserved quirks, explicit avoids, and evidenced channel overrides.

Every meaningful inferred trait needs a scope, confidence, and brief evidence summary using sample IDs, not excerpts. Mark repeatedly corroborated traits high, repeated but narrow-context observations medium, and sparse/contradictory observations low. These are editorial confidence judgments, not statistical probabilities. Leave unsupported channel overrides unknown.

For supplied files, optionally run `python3 <skill-directory>/scripts/analyze_voice.py --help`, then pass their paths as separate arguments. With no paths the helper reads stdin. It prints aggregate JSON without excerpts or filenames and never creates profiles. Use separate runs per channel when relevant. Keep counting-method limitations with any saved metrics; assess syntax and rhetorical choices yourself.

## Update without flattening the voice

Read the existing profile before editing. A request to update an existing profile authorizes a careful merge into that profile; do not ask for the same permission again. Setup is not blanket permission to replace an existing profile, change its author, or discard it. Before a destructive reset or unresolved destination choice, prepare a proposed derived profile and ask a focused question.

Compare new samples with established traits in the same channel. Add channel-specific exceptions rather than replacing well-supported base traits with one new sample. Record contradictions and lower confidence where warranted. Keep explicit preferences separate from observed habits; incorporate a correction persistently only when the user asks to remember/update it.

Track new sample IDs and counts without double-counting previously analyzed samples. If overlap or old counts are uncertain, say so and retain approximate/unknown totals. Do not average old and new summary statistics as if raw observations were available; preserve separate batch summaries or recompute only from the supplied corpus. Do not save generated rewrites as new author evidence.

Make a narrow merge, re-read the original before saving to detect concurrent edits, and use a same-directory temporary file plus atomic replacement when available. Clean up temporary derived files after success; do not leave duplicate profiles or raw-sample backups. If the profile changed concurrently, reconcile before replacing it. Read back the saved file. If storage is blocked, return the proposed profile and the concrete limitation; never claim it was saved.

Report the actual saved path, sample coverage, confidence, and meaningful changes briefly. Do not include a personal biography or a verbose analysis report.
