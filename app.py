from flask import Flask, request, jsonify, render_template
import re
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def redact_text(text):
    patterns = {
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'PHONE': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'CREDIT_CARD': r'\b(?:\d[ -]*?){13,16}\b',
        'IP_ADDRESS': r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    }

    redacted_text = text
    for key, pattern in patterns.items():
        redacted_text = re.sub(pattern, f'[REDACTED {key}]', redacted_text)

    doc = nlp(redacted_text)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'GPE', 'ORG', 'DATE', 'ADDRESS', 'MONEY', 'LOC']:
            redacted_text = redacted_text.replace(ent.text, '[REDACTED]')

    return redacted_text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form["text"]
        redacted_text = redact_text(input_text)
        return render_template("index.html", original_text=input_text, redacted_text=redacted_text)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)