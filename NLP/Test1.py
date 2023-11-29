import spacy

english_nlp = spacy.load('en_core_web_sm')

text = '''
¥ தமதரசாங்கம்‌.

Government of India

காஜா முஹ்யத்தீன்‌ சை
Kaja Mohyaddeen 8

பிறந்த நாள்‌ / ௦௦8 10/11/2002
ஆண்பால்‌ / Male

8176 7259 2634

எனது ஆதார்‌, எனது அடையாளம்‌

26/08/2015

bid றதுமுதனைதுவதுமையாள ஆணையபி

AADHAAR

Unique Identification Authority of India

க ர்‌

முகவரி: தந்தை : தாய பெயர்‌. சைபுதீன்‌
BOT & மாமனந்தல்‌ கள்ளக்குறிச்சி

விழுப்புரம்‌ தமிழ்‌ நாடு. 606202

Address: S/O: Saifudeen, 8/10A, KA
MAMANANDAL, Kallakkurichi, Villupuram

Tamil Nadu, 606202 Romy Rese
sa

8176 7259 2634 ay

MS help@uidai.gov.In www. uidai.gov.in

ஜீ 1947
'''

text2 = '''
ஸ்ரீராம்‌ மாமுண்டி
Sriram Mamundi

பிறந்த நாள்‌ / DOB: 11/04/1992
ஆண்‌ | MALE

8416 1590 3267
'''

spacy_parser = english_nlp(text2)

for entity in spacy_parser.ents:
    print(f'Found: {entity.text} of type: {entity.label_}')