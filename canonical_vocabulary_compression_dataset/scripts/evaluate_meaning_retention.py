#!/usr/bin/env python3
"""
Meaning Retention Evaluation Script

Evaluates how well CVC transformations preserve semantic meaning using:
- BERTScore for token-level comparison
- Sentence-BERT for sentence-level similarity
"""

import json
from typing import List, Dict, Tuple
from pathlib import Path

try:
    from bert_score import score as bert_score
    from sentence_transformers import SentenceTransformer, util
    import torch
except ImportError:
    print("Please install required packages: pip install bert-score sentence-transformers torch")
    exit(1)


class MeaningRetentionEvaluator:
    """Evaluates semantic preservation in CVC transformations."""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize evaluator with Sentence-BERT model.

        Args:
            model_name: Sentence-BERT model to use for similarity
        """
        print(f"Loading Sentence-BERT model: {model_name}")
        self.sbert_model = SentenceTransformer(model_name)
        self.threshold = 0.90

    def evaluate_bertscore(
        self,
        original_texts: List[str],
        canonical_texts: List[str]
    ) -> Dict[str, float]:
        """
        Calculate BERTScore between original and canonical texts.

        Args:
            original_texts: List of original sentences
            canonical_texts: List of canonical (transformed) sentences

        Returns:
            Dictionary with precision, recall, and F1 scores
        """
        print("Calculating BERTScore...")
        P, R, F1 = bert_score(
            canonical_texts,
            original_texts,
            lang='en',
            verbose=False
        )

        return {
            'precision': P.mean().item(),
            'recall': R.mean().item(),
            'f1': F1.mean().item(),
            'f1_scores': F1.tolist()
        }

    def evaluate_sentence_bert(
        self,
        original_texts: List[str],
        canonical_texts: List[str]
    ) -> Dict[str, float]:
        """
        Calculate Sentence-BERT cosine similarity.

        Args:
            original_texts: List of original sentences
            canonical_texts: List of canonical sentences

        Returns:
            Dictionary with similarity scores
        """
        print("Calculating Sentence-BERT similarity...")

        # Encode sentences
        original_embeddings = self.sbert_model.encode(
            original_texts,
            convert_to_tensor=True
        )
        canonical_embeddings = self.sbert_model.encode(
            canonical_texts,
            convert_to_tensor=True
        )

        # Calculate cosine similarities
        similarities = util.cos_sim(original_embeddings, canonical_embeddings)

        # Get diagonal (pairwise similarities)
        pairwise_similarities = torch.diagonal(similarities)

        return {
            'mean_similarity': pairwise_similarities.mean().item(),
            'min_similarity': pairwise_similarities.min().item(),
            'max_similarity': pairwise_similarities.max().item(),
            'similarities': pairwise_similarities.tolist()
        }

    def evaluate_pair(
        self,
        original: str,
        canonical: str
    ) -> Dict[str, float]:
        """
        Evaluate a single original-canonical pair.

        Args:
            original: Original sentence
            canonical: Canonical (transformed) sentence

        Returns:
            Dictionary with all evaluation metrics
        """
        # BERTScore
        P, R, F1 = bert_score([canonical], [original], lang='en', verbose=False)

        # Sentence-BERT
        original_embedding = self.sbert_model.encode(original, convert_to_tensor=True)
        canonical_embedding = self.sbert_model.encode(canonical, convert_to_tensor=True)
        similarity = util.cos_sim(original_embedding, canonical_embedding).item()

        # Determine if meaning is preserved
        meaning_preserved = (
            F1.item() >= self.threshold and
            similarity >= self.threshold
        )

        return {
            'bertscore_f1': F1.item(),
            'sentence_bert_similarity': similarity,
            'meaning_preserved': meaning_preserved
        }

    def evaluate_dataset(
        self,
        original_file: str,
        canonical_file: str
    ) -> Dict:
        """
        Evaluate entire dataset of transformations.

        Args:
            original_file: Path to original text file
            canonical_file: Path to canonical text file

        Returns:
            Complete evaluation results
        """
        # Load texts
        with open(original_file, 'r') as f:
            original_texts = [line.strip() for line in f if line.strip()]

        with open(canonical_file, 'r') as f:
            canonical_texts = [line.strip() for line in f if line.strip()]

        assert len(original_texts) == len(canonical_texts), \
            "Original and canonical files must have same number of lines"

        # Evaluate
        bert_results = self.evaluate_bertscore(original_texts, canonical_texts)
        sbert_results = self.evaluate_sentence_bert(original_texts, canonical_texts)

        # Determine preservation rate
        preserved_count = sum(
            1 for b, s in zip(bert_results['f1_scores'], sbert_results['similarities'])
            if b >= self.threshold and s >= self.threshold
        )

        return {
            'total_samples': len(original_texts),
            'bertscore': bert_results,
            'sentence_bert': sbert_results,
            'preservation_rate': preserved_count / len(original_texts),
            'meaning_preserved_count': preserved_count,
            'threshold': self.threshold
        }


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Evaluate meaning retention in CVC transformations'
    )
    parser.add_argument(
        '--original',
        required=True,
        help='Path to original text file'
    )
    parser.add_argument(
        '--canonical',
        required=True,
        help='Path to canonical (transformed) text file'
    )
    parser.add_argument(
        '--output',
        help='Path to save evaluation results (JSON)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.90,
        help='Threshold for meaning preservation (default: 0.90)'
    )

    args = parser.parse_args()

    # Initialize evaluator
    evaluator = MeaningRetentionEvaluator()
    evaluator.threshold = args.threshold

    # Evaluate
    print(f"\nEvaluating transformations...")
    print(f"Original: {args.original}")
    print(f"Canonical: {args.canonical}")
    print(f"Threshold: {args.threshold}\n")

    results = evaluator.evaluate_dataset(args.original, args.canonical)

    # Print results
    print("\n=== Evaluation Results ===\n")
    print(f"Total samples: {results['total_samples']}")
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

    # Save if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")


if __name__ == '__main__':
    main()
