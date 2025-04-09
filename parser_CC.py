import re

def extract_credit_card_info(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines.reverse()  # Scan bottom to top

    card_number = None
    cardholder_name = None
    valid_thru = None
    card_issuer = None

    for line in lines:
        # Cardholder Name: Usually at the bottom, all uppercase, no digits
        if not cardholder_name:
            if re.fullmatch(r'[A-Z ]{5,}', line) and not any(char.isdigit() for char in line):
                cardholder_name = line
                continue

        # Valid Thru: Right above name, format MM/YY or MM-YY
        if not valid_thru:
            match = re.search(r'(0[1-9]|1[0-2])[\/\-]\d{2}', line)
            if match:
                valid_thru = match.group()
                continue

        # Card Number: One of the top lines, 16 digits usually with spaces or dashes
        if not card_number:
            match = re.search(r'(\d{4}[\s-]?){3}\d{4}', line)
            if match:
                card_number = match.group().replace(" ", "").replace("-", "")

                # Determine card issuer
                if card_number.startswith('4'):
                    card_issuer = 'Visa'
                elif card_number.startswith('5'):
                    card_issuer = 'MasterCard'
                elif card_number.startswith(('34', '37')):
                    card_issuer = 'American Express'
                elif card_number.startswith('6'):
                    card_issuer = 'Discover'
                else:
                    card_issuer = 'Unknown'
                continue

        # If all fields found, stop early
        if card_number and valid_thru and cardholder_name:
            break

    return {
        "card_number": card_number,
        "cardholder_name": cardholder_name,
        "valid_thru": valid_thru,
        "card_issuer": card_issuer
    }
