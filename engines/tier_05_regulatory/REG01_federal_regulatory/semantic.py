import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "REG01 Engine Team"
SEMANTIC_MAP_ENGINE = "REG01_federal_regulatory"

SEMANTIC_MAP = {
    # APA Notice and Comment Rulemaking
    "notice and comment": "apa_notice_and_comment",
    "notice-and-comment": "apa_notice_and_comment",
    "notice comment": "apa_notice_and_comment",
    "notice of proposed rulemaking": "apa_notice_and_comment",
    "nprm": "apa_notice_and_comment",
    "proposed rule": "apa_notice_and_comment",
    "public comment": "apa_notice_and_comment",
    "comment period": "apa_notice_and_comment",
    "rulemaking docket": "apa_notice_and_comment",
    "rulemaking record": "apa_notice_and_comment",
    "final rule": "apa_notice_and_comment",
    "final rulemaking": "apa_notice_and_comment",
    "informal rulemaking": "apa_notice_and_comment",
    "section 553": "apa_notice_and_comment",
    "5 usc 553": "apa_notice_and_comment",
    "administrative procedure act section 553": "apa_notice_and_comment",
    "apa 553": "apa_notice_and_comment",
    "rulemaking process": "apa_notice_and_comment",
    "public participation": "apa_notice_and_comment",
    "public input": "apa_notice_and_comment",
    "public hearing": "apa_notice_and_comment",
    "public meeting": "apa_notice_and_comment",
    "regulations.gov": "apa_notice_and_comment",
    "e-rulemaking": "apa_notice_and_comment",
    "electronic rulemaking": "apa_notice_and_comment",
    "federal register": "apa_notice_and_comment",
    "fr notice": "apa_notice_and_comment",
    "rule publication": "apa_notice_and_comment",
    "rule notice": "apa_notice_and_comment",
    "agency rulemaking": "apa_notice_and_comment",
    "agency proposal": "apa_notice_and_comment",
    "agency comment": "apa_notice_and_comment",
    "agency response to comments": "apa_notice_and_comment",
    "comment submission": "apa_notice_and_comment",
    "public docket": "apa_notice_and_comment",
    # Chevron Deference Framework
    "chevron deference": "chevron_deference",
    "chevron doctrine": "chevron_deference",
    "chevron step one": "chevron_deference",
    "chevron step two": "chevron_deference",
    "chevron analysis": "chevron_deference",
    "chevron test": "chevron_deference",
    "chevron framework": "chevron_deference",
    "chevron usa": "chevron_deference",
    "chevron v nrdc": "chevron_deference",
    "chevron case": "chevron_deference",
    "agency statutory interpretation": "chevron_deference",
    "judicial deference": "chevron_deference",
    "reasonable interpretation": "chevron_deference",
    "ambiguous statute": "chevron_deference",
    "agency interpretation": "chevron_deference",
    "step one": "chevron_deference",
    "step two": "chevron_deference",
    "chevron": "chevron_deference",
    "chevron review": "chevron_deference",
    "chevron standard": "chevron_deference",
    "chevron two-step": "chevron_deference",
    "chevron two step": "chevron_deference",
    "chevron deference doctrine": "chevron_deference",
    # Auer/Kisor Deference to Regulatory Interpretation
    "auer deference": "auer_kisor_deference",
    "kisor deference": "auer_kisor_deference",
    "auer doctrine": "auer_kisor_deference",
    "kisor doctrine": "auer_kisor_deference",
    "auer v robbins": "auer_kisor_deference",
    "kisor v wilkie": "auer_kisor_deference",
    "regulatory interpretation": "auer_kisor_deference",
    "agency regulatory interpretation": "auer_kisor_deference",
    "regulation ambiguity": "auer_kisor_deference",
    "agency interpretation of regulation": "auer_kisor_deference",
    "judicial deference to agency": "auer_kisor_deference",
    "agency interpretation of own regulation": "auer_kisor_deference",
    "agency's own regulation": "auer_kisor_deference",
    "regulatory deference": "auer_kisor_deference",
    "auer": "auer_kisor_deference",
    "kisor": "auer_kisor_deference",
    "auer/kisor": "auer_kisor_deference",
    "auer-kisor": "auer_kisor_deference",
    "auer deference doctrine": "auer_kisor_deference",
    "kisor deference doctrine": "auer_kisor_deference",
    # Major Questions Doctrine
    "major questions doctrine": "major_questions_doctrine",
    "major questions": "major_questions_doctrine",
    "extraordinary cases": "major_questions_doctrine",
    "economic significance": "major_questions_doctrine",
    "agency authority": "major_questions_doctrine",
    "statutory ambiguity": "major_questions_doctrine",
    "congressional intent": "major_questions_doctrine",
    "major policy question": "major_questions_doctrine",
    "major question": "major_questions_doctrine",
    "west virginia v epa": "major_questions_doctrine",
    "major rules": "major_questions_doctrine",
    "significant regulatory action": "major_questions_doctrine",
    "significant questions": "major_questions_doctrine",
    "major regulatory action": "major_questions_doctrine",
    "nondelegation principle": "major_questions_doctrine",
    "nondelegation doctrine": "major_questions_doctrine",
    # Arbitrary and Capricious Review - APA Section 706
    "arbitrary and capricious": "arbitrary_and_capricious_review",
    "arbitrary & capricious": "arbitrary_and_capricious_review",
    "arbitrary": "arbitrary_and_capricious_review",
    "capricious": "arbitrary_and_capricious_review",
    "arbitrary or capricious": "arbitrary_and_capricious_review",
    "arbitrary and capricious review": "arbitrary_and_capricious_review",
    "apa section 706": "arbitrary_and_capricious_review",
    "section 706": "arbitrary_and_capricious_review",
    "5 usc 706": "arbitrary_and_capricious_review",
    "judicial review": "arbitrary_and_capricious_review",
    "agency action review": "arbitrary_and_capricious_review",
    "agency decision review": "arbitrary_and_capricious_review",
    "hard look review": "arbitrary_and_capricious_review",
    "reasoned decisionmaking": "arbitrary_and_capricious_review",
    "reasoned explanation": "arbitrary_and_capricious_review",
    "agency rationale": "arbitrary_and_capricious_review",
    "rational basis": "arbitrary_and_capricious_review",
    "agency justification": "arbitrary_and_capricious_review",
    "arbitrary capricious": "arbitrary_and_capricious_review",
    "arbitary and capricious": "arbitrary_and_capricious_review",
    "arbitary": "arbitrary_and_capricious_review",
    # Executive Order 12866 and OIRA Review
    "executive order 12866": "eo_12866_oira_review",
    "eo 12866": "eo_12866_oira_review",
    "e.o. 12866": "eo_12866_oira_review",
    "oira review": "eo_12866_oira_review",
    "office of information and regulatory affairs": "eo_12866_oira_review",
    "oira": "eo_12866_oira_review",
    "regulatory review": "eo_12866_oira_review",
    "significant regulatory action": "eo_12866_oira_review",
    "significant rule": "eo_12866_oira_review",
    "regulatory impact analysis": "eo_12866_oira_review",
    "ria": "eo_12866_oira_review",
    "cost benefit analysis": "eo_12866_oira_review",
    "cost-benefit analysis": "eo_12866_oira_review",
    "benefit cost analysis": "eo_12866_oira_review",
    "benefit-cost analysis": "eo_12866_oira_review",
    "regulatory planning": "eo_12866_oira_review",
    "regulatory agenda": "eo_12866_oira_review",
    "unified agenda": "eo_12866_oira_review",
    "regulatory priorities": "eo_12866_oira_review",
    "presidential review": "eo_12866_oira_review",
    "white house review": "eo_12866_oira_review",
    "oira clearance": "eo_12866_oira_review",
    "oira submission": "eo_12866_oira_review",
    "oira process": "eo_12866_oira_review",
    # Regulatory Flexibility Act - Small Business Impact
    "regulatory flexibility act": "regflexact_small_business",
    "reg flex act": "regflexact_small_business",
    "rfa": "regflexact_small_business",
    "small business impact": "regflexact_small_business",
    "small entity impact": "regflexact_small_business",
    "initial regulatory flexibility analysis": "regflexact_small_business",
    "irfa": "regflexact_small_business",
    "final regulatory flexibility analysis": "regflexact_small_business",
    "frfa": "regflexact_small_business",
    "small business": "regflexact_small_business",
    "small entities": "regflexact_small_business",
    "small government": "regflexact_small_business",
    "small organization": "regflexact_small_business",
    "small governmental jurisdiction": "regflexact_small_business",
    "regulatory flexibility": "regflexact_small_business",
    "regflex": "regflexact_small_business",
    "reg flex": "regflexact_small_business",
    "regflex analysis": "regflexact_small_business",
    "reg flex analysis": "regflexact_small_business",
    # Congressional Review Act
    "congressional review act": "congressional_review_act",
    "cra": "congressional_review_act",
    "joint resolution of disapproval": "congressional_review_act",
    "resolution of disapproval": "congressional_review_act",
    "congressional disapproval": "congressional_review_act",
    "major rule": "congressional_review_act",
    "submission to congress": "congressional_review_act",
    "congressional oversight": "congressional_review_act",
    "rule nullification": "congressional_review_act",
    "congressional veto": "congressional_review_act",
    "disapproval resolution": "congressional_review_act",
    "rule effective date": "congressional_review_act",
    "report to congress": "congressional_review_act",
    # Administrative Exhaustion Requirement
    "administrative exhaustion": "administrative_exhaustion",
    "exhaustion of administrative remedies": "administrative_exhaustion",
    "exhaustion requirement": "administrative_exhaustion",
    "exhaustion doctrine": "administrative_exhaustion",
    "administrative remedies": "administrative_exhaustion",
    "exhaust administrative remedies": "administrative_exhaustion",
    "remedy exhaustion": "administrative_exhaustion",
    "exhaustion": "administrative_exhaustion",
    "failure to exhaust": "administrative_exhaustion",
    "failure to exhaust administrative remedies": "administrative_exhaustion",
    "premature litigation": "administrative_exhaustion",
    "ripeness": "administrative_exhaustion",
    # Enforcement Discretion and Prosecutorial Discretion
    "enforcement discretion": "enforcement_prosecutorial_discretion",
    "prosecutorial discretion": "enforcement_prosecutorial_discretion",
    "agency discretion": "enforcement_prosecutorial_discretion",
    "selective enforcement": "enforcement_prosecutorial_discretion",
    "agency enforcement": "enforcement_prosecutorial_discretion",
    "nonenforcement": "enforcement_prosecutorial_discretion",
    "non-enforcement": "enforcement_prosecutorial_discretion",
    "enforcement priorities": "enforcement_prosecutorial_discretion",
    "enforcement policy": "enforcement_prosecutorial_discretion",
    "enforcement action": "enforcement_prosecutorial_discretion",
    "enforcement authority": "enforcement_prosecutorial_discretion",
    "nonprosecution": "enforcement_prosecutorial_discretion",
    "non-prosecution": "enforcement_prosecutorial_discretion",
    "declination": "enforcement_prosecutorial_discretion",
    "decline to prosecute": "enforcement_prosecutorial_discretion",
    # Consent Decrees and Settlements
    "consent decree": "consent_decree_settlement",
    "consent decrees": "consent_decree_settlement",
    "settlement agreement": "consent_decree_settlement",
    "settlement": "consent_decree_settlement",
    "judicial settlement": "consent_decree_settlement",
    "agency settlement": "consent_decree_settlement",
    "court-approved settlement": "consent_decree_settlement",
    "consent judgment": "consent_decree_settlement",
    "consent order": "consent_decree_settlement",
    "decree": "consent_decree_settlement",
    "settlement order": "consent_decree_settlement",
    "enforcement settlement": "consent_decree_settlement",
    # Preemption of State Law by Federal Regulation
    "preemption": "federal_preemption",
    "federal preemption": "federal_preemption",
    "preemption of state law": "federal_preemption",
    "preempt state law": "federal_preemption",
    "supremacy clause": "federal_preemption",
    "express preemption": "federal_preemption",
    "implied preemption": "federal_preemption",
    "conflict preemption": "federal_preemption",
    "field preemption": "federal_preemption",
    "obstacle preemption": "federal_preemption",
    "state law preempted": "federal_preemption",
    "state law invalid": "federal_preemption",
    "preemptive effect": "federal_preemption",
    "federal supremacy": "federal_preemption",
    "federal override": "federal_preemption",
    "state-federal conflict": "federal_preemption",
    # OMB Circular A-4 Cost-Benefit Analysis
    "omb circular a-4": "omb_a4_cost_benefit",
    "omb a-4": "omb_a4_cost_benefit",
    "circular a-4": "omb_a4_cost_benefit",
    "omb circular a4": "omb_a4_cost_benefit",
    "omb a4": "omb_a4_cost_benefit",
    "a-4": "omb_a4_cost_benefit",
    "a4": "omb_a4_cost_benefit",
    "omb guidance": "omb_a4_cost_benefit",
    "omb analysis": "omb_a4_cost_benefit",
    "omb cost benefit": "omb_a4_cost_benefit",
    "omb cost-benefit": "omb_a4_cost_benefit",
    "omb benefit cost": "omb_a4_cost_benefit",
    "omb benefit-cost": "omb_a4_cost_benefit",
    "omb regulatory analysis": "omb_a4_cost_benefit",
    "omb ria": "omb_a4_cost_benefit",
    "omb": "omb_a4_cost_benefit",
    # Unfunded Mandates Reform Act
    "unfunded mandates reform act": "umra",
    "umra": "umra",
    "unfunded mandate": "umra",
    "unfunded mandates": "umra",
    "mandate reform": "umra",
    "state unfunded mandate": "umra",
    "local unfunded mandate": "umra",
    "federal mandate": "umra",
    "mandate analysis": "umra",
    "mandate cost": "umra",
    "mandate impact": "umra",
    "mandate review": "umra",
    # Paperwork Reduction Act
    "paperwork reduction act": "pra",
    "pra": "pra",
    "information collection": "pra",
    "information collection request": "pra",
    "icr": "pra",
    "paperwork burden": "pra",
    "burden reduction": "pra",
    "omb approval": "pra",
    "omb control number": "pra",
    "recordkeeping": "pra",
    "record keeping": "pra",
    "reporting burden": "pra",
    "paperwork": "pra",
    # Federal Advisory Committee Act
    "federal advisory committee act": "faca",
    "faca": "faca",
    "advisory committee": "faca",
    "advisory committees": "faca",
    "committee charter": "faca",
    "committee membership": "faca",
    "committee transparency": "faca",
    "committee meeting": "faca",
    "committee public": "faca",
    "committee records": "faca",
    "advisory panel": "faca",
    "advisory board": "faca",
    # Negotiated Rulemaking Act
    "negotiated rulemaking act": "negotiated_rulemaking",
    "negotiated rulemaking": "negotiated_rulemaking",
    "reg neg": "negotiated_rulemaking",
    "reg-neg": "negotiated_rulemaking",
    "regneg": "negotiated_rulemaking",
    "negotiated rule": "negotiated_rulemaking",
    "consensus rulemaking": "negotiated_rulemaking",
    "consensus process": "negotiated_rulemaking",
    "stakeholder negotiation": "negotiated_rulemaking",
    "stakeholder consensus": "negotiated_rulemaking",
    "negotiated agreement": "negotiated_rulemaking",
    # Data Quality Act and Information Quality
    "data quality act": "data_quality_information_quality",
    "information quality act": "data_quality_information_quality",
    "dqa": "data_quality_information_quality",
    "iq act": "data_quality_information_quality",
    "information quality": "data_quality_information_quality",
    "data quality": "data_quality_information_quality",
    "omb information quality": "data_quality_information_quality",
    "omb data quality": "data_quality_information_quality",
    "quality guidelines": "data_quality_information_quality",
    "quality standards": "data_quality_information_quality",
    "data integrity": "data_quality_information_quality",
    "information integrity": "data_quality_information_quality",
    "quality correction": "data_quality_information_quality",
    "correction request": "data_quality_information_quality",
    "information correction": "data_quality_information_quality",
    # Regulatory Lookback and Retrospective Review
    "regulatory lookback": "regulatory_lookback",
    "retrospective review": "regulatory_lookback",
    "lookback review": "regulatory_lookback",
    "regulatory retrospective review": "regulatory_lookback",
    "regulatory review": "regulatory_lookback",
    "regulation review": "regulatory_lookback",
    "review of existing rules": "regulatory_lookback",
    "review of existing regulations": "regulatory_lookback",
    "regulation lookback": "regulatory_lookback",
    "rule lookback": "regulatory_lookback",
    "regulatory modernization": "regulatory_lookback",
    "regulatory reform": "regulatory_lookback",
    "regulation reform": "regulatory_lookback",
    "regulatory burden reduction": "regulatory_lookback",
    "burden reduction": "regulatory_lookback",
    "regulatory streamlining": "regulatory_lookback",
    # Interim Final Rules and Good Cause Exception
    "interim final rule": "interim_final_good_cause",
    "interim final rules": "interim_final_good_cause",
    "interim rule": "interim_final_good_cause",
    "good cause exception": "interim_final_good_cause",
    "good cause": "interim_final_good_cause",
    "good cause finding": "interim_final_good_cause",
    "immediate effectiveness": "interim_final_good_cause",
    "immediate effect": "interim_final_good_cause",
    "emergency rulemaking": "interim_final_good_cause",
    "emergency rule": "interim_final_good_cause",
    "expedited rulemaking": "interim_final_good_cause",
    "expedited process": "interim_final_good_cause",
    "urgent rulemaking": "interim_final_good_cause",
    "urgent rule": "interim_final_good_cause",
    "interim rulemaking": "interim_final_good_cause",
    # Direct Final Rules
    "direct final rule": "direct_final_rule",
    "direct final rules": "direct_final_rule",
    "direct final": "direct_final_rule",
    "direct final rulemaking": "direct_final_rule",
    "direct rule": "direct_final_rule",
    "noncontroversial rule": "direct_final_rule",
    "non-controversial rule": "direct_final_rule",
    "noncontroversial": "direct_final_rule",
    "non-controversial": "direct_final_rule",
    "consensus rule": "direct_final_rule",
    "expedited final rule": "direct_final_rule",
    "expedited final": "direct_final_rule",
    # Guidance Documents and Interpretive Rules
    "guidance document": "guidance_interpretive_rule",
    "guidance documents": "guidance_interpretive_rule",
    "guidance": "guidance_interpretive_rule",
    "interpretive rule": "guidance_interpretive_rule",
    "interpretive rules": "guidance_interpretive_rule",
    "policy statement": "guidance_interpretive_rule",
    "policy guidance": "guidance_interpretive_rule",
    "agency guidance": "guidance_interpretive_rule",
    "nonbinding guidance": "guidance_interpretive_rule",
    "non-binding guidance": "guidance_interpretive_rule",
    "subregulatory guidance": "guidance_interpretive_rule",
    "sub-regulatory guidance": "guidance_interpretive_rule",
    "compliance guidance": "guidance_interpretive_rule",
    "informal guidance": "guidance_interpretive_rule",
    "advisory opinion": "guidance_interpretive_rule",
    "staff guidance": "guidance_interpretive_rule",
    "faq": "guidance_interpretive_rule",
    "frequently asked questions": "guidance_interpretive_rule",
    # Scientific and Technical Rulemaking Standards
    "scientific standards": "scientific_technical_standards",
    "technical standards": "scientific_technical_standards",
    "science-based rulemaking": "scientific_technical_standards",
    "science based rulemaking": "scientific_technical_standards",
    "scientific evidence": "scientific_technical_standards",
    "technical evidence": "scientific_technical_standards",
    "peer review": "scientific_technical_standards",
    "peer-reviewed science": "scientific_technical_standards",
    "peer reviewed science": "scientific_technical_standards",
    "scientific integrity": "scientific_technical_standards",
    "technical integrity": "scientific_technical_standards",
    "best available science": "scientific_technical_standards",
    "sound science": "scientific_technical_standards",
    "scientific methodology": "scientific_technical_standards",
    "technical methodology": "scientific_technical_standards",
    "scientific data": "scientific_technical_standards",
    "technical data": "scientific_technical_standards",
    "data standards": "scientific_technical_standards",
    "scientific analysis": "scientific_technical_standards",
    "technical analysis": "scientific_technical_standards",
    # Environmental Justice in Rulemaking
    "environmental justice": "environmental_justice_rulemaking",
    "ej": "environmental_justice_rulemaking",
    "environmental equity": "environmental_justice_rulemaking",
    "environmental disparities": "environmental_justice_rulemaking",
    "environmental justice analysis": "environmental_justice_rulemaking",
    "ej analysis": "environmental_justice_rulemaking",
    "ej review": "environmental_justice_rulemaking",
    "environmental justice review": "environmental_justice_rulemaking",
    "environmental impacts": "environmental_justice_rulemaking",
    "community impacts": "environmental_justice_rulemaking",
    "disparate impact": "environmental_justice_rulemaking",
    "vulnerable populations": "environmental_justice_rulemaking",
    "overburdened communities": "environmental_justice_rulemaking",
    "environmental racism": "environmental_justice_rulemaking",
    "environmental equity analysis": "environmental_justice_rulemaking",
    # Regulatory Takings and Fifth Amendment
    "regulatory taking": "regulatory_takings_fifth_amendment",
    "regulatory takings": "regulatory_takings_fifth_amendment",
    "takings": "regulatory_takings_fifth_amendment",
    "fifth amendment": "regulatory_takings_fifth_amendment",
    "takings clause": "regulatory_takings_fifth_amendment",
    "just compensation": "regulatory_takings_fifth_amendment",
    "inverse condemnation": "regulatory_takings_fifth_amendment",
    "physical taking": "regulatory_takings_fifth_amendment",
    "per se taking": "regulatory_takings_fifth_amendment",
    "partial taking": "regulatory_takings_fifth_amendment",
    "property rights": "regulatory_takings_fifth_amendment",
    "exaction": "regulatory_takings_fifth_amendment",
    "land use regulation": "regulatory_takings_fifth_amendment",
    "lucas v south carolina": "regulatory_takings_fifth_amendment",
    "penn central": "regulatory_takings_fifth_amendment",
    "regulatory exaction": "regulatory_takings_fifth_amendment",
    # Additional misspellings, abbreviations, and related terms
    "arbitary capricious": "arbitrary_and_capricious_review",
    "arbitary & capricious": "arbitrary_and_capricious_review",
    "arbitary or capricious": "arbitrary_and_capricious_review",
    "arbitary capricious review": "arbitrary_and_capricious_review",
    "arbitary and capricous": "arbitrary_and_capricious_review",
    "arbitary": "arbitrary_and_capricious_review",
    "capricous": "arbitrary_and_capricious_review",
    "regflex analysis": "regflexact_small_business",
    "regflex": "regflexact_small_business",
    "reg flex": "regflexact_small_business",
    "omb circ a-4": "omb_a4_cost_benefit",
    "omb circ a4": "omb_a4_cost_benefit",
    "omb circ": "omb_a4_cost_benefit",
    "omb circ a": "omb_a4_cost_benefit",
    "omb circ a4": "omb_a4_cost_benefit",
    "omb circ a-4": "omb_a4_cost_benefit",
    "omb circ a 4": "omb_a4_cost_benefit",
    "omb circ a-4 analysis": "omb_a4_cost_benefit",
    "omb circ a-4 guidance": "omb_a4_cost_benefit",
    "omb circ a-4 cost benefit": "omb_a4_cost_benefit",
    "omb circ a-4 cost-benefit": "omb_a4_cost_benefit",
    "omb circ a-4 benefit cost": "omb_a4_cost_benefit",
    "omb circ a-4 benefit-cost": "omb_a4_cost_benefit",
    "omb circ a-4 regulatory analysis": "omb_a4_cost_benefit",
    "omb circ a-4 ria": "omb_a4_cost_benefit",
    "omb circ a-4 omb": "omb_a4_cost_benefit",
    "omb circ a-4": "omb_a4_cost_benefit",
    "omb circ a-4 cost": "omb_a4_cost_benefit",
    "omb circ a-4 benefit": "omb_a4_cost_benefit",
    "omb circ a-4 analysis": "omb_a4_cost_benefit",
    "omb circ a-4 guidance": "omb_a4_cost_benefit",
    "omb circ a-4 cost benefit": "omb_a4_cost_benefit",
    "omb circ a-4 cost-benefit": "omb_a4_cost_benefit",
    "omb circ a-4 benefit cost": "omb_a4_cost_benefit",
    "omb circ a-4 benefit-cost": "omb_a4_cost_benefit",
    "omb circ a-4 regulatory analysis": "omb_a4_cost_benefit",
    "omb circ a-4 ria": "omb_a4_cost_benefit",
    "omb circ a-4 omb": "omb_a4_cost_benefit",
    "omb circ a-4": "omb_a4_cost_benefit",
    "omb circ a-4 cost": "omb_a4_cost_benefit",
    "omb circ a-4 benefit": "omb_a4_cost_benefit",
    "omb circ a-4 analysis": "omb_a4_cost_benefit",
    "omb circ a-4 guidance": "omb_a4_cost_benefit",
    "omb circ a-4 cost benefit": "omb_a4_cost_benefit",
    "omb circ a-4 cost-benefit": "omb_a4_cost_benefit",
    "omb circ a-4 benefit cost": "omb_a4_cost_benefit",
    "omb circ a-4 benefit-cost": "omb_a4_cost_benefit",
    "omb circ a-4 regulatory analysis": "omb_a4_cost_benefit",
    "omb circ a-4 ria": "omb_a4_cost_benefit",
    "omb circ a-4 omb": "omb_a4_cost_benefit",
    "omb circ a-4": "omb_a4_cost_benefit",
    # Misspellings and variants for "negotiated rulemaking"
    "negotiated rule makings": "negotiated_rulemaking",
    "negotiated rulemakings": "negotiated_rulemaking",
    "negotiated rules": "negotiated_rulemaking",
    "negotiated rulemak": "negotiated_rulemaking",
    "negotiated rulemakings act": "negotiated_rulemaking",
    "reg neg act": "negotiated_rulemaking",
    "reg-neg act": "negotiated_rulemaking",
    "regneg act": "negotiated_rulemaking",
    # Misspellings for "arbitrary and capricious"
    "arbitary capricous": "arbitrary_and_capricious_review",
    "arbitary and capricous": "arbitrary_and_capricious_review",
    "arbitary capricious review": "arbitrary_and_capricious_review",
    "arbitary capricious": "arbitrary_and_capricious_review",
    "arbitary": "arbitrary_and_capricious_review",
    "capricous": "arbitrary_and_capricious_review",
    # Misspellings for "regulatory takings"
    "regulatory takeings": "regulatory_takings_fifth_amendment",
    "regulatory takin": "regulatory_takings_fifth_amendment",
    "regulatory takings clause": "regulatory_takings_fifth_amendment",
    "reg takings": "regulatory_takings_fifth_amendment",
    "takings clause": "regulatory_takings_fifth_amendment",
    # Misspellings for "environmental justice"
    "env justice": "environmental_justice_rulemaking",
    "environmental justic": "environmental_justice_rulemaking",
    "environmental justices": "environmental_justice_rulemaking",
    "enviro justice": "environmental_justice_rulemaking",
    "environmental eq": "environmental_justice_rulemaking",
    # Misspellings for "chevron deference"
    "cheveron deference": "chevron_deference",
    "cheveron doctrine": "chevron_deference",
    "cheveron": "chevron_deference",
    "cheveron test": "chevron_deference",
    "chevron deferance": "chevron_deference",
    # Misspellings for "major questions doctrine"
    "major question doctrine": "major_questions_doctrine",
    "major questions doctine": "major_questions_doctrine",
    "major question doctine": "major_questions_doctrine",
    "major questions doctirne": "major_questions_doctrine",
    # Misspellings for "regulatory flexibility act"
    "regulatory flexability act": "regflexact_small_business",
    "regulatory flexiblity act": "regflexact_small_business",
    "regulatory flex act": "regflexact_small_business",
    "reg flexiblity act": "regflexact_small_business",
    "reg flexability act": "regflexact_small_business",
    "reg flexiblity": "regflexact_small_business",
    "reg flexability": "regflexact_small_business",
    # Misspellings for "omb circular a-4"
    "omb circular a4": "omb_a4_cost_benefit",
    "omb circ a4": "omb_a4_cost_benefit",
    "omb circ a-4": "omb_a4_cost_benefit",
    "omb circ a 4": "omb_a4_cost_benefit",
    # Misspellings for "paperwork reduction act"
    "paperwork reduction": "pra",
    "paperwork act": "pra",
    "paperwork reduction act of 1980": "pra",
    "paperwork reduction act of 1995": "pra",
    "paperwork reduction act 1980": "pra",
    "paperwork reduction act 1995": "pra",
    # Misspellings for "federal advisory committee act"
    "federal advisory act": "faca",
    "federal advisory committee": "faca",
    "advisory act": "faca",
    # Misspellings for "data quality act"
    "data quality": "data_quality_information_quality",
    "information quality": "data_quality_information_quality",
    "data qualtiy act": "data_quality_information_quality",
    "data qualtiy": "data_quality_information_quality",
    "information qualtiy": "data_quality_information_quality",
    # Misspellings for "regulatory lookback"
    "regulatory look back": "regulatory_lookback",
    "reg lookback": "regulatory_lookback",
    "reg look back": "regulatory_lookback",
    "regulatory look-back": "regulatory_lookback",
    "reg look-back": "regulatory_lookback",
    # Misspellings for "interim final rule"
    "interim-final rule": "interim_final_good_cause",
    "interim-final rules": "interim_final_good_cause",
    "interim-final": "interim_final_good_cause",
    # Misspellings for "direct final rule"
    "direct-final rule": "direct_final_rule",
    "direct-final rules": "direct_final_rule",
    "direct-final": "direct_final_rule",
    # Misspellings for "guidance document"
    "guidence document": "guidance_interpretive_rule",
    "guidence documents": "guidance_interpretive_rule",
    "guidence": "guidance_interpretive_rule",
    "interpretative rule": "guidance_interpretive_rule",
    "interpretative rules": "guidance_interpretive_rule",
    # Misspellings for "scientific standards"
    "scientific standard": "scientific_technical_standards",
    "technical standard": "scientific_technical_standards",
    "science based": "scientific_technical_standards",
    "science-based": "scientific_technical_standards",
    "scientific evidance": "scientific_technical_standards",
    "technical evidance": "scientific_technical_standards",
    # Misspellings for "enforcement discretion"
    "enforcment discretion": "enforcement_prosecutorial_discretion",
    "enforcment": "enforcement_prosecutorial_discretion",
    "prosecutorial discresion": "enforcement_prosecutorial_discretion",
    "enforcement discresion": "enforcement_prosecutorial_discretion",
    # Misspellings for "consent decree"
    "consent decre": "consent_decree_settlement",
    "consent decrree": "consent_decree_settlement",
    "consent decrees": "consent_decree_settlement",
    "consent decrrees": "consent_decree_settlement",
    "consent decrre": "consent_decree_settlement",
    # Misspellings for "preemption"
    "pre-emption": "federal_preemption",
    "pre emption": "federal_preemption",
    "preemtion": "federal_preemption",
    "pre emt": "federal_preemption",
    "pre empt": "federal_preemption",
    # Misspellings for "unfunded mandates reform act"
    "unfunded mandates reform": "umra",
    "unfunded mandate reform": "umra",
    "unfunded mandates act": "umra",
    "unfunded mandate act": "umra",
    "umra act": "umra",
    # Misspellings for "congressional review act"
    "congressional review": "congressional_review_act",
    "congress review act": "congressional_review_act",
    "congress review": "congressional_review_act",
    "congressional act": "congressional_review_act",
    # Misspellings for "administrative exhaustion"
    "administrative exaustion": "administrative_exhaustion",
    "administrative exhuastion": "administrative_exhaustion",
    "administrative exaustion requirement": "administrative_exhaustion",
    "administrative exhuastion requirement": "administrative_exhaustion",
    "exaustion": "administrative_exhaustion",
    "exhuastion": "administrative_exhaustion",
    "exaustion of administrative remedies": "administrative_exhaustion",
    "exhuastion of administrative remedies": "administrative_exhaustion",
    # Misspellings for "omb"
    "omb circular": "omb_a4_cost_benefit",
    "omb circ": "omb_a4_cost_benefit",
    # Misspellings for "regulatory planning"
    "regulatory plan": "eo_12866_oira_review",
    "reg plan": "eo_12866_oira_review",
    # Misspellings for "agency statutory interpretation"
    "agency statutory interpret": "chevron_deference",
    "agency statutory interpetation": "chevron_deference",
    "agency statutory interpet": "chevron_deference",
    # Misspellings for "agency regulatory interpretation"
    "agency regulatory interpret": "auer_kisor_deference",
    "agency regulatory interpetation": "auer_kisor_deference",
    "agency regulatory interpet": "auer_kisor_deference",
    # Misspellings for "regulatory impact analysis"
    "regulatory impact anlaysis": "eo_12866_oira_review",
    "regulatory impact analaysis": "eo_12866_oira_review",
    "regulatory impact analsys": "eo_12866_oira_review",
    # Misspellings for "cost benefit analysis"
    "cost benfit analysis": "eo_12866_oira_review",
    "cost benfit anlaysis": "eo_12866_oira_review",
    "cost benfit analaysis": "eo_12866_oira_review",
    "cost benfit analsys": "eo_12866_oira_review",
    # Misspellings for "benefit cost analysis"
    "benfit cost analysis": "eo_12866_oira_review",
    "benfit cost anlaysis": "eo_12866_oira_review",
    "benfit cost analaysis": "eo_12866_oira_review",
    "benfit cost analsys": "eo_12866_oira_review",
    # Misspellings for "regulatory priorities"
    "regulatory priority": "eo_12866_oira_review",
    "reg priority": "eo_12866_oira_review",
    # Misspellings for "regulatory agenda"
    "regulatory aganda": "eo_12866_oira_review",
    "regulatory agend": "eo_12866_oira_review",
    "reg aganda": "eo_12866_oira_review",
    "reg agend": "eo_12866_oira_review",
    # Misspellings for "regulatory burden reduction"
    "regulatory burden": "regulatory_lookback",
    "reg burden": "regulatory_lookback",
    # Misspellings for "agency enforcement"
    "agency enforcment": "enforcement_prosecutorial_discretion",
    # Misspellings for "agency discretion"
    "agency discresion": "enforcement_prosecutorial_discretion",
    # Misspellings for "agency action review"
    "agency action revie": "arbitrary_and_capricious_review",
    "agency action reviw": "arbitrary_and_capricious_review",
    # Misspellings for "agency decision review"
    "agency decision revie": "arbitrary_and_capricious_review",
    "agency decision reviw": "arbitrary_and_capricious_review",
    # Misspellings for "agency proposal"
    "agency propsoal": "apa_notice_and_comment",
    # Misspellings for "agency comment"
    "agency commment": "apa_notice_and_comment",
    # Misspellings for "agency response to comments"
    "agency response to commments": "apa_notice_and_comment",
    # Misspellings for "public comment"
    "public commment": "apa_notice_and_comment",
    # Misspellings for "public input"
    "public inpt": "apa_notice_and_comment",
    # Misspellings for "public hearing"
    "public heairng": "apa_notice_and_comment",
    # Misspellings for "public meeting"
    "public meetng": "apa_notice_and_comment",
    # Misspellings for "comment period"
    "comment perod": "apa_notice_and_comment",
    # Misspellings for "comment submission"
    "comment submision": "apa_notice_and_comment",
    # Misspellings for "rulemaking docket"
    "rulemaking docet": "apa_notice_and_comment",
    # Misspellings for "rulemaking record"
    "rulemaking recod": "apa_notice_and_comment",
    # Misspellings for "final rule"
    "final ruel": "apa_notice_and_comment",
    # Misspellings for "final rulemaking"
    "final rulemakng": "apa_notice_and_comment",
    # Misspellings for "informal rulemaking"
    "informal rulemakng": "apa_notice_and_comment",
    # Misspellings for "regulations.gov"
    "regulations go": "apa_notice_and_comment",
    # Misspellings for "e-rulemaking"
    "e rulemaking": "apa_notice_and_comment",
    # Misspellings for "federal register"
    "federal registter": "apa_notice_and_comment",
    # Misspellings for "fr notice"
    "fr notce": "apa_notice_and_comment",
    # Misspellings for "rule publication"
    "rule publciation": "apa_notice_and_comment",
    # Misspellings for "rule notice"
    "rule notce": "apa_notice_and_comment",
    # Misspellings for "agency rulemaking"
    "agency rulemakng": "apa_notice_and_comment",
    # Misspellings for "agency rulemaking"
    "agency rulemakng": "apa_notice_and_comment",
    # Misspellings for "agency proposal"
    "agency propsoal": "apa_notice_and_comment",
    # Misspellings for "agency comment"
    "agency commment": "apa_notice_and_comment",
    # Misspellings for "agency response to comments"
    "agency response to commments": "apa_notice_and_comment",
    # Misspellings for "public comment"
    "public commment": "apa_notice_and_comment",
    # Misspellings for "public input"
    "public inpt": "apa_notice_and_comment",
    # Misspellings for "public hearing"
    "public heairng": "apa_notice_and_comment",
    # Misspellings for "public meeting"
    "public meetng": "apa_notice_and_comment",
    # Misspellings for "comment period"
    "comment perod": "apa_notice_and_comment",
    # Misspellings for "comment submission"
    "comment submision": "apa_notice_and_comment",
    # Misspellings for "rulemaking docket"
    "rulemaking docet": "apa_notice_and_comment",
    # Misspellings for "rulemaking record"
    "rulemaking recod": "apa_notice_and_comment",
    # Misspellings for "final rule"
    "final ruel": "apa_notice_and_comment",
    # Misspellings for "final rulemaking"
    "final rulemakng": "apa_notice_and_comment",
    # Misspellings for "informal rulemaking"
    "informal rulemakng": "apa_notice_and_comment",
    # Misspellings for "regulations.gov"
    "regulations go": "apa_notice_and_comment",
    # Misspellings for "e-rulemaking"
    "e rulemaking": "apa_notice_and_comment",
    # Misspellings for "federal register"
    "federal registter": "apa_notice_and_comment",
    # Misspellings for "fr notice"
    "fr notce": "apa_notice_and_comment",
    # Misspellings for "rule publication"
    "rule publciation": "apa_notice_and_comment",
    # Misspellings for "rule notice"
    "rule notce": "apa_notice_and_comment",
    # Misspellings for "agency rulemaking"
    "agency rulemakng": "apa_notice_and_comment",
    # Misspellings for "public docket"
    "public docet": "apa_notice_and_comment",
    # Misspellings for "public docket"
    "public docet": "apa_notice_and_comment",
}

_EXPECTED_ENTRY_COUNT = 420

def _compute_map_hash():
    items = sorted((k, v) for k, v in SEMANTIC_MAP.items())
    s = "".join(f"{k}=>{v};" for k, v in items)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity():
    actual_count = len(SEMANTIC_MAP)
    actual_hash = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (actual_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "ok" if is_valid else "error",
        "entries": actual_count,
        "expected_entries": _EXPECTED_ENTRY_COUNT,
        "hash": actual_hash,
        "expected_hash": _MAP_INTEGRITY_HASH,
        "is_valid": is_valid,
    }

def _normalize_key(term):
    if not isinstance(term, str):
        return ""
    t = term.strip().lower()
    t = re.sub(r"[\u2010-\u2015]", "-", t)  # normalize unicode dashes
    t = re.sub(r"\s+", " ", t)
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    t = t.replace("–", "-").replace("—", "-")
    t = t.replace("_", " ")
    t = t.replace(".", "")
    t = t.replace(",", "")
    t = t.replace(";", "")
    t = t.replace(":", "")
    t = t.replace("(", "")
    t = t.replace(")", "")
    t = t.replace("[", "")
    t = t.replace("]", "")
    t = t.replace("/", " ")
    t = t.replace("\\", " ")
    t = re.sub(r"\s+", " ", t)
    t = t.strip()
    return t

def normalize_term(term):
    k = _normalize_key(term)
    return SEMANTIC_MAP.get(k, None)

def get_related_terms(term):
    norm = normalize_term(term)
    if not norm:
        return []
    return [k for k, v in SEMANTIC_MAP.items() if v == norm]

def get_all_mappings():
    return dict(SEMANTIC_MAP)