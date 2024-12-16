# Lyrics Analysis Framework

## Project Overview

This project provides a reusable framework for comparative text analysis, demonstrated using song lyrics from SZA's albums *Ctrl* and *SOS*. The framework preprocesses lyrics, performs analysis, and generates visualizations to compare text data. It is designed to be extensible and reusable for other text datasets.

## Features

- **Text Preprocessing**:
  - Removes punctuation, capitalization, and stop words (with support for custom stop words).
  - Computes word counts and prepares data for visualization.
  
- **Custom Parsing**:
  - Support for domain-specific parsers to handle unique text formats.
  
- **Visualizations**:
  - **Sankey Diagram**: Links songs to their most frequent words, with line thickness representing word frequency.
  - **Word Frequency Plot**: Subplots showing the top 10 words for each song.
  - **Sentiment Analysis Scatter Plot**: Compares sentiment polarity for songs across albums.

## Requirements

- Python 3.x
- Libraries:
  - `nltk` for text preprocessing
  - `matplotlib` and `plotly` for visualizations
  - `textblob` for sentiment analysis
  - `beautifulsoup4` and `requests` for web scraping

## How to Run

### 1. Clone the repository:
```bash
git clone https://github.com/nalikapalayoor/lyrics_analysis.git
cd lyrics_analysis
```
### 2. Install dependencies:
```bash
pip install -r requirements.txt
```
### 3. Scrape lyrics from Genius:
```bash
python test_scraper.py
```
This will save the lyrics as .txt files in the data/ctrl and data/sos directories.

### 4. Run the analysis:
```bash
python lyrics_analysis.py
```

## Authors

- [Nalika Palayoor](https://github.com/nalikapalayoor)

