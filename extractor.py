import os
import re
import requests
from bs4 import BeautifulSoup
from readability import Document
from PIL import Image
import pytesseract

def is_url(input_str):
    return re.match(r'^https?://', input_str) is not None

def is_image_file(input_str):
    return os.path.isfile(input_str) and input_str.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))

def extract_text_from_url(url):
    resp = requests.get(url, timeout=10)
    doc = Document(resp.text)
    html = doc.summary()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return text

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='jpn+eng')
    return text

def extract_article_text(input_str):
    if is_url(input_str):
        return extract_text_from_url(input_str)
    elif is_image_file(input_str):
        return extract_text_from_image(input_str)
    else:
        return input_str  # そのままテキストとして扱う 