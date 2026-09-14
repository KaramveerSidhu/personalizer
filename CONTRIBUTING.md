# Contributing to Personalizer

Keep changes focused on writing quality, author voice, factual preservation, and portability. A useful report includes a minimal fictional example, the host and model used, what happened, and what you expected. Do not post real profiles, private writing, or identifying sample details in issues or pull requests.

Use [GitHub issues](https://github.com/KaramveerSidhu/personalizer/issues) for reproducible problems and focused suggestions. For changes, open a pull request that explains the behavior and the checks you ran. Preserve the [MIT license](LICENSE.txt) and applicable [third-party notices](THIRD_PARTY_NOTICES.md).

## Automated checks

The optional measurement helper uses only the standard library. Run its tests with Python 3.10+:

```sh
python3 -B -m unittest discover -s tests -v
```

Format validation uses the official [Agent Skills reference implementation](https://github.com/agentskills/agentskills/tree/main/skills-ref), pinned in [requirements-dev.txt](requirements-dev.txt). With Python 3.11+ and Git, from a clone named `personalizer`:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
skills-ref validate "$PWD"
```

Use your shell's virtual-environment activation command on other platforms. Pass an absolute path: the validator checks that the directory name matches the skill's `name`. These dependencies are for validation only; people using the writing skill do not need them.

[CI](.github/workflows/ci.yml) runs format validation on Python 3.14 and helper tests on Python 3.10 and 3.14. Format validation checks the package structure and metadata; it does not establish writing quality.

## Behavior checks

Use the [manual evaluation pack](evals/README.md) for relevant instruction changes. It covers protected text, calibration, profile updates, explicit profile selection, tone, diagnostics, shared storage, and hosts without persistent state. Use only the fictional fixtures and temporary workspaces. Record the host, model, commit, case, and observed result.

For helper changes, test the observable behavior or bug being fixed. For documentation changes, verify commands and local links. Do not turn subjective voice matching into an exact-output test or treat a passing format check as evidence that every host was exercised.

## Release checks

Before tagging a release:

- Verify the current commit's CI and relevant behavior checks.
- Check that no real writing, profiles, temporary results, or credentials are included.
- Verify Skills CLI discovery and an isolated installation with all referenced resources present.
- Keep the guide's pinned install command and release notes aligned with the tag.

After publishing the tag, verify installation from that tag and publish the release notes for the tested commit. Keep limitations and supported environments accurate.
