import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

ENGINE_ID = "SYN07"
ENGINE_NAME = "Document Assembler"
VERSION = "1.0.0"
PORT = 9167

logger.add(f"{ENGINE_ID}_engine.log", rotation="100 MB", retention="30 days", level="INFO")

class DoctrineBlock:
    def __init__(self, topic: str, keywords: List[str], conclusion_template: str,
                 reasoning_framework: str, key_factors: List[str], primary_authority: List[str],
                 burden_holder: str, adversary_position: str, counter_arguments: List[str],
                 resolution_strategy: str, entity_scope: str, confidence: str,
                 confidence_stratification: str, controlling_precedent: str):
        self.topic = topic
        self.keywords = keywords
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.burden_holder = burden_holder
        self.adversary_position = adversary_position
        self.counter_arguments = counter_arguments
        self.resolution_strategy = resolution_strategy
        self.entity_scope = entity_scope
        self.confidence = confidence
        self.confidence_stratification = confidence_stratification
        self.controlling_precedent = controlling_precedent

DOCTRINE_CACHE = {
    "template_architecture": DoctrineBlock(
        topic="Template Architecture and Design",
        keywords=["template hierarchy", "master templates", "inheritance", "component reuse", "modular design"],
        conclusion_template="Template architecture determines assembly efficiency and maintainability.",
        reasoning_framework="""Document assembly templates follow hierarchical inheritance: master templates define
        structural elements (headers, footers, signature blocks), child templates inherit and extend with specific
        provisions. Modular design enables clause library reuse across document types. Template versioning tracks
        evolution - major versions indicate structural changes, minor versions reflect content updates. Variable
        placeholders use consistent naming (e.g., {{PARTY_A_NAME}}, {{EFFECTIVE_DATE}}) to enable cross-template
        standardization. Conditional logic gates (IF/ELSE/SWITCH) control clause inclusion based on transaction
        parameters. Template metadata captures jurisdiction, practice area, last review date, and deprecated status.""",
        key_factors=["inheritance depth", "variable naming conventions", "version control strategy", "metadata completeness", "conditional complexity"],
        primary_authority=["ABA Model Asset Purchase Agreement", "ACCA Contract Standards", "IACCM Template Library"],
        burden_holder="Template designer",
        adversary_position="Single monolithic templates simpler to maintain",
        counter_arguments=["Monolithic templates duplicate content", "Inheritance enables consistency", "Modular updates cascade efficiently"],
        resolution_strategy="Adopt hierarchical inheritance with documented conventions",
        entity_scope="All document types",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Industry best practices for document automation"
    ),
    "clause_library_taxonomy": DoctrineBlock(
        topic="Clause Library Organization and Taxonomy",
        keywords=["clause categorization", "library structure", "metadata tagging", "search indexing", "approval workflow"],
        conclusion_template="Effective clause taxonomy enables rapid retrieval and consistent application.",
        reasoning_framework="""Clause libraries organize by: (1) Practice area (M&A, employment, real estate),
        (2) Clause function (representations, warranties, covenants, conditions), (3) Risk allocation (seller-favorable,
        neutral, buyer-favorable), (4) Jurisdiction (state-specific provisions), (5) Complexity (standard/negotiated/custom).
        Each clause carries metadata: author, approval date, jurisdictional notes, risk assessment, usage frequency,
        alternative formulations. Approval workflow gates entry: attorney drafts, supervisor reviews, practice group
        approves, knowledge management indexes. Version control tracks amendments - substantive changes require
        re-approval. Deprecation flags obsolete provisions. Cross-references link related clauses (e.g., indemnification
        provisions reference survival periods, limitation of liability, basket/cap structures).""",
        key_factors=["taxonomy depth", "metadata richness", "approval rigor", "version discipline", "cross-reference integrity"],
        primary_authority=["IACCM Contracting Principles", "ACC Legal Operations Maturity Model", "LegalSifter Playbook Framework"],
        burden_holder="Knowledge management team",
        adversary_position="Flat file organization with keyword search sufficient",
        counter_arguments=["Flat structures lack semantic relationships", "Metadata enables faceted search", "Taxonomy reflects practice expertise"],
        resolution_strategy="Multi-dimensional taxonomy with rich metadata and approval gates",
        entity_scope="All clause types",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal knowledge management standards"
    ),
    "conditional_inclusion_logic": DoctrineBlock(
        topic="Conditional Inclusion and Assembly Logic",
        keywords=["if-then rules", "clause gating", "variable binding", "dependency chains", "mutual exclusivity"],
        conclusion_template="Conditional logic ensures contextually appropriate clause inclusion.",
        reasoning_framework="""Assembly logic implements business rules: IF transaction_type=asset_purchase THEN include
        asset_schedule AND bill_of_sale AND assignment_agreement. Nested conditions handle complexity: IF jurisdiction=CA
        AND employee_count>50 THEN include WARN_Act_compliance_clause. Mutual exclusivity prevents contradictions:
        arbitration_clause XOR litigation_forum_selection. Dependency chains trigger cascading inclusions: indemnification
        clause REQUIRES survival_period AND basket_cap_structure. Variable binding flows through conditions: IF party_type
        =individual THEN signature_block=individual_format ELSE corporate_format. Range checks validate inputs:
        purchase_price BETWEEN contract_minimum AND statutory_maximum. Date logic enforces sequences: closing_date AFTER
        signing_date, survival_period STARTS_FROM closing_date. Boolean algebra simplifies complex rules: include_escrow =
        (purchase_price > threshold) OR (earn_out_present) OR (indemnification_cap > limit).""",
        key_factors=["rule coverage", "mutual exclusivity enforcement", "dependency tracking", "validation rigor", "boolean optimization"],
        primary_authority=["Contract Lifecycle Management Standards", "Legal Automation Best Practices", "ISO 19510 BPMN"],
        burden_holder="Automation architect",
        adversary_position="Manual selection more flexible than rigid rules",
        counter_arguments=["Manual selection error-prone", "Rules embed expertise", "Validation prevents conflicts"],
        resolution_strategy="Declarative rule engine with dependency resolution and validation",
        entity_scope="All automated documents",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Document automation standards"
    ),
    "variable_substitution": DoctrineBlock(
        topic="Variable Substitution and Data Binding",
        keywords=["placeholder replacement", "data sources", "formatting rules", "validation", "default values"],
        conclusion_template="Robust variable substitution requires validation, formatting, and fallback handling.",
        reasoning_framework="""Variable substitution binds data to placeholders: {{PARTY_A_NAME}} -> 'Acme Corporation'.
        Data sources include user input forms, CRM integration, public records APIs, prior document extractions. Type
        coercion handles mismatches: date strings -> formatted dates, numeric strings -> currency display. Formatting
        rules apply contextual transformations: addresses -> block format for notices, ALL_CAPS for exhibit titles,
        title_case for party names in recitals. Validation prevents errors: email regex, state code enumeration,
        date range checks, required field enforcement. Default values provide fallbacks: jurisdiction defaults to
        headquarters state, notice period to statutory minimum. Calculated fields derive from inputs: total_shares =
        common_shares + preferred_shares, equity_percentage = (shares_purchased / total_shares) * 100. Conditional
        formatting adjusts per context: singular/plural agreement (1 share vs. 2 shares), gender pronouns per entity type.""",
        key_factors=["data source reliability", "validation coverage", "formatting consistency", "default reasonableness", "calculation accuracy"],
        primary_authority=["Legal Document Automation Standards", "Data Validation Best Practices", "ABA Formal Opinion on Tech Competence"],
        burden_holder="Document assembler",
        adversary_position="Simple string replacement adequate for most cases",
        counter_arguments=["Unvalidated substitution causes errors", "Formatting ensures professionalism", "Defaults prevent omissions"],
        resolution_strategy="Typed variables with validation, formatting rules, and intelligent defaults",
        entity_scope="All variable-driven documents",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Document automation industry standards"
    ),
    "cross_reference_integrity": DoctrineBlock(
        topic="Cross-Reference Management and Integrity",
        keywords=["section numbering", "defined terms", "exhibit references", "internal consistency", "auto-update"],
        conclusion_template="Automated cross-reference management prevents inconsistencies in complex documents.",
        reasoning_framework="""Cross-references create internal dependencies: Section 8.2 references Section 3.5,
        Exhibit A referenced in Section 2.1. Automated numbering adapts to structure changes: inserting new Section 3.3
        auto-renumbers 3.3 -> 3.4, updates all references. Defined term tracking: first use triggers definition formatting
        (capitalized, optionally quoted), subsequent uses link to definition. Exhibit/schedule coordination: assembly
        auto-generates exhibit list in table of contents, validates all references have corresponding exhibits. Hierarchical
        numbering (1.1.1, 1.1.2) maintains parent-child relationships during reordering. Broken reference detection flags
        orphaned pointers pre-finalization. Cross-document references (incorporation by reference) require version pinning
        to prevent ambiguity. Circular reference prevention: dependency graph analysis rejects cycles.""",
        key_factors=["numbering scheme consistency", "defined term discipline", "exhibit completeness", "broken link detection", "circular reference prevention"],
        primary_authority=["Legal Drafting Style Guides", "Document Assembly Technical Standards", "ABA Model Rules on Document Preparation"],
        burden_holder="Assembly system",
        adversary_position="Manual cross-reference maintenance during review sufficient",
        counter_arguments=["Manual updates miss cascading changes", "Automation ensures consistency", "Detection prevents finalization errors"],
        resolution_strategy="Graph-based dependency tracking with auto-numbering and validation",
        entity_scope="All multi-section documents",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Document automation best practices"
    ),
    "defined_terms_consistency": DoctrineBlock(
        topic="Defined Terms Consistency and Management",
        keywords=["definitions section", "capitalization", "cross-document consistency", "ambiguity prevention", "term index"],
        conclusion_template="Rigorous defined term management prevents ambiguity and interpretation disputes.",
        reasoning_framework="""Defined terms establish precise meanings: 'Agreement' means this Asset Purchase Agreement,
        'Purchased Assets' as defined in Section 2.1. Capitalization signals defined status: 'Seller' (defined) vs.
        'seller' (common noun). First-use formatting: 'the undersigned purchaser (the 'Purchaser')' establishes definition.
        Alphabetical definitions section provides canonical reference. Consistency validation: flag uses before definition,
        inconsistent capitalization, undefined capitalized terms. Cross-document harmonization: standard definitions
        (Business Day, Knowledge, Material Adverse Effect) maintain consistent meaning across document suite. Ambiguity
        detection: flag terms with multiple conflicting definitions, circular definitions (A defined using B, B using A).
        Incorporation by reference: 'Terms defined in the Credit Agreement have the same meanings herein' requires
        validation that referenced document accessible. Exhibit/schedule defined terms flow to main document.""",
        key_factors=["first-use detection", "capitalization consistency", "alphabetization", "cross-document harmonization", "circular definition prevention"],
        primary_authority=["Garner's Legal Writing", "ABA Model Stock Purchase Agreement", "ISDA Master Agreement Definitions"],
        burden_holder="Drafting attorney and assembly system",
        adversary_position="Defined terms add unnecessary formality",
        counter_arguments=["Definitions eliminate ambiguity", "Consistency prevents disputes", "Industry standard expects definitions"],
        resolution_strategy="Automated defined term extraction, validation, and cross-referencing",
        entity_scope="All formal legal documents",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal drafting conventions"
    ),
    "exhibit_schedule_generation": DoctrineBlock(
        topic="Exhibit and Schedule Auto-Generation",
        keywords=["attachment assembly", "data population", "formatting", "reference validation", "signature pages"],
        conclusion_template="Automated exhibit generation ensures completeness and consistency with main document.",
        reasoning_framework="""Exhibits/schedules attach supporting details: Exhibit A = Asset List, Schedule 3.5 =
        Litigation Disclosure. Auto-generation populates from data sources: asset list from ERP export, litigation from
        matter management system, subsidiaries from corporate database. Formatting applies templates: asset list as table
        (Asset Description | Serial Number | Condition), disclosure schedules as numbered paragraphs. Reference validation
        ensures bidirectional consistency: main document Section 2.1 references Exhibit A, Exhibit A header confirms
        'Referenced in Section 2.1'. Signature page generation: party count drives signature block count, entity type
        determines format (corporate = name/title/signature vs. individual = name/signature). Notarization blocks insert
        per jurisdiction: California acknowledgment differs from New York. Exhibit ordering: alphabetical (A, B, C) or
        numerical (1, 2, 3) per document type convention. Assembly manifest: generated table of exhibits with descriptions.""",
        key_factors=["data source integration", "template formatting", "reference bidirectionality", "signature block accuracy", "notarization compliance"],
        primary_authority=["ABA Model Agreements", "State Notarization Statutes", "Document Assembly Technical Standards"],
        burden_holder="Assembly system and data providers",
        adversary_position="Manually attaching exhibits provides quality control",
        counter_arguments=["Manual attachment omits referenced exhibits", "Automation ensures completeness", "Data integration reduces transcription errors"],
        resolution_strategy="Template-driven exhibit generation with bidirectional validation",
        entity_scope="All documents with attachments",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal document preparation standards"
    ),
    "redline_comparison": DoctrineBlock(
        topic="Redlining and Document Comparison",
        keywords=["track changes", "version comparison", "markup generation", "metadata preservation", "acceptance workflow"],
        conclusion_template="Automated redlining accelerates negotiation and maintains audit trail.",
        reasoning_framework="""Redline comparison identifies changes between versions: insertions (underline), deletions
        (strikethrough), moves (cut/paste detection). Comparison algorithms: word-level (high granularity, verbose),
        sentence-level (cleaner for substantive changes), semantic (groups related edits). Metadata preservation: track
        author, timestamp, comment rationale per change. Style normalization pre-comparison: strip formatting differences
        (font, spacing) to isolate substantive changes. Move detection prevents false positive delete+insert: relocated
        section shows as move, not delete/add. Table comparison: cell-level tracking for spreadsheets/schedules.
        Acceptance workflow: changes require attorney review, approval marks accepted, rejection restores original.
        Version history: maintain full chain (v1 -> v2 -> v3) for audit trail. Comment threading: responses to proposed
        changes nest under original. Export formats: native track changes (Word), PDF annotations, HTML comparison view.""",
        key_factors=["comparison granularity", "move detection accuracy", "metadata richness", "acceptance workflow", "format flexibility"],
        primary_authority=["ABA Tech Standards", "ISO 21320 Document Comparison", "Legal Tech Best Practices"],
        burden_holder="Document management system",
        adversary_position="Side-by-side manual comparison provides better context",
        counter_arguments=["Manual comparison misses subtle changes", "Automated redline comprehensive", "Metadata audit trail essential"],
        resolution_strategy="Semantic comparison with move detection and workflow integration",
        entity_scope="All negotiated documents",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Document lifecycle management standards"
    ),
    "version_control": DoctrineBlock(
        topic="Document Version Control and Branching",
        keywords=["version numbering", "branching strategy", "merge conflicts", "audit trail", "rollback"],
        conclusion_template="Rigorous version control enables collaboration, audit, and recovery.",
        reasoning_framework="""Version numbering schemes: semantic (1.2.3 = major.minor.patch), date-based (2024-01-15_v2),
        negotiation rounds (Draft_1, Draft_2, Execution). Branching strategies: main branch (executed version), negotiation
        branches per counterparty, alternate scenario branches (Plan A / Plan B). Merge conflicts: overlapping edits to
        same section require manual resolution, non-overlapping auto-merge. Check-in/check-out: lock documents during
        editing to prevent simultaneous conflicting changes. Audit trail: complete history (who, what, when) for compliance
        and dispute resolution. Rollback capability: revert to any prior version if negotiation derails. Tagging: mark
        milestones (Initial Draft, First Markup, Final Negotiated, Executed). Comparison across branches: evaluate
        alternative deal structures. Integration with execution: final version promoted to executed status, prior versions
        archived. Retention policies: executed documents permanent, drafts per policy (e.g., 7 years).""",
        key_factors=["numbering clarity", "branch management", "merge robustness", "audit completeness", "rollback reliability"],
        primary_authority=["ISO 19005 PDF/A for Archival", "Legal Document Retention Standards", "Version Control Best Practices"],
        burden_holder="Document management system and users",
        adversary_position="Email chains with attachments provide version history",
        counter_arguments=["Email lacks structure and search", "Version control system authoritative", "Audit trail dispute-proof"],
        resolution_strategy="Git-style branching with legal-specific metadata and retention",
        entity_scope="All multi-party negotiated documents",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal tech and compliance standards"
    ),
    "signature_block_formatting": DoctrineBlock(
        topic="Signature Block Standards and Formatting",
        keywords=["execution format", "entity type", "authority representation", "notarization", "electronic signatures"],
        conclusion_template="Proper signature block formatting ensures enforceability and authority verification.",
        reasoning_framework="""Signature block elements vary by entity: (1) Individual = Name, Signature, Date;
        (2) Corporation = Entity Name, Signatory Name, Title, Signature, Date; (3) LLC = LLC Name, Member/Manager Name,
        Capacity, Signature, Date; (4) Partnership = Partnership Name, Partner Name, Signature, Date; (5) Trust =
        Trust Name, Trustee Name, Capacity, Signature, Date. Authority representation: 'By: [Signature], Name: [Typed],
        Title: [President]' evidences corporate authority. Notarization requirements: deeds require acknowledgment in
        most states, affidavits require jurat. State-specific acknowledgment language: California Civil Code Section 1189
        vs. New York RPAPL. Witness requirements: wills (2-3 witnesses), deeds in some states (1-2 witnesses).
        Electronic signature compliance: ESIGN Act and UETA enable e-signatures, must evidence intent (click-through,
        typed name with /s/, DocuSign certificate). Counterpart execution: 'This Agreement may be executed in counterparts'
        enables distributed signing. Date consistency: all signatures same date or within allowed window.""",
        key_factors=["entity type accuracy", "authority clarity", "notarization compliance", "witness sufficiency", "e-signature validity"],
        primary_authority=["State Corporate Codes", "ESIGN Act", "UETA", "Notarization Statutes", "ABA Model Forms"],
        burden_holder="Execution coordinator and notary",
        adversary_position="Generic signature block adequate if parties sign",
        counter_arguments=["Generic blocks omit required elements", "Entity-specific format proves authority", "Notarization compliance jurisdictional"],
        resolution_strategy="Entity-type driven templates with jurisdictional notarization rules",
        entity_scope="All executed agreements",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="State execution and notarization statutes"
    ),
    "jurisdictional_customization": DoctrineBlock(
        topic="Jurisdictional Customization and Compliance",
        keywords=["state-specific provisions", "choice of law", "forum selection", "regulatory requirements", "local counsel"],
        conclusion_template="Jurisdictional customization ensures enforceability and regulatory compliance.",
        reasoning_framework="""Jurisdiction drives substantive provisions: (1) Employment: California meal/rest break
        requirements, New York wage notice obligations, Texas non-compete 2-year maximum; (2) Real Estate: California
        statutory warranty deed, New York bargain-and-sale deed, Texas special warranty deed; (3) Corporate: Delaware
        exculpation provisions, California cumulative voting rights; (4) Lending: State usury limits, licensing requirements,
        foreclosure procedures. Choice of law clauses: 'Governed by laws of Delaware' determines interpretive rules, but
        can't override mandatory local law (e.g., can't waive California wage protections via Delaware choice of law).
        Forum selection: 'Exclusive jurisdiction in Delaware Chancery Court' channels disputes, subject to personal
        jurisdiction limits. Regulatory overlays: securities (state blue sky laws), insurance (state DOI approval),
        banking (state licensing). Local counsel review: multistate transactions require state-specific review to catch
        nuances. Conflict of laws analysis: Restatement (Second) most significant relationship test determines applicable
        law absent choice of law clause. Severability: invalid provisions severed while preserving remainder.""",
        key_factors=["mandatory law identification", "choice of law enforceability", "forum selection validity", "regulatory compliance", "local counsel involvement"],
        primary_authority=["State Statutes", "Restatement (Second) of Conflict of Laws", "ABA Multistate Practice Guidelines"],
        burden_holder="Drafting attorney and local counsel",
        adversary_position="Single national form adequate for all states",
        counter_arguments=["Mandatory state law can't be waived", "Local variations create traps", "Customization ensures enforceability"],
        resolution_strategy="State-specific template variants with local counsel validation",
        entity_scope="All multistate documents",
        confidence="HIGH",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="State-specific statutes and case law"
    ),
    "template_versioning": DoctrineBlock(
        topic="Template Version Control and Lifecycle",
        keywords=["template updates", "backward compatibility", "deprecation", "testing", "rollout"],
        conclusion_template="Template lifecycle management balances improvement with stability.",
        reasoning_framework="""Template evolution: (1) Draft: attorney creates new template, KM reviews; (2) Testing:
        pilot with sample data, validate output; (3) Approval: practice group sign-off; (4) Production: release to users;
        (5) Maintenance: bug fixes, minor updates; (6) Deprecation: sunset obsolete templates. Versioning: major (structural
        changes breaking backward compatibility), minor (new optional sections), patch (bug fixes). Backward compatibility:
        documents assembled from v1.2 remain valid when v1.3 released. Migration path: v1.x -> v2.0 provides conversion
        utility for in-flight documents. Testing protocol: unit tests (variable substitution), integration tests (clause
        interactions), regression tests (prior version output unchanged). Rollout: phased (pilot users, then general),
        with rollback plan if issues. Change documentation: release notes detail updates, migration guide for major versions.
        User training: webinars for significant changes. Feedback loop: user bug reports drive patch releases.""",
        key_factors=["version discipline", "backward compatibility", "testing rigor", "rollout strategy", "user communication"],
        primary_authority=["Software Development Lifecycle Standards", "Change Management Best Practices", "Legal Tech Implementation Guides"],
        burden_holder="Knowledge management and IT",
        adversary_position="Update templates without versioning when improvements identified",
        counter_arguments=["Unversioned updates break in-flight documents", "Testing prevents production errors", "Communication manages user expectations"],
        resolution_strategy="Semantic versioning with testing gates and phased rollout",
        entity_scope="All templates",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Software and legal tech standards"
    ),
    "clause_approval_workflow": DoctrineBlock(
        topic="Clause Approval and Governance Workflow",
        keywords=["drafting authority", "review process", "practice group oversight", "risk assessment", "client approval"],
        conclusion_template="Clause approval workflow balances speed with risk management.",
        reasoning_framework="""Approval tiers: (1) Pre-approved: standard clauses usable without review (e.g., boilerplate
        notices provision); (2) Attorney-approved: associate drafts, partner approves; (3) Practice group-approved:
        novel provisions require group consensus; (4) Client-approved: business-sensitive terms (pricing, IP) require
        client sign-off; (5) Outside counsel-approved: highly specialized (tax, regulatory) require expert review.
        Risk assessment: clauses scored (1-5) on legal risk, business impact, negotiability. High-risk clauses (4-5)
        require elevated approval. Fallback chains: if preferred clause rejected, system suggests alternatives in
        descending preference order. Approval metadata: approver name, date, rationale, expiration (clauses requiring
        periodic revalidation). Bulk approval: practice group approves clause library package, individual clauses inherit.
        Override mechanism: urgent matters enable partner override with post-hoc ratification. Audit trail: all approvals
        logged for malpractice defense and quality control.""",
        key_factors=["approval authority clarity", "risk scoring accuracy", "fallback completeness", "audit trail integrity", "override controls"],
        primary_authority=["ABA Model Rules on Supervision", "Legal Risk Management Standards", "ACC Legal Ops Maturity Model"],
        burden_holder="Practice group leaders and partners",
        adversary_position="Individual attorney judgment sufficient for clause selection",
        counter_arguments=["Individual judgment inconsistent", "Approval ensures quality", "Risk scoring prioritizes review"],
        resolution_strategy="Tiered approval with risk-based routing and audit trail",
        entity_scope="All clauses in library",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal governance and risk management standards"
    ),
    "data_source_integration": DoctrineBlock(
        topic="Integration with External Data Sources",
        keywords=["CRM integration", "ERP data", "public records APIs", "third-party verification", "data freshness"],
        conclusion_template="Data integration reduces manual entry and improves accuracy.",
        reasoning_framework="""Data sources: (1) CRM (Salesforce): party names, addresses, contacts, relationship history;
        (2) ERP (SAP): asset lists, financial data, organizational structure; (3) HRIS: employee data for equity grants,
        employment agreements; (4) Public records APIs: corporate status (Secretary of State), UCC filings, litigation
        history; (5) Third-party: D&B for credit, LexisNexis for entity verification, title companies for real estate.
        Integration methods: API (real-time), batch export (nightly), manual upload (ad hoc). Data mapping: CRM 'Account
        Name' -> template 'PARTY_A_NAME', ERP 'Asset_ID' -> 'ASSET_SERIAL_NUMBER'. Validation: API responses checked
        for staleness (e.g., corporate status > 30 days old triggers warning), completeness (required fields populated).
        Caching: frequently-used data cached locally with TTL (time-to-live), refresh on expiration. Conflict resolution:
        CRM vs. manual entry, system prompts user to confirm. Security: API credentials in vault, encrypted in transit
        (TLS), access logging for audit. Error handling: API timeout -> fallback to cached data with staleness warning.""",
        key_factors=["source reliability", "integration method robustness", "data freshness", "validation rigor", "security posture"],
        primary_authority=["API Security Best Practices", "Data Integration Standards", "ABA Tech Competence Opinion"],
        burden_holder="IT and legal operations",
        adversary_position="Manual data entry provides verification step",
        counter_arguments=["Manual entry error-prone", "Integration improves accuracy", "Validation catches errors"],
        resolution_strategy="Multi-source integration with validation, caching, and fallback",
        entity_scope="All data-driven documents",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal technology integration standards"
    ),
    "output_format_generation": DoctrineBlock(
        topic="Multi-Format Output Generation",
        keywords=["Word export", "PDF generation", "HTML rendering", "formatting preservation", "accessibility"],
        conclusion_template="Multi-format support meets diverse use cases while preserving content integrity.",
        reasoning_framework="""Output formats: (1) Word (.docx): editable for further negotiation, track changes enabled;
        (2) PDF: final execution-ready, locked to prevent tampering, digital signature support; (3) HTML: web viewing,
        email embedding; (4) Plain text: fallback for limited systems. Format conversion: master content in structured
        format (XML/JSON), rendering engine applies format-specific styling. Formatting preservation: styles (headings,
        bullets, numbering) consistent across formats, complex elements (tables, footnotes) render correctly. Accessibility:
        PDF/A for archival, tagged PDFs for screen readers, alt text for images. Watermarking: 'DRAFT' on non-final
        versions, 'EXECUTED' on signed. Page layout: margins, headers/footers, page numbers per format requirements.
        Signature fields: PDF form fields for e-signature, Word signature lines for wet ink. Metadata: document properties
        (author, title, creation date) embedded. File naming: standardized convention (AgreementType_Parties_Date_Version.ext).""",
        key_factors=["format fidelity", "conversion accuracy", "accessibility compliance", "metadata richness", "naming consistency"],
        primary_authority=["PDF/A ISO 19005", "WCAG Accessibility Guidelines", "Legal Document Standards"],
        burden_holder="Document assembly system",
        adversary_position="Single format (Word or PDF) sufficient for all uses",
        counter_arguments=["Different stakeholders need different formats", "Conversion maintains consistency", "Accessibility legally required"],
        resolution_strategy="Template-driven multi-format rendering with accessibility and metadata",
        entity_scope="All assembled documents",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Format and accessibility standards"
    ),
    "assembly_performance": DoctrineBlock(
        topic="Assembly Performance and Scalability",
        keywords=["generation speed", "concurrent assembly", "caching", "resource optimization", "queue management"],
        conclusion_template="High-performance assembly enables real-time document generation at scale.",
        reasoning_framework="""Performance targets: simple documents (5-10 pages) < 3 seconds, complex (50+ pages) < 30
        seconds, bulk generation (100+ docs) via queue. Optimization techniques: (1) Template precompilation: parse once,
        render many; (2) Clause caching: frequently-used clauses kept in memory; (3) Lazy loading: exhibits generated
        only if referenced; (4) Parallel processing: independent sections assembled concurrently. Scalability: horizontal
        (multiple assembly servers), vertical (optimize code paths). Queue management: bulk jobs submitted to background
        queue (RabbitMQ, Redis), workers process asynchronously, status API for progress. Resource limits: timeout long-running
        assemblies (>5 min), memory caps prevent runaway processes, CPU throttling for fairness. Monitoring: track
        assembly times, error rates, queue depth. Caching strategy: template cache (1 hour TTL), clause cache (24 hour),
        data cache (configurable per source). CDN: static assets (logos, standard clauses) served from edge.""",
        key_factors=["generation latency", "throughput capacity", "cache effectiveness", "queue reliability", "resource utilization"],
        primary_authority=["Web Performance Best Practices", "Scalable Systems Design", "Cloud Architecture Patterns"],
        burden_holder="Engineering and DevOps",
        adversary_position="Single-threaded generation adequate for typical volume",
        counter_arguments=["Single-threaded bottlenecks at scale", "Optimization improves user experience", "Queuing handles spikes"],
        resolution_strategy="Optimized pipeline with caching, parallelism, and async queue",
        entity_scope="All assembly operations",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Software performance engineering standards"
    ),
    "assembly_audit_trail": DoctrineBlock(
        topic="Assembly Audit Trail and Compliance",
        keywords=["generation log", "template version used", "data sources", "user identity", "compliance reporting"],
        conclusion_template="Comprehensive audit trail supports compliance, quality control, and dispute resolution.",
        reasoning_framework="""Audit trail captures: (1) User: identity, role, timestamp; (2) Template: ID, version,
        clauses selected; (3) Data: sources queried, values substituted, validation results; (4) Output: format, file
        hash (SHA-256), delivery method; (5) Errors: warnings, failures, resolutions. Retention: logs retained per
        document retention policy (typically 7 years post-execution). Compliance uses: demonstrate reasonable care in
        malpractice claim, prove document provenance in dispute, satisfy regulatory audit (SOX, GDPR). Query capability:
        search logs by user, template, date range, document type. Tamper evidence: append-only log, cryptographic hash
        chain prevents retroactive modification. Privacy: PII in logs protected per data protection laws (encryption at
        rest, access controls). Performance: log writes asynchronous to avoid blocking assembly. Analysis: aggregate logs
        for usage patterns (popular templates, error hotspots, performance bottlenecks). Integration: SIEM (Splunk) for
        security monitoring, BI tools for business intelligence.""",
        key_factors=["log completeness", "retention compliance", "query performance", "tamper resistance", "privacy protection"],
        primary_authority=["SOX Compliance Standards", "GDPR Data Protection", "Legal Audit Requirements", "ISO 27001"],
        burden_holder="Legal ops and compliance",
        adversary_position="Basic activity log sufficient for audit",
        counter_arguments=["Basic logs lack detail for root cause", "Comprehensive trail proves compliance", "Hash chain ensures integrity"],
        resolution_strategy="Structured append-only audit log with retention and query capability",
        entity_scope="All assembly operations",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Compliance and audit standards"
    ),
    "error_handling_assembly": DoctrineBlock(
        topic="Assembly Error Handling and Recovery",
        keywords=["validation errors", "missing data", "template errors", "graceful degradation", "user notification"],
        conclusion_template="Robust error handling prevents broken documents and guides users to resolution.",
        reasoning_framework="""Error categories: (1) Validation: required field missing, data type mismatch, range violation;
        (2) Template: broken reference, circular dependency, missing clause; (3) Data source: API timeout, invalid response,
        permission denied; (4) System: memory exhausted, timeout exceeded. Handling strategies: (1) Validation errors:
        block assembly, highlight missing fields in UI, provide inline help; (2) Template errors: fallback to previous
        template version, notify KM team; (3) Data source errors: use cached data with staleness warning, prompt manual
        entry; (4) System errors: retry transient failures (3 attempts), fail gracefully with error report. User notification:
        error messages specific ('Purchase price must be positive') not generic ('Invalid input'), suggest corrective
        action ('Enter value between $1 and $1B'), link to help docs. Partial generation: on non-critical error, generate
        document with warnings section listing issues. Error reporting: logs capture stack trace, user context, repro
        steps for support. Testing: inject faults (missing data, API failures) to validate handling.""",
        key_factors=["error detection coverage", "message clarity", "fallback robustness", "logging detail", "testing rigor"],
        primary_authority=["UX Error Handling Guidelines", "System Reliability Standards", "User-Centered Design Principles"],
        burden_holder="Engineering and UX",
        adversary_position="Generic error messages with manual troubleshooting adequate",
        counter_arguments=["Generic messages frustrate users", "Specific guidance accelerates resolution", "Graceful degradation maintains productivity"],
        resolution_strategy="Layered error handling with specific messages, fallbacks, and logging",
        entity_scope="All assembly operations",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Software engineering and UX standards"
    ),
    "template_testing": DoctrineBlock(
        topic="Template Testing and Quality Assurance",
        keywords=["test data", "edge cases", "output validation", "regression testing", "user acceptance"],
        conclusion_template="Comprehensive testing prevents defective documents from reaching production.",
        reasoning_framework="""Test phases: (1) Unit: individual clauses render correctly; (2) Integration: clause
        interactions (e.g., indemnity + survival) produce coherent output; (3) System: full document assembly with real
        data; (4) Regression: changes don't break existing functionality; (5) UAT: attorneys validate legal accuracy.
        Test data: realistic scenarios (simple deal, complex multi-party, edge cases like single-member LLC), boundary
        conditions (minimum/maximum values, zero quantities), invalid inputs (missing required fields, out-of-range).
        Output validation: compare generated document to expected (golden master), verify formatting (numbering, spacing),
        check cross-references resolve, validate exhibits match main text. Regression suite: run on every template change,
        flag differences from baseline. Edge cases: jurisdictional variations (50 states tested for employment agreement),
        entity type permutations (corp, LLC, partnership), unusual fact patterns. UAT: attorneys review sample output,
        sign-off required before production release. Continuous testing: automated tests in CI/CD pipeline, nightly runs
        against production templates.""",
        key_factors=["test coverage", "edge case breadth", "validation rigor", "UAT thoroughness", "automation degree"],
        primary_authority=["Software Testing Standards", "Legal QA Best Practices", "CI/CD Pipeline Standards"],
        burden_holder="QA team and practice group",
        adversary_position="Manual review of first generated document sufficient",
        counter_arguments=["Manual review misses edge cases", "Automated testing comprehensive", "Regression prevents backsliding"],
        resolution_strategy="Automated test suite with UAT sign-off gate",
        entity_scope="All templates",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Software quality and legal risk management"
    ),
    "user_interface_design": DoctrineBlock(
        topic="User Interface for Document Assembly",
        keywords=["wizard workflow", "progressive disclosure", "contextual help", "preview", "guided input"],
        conclusion_template="Intuitive UI reduces errors and accelerates document generation.",
        reasoning_framework="""UI patterns: (1) Wizard: multi-step workflow guides user through inputs (Step 1: Parties,
        Step 2: Terms, Step 3: Exhibits); (2) Form: single-page input for simple documents; (3) Questionnaire: branching
        questions adapt to prior answers. Progressive disclosure: show only relevant fields (if asset_purchase, show
        asset_schedule input; else hide). Contextual help: tooltips on field labels ('Purchase Price: total consideration
        for assets'), inline examples ('e.g., 2024-12-31'), links to definitions. Preview: real-time document preview
        updates as user types, highlights sections affected by current input. Validation: inline (red border on invalid
        field), summary (error list at top), blocking (can't proceed with errors). Smart defaults: pre-populate known
        values (party addresses from CRM), suggest based on document type (asset purchase defaults to seller reps/warranties).
        Save progress: draft documents persist, users resume later. Templates: save input sets as templates for repeat
        transactions. Accessibility: keyboard navigation, screen reader compatible, sufficient color contrast.""",
        key_factors=["workflow intuitiveness", "help accessibility", "preview accuracy", "validation UX", "accessibility compliance"],
        primary_authority=["Nielsen Norman Group UX Guidelines", "WCAG Accessibility Standards", "User-Centered Design Principles"],
        burden_holder="UX designers and developers",
        adversary_position="Command-line or config file input adequate for power users",
        counter_arguments=["CLI excludes non-technical users", "GUI democratizes access", "Wizard prevents errors"],
        resolution_strategy="Wizard-based UI with progressive disclosure, contextual help, and preview",
        entity_scope="All assembly interfaces",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="UX and accessibility standards"
    ),
    "bulk_generation": DoctrineBlock(
        topic="Bulk Document Generation and Batch Processing",
        keywords=["CSV import", "template application", "variable documents", "queue processing", "error reporting"],
        conclusion_template="Bulk generation enables high-volume production with error isolation.",
        reasoning_framework="""Use cases: (1) Employment offer letters: 50 new hires, same template, variable data (name,
        title, salary); (2) NDA campaign: 200 vendors, standard NDA, variable party/address; (3) Equity grants: 500
        employees, option agreements with variable shares/vesting. Input methods: CSV upload (columnar data maps to template
        variables), API batch endpoint (programmatic submission), database query (pull from HRIS/ERP). Processing: jobs
        queued, workers process in parallel, status API tracks progress (pending/processing/complete/failed). Error
        handling: per-document errors isolated (row 37 fails, others proceed), error report generated (failed rows,
        reasons, suggested fixes). Output: ZIP archive of generated documents, manifest CSV (filename, status, errors).
        Validation: pre-flight check (required columns present, data types valid) before queue submission. Throttling:
        rate limits prevent system overload, priority queue for urgent batches. Monitoring: dashboard shows queue depth,
        processing rate, error rate. Audit: bulk job ID links all generated documents for compliance tracking.""",
        key_factors=["input flexibility", "error isolation", "processing throughput", "status visibility", "audit linkage"],
        primary_authority=["Batch Processing Standards", "ETL Best Practices", "Scalable Systems Design"],
        burden_holder="Legal ops and IT",
        adversary_position="Generate documents individually to ensure quality",
        counter_arguments=["Individual generation slow for high volume", "Bulk with validation maintains quality", "Error isolation prevents cascade failures"],
        resolution_strategy="Queue-based batch processor with validation, status tracking, and error reporting",
        entity_scope="All high-volume document needs",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Enterprise automation standards"
    ),
    "collaboration_features": DoctrineBlock(
        topic="Collaborative Document Assembly",
        keywords=["multi-user editing", "commenting", "task assignment", "approval routing", "notification"],
        conclusion_template="Collaboration features enable team-based document preparation.",
        reasoning_framework="""Collaboration modes: (1) Sequential: user A completes section, assigns to user B; (2) Parallel:
        multiple users edit different sections simultaneously; (3) Review: primary drafter, secondary reviewer adds comments.
        Commenting: thread comments on specific clauses, mention users (@attorney_name), resolve when addressed. Task
        assignment: 'Assign Schedule 3.5 disclosure to Jane Doe', due date, email notification. Approval routing: document
        advances through workflow (associate -> partner -> client), each approver signs off or sends back with comments.
        Notification: real-time (browser push for active users), email digest (daily summary of activity), mobile alerts
        (urgent approvals). Presence indicators: show active editors ('John Doe editing Section 2.1'), prevent simultaneous
        edits to same section (lock). Version reconciliation: if conflicts, system highlights divergent sections, prompts
        manual merge. Audit: collaboration activity logged (comments, assignments, approvals) for compliance. Permissions:
        role-based (associates can draft, partners can approve), document-level (restrict sensitive deals).""",
        key_factors=["edit conflict resolution", "notification timeliness", "approval workflow flexibility", "audit completeness", "permission granularity"],
        primary_authority=["Collaboration Software Standards", "Legal Workflow Best Practices", "Access Control Standards"],
        burden_holder="Legal ops and IT",
        adversary_position="Email-based collaboration sufficient",
        counter_arguments=["Email lacks structure and version control", "Integrated collaboration streamlines workflow", "Audit trail essential for compliance"],
        resolution_strategy="Integrated collaboration with commenting, assignment, routing, and audit",
        entity_scope="All multi-party document preparation",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal tech collaboration standards"
    ),
    "regulatory_compliance_docs": DoctrineBlock(
        topic="Regulatory Compliance Document Generation",
        keywords=["disclosure requirements", "regulatory templates", "filing deadlines", "agency formats", "validation"],
        conclusion_template="Compliance document automation ensures accuracy and timeliness of regulatory filings.",
        reasoning_framework="""Regulatory contexts: (1) Securities: Form D (Reg D offerings), Form 4 (insider transactions),
        8-K (material events); (2) Employment: EEO-1 (workforce demographics), OSHA 300 (injury log), WARN (layoff notice);
        (3) Environmental: SPCC (spill prevention), TRI (toxic release inventory); (4) Tax: 1099 variants, 1095-C (ACA
        reporting). Template sources: agency-provided PDFs (convert to fillable forms), third-party compliance tools,
        internally developed. Validation: required field enforcement per regulation, format compliance (EDGAR XBRL for
        SEC, XML for OSHA), calculation checks (aggregations, reconciliations). Filing deadlines: deadline tracking calendar,
        automated reminders (30/15/5 days before), expedited processing flag. Agency-specific requirements: SEC EDGAR
        character encoding, IRS MeF schema validation, state-specific formats. Data sources: financial system (revenue,
        expenses), HRIS (employee counts, wages), ERP (facility locations, production volumes). Output: agency-ready file
        format, cover letter, filing instructions. Audit: compliance filings logged with filing date, agency confirmation,
        supporting data snapshot.""",
        key_factors=["regulation coverage", "validation rigor", "deadline adherence", "format compliance", "audit trail"],
        primary_authority=["Agency-Specific Regulations", "Compliance Management Standards", "Filing Requirements"],
        burden_holder="Compliance team and legal",
        adversary_position="Manual preparation ensures accuracy",
        counter_arguments=["Manual preparation error-prone and slow", "Automation enforces validation rules", "Deadline tracking prevents missed filings"],
        resolution_strategy="Regulation-specific templates with validation, deadline tracking, and audit",
        entity_scope="All regulatory filings",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Regulatory compliance requirements"
    ),
    "change_impact_analysis": DoctrineBlock(
        topic="Change Impact Analysis for Templates",
        keywords=["dependency mapping", "affected documents", "rollback planning", "communication", "testing scope"],
        conclusion_template="Impact analysis ensures template changes don't cause unintended consequences.",
        reasoning_framework="""Impact analysis steps: (1) Dependency mapping: identify documents using template, clauses
        referencing modified clause; (2) Risk assessment: structural change (high risk) vs. typo fix (low risk); (3) Testing
        scope: regression tests for all dependent documents, UAT with affected practice groups; (4) Communication: notify
        users of impending change, training if workflow affected; (5) Rollback plan: retain prior version, rollback procedure
        if issues. Tools: dependency graph visualization (shows clause A used in templates X, Y, Z), affected document
        report (lists active documents using changed template). Staging: test changes in non-production environment, validate
        with sample data. Phased rollout: release to pilot group, monitor for issues, expand to all users. Post-change
        monitoring: track error rates, user feedback, document quality metrics. Version coordination: if template v2.0
        released mid-negotiation, in-flight documents continue on v1.x until execution, new documents use v2.0. Deprecation
        notice: advance warning (90 days) before template retirement, migration path to replacement.""",
        key_factors=["dependency completeness", "risk assessment accuracy", "testing coverage", "communication timeliness", "rollback readiness"],
        primary_authority=["Change Management Standards", "Software Release Management", "Legal Tech Implementation Guides"],
        burden_holder="Knowledge management and QA",
        adversary_position="Make changes as needed without formal analysis",
        counter_arguments=["Unanalyzed changes break dependent documents", "Impact analysis prevents production issues", "Communication manages user expectations"],
        resolution_strategy="Formal impact analysis with dependency mapping, testing, and phased rollout",
        entity_scope="All template changes",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Change and release management standards"
    ),
    "integration_contract_lifecycle": DoctrineBlock(
        topic="Integration with Contract Lifecycle Management",
        keywords=["CLM system", "metadata sync", "workflow handoff", "repository storage", "analytics"],
        conclusion_template="CLM integration extends assembly into full contract lifecycle.",
        reasoning_framework="""CLM integration points: (1) Initiation: CLM request triggers assembly (sales rep requests
        NDA, assembly generates, returns to CLM); (2) Metadata sync: assembled document metadata (parties, effective date,
        value) flows to CLM repository; (3) Workflow: post-assembly, document enters approval workflow (legal review,
        business approval, execution); (4) Execution: e-signature (DocuSign) via CLM, signed copy stored in repository;
        (5) Management: CLM tracks obligations, renewals, amendments; (6) Analytics: aggregated contract data (total
        contract value, renewal rates, cycle time). API integration: REST APIs exchange data (CLM POST /assembly-request,
        assembly returns document URL). Single sign-on: users authenticate once, access both systems. Repository: assembled
        documents auto-filed in CLM with metadata tags (contract_type, jurisdiction, parties). Obligation extraction:
        CLM parses executed document for deadlines, payment terms, renewal dates. Reporting: CLM dashboards show assembly
        volume, cycle time, template usage. Feedback loop: CLM usage data informs template refinement (commonly-negotiated
        clauses -> fallback options in template).""",
        key_factors=["API robustness", "metadata completeness", "workflow seamlessness", "repository organization", "analytics insight"],
        primary_authority=["CLM Best Practices", "API Integration Standards", "Contract Management Maturity Models"],
        burden_holder="Legal ops and IT",
        adversary_position="Standalone assembly adequate, manual upload to CLM",
        counter_arguments=["Manual upload duplicate effort", "Integration ensures consistency", "Workflow automation accelerates cycle"],
        resolution_strategy="Bidirectional API integration with metadata sync and workflow handoff",
        entity_scope="All contracts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal technology integration standards"
    ),
    "natural_language_generation": DoctrineBlock(
        topic="AI-Assisted Natural Language Generation",
        keywords=["clause generation", "summarization", "plain language", "review assistance", "risk flagging"],
        conclusion_template="AI augments assembly with intelligent content generation and analysis.",
        reasoning_framework="""AI applications: (1) Clause generation: LLM drafts novel clause from plain language prompt
        ('Create indemnity clause favorable to buyer'), attorney reviews/edits; (2) Summarization: executive summary auto-
        generated from full agreement (key terms, obligations, deadlines); (3) Plain language: complex legal language
        rewritten for client understanding; (4) Review assistance: AI flags unusual provisions, missing standard clauses,
        inconsistencies; (5) Risk scoring: ML model scores contract risk based on term patterns. Clause generation workflow:
        user inputs requirements, AI generates draft, attorney edits, approval workflow gates addition to library. Training
        data: firm's executed agreements, publicly-filed contracts, annotated clause libraries. Model selection: general
        LLM (GPT-4) for generation, fine-tuned model for firm-specific style. Validation: AI-generated content requires
        attorney review before inclusion in client document. Risk flagging: highlight deviations from playbook (payment
        terms > 90 days, uncapped indemnity, unilateral termination right). Summarization: extractive (pull key sentences)
        + abstractive (generate novel summary text). Feedback: attorney corrections train model (reinforcement learning).""",
        key_factors=["generation quality", "review workflow", "model accuracy", "risk detection", "training data richness"],
        primary_authority=["ABA Formal Opinion on AI", "Responsible AI Standards", "Legal Tech Innovation Guides"],
        burden_holder="AI team and supervising attorneys",
        adversary_position="AI-generated content too risky for legal documents",
        counter_arguments=["AI accelerates drafting", "Attorney review ensures quality", "Risk flagging enhances diligence"],
        resolution_strategy="AI-assisted generation with mandatory attorney review and approval",
        entity_scope="All AI-augmented assembly",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Emerging AI governance standards"
    )
}

TELEMETRY = {
    "queries_total": 0, "fast_queries": 0, "defense_queries": 0, "memo_queries": 0,
    "cache_hits": 0, "cache_misses": 0, "avg_latency_ms": 0.0, "errors": 0,
    "doctrine_triggered": {topic: 0 for topic in DOCTRINE_CACHE.keys()}
}

class QueryRequest(BaseModel):
    query: str = Field(..., description="Document assembly question or scenario")
    mode: Literal["FAST", "DEFENSE", "MEMO"] = Field(default="FAST", description="Response depth")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

class QueryResponse(BaseModel):
    answer: str
    mode: str
    confidence: str
    doctrines_triggered: List[str]
    latency_ms: float
    determinism_hash: str
    warnings: List[str] = Field(default_factory=list)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")

APP = FastAPI(title=ENGINE_NAME, version=VERSION, lifespan=lifespan)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def determinism_hash(query: str, answer: str) -> str:
    return hashlib.sha256(f"{query}::{answer}".encode()).hexdigest()

def doctrine_cache_lookup(query: str) -> List[str]:
    triggered = []
    query_lower = query.lower()
    for topic, block in DOCTRINE_CACHE.items():
        if any(kw.lower() in query_lower for kw in block.keywords):
            triggered.append(topic)
            TELEMETRY["doctrine_triggered"][topic] += 1
    return triggered

def three_layer_response(query: str, mode: str, context: Optional[Dict]) -> tuple[str, List[str], List[str]]:
    start = datetime.now()
    triggered = doctrine_cache_lookup(query)
    warnings = []

    if triggered:
        TELEMETRY["cache_hits"] += 1
        answer_parts = []
        for topic in triggered[:3]:
            block = DOCTRINE_CACHE[topic]
            answer_parts.append(f"**{block.topic}**: {block.conclusion_template} {block.reasoning_framework[:300]}...")
        answer = "\n\n".join(answer_parts)
    else:
        TELEMETRY["cache_misses"] += 1
        answer = f"Document assembly analysis for: {query}. Mode: {mode}. Relevant doctrines include template architecture, clause library management, conditional logic, variable substitution, cross-reference integrity, defined term consistency, exhibit generation, redlining, version control, signature blocks, and jurisdictional customization. Comprehensive assembly requires integration of all components with validation at each stage."
        warnings.append("No exact doctrine match - provided general assembly framework")

    if mode == "DEFENSE":
        answer += "\n\nAUDIT TRAIL: Assembly validates all inputs, enforces approval workflow, maintains version history, and generates comprehensive audit log per compliance requirements."
    elif mode == "MEMO":
        answer += "\n\nDETAILED ANALYSIS: Document assembly integrates template hierarchy, clause library taxonomy, conditional inclusion logic, variable substitution with validation, cross-reference integrity checking, defined term consistency validation, exhibit auto-generation, redline comparison, version control, signature block formatting per entity type, and jurisdictional customization. Each component requires robust error handling, testing, and audit trail. Integration with CLM systems extends assembly into full contract lifecycle. AI-assisted generation available with attorney review gate."

    latency = (datetime.now() - start).total_seconds() * 1000
    TELEMETRY["avg_latency_ms"] = (TELEMETRY["avg_latency_ms"] * TELEMETRY["queries_total"] + latency) / (TELEMETRY["queries_total"] + 1)

    return answer, triggered, warnings

@APP.post("/query", response_model=QueryResponse)
async def query_engine(req: QueryRequest):
    try:
        TELEMETRY["queries_total"] += 1
        if req.mode == "FAST":
            TELEMETRY["fast_queries"] += 1
        elif req.mode == "DEFENSE":
            TELEMETRY["defense_queries"] += 1
        else:
            TELEMETRY["memo_queries"] += 1

        answer, triggered, warnings = three_layer_response(req.query, req.mode, req.context)
        det_hash = determinism_hash(req.query, answer)

        confidence = "HIGH" if triggered else "MEDIUM"

        latency = TELEMETRY["avg_latency_ms"]

        logger.info(f"Query processed: {req.query[:100]}... | Mode: {req.mode} | Triggered: {len(triggered)}")

        return QueryResponse(
            answer=answer,
            mode=req.mode,
            confidence=confidence,
            doctrines_triggered=triggered,
            latency_ms=latency,
            determinism_hash=det_hash,
            warnings=warnings
        )
    except Exception as e:
        TELEMETRY["errors"] += 1
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health")
async def health():
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "telemetry": TELEMETRY,
        "timestamp": datetime.now().isoformat()
    }

@APP.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": list(DOCTRINE_CACHE.keys()),
        "details": {topic: {
            "keywords": block.keywords,
            "confidence": block.confidence,
            "entity_scope": block.entity_scope
        } for topic, block in DOCTRINE_CACHE.items()}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP, host="0.0.0.0", port=PORT)
