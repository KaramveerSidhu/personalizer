import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "analyze_voice.py"


class AnalyzeVoiceTests(unittest.TestCase):
    def invoke(self, *paths, text=None):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, paths)],
                              input=text, capture_output=True, text=True)

    def analyze(self, text):
        result = self.invoke(text=text)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def test_basic_counts_and_distribution(self):
        report = self.analyze("I like this. You do too!\n\nWe agree.")
        self.assertEqual(report["counts"], {"words": 8, "sentences": 3, "paragraphs": 2})
        lengths = report["sentence_length_words"]
        self.assertAlmostEqual(lengths["mean"], 8 / 3, places=3)
        self.assertEqual(lengths["median"], 3)
        self.assertAlmostEqual(lengths["population_stdev"], 0.4714, places=3)
        self.assertEqual(lengths["bins"], {"1-10": 3, "11-20": 0, "21-30": 0, "31+": 0})
        self.assertEqual(report["paragraph_length_words"]["mean"], 4)

    def test_unicode_punctuation_and_person_markers(self):
        report = self.analyze("I’m ready—you aren’t. We’ll go… “Really?”")
        self.assertEqual(report["features"]["contractions"]["count"], 3)
        self.assertEqual(report["features"]["first_person"]["count"], 2)
        self.assertEqual(report["features"]["second_person"]["count"], 1)
        punctuation = report["punctuation"]
        self.assertEqual(punctuation["counts"]["em_dash"], 1)
        self.assertEqual(punctuation["counts"]["ellipsis"], 1)
        self.assertEqual(punctuation["counts"]["double_quote"], 2)
        self.assertEqual(punctuation["per_100_words"]["question"], 14.286)

    def test_empty_input_has_zero_values_and_warning(self):
        report = self.analyze(" \n\t")
        self.assertEqual(report["counts"], {"words": 0, "sentences": 0, "paragraphs": 0})
        self.assertEqual(report["sentence_length_words"]["mean"], 0)
        self.assertEqual(report["punctuation"]["per_100_words"]["comma"], 0)
        self.assertTrue(report["warnings"])

    def test_samples_keep_independent_boundaries_and_paths_private(self):
        with tempfile.TemporaryDirectory(prefix="private-voice-") as directory:
            paths = [Path(directory) / "secret-first.txt", Path(directory) / "secret-second.txt"]
            paths[0].write_text("Privatealpha", encoding="utf-8")
            paths[1].write_text("Privatebeta", encoding="utf-8")
            result = self.invoke(*paths)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["metadata"]["samples"], 2)
        self.assertEqual(report["counts"], {"words": 2, "sentences": 2, "paragraphs": 2})
        for private in [directory, "Privatealpha", "Privatebeta", "secret-first"]:
            self.assertNotIn(private, result.stdout + result.stderr)

    def test_markdown_excludes_non_author_prose(self):
        report = self.analyze("""---
title: Should not count
---
Hello `print('code')` [friend](https://secret.example/path).
> Quoted words should not count.

```python
lots of code words
```
~~~
more code words
~~~
[ref]: https://secret.example
Use [this][ref] now.
""")
        self.assertEqual(report["counts"]["words"], 5)
        self.assertEqual(report["counts"]["sentences"], 2)

    def test_bare_urls_do_not_count_as_words_or_destroy_terminal_period(self):
        report = self.analyze("Read https://secret.example/path. Then https://example.org?q=x!")
        self.assertEqual(report["counts"]["words"], 2)
        self.assertEqual(report["counts"]["sentences"], 2)

    def test_decimals_and_common_abbreviations_preserve_sentences(self):
        report = self.analyze("Dr. Smith paid 3.14 dollars, e.g. yesterday. It worked.")
        self.assertEqual(report["counts"]["sentences"], 2)
        self.assertEqual(report["counts"]["words"], 10)

    def test_heading_and_list_density_uses_nonempty_prose_lines(self):
        report = self.analyze("# Heading\n\n- First item\n- Second item\n\nFinal sentence.")
        structure = report["structure"]
        self.assertEqual(structure["nonempty_lines"], 4)
        self.assertEqual(structure["headings"], 1)
        self.assertEqual(structure["list_items"], 2)
        self.assertEqual(structure["headings_per_100_lines"], 25)
        self.assertEqual(structure["list_items_per_100_lines"], 50)

    def test_missing_file_has_private_error_and_no_partial_report(self):
        result = self.invoke("/missing/private-personalizer-file.txt")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("could not read input", result.stderr)
        self.assertNotIn("private-personalizer-file", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_invalid_utf8_has_private_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sensitive.txt"
            path.write_bytes(b"\xffsecret text")
            result = self.invoke(path)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("could not read input", result.stderr)
        self.assertNotIn("secret", result.stderr)
        self.assertNotIn("sensitive", result.stderr)

    def test_help_describes_input_output_and_limits(self):
        result = self.invoke("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for term in ["UTF-8", "stdin", "aggregate", "English", "heuristic"]:
            self.assertIn(term, result.stdout)


if __name__ == "__main__":
    unittest.main()
