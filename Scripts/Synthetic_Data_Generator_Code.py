import random
import json
from faker import Faker

fake = Faker()
Faker.seed(42)

# Sample organizations to simulate realistic names
org_keywords = [
   org_keywords = [
    "Solutions", "Services", "Logistics", "Technologies", "Enterprises",
    "Systems", "Consulting", "Industries", "Management", "Partners", "Ltd", "Inc",
    "Corporation", "LLC", "Associates", "Holdings", "International", "Global",
    "Financial", "Development", "Networks", "Resources", "Innovations", "Designs",
    "Engineering", "Construction", "Marketing", "Retail", "Healthcare", "Group",
    "Agency", "Firm", "Company", "Corp", "LP", "L.P", "Limited", "Ltd.", "Inc.",
    "Partnership", "Electrical", "Groups", "Co.", "Enterprises", "Solutions Inc",
    "Transport", "Distributors", "Procurement", "Fulfillment", "Warehousing",
    "Chain", "Supply", "Integrated", "Ventures", "Distribution", "Operations"
]


]
# Sample address formats
ADDRESS_FORMATS = [
"191 Caldari Road,Unit 2Concord, OntarioL4K 4A1" ,"1132682 Alberta Ltd oa"   ," LP 4175,  14th Avenue ,Markham ON L3R 0J2",
""
]
# Templates simulating messy real-world phrasing
templates = [
    "Client Required Wording For This Additionally Insured Statement Must Show As {ORG} {ORG} Name and Address for Certificate Holder must show as {ADDRESS}",
    "An Additionally Insured statement is mandatory. Must Show As {ORG} {ORG} located at {ADDRESS}",
    "Client Unit Required Wording For This Additionally Insured Statement Must Show As {ORG} {ORG} Name and Address for Certificate Holder must show as {ORG}{ADDRESS}",
    "You must include {ORG} {ORG} as additionally insured. Certificate holder: {ADDRESS}",
    "Must Show As {ORG} {ORG}. Certificate address: {ADDRESS}",
    "Client requires this: {ORG} {ORG}, {ADDRESS} – must be shown as additional insured",
    "Additional Insured wording must show as {ORG} {ORG}. Their address is {ADDRESS}",
    "Name and Address for Certificate Holder must show as {ORG}{Address}{ORG}",
    "Name and Address for Certificate Holder must show as {ORG} {Address}",
    "Client Required Wording For This Additionally Insured Statement Must Show As {ORG}{ORG} Sometimes your insurance broker requires the address of the client {ORG} {ADDRESS}",
    "Please note that Catalyst Paper Corporation must be named as additional insured on your Commercial General Liability and Umbrella Insurance policies Client Required Wording For This Additionally Insured Statement Must Show As {ORG}{ORG} Name and Address for Certificate Holder must show as {ORG}{ADDRESS}",
    ""

]

# Generate entity-annotated training data
def generate_training_example():
    org_base = fake.company()
    org_suffix = random.choice(org_keywords)
    org_full = f"{org_base} {org_suffix}"

    address = fake.address().replace("\n", " ")
    template = random.choice(templates)

    text = template.format(ORG=org_full, ADDRESS=address)

    # Find start/end indices of org and address
    org_start = text.find(org_full)
    org_end = org_start + len(org_full)

    addr_start = text.find(address)
    addr_end = addr_start + len(address)

    entities = [
        (org_start, org_end, "ORG"),
        (addr_start, addr_end, "ADDRESS")
    ]

    return (text, {"entities": entities})

# Generate 700 samples
train_data = [generate_training_example() for _ in range(700)]

# Save to JSON
with open("spacy_train_data_noisy.json", "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=2)

print("✅ Data generated and saved to spacy_train_data_noisy.json")
