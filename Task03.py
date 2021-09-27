import requests

#Open the list of the verified publications
f1 = open("verified_ref.txt", "r", encoding="utf8")

#Reading the full records
with open('verified_ref.txt', 'r', encoding="utf8") as file:
    text = file.read()

evidences = []
for line in f1:
    #Getting the metadata of verified evidences from OpenCitations COCI
    doi = line[:-1]
    idurl = "https://opencitations.net/index/coci/api/v1/metadata/"+doi
    idget = requests.get(idurl)
    #Getting the references and citations of verified evidences
    idjson = idget.json()
    references = idjson[0]["reference"]
    citations = idjson[0]["citation"]
    list01 = references + "; " + citations
    list_links = list01.split("; ")
    list_links = [w for w in list_links if w != ""]
    #Getting the references and citations of identified publications through snowballing
    for evidence in list_links:
        idurl1 = "https://opencitations.net/index/coci/api/v1/metadata/"+evidence
        idget1 = requests.get(idurl1)
        #Getting the references and citations of verified evidences
        idjson1 = idget1.json()
        references1 = idjson1[0]["reference"]
        citations1 = idjson1[0]["citation"]
        list02 = references1 + "; " + citations1
        list_links1 = list02.split("; ")
        list_links1 = [w for w in list_links1 if w != ""]
        #Verifying if the unidentified scholarly publications are related to two scholarly publications through a citation link
        i = 0
        link = 0
        while (i < len(list_links1)) and (link < 2):
            if (text.find(list_links1[i])>=0): link +=1
            i += 1
        if (link == 2): evidences.append(evidence)

#Eliminating duplicates
evidences = list(dict.fromkeys(evidences))

#Creating the list of scholarly evidences
f2 = open("snowb_ref.txt", "w", encoding="utf8")
for evidence in evidences:
    f2.write(evidence)
    f2.flush()
f2.close()
