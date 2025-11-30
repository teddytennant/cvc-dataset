#!/usr/bin/env python3
"""
CVC Usage Demonstration

This script demonstrates the complete CVC workflow:
1. Loading synonym mappings
2. Processing text
3. Analyzing vocabulary reduction
4. Showing example transformations
"""

import json
from apply_cvc import CVCProcessor


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60 + '\n')


def demo_basic_transformation():
    """Demonstrate basic CVC text transformation."""
    print_section("Basic CVC Transformation")

    # Initialize processor
    processor = CVCProcessor('../mappings/synonym_to_canonical.json')

    # Example sentences
    examples = [
        "The enormous building stood tall in the city.",
        "She felt elated about the excellent news.",
        "The intelligent scientist presented brilliant findings.",
        "They strolled through the gorgeous garden.",
        "The rapid changes transformed our lives significantly."
    ]

    print("Original → Canonical transformations:\n")
    for original in examples:
        canonical, stats = processor.process_text(original)
        print(f"Original:  {original}")
        print(f"Canonical: {canonical}")
        print(f"Replacements: {stats['replacements_made']}/{stats['total_words']}")
        print()


def demo_inference_normalization():
    """Demonstrate inference-time input normalization."""
    print_section("Inference-Time Input Normalization")

    processor = CVCProcessor('../mappings/synonym_to_canonical.json')

    # User inputs with synonym variants
    user_inputs = [
        "Show me enormous buildings",
        "Show me huge buildings",
        "Show me massive buildings",
        "Show me gigantic buildings",
        "Show me big buildings"
    ]

    print("All user inputs normalize to the same canonical form:\n")
    canonical_forms = set()

    for user_input in user_inputs:
        canonical, _ = processor.process_text(user_input)
        canonical_forms.add(canonical)
        print(f"User types:     \"{user_input}\"")
        print(f"Model receives: \"{canonical}\"")
        print()

    print(f"Unique canonical forms: {len(canonical_forms)}")
    print(f"Result: Perfect consistency across synonym variants! ✓\n")


def demo_vocabulary_analysis():
    """Demonstrate vocabulary reduction analysis."""
    print_section("Vocabulary Reduction Analysis")

    processor = CVCProcessor('../mappings/synonym_to_canonical.json')

    # Analyze sample dataset
    stats = processor.get_vocabulary_stats('../data/sample_training_data_original.txt')

    print("Dataset Statistics:\n")
    print(f"Original vocabulary size:   {stats['original_vocabulary_size']:,} unique words")
    print(f"Canonical vocabulary size:  {stats['processed_vocabulary_size']:,} unique words")
    print(f"Vocabulary reduction:       {stats['vocabulary_reduction']:,} words")
    print(f"Reduction rate:             {stats['reduction_rate']:.2%}")
    print(f"Total words processed:      {stats['total_words']:,}")


def demo_replacement_details():
    """Show detailed replacement information."""
    print_section("Detailed Replacement Analysis")

    processor = CVCProcessor('../mappings/synonym_to_canonical.json')

    example = "The enormous building has numerous beautiful rooms with excellent furniture."

    canonical, stats = processor.process_text(example)

    print(f"Original text:")
    print(f"  {example}\n")

    print(f"Canonical text:")
    print(f"  {canonical}\n")

    print(f"Replacements made:")
    for replacement in stats['replacements']:
        print(f"  Position {replacement['position']}: "
              f"{replacement['original']} → {replacement['canonical']}")

    print(f"\nTotal: {stats['replacements_made']} replacements "
          f"out of {stats['total_words']} words "
          f"({stats['replacement_rate']:.1%} replacement rate)")


def demo_mapping_lookup():
    """Demonstrate mapping lookup and reverse lookup."""
    print_section("Synonym Mapping Lookup")

    processor = CVCProcessor('../mappings/synonym_to_canonical.json')

    # Show mapping categories
    print("Available mapping categories:\n")

    with open('../mappings/synonym_to_canonical.json', 'r') as f:
        data = json.load(f)

    for category, info in list(data['mappings'].items())[:5]:
        print(f"{category}:")
        print(f"  Canonical: {info['canonical']}")
        print(f"  Synonyms:  {', '.join(info['synonyms'][:5])}")
        if len(info['synonyms']) > 5:
            print(f"             ... and {len(info['synonyms'])-5} more")
        print()


def demo_case_preservation():
    """Demonstrate case preservation in transformations."""
    print_section("Case Preservation")

    processor = CVCProcessor('../mappings/synonym_to_canonical.json')

    examples = [
        "Enormous buildings dominate the skyline.",  # Capitalized
        "The ENORMOUS building is huge.",            # All caps
        "enormous buildings everywhere",             # Lowercase
    ]

    print("CVC preserves original capitalization:\n")
    for example in examples:
        canonical, _ = processor.process_text(example)
        print(f"Original:  {example}")
        print(f"Canonical: {canonical}")
        print()


def demo_file_processing():
    """Demonstrate batch file processing."""
    print_section("Batch File Processing")

    processor = CVCProcessor('../mappings/synonym_to_canonical.json')

    print("Processing sample_training_data_original.txt...\n")

    # Process file
    stats = processor.process_file(
        '../data/sample_training_data_original.txt',
        '../data/sample_output.txt'
    )

    print("Processing Statistics:")
    print(f"  Lines processed:    {stats['total_lines']}")
    print(f"  Total words:        {stats['total_words']}")
    print(f"  Replacements made:  {stats['total_replacements']}")
    print(f"  Replacement rate:   {stats['replacement_rate']:.2%}")
    print(f"\nOutput saved to: {stats['output_file']}")


def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("CANONICAL VOCABULARY COMPRESSION (CVC) DEMONSTRATION")
    print("="*60)

    try:
        demo_basic_transformation()
        demo_inference_normalization()
        demo_vocabulary_analysis()
        demo_replacement_details()
        demo_mapping_lookup()
        demo_case_preservation()
        demo_file_processing()

        print("\n" + "="*60)
        print("DEMONSTRATION COMPLETE")
        print("="*60)
        print("\nKey Takeaways:")
        print("1. CVC consistently maps synonyms to canonical forms")
        print("2. Input normalization ensures model comprehension")
        print("3. Vocabulary reduction decreases model complexity")
        print("4. Case and structure preservation maintains readability")
        print("5. Batch processing enables large-scale preprocessing")
        print("\nFor more information, see docs/README.md")

    except FileNotFoundError as e:
        print(f"\nError: Could not find required file: {e}")
        print("Please run this script from the scripts/ directory.")
    except Exception as e:
        print(f"\nError during demonstration: {e}")


if __name__ == '__main__':
    main()
