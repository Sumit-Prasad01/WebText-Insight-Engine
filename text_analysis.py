import os
import re 
import pandas as pd

## Config
ARTICLES_FOLDER = "articles"          # Folder containing extracted article .txt files
STOPWORDS_FOLDER = "StopWords"        # Folder containing multiple stopwords .txt files
POSITIVE_FILE = "MasterDictionary/positive-words.txt"
NEGATIVE_FILE = "MasterDictionary/negative-words.txt"
OUTPUT_FILE = "Output Data Structure.xlsx"

## Load StopWords

stop_words = set()
for file in os.listdir(STOPWORDS_FOLDER):
    if file.endswith('.txt'):
        with open(os.path.join(STOPWORDS_FOLDER, file), 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip() and not line.startswith('|'):
                    stop_words.add(line.strip().lower())


## Load Positive and Negative Words

def load_word_list(file_path):
    words = set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.strip() and not line.startswith(';'):
                words.add(line.strip().lower())
    return words

positive_words = load_word_list(POSITIVE_FILE)
negative_words = load_word_list(NEGATIVE_FILE)

## Helper Functions

def count_syllables(word):
    word = word.lower()
    vowels = 'aeiou'
    count = 0
    prev_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                count += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False

        if word.endswith("e"):
            count -= 1
        if count <= 0:
            count = 1
        return count
    
def analyze_text(text):
    # Tokenize
    words = re.findall(r'\b\w+\b', text.lower())
    sentences = re.split(r'[.!?]', text)

    # Remove stop words
    filtered_words = [w for w in words if w not in stop_words]

    ## Positive and Negative Scores
    pos_score = sum(1 for w in filtered_words if w in positive_words)
    neg_score = sum(1 for w in filtered_words if w in negative_words)

    # Polarity & Subjectivity 
    polarity = (pos_score - neg_score) / ((pos_score + neg_score) + 1e-6)
    subjectivity = (pos_score + neg_score) / (len(filtered_words) + 1e-6)

    # Average Sentence Length
    avg_sentence_length = len(filtered_words) / max(len(sentences), 1)

    # Complex words
    complex_words = [w for w in filtered_words if count_syllables(w) >= 3]
    complex_words_count = len(complex_words)
    percent_complex_words = (complex_words_count / len(filtered_words)) if filtered_words else 0

    # Fog Index
    fog_index = 0.4 * (avg_sentence_length + percent_complex_words)

    # Syllables per word
    syllable_per_word = sum(count_syllables(w) for w in filtered_words) / max(len(filtered_words), 1)

    #Personal Pronouns
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, flags = re.I))

    # Average word length 
    avg_word_length = sum(len(w) for w in filtered_words) / max(len(filtered_words), 1)


    return [
        pos_score, neg_score, polarity, subjectivity,
        avg_sentence_length, percent_complex_words, fog_index,
        avg_sentence_length,  
        complex_words_count, len(filtered_words), syllable_per_word,
        personal_pronouns, avg_word_length
    ]


def process_article_and_save():
    results = []

    for file in os.listdir(ARTICLES_FOLDER):
        if file.endswith(".txt"):
            url_id = file.replace(".txt", "")
            with open(os.path.join(ARTICLES_FOLDER, file), 'r', encoding='utf-8', errors='ignore') as f:
                text  = f.read()
        
            metrices = analyze_text(text)
            results.append([url_id] + metrices)


    # create dataframe and save

    columns = [
        "URL_ID", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
        "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
        "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT",
        "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
    ]

    df_out = pd.DataFrame(results, columns=columns)
    df_out.to_excel(OUTPUT_FILE, index= False)

    print(f"Analysis complete. Results saved to '{OUTPUT_FILE}'")


# if __name__ == "__main__":
#     process_article_and_save()