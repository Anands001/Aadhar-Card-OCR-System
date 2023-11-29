import re
import langid


import re

import spacy


def adhaar_read_data1(text):
    name = None
    dob = None
    adh = None
    sex = None

    try:
        # Extract names
        # name_pattern = re.compile(r'\b[A-Z][a-zA-Z\s.]+\b')
        # name_pattern = re.compile(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+")
        # names = name_pattern.findall(text)
        # name = ' '.join(names).strip()

        NER = spacy.load("en_core_web_sm")

        # Extracting entities using spaCy NER
        doc = NER(text)
        regex_name = []

        # Extracting names using spaCy NER
        # for ent in doc.ents:
        #     if ent.label_ in ["PERSON", "NOUN", "PROPN"]:
        #         regex_name.extend(re.findall("[A-Z][a-z]+", ent.text))
        #
        # # If no names found, use a fallback regex on the entire OCR result
        # if not regex_name:
        #     regex_name.extend(re.findall("[A-Z][a-z]+", text))
        #
        # # Extracted names
        # print("Extracted Names:", regex_name)
        img2str_config_name = "--psm 4 --oem 3"
        res_string_name = text
        name = NER(res_string_name)

        for word in name.ents:
            if word.label_ == "PERSON":
                regex_name = re.findall("[A-Z][a-z]+", word.text)
        if not regex_name:
            regex_name = re.findall("[A-Z][a-z]+", res_string_name)
        print(res_string_name)
        print(regex_name)
        name = regex_name

        # Extract date of birth
        dob_pattern = re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b')
        dob = dob_pattern.search(text).group(0)

        # Extract Aadhaar number
        adh_pattern = re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b')
        adh = adh_pattern.search(text).group(0)

        # Determine gender
        sex_pattern = re.compile(r'\bMale\b|\bFemale\b')
        sex_match = sex_pattern.search(text)
        sex = "MALE" if (sex_match and "Male" in sex_match.group(0)) else "FEMALE"

        # Post-process the name to remove unwanted information
        if "AADHAAR" in name:
            name = name.split("AADHAAR")[0].strip()

    except Exception as e:
        print(f"Error: {e}")

    data = {
        'Name': name,
        'Date of Birth': dob,
        'Adhaar Number': adh,
        'Sex': sex,
        'ID Type': 'Adhaar'
    }

    print("data: ",data)

    return data



def adhaar_read_data(text):
    res = text.split()
    name = None
    dob = None
    adh = None
    sex = None
    nameline = []
    dobline = []
    text0 = []
    text1 = []
    text2 = []
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n', '')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    if 'female' in text.lower():
        sex = "FEMALE"
    else:
        sex = "MALE"

    text1 = list(filter(None, text1))
    text0 = text1[:]
    print(text0)
    print(text1)
    print(text2)
    try:

        name_pattern = re.compile(r'\b[A-Z][a-z]* [A-Z][a-z]*\b')

        # Find all matches in the text
        matches = name_pattern.findall(text)

        # Extracted names
        names = [match.strip() for match in matches]

        # Print or use the extracted names as needed

        # Cleaning first names
        # name = names.pop()
        for name in names:
            name = name.rstrip()
            name = name.lstrip()
            name = name.replace("8", "B")
            name = name.replace("0", "D")
            name = name.replace("6", "G")
            name = name.replace("1", "I")
            name = re.sub('[^a-zA-Z] +', ' ', name)

        text1 = ' '.join(names)
        NER = spacy.load("en_core_web_sm")

        res_string_name = text1
        name = NER(res_string_name)

        for word in name.ents:
            if word.label_ == "PERSON":
                regex_name = re.findall("[A-Z][a-z]+", word.text)
        if not regex_name:
            regex_name = re.findall("[A-Z][a-z]+", res_string_name)
        print(res_string_name)
        print(regex_name)
        name = regex_name
        print("Names:", names)




        # Cleaning DOB
        # dob = text0[2][-10:]
        # dob = dob.rstrip()
        # dob = dob.lstrip()
        # dob = dob.replace('l', '/')
        # dob = dob.replace('L', '/')
        # dob = dob.replace('I', '/')
        # dob = dob.replace('i', '/')
        # dob = dob.replace('|', '/')
        # dob = dob.replace('\"', '/1')
        # dob = dob.replace(":", "")
        # dob = dob.replace(" ", "")

        dob_pattern = re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b')
        dobs = [match.group(0) for match in dob_pattern.finditer(' '.join(text0))]
        dobs.sort()
        if len(dobs)>1:
            issue_date = dobs[1]
            print('issue date: ',issue_date)
            dob = dobs[0]
        else:
            dob = dobs[0]
        # print("Dob",dob)

        # Cleaning Adhaar number details
        # aadhar_number = ''
        # for word in res:
        #     if len(word) == 4 and word.isdigit():
        #         aadhar_number = aadhar_number + word + ' '
        # if len(aadhar_number) >= 14:
        #     print("Aadhar number is :" + aadhar_number)
        # else:
        #     print("Aadhar number not read")
        adh_pattern = re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b')
        adh = adh_pattern.search(text).group(0)



    except:
        pass

    data = {}
    data['Name'] = name
    data['Date of Birth'] = dob
    data['Adhaar Number'] = adh
    data['Sex'] = sex
    data['ID Type'] = "Adhaar"
    return data




def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split()
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno + 1:]
            return textlist
    return textlist