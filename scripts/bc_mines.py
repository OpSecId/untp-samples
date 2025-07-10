import requests
import json
import os
import uuid
from difflib import SequenceMatcher


MINE_COUNT = 1000
DID_LOCATION = "did:web:opsecid.github.io:untp-samples"
BC_NRS_MINE_URL = "https://mines.nrs.gov.bc.ca/mine"
BC_ORGBOOK_URL = "https://orgbook.gov.bc.ca"
BC_ORGBOOK_API = f"{BC_ORGBOOK_URL}/api"
BC_MINE_API = "https://nrpti-api-f00029-prod.apps.silver.devops.gov.bc.ca/api/public"
BC_MINE_URL = f"{BC_MINE_API}/search?dataset=Item"
BC_MINES_URL = f"{BC_MINE_API}/search?dataset=MineBCMI&pageNum=0&sortBy=+name"
BC_PERMIT_URL = f"{BC_MINE_API}/search?dataset=CollectionDocuments"
BC_PERMITS_URL = f"{BC_MINE_API}/search?dataset=CollectionBCMI&sortBy=-date"

COMMODITY_MAPPINGS = {}

SYMBOL_MAPPING = {
    '\u201c': '',
    '\u201d': '',
}

        
def get_matched_dict(data, key, value):
    return next(filter(lambda x: x[key] == value, data), None)

class BCMinesClient:
    def __init__(self):
        self.mine_url = BC_MINE_URL
        self.mines_url = BC_MINES_URL
        self.permit_url = BC_PERMIT_URL
        self.permits_url = BC_PERMITS_URL
        self.orgbook_api = BC_ORGBOOK_API
        self.dia_issuer = f"{DID_LOCATION}:regulators:registrar-of-companies"
        self.dfr_issuer = f"{DID_LOCATION}:regulators:chief-permitting-inspector"
        
    def get_mines(self, page_size=MINE_COUNT):
        r = requests.get(f'{self.mines_url}&pageSize={page_size}')
        mines = r.json()[0].get('searchResults')
        mine_records = [
            {
                "_id": mine.get("_id"),
                "name": mine.get("name"),
                "mineType": mine.get("type"),
                "permittee": mine.get("permittee"),
                "commodities": list(set(mine.get("commodities"))),
                "status": mine.get("status"),
                "permitNumber": mine.get("permitNumber"),
                # "permit": mine.get("permit"),
                "tailingsImpoundments": mine.get("tailingsImpoundments"),
                "region": mine.get("region"),
                "location": {
                    "type": mine.get("location").get("type"),
                    "coordinates": mine.get("location").get("coordinates"),
                },
                # "summary": mine.get("summary"),
                "description": mine.get("description"),
                "validFrom": mine.get("dateAdded") or mine.get("datePublished") or mine.get("dateUpdated"),
                # "links": mine.get("links"),
            } for mine in mines
        ]
        return mine_records
        
    def get_mine(self, mine_id):
        r = requests.get(f'{self.mine_url}&_id={mine_id}')
        mine = r.json()[0]
        mine_record = {
            "name": mine.get("name"),
            "mineType": mine.get("type"),
            "permittee": mine.get("permittee"),
            "commodities": list(set(mine.get("commodities"))),
            "status": mine.get("status"),
            "permitNumber": mine.get("permitNumber"),
            # "permit": mine.get("permit"),
            "tailingsImpoundments": mine.get("tailingsImpoundments"),
            "region": mine.get("region"),
            "location": {
                "type": mine.get("location").get("type"),
                "coordinates": mine.get("location").get("coordinates"),
            },
            # "summary": mine.get("summary"),
            "description": mine.get("description"),
            "validFrom": mine.get("dateAdded") or mine.get("datePublished") or mine.get("dateUpdated"),
            # "links": mine.get("links"),
        }
        return mine_record
        
    def get_permits(self, mine_id):
        r = requests.get(f'{self.permits_url}&and[project]={mine_id}')
        permits = r.json()[0].get("searchResults")
        permit_records = [
            {
                '_id': permit.get('_id'),
                'validFrom': permit.get('datePublished') or permit.get('dateAdded') or permit.get('dateUpdated'),
                'permitType': permit.get('type'),
                'permitNumber': permit.get('permitNumber'),
            } for permit in permits
        ]
        return permit_records
        
    def get_permit_numbers(self, permit_records):
        return [permit_record.get('permitNumber') for permit_record in permit_records if permit_record.get('permitNumber') != ""]
        
    def filter_permits(self, permit_records, permit_number):
        return [permit_record for permit_record in permit_records if permit_record.get('permitNumber') == permit_number]
        
    def get_permit_url(self, permit_id):
        r = requests.get(f'{self.permit_url}&_id={permit_id}')
        permit_info = r.json()[0]
        return permit_info.get("url")
        
    def get_organisation_info(self, organisation_name):
        organisation_name = organisation_name.upper()
        r = requests.get(f'{self.orgbook_api}/v4/search/topic?ordering=-score&q={organisation_name}')
        result = r.json().get('results')[0]
        if result.get('type') != 'registration.registries.ca':
            return None
        result_organisation_name = get_matched_dict(result.get('names'), 'type', 'entity_name').get('text')
        print(SequenceMatcher(None, organisation_name, result_organisation_name).ratio())
        
        if SequenceMatcher(None, organisation_name, result_organisation_name).ratio() <= 0.8:
            print(f'⛔ {organisation_name} != {result_organisation_name}')
            return None
        if organisation_name != result_organisation_name:
            print(f'⚠️ {organisation_name} != {result_organisation_name}')
        if organisation_name == result_organisation_name:
            print(f'✅ {organisation_name} == {result_organisation_name}')
            
        organisation_info = {
            'name': result_organisation_name,
            'validFrom': get_matched_dict(result.get('attributes'), 'type', 'registration_date').get('value'),
            'entityType': get_matched_dict(result.get('attributes'), 'type', 'entity_type').get('value'),
            'entityStatus': get_matched_dict(result.get('attributes'), 'type', 'entity_status').get('value'),
            'jurisdiction': get_matched_dict(result.get('attributes'), 'type', 'home_jurisdiction').get('value'),
            'registrationId': result.get('source_id'),
            # 'businessNumber': get_matched_dict(result.get('names'), 'type', 'business_number').get('text'),
        }
        return organisation_info
        
    def create_mines_act_permit(self):
        return
        
    def create_digital_facility_record(self):
        return
        
    def create_whois_vp(self, holder, credential):
        return {
            "@context": ["https://www.w3.org/ns/credentials/v2"],
            "type": ["VerifiablePresentation"],
            "holder": holder,
            "verifiableCredential": [credential]
        }
        
    def create_did_document(self, did, service=None):
        did_document = {
            "@context": ["https://www.w3.org/ns/did/v1"],
            "id": did
        }
        if service:
            did_document['service'] = [service]
        return did_document
    # https://mines.nrs.gov.bc.ca/authorizations#minesActPermits
        
    def create_digital_facility_record(self, facility_id, facility_info, operating_organisation):
        return {
            "@context": [
                "https://www.w3.org/ns/credentials/v2",
                "https://test.uncefact.org/vocabulary/untp/dfr/0.6.0/"
            ],
            "type": ["DigitalFacilityRecord", "VerifiableCredential"],
            "id": f"urn:uuid:{str(uuid.uuid4())}",
            "issuer": {
                "id": self.dfr_issuer,
                "name": "Chief Permitting Inspector"
            },
            "credentialSubject": {
                "type": ["FacilityRecord"],
                "facility": {
                    "type": ["Facility"],
                    "id": facility_id,
                    "name": facility_info.get('name'),
                    "description": facility_info.get('description'),
                    "registeredId": facility_info.get('_id'),
                    "idScheme": {
                        "type": [
                            "IdentifierScheme"
                        ],
                        "id": "https://mines.nrs.gov.bc.ca/",
                        "name": "BC Natural Resource Online Services"
                    },
                    "countryOfOperation": "CA",
                    "operatedByParty": operating_organisation,
                    "locationInformation": {
                        "geoLocation": {
                            "type": "Point",
                            "coordinates": facility_info.get('location').get("coordinates")
                        }
                    },
                    "processCategory": [
                        {
                            "type": [
                                "Classification"
                            ],
                            # "id": "https://unstats.un.org/unsd/classifications/Econ/cpc/46410",
                            # "code": "46410",
                            "name": commodity,
                            # "schemeID": "https://unstats.un.org/unsd/classifications/Econ/cpc/",
                            # "schemeName": "UN Central Product Classification (CPC)"
                        } for commodity in facility_info.get('commodities')
                    ]
                },
                "conformityClaim": [
                    {
                        "type": ["Claim", "Declaration"],
                        # "id": "",
                        # "description": "",
                        "referenceStandard": {
                            "type": ["Standard"],
                            "id": "",
                            "name": "",
                            # "issueDate": "2023-12-05",
                            # "issuingParty": {
                            #     "id": "https://abr.business.gov.au/ABN/View?abn=90664869327",
                            #     "name": "Sample Company Pty Ltd.",
                            #     "registeredId": "90664869327",
                            #     "idScheme": {
                            #         "type": ["IdentifierScheme"],
                            #         "id": "https://id.gs1.org/01/",
                            #         "name": "Global Trade Identification Number (GTIN)"
                            #     }
                            # }
                        },
                        "referenceRegulation": {
                            "type": ["Regulation"],
                            # "id": "https://www.legislation.gov.au/F2008L02309/latest/versions",
                            # "name": "NNational Greenhouse and Energy Reporting (Measurement) Determination",
                            # "jurisdictionCountry": "AU",
                            # "administeredBy": {
                            #     "id": "https://abr.business.gov.au/ABN/View?abn=90664869327",
                            #     "name": "Sample Company Pty Ltd.",
                            #     "registeredId": "90664869327",
                            #     "idScheme": {
                            #     "type": [
                            #         "IdentifierScheme"
                            #     ],
                            #     "id": "https://id.gs1.org/01/",
                            #     "name": "Global Trade Identification Number (GTIN)"
                            #     }
                            # },
                            # "effectiveDate": "2024-03-20"
                        }
                    }
                ],
                "assessmentCriteria": [
                    # {
                    #     "type": ["Criterion"],
                    #     "id": "https://www.globalbattery.org/media/publications/gba-rulebook-v2.0-master.pdf#BatteryAssembly",
                    #     "name": "GBA Battery rule book v2.0 battery assembly guidelines.",
                    #     "description": "Battery is designed for easy disassembly and recycling at end-of-life.",
                    #     "conformityTopic": "circularity.content",
                    #     "status": "proposed",
                    #     "performanceLevel": "\"Category 3 recyclable with 73% recyclability\"",
                    #     "tags": "The quick brown fox jumps over the lazy dog."
                    # }
                ],
                "assessmentDate": facility_info.get('validFrom'),
                "conformance": True,
                "conformityTopic": "governance.compliance",
                "conformityEvidence": {
                    # "linkURL": "https://files.example-certifier.com/1234567.json",
                    # "linkName": "GBA rule book conformity certificate",
                    # "linkType": "https://test.uncefact.org/vocabulary/linkTypes/dcc",
                    # "hashDigest": "6239119dda5bd4c8a6ffb832fe16feaa5c27b7dba154d24c53d4470a2c69adc2",
                    # "hashMethod": "SHA-256",
                    # "encryptionMethod": "AES"
                }
            }
        }
        
    def create_digital_identity_anchor(self, organisation_id, organisation_info):
        return {
            "@context": [
                "https://www.w3.org/ns/credentials/v2",
                "https://test.uncefact.org/vocabulary/untp/dia/0.6.0/"
            ],
            "type": ["DigitalIdentityAnchor", "VerifiableCredential"],
            "id": f"urn:uuid:{str(uuid.uuid4())}",
            "issuer": {
                "id": self.dia_issuer,
                "name": "Registrar of Companies"
            },
            "credentialSubject": {
                "type": ["RegisteredIdentity"],
                "id": organisation_id,
                "name": organisation_info.get('name'),
                "registerType": "Business",
                "registeredId": organisation_info.get('registeredId'),
                "idScheme": {
                    "type": ["IdentifierScheme"],
                    "id": "https://www.bcregistry.gov.bc.ca/",
                    "name": "BC Registry"
                }
            }
        }


mine_client = BCMinesClient()
mine_records = mine_client.get_mines(MINE_COUNT)

mine_count = len(mine_records)
matches = []
no_matches = []
statuses = []

for idx, mine_record in enumerate(mine_records):
    print()
    print(f'{idx}/{mine_count}')
    print(mine_record.get('_id'))
    print(mine_record.get('name'))
    print(mine_record.get('permittee'))
    print(mine_record.get('status'))
    # if mine_record.get('status') not in statuses:
    #     statuses.append(mine_record.get('status'))
    # permit_records = mine_client.get_permits(mine_record.get('_id'))
    # permit_records = mine_client.filter_permits(permit_records, mine_record.get('permitNumber'))
    # for idx, permit_record in enumerate(permit_records):
    #     permit_record["url"] = mine_client.get_permit_url(permit_record.get("_id"))
    #     permit_records[idx] = permit_record

    permittee = mine_record.get('permittee')
    organisation_info = mine_client.get_organisation_info(permittee)
    if not organisation_info:
        no_matches.append(permittee)
        continue
    matches.append(permittee)
    
    
    # Organisational DID & DIA
    registration_id = organisation_info.get('registrationId')
    organisation_id = f"{DID_LOCATION}:organisations:{registration_id}"
    orgbook_service = {
        "id": f"{organisation_id}#orgbook",
        "type": "LinkedDomain",
        "serviceEndpoint": f"{BC_ORGBOOK_URL}/entity/{registration_id}"
    }
    did_document = mine_client.create_did_document(organisation_id, orgbook_service)
    filename = f'../docs/organisations/{registration_id}/did.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+') as f:
        f.write(json.dumps(did_document, indent=2))
        
    dia_credential = mine_client.create_digital_identity_anchor(organisation_id, organisation_info)
    whois_vp = mine_client.create_whois_vp(organisation_id, dia_credential)
    filename = f'../docs/organisations/{registration_id}/whois.vp'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+') as f:
        f.write(json.dumps(whois_vp, indent=2))
    
    # Mining Facility DID & DFR
    mine_id = mine_record.get('_id')
    facility_id = f"{DID_LOCATION}:facilities:mines:{mine_id}"
    facility_service = {
        "id": f"{facility_id}#bc-mine-information",
        "type": "LinkedDomain",
        "serviceEndpoint": f"{BC_NRS_MINE_URL}/{mine_id}"
    }
    did_document = mine_client.create_did_document(facility_id, facility_service)
    filename = f'../docs/facilities/mines/{mine_id}/did.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+') as f:
        f.write(json.dumps(did_document, indent=2))
    
    
    operating_organisation = {
        "id": organisation_id,
        "name": organisation_info.get('name'),
        "registeredId": organisation_info.get('registrationId'),
        "idScheme": {
            "type": ["IdentifierScheme"],
            "id": "https://www.bcregistry.gov.bc.ca/",
            "name": "BC Registry"
        }
    }
    dfr_credential = mine_client.create_digital_facility_record(facility_id, mine_record, operating_organisation)
    whois_vp = mine_client.create_whois_vp(facility_id, dfr_credential)
    filename = f'../docs/facilities/mines/{mine_id}/whois.vp'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+') as f:
        f.write(json.dumps(whois_vp, indent=2))
    
print()
print(f'Matches: {len(matches)}/{mine_count}')
print(f'No Matches: {len(no_matches)}/{mine_count}')
print(statuses)
"""
Closed Care & Maintenance
Closed Reclamation
Closed Reclamation Long-Term Maintenance
Closed Unknown
Operating Seasonal
"""