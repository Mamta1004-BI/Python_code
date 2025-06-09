import os
import pandas as pd
import re
from cleanco import basename
import html

org_keywords = [
    "Solutions", "Services", "Logistics", "Technologies", "Enterprises",
    "Systems", "Consulting", "Industries", "Management", "Partners", "Ltd", "Inc",
    "Corporation", "LLC", "Associates", "Holdings", "International", "Global",
    "Financial", "Development", "Networks", "Resources", "Innovations", "Designs",
    "Engineering", "Construction", "Marketing", "Retail", "Healthcare", "Group",
    "Agency", "Firm", "Company", "Corp", "LP", "L.P", "Limited", "Ltd.", "Inc.",
    "Partnership", "Electrical", "Groups", "Co.", "Enterprises", "Solutions Inc",
    "Transport", "Distributors", "Procurement", "Fulfillment", "Warehousing",
    "Chain", "Supply", "Integrated", "Ventures", "Distribution", "Operations","ULC", "LLP", "PLC", "Pty Ltd", "GmbH", "S.A.", "S.L.", "B.V.", "K.K.", "Sdn Bhd"
]

phrases_to_remove = [
    'must show as:', 'certificate holder', 'client required wording',
    'must be named as', 'must include as', 'on your certificate.',
    'insurance certificate must list', 'additional insured statement:',
    '"additionally insured" statement', 'additionally insured statement:'
]


# Step 1: Set working directory
os.chdir('C:\\Users\\Mamtachaudhary\\OneDrive - Veriforce\\Desktop\\Personal\\nlp_LEARNING')

# Step 2: Load CSV file
df = pd.read_csv('Name_addrees_extraction.csv')

# Step 3: Preprocessing function
def preprocess_text(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'&[^\s]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'&', 'and', text)
    text = re.sub(r'\(inactive\)', '', text, flags=re.IGNORECASE)
    return text.strip()

# Step 3.1: Filter out rows based on undesired starting phrases
ignore_starts = ['if you have', 'additional insured', 'note: cgl policy must only reference']
df = df[~df['Explanation'].str.strip().str.lower().str.startswith(tuple(ignore_starts))].copy()

# Step 4: Focused cleaning function
def clean_and_focus_text(text):
    if not isinstance(text, str):
        return ''
    lowered = text.lower()
    keywords = [
        'must show as:', 'certificate holder', 'client required wording',
        'must be named as', 'must include as', "on your certificate.",
        "insurance certificate must list", "additional insured statement:","\"additionally insured\" statement",
        "additionally insured statement:"
    ]
    for keyword in keywords:
        if keyword in lowered:
            return text[lowered.rfind(keyword):].strip()
    return text[-250:].strip()


def split_on_first_org_keyword(text):
    if not isinstance(text, str) or not text.strip():
        return pd.Series(['', ''])
    text = preprocess_text(text)
    focused_text = clean_and_focus_text(text)
    lowered_text = focused_text.lower()
    
    keyword_positions = []
    for keyword in org_keywords:
        keyword = keyword.lower()
        # Match whole word only to avoid false splits inside other words
        match = re.search(r'\b' + re.escape(keyword) + r'\b', lowered_text)
        if match:
            keyword_positions.append((match.start(), match.group()))

    if not keyword_positions:
        return pd.Series([focused_text, ''])

    # Get first occurrence from the END (closest to the actual company name)
    split_pos, matched_keyword = max(keyword_positions, key=lambda x: x[0])

    # ⚠️ Include the matched keyword with the first part (Extractiontest)
    split_index = split_pos + len(matched_keyword)
    part_before = focused_text[:split_index].strip()
    part_after = focused_text[split_index:].strip()

    return pd.Series([part_before, part_after])

def clean_extraction_text(text):
    if not isinstance(text, str):
        return ''
    
    lowered_text = text.lower()
    for phrase in phrases_to_remove:
        lowered_text = lowered_text.replace(phrase.lower(), '')

    return lowered_text.strip()


""" # Step 5: Extraction logic
def extract_name_address(text):
    text = preprocess_text(text)
    focused_text = clean_and_focus_text(text)
    name = None
    address = None

    # Try structured patterns first
    name_patterns = [
        r"(?:must show as|must be named as|must include as|on your certificate.|Additional Insured Statement|Additionally Insured Statement:|\"Additionally Insured\" Statement)\s*[:\-]?\s*(.*?)(?=\s+name and address|must be named as|certificate holder|$)",
        r"(?:additionally insured statement\s*[:\-]?\s*)(.*?)(?=\s+name and address|certificate holder|$)",
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, focused_text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            break

    address_patterns = [
        r"(?:name and address.*?must show as\s*[:\-]?\s*)(.*?)(?:\.|$)",
        r"(?:certificate holder.*?must show as\s*[:\-]?\s*)(.*?)(?:\.|$)",
    ]
    
    for pattern in address_patterns:
        match = re.search(pattern, focused_text, re.IGNORECASE | re.DOTALL)
        if match:
            address = match.group(1).strip()
            break """

"""     # Fallback if above fails
    if not address:
        fallback_address_match = re.findall(
            r"([A-Z][A-Za-z&\s]+)\s+(\d{2,5}\s+[\w\s\.\-]+,\s*[\w\s]+,\s*[A-Z]{2,3}\s*\d[A-Z0-9]\d)", text)
        if fallback_address_match:
            # Take the first match (could be improved later to capture all)
            name, address = fallback_address_match[0]
            name = name.strip()
            address = address.strip()

    return pd.Series([focused_text, name, address])
 """


# Step 6: Apply logic
df[['Extractiontest', 'Focused_Block']] = df['Explanation'].apply(split_on_first_org_keyword)
df['Extractiontest'] = df['Extractiontest'].apply(clean_extraction_text)


# Step 7: Export results
df.to_excel('C:\\Mamta_Codes\\Python_WS\\Outputs\\output.xlsx', sheet_name='Sheet1', index=False)

print("✅ Extraction complete. Output written to 'output.xlsx'")
