# Implementation notes

## Overview

This document summarizes the current implementation status of the API endpoints. It discusses missing features, known problems, and suggestions for improvements.

## Common issues across endpoints

- The API is implemented as a wrapper over the existing SKOSMOS API. The SKOSMOS API does not expose much metadata and as a result many endpoints have sparse implementations
- The data returned in the implemented endpoints with pagination is semantically equivalent to the MOD API specification but returned JSON-LD data does not have the same structure as the specification. Notably, the list of `hydra:members` includes only the URIs of the members and member objects are included separately in the graph. It is unclear if the structure of the JSON document is significant in the API specification or if it is sufficient to conform to the data model.
- Many endpoints require utilizing complete vocabulary datasets as the SKOSMOS API does not expose all necessary data. Parsing and querying the datasets is very slow with rdflib.
- JSON-LD context object often includes prefixes that are not actually used in the graph and it does not include all prefixes listed in the specification
- `Format` parameter is implemented for all endpoints but nothing is returned for the value `html`
- `Accept` header is not used to determine the format of the returned document
- `Display` parameter is not implemented for any endpoint because it is not defined for non-artefact endpoints and it's not clear what the default value should be in these cases

### /artefacts

- **Implementation status**: Implemented with missing mandatory fields
- **Issues**:
  - Only a few of the mandatory fields are returned as SKOSMOS API includes limited metadata about vocabularies
  - Landing pages are hardcoded to be in the finto.fi domain

### /artefacts/{artefactID}

- **Implementation status**: Implemented with missing mandatory fields
- **Issues**:
  - Only a few of the mandatory fields are returned as SKOSMOS API includes limited metadata about vocabularies
  - Landing pages are hardcoded to be in the finto.fi domain

### /artefacts/{artefactID}/distributions

- **Implementation status**: Implemented with missing mandatory fields
- **Issues**:
  - Only a few of the mandatory fields are returned as SKOSMOS API includes limited metadata about distributions
  - Different serializations of vocab data are returned as distributions (i.e. turtle, rdfxml, etc.) and no versioning exists for distributions
  - Distribution IDs are not permanent URIs and could change if the implementation is changed
  - Access URLs are hardcoded to be in the finto.fi domain

### /artefacts/{artefactID}/distributions/{distributionID}

- **Implementation status**: Implemented with missing mandatory fields
- **Issues**:
  - Only a few of the mandatory fields are returned as SKOSMOS API includes limited metadata about distributions
  - Different serializations of vocab data are returned as distributions (i.e. turtle, rdfxml, etc.) and no versioning exists for distributions
  - Distribution IDs are not permanent URIs and could change if the implementation is changed
  - Access URLs are hardcoded to be in the finto.fi domain

### /artefacts/{artefactID}/distributions/latest

- **Implementation status**: Not implemented
- **Issues**:
  - All distributions hold the same data in different formats and there is no versioning of the underlying data available in SKOSMOS API

### /artefacts/{artefactID}/record

- **Implementation status**: Not implemented
- **Issues**:
  - SKOSMOS API does not expose this information

### /artefacts/{artefactID}/resources

- **Implementation status**: Fully implemented
- **Issues**:
  - Implementation runs very slowly as parsing and querying the full dataset using rdflib is slow

### /artefacts/{artefactID}/resources/{resourceID}

- **Implementation status**: Fully implemented

### /artefacts/{artefactID}/resources/classes

- **Implementation status**: Fully implemented
- **Issues**:
  - `types` method of the SKOSMOS API does not return much metadata on classes

### /artefacts/{artefactID}/resources/concepts

- **Implementation status**: Fully implemented
- **Issues**:
  - Implementation runs very slowly as parsing and querying the full dataset using rdflib is slow

### /artefacts/{artefactID}/resources/properties

- **Implementation status**: Fully implemented
- **Issues**:
  - Implementation runs very slowly as parsing and querying the full dataset using rdflib is slow

### /artefacts/{artefactID}/resources/individuals

- **Implementation status**: Not implemented
- **Issues**:
  - It is not clear exactly which resources this endpoint should return

### /artefacts/{artefactID}/resources/schemes

- **Implementation status**: Fully implemented
- **Issues**:
  - SKOSMOS API does not return much metadata on concept schemes

### /artefacts/{artefactID}/resources/collections

- **Implementation status**: Fully implemented
- **Issues**:
  - `groups` method of the SKOSMOS API does not return much metadata on collections

### /artefacts/{artefactID}/resources/labels

- **Implementation status**: Fully implemented
- **Issues**:
  - Implementation runs very slowly as parsing and querying the full dataset using rdflib is slow

### /

- **Implementation status**: Not implemented
- **Issues**:
  - SKOSMOS API does not expose any metadata about the service itself

### /records

- **Implementation status**: Not implemented
- **Issues**:
  - SKOSMOS API does not expose this information

### /records/{artefactID}

- **Implementation status**: Not implemented
- **Issues**:
  - SKOSMOS API does not expose this information

### /search

- **Implementation status**: Not implemented
- **Issues**:
  - SKOSMOS API does not include a way to search for metadata

### /search/content

- **Implementation status**: Fully implemented
- **Issues**:
  - In order to allow pagination, the data needs to be parsed and serialized an additional time which slows responses down and adds complexity to the implementation
  - SKOSMOS API `search` method only exposes limited metadata on search results

### /search/metadata

- **Implementation status**: Not implemented
- **Issues**:
  - SKOSMOS API does not include a way to search for metadata

### /doc/api

- **Implementation status**: Not implemented
- **Issues**:
  - Documentation for the API implementation is not hosted anywhere

