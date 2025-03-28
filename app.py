from flask import Flask, make_response, request
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, DCTERMS, DCAT, SKOS
import requests

app = Flask(__name__)


MOD = Namespace("https://w3id.org/mod#")
SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")

JSONLD_CONTEXT = {
    "dcterms": str(DCTERMS),
    "dcat": str(DCAT),
    "mod": str(MOD),
    "rdfs": str(RDFS),
    "skos": str(SKOS),
    "skosxl": str(SKOSXL)
}

FORMATS = [
    { "format": "text/turtle", "uri": "http://www.w3.org/ns/formats/Turtle" },
    { "format": "application/rdf+xml", "uri": "https://www.w3.org/ns/formats/data/RDF_XML" },
    { "format": "application/marcxml+xml", "uri": "https://www.loc.gov/standards/marcxml/" },
    { "format": "application/json+ld", "uri": "http://www.w3.org/ns/formats/JSON-LD" }
]

API_BASE_URL = "https://api.finto.fi/rest/v1/"


@app.route("/artefacts", methods=["GET"])
def artefacts():
    pagesize = int(request.args.get("pagesize", 50))
    page = int(request.args.get("page", 1))

    g = Graph()

    ret = requests.get(API_BASE_URL + "vocabularies/", params={ "lang": "en" }).json()

    start_index = (page - 1) * pagesize
    end_index = start_index + pagesize
    vocabularies = sorted(ret["vocabularies"], key=lambda d: d["id"])[start_index:end_index]
    for voc in vocabularies:
        voc_details = requests.get(API_BASE_URL + voc["id"] + "/", params={ "lang": "en" }).json()

        uri = URIRef(request.url_root + "artefacts/" + voc_details["id"])

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

    ret = requests.get(API_BASE_URL + artefactID + "/", params={ "lang": "en" })
    if ret.status_code == 404:
        return "Artefact not found", 404

    voc_details = ret.json()

    uri = URIRef(request.url_root + "artefacts/" + voc_details["id"])

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
    g = Graph()

    for i, f in enumerate(FORMATS):
        data = requests.head(API_BASE_URL + artefactID + "/data", params={"format": f["format"]})
        if data.status_code == 404:
            return "Artefact not found", 404

        if data.status_code == 302:
            uri = URIRef(request.url_root + "artefacts/" + artefactID + "/distributions/" + str(i + 1))

            g.add((uri, RDF.type, MOD.semanticArtefactDistribution))
            g.add((uri, DCAT.downloadURL, URIRef(data.headers["location"])))
            g.add((uri, DCAT.accessURL, URIRef("https://finto.fi/" + artefactID)))
            g.add((uri, DCTERMS.accessRights, Literal("public", lang="en")))
            g.add((uri, MOD.hasSyntax, URIRef(f["uri"])))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/distributions/<distributionID>", methods=["GET"])
def artefact_distribution(artefactID, distributionID):
    g = Graph()

    if (not distributionID.isdigit() or int(distributionID) < 1 or int(distributionID) > len(FORMATS)):
        return "Distribution not found", 404

    f = FORMATS[int(distributionID) - 1]
    data = requests.head(API_BASE_URL + artefactID + "/data", params={"format": f["format"]})
    if data.status_code == 404:
        return "Artefact not found", 404
    
    if data.status_code == 302:
        uri = URIRef(request.url_root + "artefacts/" + artefactID + "/distributions/" + distributionID)

        g.add((uri, RDF.type, MOD.semanticArtefactDistribution))
        g.add((uri, DCAT.downloadURL, URIRef(data.headers["location"])))
        g.add((uri, DCAT.accessURL, URIRef("https://finto.fi/" + artefactID)))
        g.add((uri, DCTERMS.accessRights, Literal("public", lang="en")))
        g.add((uri, MOD.hasSyntax, URIRef(f["uri"])))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/distributions/latest", methods=["GET"])
def artefact_distribution_latest(artefactID):
    return "/artefacts/" + artefactID + "/distributions/latest"


@app.route("/artefacts/<artefactID>/record", methods=["GET"])
def artefact_record(artefactID):
    return "/artefacts/" + artefactID + "/record"


@app.route("/artefacts/<artefactID>/resources", methods=["GET"])
def artefact_resources(artefactID):
    ret = requests.get(API_BASE_URL + artefactID + "/data", params={"lang": "en", "format": "text/turtle"})
    if ret.status_code == 404:
        return "Artefact not found", 404

    data = ret.text

    g = Graph()
    g.parse(data=data)

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/resources/<path:resourceID>", methods=["GET"])
def artefact_resource(artefactID, resourceID):
    ret = requests.get(API_BASE_URL + artefactID + "/data", params={"uri": resourceID, "lang": "en", "format": "application/ld+json"})
    if ret.status_code == 404:
        return "Artefact or resource not found", 404

    data = ret.json()

    response = make_response(data)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/resources/classes", methods=["GET"])
def artefact_resource_classes(artefactID):
    pagesize = int(request.args.get("pagesize", 50))
    page = int(request.args.get("page", 1))

    g = Graph()

    ret = requests.get(API_BASE_URL + artefactID + "/types", params={ "lang": "en" })
    if ret.status_code == 404:
        return "Artefact not found", 404

    data = ret.json()

    start_index = (page - 1) * pagesize
    end_index = start_index + pagesize
    types = sorted(data.get("types", []), key=lambda d: d["uri"])[start_index:end_index]
    for voc_type in types:
        uri = URIRef(voc_type["uri"])
        if voc_type.get("label"):
            g.add((uri, RDFS.label, Literal(voc_type["label"], lang="en")))
        if voc_type.get("superclass"):
            g.add((uri, RDFS.subClassOf, URIRef(voc_type["superclass"])))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/resources/concepts", methods=["GET"])
def artefact_resource_concepts(artefactID):
    pagesize = request.args.get("pagesize", 50)
    page = request.args.get("page", 1)

    ret = requests.get(API_BASE_URL + artefactID + "/data", params={"lang": "en", "format": "text/turtle"})
    if ret.status_code == 404:
        return "Artefact not found", 404

    data = ret.text

    query = """
        PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
        DESCRIBE ?s
        WHERE {
            ?s a skos:Concept .
        }
        ORDER BY (str(?s))
        LIMIT %s
        OFFSET %s
    """ % (pagesize, (int(page) - 1) * int(pagesize))
    
    g=Graph()
    g.parse(data=data)

    result_graph = Graph()
    result_graph += g.query(query)

    response = make_response(result_graph.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/resources/properties", methods=["GET"])
def artefact_resource_properties(artefactID):
    pagesize = request.args.get("pagesize", 50)
    page = request.args.get("page", 1)

    ret = requests.get(API_BASE_URL + artefactID + "/data", params={"lang": "en", "format": "text/turtle"})
    if ret.status_code == 404:
        return "Artefact not found", 404

    data = ret.text

    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        DESCRIBE ?p
        WHERE {
            ?p a rdf:Property .
        }
        ORDER BY (str(?p))
        LIMIT %s
        OFFSET %s
    """ % (pagesize, (int(page) - 1) * int(pagesize))
    
    g=Graph()
    g.parse(data=data)

    result_graph = Graph()
    result_graph += g.query(query)

    response = make_response(result_graph.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/resources/individuals", methods=["GET"])
def artefact_resource_individuals(artefactID):
    return "/artefacts/" + artefactID + "/resources/individuals"


@app.route("/artefacts/<artefactID>/resources/schemes", methods=["GET"])
def artefact_resource_schemes(artefactID):
    pagesize = int(request.args.get("pagesize", 50))
    page = int(request.args.get("page", 1))

    g = Graph()

    ret = requests.get(API_BASE_URL + artefactID + "/", params={ "lang": "en" })
    if ret.status_code == 404:
        return "Artefact not found", 404

    data = ret.json()

    start_index = (page - 1) * pagesize
    end_index = start_index + pagesize
    schemes = sorted(data.get("conceptschemes", []), key=lambda d: d["uri"])[start_index:end_index]
    for scheme in schemes:
        uri = URIRef(scheme["uri"])
        g.add((uri, RDF.type, URIRef(scheme["type"])))
        if scheme.get("label"):
            g.add((uri, RDFS.label, Literal(scheme["label"], lang="en")))
        if scheme.get("prefLabel"):
            g.add((uri, SKOS.prefLabel, Literal(scheme["prefLabel"], lang="en")))
        if scheme.get("title"):
            g.add((uri, DCTERMS.title, Literal(scheme["title"], lang="en")))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/resources/collection", methods=["GET"])
def artefact_resource_collection(artefactID):
    pagesize = int(request.args.get("pagesize", 50))
    page = int(request.args.get("page", 1))

    g = Graph()

    ret = requests.get(API_BASE_URL + artefactID + "/groups", params={ "lang": "en" })
    if ret.status_code == 404:
        return "Artefact not found", 404

    data = ret.json()

    start_index = (page - 1) * pagesize
    end_index = start_index + pagesize
    groups = sorted(data.get("groups", []), key=lambda d: d["uri"])[start_index:end_index]
    for group in groups:
        uri = URIRef(group["uri"])
        
        g.add((uri, RDF.type, SKOS.Collection))
        g.add((uri, SKOS.prefLabel, Literal(group["prefLabel"], lang="en")))

        for child in group.get("childGroups", []):
            g.add((uri, SKOS.member, URIRef(child)))

    response = make_response(g.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/artefacts/<artefactID>/resources/labels", methods=["GET"])
def artefact_resource_labels(artefactID):
    pagesize = request.args.get("pagesize", 50)
    page = request.args.get("page", 1)

    ret = requests.get(API_BASE_URL + artefactID + "/data", params={"lang": "en", "format": "text/turtle"})
    if ret.status_code == 404:
        return "Artefact not found", 404

    data = ret.text

    query = """
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
        DESCRIBE ?s
        WHERE {
            ?s a skosxl:Label .
        }
        ORDER BY (str(?s))
        LIMIT %s
        OFFSET %s
    """ % (pagesize, (int(page) - 1) * int(pagesize))
    
    g=Graph()
    g.parse(data=data)

    result_graph = Graph()
    result_graph += g.query(query)

    response = make_response(result_graph.serialize(format="json-ld", context=JSONLD_CONTEXT))
    response.headers["Content-Type"] = "application/json"
    return response


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
