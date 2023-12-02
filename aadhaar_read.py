import re
import langid
from rapidfuzz import fuzz

import re

import spacy

def extract_and_clean_names(text):
    """
    Extract and clean names from the given text.

    Parameters:
    - text (str): The input text containing names.

    Returns:
    - str: The cleaned and extracted name(s).
    """

    # Check if the 're' and 'spacy' modules are available
    try:
        import re
        import spacy
    except ImportError:
        raise ImportError("The 're' and 'spacy' modules are required. Please install them.")

    # Check if the spaCy model is installed
    if "en_core_web_sm" not in spacy.util.get_installed_models():
        raise ValueError("The spaCy model 'en_core_web_sm' is required. Please install it using 'python -m spacy download en_core_web_sm'.")

    # Extract names using regex
    text = ''.join(text)
    address_position = text.find("address".lower())
    name_text = text[:address_position].strip()
    name_pattern = re.compile(r'\b[A-Z][a-z]* [A-Z][a-z]*\b')
    matches = name_pattern.findall(name_text)
    names = [match.strip() for match in matches]

    # Clean and modify names
    for i in range(len(names)):
        names[i] = names[i].rstrip()
        names[i] = names[i].lstrip()
        names[i] = names[i].replace("8", "B")
        names[i] = names[i].replace("0", "D")
        names[i] = names[i].replace("6", "G")
        names[i] = names[i].replace("1", "I")
        names[i] = re.sub('[^a-zA-Z]+', ' ', names[i])

    common_strings = ['Unique Identification', 'Government', 'India', 'authority', 'aadhar', 'Issue Date']

    # Filter out names containing common strings
    cleaned_names = [name for name in names if not any(common_str.lower() in name.lower() for common_str in common_strings)]

    # Check if there are cleaned names to process
    if not cleaned_names:
        return "No valid names found in the input text."

    # Join cleaned names into a single string
    full_name = ''.join(cleaned_names)

    # If there is only one name, return it
    if len(cleaned_names) == 1:
        return full_name
    else:
        # Process with spaCy for named entity recognition
        NER = spacy.load("en_core_web_sm")
        text1 = ' '.join(cleaned_names)
        name_entities = NER(text1)

        # Extract names from spaCy entities
        extracted_names = [ent.text for ent in name_entities.ents if ent.label_ == "PERSON"]

        state_names = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat',
                       'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
                       'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
                       'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                       'Uttarakhand', 'West Bengal', 'Andaman', 'Nicobar', 'Chandigarh', 'Dadra', 'Nagar Haveli',
                       'Daman', 'Diu', 'Lakshadweep', 'Delhi', 'Puducherry', 'Jammu', 'Kashmir', 'Ladakh']

        # Filter out names containing state names
        cleaned_names = [word for word in extracted_names if word not in state_names]

        # Join the final cleaned names into a single string
        full_name = ' '.join(cleaned_names)

        return full_name

def adhaar_read_data(text,img):
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
    # print('text0 ',text0)
    # print('text1 ',text1)
    # print('text2 ',text2)
    try:
        extracted_names = extract_and_clean_names(text)

        # print("Cleaned Names:", cleaned_names)
        print("Extracted Names:", extracted_names)
        name = extracted_names
        # print("Names:", names)
    except Exception as e:
        print("Exception occured while extracting name")
        print(e)
    try:

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
        adh_pattern = re.compile(r'\d\d\d\d \d\d\d\d \d\d\d\d')
        adh = adh_pattern.search(text).group(0)

        if(text.find("address".lower()) ):
            # print("Address : ",get_address(img,True))
            print("Address dict : ",get_address1(text))
    except Exception as e:
        print("Exception oocured while extracting: ",e)

    data = {}
    data['Name'] = name
    data['Date of Birth'] = dob
    data['Adhaar Number'] = adh
    data['Sex'] = sex
    data['ID Type'] = "Adhaar"
    return data



def get_address1(text):
    address_position = text.lower().find("address".lower())
    addr_text = text[address_position:].strip()
    print("Address text: ", addr_text)
    state_names = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat',
                   'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
                   'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
                   'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                   'Uttarakhand', 'West Bengal', 'Andaman', 'Nicobar', 'Chandigarh', 'Dadra', 'Nagar Haveli',
                   'Daman', 'Diu', 'Lakshadweep', 'Delhi', 'Puducherry', 'Jammu', 'Kashmir', 'Ladakh']

    indian_cities = {
        "Andaman and Nicobar Islands": [
            "Port Blair"
        ],
        "Haryana": [
            "Faridabad",
            "Gurgaon",
            "Hisar",
            "Rohtak",
            "Panipat",
            "Karnal",
            "Sonipat",
            "Yamunanagar",
            "Panchkula",
            "Bhiwani",
            "Bahadurgarh",
            "Jind",
            "Sirsa",
            "Thanesar",
            "Kaithal",
            "Palwal",
            "Rewari",
            "Hansi",
            "Narnaul",
            "Fatehabad",
            "Gohana",
            "Tohana",
            "Narwana",
            "Mandi Dabwali",
            "Charkhi Dadri",
            "Shahbad",
            "Pehowa",
            "Samalkha",
            "Pinjore",
            "Ladwa",
            "Sohna",
            "Safidon",
            "Taraori",
            "Mahendragarh",
            "Ratia",
            "Rania",
            "Sarsod"
        ],
        "Tamil Nadu": [
            "Chennai",
            "Coimbatore",
            "Madurai",
            "Tiruchirappalli",
            "Salem",
            "Tirunelveli",
            "Tiruppur",
            "Ranipet",
            "Nagercoil",
            "Thanjavur",
            "Vellore",
            "Kancheepuram",
            "Erode",
            "Tiruvannamalai",
            "Pollachi",
            "Rajapalayam",
            "Sivakasi",
            "Pudukkottai",
            "Neyveli (TS)",
            "Nagapattinam",
            "Viluppuram",
            "Tiruchengode",
            "Vaniyambadi",
            "Theni Allinagaram",
            "Udhagamandalam",
            "Aruppukkottai",
            "Paramakudi",
            "Arakkonam",
            "Virudhachalam",
            "Srivilliputhur",
            "Tindivanam",
            "Virudhunagar",
            "Karur",
            "Valparai",
            "Sankarankovil",
            "Tenkasi",
            "Palani",
            "Pattukkottai",
            "Tirupathur",
            "Ramanathapuram",
            "Udumalaipettai",
            "Gobichettipalayam",
            "Thiruvarur",
            "Thiruvallur",
            "Panruti",
            "Namakkal",
            "Thirumangalam",
            "Vikramasingapuram",
            "Nellikuppam",
            "Rasipuram",
            "Tiruttani",
            "Nandivaram-Guduvancheri",
            "Periyakulam",
            "Pernampattu",
            "Vellakoil",
            "Sivaganga",
            "Vadalur",
            "Rameshwaram",
            "Tiruvethipuram",
            "Perambalur",
            "Usilampatti",
            "Vedaranyam",
            "Sathyamangalam",
            "Puliyankudi",
            "Nanjikottai",
            "Thuraiyur",
            "Sirkali",
            "Tiruchendur",
            "Periyasemur",
            "Sattur",
            "Vandavasi",
            "Tharamangalam",
            "Tirukkoyilur",
            "Oddanchatram",
            "Palladam",
            "Vadakkuvalliyur",
            "Tirukalukundram",
            "Uthamapalayam",
            "Surandai",
            "Sankari",
            "Shenkottai",
            "Vadipatti",
            "Sholingur",
            "Tirupathur",
            "Manachanallur",
            "Viswanatham",
            "Polur",
            "Panagudi",
            "Uthiramerur",
            "Thiruthuraipoondi",
            "Pallapatti",
            "Ponneri",
            "Lalgudi",
            "Natham",
            "Unnamalaikadai",
            "P.N.Patti",
            "Tharangambadi",
            "Tittakudi",
            "Pacode",
            "O' Valley",
            "Suriyampalayam",
            "Sholavandan",
            "Thammampatti",
            "Namagiripettai",
            "Peravurani",
            "Parangipettai",
            "Pudupattinam",
            "Pallikonda",
            "Sivagiri",
            "Punjaipugalur",
            "Padmanabhapuram",
            "Thirupuvanam"
        ],
        "Madhya Pradesh": [
            "Indore",
            "Bhopal",
            "Jabalpur",
            "Gwalior",
            "Ujjain",
            "Sagar",
            "Ratlam",
            "Satna",
            "Murwara (Katni)",
            "Morena",
            "Singrauli",
            "Rewa",
            "Vidisha",
            "Ganjbasoda",
            "Shivpuri",
            "Mandsaur",
            "Neemuch",
            "Nagda",
            "Itarsi",
            "Sarni",
            "Sehore",
            "Mhow Cantonment",
            "Seoni",
            "Balaghat",
            "Ashok Nagar",
            "Tikamgarh",
            "Shahdol",
            "Pithampur",
            "Alirajpur",
            "Mandla",
            "Sheopur",
            "Shajapur",
            "Panna",
            "Raghogarh-Vijaypur",
            "Sendhwa",
            "Sidhi",
            "Pipariya",
            "Shujalpur",
            "Sironj",
            "Pandhurna",
            "Nowgong",
            "Mandideep",
            "Sihora",
            "Raisen",
            "Lahar",
            "Maihar",
            "Sanawad",
            "Sabalgarh",
            "Umaria",
            "Porsa",
            "Narsinghgarh",
            "Malaj Khand",
            "Sarangpur",
            "Mundi",
            "Nepanagar",
            "Pasan",
            "Mahidpur",
            "Seoni-Malwa",
            "Rehli",
            "Manawar",
            "Rahatgarh",
            "Panagar",
            "Wara Seoni",
            "Tarana",
            "Sausar",
            "Rajgarh",
            "Niwari",
            "Mauganj",
            "Manasa",
            "Nainpur",
            "Prithvipur",
            "Sohagpur",
            "Nowrozabad (Khodargama)",
            "Shamgarh",
            "Maharajpur",
            "Multai",
            "Pali",
            "Pachore",
            "Rau",
            "Mhowgaon",
            "Vijaypur",
            "Narsinghgarh"
        ],
        "Jharkhand": [
            "Dhanbad",
            "Ranchi",
            "Jamshedpur",
            "Bokaro Steel City",
            "Deoghar",
            "Phusro",
            "Adityapur",
            "Hazaribag",
            "Giridih",
            "Ramgarh",
            "Jhumri Tilaiya",
            "Saunda",
            "Sahibganj",
            "Medininagar (Daltonganj)",
            "Chaibasa",
            "Chatra",
            "Gumia",
            "Dumka",
            "Madhupur",
            "Chirkunda",
            "Pakaur",
            "Simdega",
            "Musabani",
            "Mihijam",
            "Patratu",
            "Lohardaga",
            "Tenu dam-cum-Kathhara"
        ],
        "Mizoram": [
            "Aizawl",
            "Lunglei",
            "Saiha"
        ],
        "Nagaland": [
            "Dimapur",
            "Kohima",
            "Zunheboto",
            "Tuensang",
            "Wokha",
            "Mokokchung"
        ],
        "Himachal Pradesh": [
            "Shimla",
            "Mandi",
            "Solan",
            "Nahan",
            "Sundarnagar",
            "Palampur",
            "Kullu"
        ],
        "Tripura": [
            "Agartala",
            "Udaipur",
            "Dharmanagar",
            "Pratapgarh",
            "Kailasahar",
            "Belonia",
            "Khowai"
        ],
        "Andhra Pradesh": [
            "Visakhapatnam",
            "Vijayawada",
            "Guntur",
            "Nellore",
            "Kurnool",
            "Rajahmundry",
            "Kakinada",
            "Tirupati",
            "Anantapur",
            "Kadapa",
            "Vizianagaram",
            "Eluru",
            "Ongole",
            "Nandyal",
            "Machilipatnam",
            "Adoni",
            "Tenali",
            "Chittoor",
            "Hindupur",
            "Proddatur",
            "Bhimavaram",
            "Madanapalle",
            "Guntakal",
            "Dharmavaram",
            "Gudivada",
            "Srikakulam",
            "Narasaraopet",
            "Rajampet",
            "Tadpatri",
            "Tadepalligudem",
            "Chilakaluripet",
            "Yemmiganur",
            "Kadiri",
            "Chirala",
            "Anakapalle",
            "Kavali",
            "Palacole",
            "Sullurpeta",
            "Tanuku",
            "Rayachoti",
            "Srikalahasti",
            "Bapatla",
            "Naidupet",
            "Nagari",
            "Gudur",
            "Vinukonda",
            "Narasapuram",
            "Nuzvid",
            "Markapur",
            "Ponnur",
            "Kandukur",
            "Bobbili",
            "Rayadurg",
            "Samalkot",
            "Jaggaiahpet",
            "Tuni",
            "Amalapuram",
            "Bheemunipatnam",
            "Venkatagiri",
            "Sattenapalle",
            "Pithapuram",
            "Palasa Kasibugga",
            "Parvathipuram",
            "Macherla",
            "Gooty",
            "Salur",
            "Mandapeta",
            "Jammalamadugu",
            "Peddapuram",
            "Punganur",
            "Nidadavole",
            "Repalle",
            "Ramachandrapuram",
            "Kovvur",
            "Tiruvuru",
            "Uravakonda",
            "Narsipatnam",
            "Yerraguntla",
            "Pedana",
            "Puttur",
            "Renigunta",
            "Rajam",
            "Srisailam Project (Right Flank Colony) Township"
        ],
        "Punjab": [
            "Ludhiana",
            "Patiala",
            "Amritsar",
            "Jalandhar",
            "Bathinda",
            "Pathankot",
            "Hoshiarpur",
            "Batala",
            "Moga",
            "Malerkotla",
            "Khanna",
            "Mohali",
            "Barnala",
            "Firozpur",
            "Phagwara",
            "Kapurthala",
            "Zirakpur",
            "Kot Kapura",
            "Faridkot",
            "Muktsar",
            "Rajpura",
            "Sangrur",
            "Fazilka",
            "Gurdaspur",
            "Kharar",
            "Gobindgarh",
            "Mansa",
            "Malout",
            "Nabha",
            "Tarn Taran",
            "Jagraon",
            "Sunam",
            "Dhuri",
            "Firozpur Cantt.",
            "Sirhind Fatehgarh Sahib",
            "Rupnagar",
            "Jalandhar Cantt.",
            "Samana",
            "Nawanshahr",
            "Rampura Phul",
            "Nangal",
            "Nakodar",
            "Zira",
            "Patti",
            "Raikot",
            "Longowal",
            "Urmar Tanda",
            "Morinda, India",
            "Phillaur",
            "Pattran",
            "Qadian",
            "Sujanpur",
            "Mukerian",
            "Talwara"
        ],
        "Chandigarh": [
            "Chandigarh"
        ],
        "Rajasthan": [
            "Jaipur",
            "Jodhpur",
            "Bikaner",
            "Udaipur",
            "Ajmer",
            "Bhilwara",
            "Alwar",
            "Bharatpur",
            "Pali",
            "Barmer",
            "Sikar",
            "Tonk",
            "Sadulpur",
            "Sawai Madhopur",
            "Nagaur",
            "Makrana",
            "Sujangarh",
            "Sardarshahar",
            "Ladnu",
            "Ratangarh",
            "Nokha",
            "Nimbahera",
            "Suratgarh",
            "Rajsamand",
            "Lachhmangarh",
            "Rajgarh (Churu)",
            "Nasirabad",
            "Nohar",
            "Phalodi",
            "Nathdwara",
            "Pilani",
            "Merta City",
            "Sojat",
            "Neem-Ka-Thana",
            "Sirohi",
            "Pratapgarh",
            "Rawatbhata",
            "Sangaria",
            "Lalsot",
            "Pilibanga",
            "Pipar City",
            "Taranagar",
            "Vijainagar, Ajmer",
            "Sumerpur",
            "Sagwara",
            "Ramganj Mandi",
            "Lakheri",
            "Udaipurwati",
            "Losal",
            "Sri Madhopur",
            "Ramngarh",
            "Rawatsar",
            "Rajakhera",
            "Shahpura",
            "Shahpura",
            "Raisinghnagar",
            "Malpura",
            "Nadbai",
            "Sanchore",
            "Nagar",
            "Rajgarh (Alwar)",
            "Sheoganj",
            "Sadri",
            "Todaraisingh",
            "Todabhim",
            "Reengus",
            "Rajaldesar",
            "Sadulshahar",
            "Sambhar",
            "Prantij",
            "Mount Abu",
            "Mangrol",
            "Phulera",
            "Mandawa",
            "Pindwara",
            "Mandalgarh",
            "Takhatgarh"
        ],
        "Assam": [
            "Guwahati",
            "Silchar",
            "Dibrugarh",
            "Nagaon",
            "Tinsukia",
            "Jorhat",
            "Bongaigaon City",
            "Dhubri",
            "Diphu",
            "North Lakhimpur",
            "Tezpur",
            "Karimganj",
            "Sibsagar",
            "Goalpara",
            "Barpeta",
            "Lanka",
            "Lumding",
            "Mankachar",
            "Nalbari",
            "Rangia",
            "Margherita",
            "Mangaldoi",
            "Silapathar",
            "Mariani",
            "Marigaon"
        ],
        "Odisha": [
            "Bhubaneswar",
            "Cuttack",
            "Raurkela",
            "Brahmapur",
            "Sambalpur",
            "Puri",
            "Baleshwar Town",
            "Baripada Town",
            "Bhadrak",
            "Balangir",
            "Jharsuguda",
            "Bargarh",
            "Paradip",
            "Bhawanipatna",
            "Dhenkanal",
            "Barbil",
            "Kendujhar",
            "Sunabeda",
            "Rayagada",
            "Jatani",
            "Byasanagar",
            "Kendrapara",
            "Rajagangapur",
            "Parlakhemundi",
            "Talcher",
            "Sundargarh",
            "Phulabani",
            "Pattamundai",
            "Titlagarh",
            "Nabarangapur",
            "Soro",
            "Malkangiri",
            "Rairangpur",
            "Tarbha"
        ],
        "Chhattisgarh": [
            "Raipur",
            "Bhilai Nagar",
            "Korba",
            "Bilaspur",
            "Durg",
            "Rajnandgaon",
            "Jagdalpur",
            "Raigarh",
            "Ambikapur",
            "Mahasamund",
            "Dhamtari",
            "Chirmiri",
            "Bhatapara",
            "Dalli-Rajhara",
            "Naila Janjgir",
            "Tilda Newra",
            "Mungeli",
            "Manendragarh",
            "Sakti"
        ],
        "Jammu and Kashmir": [
            "Srinagar",
            "Jammu",
            "Baramula",
            "Anantnag",
            "Sopore",
            "KathUrban Agglomeration",
            "Rajauri",
            "Punch",
            "Udhampur"
        ],
        "Karnataka": [
            "Bengaluru",
            "Hubli-Dharwad",
            "Belagavi",
            "Mangaluru",
            "Davanagere",
            "Ballari",
            "Mysore",
            "Tumkur",
            "Shivamogga",
            "Raayachuru",
            "Robertson Pet",
            "Kolar",
            "Mandya",
            "Udupi",
            "Chikkamagaluru",
            "Karwar",
            "Ranebennuru",
            "Ranibennur",
            "Ramanagaram",
            "Gokak",
            "Yadgir",
            "Rabkavi Banhatti",
            "Shahabad",
            "Sirsi",
            "Sindhnur",
            "Tiptur",
            "Arsikere",
            "Nanjangud",
            "Sagara",
            "Sira",
            "Puttur",
            "Athni",
            "Mulbagal",
            "Surapura",
            "Siruguppa",
            "Mudhol",
            "Sidlaghatta",
            "Shahpur",
            "Saundatti-Yellamma",
            "Wadi",
            "Manvi",
            "Nelamangala",
            "Lakshmeshwar",
            "Ramdurg",
            "Nargund",
            "Tarikere",
            "Malavalli",
            "Savanur",
            "Lingsugur",
            "Vijayapura",
            "Sankeshwara",
            "Madikeri",
            "Talikota",
            "Sedam",
            "Shikaripur",
            "Mahalingapura",
            "Mudalagi",
            "Muddebihal",
            "Pavagada",
            "Malur",
            "Sindhagi",
            "Sanduru",
            "Afzalpur",
            "Maddur",
            "Madhugiri",
            "Tekkalakote",
            "Terdal",
            "Mudabidri",
            "Magadi",
            "Navalgund",
            "Shiggaon",
            "Shrirangapattana",
            "Sindagi",
            "Sakaleshapura",
            "Srinivaspur",
            "Ron",
            "Mundargi",
            "Sadalagi",
            "Piriyapatna",
            "Adyar"
        ],
        "Manipur": [
            "Imphal",
            "Thoubal",
            "Lilong",
            "Mayang Imphal"
        ],
        "Kerala": [
            "Thiruvananthapuram",
            "Kochi",
            "Kozhikode",
            "Kollam",
            "Thrissur",
            "Palakkad",
            "Alappuzha",
            "Malappuram",
            "Ponnani",
            "Vatakara",
            "Kanhangad",
            "Taliparamba",
            "Koyilandy",
            "Neyyattinkara",
            "Kayamkulam",
            "Nedumangad",
            "Kannur",
            "Tirur",
            "Kottayam",
            "Kasaragod",
            "Kunnamkulam",
            "Ottappalam",
            "Thiruvalla",
            "Thodupuzha",
            "Chalakudy",
            "Changanassery",
            "Punalur",
            "Nilambur",
            "Cherthala",
            "Perinthalmanna",
            "Mattannur",
            "Shoranur",
            "Varkala",
            "Paravoor",
            "Pathanamthitta",
            "Peringathur",
            "Attingal",
            "Kodungallur",
            "Pappinisseri",
            "Chittur-Thathamangalam",
            "Muvattupuzha",
            "Adoor",
            "Mavelikkara",
            "Mavoor",
            "Perumbavoor",
            "Vaikom",
            "Palai",
            "Panniyannur",
            "Guruvayoor",
            "Puthuppally",
            "Panamattom"
        ],
        "Delhi": [
            "Delhi",
            "New Delhi"
        ],
        "Dadra and Nagar Haveli": [
            "Silvassa"
        ],
        "Puducherry": [
            "Pondicherry",
            "Karaikal",
            "Yanam",
            "Mahe"
        ],
        "Uttarakhand": [
            "Dehradun",
            "Hardwar",
            "Haldwani-cum-Kathgodam",
            "Srinagar",
            "Kashipur",
            "Roorkee",
            "Rudrapur",
            "Rishikesh",
            "Ramnagar",
            "Pithoragarh",
            "Manglaur",
            "Nainital",
            "Mussoorie",
            "Tehri",
            "Pauri",
            "Nagla",
            "Sitarganj",
            "Bageshwar"
        ],
        "Uttar Pradesh": [
            "Lucknow",
            "Kanpur",
            "Firozabad",
            "Agra",
            "Meerut",
            "Varanasi",
            "Allahabad",
            "Amroha",
            "Moradabad",
            "Aligarh",
            "Saharanpur",
            "Noida",
            "Loni",
            "Jhansi",
            "Shahjahanpur",
            "Rampur",
            "Modinagar",
            "Hapur",
            "Etawah",
            "Sambhal",
            "Orai",
            "Bahraich",
            "Unnao",
            "Rae Bareli",
            "Lakhimpur",
            "Sitapur",
            "Lalitpur",
            "Pilibhit",
            "Chandausi",
            "Hardoi ",
            "Azamgarh",
            "Khair",
            "Sultanpur",
            "Tanda",
            "Nagina",
            "Shamli",
            "Najibabad",
            "Shikohabad",
            "Sikandrabad",
            "Shahabad, Hardoi",
            "Pilkhuwa",
            "Renukoot",
            "Vrindavan",
            "Ujhani",
            "Laharpur",
            "Tilhar",
            "Sahaswan",
            "Rath",
            "Sherkot",
            "Kalpi",
            "Tundla",
            "Sandila",
            "Nanpara",
            "Sardhana",
            "Nehtaur",
            "Seohara",
            "Padrauna",
            "Mathura",
            "Thakurdwara",
            "Nawabganj",
            "Siana",
            "Noorpur",
            "Sikandra Rao",
            "Puranpur",
            "Rudauli",
            "Thana Bhawan",
            "Palia Kalan",
            "Zaidpur",
            "Nautanwa",
            "Zamania",
            "Shikarpur, Bulandshahr",
            "Naugawan Sadat",
            "Fatehpur Sikri",
            "Shahabad, Rampur",
            "Robertsganj",
            "Utraula",
            "Sadabad",
            "Rasra",
            "Lar",
            "Lal Gopalganj Nindaura",
            "Sirsaganj",
            "Pihani",
            "Shamsabad, Agra",
            "Rudrapur",
            "Soron",
            "SUrban Agglomerationr",
            "Samdhan",
            "Sahjanwa",
            "Rampur Maniharan",
            "Sumerpur",
            "Shahganj",
            "Tulsipur",
            "Tirwaganj",
            "PurqUrban Agglomerationzi",
            "Shamsabad, Farrukhabad",
            "Warhapur",
            "Powayan",
            "Sandi",
            "Achhnera",
            "Naraura",
            "Nakur",
            "Sahaspur",
            "Safipur",
            "Reoti",
            "Sikanderpur",
            "Saidpur",
            "Sirsi",
            "Purwa",
            "Parasi",
            "Lalganj",
            "Phulpur",
            "Shishgarh",
            "Sahawar",
            "Samthar",
            "Pukhrayan",
            "Obra",
            "Niwai",
            "Mirzapur"
        ],
        "Bihar": [
            "Patna",
            "Gaya",
            "Bhagalpur",
            "Muzaffarpur",
            "Darbhanga",
            "Arrah",
            "Begusarai",
            "Chhapra",
            "Katihar",
            "Munger",
            "Purnia",
            "Saharsa",
            "Sasaram",
            "Hajipur",
            "Dehri-on-Sone",
            "Bettiah",
            "Motihari",
            "Bagaha",
            "Siwan",
            "Kishanganj",
            "Jamalpur",
            "Buxar",
            "Jehanabad",
            "Aurangabad",
            "Lakhisarai",
            "Nawada",
            "Jamui",
            "Sitamarhi",
            "Araria",
            "Gopalganj",
            "Madhubani",
            "Masaurhi",
            "Samastipur",
            "Mokameh",
            "Supaul",
            "Dumraon",
            "Arwal",
            "Forbesganj",
            "BhabUrban Agglomeration",
            "Narkatiaganj",
            "Naugachhia",
            "Madhepura",
            "Sheikhpura",
            "Sultanganj",
            "Raxaul Bazar",
            "Ramnagar",
            "Mahnar Bazar",
            "Warisaliganj",
            "Revelganj",
            "Rajgir",
            "Sonepur",
            "Sherghati",
            "Sugauli",
            "Makhdumpur",
            "Maner",
            "Rosera",
            "Nokha",
            "Piro",
            "Rafiganj",
            "Marhaura",
            "Mirganj",
            "Lalganj",
            "Murliganj",
            "Motipur",
            "Manihari",
            "Sheohar",
            "Maharajganj",
            "Silao",
            "Barh",
            "Asarganj"
        ],
        "Gujarat": [
            "Ahmedabad",
            "Surat",
            "Vadodara",
            "Rajkot",
            "Bhavnagar",
            "Jamnagar",
            "Nadiad",
            "Porbandar",
            "Anand",
            "Morvi",
            "Mahesana",
            "Bharuch",
            "Vapi",
            "Navsari",
            "Veraval",
            "Bhuj",
            "Godhra",
            "Palanpur",
            "Valsad",
            "Patan",
            "Deesa",
            "Amreli",
            "Anjar",
            "Dhoraji",
            "Khambhat",
            "Mahuva",
            "Keshod",
            "Wadhwan",
            "Ankleshwar",
            "Savarkundla",
            "Kadi",
            "Visnagar",
            "Upleta",
            "Una",
            "Sidhpur",
            "Unjha",
            "Mangrol",
            "Viramgam",
            "Modasa",
            "Palitana",
            "Petlad",
            "Kapadvanj",
            "Sihor",
            "Wankaner",
            "Limbdi",
            "Mandvi",
            "Thangadh",
            "Vyara",
            "Padra",
            "Lunawada",
            "Rajpipla",
            "Vapi",
            "Umreth",
            "Sanand",
            "Rajula",
            "Radhanpur",
            "Mahemdabad",
            "Ranavav",
            "Tharad",
            "Mansa",
            "Umbergaon",
            "Talaja",
            "Vadnagar",
            "Manavadar",
            "Salaya",
            "Vijapur",
            "Pardi",
            "Rapar",
            "Songadh",
            "Lathi",
            "Adalaj",
            "Chhapra",
            "Gandhinagar"
        ],
        "Telangana": [
            "Hyderabad",
            "Warangal",
            "Nizamabad",
            "Karimnagar",
            "Ramagundam",
            "Khammam",
            "Mahbubnagar",
            "Mancherial",
            "Adilabad",
            "Suryapet",
            "Jagtial",
            "Miryalaguda",
            "Nirmal",
            "Kamareddy",
            "Kothagudem",
            "Bodhan",
            "Palwancha",
            "Mandamarri",
            "Koratla",
            "Sircilla",
            "Tandur",
            "Siddipet",
            "Wanaparthy",
            "Kagaznagar",
            "Gadwal",
            "Sangareddy",
            "Bellampalle",
            "Bhongir",
            "Vikarabad",
            "Jangaon",
            "Bhadrachalam",
            "Bhainsa",
            "Farooqnagar",
            "Medak",
            "Narayanpet",
            "Sadasivpet",
            "Yellandu",
            "Manuguru",
            "Kyathampalle",
            "Nagarkurnool"
        ],
        "Meghalaya": [
            "Shillong",
            "Tura",
            "Nongstoin"
        ],
        "Himachal Praddesh": [
            "Manali"
        ],
        "Arunachal Pradesh": [
            "Naharlagun",
            "Pasighat"
        ],
        "Maharashtra": [
            "Mumbai",
            "Pune",
            "Nagpur",
            "Thane",
            "Nashik",
            "Kalyan-Dombivali",
            "Vasai-Virar",
            "Solapur",
            "Mira-Bhayandar",
            "Bhiwandi",
            "Amravati",
            "Nanded-Waghala",
            "Sangli",
            "Malegaon",
            "Akola",
            "Latur",
            "Dhule",
            "Ahmednagar",
            "Ichalkaranji",
            "Parbhani",
            "Panvel",
            "Yavatmal",
            "Achalpur",
            "Osmanabad",
            "Nandurbar",
            "Satara",
            "Wardha",
            "Udgir",
            "Aurangabad",
            "Amalner",
            "Akot",
            "Pandharpur",
            "Shrirampur",
            "Parli",
            "Washim",
            "Ambejogai",
            "Manmad",
            "Ratnagiri",
            "Uran Islampur",
            "Pusad",
            "Sangamner",
            "Shirpur-Warwade",
            "Malkapur",
            "Wani",
            "Lonavla",
            "Talegaon Dabhade",
            "Anjangaon",
            "Umred",
            "Palghar",
            "Shegaon",
            "Ozar",
            "Phaltan",
            "Yevla",
            "Shahade",
            "Vita",
            "Umarkhed",
            "Warora",
            "Pachora",
            "Tumsar",
            "Manjlegaon",
            "Sillod",
            "Arvi",
            "Nandura",
            "Vaijapur",
            "Wadgaon Road",
            "Sailu",
            "Murtijapur",
            "Tasgaon",
            "Mehkar",
            "Yawal",
            "Pulgaon",
            "Nilanga",
            "Wai",
            "Umarga",
            "Paithan",
            "Rahuri",
            "Nawapur",
            "Tuljapur",
            "Morshi",
            "Purna",
            "Satana",
            "Pathri",
            "Sinnar",
            "Uchgaon",
            "Uran",
            "Pen",
            "Karjat",
            "Manwath",
            "Partur",
            "Sangole",
            "Mangrulpir",
            "Risod",
            "Shirur",
            "Savner",
            "Sasvad",
            "Pandharkaoda",
            "Talode",
            "Shrigonda",
            "Shirdi",
            "Raver",
            "Mukhed",
            "Rajura",
            "Vadgaon Kasba",
            "Tirora",
            "Mahad",
            "Lonar",
            "Sawantwadi",
            "Pathardi",
            "Pauni",
            "Ramtek",
            "Mul",
            "Soyagaon",
            "Mangalvedhe",
            "Narkhed",
            "Shendurjana",
            "Patur",
            "Mhaswad",
            "Loha",
            "Nandgaon",
            "Warud"
        ],
        "Goa": [
            "Marmagao",
            "Panaji",
            "Margao",
            "Mapusa"
        ],
        "West Bengal": [
            "Kolkata",
            "Siliguri",
            "Asansol",
            "Raghunathganj",
            "Kharagpur",
            "Naihati",
            "English Bazar",
            "Baharampur",
            "Hugli-Chinsurah",
            "Raiganj",
            "Jalpaiguri",
            "Santipur",
            "Balurghat",
            "Medinipur",
            "Habra",
            "Ranaghat",
            "Bankura",
            "Nabadwip",
            "Darjiling",
            "Purulia",
            "Arambagh",
            "Tamluk",
            "AlipurdUrban Agglomerationr",
            "Suri",
            "Jhargram",
            "Gangarampur",
            "Rampurhat",
            "Kalimpong",
            "Sainthia",
            "Taki",
            "Murshidabad",
            "Memari",
            "Paschim Punropara",
            "Tarakeswar",
            "Sonamukhi",
            "PandUrban Agglomeration",
            "Mainaguri",
            "Malda",
            "Panchla",
            "Raghunathpur",
            "Mathabhanga",
            "Monoharpur",
            "Srirampore",
            "Adra"
        ]
    }
    state_found = None
    city_found = None
    state_threshold = 80  # Adjust this threshold based on your requirements
    city_threshold = 80  # Adjust this threshold based on your requirements

    # print("State Names: ", state_names)
    # print("Indian Cities: ", indian_cities)

    for state in state_names:
        similarity = fuzz.partial_ratio(state.lower(), addr_text.lower())
        print(f"State: {state}, Similarity: {similarity}")
        if similarity >= state_threshold:
            state_found = state
            break

    print("Final State: ", state_found)

    if state_found:
        cities = indian_cities.get(state_found, [])
        # print("Possible Cities: ", cities)

        for city in cities:
            similarity = fuzz.partial_ratio(city.lower(), addr_text.lower())
            print(f"City: {city}, Similarity: {similarity}")
            if similarity >= city_threshold:
                city_found = city
                break

        print("Final City: ", city_found)
    else:
        print("State not found in the address.")
    address = {
        "state" : state_found,
        "district" : city_found
    }
    # Use regular expressions to extract pin code, name, and additional details
    pin_pattern = re.compile(r'\b(\d{6})\b')
    name_pattern = re.compile(r'S/O: (\w+),')
    additional_details_pattern = re.compile(r'S/O: (\w+), \d+, (.+), (\d{6})')

    pin_match = pin_pattern.search(text)
    name_match = name_pattern.search(text)
    additional_details_match = additional_details_pattern.search(text)

    # Extracted information
    pincode_found = pin_match.group(1) if pin_match else None
    name_found = name_match.group(1) if name_match else None
    additional_details_found = additional_details_match.group(1) if additional_details_match else None

    # Print the extracted information
    print("PIN Code:", pincode_found)
    print("Name:", name_found)
    print("Additional Details:", additional_details_found)

    return address

def get_address(img, address=True):
    global four_points
    four_points = []
    res_string_address = None

    thresh = image_processing(img, address)
    # print("Thresh",thresh.shape)
    img2str_config_name = "--psm 4 --oem 3"
    res_string_address = pytesseract.image_to_string(thresh, lang='eng', config=img2str_config_name)
    regex_address = res_string_address.replace("Address:", "")
    regex_address = res_string_address.replace("Address :", "")
    regex_address = os.linesep.join([s for s in res_string_address.splitlines() if s])
    address_text = regex_address
    # Extract information using regular expressions
    name_pattern = re.compile(r'S/O: (\w+),')
    street_pattern = re.compile(r'\b(\d+/\w+), (\w+), (\w+),')
    pin_pattern = re.compile(r'\b(\d{6})\b')

    # Find matches in the address text
    name_match = name_pattern.search(address_text)
    street_match = street_pattern.search(address_text)
    pin_match = pin_pattern.search(address_text)

    # Extracted informationA
    name = name_match.group(1) if name_match else None
    street = street_match.group(1) if street_match else None
    city = street_match.group(2) if street_match else None
    state = street_match.group(3) if street_match else None
    pin_code = pin_match.group(1) if pin_match else None

    # Print the extracted information
    print("Name:", name)
    print("Street:", street)
    print("City:", city)
    print("State:", state)
    print("PIN Code:", pin_code)

    addr = {
        "name" : name,
        "street" : street,
        "city" : city,
        "state" : state,
        "pincode" : pin_code
    }

    return addr



def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split()
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno + 1:]
            return textlist
    return textlist