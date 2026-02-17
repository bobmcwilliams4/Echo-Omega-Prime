import hashlib
import re
from typing import Dict, List, Any

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "ET08_security_auditor"
SEMANTIC_MAP_ENGINE = "ET08"
_EXPECTED_ENTRY_COUNT = 212

SEMANTIC_MAP = {
    # Voice Transcript Audit Logging
    "voice transcript audit logging": "voice_audit_logging",
    "audit logging": "voice_audit_logging",
    "transcript audit log": "voice_audit_logging",
    "voice audit log": "voice_audit_logging",
    "voice log": "voice_audit_logging",
    "audit trail": "voice_audit_logging",
    "audit log": "voice_audit_logging",
    "audit record": "voice_audit_logging",
    "audit logs": "voice_audit_logging",
    "voice transcript audit log": "voice_audit_logging",
    "transcript audit logging": "voice_audit_logging",
    "audit logging for voice": "voice_audit_logging",
    "audit logging voice": "voice_audit_logging",
    "voice transcript logging": "voice_audit_logging",
    "voice logging": "voice_audit_logging",
    "audit": "voice_audit_logging",

    # PII Detection in Voice Transcripts
    "pii detection": "pii_detection_voice",
    "voice pii detection": "pii_detection_voice",
    "personal data detection": "pii_detection_voice",
    "personally identifiable information detection": "pii_detection_voice",
    "pii": "pii_detection_voice",
    "pii scan": "pii_detection_voice",
    "pii identification": "pii_detection_voice",
    "voice transcript pii": "pii_detection_voice",
    "transcript pii detection": "pii_detection_voice",
    "voice transcript personal data": "pii_detection_voice",
    "voice transcript sensitive data": "pii_detection_voice",
    "voice transcript privacy": "pii_detection_voice",
    "voice privacy": "pii_detection_voice",
    "voice transcript privacy scan": "pii_detection_voice",

    # Transcript-to-Evidence Binding
    "transcript evidence binding": "transcript_evidence_binding",
    "transcript to evidence binding": "transcript_evidence_binding",
    "evidence binding": "transcript_evidence_binding",
    "binding transcript to evidence": "transcript_evidence_binding",
    "voice transcript evidence binding": "transcript_evidence_binding",
    "transcript evidence link": "transcript_evidence_binding",
    "transcript-evidence binding": "transcript_evidence_binding",
    "transcript evidence association": "transcript_evidence_binding",
    "transcript evidence mapping": "transcript_evidence_binding",
    "transcript evidence correlation": "transcript_evidence_binding",
    "transcript evidence reference": "transcript_evidence_binding",
    "transcript evidence tie": "transcript_evidence_binding",

    # Audit Trail Format for Voice
    "audit trail format": "voice_audit_trail_format",
    "voice audit trail format": "voice_audit_trail_format",
    "audit format": "voice_audit_trail_format",
    "audit trail voice format": "voice_audit_trail_format",
    "voice audit format": "voice_audit_trail_format",
    "audit trail schema": "voice_audit_trail_format",
    "audit trail structure": "voice_audit_trail_format",
    "audit trail template": "voice_audit_trail_format",
    "audit trail layout": "voice_audit_trail_format",
    "audit trail specification": "voice_audit_trail_format",

    # Voice Authentication Verification
    "voice authentication verification": "voice_auth_verification",
    "voice authentication": "voice_auth_verification",
    "voice auth verification": "voice_auth_verification",
    "voice auth": "voice_auth_verification",
    "voice verification": "voice_auth_verification",
    "voice identity verification": "voice_auth_verification",
    "voice transcript authentication": "voice_auth_verification",
    "voice transcript verification": "voice_auth_verification",
    "voice transcript auth": "voice_auth_verification",

    # Speaker Verification Logging
    "speaker verification logging": "speaker_verification_logging",
    "speaker verification log": "speaker_verification_logging",
    "speaker log": "speaker_verification_logging",
    "speaker verification": "speaker_verification_logging",
    "speaker identity verification": "speaker_verification_logging",
    "speaker transcript verification": "speaker_verification_logging",
    "speaker transcript log": "speaker_verification_logging",
    "speaker verification audit": "speaker_verification_logging",
    "speaker verification record": "speaker_verification_logging",

    # Conversation Recording Consent
    "conversation recording consent": "recording_consent",
    "recording consent": "recording_consent",
    "voice recording consent": "recording_consent",
    "recording permission": "recording_consent",
    "consent to record": "recording_consent",
    "record consent": "recording_consent",
    "recording authorization": "recording_consent",
    "voice consent": "recording_consent",
    "voice transcript consent": "recording_consent",
    "recording approval": "recording_consent",

    # Retention Policy Enforcement
    "retention policy enforcement": "retention_policy_enforcement",
    "retention enforcement": "retention_policy_enforcement",
    "voice retention policy": "retention_policy_enforcement",
    "voice retention enforcement": "retention_policy_enforcement",
    "transcript retention policy": "retention_policy_enforcement",
    "retention policy": "retention_policy_enforcement",
    "retention rules": "retention_policy_enforcement",
    "retention compliance": "retention_policy_enforcement",
    "retention management": "retention_policy_enforcement",
    "retention policy voice": "retention_policy_enforcement",

    # Voice Data Encryption Requirements
    "voice data encryption requirements": "voice_encryption_requirements",
    "voice encryption requirements": "voice_encryption_requirements",
    "voice data encryption": "voice_encryption_requirements",
    "voice encryption": "voice_encryption_requirements",
    "voice transcript encryption": "voice_encryption_requirements",
    "voice transcript encryption requirements": "voice_encryption_requirements",
    "voice data security": "voice_encryption_requirements",
    "voice transcript security": "voice_encryption_requirements",
    "voice data protection": "voice_encryption_requirements",
    "voice transcript protection": "voice_encryption_requirements",

    # HIPAA Compliance for Voice Transcripts
    "hipaa compliance voice transcripts": "hipaa_compliance_voice",
    "hipaa compliance": "hipaa_compliance_voice",
    "hipaa voice transcript": "hipaa_compliance_voice",
    "hipaa transcript": "hipaa_compliance_voice",
    "hipaa voice": "hipaa_compliance_voice",
    "hipaa transcript compliance": "hipaa_compliance_voice",
    "hipaa voice compliance": "hipaa_compliance_voice",
    "hipaa voice transcript compliance": "hipaa_compliance_voice",
    "hipaa": "hipaa_compliance_voice",
    "hipaa regulations voice": "hipaa_compliance_voice",

    # Attorney-Client Privilege Detection
    "attorney-client privilege detection": "attorney_client_privilege_detection",
    "attorney client privilege detection": "attorney_client_privilege_detection",
    "attorney client privilege": "attorney_client_privilege_detection",
    "attorney privilege detection": "attorney_client_privilege_detection",
    "client privilege detection": "attorney_client_privilege_detection",
    "privilege detection": "attorney_client_privilege_detection",
    "privileged transcript detection": "attorney_client_privilege_detection",
    "privileged voice detection": "attorney_client_privilege_detection",
    "voice privilege detection": "attorney_client_privilege_detection",
    "transcript privilege detection": "attorney_client_privilege_detection",

    # Work Product Doctrine for Voice Transcripts
    "work product doctrine voice transcripts": "work_product_voice",
    "work product doctrine": "work_product_voice",
    "work product voice transcript": "work_product_voice",
    "work product transcript": "work_product_voice",
    "work product voice": "work_product_voice",
    "work product transcript doctrine": "work_product_voice",
    "work product privilege": "work_product_voice",
    "work product detection": "work_product_voice",
    "work product voice detection": "work_product_voice",
    "work product transcript detection": "work_product_voice",

    # Voice Evidence Chain of Custody
    "voice evidence chain of custody": "voice_chain_of_custody",
    "chain of custody voice": "voice_chain_of_custody",
    "voice chain of custody": "voice_chain_of_custody",
    "transcript chain of custody": "voice_chain_of_custody",
    "chain of custody transcript": "voice_chain_of_custody",
    "chain of custody": "voice_chain_of_custody",
    "chain of custody audit": "voice_chain_of_custody",
    "voice transcript chain of custody": "voice_chain_of_custody",
    "voice transcript custody": "voice_chain_of_custody",
    "custody chain voice": "voice_chain_of_custody",

    # Transcript Accuracy Verification
    "transcript accuracy verification": "transcript_accuracy_verification",
    "accuracy verification": "transcript_accuracy_verification",
    "transcript verification": "transcript_accuracy_verification",
    "voice transcript accuracy": "transcript_accuracy_verification",
    "voice transcript verification accuracy": "transcript_accuracy_verification",
    "transcript accuracy": "transcript_accuracy_verification",
    "accuracy check": "transcript_accuracy_verification",
    "accuracy audit": "transcript_accuracy_verification",
    "transcript audit accuracy": "transcript_accuracy_verification",
    "transcript accuracy check": "transcript_accuracy_verification",

    # Redaction Rules for Sensitive Voice Data
    "redaction rules sensitive voice data": "voice_redaction_rules",
    "redaction rules": "voice_redaction_rules",
    "voice redaction rules": "voice_redaction_rules",
    "voice transcript redaction": "voice_redaction_rules",
    "voice redaction": "voice_redaction_rules",
    "transcript redaction rules": "voice_redaction_rules",
    "transcript redaction": "voice_redaction_rules",
    "voice transcript redaction rules": "voice_redaction_rules",
    "voice transcript sensitive data redaction": "voice_redaction_rules",
    "voice transcript redaction policy": "voice_redaction_rules",

    # Voice Data Access Control
    "voice data access control": "voice_access_control",
    "voice access control": "voice_access_control",
    "voice transcript access control": "voice_access_control",
    "transcript access control": "voice_access_control",
    "access control voice": "voice_access_control",
    "access control transcript": "voice_access_control",
    "voice access": "voice_access_control",
    "transcript access": "voice_access_control",
    "voice transcript access": "voice_access_control",
    "voice transcript access policy": "voice_access_control",

    # Voice Session Integrity
    "voice session integrity": "voice_session_integrity",
    "session integrity": "voice_session_integrity",
    "voice transcript session integrity": "voice_session_integrity",
    "transcript session integrity": "voice_session_integrity",
    "voice integrity": "voice_session_integrity",
    "session integrity voice": "voice_session_integrity",
    "voice transcript integrity": "voice_session_integrity",
    "voice session": "voice_session_integrity",
    "transcript session": "voice_session_integrity",
    "voice transcript session": "voice_session_integrity",

    # Tampering Detection in Voice Transcripts
    "tampering detection voice transcripts": "voice_tampering_detection",
    "tampering detection": "voice_tampering_detection",
    "voice tampering detection": "voice_tampering_detection",
    "transcript tampering detection": "voice_tampering_detection",
    "tampering detection transcript": "voice_tampering_detection",
    "tampering detection voice": "voice_tampering_detection",
    "voice transcript tampering": "voice_tampering_detection",
    "voice transcript tampering detection": "voice_tampering_detection",
    "voice tampering": "voice_tampering_detection",
    "transcript tampering": "voice_tampering_detection",

    # Voice Audit Report Generation
    "voice audit report generation": "voice_audit_report_generation",
    "audit report generation": "voice_audit_report_generation",
    "voice transcript audit report": "voice_audit_report_generation",
    "voice audit report": "voice_audit_report_generation",
    "audit report voice": "voice_audit_report_generation",
    "audit report transcript": "voice_audit_report_generation",
    "audit report": "voice_audit_report_generation",
    "voice transcript audit report generation": "voice_audit_report_generation",
    "voice transcript report generation": "voice_audit_report_generation",
    "voice transcript report": "voice_audit_report_generation",

    # Regulatory Compliance Checking
    "regulatory compliance checking": "regulatory_compliance_checking",
    "compliance checking": "regulatory_compliance_checking",
    "regulatory compliance": "regulatory_compliance_checking",
    "compliance check": "regulatory_compliance_checking",
    "compliance audit": "regulatory_compliance_checking",
    "regulatory check": "regulatory_compliance_checking",
    "regulatory audit": "regulatory_compliance_checking",
    "regulatory compliance audit": "regulatory_compliance_checking",
    "voice regulatory compliance": "regulatory_compliance_checking",
    "transcript regulatory compliance": "regulatory_compliance_checking",

    # Voice Transcript Metadata Completeness
    "voice transcript metadata completeness": "voice_metadata_completeness",
    "metadata completeness": "voice_metadata_completeness",
    "voice metadata completeness": "voice_metadata_completeness",
    "transcript metadata completeness": "voice_metadata_completeness",
    "voice transcript metadata": "voice_metadata_completeness",
    "transcript metadata": "voice_metadata_completeness",
    "voice metadata": "voice_metadata_completeness",
    "voice transcript metadata check": "voice_metadata_completeness",
    "voice transcript metadata audit": "voice_metadata_completeness",
    "voice transcript metadata verification": "voice_metadata_completeness",

    # Voice Transcript Exportability
    "voice transcript exportability": "voice_exportability",
    "transcript exportability": "voice_exportability",
    "voice exportability": "voice_exportability",
    "voice transcript export": "voice_exportability",
    "transcript export": "voice_exportability",
    "voice export": "voice_exportability",
    "voice transcript export check": "voice_exportability",
    "voice transcript export audit": "voice_exportability",
    "voice transcript export verification": "voice_exportability",
    "voice transcript export compliance": "voice_exportability",

    # Voice Transcript Session Termination Logging
    "voice transcript session termination logging": "voice_session_termination_logging",
    "session termination logging": "voice_session_termination_logging",
    "voice session termination logging": "voice_session_termination_logging",
    "transcript session termination logging": "voice_session_termination_logging",
    "session termination log": "voice_session_termination_logging",
    "voice session termination log": "voice_session_termination_logging",
    "transcript session termination log": "voice_session_termination_logging",
    "voice transcript session termination log": "voice_session_termination_logging",
    "voice transcript session termination": "voice_session_termination_logging",
    "session termination voice": "voice_session_termination_logging",

    # Voice Transcript Reviewer Accountability
    "voice transcript reviewer accountability": "voice_reviewer_accountability",
    "reviewer accountability": "voice_reviewer_accountability",
    "voice reviewer accountability": "voice_reviewer_accountability",
    "transcript reviewer accountability": "voice_reviewer_accountability",
    "reviewer accountability voice": "voice_reviewer_accountability",
    "reviewer accountability transcript": "voice_reviewer_accountability",
    "voice transcript reviewer": "voice_reviewer_accountability",
    "transcript reviewer": "voice_reviewer_accountability",
    "voice reviewer": "voice_reviewer_accountability",
    "voice transcript reviewer log": "voice_reviewer_accountability",

    # Voice Transcript Compliance Exception Handling
    "voice transcript compliance exception handling": "voice_compliance_exception_handling",
    "compliance exception handling": "voice_compliance_exception_handling",
    "voice compliance exception handling": "voice_compliance_exception_handling",
    "transcript compliance exception handling": "voice_compliance_exception_handling",
    "compliance exception voice": "voice_compliance_exception_handling",
    "compliance exception transcript": "voice_compliance_exception_handling",
    "voice transcript compliance exception": "voice_compliance_exception_handling",
    "voice compliance exception": "voice_compliance_exception_handling",
    "transcript compliance exception": "voice_compliance_exception_handling",
    "voice transcript exception handling": "voice_compliance_exception_handling",

    # Voice Transcript Regulatory Notification Logging
    "voice transcript regulatory notification logging": "voice_regulatory_notification_logging",
    "regulatory notification logging": "voice_regulatory_notification_logging",
    "voice regulatory notification logging": "voice_regulatory_notification_logging",
    "transcript regulatory notification logging": "voice_regulatory_notification_logging",
    "regulatory notification log": "voice_regulatory_notification_logging",
    "voice regulatory notification log": "voice_regulatory_notification_logging",
    "transcript regulatory notification log": "voice_regulatory_notification_logging",
    "voice transcript regulatory notification log": "voice_regulatory_notification_logging",
    "voice transcript regulatory notification": "voice_regulatory_notification_logging",
    "regulatory notification voice": "voice_regulatory_notification_logging",

    # Voice Transcript Compliance Training Logging
    "voice transcript compliance training logging": "voice_compliance_training_logging",
    "compliance training logging": "voice_compliance_training_logging",
    "voice compliance training logging": "voice_compliance_training_logging",
    "transcript compliance training logging": "voice_compliance_training_logging",
    "compliance training log": "voice_compliance_training_logging",
    "voice compliance training log": "voice_compliance_training_logging",
    "transcript compliance training log": "voice_compliance_training_logging",
    "voice transcript compliance training log": "voice_compliance_training_logging",
    "voice transcript compliance training": "voice_compliance_training_logging",
    "compliance training voice": "voice_compliance_training_logging",

    # Voice Transcript System Configuration Logging
    "voice transcript system configuration logging": "voice_system_configuration_logging",
    "system configuration logging": "voice_system_configuration_logging",
    "voice system configuration logging": "voice_system_configuration_logging",
    "transcript system configuration logging": "voice_system_configuration_logging",
    "system configuration log": "voice_system_configuration_logging",
    "voice system configuration log": "voice_system_configuration_logging",
    "transcript system configuration log": "voice_system_configuration_logging",
    "voice transcript system configuration log": "voice_system_configuration_logging",
    "voice transcript system configuration": "voice_system_configuration_logging",
    "system configuration voice": "voice_system_configuration_logging",

    # Voice Transcript Incident Response Logging
    "voice transcript incident response logging": "voice_incident_response_logging",
    "incident response logging": "voice_incident_response_logging",
    "voice incident response logging": "voice_incident_response_logging",
    "transcript incident response logging": "voice_incident_response_logging",
    "incident response log": "voice_incident_response_logging",
    "voice incident response log": "voice_incident_response_logging",
    "transcript incident response log": "voice_incident_response_logging",
    "voice transcript incident response log": "voice_incident_response_logging",
    "voice transcript incident response": "voice_incident_response_logging",
    "incident response voice": "voice_incident_response_logging",
}

def _compute_map_hash() -> str:
    items = sorted(SEMANTIC_MAP.items())
    map_str = "".join([f"{k}:{v};" for k, v in items])
    meta_str = f"{SEMANTIC_MAP_VERSION}:{SEMANTIC_MAP_AUTHOR}:{SEMANTIC_MAP_ENGINE}:{_EXPECTED_ENTRY_COUNT}"
    full_str = map_str + meta_str
    return hashlib.sha256(full_str.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> Dict[str, Any]:
    actual_count = len(SEMANTIC_MAP)
    actual_hash = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (actual_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "valid" if is_valid else "invalid",
        "entries": actual_count,
        "hash": actual_hash,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    term_clean = term.lower().strip()
    term_clean = re.sub(r"[^\w\s\-]", "", term_clean)
    return SEMANTIC_MAP.get(term_clean, term_clean)

def get_related_terms(term: str) -> List[str]:
    norm = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == norm]
    return related

def get_all_mappings() -> Dict[str, str]:
    return dict(SEMANTIC_MAP)