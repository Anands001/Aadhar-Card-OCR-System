import regex

def extract_aadhaar_names(text):
    # Regular expression pattern to match names in multiple languages
    name_pattern = regex.compile(r'\p{L}[\p{L}\s.,-]*', regex.UNICODE)

    # Find all matches in the given text
    matches = name_pattern.findall(text)

    # Join the matches to form the complete name
    extracted_name = ' '.join(matches).strip()

    return extracted_name if extracted_name else None

# Example usage with Aadhaar card text in different languages
aadhaar_texts = [
    'John Doe',
    'जॉन डो',
    'ஜான் டோ',
    'ജോൺ ഡോ',
    'ಜಾನ್ ಡೋ',
]

# Extract names from each Aadhaar card text
aadhaar_names = [extract_aadhaar_names(text) for text in aadhaar_texts]

# Filter out None values (where a name couldn't be found)
aadhaar_names = [name for name in aadhaar_names if name is not None]

print("Extracted Aadhaar Names:", aadhaar_names)
