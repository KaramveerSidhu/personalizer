#!/usr/bin/env python3
"""Local, dependency-free descriptive counts; no text or identity inference."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import statistics
import sys


WORD = re.compile(r"[^\W_]+(?:['’][^\W_]+)*(?:\.[0-9]+)?", re.UNICODE)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+")
LIST = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+")
ABBREVIATION = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc)\.|\b(?:e\.g\.|i\.e\.|[A-Z](?:\.[A-Z])+\.)", re.I)
PUNCTUATION = {
    "period": r"(?<!\.)\.(?!\.)", "comma": r",", "semicolon": r";",
    "colon": r":", "exclamation": r"!", "question": r"\?",
    "em_dash": r"—", "en_dash": r"–", "hyphen": r"-",
    "ellipsis": r"\.{3,}|…", "parenthesis": r"[()]",
    "double_quote": r'["“”]', "apostrophe": r"['’]",
}
FIRST_PERSON = set("i me my mine myself we us our ours ourselves".split())
SECOND_PERSON = set("you your yours yourself yourselves".split())
CONTRACTION = re.compile(r"(?:n't|'(?:m|re|ve|ll|d))$|^(?:it|that|there|here|what|who|where|how|let)'s$")
LIMITATIONS = [
    "English-oriented heuristics, not validated linguistic or authorship measurement.",
    "Unicode word tokens include numbers and contractions; dotted abbreviations may be multiple tokens.",
    "Sentence boundaries are estimated; fragments count, common abbreviations and decimals are protected.",
    "Paragraphs are nonempty blocks separated by blank lines; samples never share boundaries.",
    "Basic Markdown cleanup excludes code, URL destinations, frontmatter and marked blockquotes; complex Markdown, HTML and unmarked quotations need manual cleanup.",
    "Headings detect ATX syntax only; list density counts marked lines, not semantic items.",
    "Punctuation counts retained prose characters, including abbreviation and decimal periods; ellipses count once.",
    "Contractions and pronouns use small English marker lists; ambiguous apostrophe-s forms are conservative.",
    "Aggregate output omits sample text, paths and phrases; it makes no confidence, personality or authorship claims.",
]


def _clean(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    text = re.sub(r"\A---\s*\n.*?\n(?:---|\.\.\.)\s*(?:\n|$)", "", text, flags=re.S)
    kept, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            kept.append("")
        elif marker:
            fence = marker[1]
            kept.append("")
        elif re.match(r"^\s*>|^\s{0,3}\[[^\]]+\]:\s*", line):
            kept.append("")
        else:
            kept.append(line)
    text = "\n".join(kept)
    text = re.sub(r"(`+).*?\1", " ", text, flags=re.S)
    text = re.sub(r"!?\[([^\]]*)\]\([^\n)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", text)
    text = re.sub(r"(?:https?://|www\.)[^\s<>()]+", lambda m: re.search(r"[.!?,;:]*$", m[0])[0], text)
    lines = text.splitlines()
    structure = Counter(nonempty_lines=sum(bool(WORD.search(line)) for line in lines),
                        headings=sum(bool(HEADING.match(line)) and bool(WORD.search(line)) for line in lines),
                        list_items=sum(bool(LIST.match(line)) and bool(WORD.search(line)) for line in lines))
    return "\n".join(LIST.sub("", HEADING.sub("", line)) for line in lines), structure


def _sentence_lengths(paragraph):
    protected = re.sub(r"(?<=\d)\.(?=\d)", "\x00", paragraph)
    protected = ABBREVIATION.sub(lambda m: m[0].replace(".", "\x00"), protected)
    pieces = re.split(r"[.!?…]+[\"”’')\]]*(?:\s+|$)", protected)
    return [count for part in pieces if (count := len(WORD.findall(part.replace("\x00", "."))))]


def _stats(values):
    return {
        "mean": round(statistics.mean(values), 3) if values else 0,
        "median": statistics.median(values) if values else 0,
        "population_stdev": round(statistics.pstdev(values), 3) if values else 0,
        "min": min(values, default=0), "max": max(values, default=0),
    }


def _rate(count, total):
    return round(count * 100 / total, 3) if total else 0


def analyze(samples):
    """Return aggregate JSON-serializable metrics for an iterable of text samples."""
    sentences, paragraphs = [], []
    punctuation, features, structure = Counter(), Counter(), Counter()
    sample_count = empty_count = word_count = 0
    for sample in samples:
        sample_count += 1
        prose, sample_structure = _clean(sample)
        structure.update(sample_structure)
        words = [word.lower().replace("’", "'") for word in WORD.findall(prose)]
        word_count += len(words)
        empty_count += not bool(words)
        for paragraph in re.split(r"\n\s*\n", prose):
            size = len(WORD.findall(paragraph))
            if size:
                paragraphs.append(size)
                sentences.extend(_sentence_lengths(paragraph))
        punctuation.update({name: len(re.findall(pattern, prose)) for name, pattern in PUNCTUATION.items()})
        features["contractions"] += sum(bool(CONTRACTION.search(word)) for word in words)
        features["first_person"] += sum(word.split("'")[0] in FIRST_PERSON for word in words)
        features["second_person"] += sum(word.split("'")[0] in SECOND_PERSON for word in words)
    length_stats = _stats(sentences)
    length_stats["bins"] = {label: sum(low <= value <= high for value in sentences)
                            for label, low, high in [("1-10", 1, 10), ("11-20", 11, 20), ("21-30", 21, 30), ("31+", 31, float("inf"))]}
    return {
        "metadata": {"schema_version": 1, "samples": sample_count, "empty_samples": empty_count,
                     "limitations": LIMITATIONS},
        "counts": {"words": word_count, "sentences": len(sentences), "paragraphs": len(paragraphs)},
        "sentence_length_words": length_stats,
        "paragraph_length_words": _stats(paragraphs),
        "punctuation": {"counts": {key: punctuation[key] for key in PUNCTUATION},
                        "per_100_words": {key: _rate(punctuation[key], word_count) for key in PUNCTUATION}},
        "features": {key: {"count": features[key], "per_100_words": _rate(features[key], word_count)}
                     for key in ["contractions", "first_person", "second_person"]},
        "structure": {**{key: structure[key] for key in ["nonempty_lines", "headings", "list_items"]},
                      "headings_per_100_lines": _rate(structure["headings"], structure["nonempty_lines"]),
                      "list_items_per_100_lines": _rate(structure["list_items"], structure["nonempty_lines"])},
        "warnings": (["No prose words remained after cleanup."] if not word_count else [])
                    + (["One or more samples contained no prose words after cleanup."] if empty_count and word_count else []),
    }


class _PrivateParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, "analyze_voice.py: invalid arguments; use --help.\n")


def main(argv=None):
    parser = _PrivateParser(prog="analyze_voice.py", description=(
        "Read UTF-8 files as separate samples, or stdin as one sample when no paths are given. "
        "Print aggregate JSON only; never write files or include sample text or paths in output. "
        "English-oriented descriptive heuristics; no identity or personality scoring."),
        epilog="Basic Markdown cleanup is approximate. Inspect metadata.limitations in the JSON. "
               "Use -- before filenames beginning with a dash. No raw-text argument is supported.")
    parser.add_argument("paths", nargs="*", metavar="FILE", help="UTF-8 sample files; omit all files to read stdin")
    args = parser.parse_args(argv)
    try:
        samples = [Path(path).read_text(encoding="utf-8") for path in args.paths] if args.paths else [sys.stdin.buffer.read().decode("utf-8")]
    except (OSError, UnicodeError, ValueError):
        print("analyze_voice.py: could not read input as UTF-8; check files or stdin.", file=sys.stderr)
        return 2
    print(json.dumps(analyze(samples), ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
