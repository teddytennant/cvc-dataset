# Canonical Vocabulary Compression (CVC) Dataset

A research dataset for evaluating canonical vocabulary compression in large language models. CVC preprocesses training data and user inputs to eliminate lexical redundancy by mapping synonyms to canonical forms.

For a detailed exploration of the methodology, see the [CVC paper](https://theodoretennant.vercel.app/papers/vocabulary-compression-paper.html).

## Quick Start

```bash
cd canonical_vocabulary_compression_dataset/scripts
pip install -r requirements.txt
python demo_usage.py
```

```python
from scripts.apply_cvc import CVCProcessor

processor = CVCProcessor('mappings/synonym_to_canonical.json')
canonical, stats = processor.process_text("The enormous building has numerous beautiful rooms.")
# Output: "The big building has many beautiful rooms."
```

## Dataset Contents

- **250+ synonym mappings** across 36 semantic categories
- **100 sample training pairs** (original + canonical)
- **Evaluation benchmarks** for classification, similarity, QA, and generation
- **Python tools** for preprocessing and evaluation

See [`canonical_vocabulary_compression_dataset/README.md`](canonical_vocabulary_compression_dataset/README.md) for full documentation.

## License

MIT License - see LICENSE file for details.
