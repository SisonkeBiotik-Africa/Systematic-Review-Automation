# Systematic-Review-Automation
A set of Python tools for the automation of the main tasks for the creation and refinement of bibliometric studies and systematic reviews

## QuickStart 
- TODO Chris 

## Contributing
- TODO Chris 

## Introduction
Within the framework of Sisonkebiotik Community, it will be interesting to conduct research works to identify the state-of-the-art of biomedical artificial intelligence in Africa and abroad. This will enable the recognition of research and development capacities in Africa that can contribute to the enhancement of Biomedical Machine Learning in Africa and consequently the development of continent-level research collaborations about this interesting topic. Such scholarly publications include bibliometric studies that quantitatively and qualitatively assess the research productivity of individuals, groups and countries based on the large-scale analysis of bibliographic metadata using statistics and association analysis. They also involve systematic reviews and meta-analyses that retrieve the findings and settings of research papers about a given research topic using natural language processing techniques and human curation and represent them in structured summary tables and visualizations. The development of such an output requires a lot of work. Effectively, authors need to formulate the most efficient query that allows them to get all the scholarly publications on the assessed topic. Then, the authors have to eliminate the odd records that are not related to the area from the initially returned search results. After that, the authors need to define the characteristics that should be retrieved from scholarly publications to allow the creation of a systematic review or a bibliometric study. In this project, we will try to automate these three tasks for a quicker development of literature reviews and scientometric analyses. We restrict our work to the research outputs indexed by Clarivate's [Web of Science Core Collection](https://webofknowledge.com).

## Source codes
* **Task01**: This code augments the search query by adding the synonyms of the mainly used keywords as well as its aspects, subclasses and parts so that further relevant evidences can be identified. For this, the main keywords related to the assessed topic are linked to their corresponding Wikidata item using [Wikidata Hub Service](https://hub.toolforge.org). Subsequently, the [aspects](https://www.wikidata.org/wiki/Property:P1552), [subclasses](https://www.wikidata.org/wiki/Property:P279) and [parts](https://www.wikidata.org/wiki/Property:P361) of the keywords are extracted from Wikidata using a specific SPARQL query and SPARQLWrapper as a Python Library.
* **Task02**: This code performs a citation analysis on the initally identified records retrieved from Web of Science as a plain text. It considers the papers having a [Digital Object Identifier](https://www.doi.org/) that have been citing or cited by another identified publication or co-citing the same research publication as valid for inclusion in the developed systematic review. End users can use this list to return the list of unverified research publications that need to be validated by hand.
* **Task03**: This code proposes a list of unidentified scholarly publications that can be related to the topic of the systematic review through the backward and forward snowballing of the verified research evidences. This list is created through the analysis of the references and citations of verified research evidences based on [OpenCitations COCI Corpus API](https://opencitations.net/index/coci/api/v1#/metadata/{dois}). A new scholarly publication is added where two verified evidences are included in its references' or citations' list. After the list of scholarly evidences is finally created, it should be manually parsed to verify if its members are eligible for inclusion in the systematic review.
* **Task04**: This code tries to map the features of the assessed topic that should be considered to represent the findings of scholarly publications in the context of systematic reviews. It analyzes the abstracts of scholarly publications and retrieves all identified noun phrases in it using [SpaCy](https://spacy.io/) and [en core web sm](https://libraries.io/pypi/en-core-web-sm). Then, it cleans the extracted noun phrases by eliminating uncommon named entities using [Collections](https://docs.python.org/3/library/collections.html), making them in the singular form using [Pattern](https://github.com/clips/pattern) and by removing stop words using [NLTK](https://www.nltk.org/). Finally, we assign the significant named entities to their parent classes based on Wikidata statements using [Wikibase Integrator](https://github.com/LeMyst/WikibaseIntegrator). 
* **Savedrecs**: Sample Plain Text File from Web of Science Core Collection for testing Python codes.
# Requirements
* en-core-web-sm     3.1.0
* nltk               3.3
* Pattern            3.6
* requests           2.26.0
* spacy              3.1.3
* SPARQLWrapper      1.8.5
* wikibaseintegrator 0.11.0
## References
* Turki, H., Hadj Taieb, M. A., Ben Aouicha, M., Fraumann, G., Hauschke, C., & Heller, L. (2021). Enhancing Knowledge Graph Extraction and Validation From Scholarly Publications Using Bibliographic Metadata. *Frontiers in research metrics and analytics*, 6, 694307.
* Turki, H. (2018). Citation analysis is also useful to assess the eligibility of biomedical research works for inclusion in living systematic reviews. *Journal of clinical epidemiology*, 97, 124-125.
* Turki, H., Hadj Taieb, M. A., & Ben Aouicha, M. (2018). MeSH qualifiers, publication types and relation occurrence frequency are also useful for a better sentence-level extraction of biomedical relations. *Journal of biomedical informatics*, 83, 217-218.
* Turki, H., Shafee, T., Hadj Taieb, M. A., Ben Aouicha, M., Vrandečić, D., Das, D., & Hamdi, H. (2019). Wikidata: A large-scale collaborative ontological medical database. *Journal of biomedical informatics*, 99, 103292.
* Turki, H., Hadj Taieb, M. A., Shafee, T., Lubiana, T., Jemielniak, D., Ben Aouicha, M., Labra Gayo, J. E., Youngstrom, E. A., Banat, M., Das, D., & Mietchen, D. (2022). Representing COVID-19 information in collaborative knowledge graphs: the case of Wikidata. *Semantic Web Journal*, 13(2).
