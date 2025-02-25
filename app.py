from flask import Flask, make_response, request
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, DCTERMS, DCAT, SKOS
import requests

app = Flask(__name__)


MOD = Namespace("https://w3id.org/mod#")

JSONLD_CONTEXT = {
    "dcterms": str(DCTERMS),
    "dcat": str(DCAT),
    "mod": str(MOD),
    "rdfs": str(RDFS),
    "skos": str(SKOS)
}

API_BASE_URL = "https://api.finto.fi/rest/v1/"

@app.route("/artefacts", methods=["GET"])
def artefacts():
    g = Graph()

    vocabularies = requests.get(API_BASE_URL + "vocabularies/", params={ "lang": "en" }).json()
    for voc in vocabularies["vocabularies"]:
        voc_details = requests.get(API_BASE_URL + voc["id"] + "/", params={ "lang": "en" }).json()

        uri = URIRef("http://example.org/" + voc_details["id"])

        g.add((uri, RDF.type, MOD.SemanticArtefact))
        g.add((uri, DCTERMS.title, Literal(voc_details["title"], lang="en")))
        g.add((uri, DCTERMS.identifier, Literal(voc_details["id"], lang="en")))
        g.add((uri, DCTERMS.type, MOD.SemanticArtefact))
        g.add((uri, DCTERMS.accessRights, Literal("public", lang="en")))
        g.add((uri, DCAT.landingPage, URIRef("https://finto.fi/" + voc_details["id"])))

        for lang in voc_details["languages"]:
            g.add((uri, DCTERMS.language, Literal(lang)))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>", methods=["GET"])
def artefact(artefactID):
    g = Graph()

    voc_details = requests.get(API_BASE_URL + artefactID + "/", params={ "lang": "en" }).json()

    uri = URIRef("http://example.org/" + voc_details["id"])

    g.add((uri, RDF.type, MOD.SemanticArtefact))
    g.add((uri, DCTERMS.title, Literal(voc_details["title"], lang="en")))
    g.add((uri, DCTERMS.identifier, Literal(voc_details["id"], lang="en")))
    g.add((uri, DCTERMS.type, MOD.SemanticArtefact))
    g.add((uri, DCTERMS.accessRights, Literal("public", lang="en")))
    g.add((uri, DCAT.landingPage, URIRef("https://finto.fi/" + voc_details["id"])))

    for lang in voc_details["languages"]:
        g.add((uri, DCTERMS.language, Literal(lang)))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/distributions", methods=["GET"])
def artefact_distributions(artefactID):
    return "/artefacts/" + artefactID + "/distributions"


@app.route("/artefacts/<artefactID>/distributions/<distributionID>", methods=["GET"])
def artefact_distribution(artefactID, distributionID):
    return "/artefacts/" + artefactID + "/distributions/"+ distributionID


@app.route("/artefacts/<artefactID>/distributions/latest/resources", methods=["GET"])
def artefact_distribution_latest_resources(artefactID):
    return "/artefacts/" + artefactID + "/distributions/latest/resources"


@app.route("/artefacts/<artefactID>/record", methods=["GET"])
def artefact_record(artefactID):
    return "/artefacts/" + artefactID + "/record"


@app.route("/artefacts/<artefactID>/resources", methods=["GET"])
def artefact_resources(artefactID):
    return "/artefacts/" + artefactID + "/resources"


@app.route("/artefacts/<artefactID>/resources/<resourceID>", methods=["GET"])
def artefact_resource(artefactID, resourceID):
    return "/artefacts/" + artefactID + "/resources/" + resourceID


@app.route("/artefacts/<artefactID>/resources/classes", methods=["GET"])
def artefact_resource_classes(artefactID):
    return "/artefacts/" + artefactID + "/resources/classes"


@app.route("/artefacts/<artefactID>/resources/concepts", methods=["GET"])
def artefact_resource_concepts(artefactID):
    return "/artefacts/" + artefactID + "/resources/concepts"


@app.route("/artefacts/<artefactID>/resources/properties", methods=["GET"])
def artefact_resource_properties(artefactID):
    return "/artefacts/" + artefactID + "/resources/properties"


@app.route("/artefacts/<artefactID>/resources/individuals", methods=["GET"])
def artefact_resource_individuals(artefactID):
    return "/artefacts/" + artefactID + "/resources/individuals"


@app.route("/artefacts/<artefactID>/resources/schemes", methods=["GET"])
def artefact_resource_schemes(artefactID):
    g = Graph()

    voc_details = requests.get(API_BASE_URL + artefactID + "/", params={ "lang": "en" }).json()

    for scheme in voc_details.get("conceptschemes"):
        uri = URIRef(scheme["uri"])
        g.add((uri, RDF.type, URIRef(scheme["type"])))
        if scheme.get("label"):
            g.add((uri, RDFS.label, Literal(scheme["label"], lang="en")))
        if scheme.get("prefLabel"):
            g.add((uri,SKOS.prefLabel, Literal(scheme["prefLabel"], lang="en")))
        if scheme.get("title"):
            g.add((uri, DCTERMS.title, Literal(scheme["title"], lang="en")))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/resources/collection", methods=["GET"])
def artefact_resource_collection(artefactID):
    return "/artefacts/" + artefactID + "/resources/collection"


@app.route("/artefacts/<artefactID>/resources/labels", methods=["GET"])
def artefact_resource_labels(artefactID):
    return "/artefacts/" + artefactID + "/resources/labels"


@app.route("/", methods=["GET"])
def catalogue():
    return "/"


@app.route("/records", methods=["GET"])
def records():
    return "/records"


@app.route("/records/<artefactID>", methods=["GET"])
def record(artefactID):
    return "/records/" + artefactID


@app.route("/search", methods=["GET"])
def search():
    return "/search"


@app.route("/search/content", methods=["GET"])
def search_content():
    g = Graph()
    q = request.args.get("q")

    search_results = requests.get(API_BASE_URL + "/search/", params={ "query": q, "lang": "en", "unique": True }).json()["results"]
    for res in search_results:
        uri = URIRef(res["uri"])

        g.add((uri, SKOS.prefLabel, Literal(res["prefLabel"], lang="en")))
        for res_type in res.get("type"):
            g.add((uri, RDF.type, URIRef(res_type)))
        if res.get("altLabel"):
            g.add((uri, SKOS.altLabel, Literal(res["altLabel"], lang="en")))
        if res.get("hiddenLabel"):
            g.add((uri, SKOS.hiddenLabel, Literal(res["hiddenLabel"], lang="en")))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/search/metadata", methods=["GET"])
def search_metadata():
    return "/search/metadata"


@app.route("/doc/api", methods=["GET"])
def doc_api():
    return "/doc/api"
