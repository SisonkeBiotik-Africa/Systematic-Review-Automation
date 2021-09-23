import spacy
import collections
import nltk
from nltk.corpus import stopwords
from wikibaseintegrator import wbi_functions, wbi_core
from pattern.text.en import singularize

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

#Open Clarivate Analytics Web of Science Plain Text
f = open("savedrecs01.txt", "r", encoding="utf8")

#Defining stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Process whole documents
s = []
for text in f:
    if (text.find("AB ")==0):
        text = text[3:].lower()
        doc = nlp(text)
        # Analyze syntax and get all noun phrases
        s += [chunk.text for chunk in doc.noun_chunks]

#Eliminating stop words and punctuations from noun phrases
sf = []
for i in s:
    word_tokens = i.split( )
    filtered_ngram = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_ngram = [singularize(plural) for plural in filtered_ngram]
    ss = " ".join(filtered_ngram)
    for j in [",", ";", "(", ")", "[", "]", "{", "}", "."]:
        ss = ss.replace(j,"")
    sf.append(ss)

#Eliminating uncommon noun phrases  
occurrences = collections.Counter(sf).most_common(300)

ontology = []
for item in occurrences:
    if (item[0]!=""):
        #Aligning common noun phrases to Wikidata
        wikidata_id = wbi_functions.search_entities(item[0])
        if (wikidata_id != []):
            wikidata_item = wbi_core.ItemEngine(item_id=wikidata_id[0], search_only=True)
            label = wikidata_item.get_aliases("en")
            label.append(wikidata_item.get_label("en"))
            label = [element.lower() for element in label]
            #Assigning common noun phrases to their parent classes in Wikidata
            if item[0] in label:
                try:
                    classes = [x["mainsnak"]["datavalue"]["value"]["id"] for x in wikidata_item.get_json_representation()["claims"]["P279"]]
                except KeyError:
                    print("P279 Statements Not Available")
                print(classes)
                try:
                    classes += [x["mainsnak"]["datavalue"]["value"]["id"] for x in wikidata_item.get_json_representation()["claims"]["P31"]]
                except KeyError:
                    print("P31 Statements Not Available")
                print(classes)
                for c in classes:
                    wikidata_class = wbi_core.ItemEngine(item_id=c, search_only=True)
                    ontology.append((item[0], wikidata_class.get_label("en"), item[1]))
                    print(ontology)

#Eliminating uncommon parent classes
classes_list1 = [(ii[1], ii[2]) for ii in ontology]
classes_occurrences = {}
for entity in classes_list1:
    try:
        classes_occurrences[entity[0]] += entity[1]
    except KeyError:
        classes_occurrences[entity[0]] = entity[1]
common_classes = collections.Counter(classes_occurrences).most_common(20)

#Visualizing value examples for each common parent classs
print("Common classes with examples:\n")
for item01 in common_classes:
    examples = []
    for sample in ontology:
        if (item01[0] == sample[1]): examples.append(sample[0])
    print(item01, ": ", examples, "\n")

