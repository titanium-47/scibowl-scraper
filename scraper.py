import re
import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
QUESTION_PATH = os.environ["QUESTION_PATH"]
QUESTION_URL = os.environ["QUESTION_URL"]
QUESTION_FOLDER = os.environ["QUESTION_FOLDER"]
BASE_URL = os.environ["BASE_URL"]

pdf_link_pattern = re.compile(r'<a\s+[^>]*href=["\'](.*?\.pdf)["\'][^>]*>', re.IGNORECASE)

response = requests.get(QUESTION_URL)

pdf_links = pdf_link_pattern.findall(response.text)

x = 1

if os.path.exists(f'{QUESTION_FOLDER}{len(pdf_links) - 1}.pdf'):
    pass
else:
    for link in pdf_links[:-1]:
        response = requests.get(f'{BASE_URL}{link}')
        pdf = open(f"{QUESTION_FOLDER}{x}.pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
        x+=1

df = pd.DataFrame(columns=["Round", "Question", "Category", "Type"])

for i in range(1, len(pdf_links)):
    print(i)

    if i == 44:
        continue

    reader = PdfReader(f'{QUESTION_FOLDER}{i}.pdf')
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    num = re.search(r'\b\d+\b', text)[0]
    tossups = re.findall(r'TOSS\s?-?\s?UP(.*?)(?=\s*BONUS)', text, re.DOTALL)
    bonuses = re.findall(r'BONUS(.*?)(?=\s*TOSS-UP)', text, re.DOTALL)
    
    for tossup in tossups:
        category = re.findall(r'\d+\)\s*([A-Z][A-Z\s]+)', tossup)
        if category == []:
            category = re.findall(r'\d+\)\s*([A-Za-z\s-]+)\s*–', tossup)
        if category != []:
            category = category[0][:-1].strip()
            df.loc[len(df)] = [num, tossup.strip(), category.lower(), "toss-up"]

    for bonus in bonuses:
        category = re.findall(r'\d+\)\s*([A-Z][A-Z\s]+)', bonus)
        if category == []:
            category = re.findall(r'\d+\)\s*([A-Za-z\s-]+)\s*–', bonus)
        if category != []:
            category = category[0][:-1].strip()
            df.loc[len(df)] = [num, bonus.strip(), category.lower(), "bonus"]

df.to_csv(QUESTION_PATH)