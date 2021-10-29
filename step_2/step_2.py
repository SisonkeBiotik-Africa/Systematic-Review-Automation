#Open Clarivate Analytics Web of Science Plain Text
f = open("savedrecs.txt", "r", encoding="utf8")

#Create a file for the verified publications
f1 = open("verified_ref.txt", "w", encoding="utf8")

#Reading the full records
with open('savedrecs.txt', 'r', encoding="utf8") as file:
    text = file.read()
condition_ref = False
ref = []
c = False
c1 = False
for line in f:
    #Getting the list of references of the research work
    if (line.find("CR")==0):
        condition_ref = True
    if (line.find("   ")!=0) and (line.find("CR")!=0):
        condition_ref = False
    if (condition_ref == True):
        if (line.find("DOI ")>=0): ref.append(line[line.find("DOI")+4:-1])
    #Adding the work to the list of verified publications if applicable
    if (line.find("DI")==0):
        DOI = line[3:-1]
        n = text.count(DOI)
        if (n > 1):
            f1.write(line[3:])
            f1.flush()
        if (ref != []):
            c = False
            c1 = False
            iteration = 0
            while (c == False):
                if (text.count(ref[iteration])>1):
                    c = True
                    c1 = True
                    ref = []
                else:
                    iteration += 1
                if (iteration == len(ref)):
                    c = True
                    ref = []
        if (c1 == True):
            f1.write(line[3:])
            f1.flush()
f1.close()
            
        
