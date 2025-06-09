import pandas as pd
from transformers import pipeline

# Load your data
df = pd.read_csv("C:\\Users\\Mamtachaudhary\\OneDrive - Veriforce\\Desktop\\Personal\\nlp_LEARNING\\Name_addrees_extraction.csv")

# Load pre-trained NER model (general-purpose)
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

# Function to apply NER and extract ORG/LOC/GPE entities
def extract_entities(text):
    if not isinstance(text, str) or text.strip() == "":
        return pd.Series(["", ""])
    
    try:
        results = ner_pipeline(text)
    except Exception:
        return pd.Series(["", ""])  # fallback for any processing errors

    orgs = [r['word'] for r in results if r['entity_group'] == 'ORG']
    locs = [r['word'] for r in results if r['entity_group'] in ['LOC', 'PER', 'MISC']]
    
    return pd.Series([
        ', '.join(orgs),
        ', '.join(locs)
    ])

# Apply to the column (you can change to 'Focused_Block' if needed)
df[['NER_Organizations', 'NER_Locations']] = df['Explanation'].apply(extract_entities)

# Save results
df.to_excel("huggingface_ner_output.xlsx", index=False)
print("✅ NER extraction complete. Saved to huggingface_ner_output.xlsx")
