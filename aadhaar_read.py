import re


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
        print("Names:", names)

        # Cleaning first names
        name = names.pop()
        name = name.rstrip()
        name = name.lstrip()
        name = name.replace("8", "B")
        name = name.replace("0", "D")
        name = name.replace("6", "G")
        name = name.replace("1", "I")
        name = re.sub('[^a-zA-Z] +', ' ', name)
        #
        # name_pattern = re.compile(r'[A-Za-z ]+')
        # names = [match.group(0).strip() for match in name_pattern.finditer(' '.join(text0))]
        # print("Name :: ",names)



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
            issue_date = dobs[0]
            print('issue date: ',issue_date)
            dob = dobs[1]
        else:
            dob = dobs[0]
        # print("Dob",dob)

        # Cleaning Adhaar number details
        aadhar_number = ''
        for word in res:
            if len(word) == 4 and word.isdigit():
                aadhar_number = aadhar_number + word + ' '
        if len(aadhar_number) >= 14:
            print("Aadhar number is :" + aadhar_number)
        else:
            print("Aadhar number not read")
        adh = aadhar_number



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