from SPARQLWrapper import JSON, SPARQLWrapper

import tags

identifiers = [
    'date of birth',
    'born',
    'birth date'
]

def match(word_tag):
    first_word = word_tag[0]
    sentence = ' '.join([word[tags.WORD_INDEX] for word in word_tag])
    if first_word[tags.TAG_INDEX] == tags.WH_PRONOUN or first_word[tags.TAG_INDEX] == tags.WH_ADVERB:
        for identifier in identifiers:
            if identifier in sentence:
                return birthName(word_tag)

def birthName(words):
    words = [word for word in words
             if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
             word[tags.WORD_INDEX] not in identifiers and \
             word[tags.WORD_INDEX] != 'date' and \
             word[tags.WORD_INDEX] != 'born' and \
             word[tags.WORD_INDEX] != 'birth'  ]
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return sparql(words)
    return None

def sparql(artist):

    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery( """ 
         PREFIX dbo: <http://dbpedia.org/ontology/>
         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

         SELECT (CONCAT(STR(DAY(?date)), 
                     "/", 
                     STR(MONTH(?date)), 
                     "/", 
                    STR(YEAR(?date))) as ?birth_date)
         WHERE  { 
           ?person rdf:type dbo:MusicalArtist ;
                   rdfs:label ?label ;
                   dbo:birthDate ?date
           FILTER regex(?label, "^%s", "i")
         }
         LIMIT 1
         """ % ' '.join(artist)
    )

    results = wrapper.query().convert()['results']['bindings']
    if len(results) > 0:
       return "The birth date is " + results[0]["birth_date"]["value"]
    return None
