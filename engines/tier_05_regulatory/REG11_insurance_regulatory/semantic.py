import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "REG11_insurance_regulatory"
SEMANTIC_MAP_ENGINE = "REG11"
_EXPECTED_ENTRY_COUNT = 215

SEMANTIC_MAP = {
    # McCarran-Ferguson Act Federal Antitrust Exemption
    "mccarran-ferguson act": "mccarran-ferguson act federal antitrust exemption",
    "mccarran ferguson act": "mccarran-ferguson act federal antitrust exemption",
    "mccarran-ferguson": "mccarran-ferguson act federal antitrust exemption",
    "mccarran ferguson": "mccarran-ferguson act federal antitrust exemption",
    "mccarran-ferguson antitrust exemption": "mccarran-ferguson act federal antitrust exemption",
    "federal antitrust exemption": "mccarran-ferguson act federal antitrust exemption",
    "antitrust exemption": "mccarran-ferguson act federal antitrust exemption",
    "mfa": "mccarran-ferguson act federal antitrust exemption",
    "mcarran-ferguson": "mccarran-ferguson act federal antitrust exemption",
    "mcarran-ferguson act exemption": "mccarran-ferguson act federal antitrust exemption",
    "mccarran-ferguson act antitrust": "mccarran-ferguson act federal antitrust exemption",
    "mccarran-ferguson act federal exemption": "mccarran-ferguson act federal antitrust exemption",

    # Texas Rate Filing Prior Approval Requirement
    "texas rate filing": "texas rate filing prior approval requirement",
    "rate filing prior approval": "texas rate filing prior approval requirement",
    "rate filing approval": "texas rate filing prior approval requirement",
    "rate approval": "texas rate filing prior approval requirement",
    "tx rate filing": "texas rate filing prior approval requirement",
    "tx prior approval": "texas rate filing prior approval requirement",
    "texas prior approval": "texas rate filing prior approval requirement",
    "rate filing requirement": "texas rate filing prior approval requirement",
    "rate filing": "texas rate filing prior approval requirement",
    "rate prior approval": "texas rate filing prior approval requirement",
    "rate approval requirement": "texas rate filing prior approval requirement",
    "texas insurance rate approval": "texas rate filing prior approval requirement",

    # Surplus Lines Eligibility and Tax Code Section 226
    "surplus lines eligibility": "surplus lines eligibility and tax code section 226",
    "surplus lines": "surplus lines eligibility and tax code section 226",
    "surplus lines tax": "surplus lines eligibility and tax code section 226",
    "surplus lines section 226": "surplus lines eligibility and tax code section 226",
    "surplus lines tax code": "surplus lines eligibility and tax code section 226",
    "surplus lines code 226": "surplus lines eligibility and tax code section 226",
    "surplus lines eligibility requirement": "surplus lines eligibility and tax code section 226",
    "surplus lines eligibility requirements": "surplus lines eligibility and tax code section 226",
    "surplus lines tax section 226": "surplus lines eligibility and tax code section 226",
    "surplus lines tax code section 226": "surplus lines eligibility and tax code section 226",
    "sl eligibility": "surplus lines eligibility and tax code section 226",
    "sl tax": "surplus lines eligibility and tax code section 226",
    "sl section 226": "surplus lines eligibility and tax code section 226",

    # Risk-Based Capital (RBC) Requirements and Solvency Monitoring
    "risk-based capital": "risk-based capital requirements and solvency monitoring",
    "risk based capital": "risk-based capital requirements and solvency monitoring",
    "rbc": "risk-based capital requirements and solvency monitoring",
    "rbc requirements": "risk-based capital requirements and solvency monitoring",
    "risk-based capital requirements": "risk-based capital requirements and solvency monitoring",
    "solvency monitoring": "risk-based capital requirements and solvency monitoring",
    "solvency requirements": "risk-based capital requirements and solvency monitoring",
    "solvency": "risk-based capital requirements and solvency monitoring",
    "capital requirements": "risk-based capital requirements and solvency monitoring",
    "risk based capital monitoring": "risk-based capital requirements and solvency monitoring",
    "risk-based capital monitoring": "risk-based capital requirements and solvency monitoring",
    "risk based capital solvency": "risk-based capital requirements and solvency monitoring",

    # Market Conduct Examinations and NAIC Market Regulation Handbook
    "market conduct examination": "market conduct examinations and naic market regulation handbook",
    "market conduct examinations": "market conduct examinations and naic market regulation handbook",
    "market conduct": "market conduct examinations and naic market regulation handbook",
    "market regulation handbook": "market conduct examinations and naic market regulation handbook",
    "naic market regulation handbook": "market conduct examinations and naic market regulation handbook",
    "market conduct exam": "market conduct examinations and naic market regulation handbook",
    "market conduct exams": "market conduct examinations and naic market regulation handbook",
    "market regulation": "market conduct examinations and naic market regulation handbook",
    "naic market conduct": "market conduct examinations and naic market regulation handbook",
    "market conduct handbook": "market conduct examinations and naic market regulation handbook",
    "market conduct review": "market conduct examinations and naic market regulation handbook",
    "market conduct investigation": "market conduct examinations and naic market regulation handbook",

    # Unfair Claims Settlement Practices Act (UCSPA)
    "unfair claims settlement practices act": "unfair claims settlement practices act",
    "ucspa": "unfair claims settlement practices act",
    "unfair claims settlement": "unfair claims settlement practices act",
    "unfair claim settlement": "unfair claims settlement practices act",
    "unfair claims act": "unfair claims settlement practices act",
    "unfair claims practices": "unfair claims settlement practices act",
    "claims settlement act": "unfair claims settlement practices act",
    "unfair claim practices": "unfair claims settlement practices act",
    "unfair settlement act": "unfair claims settlement practices act",
    "unfair claims": "unfair claims settlement practices act",
    "claims settlement practices act": "unfair claims settlement practices act",

    # Producer Licensing and Appointment Requirements
    "producer licensing": "producer licensing and appointment requirements",
    "producer license": "producer licensing and appointment requirements",
    "producer appointment": "producer licensing and appointment requirements",
    "producer licensing requirements": "producer licensing and appointment requirements",
    "producer appointment requirements": "producer licensing and appointment requirements",
    "producer license requirements": "producer licensing and appointment requirements",
    "producer requirements": "producer licensing and appointment requirements",
    "producer appointment requirement": "producer licensing and appointment requirements",
    "producer licensing requirement": "producer licensing and appointment requirements",
    "producer appointment req": "producer licensing and appointment requirements",
    "producer licensing req": "producer licensing and appointment requirements",
    "producer licensure": "producer licensing and appointment requirements",
    "producer licensure requirements": "producer licensing and appointment requirements",
    "producer appointment reqs": "producer licensing and appointment requirements",

    # Texas Guaranty Association Coverage and Assessments
    "texas guaranty association": "texas guaranty association coverage and assessments",
    "texas guaranty association coverage": "texas guaranty association coverage and assessments",
    "texas guaranty association assessment": "texas guaranty association coverage and assessments",
    "texas guaranty association assessments": "texas guaranty association coverage and assessments",
    "tx guaranty association": "texas guaranty association coverage and assessments",
    "guaranty association coverage": "texas guaranty association coverage and assessments",
    "guaranty association assessment": "texas guaranty association coverage and assessments",
    "guaranty association assessments": "texas guaranty association coverage and assessments",
    "guaranty association": "texas guaranty association coverage and assessments",
    "texas insurance guaranty association": "texas guaranty association coverage and assessments",
    "guaranty association tx": "texas guaranty association coverage and assessments",

    # Form Approval and Policy Language Requirements
    "form approval": "form approval and policy language requirements",
    "policy language requirements": "form approval and policy language requirements",
    "form approval requirements": "form approval and policy language requirements",
    "policy language requirement": "form approval and policy language requirements",
    "form approval requirement": "form approval and policy language requirements",
    "policy language": "form approval and policy language requirements",
    "form approval req": "form approval and policy language requirements",
    "policy language req": "form approval and policy language requirements",
    "form approval reqs": "form approval and policy language requirements",
    "policy language reqs": "form approval and policy language requirements",
    "policy form approval": "form approval and policy language requirements",
    "policy form approval requirements": "form approval and policy language requirements",

    # Reinsurance Credit and Unauthorized Reinsurer Collateral Requirements
    "reinsurance credit": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "unauthorized reinsurer collateral requirements": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "reinsurance credit requirements": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "unauthorized reinsurer collateral": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "reinsurance collateral requirements": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "reinsurance collateral": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "unauthorized reinsurer requirements": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "unauthorized reinsurer requirement": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "unauthorized reinsurer": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "reinsurer collateral requirements": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "reinsurer collateral": "reinsurance credit and unauthorized reinsurer collateral requirements",

    # NAIC Model Laws and Uniform State Adoption
    "naic model laws": "naic model laws and uniform state adoption",
    "naic model law": "naic model laws and uniform state adoption",
    "model laws": "naic model laws and uniform state adoption",
    "model law": "naic model laws and uniform state adoption",
    "naic uniform state adoption": "naic model laws and uniform state adoption",
    "uniform state adoption": "naic model laws and uniform state adoption",
    "naic uniform adoption": "naic model laws and uniform state adoption",
    "model law adoption": "naic model laws and uniform state adoption",
    "model laws adoption": "naic model laws and uniform state adoption",
    "naic adoption": "naic model laws and uniform state adoption",
    "naic model": "naic model laws and uniform state adoption",
    "naic model laws adoption": "naic model laws and uniform state adoption",

    # Insurance Holding Company System and Form B/C/D/E Filings
    "insurance holding company system": "insurance holding company system and form b/c/d/e filings",
    "holding company system": "insurance holding company system and form b/c/d/e filings",
    "insurance holding company": "insurance holding company system and form b/c/d/e filings",
    "form b filings": "insurance holding company system and form b/c/d/e filings",
    "form c filings": "insurance holding company system and form b/c/d/e filings",
    "form d filings": "insurance holding company system and form b/c/d/e filings",
    "form e filings": "insurance holding company system and form b/c/d/e filings",
    "form b/c/d/e filings": "insurance holding company system and form b/c/d/e filings",
    "insurance holding company system filings": "insurance holding company system and form b/c/d/e filings",
    "holding company filings": "insurance holding company system and form b/c/d/e filings",
    "holding company form filings": "insurance holding company system and form b/c/d/e filings",
    "insurance holding company form filings": "insurance holding company system and form b/c/d/e filings",

    # Rebating Prohibition and Permitted Inducements
    "rebating prohibition": "rebating prohibition and permitted inducements",
    "rebating": "rebating prohibition and permitted inducements",
    "rebating inducements": "rebating prohibition and permitted inducements",
    "rebating permitted inducements": "rebating prohibition and permitted inducements",
    "permitted inducements": "rebating prohibition and permitted inducements",
    "rebate prohibition": "rebating prohibition and permitted inducements",
    "rebate": "rebating prohibition and permitted inducements",
    "rebate inducements": "rebating prohibition and permitted inducements",
    "rebate permitted inducements": "rebating prohibition and permitted inducements",
    "rebating rules": "rebating prohibition and permitted inducements",
    "rebating regulation": "rebating prohibition and permitted inducements",

    # Twisting and Replacement Regulation
    "twisting regulation": "twisting and replacement regulation",
    "twisting": "twisting and replacement regulation",
    "replacement regulation": "twisting and replacement regulation",
    "replacement": "twisting and replacement regulation",
    "twisting and replacement": "twisting and replacement regulation",
    "twisting and replacement regulation": "twisting and replacement regulation",
    "twisting rules": "twisting and replacement regulation",
    "replacement rules": "twisting and replacement regulation",
    "twisting replacement": "twisting and replacement regulation",
    "twisting replacement regulation": "twisting and replacement regulation",

    # Advertising and Marketing Regulation
    "advertising regulation": "advertising and marketing regulation",
    "marketing regulation": "advertising and marketing regulation",
    "advertising and marketing regulation": "advertising and marketing regulation",
    "advertising": "advertising and marketing regulation",
    "marketing": "advertising and marketing regulation",
    "advertising and marketing": "advertising and marketing regulation",
    "advertising rules": "advertising and marketing regulation",
    "marketing rules": "advertising and marketing regulation",
    "advertising marketing regulation": "advertising and marketing regulation",

    # Privacy and Information Security (GLBA and State Laws)
    "privacy and information security": "privacy and information security (glba and state laws)",
    "privacy": "privacy and information security (glba and state laws)",
    "information security": "privacy and information security (glba and state laws)",
    "glba": "privacy and information security (glba and state laws)",
    "gramm-leach-bliley act": "privacy and information security (glba and state laws)",
    "gramm leach bliley act": "privacy and information security (glba and state laws)",
    "gramm leach bliley": "privacy and information security (glba and state laws)",
    "glba privacy": "privacy and information security (glba and state laws)",
    "glba security": "privacy and information security (glba and state laws)",
    "state privacy laws": "privacy and information security (glba and state laws)",
    "state information security laws": "privacy and information security (glba and state laws)",
    "privacy laws": "privacy and information security (glba and state laws)",
    "information security laws": "privacy and information security (glba and state laws)",
    "privacy regulation": "privacy and information security (glba and state laws)",
    "information security regulation": "privacy and information security (glba and state laws)",
    "privacy and security": "privacy and information security (glba and state laws)",

    # Annual Financial Statement Filing and Statutory Accounting
    "annual financial statement filing": "annual financial statement filing and statutory accounting",
    "annual financial statement": "annual financial statement filing and statutory accounting",
    "statutory accounting": "annual financial statement filing and statutory accounting",
    "statutory accounting requirements": "annual financial statement filing and statutory accounting",
    "annual statement filing": "annual financial statement filing and statutory accounting",
    "annual statement": "annual financial statement filing and statutory accounting",
    "financial statement filing": "annual financial statement filing and statutory accounting",
    "financial statement": "annual financial statement filing and statutory accounting",
    "annual financial statement requirements": "annual financial statement filing and statutory accounting",
    "annual statement requirements": "annual financial statement filing and statutory accounting",
    "statutory accounting filing": "annual financial statement filing and statutory accounting",
    "statutory accounting filing requirements": "annual financial statement filing and statutory accounting",

    # Financial Examination Authority and Examination Report
    "financial examination authority": "financial examination authority and examination report",
    "financial examination": "financial examination authority and examination report",
    "examination authority": "financial examination authority and examination report",
    "examination report": "financial examination authority and examination report",
    "financial examination report": "financial examination authority and examination report",
    "financial exam authority": "financial examination authority and examination report",
    "financial exam report": "financial examination authority and examination report",
    "financial exam": "financial examination authority and examination report",
    "exam authority": "financial examination authority and examination report",
    "exam report": "financial examination authority and examination report",
    "financial examination requirements": "financial examination authority and examination report",
    "financial exam requirements": "financial examination authority and examination report",

    # Own Risk and Solvency Assessment (ORSA) Requirement
    "own risk and solvency assessment": "own risk and solvency assessment requirement",
    "orsa": "own risk and solvency assessment requirement",
    "orsa requirement": "own risk and solvency assessment requirement",
    "orsa requirements": "own risk and solvency assessment requirement",
    "own risk solvency assessment": "own risk and solvency assessment requirement",
    "own risk and solvency assessment requirement": "own risk and solvency assessment requirement",
    "own risk and solvency assessment requirements": "own risk and solvency assessment requirement",
    "orsa regulation": "own risk and solvency assessment requirement",
    "orsa regulations": "own risk and solvency assessment requirement",
    "own risk assessment": "own risk and solvency assessment requirement",
    "solvency assessment": "own risk and solvency assessment requirement",

    # Misspellings, abbreviations, and related terms
    "mcarran-ferguson antitrust": "mccarran-ferguson act federal antitrust exemption",
    "mcarran-ferguson exemption": "mccarran-ferguson act federal antitrust exemption",
    "mcarran-ferguson act antitrust exemption": "mccarran-ferguson act federal antitrust exemption",
    "mcarran-ferguson act federal antitrust": "mccarran-ferguson act federal antitrust exemption",
    "mcarran-ferguson act antitrust exemption": "mccarran-ferguson act federal antitrust exemption",
    "mcarran-ferguson act antitrust": "mccarran-ferguson act federal antitrust exemption",
    "mcarran-ferguson act exemption": "mccarran-ferguson act federal antitrust exemption",

    "tx rate prior approval": "texas rate filing prior approval requirement",
    "texas rate prior approval": "texas rate filing prior approval requirement",
    "rate prior approval requirement": "texas rate filing prior approval requirement",

    "sl eligibility requirement": "surplus lines eligibility and tax code section 226",
    "sl eligibility requirements": "surplus lines eligibility and tax code section 226",
    "sl tax section 226": "surplus lines eligibility and tax code section 226",
    "sl tax code section 226": "surplus lines eligibility and tax code section 226",

    "risk-based capital req": "risk-based capital requirements and solvency monitoring",
    "risk based capital req": "risk-based capital requirements and solvency monitoring",
    "risk based capital requirements": "risk-based capital requirements and solvency monitoring",
    "solvency monitoring requirements": "risk-based capital requirements and solvency monitoring",

    "market conduct examination requirements": "market conduct examinations and naic market regulation handbook",
    "market conduct exam requirements": "market conduct examinations and naic market regulation handbook",
    "market regulation exam": "market conduct examinations and naic market regulation handbook",
    "market regulation exams": "market conduct examinations and naic market regulation handbook",
    "market regulation examination": "market conduct examinations and naic market regulation handbook",
    "market regulation examination requirements": "market conduct examinations and naic market regulation handbook",

    "unfair claims settlement practices": "unfair claims settlement practices act",
    "unfair claims settlement practice": "unfair claims settlement practices act",
    "unfair claim settlement practice": "unfair claims settlement practices act",
    "unfair claims settlement practices act requirements": "unfair claims settlement practices act",
    "unfair claims settlement act": "unfair claims settlement practices act",

    "producer licensing and appointment": "producer licensing and appointment requirements",
    "producer licensing and appointment requirements": "producer licensing and appointment requirements",
    "producer appointment and licensing": "producer licensing and appointment requirements",
    "producer appointment and licensing requirements": "producer licensing and appointment requirements",

    "texas guaranty association requirements": "texas guaranty association coverage and assessments",
    "texas guaranty association req": "texas guaranty association coverage and assessments",
    "guaranty association requirements": "texas guaranty association coverage and assessments",
    "guaranty association req": "texas guaranty association coverage and assessments",

    "form approval and policy language": "form approval and policy language requirements",
    "form approval and policy language requirements": "form approval and policy language requirements",
    "policy form language requirements": "form approval and policy language requirements",
    "policy form language requirement": "form approval and policy language requirements",

    "reinsurance credit and unauthorized reinsurer collateral": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "reinsurance credit and unauthorized reinsurer collateral requirements": "reinsurance credit and unauthorized reinsurer collateral requirements",
    "unauthorized reinsurer collateral requirement": "reinsurance credit and unauthorized reinsurer collateral requirements",

    "naic model laws and uniform state adoption": "naic model laws and uniform state adoption",
    "model laws and uniform state adoption": "naic model laws and uniform state adoption",
    "model law and uniform state adoption": "naic model laws and uniform state adoption",

    "insurance holding company system and form b filings": "insurance holding company system and form b/c/d/e filings",
    "insurance holding company system and form c filings": "insurance holding company system and form b/c/d/e filings",
    "insurance holding company system and form d filings": "insurance holding company system and form b/c/d/e filings",
    "insurance holding company system and form e filings": "insurance holding company system and form b/c/d/e filings",

    "rebating prohibition and permitted inducements": "rebating prohibition and permitted inducements",
    "rebating and permitted inducements": "rebating prohibition and permitted inducements",
    "rebating and inducements": "rebating prohibition and permitted inducements",

    "twisting and replacement regulation": "twisting and replacement regulation",
    "twisting and replacement": "twisting and replacement regulation",

    "advertising and marketing regulation": "advertising and marketing regulation",
    "advertising and marketing": "advertising and marketing regulation",

    "privacy and information security (glba and state laws)": "privacy and information security (glba and state laws)",
    "privacy and information security laws": "privacy and information security (glba and state laws)",
    "privacy and information security requirements": "privacy and information security (glba and state laws)",

    "annual financial statement filing and statutory accounting": "annual financial statement filing and statutory accounting",
    "annual financial statement filing requirements": "annual financial statement filing and statutory accounting",
    "statutory accounting and annual financial statement filing": "annual financial statement filing and statutory accounting",

    "financial examination authority and examination report": "financial examination authority and examination report",
    "financial examination authority requirements": "financial examination authority and examination report",
    "examination authority and report": "financial examination authority and examination report",

    "own risk and solvency assessment requirement": "own risk and solvency assessment requirement",
    "own risk and solvency assessment requirements": "own risk and solvency assessment requirement",
    "orsa and solvency assessment": "own risk and solvency assessment requirement",
    "orsa and solvency assessment requirement": "own risk and solvency assessment requirement",
    "orsa and solvency assessment requirements": "own risk and solvency assessment requirement",
}

def _compute_map_hash():
    items = sorted(SEMANTIC_MAP.items())
    joined = "".join(f"{k}:{v};" for k, v in items)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity():
    actual_count = len(SEMANTIC_MAP)
    computed_hash = _compute_map_hash()
    is_valid = (
        actual_count == _EXPECTED_ENTRY_COUNT and
        computed_hash == _MAP_INTEGRITY_HASH
    )
    return {
        "status": "OK" if is_valid else "ERROR",
        "entries": actual_count,
        "hash": computed_hash,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    t = term.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return SEMANTIC_MAP.get(t, t)

def get_related_terms(term: str) -> list[str]:
    normalized = normalize_term(term)
    related = []
    for k, v in SEMANTIC_MAP.items():
        if v == normalized and k != normalized:
            related.append(k)
    return related

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)