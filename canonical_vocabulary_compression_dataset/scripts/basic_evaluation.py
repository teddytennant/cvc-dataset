#!/usr/bin/env python3
"""
Basic Evaluation Script - First Step
Computes fundamental metrics without heavy ML models
"""

import json
from collections import Counter
from pathlib import Path

def load_text_file(filepath):
    """Load text file and return list of sentences."""
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def compute_vocabulary_stats(texts):
    """Compute vocabulary statistics."""
    all_words = []
    for text in texts:
        words = text.lower().split()
        all_words.extend(words)

    word_counts = Counter(all_words)
    return {
        'total_words': len(all_words),
        'unique_words': len(word_counts),
        'most_common': word_counts.most_common(10)
    }

def compute_replacement_stats(original_texts, canonical_texts, mappings_file):
    """Compute replacement statistics."""
    with open(mappings_file, 'r') as f:
        data = json.load(f)

    mappings = data.get('mappings', {})

    # Create reverse lookup
    reverse_lookup = {}
    for category, mapping_data in mappings.items():
        if 'synonyms' in mapping_data and 'canonical' in mapping_data:
            canonical = mapping_data['canonical'].lower()
            for synonym in mapping_data['synonyms']:
                reverse_lookup[synonym.lower()] = canonical

    total_replacements = 0
    total_words = 0

    for orig, canon in zip(original_texts, canonical_texts):
        orig_words = orig.lower().split()
        canon_words = canon.lower().split()
        total_words += len(orig_words)

        for orig_word, canon_word in zip(orig_words, canon_words):
            if orig_word in reverse_lookup and reverse_lookup[orig_word] == canon_word:
                total_replacements += 1

    return {
        'total_words': total_words,
        'total_replacements': total_replacements,
        'replacement_rate': total_replacements / total_words if total_words > 0 else 0
    }

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Basic CVC evaluation metrics')
    parser.add_argument('--original', required=True, help='Original text file')
    parser.add_argument('--canonical', required=True, help='Canonical text file')
    parser.add_argument('--mappings', required=True, help='Mappings JSON file')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    # Load data
    original_texts = load_text_file(args.original)
    canonical_texts = load_text_file(args.canonical)

    print(f"Loaded {len(original_texts)} sentence pairs")

    # Compute statistics
    orig_vocab = compute_vocabulary_stats(original_texts)
    canon_vocab = compute_vocabulary_stats(canonical_texts)
    replacement_stats = compute_replacement_stats(original_texts, canonical_texts, args.mappings)

    results = {
        'dataset_size': len(original_texts),
        'original_vocabulary': orig_vocab,
        'canonical_vocabulary': canon_vocab,
        'vocabulary_reduction': {
            'words_reduced': orig_vocab['unique_words'] - canon_vocab['unique_words'],
            'reduction_rate': (orig_vocab['unique_words'] - canon_vocab['unique_words']) / orig_vocab['unique_words']
        },
        'replacement_statistics': replacement_stats
    }

    # Print results
    print("\n=== Basic Evaluation Results ===")
    print(f"Dataset size: {results['dataset_size']} sentences")
    print(f"\nVocabulary Statistics:")
    print(f"  Original: {results['original_vocabulary']['unique_words']} unique words")
    print(f"  Canonical: {results['canonical_vocabulary']['unique_words']} unique words")
    print(f"  Reduction: {results['vocabulary_reduction']['words_reduced']} words ({results['vocabulary_reduction']['reduction_rate']:.2%})")
    print(f"\nReplacement Statistics:")
    print(f"  Total replacements: {results['replacement_statistics']['total_replacements']}")
    print(f"  Replacement rate: {results['replacement_statistics']['replacement_rate']:.2%}")

    # Save results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

if __name__ == '__main__':
    main()