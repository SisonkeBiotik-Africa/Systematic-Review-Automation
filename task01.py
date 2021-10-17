import requests
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

#Defining the SPARQL endpoint of Wikidata
endpoint_url = "https://query.wikidata.org/sparql"

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

#Getting the main keywords
n = input("How many main keywords are there")
t = []
for i in range(int(n)):
  ms = "Provide the Keyword " + str(i+1)
  ss = input(ms)
  t.append(ss)
  
squery = []
#Aligning term to Wikidata
for term in t:
  augm = []
  tt = term.replace(" ", "_")
  idurl = "https://hub.toolforge.org/enwiki:" + tt + "?site=wikidata&format=json"
  idget = requests.get(idurl)
  idjson = idget.json()
  #Augmenting the search query
  if 'destination' in idjson and 'preferedSitelink' in idjson['destination']:
    cit_wikidata_id = idjson["destination"]["preferedSitelink"]["title"]
  else:
    cit_wikidata_id = ""
  if (cit_wikidata_id != ""):
    query = """SELECT * WHERE {
    {?x wdt:P31* wd:""" + cit_wikidata_id +"""} UNION {?x wdt:P279* wd:""" + cit_wikidata_id + """} UNION {?x wdt:P361* wd:""" + cit_wikidata_id + """} UNION {wd:""" + cit_wikidata_id + """ wdt:P1552 ?x}.
    {?x rdfs:label ?label} UNION {?x skos:altLabel ?label}.
    FILTER(LANG(?label)="en")
    }
    LIMIT 50"""
    results = get_results(endpoint_url, query)
    for result in results["results"]["bindings"]:
      augm.append(result["label"]["value"])
  augm.append(term)
  linker = ") OR ("
  squery.append("("+linker.join(augm)+")")

linker_and = ") AND ("  
final_query = "("+linker.join(squery)+")"
print(final_query)
  
