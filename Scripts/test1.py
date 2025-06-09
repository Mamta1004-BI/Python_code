import spacy
import pandas as pd
import os
import re
import html

# Load the English model
nlp = spacy.load("en_core_web_sm")

# Step 1: Set working directory
os.chdir('C:\\Users\\Mamtachaudhary\\OneDrive - Veriforce\\Desktop\\Personal\\nlp_LEARNING')

# Step 2: Load CSV file
df = pd.read_csv('Name_addrees_extraction.csv')


# Step 3: Preprocessing function (optional cleanup)
def preprocess_text(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'&[^\s]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'&', 'and', text)
    text = re.sub(r'\(inactive\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

# Function to extract named entities
def extract_entities(text):
    text = preprocess_text(text)
    doc = nlp(text)
    names = []
    addresses = []
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON"]:
            names.append(ent.text)
        elif ent.label_ == "GPE":  # Geopolitical Entity, often used for addresses
            addresses.append(ent.text)
    
    return pd.Series(["; ".join(set(names)), "; ".join(set(addresses))], index=["Names", "Addresses"])

# Apply to your data
df[["Names", "Addresses"]] = df["Explanation"].apply(extract_entities)

# Save the output
df.to_excel("C:\\Mamta_Codes\\Python_WS\\Outputs\\spacy_entity_output.xlsx", index=False)
