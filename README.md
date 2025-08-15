# WebText-Insight-Engine

## **Overview**
This project automates the extraction of article text from a given list of URLs and performs textual analysis to compute sentiment, readability, and linguistic metrics.  
It is implemented in **Python** using `BeautifulSoup`, `Selenium`, and `pandas`.

---

## **Project Structure**
```
project/
├── main.py                 # Entry point to run both extraction & analysis
├── extract_articles.py     # Step 1: Data Extraction
├── text_analysis.py        # Step 2: Text Analysis
├── Input.xlsx              # Contains URL_ID and URLs
├── articles/               # Extracted article text files
├── StopWords/              # Multiple .txt stopword lists
├── MasterDictionary/       # Positive & Negative word lists
└── Output Data Structure.xlsx  # Final output after analysis
```

---

## **Workflow**

### **Step 1 – Data Extraction (`extract_articles.py`)**
- Reads `Input.xlsx` for URLs and their `URL_ID`.
- For **static pages**, uses `requests + BeautifulSoup` to scrape title and main text.
- For **dynamic pages**, falls back to `Selenium` to load JavaScript-rendered content.
- Saves each article as `{URL_ID}.txt` in the `articles/` folder.
- Removes website headers, footers, and irrelevant content.

### **Step 2 – Text Analysis (`text_analysis.py`)**
- Reads `.txt` files from `articles/`.
- Loads:
  - **Stopwords** from `StopWords/` (multiple `.txt` files merged)
  - **Positive words** from `positive-words.txt`
  - **Negative words** from `negative-words.txt`
- Computes:
  - POSITIVE SCORE, NEGATIVE SCORE, POLARITY SCORE, SUBJECTIVITY SCORE
  - AVG SENTENCE LENGTH, % COMPLEX WORDS, FOG INDEX
  - COMPLEX WORD COUNT, WORD COUNT, SYLLABLE PER WORD
  - PERSONAL PRONOUNS, AVG WORD LENGTH
- Saves results in **`Output Data Structure.xlsx`** with the required column order.

---

## **Running the Project**

### **1. Install Dependencies**
```bash
pip install pandas requests beautifulsoup4 selenium openpyxl
```
Also install [ChromeDriver](https://chromedriver.chromium.org/downloads) for Selenium.

### **2. Run the Main Script**
```bash
python main.py
```
The `main.py` script will:
1. Call `extract_articles.py` to scrape and save articles.
2. Call `text_analysis.py` to process the saved articles and generate the final Excel output.

---

## **Deliverables**
1. **Python scripts**: `extract_articles.py`, `text_analysis.py`, `main.py`
2. **Output Excel**: `Output Data Structure.xlsx`
3. **Instructions**: This `README.md` file.

---