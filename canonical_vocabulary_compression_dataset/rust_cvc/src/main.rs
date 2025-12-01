use clap::Parser;
use rust_cvc::CVCProcessor;
use std::process;

#[derive(Parser)]
#[command(name = "cvc")]
#[command(about = "Canonical Vocabulary Compression (CVC) CLI Tool")]
#[command(version = "0.1.0")]
struct Args {
    /// Path to synonym-to-canonical mapping file
    #[arg(short, long, default_value = "mappings/synonym_to_canonical.json")]
    mapping: String,

    /// Input text file to process
    #[arg(short, long)]
    input: String,

    /// Output file for processed text
    #[arg(short, long)]
    output: String,

    /// Print vocabulary statistics
    #[arg(long)]
    stats: bool,

    /// Preserve original capitalization
    #[arg(long, default_value_t = true)]
    preserve_case: bool,
}

fn main() {
    let args = Args::parse();

    // Initialize processor
    let processor = match CVCProcessor::new(&args.mapping) {
        Ok(p) => p,
        Err(e) => {
            eprintln!("Error: Failed to initialize CVC processor: {}", e);
            process::exit(1);
        }
    };

    // Process file
    println!("Processing {}...", args.input);
    match processor.process_file(&args.input, &args.output) {
        Ok(stats) => {
            println!("\nProcessing complete!");
            println!("Total lines: {}", stats.total_lines);
            println!("Total words: {}", stats.total_words);
            println!("Replacements made: {}", stats.total_replacements);
            println!("Replacement rate: {:.2}%", stats.replacement_rate * 100.0);

            if args.stats {
                println!("\nVocabulary Statistics:");
                match processor.get_vocabulary_stats(&args.input) {
                    Ok(vocab_stats) => {
                        println!("Original vocabulary size: {}", vocab_stats.original_vocabulary_size);
                        println!("Processed vocabulary size: {}", vocab_stats.processed_vocabulary_size);
                        println!("Vocabulary reduction: {}", vocab_stats.vocabulary_reduction);
                        println!("Reduction rate: {:.2}%", vocab_stats.reduction_rate * 100.0);
                    }
                    Err(e) => {
                        eprintln!("Warning: Failed to compute vocabulary statistics: {}", e);
                    }
                }
            }
        }
        Err(e) => {
            eprintln!("Error: Failed to process file: {}", e);
            process::exit(1);
        }
    }
}