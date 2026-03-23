"""Tests for CVCProcessor."""

import json
import os
import sys
import tempfile

import pytest

# Add scripts to path
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "canonical_vocabulary_compression_dataset",
        "scripts",
    ),
)
from apply_cvc import CVCProcessor

MAPPING_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "canonical_vocabulary_compression_dataset",
    "mappings",
    "synonym_to_canonical.json",
)


@pytest.fixture
def processor():
    """Create a CVCProcessor with the real mapping file."""
    return CVCProcessor(MAPPING_PATH)


@pytest.fixture
def mini_processor(tmp_path):
    """Create a CVCProcessor with a minimal test mapping."""
    mapping = {
        "metadata": {"version": "test", "total_synonyms": 4},
        "mappings": {
            "size_big": {
                "canonical": "big",
                "synonyms": ["large", "huge", "enormous"],
            },
            "speed_fast": {
                "canonical": "fast",
                "synonyms": ["quick", "rapid", "swift"],
            },
        },
        "reverse_lookup": {
            "large": "big",
            "huge": "big",
            "enormous": "big",
            "quick": "fast",
            "rapid": "fast",
            "swift": "fast",
        },
    }
    path = tmp_path / "test_mappings.json"
    path.write_text(json.dumps(mapping))
    return CVCProcessor(str(path))


# === Basic text processing ===


class TestProcessText:
    def test_synonym_replaced(self, mini_processor):
        result, stats = mini_processor.process_text("The house is enormous")
        assert result == "The house is big"
        assert stats["replacements_made"] == 1

    def test_no_replacement_for_canonical(self, mini_processor):
        result, stats = mini_processor.process_text("The house is big")
        assert result == "The house is big"
        assert stats["replacements_made"] == 0

    def test_unknown_word_unchanged(self, mini_processor):
        result, _ = mini_processor.process_text("The cat sat quietly")
        assert result == "The cat sat quietly"

    def test_multiple_replacements(self, mini_processor):
        result, stats = mini_processor.process_text("A huge and rapid change")
        assert result == "A big and fast change"
        assert stats["replacements_made"] == 2

    def test_empty_string(self, mini_processor):
        result, stats = mini_processor.process_text("")
        assert result == ""
        assert stats["replacements_made"] == 0
        assert stats["total_words"] == 0

    def test_single_synonym_word(self, mini_processor):
        result, _ = mini_processor.process_text("enormous")
        assert result == "big"

    def test_punctuation_preserved(self, mini_processor):
        result, stats = mini_processor.process_text('"enormous!"')
        assert result == '"big!"'
        assert stats["replacements_made"] == 1

    def test_parentheses_preserved(self, mini_processor):
        result, _ = mini_processor.process_text("(huge)")
        assert result == "(big)"

    def test_statistics_replacement_rate(self, mini_processor):
        _, stats = mini_processor.process_text("huge big cat")
        assert stats["total_words"] == 3
        assert stats["replacements_made"] == 1
        assert abs(stats["replacement_rate"] - 1 / 3) < 0.001


# === Case preservation ===


class TestCasePreservation:
    def test_lowercase_preserved(self, mini_processor):
        result, _ = mini_processor.process_text("enormous")
        assert result == "big"

    def test_capitalized_preserved(self, mini_processor):
        result, _ = mini_processor.process_text("Enormous")
        assert result == "Big"

    def test_uppercase_preserved(self, mini_processor):
        result, _ = mini_processor.process_text("ENORMOUS")
        assert result == "BIG"

    def test_preserve_case_disabled(self, mini_processor):
        result, _ = mini_processor.process_text("ENORMOUS", preserve_case=False)
        assert result == "big"

    def test_empty_canonical_returns_canonical(self, mini_processor):
        # _preserve_case should handle empty strings gracefully
        assert mini_processor._preserve_case("", "big") == "big"
        assert mini_processor._preserve_case("word", "") == ""


# === Hyphenated word processing ===


class TestHyphenatedWords:
    def test_hyphenated_part_replaced(self, mini_processor):
        result, stats = mini_processor.process_text("an enormous-scale thing")
        assert result == "an big-scale thing"
        assert stats["replacements_made"] == 1

    def test_multiple_hyphenated_parts(self, mini_processor):
        result, _ = mini_processor.process_text("a huge-and-rapid process")
        assert result == "a big-and-fast process"

    def test_no_hyphenated_match(self, mini_processor):
        result, _ = mini_processor.process_text("a well-known fact")
        assert result == "a well-known fact"

    def test_hyphenated_with_punctuation(self, mini_processor):
        result, _ = mini_processor.process_text('"enormous-scale"')
        assert result == '"big-scale"'


# === File processing ===


class TestFileProcessing:
    def test_process_file(self, mini_processor, tmp_path):
        input_file = tmp_path / "input.txt"
        output_file = tmp_path / "output.txt"
        input_file.write_text("The enormous cat.\nA rapid fox.\n")

        stats = mini_processor.process_file(str(input_file), str(output_file))

        output = output_file.read_text()
        assert "big" in output
        assert "fast" in output
        assert stats["total_lines"] == 2
        assert stats["total_replacements"] == 2

    def test_process_empty_file(self, mini_processor, tmp_path):
        input_file = tmp_path / "empty.txt"
        output_file = tmp_path / "out.txt"
        input_file.write_text("")

        stats = mini_processor.process_file(str(input_file), str(output_file))
        assert stats["total_lines"] == 0
        assert stats["total_replacements"] == 0


# === Real mapping integration ===


class TestRealMappings:
    def test_loads_real_mappings(self, processor):
        assert len(processor.reverse_lookup) > 0

    def test_known_synonym(self, processor):
        """Test that a known synonym from the real mappings is replaced."""
        result, stats = processor.process_text("The building was enormous")
        assert "big" in result.lower() or stats["replacements_made"] > 0

    def test_real_case_insensitive(self, processor):
        canonical = processor._get_canonical("Enormous")
        assert canonical is not None
