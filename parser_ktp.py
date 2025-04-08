import re
import difflib

# Province and City Lists (you can extend these as needed)
INDONESIAN_PROVINCES = [
    "ACEH", "SUMATERA UTARA", "SUMATERA BARAT", "RIAU", "JAMBI", "SUMATERA SELATAN",
    "BENGKULU", "LAMPUNG", "KEPULAUAN BANGKA BELITUNG", "KEPULAUAN RIAU", "DKI JAKARTA",
    "JAWA BARAT", "JAWA TENGAH", "DI YOGYAKARTA", "JAWA TIMUR", "BANTEN",
    "BALI", "NUSA TENGGARA BARAT", "NUSA TENGGARA TIMUR", "KALIMANTAN BARAT",
    "KALIMANTAN TENGAH", "KALIMANTAN SELATAN", "KALIMANTAN TIMUR", "KALIMANTAN UTARA",
    "SULAWESI UTARA", "SULAWESI TENGAH", "SULAWESI SELATAN", "SULAWESI TENGGARA",
    "GORONTALO", "SULAWESI BARAT", "MALUKU", "MALUKU UTARA", "PAPUA", "PAPUA BARAT"
]

INDONESIAN_CITIES = [
    "JAKARTA SELATAN", "JAKARTA TIMUR", "JAKARTA BARAT", "JAKARTA UTARA", "JAKARTA PUSAT",
    "BANDUNG", "SURABAYA", "MEDAN", "PALEMBANG", "SEMARANG", "YOGYAKARTA", "DENPASAR",
    "MAKASSAR", "BALIKPAPAN", "MANADO", "PADANG", "PEKANBARU", "BANJARMASIN", "PONTIANAK"
]

def best_match(query, choices, cutoff=0.7):
    matches = difflib.get_close_matches(query, choices, n=1, cutoff=cutoff)
    return matches[0] if matches else "Not Found"

def extract_province_and_city(text):
    text = text.upper().replace('\n', ' ')
    tokens = text.split()

    province = "Not Found"
    city = "Not Found"

    for i in range(len(tokens)):
        for j in range(i + 1, min(i + 4, len(tokens)) + 1):
            phrase = " ".join(tokens[i:j])
            if province == "Not Found":
                p = best_match(phrase, INDONESIAN_PROVINCES)
                if p != "Not Found":
                    province = p
            if city == "Not Found":
                c = best_match(phrase, INDONESIAN_CITIES)
                if c != "Not Found":
                    city = c
            if province != "Not Found" and city != "Not Found":
                break
        if province != "Not Found" and city != "Not Found":
            break

    return province, city

def parse_ktp_text(text):
    text = text.replace('Pekeriaan', 'Pekerjaan').replace('Jenkelamm', 'Jenis Kelamin')
    lines = text.split('\n')
    data = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == "NIK" and i + 1 < len(lines):
            data["NIK"] = lines[i + 1].strip()
            i += 1
        elif line == "Nama" and i + 1 < len(lines):
            data["Name"] = lines[i + 1].strip()
            i += 1
        elif line == "Alamat" and i + 1 < len(lines):
            data["Address"] = lines[i + 1].strip()
            i += 1
        elif line == "RT/RW" and i + 1 < len(lines):
            data["RT/RW"] = lines[i + 1].strip()
            i += 1
        elif line == "Kel/Desa" and i + 1 < len(lines):
            data["Kelurahan/Desa"] = lines[i + 1].strip()
            i += 1
        elif line == "Kecamatan" and i + 1 < len(lines):
            data["Kecamatan"] = lines[i + 1].strip()
            i += 1
        elif line == "Agama" and i + 1 < len(lines):
            data["Agama"] = lines[i + 1].strip()
            i += 1
        elif line.startswith("Status Perkawinan") and ':' in line:
            data["Status Perkawinan"] = line.split(':', 1)[1].strip()
        elif line.startswith("Pekerjaan") or line.startswith("Pekeriaan"):
            if ':' in line:
                pekerjaan = line.split(':', 1)[1].strip()
            else:
                pekerjaan = lines[i + 1].strip() if i + 1 < len(lines) else ""
                i += 1
            data["Pekerjaan"] = pekerjaan
        elif line.startswith("Kewarganegaraan") and ':' in line:
            data["Kewarganegaraan"] = line.split(':', 1)[1].strip()
        elif line == "Jenis Kelamin" and i + 1 < len(lines):
            data["Jenis Kelamin"] = lines[i + 1].strip()
            i += 1
        elif "Gol.Darah" in line:
            match = re.search(r'Gol\.Darah\s*(\w+)', line)
            if match:
                data["Golongan Darah"] = match.group(1)
        elif "BerlakuHingga" in line or "Berlaku Hingga" in line:
            if i + 1 < len(lines):
                data["Berlaku Hingga"] = lines[i + 1].strip()
                i += 1
        i += 1

    province, city = extract_province_and_city(text)
    data["Provinsi"] = province
    data["Kota/Kabupaten"] = city

    return {
        "NIK": data.get("NIK", "Not Found"),
        "Name": data.get("Name", "Not Found"),
        "Address": data.get("Address", "Not Found"),
        "RT/RW": data.get("RT/RW", "Not Found"),
        "Kelurahan/Desa": data.get("Kelurahan/Desa", "Not Found"),
        "Kecamatan": data.get("Kecamatan", "Not Found"),
        "Agama": data.get("Agama", "Not Found"),
        "Status Perkawinan": data.get("Status Perkawinan", "Not Found"),
        "Pekerjaan": data.get("Pekerjaan", "Not Found"),
        "Kewarganegaraan": data.get("Kewarganegaraan", "Not Found"),
        "Jenis Kelamin": data.get("Jenis Kelamin", "Not Found"),
        "Golongan Darah": data.get("Golongan Darah", "Not Found"),
        "Berlaku Hingga": data.get("Berlaku Hingga", "Not Found"),
        "Provinsi": province,
        "Kota/Kabupaten": city
    }
