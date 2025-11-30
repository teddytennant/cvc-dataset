# Dataset Improvement Roadmap

## High Priority Improvements

### 1. Scale & Validation
- [ ] Expand training corpus from 2,500 to 10,000+ sentences with diverse structures
- [ ] Run actual BERTScore and Sentence-BERT evaluations (currently simulated)
- [ ] Conduct real model training experiments comparing canonical vs original data

### 2. Technical Enhancements
- [ ] Implement context-aware replacement with dependency parsing and phrase whitelisting
- [ ] Add polysemy handling and sense disambiguation for ambiguous synonyms
- [ ] Implement idiom protection and connotation preservation mechanisms

## Medium Priority Improvements

### 3. Coverage Expansion
- [ ] Create domain-specific synonym mappings (medical, legal, technical)
- [ ] Expand benchmark suites with GLUE/SuperGLUE tasks and larger sample sizes

## Low Priority Improvements

### 4. Advanced Features
- [ ] Add multilingual synonym mappings for cross-lingual evaluation
- [ ] Create reproducible training scripts and detailed experimental protocols

## Success Criteria
- Achieve 90%+ meaning preservation rate (currently 73.2%)
- Demonstrate measurable performance improvements in real experiments
- Provide comprehensive documentation and reproducible results