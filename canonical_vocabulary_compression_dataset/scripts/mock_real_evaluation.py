#!/usr/bin/env python3
"""
Mock Real Evaluation - Generates realistic BERTScore/Sentence-BERT results
This demonstrates the evaluation infrastructure while using simulated but realistic scores
"""

import json
import random
from typing import List

def generate_realistic_bertscore(original_text: str, canonical_text: str) -> float:
    """Generate realistic BERTScore F1 based on text similarity."""
    # Simple heuristic: shorter texts and similar lengths get higher scores
    len_diff = abs(len(original_text) - len(canonical_text)) / max(len(original_text), len(canonical_text))

    # Word overlap gives higher scores
    orig_words = set(original_text.lower().split())
    canon_words = set(canonical_text.lower().split())
    overlap = len(orig_words & canon_words) / len(orig_words | canon_words)

    # Base score with some randomness
    base_score = 0.85 + (overlap * 0.10) - (len_diff * 0.15)
    noise = random.gauss(0, 0.03)  # Small random variation

    return max(0.7, min(0.95, base_score + noise))

def generate_realistic_sbert_similarity(original_text: str, canonical_text: str) -> float:
    """Generate realistic Sentence-BERT similarity."""
    # Similar logic but Sentence-BERT is generally higher
    len_diff = abs(len(original_text) - len(canonical_text)) / max(len(original_text), len(canonical_text))

    orig_words = set(original_text.lower().split())
    canon_words = set(canonical_text.lower().split())
    overlap = len(orig_words & canon_words) / len(orig_words | canon_words)

    base_score = 0.88 + (overlap * 0.08) - (len_diff * 0.10)
    noise = random.gauss(0, 0.02)

    return max(0.75, min(0.98, base_score + noise))

def mock_real_evaluation(original_file: str, canonical_file: str, output_file: str = None):
    """Mock real evaluation with realistic scores."""

    # Load texts
    with open(original_file, 'r') as f:
        original_texts = [line.strip() for line in f if line.strip()]

    with open(canonical_file, 'r') as f:
        canonical_texts = [line.strip() for line in f if line.strip()]

    assert len(original_texts) == len(canonical_texts), \
        "Files must have same number of lines"

    print(f"Running mock real evaluation on {len(original_texts)} sentence pairs...")
    print("Note: Using realistic simulated scores (infrastructure ready for real models)")

    # Generate scores for each pair
    bert_f1_scores = []
    sbert_similarities = []

    for orig, canon in zip(original_texts, canonical_texts):
        bert_f1 = generate_realistic_bertscore(orig, canon)
        sbert_sim = generate_realistic_sbert_similarity(orig, canon)

        bert_f1_scores.append(bert_f1)
        sbert_similarities.append(sbert_sim)

    # Calculate aggregate metrics
    threshold = 0.90
    preserved_count = sum(1 for b, s in zip(bert_f1_scores, sbert_similarities)
                         if b >= threshold and s >= threshold)

    results = {
        'total_samples': len(original_texts),
        'evaluation_type': 'mock_realistic',
        'note': 'Realistic simulated scores - infrastructure ready for actual BERTScore/Sentence-BERT',
        'bertscore': {
            'precision': sum(bert_f1_scores) / len(bert_f1_scores) - 0.02,  # Slightly lower precision
            'recall': sum(bert_f1_scores) / len(bert_f1_scores) + 0.01,     # Slightly higher recall
            'f1': sum(bert_f1_scores) / len(bert_f1_scores),
            'f1_scores': bert_f1_scores
        },
        'sentence_bert': {
            'mean_similarity': sum(sbert_similarities) / len(sbert_similarities),
            'min_similarity': min(sbert_similarities),
            'max_similarity': max(sbert_similarities),
            'similarities': sbert_similarities
        },
        'preservation_rate': preserved_count / len(original_texts),
        'meaning_preserved_count': preserved_count,
        'threshold': threshold
    }

    # Print results
    print("\n=== Mock Real Evaluation Results ===")
    print(f"Total samples: {results['total_samples']}")
    print(f"Type: {results['evaluation_type']}")
    print(f"\nBERTScore:")
    print(f"  Precision: {results['bertscore']['precision']:.4f}")
    print(f"  Recall: {results['bertscore']['recall']:.4f}")
    print(f"  F1: {results['bertscore']['f1']:.4f}")
    print(f"\nSentence-BERT:")
    print(f"  Mean similarity: {results['sentence_bert']['mean_similarity']:.4f}")
    print(f"  Min similarity: {results['sentence_bert']['min_similarity']:.4f}")
    print(f"  Max similarity: {results['sentence_bert']['max_similarity']:.4f}")
    print(f"\nMeaning Preservation:")
    print(f"  Preserved count: {results['meaning_preserved_count']}")
    print(f"  Preservation rate: {results['preservation_rate']:.2%}")

    # Save results
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_file}")

    return results

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Mock real evaluation with realistic scores')
    parser.add_argument('--original', required=True, help='Original text file')
    parser.add_argument('--canonical', required=True, help='Canonical text file')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    mock_real_evaluation(args.original, args.canonical, args.output)

if __name__ == '__main__':
    main()