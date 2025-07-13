import re
import argparse

PII_PATTERNS = {
    "Full Names (Guessed)": r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b",
    "Phone Numbers": r"\b(?:\+?\d{1,3})?[\s.-]?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}\b",
    "Country of Origin": r"\b(Ireland|United States|USA|UK|Germany|France|China|India|Canada|Mexico|Russia|Japan|Brazil|Australia)\b",
    "Gender": r"\b(Male|Female|Non-binary|Transgender|Other|Man|Woman|Boy|Girl)\b",
    "Religion": r"\b(Christian|Muslim|Islam|Jewish|Hindu|Buddhist|Atheist|Agnostic|Catholic|Protestant|Sikh)\b",
    "Political Views": r"\b(Democrat|Republican|Liberal|Conservative|Labour|Tory|Socialist|Communist|Libertarian|Green Party)\b",
    "Email Addresses": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "Credit Card Numbers": r"\b(?:\d[ -]*?){13,16}\b",
    "Social Security Numbers": r"\b\d{3}-\d{2}-\d{4}\b",
    "PPS Numbers (Ireland)": r"\b\d{7}[A-Z]{1,2}\b",
    "NINO (UK)": r"\b[A-CEGHJ-PR-TW-Z]{2}\d{6}[A-D]?\b",
    "SIN (Canada)": r"\b\d{3}-\d{3}-\d{3}\b",
    "Passport Numbers": r"\b([A-Z]{2}\d{7}|\d{9})\b",
    "Driver's License Numbers": r"\b[A-Z0-9]{5,15}\b",
    "IBAN Numbers": r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b",
    "Bank Routing Numbers": r"\b\d{9}\b",
    "Bitcoin Wallet": r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b",
    "Ethereum Wallet": r"\b0x[a-fA-F0-9]{40}\b",
    "Medical Identifiers": r"\bNHS\d{6,10}|ICD-\d{1,4}[A-Z]?\b",
    "Birth Dates": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "Street Addresses": r"\b\d{1,5}\s\w+(?:\s\w+)*\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b",
    "ZIP/Postcodes": r"\b\d{5}(?:[-\s]?\d{4})?|\b[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}\b",
    "Public IP Addresses": r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b",
    "MAC Addresses": r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b",
    "Geolocation Coordinates": r"\b[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?((1[0-7]\d)|([1-9]?\d))(\.\d+)?\b",
    "Serial Numbers": r"\b[A-Z0-9]{8,20}\b",
}

def scan_file_for_pii(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[!] File not found: {filepath}")
        return

    print(f"[*] Scanning file: {filepath}")
    results = {}
    for label, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            # Flatten matches if nested (e.g. tuples)
            flat_matches = [m[0] if isinstance(m, tuple) else m for m in matches]
            results[label] = list(set(flat_matches))  # Deduplicate

    if results:
        print("[*] PII Detected:\n")
        for category, items in results.items():
            print(f"== {category} ==")
            for item in items:
                print(f"- {item}")
            print()
    else:
        print("[*] No PII detected.")

def main():
    parser = argparse.ArgumentParser(description="Scan a file for PII using regular expressions.")
    parser.add_argument("file", help="Path to the file to scan")
    args = parser.parse_args()

    scan_file_for_pii(args.file)

if __name__ == "__main__":
    main()
