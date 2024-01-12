import os
from dotenv import load_dotenv
import re
import pandas as pd

load_dotenv()
CUSTOM_PATH = os.environ["CUSTOM_PATH"]

qfile = open(CUSTOM_PATH, 'r')
text = qfile.read()
qfile.close()

df = pd.DataFrame(columns=["Question", "Category", "Type"])

tossups = re.findall(r'TOSS\s?-?\s?UP(.*?)(?=\s*BONUS)', text, re.DOTALL)
bonuses = re.findall(r'BONUS(.*?)(?=\s*TOSS-UP)', text, re.DOTALL)

for tossup in tossups:
    category = re.findall(r'\d+\)\s*([A-Z][A-Z\s]+)', tossup)
    if category == []:
        category = re.findall(r'\d+\)\s*([A-Za-z\s-]+)\s*–', tossup)
    if category != []:
        category = category[0][:-1].strip()
        df.loc[len(df)] = [tossup.strip(), category.lower(), "toss-up"]

for bonus in bonuses:
    category = re.findall(r'\d+\)\s*([A-Z][A-Z\s]+)', bonus)
    if category == []:
        category = re.findall(r'\d+\)\s*([A-Za-z\s-]+)\s*–', bonus)
    if category != []:
        category = category[0][:-1].strip()
        df.loc[len(df)] = [bonus.strip(), category.lower(), "bonus"]

df.to_csv("custom_qs.csv")