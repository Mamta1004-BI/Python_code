import spacy

# Load your custom NER model
nlp = spacy.load("custom_ner_model")
text = """Client Required Wording For This Additionally Insured Statement Must Show
GreenCore Technologies Ltd. ,1800 Elm Street Toronto ON M5V 2L7"""

doc = nlp(text)

# Extract and print named entities
for ent in doc.ents:
    print(f"{ent.label_}: {ent.text}")
