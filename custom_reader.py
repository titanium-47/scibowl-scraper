import os
from dotenv import load_dotenv
import re
import pandas as pd

load_dotenv()
CUSTOM_PATH = os.environ["CUSTOM_PATH"]

def find_subject(text):
    subjects = ["Physics", "Biology", "Chemistry", "Mathematics", "Earth and Space"]

    for subject in subjects:
        if re.search(rf'\b{re.escape(subject)}\b', text, re.I):
            return subject

    return None

def main():
    qfile = open(CUSTOM_PATH, 'r', encoding="utf8")
    text = qfile.read()
    qfile.close()

    df = pd.DataFrame(columns=["Question", "Category", "Type"])

    tossups = re.findall(r'TOSS\s?-?\s?UP(.*?)(?=\s*BONUS)', text, re.DOTALL)
    bonuses = re.findall(r'BONUS(.*?)(?=\s*TOSS-UP)', text, re.DOTALL)

    for tossup in tossups:
        category = find_subject(tossup)
        tossup = tossup.strip()
        if tossup[1] == ")":
            tossup = tossup[2:]
        elif tossup[2] == ")":
            tossup = tossup[3:]
        if category != None:
            df.loc[len(df)] = [tossup.strip(), category.lower(), "toss-up"]

    for bonus in bonuses:
        category = find_subject(bonus)
        bonus = bonus.strip()
        if bonus[1] == ")":
            bonus = bonus[2:]
        elif bonus[2] == ")":
            bonus = bonus[3:]
        if category != None:
            df.loc[len(df)] = [bonus.strip(), category.lower(), "bonus"]

    df.to_csv("custom_qs.csv")

if __name__ == "__main__":
    main()