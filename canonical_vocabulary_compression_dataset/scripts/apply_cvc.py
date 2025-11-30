#!/usr/bin/env python3
"""
Canonical Vocabulary Compression (CVC) Preprocessing Script

This script applies synonym-to-canonical mappings to input text,
implementing the CVC paradigm for both training data preprocessing
and inference-time input normalization.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class CVCProcessor:
    """Processes text using canonical vocabulary compression."""

    def __init__(self, mapping_file: str):
        """
        Initialize CVC processor with synonym mappings.

        Args:
            mapping_file: Path to JSON file containing synonym-to-canonical mappings
        """
        with open(mapping_file, 'r') as f:
            data = json.load(f)

        self.reverse_lookup = data['reverse_lookup']
        self.mappings = data['mappings']
        self.metadata = data.get('metadata', {})

        # Build case-insensitive lookup for better matching
        self.case_insensitive_lookup = {
            k.lower(): v for k, v in self.reverse_lookup.items()
        }

    def process_text(self, text: str, preserve_case: bool = True) -> Tuple[str, Dict]:
        """
        Apply CVC transformation to input text.

        Args:
            text: Input text to process
            preserve_case: Whether to preserve original capitalization

        Returns:
            Tuple of (processed_text, statistics)
        """
        words = text.split()
        processed_words = []
        replacements = []

        for i, word in enumerate(words):
            # Extract word without punctuation
            match = re.match(r'^([^\w]*)(\w+)([^\w]*)$', word)
            if not match:
                processed_words.append(word)
                continue

            prefix, core_word, suffix = match.groups()

            # Check for canonical mapping
            canonical = self._get_canonical(core_word)

            if canonical:
                # Preserve original capitalization pattern
                if preserve_case:
                    canonical = self._preserve_case(core_word, canonical)

                processed_words.append(f"{prefix}{canonical}{suffix}")
                replacements.append({
                    'position': i,
                    'original': core_word,
                    'canonical': canonical
                })
            else:
                processed_words.append(word)

        processed_text = ' '.join(processed_words)

        statistics = {
            'total_words': len(words),
            'replacements_made': len(replacements),
            'replacement_rate': len(replacements) / len(words) if words else 0,
            'replacements': replacements
        }

        return processed_text, statistics

    def _get_canonical(self, word: str) -> Optional[str]:
        """Get canonical form for a word."""
        # Try exact match first
        if word in self.reverse_lookup:
            return self.reverse_lookup[word]

        # Try case-insensitive match
        if word.lower() in self.case_insensitive_lookup:
            return self.case_insensitive_lookup[word.lower()]

        return None

    def _preserve_case(self, original: str, canonical: str) -> str:
        """Preserve the capitalization pattern of original word."""
        if original.isupper():
            return canonical.upper()
        elif original[0].isupper():
            return canonical.capitalize()
        else:
            return canonical.lower()

    def process_file(self, input_file: str, output_file: str) -> Dict:
        """
        Process an entire file with CVC transformation.

        Args:
            input_file: Path to input file
            output_file: Path to output file

        Returns:
            Dictionary of processing statistics
        """
        with open(input_file, 'r') as f:
            lines = f.readlines()

        processed_lines = []
        total_replacements = 0
        total_words = 0

        for line in lines:
            processed_line, stats = self.process_text(line.strip())
            processed_lines.append(processed_line + '\n')
            total_replacements += stats['replacements_made']
            total_words += stats['total_words']

        with open(output_file, 'w') as f:
            f.writelines(processed_lines)

        return {
            'input_file': input_file,
            'output_file': output_file,
            'total_lines': len(lines),
            'total_words': total_words,
            'total_replacements': total_replacements,
            'replacement_rate': total_replacements / total_words if total_words else 0
        }

    def get_vocabulary_stats(self, text_file: str) -> Dict:
        """
        Analyze vocabulary statistics before and after CVC.

        Args:
            text_file: Path to text file to analyze

        Returns:
            Dictionary of vocabulary statistics
        """
        with open(text_file, 'r') as f:
            text = f.read()

        # Original vocabulary
        original_words = re.findall(r'\w+', text.lower())
        original_vocab = set(original_words)

        # Process text
        processed_text, _ = self.process_text(text)
        processed_words = re.findall(r'\w+', processed_text.lower())
        processed_vocab = set(processed_words)

        # Calculate statistics
        vocab_reduction = len(original_vocab) - len(processed_vocab)
        reduction_rate = vocab_reduction / len(original_vocab) if original_vocab else 0

        return {
            'original_vocabulary_size': len(original_vocab),
            'processed_vocabulary_size': len(processed_vocab),
            'vocabulary_reduction': vocab_reduction,
            'reduction_rate': reduction_rate,
            'total_words': len(original_words)
        }


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Apply Canonical Vocabulary Compression to text'
    )
    parser.add_argument(
        '--mapping',
        default='mappings/synonym_to_canonical.json',
        help='Path to synonym-to-canonical mapping file'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input text file to process'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output file for processed text'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Print vocabulary statistics'
    )

    args = parser.parse_args()

    # Initialize processor
    processor = CVCProcessor(args.mapping)

    # Process file
    print(f"Processing {args.input}...")
    stats = processor.process_file(args.input, args.output)

    print(f"\nProcessing complete!")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Total words: {stats['total_words']}")
    print(f"Replacements made: {stats['total_replacements']}")
    print(f"Replacement rate: {stats['replacement_rate']:.2%}")

    if args.stats:
        print("\nVocabulary Statistics:")
        vocab_stats = processor.get_vocabulary_stats(args.input)
        print(f"Original vocabulary size: {vocab_stats['original_vocabulary_size']}")
        print(f"Processed vocabulary size: {vocab_stats['processed_vocabulary_size']}")
        print(f"Vocabulary reduction: {vocab_stats['vocabulary_reduction']}")
        print(f"Reduction rate: {vocab_stats['reduction_rate']:.2%}")


if __name__ == '__main__':
    main()
