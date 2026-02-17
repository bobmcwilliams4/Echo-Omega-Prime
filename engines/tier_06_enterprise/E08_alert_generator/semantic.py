import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "E08_alert_generator"
SEMANTIC_MAP_ENGINE = "E08"
# The following SEMANTIC_MAP contains 210 entries

SEMANTIC_MAP = {
    # New Filing Detection
    "new filing": "new_filing_detection",
    "filing received": "new_filing_detection",
    "filed": "new_filing_detection",
    "new application": "new_filing_detection",
    "application filed": "new_filing_detection",
    "filing submitted": "new_filing_detection",
    "submission received": "new_filing_detection",
    "document filed": "new_filing_detection",
    "document submission": "new_filing_detection",
    "filing notification": "new_filing_detection",
    "filing notice": "new_filing_detection",
    "filed notice": "new_filing_detection",
    "filing alert": "new_filing_detection",
    "filing detected": "new_filing_detection",
    "application submitted": "new_filing_detection",
    # Ownership Transfer Detection
    "ownership transfer": "ownership_transfer_detection",
    "transfer of ownership": "ownership_transfer_detection",
    "ownership change": "ownership_transfer_detection",
    "title transfer": "ownership_transfer_detection",
    "title change": "ownership_transfer_detection",
    "owner change": "ownership_transfer_detection",
    "owner transfer": "ownership_transfer_detection",
    "transfer recorded": "ownership_transfer_detection",
    "ownership assignment": "ownership_transfer_detection",
    "assignment of ownership": "ownership_transfer_detection",
    "conveyance": "ownership_transfer_detection",
    "deed transfer": "ownership_transfer_detection",
    "ownership conveyance": "ownership_transfer_detection",
    "ownership assigned": "ownership_transfer_detection",
    "transfer notice": "ownership_transfer_detection",
    # Lease Expiration Warning
    "lease expiration": "lease_expiration_warning",
    "lease expiring": "lease_expiration_warning",
    "lease expiry": "lease_expiration_warning",
    "lease ends": "lease_expiration_warning",
    "lease end date": "lease_expiration_warning",
    "lease termination": "lease_expiration_warning",
    "lease term end": "lease_expiration_warning",
    "lease warning": "lease_expiration_warning",
    "expiration notice": "lease_expiration_warning",
    "expiring lease": "lease_expiration_warning",
    "lease exp notice": "lease_expiration_warning",
    "lease exp alert": "lease_expiration_warning",
    "lease expiring soon": "lease_expiration_warning",
    "lease expiry warning": "lease_expiration_warning",
    # Lease Extension Deadline
    "lease extension": "lease_extension_deadline",
    "lease extension deadline": "lease_extension_deadline",
    "extension deadline": "lease_extension_deadline",
    "extension required": "lease_extension_deadline",
    "lease renewal": "lease_extension_deadline",
    "lease renewal deadline": "lease_extension_deadline",
    "renewal deadline": "lease_extension_deadline",
    "lease extend": "lease_extension_deadline",
    "lease renewal required": "lease_extension_deadline",
    "extension notice": "lease_extension_deadline",
    "lease extension notice": "lease_extension_deadline",
    "lease extend deadline": "lease_extension_deadline",
    # Drilling Permit Issued
    "drilling permit": "drilling_permit_issued",
    "permit issued": "drilling_permit_issued",
    "permit to drill": "drilling_permit_issued",
    "drill permit": "drilling_permit_issued",
    "permit granted": "drilling_permit_issued",
    "drilling approval": "drilling_permit_issued",
    "permit approval": "drilling_permit_issued",
    "drill approval": "drilling_permit_issued",
    "permit notification": "drilling_permit_issued",
    "permit notice": "drilling_permit_issued",
    "drilling permit issued": "drilling_permit_issued",
    "drilling permit granted": "drilling_permit_issued",
    "permit to drill issued": "drilling_permit_issued",
    # Permit Expiration Warning
    "permit expiration": "permit_expiration_warning",
    "permit expiring": "permit_expiration_warning",
    "permit expiry": "permit_expiration_warning",
    "permit ends": "permit_expiration_warning",
    "permit end date": "permit_expiration_warning",
    "permit termination": "permit_expiration_warning",
    "permit term end": "permit_expiration_warning",
    "permit warning": "permit_expiration_warning",
    "permit exp notice": "permit_expiration_warning",
    "permit exp alert": "permit_expiration_warning",
    "permit expiring soon": "permit_expiration_warning",
    "permit expiry warning": "permit_expiration_warning",
    # RRC Violation Detection
    "rrc violation": "rrc_violation_detection",
    "railroad commission violation": "rrc_violation_detection",
    "regulatory violation": "rrc_violation_detection",
    "compliance violation": "rrc_violation_detection",
    "violation detected": "rrc_violation_detection",
    "regulation violation": "rrc_violation_detection",
    "rrc notice": "rrc_violation_detection",
    "rrc enforcement": "rrc_violation_detection",
    "rrc citation": "rrc_violation_detection",
    "rrc fine": "rrc_violation_detection",
    "rrc penalty": "rrc_violation_detection",
    "rrc noncompliance": "rrc_violation_detection",
    "rrc infraction": "rrc_violation_detection",
    # Production Change Detection
    "production change": "production_change_detection",
    "production variance": "production_change_detection",
    "production fluctuation": "production_change_detection",
    "production alert": "production_change_detection",
    "production deviation": "production_change_detection",
    "production anomaly": "production_change_detection",
    "prod change": "production_change_detection",
    "prod variance": "production_change_detection",
    "prod alert": "production_change_detection",
    "output change": "production_change_detection",
    "output variance": "production_change_detection",
    "production shift": "production_change_detection",
    # Operator Change Detection
    "operator change": "operator_change_detection",
    "operator transfer": "operator_change_detection",
    "operator assignment": "operator_change_detection",
    "operator reassignment": "operator_change_detection",
    "operator update": "operator_change_detection",
    "operator notice": "operator_change_detection",
    "operator switch": "operator_change_detection",
    "operator change notice": "operator_change_detection",
    "operator change alert": "operator_change_detection",
    "operator transition": "operator_change_detection",
    "operator replacement": "operator_change_detection",
    # Lien Filed Detection
    "lien filed": "lien_filed_detection",
    "lien filing": "lien_filed_detection",
    "lien notice": "lien_filed_detection",
    "lien recorded": "lien_filed_detection",
    "lien registration": "lien_filed_detection",
    "lien claim": "lien_filed_detection",
    "lien alert": "lien_filed_detection",
    "lien entry": "lien_filed_detection",
    "lien statement": "lien_filed_detection",
    "lien document": "lien_filed_detection",
    # Lien Release Detection
    "lien release": "lien_release_detection",
    "lien removed": "lien_release_detection",
    "lien discharged": "lien_release_detection",
    "lien satisfaction": "lien_release_detection",
    "lien release notice": "lien_release_detection",
    "lien release filed": "lien_release_detection",
    "lien release document": "lien_release_detection",
    "lien cancellation": "lien_release_detection",
    "lien termination": "lien_release_detection",
    "lien release alert": "lien_release_detection",
    # Probate Filing Detection
    "probate filing": "probate_filing_detection",
    "probate filed": "probate_filing_detection",
    "probate notice": "probate_filing_detection",
    "probate application": "probate_filing_detection",
    "probate case": "probate_filing_detection",
    "probate document": "probate_filing_detection",
    "probate submission": "probate_filing_detection",
    "probate record": "probate_filing_detection",
    "probate alert": "probate_filing_detection",
    # Court Order Detection
    "court order": "court_order_detection",
    "court directive": "court_order_detection",
    "court ruling": "court_order_detection",
    "court judgment": "court_order_detection",
    "court decision": "court_order_detection",
    "order issued": "court_order_detection",
    "order entered": "court_order_detection",
    "judicial order": "court_order_detection",
    "court order notice": "court_order_detection",
    "court order alert": "court_order_detection",
    # Tax Delinquency Detection
    "tax delinquency": "tax_delinquency_detection",
    "delinquent tax": "tax_delinquency_detection",
    "tax overdue": "tax_delinquency_detection",
    "tax default": "tax_delinquency_detection",
    "tax arrears": "tax_delinquency_detection",
    "tax nonpayment": "tax_delinquency_detection",
    "tax delinquent": "tax_delinquency_detection",
    "tax delinquency notice": "tax_delinquency_detection",
    "tax delinquency alert": "tax_delinquency_detection",
    # Competitive Activity Detection
    "competitive activity": "competitive_activity_detection",
    "competitor activity": "competitive_activity_detection",
    "comp activity": "competitive_activity_detection",
    "competition detected": "competitive_activity_detection",
    "competitive notice": "competitive_activity_detection",
    "competitive alert": "competitive_activity_detection",
    "competitor alert": "competitive_activity_detection",
    "competitive event": "competitive_activity_detection",
    # Price Threshold Alert
    "price threshold": "price_threshold_alert",
    "price alert": "price_threshold_alert",
    "price limit": "price_threshold_alert",
    "price trigger": "price_threshold_alert",
    "price exceeded": "price_threshold_alert",
    "price drop": "price_threshold_alert",
    "price rise": "price_threshold_alert",
    "price breach": "price_threshold_alert",
    "price threshold alert": "price_threshold_alert",
    # Royalty Payment Alert
    "royalty payment": "royalty_payment_alert",
    "royalty paid": "royalty_payment_alert",
    "royalty notice": "royalty_payment_alert",
    "royalty alert": "royalty_payment_alert",
    "royalty distribution": "royalty_payment_alert",
    "royalty disbursement": "royalty_payment_alert",
    "royalty check": "royalty_payment_alert",
    "royalty statement": "royalty_payment_alert",
    "royalty payment alert": "royalty_payment_alert",
    # Well Shut-In Detection
    "well shut-in": "well_shut_in_detection",
    "shut-in notice": "well_shut_in_detection",
    "shut-in alert": "well_shut_in_detection",
    "well shut in": "well_shut_in_detection",
    "well closure": "well_shut_in_detection",
    "well closed": "well_shut_in_detection",
    "well suspension": "well_shut_in_detection",
    "well suspended": "well_shut_in_detection",
    "shut-in event": "well_shut_in_detection",
    # Plugging Notice Detection
    "plugging notice": "plugging_notice_detection",
    "plugging alert": "plugging_notice_detection",
    "well plugging": "plugging_notice_detection",
    "plugging event": "plugging_notice_detection",
    "plug notice": "plugging_notice_detection",
    "well plug": "plugging_notice_detection",
    "well plugged": "plugging_notice_detection",
    "plugging required": "plugging_notice_detection",
    "plugging scheduled": "plugging_notice_detection",
    # Unitization Application
    "unitization application": "unitization_application",
    "unitization filed": "unitization_application",
    "unitization notice": "unitization_application",
    "unitization request": "unitization_application",
    "unitization petition": "unitization_application",
    "unitization alert": "unitization_application",
    "unitization submission": "unitization_application",
    "unitization filing": "unitization_application",
    "unitization app": "unitization_application",
    # Force Pooling Application
    "force pooling": "force_pooling_application",
    "force pooling application": "force_pooling_application",
    "force pooling filed": "force_pooling_application",
    "force pooling notice": "force_pooling_application",
    "force pooling request": "force_pooling_application",
    "force pooling petition": "force_pooling_application",
    "force pooling alert": "force_pooling_application",
    "force pooling submission": "force_pooling_application",
    "force pooling filing": "force_pooling_application",
    "force pooling app": "force_pooling_application",
    # Surface Damage Claim
    "surface damage": "surface_damage_claim",
    "surface damage claim": "surface_damage_claim",
    "surface claim": "surface_damage_claim",
    "surface damages": "surface_damage_claim",
    "surface damage notice": "surface_damage_claim",
    "surface damage alert": "surface_damage_claim",
    "surface claim filed": "surface_damage_claim",
    "surface damage filing": "surface_damage_claim",
    # Environmental Release Detection
    "environmental release": "environmental_release_detection",
    "env release": "environmental_release_detection",
    "environmental incident": "environmental_release_detection",
    "environmental spill": "environmental_release_detection",
    "env spill": "environmental_release_detection",
    "environmental alert": "environmental_release_detection",
    "environmental notice": "environmental_release_detection",
    "environmental event": "environmental_release_detection",
    "environmental discharge": "environmental_release_detection",
    # Bankruptcy Filing Detection
    "bankruptcy filing": "bankruptcy_filing_detection",
    "bankruptcy filed": "bankruptcy_filing_detection",
    "bankruptcy notice": "bankruptcy_filing_detection",
    "bankruptcy alert": "bankruptcy_filing_detection",
    "bankruptcy petition": "bankruptcy_filing_detection",
    "bankruptcy event": "bankruptcy_filing_detection",
    "bankruptcy case": "bankruptcy_filing_detection",
    "bankruptcy document": "bankruptcy_filing_detection",
    # Title Defect Detection
    "title defect": "title_defect_detection",
    "title issue": "title_defect_detection",
    "title problem": "title_defect_detection",
    "title cloud": "title_defect_detection",
    "title defect notice": "title_defect_detection",
    "title defect alert": "title_defect_detection",
    "title defect filed": "title_defect_detection",
    "title defect document": "title_defect_detection",
    # Assignment Recording
    "assignment recording": "assignment_recording",
    "assignment filed": "assignment_recording",
    "assignment notice": "assignment_recording",
    "assignment recorded": "assignment_recording",
    "assignment document": "assignment_recording",
    "assignment submission": "assignment_recording",
    "assignment filing": "assignment_recording",
    "assignment alert": "assignment_recording",
    # Division Order Change
    "division order change": "division_order_change",
    "division order updated": "division_order_change",
    "division order update": "division_order_change",
    "division order notice": "division_order_change",
    "division order alert": "division_order_change",
    "division order amendment": "division_order_change",
    "division order change notice": "division_order_change",
    "division order change alert": "division_order_change",
    # Well Completion Notice
    "well completion": "well_completion_notice",
    "well completed": "well_completion_notice",
    "completion notice": "well_completion_notice",
    "completion filed": "well_completion_notice",
    "completion alert": "well_completion_notice",
    "well completion notice": "well_completion_notice",
    "completion document": "well_completion_notice",
    "completion submission": "well_completion_notice",
    # Spacing Order Detection
    "spacing order": "spacing_order_detection",
    "spacing order notice": "spacing_order_detection",
    "spacing order alert": "spacing_order_detection",
    "spacing order filed": "spacing_order_detection",
    "spacing order document": "spacing_order_detection",
    "spacing order submission": "spacing_order_detection",
    "spacing order application": "spacing_order_detection",
    # Force Majeure Declaration
    "force majeure": "force_majeure_declaration",
    "force majeure declaration": "force_majeure_declaration",
    "force majeure notice": "force_majeure_declaration",
    "force majeure alert": "force_majeure_declaration",
    "force majeure event": "force_majeure_declaration",
    "force majeure filed": "force_majeure_declaration",
    "force majeure filing": "force_majeure_declaration",
}

_EXPECTED_ENTRY_COUNT = 210

def _compute_map_hash():
    items = sorted((k, SEMANTIC_MAP[k]) for k in SEMANTIC_MAP)
    m = hashlib.sha256()
    for k, v in items:
        m.update(k.encode("utf-8"))
        m.update(b"->")
        m.update(v.encode("utf-8"))
        m.update(b"\n")
    return m.hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity():
    actual_count = len(SEMANTIC_MAP)
    actual_hash = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (actual_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "ok" if is_valid else "error",
        "entries": actual_count,
        "hash": actual_hash,
        "is_valid": is_valid
    }

def _normalize_key(term):
    term = term.lower()
    term = re.sub(r"[^a-z0-9\s\-]", "", term)
    term = re.sub(r"\s+", " ", term)
    return term.strip()

def normalize_term(term: str) -> str:
    key = _normalize_key(term)
    return SEMANTIC_MAP.get(key, key)

def get_related_terms(term: str) -> list:
    norm = normalize_term(term)
    return [k for k, v in SEMANTIC_MAP.items() if v == norm]

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)