import re

def parse_ktp_text(text):
    # Clean up the text by replacing newlines with spaces
    text = text.replace('\n', ' ')
    
    # Extract NIK - look for a 16-digit number
    nik_match = re.search(r'NIK\s*(\d{16})', text)
    nik = nik_match.group(1) if nik_match else "Not Found"
    
    # Extract Name - look for "Nama" followed by text
    name_match = re.search(r'Nama\s*:?\s*([A-Za-z\s]+)', text)
    name = name_match.group(1).strip() if name_match else "Not Found"
    
    # Extract Address - look for "Alamat" followed by text until the next field
    address_match = re.search(r'Alamat\s*:?\s*([A-Za-z0-9\s\.\,]+)', text)
    address = address_match.group(1).strip() if address_match else "Not Found"
    
    # Extract RT/RW
    rtrw_match = re.search(r'RT/RW\s*:?\s*(\d{3}/\d{3})', text)
    rtrw = rtrw_match.group(1) if rtrw_match else "Not Found"
    
    # Extract Kelurahan/Desa
    kel_desa_match = re.search(r'Kel/Desa\s*:?\s*([A-Za-z\s]+)', text)
    kel_desa = kel_desa_match.group(1).strip() if kel_desa_match else "Not Found"
    
    # Extract Kecamatan
    kecamatan_match = re.search(r'Kecamatan\s*:?\s*([A-Za-z\s]+)', text)
    kecamatan = kecamatan_match.group(1).strip() if kecamatan_match else "Not Found"
    
    # Extract Religion
    agama_match = re.search(r'Agama\s*:?\s*([A-Za-z\s]+)', text)
    agama = agama_match.group(1).strip() if agama_match else "Not Found"
    
    # Extract Marital Status
    status_match = re.search(r'Status Perkawinan\s*:?\s*([A-Za-z\s]+)', text)
    status = status_match.group(1).strip() if status_match else "Not Found"
    
    # Extract Occupation
    pekerjaan_match = re.search(r'Pekerjaan\s*:?\s*([A-Za-z\s/]+)', text)
    pekerjaan = pekerjaan_match.group(1).strip() if pekerjaan_match else "Not Found"
    
    # Extract Citizenship
    kewarganegaraan_match = re.search(r'Kewarganegaraan\s*:?\s*([A-Za-z\s]+)', text)
    kewarganegaraan = kewarganegaraan_match.group(1).strip() if kewarganegaraan_match else "Not Found"
    
    return {
        "NIK": nik,
        "Name": name,
        "Tempat Lahir": tempat_lahir,
        "Address": address,
        "RT/RW": rtrw,
        "Kelurahan/Desa": kel_desa,
        "Kecamatan": kecamatan,
        "Agama": agama,
        "Status Perkawinan": status,
        "Pekerjaan": pekerjaan,
        "Kewarganegaraan": kewarganegaraan
    }
