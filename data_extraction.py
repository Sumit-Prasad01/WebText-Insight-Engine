import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException



INPUT_FILE = "Input.xlsx"  
OUTPUT_FOLDER = "articles"
TIMEOUT = 10

def clean_text(text):
    """Remove excessive whitespace and unwanted characters."""
    return re.sub(r'\s+', ' ', text).strip()

def extract_static(url):
    """Extract article using requests + BeautifulSoup."""
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        #Title Extraction
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip = True) if title_tag else ''


        # Paragraph extraction - tune selector if needed
        paragraph = soup.find_all('p')
        content = ' '.join(p.get_text(strip = True) for p in paragraph)

        return clean_text(f"{title}\n\n{content}") if content else None

    except Exception as e:
        print(f"[STATIC] Failed for {url} -> {e}")
        return None
    

def extract_dynamic(url):
    """Extract article using Selenium for JS-rendered pages."""
    try: 
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options = options)


        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        #Title Extraction
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip = True) if title_tag else ''


        # Paragraph extraction - tune selector if needed
        paragraph = soup.find_all('p')
        content = ' '.join(p.get_text(strip = True) for p in paragraph)

        return clean_text(f"{title}\n\n{content}") if content else None
    
    except WebDriverException as we:
        print(f"[DYNAMIC] Selenium error for {url} -> {we}")
        return None
    
    except Exception as e:
        print(f"[DYNAMIC] Failed for {url} -> {e}")
        return None


def save_article(url_id, text):
    """Save article to the text file"""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    file_path = os.path.join(OUTPUT_FOLDER, f"{url_id}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)



def main():
    df = pd.read_excel(INPUT_FILE)

    for _, row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']

        print(f"Processing {url_id} -> {url}")

        # Try static extraction first
        article_text = extract_static(url)

        # Fallback to dynamic extraction if static fails
        if not article_text:
            print(f"⚠ Static failed, trying Selenium for {url}")
            article_text = extract_dynamic(url)

        if article_text:
            save_article(url_id, article_text)
            print(f"Saved {url_id}.txt")
        else:
            print(f"Failed to extract {url}")


if __name__ == "__main__":
    main()