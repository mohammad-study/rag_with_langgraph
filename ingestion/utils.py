import csv
import json
import re
from collections import Counter

from docx import Document


def read_docx_file(input_file):
    """
    Reads a .docx file and returns a list of lines.
    Args:        input_file (str): Path to the .docx file.
    Returns:        list: A list of lines extracted from the document.
    """
    doc = Document(input_file)
    lines = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            lines.append(text)

    return lines


def clean_text(text):
    """
    Cleans the input text by removing unwanted characters and extra whitespace.
    Args:        text (str): The input text to be cleaned.
    Returns:        str: The cleaned text.
    """
    text = re.sub(r"[•*-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords(text, top_n=5):
    """
    Extracts the most frequent keywords from the input text based on top_n.
    Args:        text (str): The input text to extract keywords from.
    Returns:        list: A list of the most frequent keywords.
    """
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    stopwords = {
        "this",
        "that",
        "with",
        "from",
        "have",
        "will",
        "must",
        "should",
        "their",
        "they",
    }
    words = [w for w in words if w not in stopwords]
    freq = Counter(words)
    return [w for w, _ in freq.most_common(top_n)]


def write_to_csv(rows: list, output_file: str):
    """
    Writes a list of dictionaries to a CSV file.
    Args:        rows (list): A list of dictionaries representing the rows to write.
        output_file (str): Path to the output CSV file.
    """
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "section",
                "subsection",
                "chunk",
                "keywords",
                "input_file",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_to_jsonl(rows: list, output_file: str):
    """Writes a list of dictionaries to a JSONL file.
    Args:        rows (list): A list of dictionaries representing the rows to write.
        output_file (str): Path to the output JSONL file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
