

BC_REG_ID_SCHEME = {
    "type": ["IdentifierScheme"],
    "id": "https://www.bcregistry.gov.bc.ca/",
    "name": "BC Registry"
}

BC_MINE_ID_SCHEME = {
    "type": ["IdentifierScheme"],
    "id": "https://mines.nrs.gov.bc.ca/",
    "name": "BC Natural Resource Online Services"
}

BC_MINE_PERMIT_STANDARD = {
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
}

BC_MINE_PERMIT_REGULATION = {
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

BC_MINE_PERMIT_CRITERIA = {
    "type": ["Criterion"],
    # "id": "https://www.globalbattery.org/media/publications/gba-rulebook-v2.0-master.pdf#BatteryAssembly",
    # "name": "GBA Battery rule book v2.0 battery assembly guidelines.",
    # "description": "Battery is designed for easy disassembly and recycling at end-of-life.",
    # "conformityTopic": "circularity.content",
    # "status": "proposed",
    # "performanceLevel": "\"Category 3 recyclable with 73% recyclability\"",
    # "tags": "The quick brown fox jumps over the lazy dog."
}

BC_MINE_PERMIT_CONFORMITY_CLAIM = {
    "type": ["Claim", "Declaration"],
    # "id": "",
    # "description": "",
    "referenceStandard": BC_MINE_PERMIT_STANDARD,
    "referenceRegulation": BC_MINE_PERMIT_REGULATION
}

CPC_21_CSV_URL = "https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/CPC_Ver_2_1_english_structure.txt"
BC_MINE_COMMODITY_CLASSIFICATION_SCHEME = {
    "type": ["Classification"],
    "schemeID": "https://unstats.un.org/unsd/classifications/unsdclassifications/cpcv21.pdf",
    "schemeName": "Central Product Classification (CPC) Version 2.1"
}
BC_MINE_COMMODITY_CLASSIFICATIONS = {
    "copper": {
        "name": "Copper",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#14210',
        "code": "14210",
    },
    "bismuth": {
        "name": "Bismuth",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#41603',
        "code": "41603",
    },
    "gold": {
        "name": "Gold",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#41320',
        "code": "41320",
    },
    "molybdenum": {
        "name": "Molybdenum",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#41601',
        "code": "41601",
    },
    "nickel": {
        "name": "Nickel",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#14220',
        "code": "14220",
    },
    "zinc": {
        "name": "Zinc",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#14290',
        "code": "14290",
    },
    "rhenium": {
        "name": "Rhenium",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#41601',
        "code": "41601",
    },
    "silica": {
        "name": "Silica",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#34270',
        "code": "34270",
    },
    "tungsten": {
        "name": "Tungsten",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#41601',
        "code": "41601",
    },
    "iron": {
        "name": "Iron",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#14100',
        "code": "14100",
    },
    "lead": {
        "name": "Lead",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#14290',
        "code": "14290",
    },
    "silver": {
        "name": "Silver",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#41310',
        "code": "41310",
    },
    "sand_and_gravel": {
        "name": "Sand and Gravel",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#15320',
        "code": "15320",
    },
    "mercury": {
        "name": "Mercury",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#34250',
        "code": "34250",
    },
    "asbestos": {
        "name": "Asbestos",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#37570',
        "code": "37570",
    },
    "magnesium": {
        "name": "Magnesium",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#41601',
        "code": "41601",
    },
    "magnetite": {
        "name": "Magnetite",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#14100',
        "code": "14100",
    },
    "magnesite": {
        "name": "Magnesite",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#41601',
        "code": "41601",
    },
    "thermal_coal": {
        "name": "Thermal Coal",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#11',
        "code": "11",
    },
    "metallurgic": {
        "name": "metallurgic",
        "id": BC_MINE_COMMODITY_CLASSIFICATION_SCHEME['schemeID'] + '#14',
        "code": "14",
    }
}