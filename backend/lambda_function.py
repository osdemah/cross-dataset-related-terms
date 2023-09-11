from rdflib import Graph, Namespace
from rdflib.plugins.stores import sparqlstore
import json
import base64


class Store:
    def __init__(self):
        neptune_endpoint = "https://database-1.cluster-cclypxvaeodz.us-west-2.neptune.amazonaws.com:8182/sparql"
        store = sparqlstore.SPARQLStore(neptune_endpoint, method='POST')
        g = Graph(store)

        g.bind("terms", Namespace("http://related-terms.io/terms/"))
        g.bind("rdfs", Namespace("http://www.w3.org/2000/01/rdf-schema#"))
        g.bind("termsv", Namespace("http://related-terms.io/vocab#"))
        g.bind("hint", Namespace("http://aws.amazon.com/neptune/vocab/v01/QueryHints#"))
        self.g = g

    def query(self, q):
        return self.g.query(q)


store = Store()


def lambda_handler(event, context):
    print(event)
    body = event["body"]
    if event['isBase64Encoded']:
        body = base64.b64decode(body)
    term = json.loads(body)["term"]
    query = '''
    SELECT ?label ?weight
    {
        hint:Query hint:joinOrder "Ordered" .
        {
            SELECT ?label ?relation 
            {
                hint:SubQuery hint:evaluationStrategy \"BottomUp" .
                ?term rdfs:label "QUERY_TERM" .
                ?related termsv:relatedTo ?term .
                ?related rdfs:label ?label .
                BIND(REPLACE(STR(?term), "http://related-terms.io/terms/", "") AS ?rterm) .
                BIND(REPLACE(STR(?related), "http://related-terms.io/terms/", "") AS ?rrelated) .
                BIND(IRI(CONCAT("http://related-terms.io/relations/", ?rterm, "-", ?rrelated)) as ?relation) .
            }
        }
        ?relation termsv:weight ?weight
    } ORDER BY DESC(?weight) LIMIT 10
    '''.replace("QUERY_TERM", term)
    result = [{"relatedTerm": row.label, "weight": row.weight} for row in store.query(query)]
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
