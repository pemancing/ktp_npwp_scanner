import re

def parse_npwp_text(text):
    npwp = re.search(r'\d{2}\.\d{3}\.\d{3}\.\d-\d{3}\.\d', text)
    name = re.search(r'Nama\s*:?\s*(.*)', text)
    return {
        "NPWP": npwp.group(0) if npwp else "Not Found",
        "Name": name.group(1) if name else "Not Found"
    }
