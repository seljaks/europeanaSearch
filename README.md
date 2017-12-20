# europeanaSearch
This is a brief overview of the europeana search and record APIs.
It also containts some of my observations as to how they function and possible ideas for relavance metrics.
Futhermore there's some simple python 3 code for using the search API and examining it's results.

General Europeana Api documentation 
https://pro.europeana.eu/resources/apis

Documentation on the Europeana search API
https://pro.europeana.eu/resources/apis/search

Documentation on the Europeana record API
https://pro.europeana.eu/resources/apis/record

## Motivation
The main motivation for this document is the lack of a relevant sorting option within the Europeana search API. The results are almost always displayed arbitrarily or are very rarely ordered with a not-so-relevant score function as seen below.
The ultimate goal would be to create an accurate metric function that takes an object's metadata as input and returns a number or several numbers that express the objects relevancy as it relates to the search query.

## Europeana search API example:
https://www.europeana.eu/api/v2/search.json?wskey=yourApiKey&query=%22Mona%20Lisa%22&qf=TYPE:IMAGE&rows=100&profile=rich

The above is a search for `"Mona Lisa"` that returns up to a hundred results (or in this case exactly a hundred) as a json object. 
While the metadata varies for each result there are some entries that are always present e.g.: `title`, `id`, `guid`(links to the europeana website where the object is located) and `link`(links to a json containing the object's record metadata), etc.
The query refinement is `TYPE:IMAGE` (case sensistive). Europeana's five major types are IMAGE, SOUND, VIDEO, TEXT and 3D although there are many more types of groupings possible. Check "facets" in the search API documentation.
Entering `profile=rich` makes the API return the maximum ammount of metadata for each result. However this is still less metadata than checking the object's record metadata itself.
You may get results that do not contain your query which implies that the search API actually searches the record of each result for the desired query. In this concrete example there are two results that do not contain "Mona Lisa" but their records do.

## Europeana record API example:
http://www.europeana.eu/api/v2/record/03919/public_mistral_joconde_fr_ACTION_CHERCHER_FIELD_1_REF_VALUE_1_000PE025604.json?wskey=yourApiKey

This is the record for the actual painting Mona Lisa that resides in Louvre. To prefered way to access a record is through the search API `link` entry, otherwise you need to specify the record ID in advance.
The metadata is arranged using the Europeana Data Model or EDM. For a quick intro to EDM see <https://pro.europeana.eu/resources/apis/intro#edm>. For more detailed documentation can be found at https://pro.europeana.eu/page/edm-documentation. I recommend checking the EDM powerpoint presentation for a relatively concise summary.
Surprisingly the above example does not contain any mention of "Paris" however it does contain "France".

### A note on score

The search API sometimes returns a `score` for each result. According to the documentation "score" is "The relevancy score calculated by the search engine. Depends of the query." 
The "Mona Lisa" example above has score and the results are ordered from highest to lowest. Score is usually a float between 0 and 5 with 6 to 10 decimal points. There are several issues with score, chief among them being that I didn't manage to find any other query besides "Mona Lisa" that would return score with the results. 
Another is that the relevancy is hardly accurate. In the "Mona Lisa" example the number one result with cca 4.2 score is a picture of a soap wrapper with Mona Lisa on it. The number two result with 3.6 is a photograph of an estonian TV drama called Mona Lisa.
Number five is a photo of an actress tha starred in an Austrian film titled "Der Raub der Mona Lisa" and so on.
The actual Lourve painting by Leonardo da Vinci has a score of about 2.1 and is between 29th and 32nd place, with several much less relevant results having higher scores. The silver lining is that in a general sense being 30th out of a 100 is not *that* bad.
A third problem is that `score` depends on the `profile` parameter and will return slightly different results whether we choose `rich`, `minimal` or `standard` (the latter being the default setting for the search API).

### Some ideas for metrics

Besides the usual heuristics of counting the number of hits our query gets in the object's metadata or checking whether an arbitrary list of entries contain the desired search query one could also look at the metadata quality itself.
Possible assumptions could be that a more relavant object has more metadata than less relevant objects or that it has more providers of metadata. This leads to heuristics such as counting the number of entries the record object has or focusing on how much metadata was provided by a certain provider and comparing the results of each object.
These results could be futher improved by making some use of the score value wherever available.
An interesting article on this topic, written by a Europeana employee, can be found here: https://dh2017.adho.org/abstracts/458/458.pdf

#### Note on using the python scripts

Create a europeanaApiKey.txt and copy your API key into it.


