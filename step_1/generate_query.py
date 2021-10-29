import sys
from datetime import datetime
import os

import requests
from omegaconf import DictConfig, OmegaConf
from SPARQLWrapper import JSON, SPARQLWrapper

CONFIG_FILE_PATH = "./configs/config.yaml"


def get_keywords(config: DictConfig, example = False) -> list: 
  """Get main keywords  

  Args:
      config (DictConfig): Configuration file for script.
      example (bool, optional): A flag if user would like to use some example keywords for query. Defaults to False. # TODO add argparse for example flag in cli 

  Returns:
      list: of keywords to be included in query 
  """
  
  keywords = []

  # check if keywords exist in config file 
  if not config.keywords[0] == "???": 
    for keyword in config.keywords:
      keywords.append(keyword)
  
  # get example keywords to generate an example query 
  if example == True:
    for keyword in config.keywords_examples:
      keywords.append(keyword)

  # ask user for input if no input file 
  if config.keywords[0] == "???" and example == False: 
    num_keywords = input("How many main keywords are there? ")
    for i in range(int(num_keywords)):
      keyword = input(f"Provide the Keyword {(i+1)}: ")
      keywords.append(keyword)

  return keywords


def build_query(keywords: list, endpoint_url: str) -> str:  
  squery = []
  # Aligning term to Wikidata
  for term in keywords:
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
      LIMIT 15"""
      results = _get_results(endpoint_url, query)
      for result in results["results"]["bindings"]:
        augm.append(result["label"]["v Get config alue"])
    augm.append(term)
    linker = ") OR ("
    squery.append("("+linker.join(augm)+")")

  linker_and = ") AND ("  # TODO investigate if this is used 
  final_query = "("+linker.join(squery)+")"
  return(final_query)


def _get_results(endpoint_url: str, query: str) -> str:
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def main():
  # Get config 
  with open(CONFIG_FILE_PATH, "r") as file:
    config = OmegaConf.load(file)

  # Defining the SPARQL endpoint of Wikidata
  endpoint_url = config.endpoint_url

  # Get keywords 
  keywords = get_keywords(config)

  # Build query 
  query = build_query(keywords, endpoint_url)

  # Save query
  now = datetime.now()
  current_time = now.strftime("%Y-%m-%d %H:%M:%S")
  os.makedirs("./outputs/queries", exist_ok=True)
  save_path = f"./outputs/queries/query-{current_time}.txt"
  with open(save_path, "w+") as file:
    file.write(query)

  # Display query to user 
  print(query)
  print(f"\nquery saved as {save_path}")


if __name__ == "__main__":
  main()
