import re
import spacy

nlp = spacy.load("en_cor_web_sm")

def redact_text(text):
    patterns ={
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'PHONE': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'CREDIT_CARD': r'\b(?:\d[ -]*?){13,16}\b',
        'IP_ADDRESS': r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    }
    redacted_text = text
    for key, pattern in patterns,items():
        redacted_text = re.sub(pattern, f'[REDACTED {key}]', redacted_text)
    
    doc =nlp(redacted_text)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'GPE', 'ORG', 'DATE', 'ADDRESS', 'MONEY', 'LOC']:
            redacted_text = redacted_text.replace(ent.text, '[XXXXX]')
        
    return redacted_text
if __name__ == "__main__":
    input_text = """John Does' email is john.doe@example.com, his phone number is 123-212-666-66, and his credit card number is 1234-5678-9012-3456. He lives in New York and works at SOM. """
    print("Original Text", input_text)
    redacted_output = redact_text(input_text)
    print("\nRedacted Text:\n", redacted_output)