use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use crate::{CVCProcessor, ProcessingStats, FileProcessingStats, VocabularyStats};

#[pyclass(name = "CVCProcessor")]
pub struct PyCVCProcessor {
    processor: CVCProcessor,
}

#[pymethods]
impl PyCVCProcessor {
    #[new]
    fn new(mapping_file: &str) -> PyResult<Self> {
        match CVCProcessor::new(mapping_file) {
            Ok(processor) => Ok(PyCVCProcessor { processor }),
            Err(e) => Err(PyValueError::new_err(format!("Failed to create CVCProcessor: {}", e))),
        }
    }

    #[pyo3(signature = (text, preserve_case=true))]
    fn process_text(&self, text: &str, preserve_case: bool) -> PyResult<(String, PyProcessingStats)> {
        match self.processor.process_text(text, preserve_case) {
            Ok((processed_text, stats)) => Ok((processed_text, PyProcessingStats::from(stats))),
            Err(e) => Err(PyValueError::new_err(format!("Failed to process text: {}", e))),
        }
    }

    fn process_file(&self, input_file: &str, output_file: &str) -> PyResult<PyFileProcessingStats> {
        match self.processor.process_file(input_file, output_file) {
            Ok(stats) => Ok(PyFileProcessingStats::from(stats)),
            Err(e) => Err(PyValueError::new_err(format!("Failed to process file: {}", e))),
        }
    }

    fn get_vocabulary_stats(&self, text_file: &str) -> PyResult<PyVocabularyStats> {
        match self.processor.get_vocabulary_stats(text_file) {
            Ok(stats) => Ok(PyVocabularyStats::from(stats)),
            Err(e) => Err(PyValueError::new_err(format!("Failed to get vocabulary stats: {}", e))),
        }
    }
}

#[pyclass(name = "ProcessingStats")]
#[derive(Clone)]
pub struct PyProcessingStats {
    #[pyo3(get)]
    pub total_words: usize,
    #[pyo3(get)]
    pub replacements_made: usize,
    #[pyo3(get)]
    pub replacement_rate: f64,
    #[pyo3(get)]
    pub replacements: Vec<PyReplacement>,
}

impl From<ProcessingStats> for PyProcessingStats {
    fn from(stats: ProcessingStats) -> Self {
        PyProcessingStats {
            total_words: stats.total_words,
            replacements_made: stats.replacements_made,
            replacement_rate: stats.replacement_rate,
            replacements: stats.replacements.into_iter().map(PyReplacement::from).collect(),
        }
    }
}

#[pyclass(name = "Replacement")]
#[derive(Clone)]
pub struct PyReplacement {
    #[pyo3(get)]
    pub position: usize,
    #[pyo3(get)]
    pub original: String,
    #[pyo3(get)]
    pub canonical: String,
}

impl From<crate::Replacement> for PyReplacement {
    fn from(replacement: crate::Replacement) -> Self {
        PyReplacement {
            position: replacement.position,
            original: replacement.original,
            canonical: replacement.canonical,
        }
    }
}

#[pyclass(name = "FileProcessingStats")]
#[derive(Clone)]
pub struct PyFileProcessingStats {
    #[pyo3(get)]
    pub input_file: String,
    #[pyo3(get)]
    pub output_file: String,
    #[pyo3(get)]
    pub total_lines: usize,
    #[pyo3(get)]
    pub total_words: usize,
    #[pyo3(get)]
    pub total_replacements: usize,
    #[pyo3(get)]
    pub replacement_rate: f64,
}

impl From<FileProcessingStats> for PyFileProcessingStats {
    fn from(stats: FileProcessingStats) -> Self {
        PyFileProcessingStats {
            input_file: stats.input_file,
            output_file: stats.output_file,
            total_lines: stats.total_lines,
            total_words: stats.total_words,
            total_replacements: stats.total_replacements,
            replacement_rate: stats.replacement_rate,
        }
    }
}

#[pyclass(name = "VocabularyStats")]
#[derive(Clone)]
pub struct PyVocabularyStats {
    #[pyo3(get)]
    pub original_vocabulary_size: usize,
    #[pyo3(get)]
    pub processed_vocabulary_size: usize,
    #[pyo3(get)]
    pub vocabulary_reduction: i64,
    #[pyo3(get)]
    pub reduction_rate: f64,
    #[pyo3(get)]
    pub total_words: usize,
}

impl From<VocabularyStats> for PyVocabularyStats {
    fn from(stats: VocabularyStats) -> Self {
        PyVocabularyStats {
            original_vocabulary_size: stats.original_vocabulary_size,
            processed_vocabulary_size: stats.processed_vocabulary_size,
            vocabulary_reduction: stats.vocabulary_reduction,
            reduction_rate: stats.reduction_rate,
            total_words: stats.total_words,
        }
    }
}

#[pymodule]
fn rust_cvc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyCVCProcessor>()?;
    m.add_class::<PyProcessingStats>()?;
    m.add_class::<PyReplacement>()?;
    m.add_class::<PyFileProcessingStats>()?;
    m.add_class::<PyVocabularyStats>()?;
    Ok(())
}