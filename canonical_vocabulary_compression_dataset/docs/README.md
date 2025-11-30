# Canonical Vocabulary Compression (CVC) Dataset

## Overview

This dataset implements the Canonical Vocabulary Compression paradigm for large language model efficiency. CVC preprocesses both training data and user inputs to eliminate lexical redundancy by mapping synonym variants to canonical representations.

## Dataset Structure

```
canonical_vocabulary_compression_dataset/
├── mappings/
│   └── synonym_to_canonical.json          # Core synonym-to-canonical mappings
├── data/
│   ├── sample_training_data_original.txt  # Original training samples
│   └── sample_training_data_canonical.txt # CVC-processed samples
├── evaluation/
│   ├── meaning_retention_scores.json      # BERTScore, Sentence-BERT evaluations
│   └── benchmark_tasks.json               # Evaluation tasks and expected results
├── scripts/
│   └── apply_cvc.py                       # CVC preprocessing implementation
└── docs/
    └── README.md                          # This file
```

## Components

### 1. Synonym-to-Canonical Mappings

**File:** `mappings/synonym_to_canonical.json`

Contains bidirectional mappings between synonym variants and canonical forms:
- **mappings**: Organized by semantic category (size, emotion, verbs, etc.)
- **reverse_lookup**: Fast O(1) lookup from synonym to canonical form
- **metadata**: Version info, sources, statistics

**Example:**
```json
{
  "size_adjectives": {
    "canonical": "big",
    "synonyms": ["large", "huge", "enormous", "gigantic", "massive"],
    "frequency_rank": 1,
    "domain": "general"
  }
}
```

Coverage:
- 250+ total mappings
- 36 semantic categories
- Size, emotion, speed, intelligence, quality adjectives
- Common verbs and nouns
- General domain focus with extensibility for specialized domains

### 2. Training Data Samples

**Original:** `data/sample_training_data_original.txt`
**Canonical:** `data/sample_training_data_canonical.txt`

Parallel corpus of 100 sentences showing:
- Original text with diverse synonym usage
- CVC-transformed text with canonical forms
- Preservation of grammatical structure
- Variety of replacement scenarios

**Example Transformation:**
```
Original:  "The enormous building stood tall, attracting numerous visitors."
Canonical: "The big building stood tall, attracting many visitors."
```

### 3. Meaning Retention Evaluation

**File:** `evaluation/meaning_retention_scores.json`

Contains 20 evaluated transformation samples with:
- **BERTScore F1**: Contextualized token embedding comparison
- **Sentence-BERT Similarity**: Sentence-level semantic similarity
- **Human Ratings**: Expert judgment on meaning preservation
- **Threshold**: 0.90 for acceptable transformations

**Aggregate Statistics:**
- Average BERTScore F1: 0.921
- Average Sentence-BERT: 0.913
- Average Human Rating: 0.902
- **95% meaning preservation rate**

**Problematic Cases Identified:**
1. Idiomatic expressions ("warm welcome" → "hot welcome")
2. Connotation loss ("stroll" → "walk")
3. Intensity reduction ("magnificent" → "big")
4. Grammatical awkwardness ("tremendous speed" → "very speed")

### 4. Benchmark Tasks

**File:** `evaluation/benchmark_tasks.json`

Comprehensive evaluation framework:

- **Classification Tasks**: Sentiment and topic classification with original/canonical pairs
- **Semantic Similarity**: Measuring consistency improvements
- **Question Answering**: Comprehension testing
- **Generation Quality**: Assessing coherence vs. diversity trade-offs
- **Robustness Testing**: Synonym variant consistency
- **Fine-tuning Efficiency**: Convergence speed and data requirements

**Expected Results:**
- Classification: 2-5% accuracy improvement
- Semantic Similarity: 3-7% improvement
- Fine-tuning: 30-50% faster convergence, 20-30% less data
- Robustness: Perfect consistency across synonym variants

### 5. CVC Preprocessing Script

**File:** `scripts/apply_cvc.py`

Python implementation of CVC preprocessing:

**Features:**
- Case-preserving transformations
- O(1) lookup performance
- Batch file processing
- Vocabulary statistics analysis
- Detailed replacement tracking

**Usage:**
```bash
python scripts/apply_cvc.py \
  --mapping mappings/synonym_to_canonical.json \
  --input your_data.txt \
  --output processed_data.txt \
  --stats
```

**Output:**
- Processed text file
- Replacement statistics
- Vocabulary reduction metrics

## Theoretical Framework

### Core Hypothesis

Eliminating lexical variation at the input stage reduces model burden of learning synonym equivalence, enabling:

1. **Reduced Vocabulary Size**: Fewer unique tokens decrease embedding dimensions
2. **Improved Semantic Consistency**: Stronger representations for canonical forms
3. **Higher Task Accuracy**: Concentrated training reduces confusion
4. **Enhanced Fine-tuning Efficiency**: Gradient concentration accelerates adaptation
5. **Robust Inference**: Input normalization ensures comprehension of all variants
6. **Faster Convergence**: Less redundant information accelerates learning

### Methodology

**Stage 1: Mapping Construction**
- WordNet synset analysis
- Frequency-based canonical selection
- Expert curation for critical terms

**Stage 2: Meaning Retention Scoring**
- BERTScore for token-level comparison
- Sentence-BERT for sentence-level similarity
- Human evaluation for ground truth
- 0.90 threshold for acceptable transformations

**Stage 3: Training Data Preprocessing**
- Systematic synonym replacement
- Grammatical structure preservation
- Meaning retention validation
- Vocabulary reduction tracking

**Stage 4: Input Normalization**
- Inference-time transformation
- Zero out-of-vocabulary synonyms
- Consistent model behavior
- Transparent user experience

## Usage Guidelines

### For Training

1. **Load mappings:**
```python
from scripts.apply_cvc import CVCProcessor
processor = CVCProcessor('mappings/synonym_to_canonical.json')
```

2. **Process training data:**
```python
stats = processor.process_file('train.txt', 'train_canonical.txt')
print(f"Replacement rate: {stats['replacement_rate']:.2%}")
```

3. **Train model on canonical data:**
- Build tokenizer vocabulary from processed text
- Standard next-token prediction
- Exclude non-canonical synonyms from vocabulary

### For Inference

1. **Normalize user input:**
```python
user_input = "Show me enormous buildings"
normalized_input, stats = processor.process_text(user_input)
# normalized_input: "Show me big buildings"
```

2. **Process with model:**
```python
response = model.generate(normalized_input)
```

3. **Return to user:**
- Model comprehends canonical form
- User experiences natural interaction
- No out-of-vocabulary errors

### Vocabulary Analysis

```python
vocab_stats = processor.get_vocabulary_stats('corpus.txt')
print(f"Vocabulary reduction: {vocab_stats['reduction_rate']:.2%}")
```

## Evaluation Protocol

### 1. Baseline Comparison

- Train identical architectures on original vs. canonical corpora
- Control training steps, batch sizes, hyperparameters
- Measure on standard benchmarks (GLUE, SuperGLUE)

### 2. Metrics

- **Accuracy**: Classification performance on synonym-rich inputs
- **Consistency**: Embedding similarity for synonym variants
- **Robustness**: Performance degradation with non-canonical vocabulary
- **Convergence**: Steps to target validation performance
- **Data Efficiency**: Minimum dataset size for adaptation
- **Generation Quality**: Human evaluation of coherence and naturalness

### 3. Statistical Rigor

- Multiple random seeds
- Confidence intervals
- Significance tests (t-tests, bootstrap)
- Variance analysis across model sizes

## Challenges and Mitigations

### Polysemy and Context Sensitivity

**Challenge:** Many synonyms aren't truly interchangeable (e.g., "big deal" vs. "large deal")

**Mitigation:**
- Context-aware replacement using dependency parsing
- Whitelist protected phrases and idioms
- Sense disambiguation for polysemous terms

### Loss of Stylistic Variation

**Challenge:** Repetitive generation, reduced expressiveness

**Mitigation:**
- Hybrid approach: canonical training + style fine-tuning
- Separate generation module for variant expansion
- Domain-specific granularity adjustment

### Granularity Selection

**Challenge:** Determining appropriate semantic clustering

**Mitigation:**
- Hierarchical clustering with multiple levels
- Domain-specific tuning
- Ablation studies on cluster granularity

## Future Directions

1. **Multilingual Extension**: Cross-lingual synonym mapping
2. **Dynamic Vocabulary**: Adaptive canonical mappings
3. **Generative Expansion**: Post-processing for stylistic variation
4. **Integration**: Combine with quantization, pruning, distillation
5. **Domain Specialization**: Medical, legal, scientific vocabularies

## Citation

If you use this dataset, please cite:

```
@dataset{cvc_dataset_2025,
  title={Canonical Vocabulary Compression Dataset},
  author={Research Community},
  year={2025},
  description={Dataset for evaluating canonical vocabulary compression in LLMs}
}
```

## Important Notes

⚠️ **Research Status**: CVC is a proposed paradigm requiring extensive empirical validation. The theoretical benefits outlined must be confirmed through rigorous testing across diverse benchmarks and model architectures.

⚠️ **Meaning Preservation**: While 95% of transformations in this dataset preserve meaning acceptably, careful validation is essential for production use.

⚠️ **Domain Specificity**: Current mappings focus on general domain. Specialized domains require customized synonym mappings.

## License

This dataset is released for research purposes. Please refer to the LICENSE file for terms of use.

## Contributing

We welcome contributions to expand:
- Synonym mappings (especially domain-specific)
- Evaluation benchmarks
- Meaning retention validation
- Implementation improvements

## Contact

For questions, issues, or contributions, please open an issue in the repository.

---

**Version:** 1.0
**Last Updated:** 2025-11-30
**Status:** Research Dataset - Empirical Validation Required
