from flask import Flask, make_response
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, DCTERMS, DCAT

app = Flask(__name__)


MOD = Namespace('https://w3id.org/mod#')

JSONLD_CONTEXT = {
    "dcterms": str(DCTERMS),
    "dcat": str(DCAT)
}

API_BASE_URL = 'https://api.finto.fi/rest/v1/'

@app.route("/artefacts", methods=['GET'])
def artefacts():
    g = Graph()

    g.add((URIRef('http://example.org/ex1'), RDF.type, MOD.SemanticArtefact))
    g.add((URIRef('http://example.org/ex1'), DCTERMS.title, Literal("Lorem Ipsum", lang='en')))
    g.add((URIRef('http://example.org/ex1'), DCTERMS.identifier, Literal("https://example.org/identifier/identifierID", lang='en')))
    g.add((URIRef('http://example.org/ex1'), DCTERMS.language, Literal("en", lang='en')))
    g.add((URIRef('http://example.org/ex1'), DCTERMS.type, Literal("Lorem Ipsum", lang='en')))
    g.add((URIRef('http://example.org/ex1'), DCTERMS.accessRights, Literal("public", lang='en')))
    g.add((URIRef('http://example.org/ex1'), DCAT.landingPage, Literal("Lorem Ipsum", lang='en')))

    response = make_response(g.serialize(format='json-ld', context=JSONLD_CONTEXT))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route("/artefacts/<artefactID>", methods=['GET'])
def artefact(artefactID):
    return "/artefacts/" + artefactID


@app.route("/artefacts/<artefactID>/distributions", methods=['GET'])
def artefact_distributions(artefactID):
    return "/artefacts/" + artefactID + "/distributions"


@app.route("/artefacts/<artefactID>/distributions/<distributionID>", methods=['GET'])
def artefact_distribution(artefactID, distributionID):
    return "/artefacts/" + artefactID + "/distributions/"+ distributionID


@app.route("/artefacts/<artefactID>/distributions/latest/resources", methods=['GET'])
def artefact_distribution_latest_resources(artefactID):
    return "/artefacts/" + artefactID + "/distributions/latest/resources"


@app.route("/artefacts/<artefactID>/record", methods=['GET'])
def artefact_record(artefactID):
    return "/artefacts/" + artefactID + "/record"


@app.route("/artefacts/<artefactID>/resources", methods=['GET'])
def artefact_resources(artefactID):
    return "/artefacts/" + artefactID + "/resources"


@app.route("/artefacts/<artefactID>/resources/<resourceID>", methods=['GET'])
def artefact_resource(artefactID, resourceID):
    return "/artefacts/" + artefactID + "/resources/" + resourceID


@app.route("/artefacts/<artefactID>/resources/classes", methods=['GET'])
def artefact_resource_classes(artefactID):
    return "/artefacts/" + artefactID + "/resources/classes"


@app.route("/artefacts/<artefactID>/resources/concepts", methods=['GET'])
def artefact_resource_concepts(artefactID):
    return "/artefacts/" + artefactID + "/resources/concepts"


@app.route("/artefacts/<artefactID>/resources/properties", methods=['GET'])
def artefact_resource_properties(artefactID):
    return "/artefacts/" + artefactID + "/resources/properties"


@app.route("/artefacts/<artefactID>/resources/individuals", methods=['GET'])
def artefact_resource_individuals(artefactID):
    return "/artefacts/" + artefactID + "/resources/individuals"


@app.route("/artefacts/<artefactID>/resources/schemes", methods=['GET'])
def artefact_resource_schemes(artefactID):
    return "/artefacts/" + artefactID + "/resources/schemes"


@app.route("/artefacts/<artefactID>/resources/collection", methods=['GET'])
def artefact_resource_collection(artefactID):
    return "/artefacts/" + artefactID + "/resources/collection"


@app.route("/artefacts/<artefactID>/resources/labels", methods=['GET'])
def artefact_resource_labels(artefactID):
    return "/artefacts/" + artefactID + "/resources/labels"


@app.route("/", methods=['GET'])
def catalogue():
    return "/"


@app.route("/records", methods=['GET'])
def records():
    return "/records"


@app.route("/records/<artefactID>", methods=['GET'])
def record(artefactID):
    return "/records/" + artefactID


@app.route("/search", methods=['GET'])
def search():
    return "/search"


@app.route("/search/content", methods=['GET'])
def search_content():
    return "/search/content"


@app.route("/search/metadata", methods=['GET'])
def search_metadata():
    return "/search/metadata"


@app.route("/doc/api", methods=['GET'])
def doc_api():
    return "/doc/api"
