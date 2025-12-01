use std::collections::HashMap;
use regex::Regex;
use serde::{Deserialize, Serialize};
use anyhow::{Result, Context};

#[cfg(feature = "python")]
mod python;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MappingInfo {
    pub canonical: String,
    pub synonyms: Vec<String>,
    pub frequency_rank: u32,
    pub domain: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Metadata {
    pub version: String,
    pub description: String,
    pub creation_date: String,
    pub total_mappings: u32,
    pub sources: Vec<String>,
    pub total_synonyms: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MappingsData {
    pub metadata: Metadata,
    pub mappings: HashMap<String, MappingInfo>,
    pub reverse_lookup: HashMap<String, String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Replacement {
    pub position: usize,
    pub original: String,
    pub canonical: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessingStats {
    pub total_words: usize,
    pub replacements_made: usize,
    pub replacement_rate: f64,
    pub replacements: Vec<Replacement>,
}

#[derive(Debug)]
pub struct CVCProcessor {
    reverse_lookup: HashMap<String, String>,
    mappings: HashMap<String, MappingInfo>,
    metadata: Metadata,
    case_insensitive_lookup: HashMap<String, String>,
    word_regex: Regex,
}

impl CVCProcessor {
    pub fn new(mapping_file: &str) -> Result<Self> {
        let data: MappingsData = serde_json::from_reader(
            std::fs::File::open(mapping_file)
                .with_context(|| format!("Failed to open mapping file: {}", mapping_file))?
        ).with_context(|| format!("Failed to parse JSON from: {}", mapping_file))?;

        let case_insensitive_lookup = data.reverse_lookup
            .iter()
            .map(|(k, v)| (k.to_lowercase(), v.clone()))
            .collect();

        let word_regex = Regex::new(r"^([^\w]*)(\w+)([^\w]*)$")
            .context("Failed to compile word regex")?;

        Ok(CVCProcessor {
            reverse_lookup: data.reverse_lookup,
            mappings: data.mappings,
            metadata: data.metadata,
            case_insensitive_lookup,
            word_regex,
        })
    }

    pub fn process_text(&self, text: &str, preserve_case: bool) -> Result<(String, ProcessingStats)> {
        let words: Vec<&str> = text.split_whitespace().collect();
        let mut processed_words = Vec::with_capacity(words.len());
        let mut replacements = Vec::new();

        for (i, word) in words.iter().enumerate() {
            if let Some((prefix, core_word, suffix)) = self.extract_word_parts(word) {
                if let Some(canonical) = self.get_canonical(core_word) {
                    let processed_word = if preserve_case {
                        format!("{}{}{}", prefix, self.preserve_case(core_word, &canonical), suffix)
                    } else {
                        format!("{}{}{}", prefix, canonical, suffix)
                    };

                    processed_words.push(processed_word);
                    replacements.push(Replacement {
                        position: i,
                        original: core_word.to_string(),
                        canonical: canonical.to_string(),
                    });
                } else {
                    processed_words.push(word.to_string());
                }
            } else {
                processed_words.push(word.to_string());
            }
        }

        let processed_text = processed_words.join(" ");
        let total_words = words.len();
        let replacements_made = replacements.len();
        let replacement_rate = if total_words > 0 {
            replacements_made as f64 / total_words as f64
        } else {
            0.0
        };

        let stats = ProcessingStats {
            total_words,
            replacements_made,
            replacement_rate,
            replacements,
        };

        Ok((processed_text, stats))
    }

    fn extract_word_parts<'a>(&self, word: &'a str) -> Option<(&'a str, &'a str, &'a str)> {
        self.word_regex.captures(word)
            .and_then(|caps| {
                let prefix = caps.get(1)?.as_str();
                let core_word = caps.get(2)?.as_str();
                let suffix = caps.get(3)?.as_str();
                Some((prefix, core_word, suffix))
            })
    }

    fn get_canonical(&self, word: &str) -> Option<&String> {
        // Try exact match first
        if let Some(canonical) = self.reverse_lookup.get(word) {
            return Some(canonical);
        }

        // Try case-insensitive match
        if let Some(canonical) = self.case_insensitive_lookup.get(&word.to_lowercase()) {
            return Some(canonical);
        }

        None
    }

    fn preserve_case(&self, original: &str, canonical: &str) -> String {
        if original.chars().all(|c| c.is_uppercase()) {
            canonical.to_uppercase()
        } else if original.chars().next().map_or(false, |c| c.is_uppercase()) {
            let mut result = canonical.to_string();
            if let Some(first_char) = result.chars().next() {
                result.replace_range(0..first_char.len_utf8(), &first_char.to_uppercase().to_string());
            }
            result
        } else {
            canonical.to_lowercase()
        }
    }

    pub fn process_file(&self, input_file: &str, output_file: &str) -> Result<FileProcessingStats> {
        let content = std::fs::read_to_string(input_file)
            .with_context(|| format!("Failed to read input file: {}", input_file))?;

        let lines: Vec<&str> = content.lines().collect();
        let total_lines = lines.len();
        let mut processed_lines = Vec::with_capacity(total_lines);
        let mut total_replacements = 0;
        let mut total_words = 0;

        for &line in &lines {
            let (processed_line, stats) = self.process_text(line, true)?;
            processed_lines.push(format!("{}\n", processed_line));
            total_replacements += stats.replacements_made;
            total_words += stats.total_words;
        }

        std::fs::write(output_file, processed_lines.concat())
            .with_context(|| format!("Failed to write output file: {}", output_file))?;

        let replacement_rate = if total_words > 0 {
            total_replacements as f64 / total_words as f64
        } else {
            0.0
        };

        Ok(FileProcessingStats {
            input_file: input_file.to_string(),
            output_file: output_file.to_string(),
            total_lines,
            total_words,
            total_replacements,
            replacement_rate,
        })
    }

    pub fn get_vocabulary_stats(&self, text_file: &str) -> Result<VocabularyStats> {
        let content = std::fs::read_to_string(text_file)
            .with_context(|| format!("Failed to read text file: {}", text_file))?;

        let word_regex = Regex::new(r"\w+")
            .context("Failed to compile word regex for vocabulary analysis")?;

        let original_words: Vec<String> = word_regex
            .find_iter(&content.to_lowercase())
            .map(|m| m.as_str().to_string())
            .collect();

        let original_vocab: std::collections::HashSet<String> = original_words.iter().cloned().collect();

        let (processed_text, _) = self.process_text(&content, true)?;
        let processed_words: Vec<String> = word_regex
            .find_iter(&processed_text.to_lowercase())
            .map(|m| m.as_str().to_string())
            .collect();

        let processed_vocab: std::collections::HashSet<String> = processed_words.iter().cloned().collect();

        let vocab_reduction = original_vocab.len() as i64 - processed_vocab.len() as i64;
        let reduction_rate = if !original_vocab.is_empty() {
            vocab_reduction as f64 / original_vocab.len() as f64
        } else {
            0.0
        };

        Ok(VocabularyStats {
            original_vocabulary_size: original_vocab.len(),
            processed_vocabulary_size: processed_vocab.len(),
            vocabulary_reduction: vocab_reduction,
            reduction_rate,
            total_words: original_words.len(),
        })
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileProcessingStats {
    pub input_file: String,
    pub output_file: String,
    pub total_lines: usize,
    pub total_words: usize,
    pub total_replacements: usize,
    pub replacement_rate: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VocabularyStats {
    pub original_vocabulary_size: usize,
    pub processed_vocabulary_size: usize,
    pub vocabulary_reduction: i64,
    pub reduction_rate: f64,
    pub total_words: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    fn create_test_mapping() -> Result<NamedTempFile, Box<dyn std::error::Error>> {
        let mut temp_file = NamedTempFile::new()?;
        let test_data = r#"{
            "metadata": {
                "version": "1.0",
                "description": "Test mappings",
                "creation_date": "2024-01-01",
                "total_mappings": 2,
                "sources": ["test"],
                "total_synonyms": 4
            },
            "mappings": {
                "size_big": {
                    "canonical": "big",
                    "synonyms": ["large", "huge"],
                    "frequency_rank": 1,
                    "domain": "general"
                },
                "emotion_happy": {
                    "canonical": "happy",
                    "synonyms": ["joyful", "glad"],
                    "frequency_rank": 1,
                    "domain": "general"
                }
            },
            "reverse_lookup": {
                "large": "big",
                "huge": "big",
                "joyful": "happy",
                "glad": "happy"
            }
        }"#;

        temp_file.write_all(test_data.as_bytes())?;
        temp_file.flush()?;
        Ok(temp_file)
    }

    #[test]
    fn test_processor_creation() {
        let temp_file = create_test_mapping().unwrap();
        let temp_path = temp_file.path().to_str().unwrap();

        let processor = CVCProcessor::new(temp_path);
        assert!(processor.is_ok());
    }

    #[test]
    fn test_basic_text_processing() {
        let temp_file = create_test_mapping().unwrap();
        let temp_path = temp_file.path().to_str().unwrap();

        let processor = CVCProcessor::new(temp_path).unwrap();

        let input = "The large building made me joyful.";
        let (output, stats) = processor.process_text(input, true).unwrap();

        assert_eq!(output, "The big building made me happy.");
        assert_eq!(stats.total_words, 6);
        assert_eq!(stats.replacements_made, 2);
        assert!(stats.replacements.len() == 2);
    }

    #[test]
    fn test_case_preservation() {
        let temp_file = create_test_mapping().unwrap();
        let temp_path = temp_file.path().to_str().unwrap();

        let processor = CVCProcessor::new(temp_path).unwrap();

        let input = "The LARGE building made me JOYFUL.";
        let (output, stats) = processor.process_text(input, true).unwrap();

        assert_eq!(output, "The BIG building made me HAPPY.");
        assert_eq!(stats.replacements_made, 2);
    }

    #[test]
    fn test_no_case_preservation() {
        let temp_file = create_test_mapping().unwrap();
        let temp_path = temp_file.path().to_str().unwrap();

        let processor = CVCProcessor::new(temp_path).unwrap();

        let input = "The LARGE building made me JOYFUL.";
        let (output, stats) = processor.process_text(input, false).unwrap();

        assert_eq!(output, "The big building made me happy.");
        assert_eq!(stats.replacements_made, 2);
    }

    #[test]
    fn test_no_matches() {
        let temp_file = create_test_mapping().unwrap();
        let temp_path = temp_file.path().to_str().unwrap();

        let processor = CVCProcessor::new(temp_path).unwrap();

        let input = "The small house made me sad.";
        let (output, stats) = processor.process_text(input, true).unwrap();

        assert_eq!(output, input); // Should be unchanged
        assert_eq!(stats.replacements_made, 0);
    }
}
