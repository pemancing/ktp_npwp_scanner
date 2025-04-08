import re

def parse_npwp_text(text):
    lines = text.split('\n')
    data = {
        "NPWP": "Not Found",
        "Name": "Not Found",
        "NIK": "Not Found",
        "Address": "Not Found",
        "KPP": "Not Found",
        "Tanggal Terdaftar": "Not Found"
    }

    # Normalize text
    text = text.replace('\n', ' ').replace(':', ' : ')

    # Extract NPWP number (format: 15 digits)
    npwp_match = re.search(r'\d{2}\.\d{3}\.\d{3}\.\d-\d{3}\.\d{3}', text)
    if not npwp_match:
        npwp_match = re.search(r'\d{2}\.\d{3}\.\d{3}\.\d-\d{3}', text)  # fallback
    if npwp_match:
        data["NPWP"] = npwp_match.group(0)

    # Extract KPP name
    for line in lines:
        if "KPP" in line.upper():
            data["KPP"] = line.strip()
            break

    # Extract name (line after NPWP number)
    for i, line in enumerate(lines):
        if data["NPWP"] in line:
            if i + 1 < len(lines):
                data["Name"] = lines[i + 1].strip()
            if i + 2 < len(lines):
                possible_nik = re.search(r'\d{16}', lines[i + 2])
                if possible_nik:
                    data["NIK"] = possible_nik.group(0)
            break

    # Extract address (after name, until "Tanggal Terdaftar")
    address_start = False
    address_lines = []
    for line in lines:
        if data["Name"] != "Not Found" and data["Name"] in line:
            address_start = True
            continue
        if address_start:
            if "TanggalTerdaftar" in line.replace(" ", ""):
                break
            address_lines.append(line.strip())

    if address_lines:
        data["Address"] = ', '.join([a for a in address_lines if a])

    # Extract Tanggal Terdaftar
    tanggal_match = re.search(r'Tanggal\s*Terdaftar\s*(\d{2}/\d{2}/\d{4})', text.replace(' ', ''))
    if tanggal_match:
        data["Tanggal Terdaftar"] = tanggal_match.group(1)

    return data
