#!/usr/bin/env python3
"""
Rust-accelerated Canonical Vocabulary Compression (CVC) Preprocessing Script

This script uses the high-performance Rust implementation for CVC processing.
"""

import json
import subprocess
import tempfile
import os
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class RustCVCProcessor:
    """CVC processor using the Rust CLI tool for high performance."""

    def __init__(self, mapping_file: str, rust_binary_path: Optional[str] = None):
        """
        Initialize Rust CVC processor.

        Args:
            mapping_file: Path to JSON file containing synonym-to-canonical mappings
            rust_binary_path: Path to the rust_cvc binary (auto-detected if None)
        """
        self.mapping_file = mapping_file

        if rust_binary_path is None:
            # Auto-detect the binary path
            script_dir = Path(__file__).parent
            rust_dir = script_dir.parent / "rust_cvc"
            rust_binary_path = str(rust_dir / "target" / "release" / "rust_cvc")

        rust_binary_path_obj = Path(rust_binary_path)
        if not rust_binary_path_obj.exists():
            raise FileNotFoundError(f"Rust binary not found at: {rust_binary_path}")

        self.rust_binary = rust_binary_path

    def process_text(self, text: str, preserve_case: bool = True) -> Tuple[str, Dict]:
        """
        Apply CVC transformation to input text using Rust.

        Args:
            text: Input text to process
            preserve_case: Whether to preserve original capitalization

        Returns:
            Tuple of (processed_text, statistics)
        """
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as input_file:
            input_file.write(text)
            input_file_path = input_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as output_file:
            output_file_path = output_file.name

        try:
            # Run Rust CLI
            cmd = [
                self.rust_binary,
                "--mapping", self.mapping_file,
                "--input", input_file_path,
                "--output", output_file_path
            ]

            if preserve_case:
                cmd.append("--preserve-case")

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Read the processed text
            with open(output_file_path, 'r') as f:
                processed_text = f.read()

            # Parse statistics from stdout (this is a simplified version)
            # In a real implementation, we'd modify the Rust CLI to output JSON stats
            stats = {
                'total_words': len(text.split()),
                'replacements_made': 0,  # Would need to parse from Rust output
                'replacement_rate': 0.0,
                'replacements': []
            }

            return processed_text, stats

        finally:
            # Clean up temporary files
            try:
                os.unlink(input_file_path)
                os.unlink(output_file_path)
            except OSError:
                pass

    def process_file(self, input_file: str, output_file: str) -> Dict:
        """
        Process an entire file with CVC transformation using Rust.

        Args:
            input_file: Path to input file
            output_file: Path to output file

        Returns:
            Dictionary of processing statistics
        """
        cmd = [
            self.rust_binary,
            "--mapping", self.mapping_file,
            "--input", input_file,
            "--output", output_file,
            "--stats"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Parse the output to extract statistics
        # This is a simplified parser - in production you'd want more robust parsing
        lines = result.stdout.strip().split('\n')
        stats = {}

        for line in lines:
            if line.startswith("Total lines:"):
                stats['total_lines'] = int(line.split(": ")[1])
            elif line.startswith("Total words:"):
                stats['total_words'] = int(line.split(": ")[1])
            elif line.startswith("Replacements made:"):
                stats['total_replacements'] = int(line.split(": ")[1])
            elif line.startswith("Replacement rate:"):
                stats['replacement_rate'] = float(line.split(": ")[1].rstrip('%')) / 100.0
            elif line.startswith("Original vocabulary size:"):
                stats['original_vocabulary_size'] = int(line.split(": ")[1])
            elif line.startswith("Processed vocabulary size:"):
                stats['processed_vocabulary_size'] = int(line.split(": ")[1])
            elif line.startswith("Vocabulary reduction:"):
                stats['vocabulary_reduction'] = int(line.split(": ")[1])
            elif line.startswith("Reduction rate:"):
                stats['reduction_rate'] = float(line.split(": ")[1].rstrip('%')) / 100.0

        return stats

    def get_vocabulary_stats(self, text_file: str) -> Dict:
        """
        Analyze vocabulary statistics before and after CVC.

        Args:
            text_file: Path to text file to analyze

        Returns:
            Dictionary of vocabulary statistics
        """
        # For now, we'll process the file and return the stats
        # In a more sophisticated implementation, we'd have a separate Rust function
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_output = temp_file.name

        try:
            stats = self.process_file(text_file, temp_output)
            # Extract vocabulary-related stats
            vocab_stats = {
                'original_vocabulary_size': stats.get('original_vocabulary_size', 0),
                'processed_vocabulary_size': stats.get('processed_vocabulary_size', 0),
                'vocabulary_reduction': stats.get('vocabulary_reduction', 0),
                'reduction_rate': stats.get('reduction_rate', 0.0),
                'total_words': stats.get('total_words', 0)
            }
            return vocab_stats
        finally:
            try:
                os.unlink(temp_output)
            except OSError:
                pass


# Backwards compatibility - alias the old class name
CVCProcessor = RustCVCProcessor


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Apply Canonical Vocabulary Compression to text (Rust accelerated)'
    )
    parser.add_argument(
        '--mapping',
        default='../mappings/synonym_to_canonical.json',
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
    parser.add_argument(
        '--rust-binary',
        help='Path to rust_cvc binary (auto-detected if not provided)'
    )

    args = parser.parse_args()

    # Initialize processor
    processor = RustCVCProcessor(args.mapping, args.rust_binary)

    # Process file
    print(f"Processing {args.input}...")
    stats = processor.process_file(args.input, args.output)

    print("\nProcessing complete!")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Total words: {stats['total_words']}")
    print(f"Replacements made: {stats['total_replacements']}")
    print(".2%")

    if args.stats:
        print("\nVocabulary Statistics:")
        vocab_stats = processor.get_vocabulary_stats(args.input)
        print(f"Original vocabulary size: {vocab_stats['original_vocabulary_size']}")
        print(f"Processed vocabulary size: {vocab_stats['processed_vocabulary_size']}")
        print(f"Vocabulary reduction: {vocab_stats['vocabulary_reduction']}")
        print(".2%")


if __name__ == '__main__':
    main()