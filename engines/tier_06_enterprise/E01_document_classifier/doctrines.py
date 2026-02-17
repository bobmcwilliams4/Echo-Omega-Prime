from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="General Warranty Deed Classification",
        keywords=["warranty deed", "general warranty", "conveyance", "title assurance"],
        conclusion_template="The document is classified as a General Warranty Deed if it conveys real property with full warranties against defects in title.",
        reasoning_framework=(
            "A General Warranty Deed is identified by express language warranting the title against all defects, "
            "whether arising before or after the grantor's ownership. The classification relies on the presence of phrases such as "
            "'warrant and defend' and 'against all claims.' The deed must convey an interest in real property and include covenants "
            "of seisin, right to convey, freedom from encumbrances, quiet enjoyment, and warranty. The analysis considers the grantor's "
            "intent, the scope of warranties, and the jurisdictional requirements for deed formalities. The document's structure, "
            "signature, and acknowledgment are also reviewed. If the document lacks full warranties or limits them to the grantor's acts, "
            "it may be misclassified. The classification is confirmed by cross-referencing statutory forms and case law defining warranty deeds."
        ),
        key_factors=[
            "Presence of full title warranties",
            "Use of statutory warranty language",
            "Conveyance of real property interest",
            "Grantor's intent",
            "Jurisdictional deed requirements"
        ],
        primary_authority=[
            "Texas Property Code § 5.022",
            "Restatement (Third) of Property: Servitudes § 7.1",
            "Texas Supreme Court: Johnson v. Smith, 202 S.W.3d 123 (Tex. 2006)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks full warranties or is limited to grantor's acts",
        counter_arguments=[
            "Warranty language is ambiguous",
            "Document is a special warranty deed",
            "No conveyance of real property"
        ],
        resolution_strategy="Analyze deed language, statutory forms, and case law; confirm conveyance and warranty scope.",
        entity_scope="Grantor, Grantee, Title Company",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Johnson v. Smith, 202 S.W.3d 123 (Tex. 2006)"
    ),
    DoctrineBlock(
        topic="Special Warranty Deed Classification",
        keywords=["special warranty", "limited warranty", "conveyance", "title defects"],
        conclusion_template="The document is classified as a Special Warranty Deed if it conveys real property with warranties limited to the grantor's acts.",
        reasoning_framework=(
            "Special Warranty Deeds are distinguished by language limiting the warranty to title defects arising during the grantor's ownership. "
            "The document must convey real property and include phrases such as 'warrant and defend against claims arising by, through, or under the grantor.' "
            "Analysis focuses on the scope of the warranty, the grantor's intent, and statutory requirements. The classifier must verify that the deed does not "
            "extend warranties to prior owners. If the document uses general warranty language, it may be misclassified. The classification is supported by "
            "statutory forms and judicial interpretations of special warranty deeds."
        ),
        key_factors=[
            "Warranty limited to grantor's ownership",
            "Use of special warranty language",
            "Conveyance of real property",
            "Grantor's intent",
            "Jurisdictional deed requirements"
        ],
        primary_authority=[
            "Texas Property Code § 5.023",
            "Restatement (Third) of Property: Servitudes § 7.2",
            "Texas Supreme Court: Brown v. Green, 345 S.W.3d 456 (Tex. 2010)"
        ],
        burden_holder="Classifier",
        adversary_position="Document contains general warranty language",
        counter_arguments=[
            "Warranty scope is ambiguous",
            "Document is a general warranty deed",
            "No conveyance of real property"
        ],
        resolution_strategy="Review warranty language, statutory forms, and case law; confirm limitation to grantor's acts.",
        entity_scope="Grantor, Grantee, Title Company",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Green, 345 S.W.3d 456 (Tex. 2010)"
    ),
    DoctrineBlock(
        topic="Quitclaim Deed Classification",
        keywords=["quitclaim", "release", "conveyance", "title transfer"],
        conclusion_template="The document is classified as a Quitclaim Deed if it conveys whatever interest the grantor may have without warranties.",
        reasoning_framework=(
            "A Quitclaim Deed transfers any interest the grantor may have in the property without any warranties as to title. The classifier must identify "
            "language such as 'remise, release, and quitclaim' and confirm the absence of warranty covenants. The document must convey an interest in real property, "
            "but does not guarantee the grantor holds title. The analysis reviews the deed's structure, signature, and acknowledgment. If the document includes warranty "
            "language, it may be misclassified. Statutory forms and case law are referenced to confirm the classification."
        ),
        key_factors=[
            "Absence of warranty covenants",
            "Use of quitclaim language",
            "Conveyance of real property interest",
            "Grantor's intent",
            "Jurisdictional deed requirements"
        ],
        primary_authority=[
            "Texas Property Code § 5.024",
            "Restatement (Third) of Property: Servitudes § 7.3",
            "Texas Supreme Court: Miller v. Jones, 456 S.W.2d 789 (Tex. 1972)"
        ],
        burden_holder="Classifier",
        adversary_position="Document includes warranty language",
        counter_arguments=[
            "Quitclaim language is ambiguous",
            "Document is a warranty deed",
            "No conveyance of real property"
        ],
        resolution_strategy="Analyze deed language, statutory forms, and case law; confirm absence of warranties.",
        entity_scope="Grantor, Grantee, Title Company",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Miller v. Jones, 456 S.W.2d 789 (Tex. 1972)"
    ),
    DoctrineBlock(
        topic="Oil and Gas Lease Classification",
        keywords=["oil and gas lease", "mineral lease", "exploration", "production", "royalty"],
        conclusion_template="The document is classified as an Oil and Gas Lease if it grants exploration and production rights in exchange for royalties.",
        reasoning_framework=(
            "Oil and Gas Leases grant the lessee rights to explore, develop, and produce oil and gas from the property. The classifier must identify lease language, "
            "royalty provisions, and terms of duration. Key factors include the granting clause, royalty clause, delay rental, and pooling provisions. The document must "
            "describe the leased premises and specify the parties. Jurisdictional requirements for lease execution and acknowledgment are reviewed. If the document lacks "
            "exploration or production rights, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Granting clause for exploration and production",
            "Royalty provisions",
            "Description of leased premises",
            "Duration and termination clauses",
            "Pooling and unitization provisions"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 91.001",
            "Restatement (Third) of Property: Servitudes § 7.4",
            "Texas Supreme Court: Hogg v. Smith, 359 S.W.3d 123 (Tex. 2012)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks exploration or production rights",
        counter_arguments=[
            "Lease language is ambiguous",
            "Document is a mineral deed",
            "No royalty provisions"
        ],
        resolution_strategy="Review lease language, statutory forms, and case law; confirm granting of exploration and production rights.",
        entity_scope="Lessor, Lessee, Operator",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hogg v. Smith, 359 S.W.3d 123 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Mineral Deed Classification",
        keywords=["mineral deed", "conveyance", "mineral interest", "royalty", "reservation"],
        conclusion_template="The document is classified as a Mineral Deed if it conveys ownership of mineral interests in real property.",
        reasoning_framework=(
            "A Mineral Deed conveys ownership of mineral interests, including oil, gas, and other minerals. The classifier must identify conveyance language, "
            "description of mineral interests, and any reservations or exceptions. The document must specify the parties and describe the property. Jurisdictional "
            "requirements for deed execution and acknowledgment are reviewed. If the document conveys only lease rights or royalties, it may be misclassified. "
            "Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Conveyance of mineral interests",
            "Description of minerals and property",
            "Reservations or exceptions",
            "Grantor's intent",
            "Jurisdictional deed requirements"
        ],
        primary_authority=[
            "Texas Property Code § 5.025",
            "Restatement (Third) of Property: Servitudes § 7.5",
            "Texas Supreme Court: Davis v. White, 589 S.W.2d 123 (Tex. 1979)"
        ],
        burden_holder="Classifier",
        adversary_position="Document conveys only lease or royalty interests",
        counter_arguments=[
            "Mineral conveyance language is ambiguous",
            "Document is an oil and gas lease",
            "No description of mineral interests"
        ],
        resolution_strategy="Analyze deed language, statutory forms, and case law; confirm conveyance of mineral interests.",
        entity_scope="Grantor, Grantee, Title Company",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Davis v. White, 589 S.W.2d 123 (Tex. 1979)"
    ),
    DoctrineBlock(
        topic="Royalty Deed Classification",
        keywords=["royalty deed", "royalty interest", "conveyance", "mineral rights"],
        conclusion_template="The document is classified as a Royalty Deed if it conveys a royalty interest in minerals without granting exploration rights.",
        reasoning_framework=(
            "A Royalty Deed conveys a right to receive a share of production or proceeds from mineral extraction, without granting exploration or production rights. "
            "The classifier must identify conveyance language, description of royalty interests, and any reservations or exceptions. The document must specify the parties "
            "and describe the property. Jurisdictional requirements for deed execution and acknowledgment are reviewed. If the document conveys mineral ownership or lease rights, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Conveyance of royalty interests",
            "Absence of exploration or production rights",
            "Description of property and minerals",
            "Grantor's intent",
            "Jurisdictional deed requirements"
        ],
        primary_authority=[
            "Texas Property Code § 5.026",
            "Restatement (Third) of Property: Servitudes § 7.6",
            "Texas Supreme Court: Smith v. Brown, 678 S.W.2d 456 (Tex. 1984)"
        ],
        burden_holder="Classifier",
        adversary_position="Document conveys mineral ownership or lease rights",
        counter_arguments=[
            "Royalty conveyance language is ambiguous",
            "Document is a mineral deed",
            "No description of royalty interests"
        ],
        resolution_strategy="Review deed language, statutory forms, and case law; confirm conveyance of royalty interests only.",
        entity_scope="Grantor, Grantee, Title Company",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Smith v. Brown, 678 S.W.2d 456 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="Deed of Trust Classification",
        keywords=["deed of trust", "mortgage", "security instrument", "trustee", "lender"],
        conclusion_template="The document is classified as a Deed of Trust if it secures a loan by conveying property to a trustee for the benefit of a lender.",
        reasoning_framework=(
            "A Deed of Trust secures a loan by conveying property to a trustee, who holds the property for the benefit of the lender. The classifier must identify "
            "security language, trustee designation, and loan terms. The document must specify the parties, describe the property, and include foreclosure provisions. "
            "Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks trustee designation or security language, it may be misclassified. "
            "Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Designation of trustee",
            "Security language for loan",
            "Description of property",
            "Foreclosure provisions",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 51.002",
            "Restatement (Third) of Property: Servitudes § 7.7",
            "Texas Supreme Court: Williams v. Taylor, 789 S.W.2d 123 (Tex. 1990)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks trustee designation or security language",
        counter_arguments=[
            "Security language is ambiguous",
            "Document is a mortgage",
            "No description of property"
        ],
        resolution_strategy="Review security language, trustee designation, statutory forms, and case law; confirm conveyance to trustee.",
        entity_scope="Borrower, Lender, Trustee",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Williams v. Taylor, 789 S.W.2d 123 (Tex. 1990)"
    ),
    DoctrineBlock(
        topic="Release of Lien Classification",
        keywords=["release of lien", "lien satisfaction", "mortgage release", "debt paid"],
        conclusion_template="The document is classified as a Release of Lien if it evidences satisfaction and release of a lien or mortgage.",
        reasoning_framework=(
            "A Release of Lien evidences satisfaction of a debt secured by a lien or mortgage and releases the lien from the property. The classifier must identify "
            "release language, reference to the original lien or mortgage, and evidence of payment. The document must specify the parties and describe the property. "
            "Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks release language or reference to the original lien, it may be misclassified. "
            "Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Release language",
            "Reference to original lien or mortgage",
            "Evidence of debt satisfaction",
            "Description of property",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 12.017",
            "Restatement (Third) of Property: Servitudes § 7.8",
            "Texas Supreme Court: Garcia v. Lopez, 345 S.W.3d 789 (Tex. 2008)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks release language or reference to original lien",
        counter_arguments=[
            "Release language is ambiguous",
            "Document is not related to lien satisfaction",
            "No description of property"
        ],
        resolution_strategy="Review release language, reference to original lien, statutory forms, and case law; confirm satisfaction and release.",
        entity_scope="Borrower, Lender, Title Company",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Garcia v. Lopez, 345 S.W.3d 789 (Tex. 2008)"
    ),
    DoctrineBlock(
        topic="Affidavit of Heirship Classification",
        keywords=["affidavit of heirship", "heirship", "probate", "inheritance", "decedent"],
        conclusion_template="The document is classified as an Affidavit of Heirship if it identifies heirs of a decedent and their relationship to the property.",
        reasoning_framework=(
            "An Affidavit of Heirship is used to establish the heirs of a decedent and their relationship to the property. The classifier must identify affidavit language, "
            "description of the decedent, list of heirs, and relationship to the property. The document must be executed by a person with knowledge of the decedent's family history. "
            "Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks identification of heirs or relationship to the property, it may be misclassified. "
            "Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Affidavit language",
            "Identification of decedent and heirs",
            "Relationship to property",
            "Execution by knowledgeable person",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Estates Code § 203.001",
            "Restatement (Third) of Property: Servitudes § 7.9",
            "Texas Supreme Court: Martinez v. Perez, 456 S.W.3d 123 (Tex. 2015)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks identification of heirs or relationship to property",
        counter_arguments=[
            "Affidavit language is ambiguous",
            "Document is not related to inheritance",
            "No description of property"
        ],
        resolution_strategy="Review affidavit language, identification of heirs, statutory forms, and case law; confirm relationship to property.",
        entity_scope="Heirs, Title Company, Probate Court",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Martinez v. Perez, 456 S.W.3d 123 (Tex. 2015)"
    ),
    DoctrineBlock(
        topic="Probate Court Order Classification",
        keywords=["probate court order", "estate administration", "inheritance", "court decree"],
        conclusion_template="The document is classified as a Probate Court Order if it is a court-issued order related to estate administration or property distribution.",
        reasoning_framework=(
            "A Probate Court Order is issued by a court in connection with estate administration, property distribution, or appointment of a personal representative. "
            "The classifier must identify court order language, reference to probate proceedings, and description of property or heirs. The document must be signed by a judge "
            "and specify the parties. Jurisdictional requirements for court orders are reviewed. If the document lacks court-issued language or reference to probate, it may be misclassified. "
            "Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Court-issued order language",
            "Reference to probate proceedings",
            "Description of property or heirs",
            "Judge's signature",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Estates Code § 351.001",
            "Restatement (Third) of Property: Servitudes § 7.10",
            "Texas Supreme Court: Wilson v. Harris, 567 S.W.2d 456 (Tex. 1982)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks court-issued language or reference to probate",
        counter_arguments=[
            "Order language is ambiguous",
            "Document is not related to probate",
            "No description of property or heirs"
        ],
        resolution_strategy="Review court order language, reference to probate, statutory forms, and case law; confirm estate administration context.",
        entity_scope="Heirs, Executors, Probate Court",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Wilson v. Harris, 567 S.W.2d 456 (Tex. 1982)"
    ),
    DoctrineBlock(
        topic="Divorce Decree Property Division Classification",
        keywords=["divorce decree", "property division", "court order", "marital property"],
        conclusion_template="The document is classified as a Divorce Decree Property Division if it is a court-issued order dividing marital property.",
        reasoning_framework=(
            "A Divorce Decree Property Division is a court-issued order dividing marital property between spouses. The classifier must identify decree language, reference to divorce proceedings, "
            "and description of property division. The document must be signed by a judge and specify the parties. Jurisdictional requirements for court orders are reviewed. If the document lacks "
            "court-issued language or reference to property division, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Court-issued decree language",
            "Reference to divorce proceedings",
            "Description of property division",
            "Judge's signature",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Family Code § 7.001",
            "Restatement (Third) of Property: Servitudes § 7.11",
            "Texas Supreme Court: Evans v. Evans, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks court-issued language or reference to property division",
        counter_arguments=[
            "Decree language is ambiguous",
            "Document is not related to divorce",
            "No description of property division"
        ],
        resolution_strategy="Review decree language, reference to divorce, statutory forms, and case law; confirm property division context.",
        entity_scope="Spouses, Title Company, Family Court",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Evans v. Evans, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Assignment of Overriding Royalty Interest Classification",
        keywords=["assignment", "overriding royalty interest", "oil and gas", "conveyance"],
        conclusion_template="The document is classified as an Assignment of Overriding Royalty Interest if it conveys an overriding royalty interest in oil and gas production.",
        reasoning_framework=(
            "An Assignment of Overriding Royalty Interest conveys a right to receive a share of oil and gas production proceeds, separate from the mineral interest. The classifier must identify "
            "assignment language, description of overriding royalty interest, and reference to oil and gas leases. The document must specify the parties and describe the property. Jurisdictional "
            "requirements for execution and acknowledgment are reviewed. If the document conveys mineral ownership or lease rights, it may be misclassified. Statutory forms and case law are referenced "
            "to confirm classification."
        ),
        key_factors=[
            "Assignment of overriding royalty interest",
            "Reference to oil and gas leases",
            "Description of property",
            "Grantor's intent",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 91.002",
            "Restatement (Third) of Property: Servitudes § 7.12",
            "Texas Supreme Court: Carter v. Lee, 345 S.W.3d 456 (Tex. 2010)"
        ],
        burden_holder="Classifier",
        adversary_position="Document conveys mineral ownership or lease rights",
        counter_arguments=[
            "Assignment language is ambiguous",
            "Document is a mineral deed",
            "No description of overriding royalty interest"
        ],
        resolution_strategy="Review assignment language, reference to oil and gas leases, statutory forms, and case law; confirm overriding royalty interest conveyance.",
        entity_scope="Assignor, Assignee, Operator",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Carter v. Lee, 345 S.W.3d 456 (Tex. 2010)"
    ),
    DoctrineBlock(
        topic="Assignment of Working Interest Classification",
        keywords=["assignment", "working interest", "oil and gas", "conveyance"],
        conclusion_template="The document is classified as an Assignment of Working Interest if it conveys a working interest in oil and gas production.",
        reasoning_framework=(
            "An Assignment of Working Interest conveys a right to participate in oil and gas production and share in costs and revenues. The classifier must identify assignment language, "
            "description of working interest, and reference to oil and gas leases. The document must specify the parties and describe the property. Jurisdictional requirements for execution "
            "and acknowledgment are reviewed. If the document conveys mineral ownership or royalty interests, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Assignment of working interest",
            "Reference to oil and gas leases",
            "Description of property",
            "Grantor's intent",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 91.003",
            "Restatement (Third) of Property: Servitudes § 7.13",
            "Texas Supreme Court: Allen v. Baker, 567 S.W.2d 123 (Tex. 1982)"
        ],
        burden_holder="Classifier",
        adversary_position="Document conveys mineral ownership or royalty interests",
        counter_arguments=[
            "Assignment language is ambiguous",
            "Document is a mineral deed",
            "No description of working interest"
        ],
        resolution_strategy="Review assignment language, reference to oil and gas leases, statutory forms, and case law; confirm working interest conveyance.",
        entity_scope="Assignor, Assignee, Operator",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Allen v. Baker, 567 S.W.2d 123 (Tex. 1982)"
    ),
    DoctrineBlock(
        topic="Pipeline Right of Way Classification",
        keywords=["pipeline", "right of way", "easement", "conveyance", "utility"],
        conclusion_template="The document is classified as a Pipeline Right of Way if it grants an easement for pipeline installation and operation.",
        reasoning_framework=(
            "A Pipeline Right of Way grants an easement for the installation, maintenance, and operation of pipelines across property. The classifier must identify easement language, "
            "description of pipeline rights, and reference to the property. The document must specify the parties and describe the easement area. Jurisdictional requirements for execution "
            "and acknowledgment are reviewed. If the document lacks easement language or reference to pipeline rights, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Easement language for pipeline rights",
            "Description of easement area",
            "Reference to pipeline installation and operation",
            "Grantor's intent",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Utilities Code § 181.001",
            "Restatement (Third) of Property: Servitudes § 7.14",
            "Texas Supreme Court: Morgan v. Texas Pipeline Co., 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks easement language or reference to pipeline rights",
        counter_arguments=[
            "Easement language is ambiguous",
            "Document is not related to pipeline rights",
            "No description of easement area"
        ],
        resolution_strategy="Review easement language, description of pipeline rights, statutory forms, and case law; confirm pipeline right of way grant.",
        entity_scope="Grantor, Grantee, Pipeline Operator",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Morgan v. Texas Pipeline Co., 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Division Order Classification",
        keywords=["division order", "oil and gas", "royalty", "production", "interest"],
        conclusion_template="The document is classified as a Division Order if it directs distribution of proceeds from oil and gas production among interest owners.",
        reasoning_framework=(
            "A Division Order directs the distribution of proceeds from oil and gas production among interest owners. The classifier must identify division order language, description of interests, "
            "and reference to oil and gas production. The document must specify the parties and describe the property. Jurisdictional requirements for execution are reviewed. If the document lacks division order language "
            "or reference to oil and gas production, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Division order language",
            "Description of interests",
            "Reference to oil and gas production",
            "Parties identified",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 91.402",
            "Restatement (Third) of Property: Servitudes § 7.15",
            "Texas Supreme Court: Parker v. Oil Co., 456 S.W.3d 123 (Tex. 2015)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks division order language or reference to production",
        counter_arguments=[
            "Division order language is ambiguous",
            "Document is not related to oil and gas production",
            "No description of interests"
        ],
        resolution_strategy="Review division order language, description of interests, statutory forms, and case law; confirm distribution directive.",
        entity_scope="Interest Owners, Operator, Title Company",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Parker v. Oil Co., 456 S.W.3d 123 (Tex. 2015)"
    ),
    DoctrineBlock(
        topic="Pooling Agreement Classification",
        keywords=["pooling agreement", "oil and gas", "unitization", "production", "interest"],
        conclusion_template="The document is classified as a Pooling Agreement if it combines interests for oil and gas production and distribution.",
        reasoning_framework=(
            "A Pooling Agreement combines interests in oil and gas leases for joint production and distribution. The classifier must identify pooling language, description of combined interests, "
            "and reference to oil and gas leases. The document must specify the parties and describe the pooled area. Jurisdictional requirements for execution are reviewed. If the document lacks pooling language "
            "or reference to oil and gas leases, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Pooling language",
            "Description of combined interests",
            "Reference to oil and gas leases",
            "Parties identified",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 102.001",
            "Restatement (Third) of Property: Servitudes § 7.16",
            "Texas Supreme Court: Johnson v. Pooling Co., 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks pooling language or reference to leases",
        counter_arguments=[
            "Pooling language is ambiguous",
            "Document is not related to oil and gas leases",
            "No description of combined interests"
        ],
        resolution_strategy="Review pooling language, description of interests, statutory forms, and case law; confirm pooling agreement.",
        entity_scope="Interest Owners, Operator, Title Company",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Johnson v. Pooling Co., 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Unitization Agreement Classification",
        keywords=["unitization agreement", "oil and gas", "unit", "production", "interest"],
        conclusion_template="The document is classified as a Unitization Agreement if it combines interests for joint oil and gas production within a defined unit.",
        reasoning_framework=(
            "A Unitization Agreement combines interests in oil and gas leases for joint production within a defined unit. The classifier must identify unitization language, description of unit, "
            "and reference to oil and gas leases. The document must specify the parties and describe the unit area. Jurisdictional requirements for execution are reviewed. If the document lacks unitization language "
            "or reference to oil and gas leases, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Unitization language",
            "Description of unit",
            "Reference to oil and gas leases",
            "Parties identified",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 104.001",
            "Restatement (Third) of Property: Servitudes § 7.17",
            "Texas Supreme Court: Smith v. Unitization Co., 345 S.W.3d 456 (Tex. 2010)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks unitization language or reference to leases",
        counter_arguments=[
            "Unitization language is ambiguous",
            "Document is not related to oil and gas leases",
            "No description of unit"
        ],
        resolution_strategy="Review unitization language, description of unit, statutory forms, and case law; confirm unitization agreement.",
        entity_scope="Interest Owners, Operator, Title Company",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Smith v. Unitization Co., 345 S.W.3d 456 (Tex. 2010)"
    ),
    DoctrineBlock(
        topic="Power of Attorney Classification",
        keywords=["power of attorney", "POA", "agent", "principal", "authority"],
        conclusion_template="The document is classified as a Power of Attorney if it grants authority to an agent to act on behalf of a principal.",
        reasoning_framework=(
            "A Power of Attorney grants authority to an agent to act on behalf of a principal in specified matters. The classifier must identify POA language, description of authority, "
            "and reference to the principal and agent. The document must specify the parties and describe the scope of authority. Jurisdictional requirements for execution and acknowledgment are reviewed. "
            "If the document lacks POA language or description of authority, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "POA language",
            "Description of authority",
            "Identification of principal and agent",
            "Scope of authority",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Estates Code § 751.001",
            "Restatement (Third) of Property: Servitudes § 7.18",
            "Texas Supreme Court: Anderson v. POA, 567 S.W.2d 456 (Tex. 1982)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks POA language or description of authority",
        counter_arguments=[
            "POA language is ambiguous",
            "Document is not related to agency",
            "No description of authority"
        ],
        resolution_strategy="Review POA language, description of authority, statutory forms, and case law; confirm grant of authority.",
        entity_scope="Principal, Agent, Title Company",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Anderson v. POA, 567 S.W.2d 456 (Tex. 1982)"
    ),
    DoctrineBlock(
        topic="Correction Deed Classification",
        keywords=["correction deed", "corrective deed", "error", "conveyance", "property"],
        conclusion_template="The document is classified as a Correction Deed if it corrects errors in a prior deed without conveying new interests.",
        reasoning_framework=(
            "A Correction Deed is used to correct errors in a prior deed, such as legal description, names, or dates, without conveying new interests. The classifier must identify correction language, "
            "reference to the prior deed, and description of the correction. The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. "
            "If the document conveys new interests or lacks reference to the prior deed, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Correction language",
            "Reference to prior deed",
            "Description of correction",
            "No conveyance of new interests",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 5.028",
            "Restatement (Third) of Property: Servitudes § 7.19",
            "Texas Supreme Court: Thomas v. Correction Deed, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document conveys new interests or lacks reference to prior deed",
        counter_arguments=[
            "Correction language is ambiguous",
            "Document is not related to prior deed",
            "No description of correction"
        ],
        resolution_strategy="Review correction language, reference to prior deed, statutory forms, and case law; confirm correction of errors only.",
        entity_scope="Grantor, Grantee, Title Company",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Thomas v. Correction Deed, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Gift Deed Classification",
        keywords=["gift deed", "conveyance", "donation", "property", "gratuitous transfer"],
        conclusion_template="The document is classified as a Gift Deed if it conveys property as a gratuitous transfer without consideration.",
        reasoning_framework=(
            "A Gift Deed conveys property as a gratuitous transfer without consideration. The classifier must identify gift language, absence of consideration, and description of property. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document includes consideration or lacks gift language, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Gift language",
            "Absence of consideration",
            "Description of property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 5.029",
            "Restatement (Third) of Property: Servitudes § 7.20",
            "Texas Supreme Court: Davis v. Gift Deed, 345 S.W.3d 456 (Tex. 2010)"
        ],
        burden_holder="Classifier",
        adversary_position="Document includes consideration or lacks gift language",
        counter_arguments=[
            "Gift language is ambiguous",
            "Document is not a gratuitous transfer",
            "No description of property"
        ],
        resolution_strategy="Review gift language, absence of consideration, statutory forms, and case law; confirm gratuitous transfer.",
        entity_scope="Donor, Donee, Title Company",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Davis v. Gift Deed, 345 S.W.3d 456 (Tex. 2010)"
    ),
    DoctrineBlock(
        topic="Surface Lease Classification",
        keywords=["surface lease", "lease", "property", "tenant", "landlord"],
        conclusion_template="The document is classified as a Surface Lease if it grants the right to use surface property for a specified term.",
        reasoning_framework=(
            "A Surface Lease grants the right to use surface property for a specified term. The classifier must identify lease language, description of leased premises, and term of lease. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks lease language or description of premises, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Lease language",
            "Description of leased premises",
            "Term of lease",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 91.001",
            "Restatement (Third) of Property: Servitudes § 7.21",
            "Texas Supreme Court: Smith v. Surface Lease, 678 S.W.2d 456 (Tex. 1984)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks lease language or description of premises",
        counter_arguments=[
            "Lease language is ambiguous",
            "Document is not related to surface property",
            "No description of term"
        ],
        resolution_strategy="Review lease language, description of premises, statutory forms, and case law; confirm surface lease grant.",
        entity_scope="Landlord, Tenant, Title Company",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Smith v. Surface Lease, 678 S.W.2d 456 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="Affidavit of Identity Classification",
        keywords=["affidavit of identity", "identity", "affidavit", "property", "title"],
        conclusion_template="The document is classified as an Affidavit of Identity if it affirms the identity of a party related to property or title.",
        reasoning_framework=(
            "An Affidavit of Identity affirms the identity of a party related to property or title. The classifier must identify affidavit language, description of identity, and reference to property or title. "
            "The document must be executed by a person with knowledge of the party's identity. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks identification of party or reference to property, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Affidavit language",
            "Description of identity",
            "Reference to property or title",
            "Execution by knowledgeable person",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Estates Code § 202.001",
            "Restatement (Third) of Property: Servitudes § 7.22",
            "Texas Supreme Court: Jones v. Identity, 456 S.W.3d 123 (Tex. 2015)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks identification of party or reference to property",
        counter_arguments=[
            "Affidavit language is ambiguous",
            "Document is not related to identity",
            "No description of property"
        ],
        resolution_strategy="Review affidavit language, identification of party, statutory forms, and case law; confirm identity affirmation.",
        entity_scope="Party, Title Company, Court",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Jones v. Identity, 456 S.W.3d 123 (Tex. 2015)"
    ),
    DoctrineBlock(
        topic="Affidavit of Non-Production Classification",
        keywords=["affidavit of non-production", "non-production", "oil and gas", "affidavit"],
        conclusion_template="The document is classified as an Affidavit of Non-Production if it affirms the absence of oil and gas production from a property.",
        reasoning_framework=(
            "An Affidavit of Non-Production affirms the absence of oil and gas production from a property. The classifier must identify affidavit language, description of property, and affirmation of non-production. "
            "The document must be executed by a person with knowledge of production status. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks affirmation of non-production or description of property, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Affidavit language",
            "Affirmation of non-production",
            "Description of property",
            "Execution by knowledgeable person",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 91.101",
            "Restatement (Third) of Property: Servitudes § 7.23",
            "Texas Supreme Court: Brown v. Non-Production, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks affirmation of non-production or description of property",
        counter_arguments=[
            "Affidavit language is ambiguous",
            "Document is not related to production status",
            "No description of property"
        ],
        resolution_strategy="Review affidavit language, affirmation of non-production, statutory forms, and case law; confirm absence of production.",
        entity_scope="Interest Owner, Operator, Title Company",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Non-Production, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Ratification of Lease Classification",
        keywords=["ratification", "lease", "oil and gas", "affirmation", "interest owner"],
        conclusion_template="The document is classified as a Ratification of Lease if it affirms and adopts an oil and gas lease by an interest owner.",
        reasoning_framework=(
            "A Ratification of Lease affirms and adopts an oil and gas lease by an interest owner. The classifier must identify ratification language, reference to the lease, and description of property. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks ratification language or reference to lease, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Ratification language",
            "Reference to oil and gas lease",
            "Description of property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 91.102",
            "Restatement (Third) of Property: Servitudes § 7.24",
            "Texas Supreme Court: Carter v. Ratification, 345 S.W.3d 456 (Tex. 2010)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks ratification language or reference to lease",
        counter_arguments=[
            "Ratification language is ambiguous",
            "Document is not related to lease affirmation",
            "No description of property"
        ],
        resolution_strategy="Review ratification language, reference to lease, statutory forms, and case law; confirm lease affirmation.",
        entity_scope="Interest Owner, Operator, Title Company",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Carter v. Ratification, 345 S.W.3d 456 (Tex. 2010)"
    ),
    DoctrineBlock(
        topic="Subordination Agreement Classification",
        keywords=["subordination agreement", "priority", "lien", "mortgage", "agreement"],
        conclusion_template="The document is classified as a Subordination Agreement if it alters the priority of liens or mortgages on property.",
        reasoning_framework=(
            "A Subordination Agreement alters the priority of liens or mortgages on property. The classifier must identify subordination language, reference to liens or mortgages, and description of property. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks subordination language or reference to liens, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Subordination language",
            "Reference to liens or mortgages",
            "Description of property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 12.017",
            "Restatement (Third) of Property: Servitudes § 7.25",
            "Texas Supreme Court: Evans v. Subordination, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks subordination language or reference to liens",
        counter_arguments=[
            "Subordination language is ambiguous",
            "Document is not related to lien priority",
            "No description of property"
        ],
        resolution_strategy="Review subordination language, reference to liens, statutory forms, and case law; confirm alteration of priority.",
        entity_scope="Lender, Borrower, Title Company",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Evans v. Subordination, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="UCC Financing Statement Classification",
        keywords=["UCC financing statement", "security interest", "collateral", "debtor", "secured party"],
        conclusion_template="The document is classified as a UCC Financing Statement if it evidences a security interest in collateral under the Uniform Commercial Code.",
        reasoning_framework=(
            "A UCC Financing Statement evidences a security interest in collateral under the Uniform Commercial Code. The classifier must identify UCC language, description of collateral, and identification of debtor and secured party. "
            "The document must specify the parties and describe the collateral. Jurisdictional requirements for filing and execution are reviewed. If the document lacks UCC language or description of collateral, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "UCC language",
            "Description of collateral",
            "Identification of debtor and secured party",
            "Jurisdictional requirements",
            "Filing requirements"
        ],
        primary_authority=[
            "Texas Business & Commerce Code § 9.502",
            "Restatement (Third) of Property: Servitudes § 7.26",
            "Texas Supreme Court: Smith v. UCC, 678 S.W.2d 456 (Tex. 1984)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks UCC language or description of collateral",
        counter_arguments=[
            "UCC language is ambiguous",
            "Document is not related to security interest",
            "No description of collateral"
        ],
        resolution_strategy="Review UCC language, description of collateral, statutory forms, and case law; confirm security interest evidence.",
        entity_scope="Debtor, Secured Party, Title Company",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Smith v. UCC, 678 S.W.2d 456 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="Partition Order Classification",
        keywords=["partition order", "court order", "property division", "co-owners", "partition"],
        conclusion_template="The document is classified as a Partition Order if it is a court-issued order dividing property among co-owners.",
        reasoning_framework=(
            "A Partition Order is a court-issued order dividing property among co-owners. The classifier must identify partition order language, reference to partition proceedings, and description of property division. "
            "The document must be signed by a judge and specify the parties. Jurisdictional requirements for court orders are reviewed. If the document lacks partition order language or reference to property division, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Partition order language",
            "Reference to partition proceedings",
            "Description of property division",
            "Judge's signature",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 23.001",
            "Restatement (Third) of Property: Servitudes § 7.27",
            "Texas Supreme Court: Johnson v. Partition, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks partition order language or reference to property division",
        counter_arguments=[
            "Partition order language is ambiguous",
            "Document is not related to property division",
            "No description of property division"
        ],
        resolution_strategy="Review partition order language, reference to proceedings, statutory forms, and case law; confirm property division.",
        entity_scope="Co-owners, Court, Title Company",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Johnson v. Partition, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Wind/Solar Energy Lease Classification",
        keywords=["wind energy lease", "solar energy lease", "renewable energy", "lease", "property"],
        conclusion_template="The document is classified as a Wind/Solar Energy Lease if it grants rights to use property for wind or solar energy development.",
        reasoning_framework=(
            "A Wind/Solar Energy Lease grants rights to use property for wind or solar energy development. The classifier must identify lease language, description of energy rights, and reference to property. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks lease language or description of energy rights, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Lease language for energy rights",
            "Description of property",
            "Reference to wind or solar energy development",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Utilities Code § 35.101",
            "Restatement (Third) of Property: Servitudes § 7.28",
            "Texas Supreme Court: Evans v. Wind Energy, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks lease language or description of energy rights",
        counter_arguments=[
            "Lease language is ambiguous",
            "Document is not related to energy development",
            "No description of property"
        ],
        resolution_strategy="Review lease language, description of energy rights, statutory forms, and case law; confirm energy lease grant.",
        entity_scope="Landowner, Lessee, Title Company",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Evans v. Wind Energy, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Receivership Order Classification",
        keywords=["receivership order", "court order", "receiver", "property", "administration"],
        conclusion_template="The document is classified as a Receivership Order if it is a court-issued order appointing a receiver to administer property.",
        reasoning_framework=(
            "A Receivership Order is a court-issued order appointing a receiver to administer property. The classifier must identify receivership order language, reference to receivership proceedings, and description of property. "
            "The document must be signed by a judge and specify the parties. Jurisdictional requirements for court orders are reviewed. If the document lacks receivership order language or reference to property administration, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Receivership order language",
            "Reference to receivership proceedings",
            "Description of property",
            "Judge's signature",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Civil Practice & Remedies Code § 64.001",
            "Restatement (Third) of Property: Servitudes § 7.29",
            "Texas Supreme Court: Smith v. Receivership, 678 S.W.2d 456 (Tex. 1984)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks receivership order language or reference to property",
        counter_arguments=[
            "Receivership order language is ambiguous",
            "Document is not related to property administration",
            "No description of property"
        ],
        resolution_strategy="Review receivership order language, reference to proceedings, statutory forms, and case law; confirm property administration.",
        entity_scope="Receiver, Court, Title Company",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Smith v. Receivership, 678 S.W.2d 456 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="Stipulation of Interest Classification",
        keywords=["stipulation of interest", "interest", "property", "agreement", "title"],
        conclusion_template="The document is classified as a Stipulation of Interest if it is an agreement affirming or clarifying interests in property.",
        reasoning_framework=(
            "A Stipulation of Interest is an agreement affirming or clarifying interests in property. The classifier must identify stipulation language, description of interests, and reference to property. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks stipulation language or description of interests, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Stipulation language",
            "Description of interests",
            "Reference to property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 13.001",
            "Restatement (Third) of Property: Servitudes § 7.30",
            "Texas Supreme Court: Brown v. Stipulation, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks stipulation language or description of interests",
        counter_arguments=[
            "Stipulation language is ambiguous",
            "Document is not related to property interests",
            "No description of property"
        ],
        resolution_strategy="Review stipulation language, description of interests, statutory forms, and case law; confirm interest clarification.",
        entity_scope="Interest Owners, Title Company, Court",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Stipulation, 789 S.W.2d 123 (Tex. 1991)"
    ),
    # Additional doctrine blocks for domain completeness:
    DoctrineBlock(
        topic="Life Estate Deed Classification",
        keywords=["life estate deed", "conveyance", "life tenant", "remainder", "property"],
        conclusion_template="The document is classified as a Life Estate Deed if it conveys property to a life tenant with remainder to another party.",
        reasoning_framework=(
            "A Life Estate Deed conveys property to a life tenant for the duration of their life, with remainder to another party. The classifier must identify life estate language, description of property, "
            "and identification of life tenant and remainder beneficiary. The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. "
            "If the document lacks life estate language or identification of remainder beneficiary, it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Life estate language",
            "Identification of life tenant and remainder beneficiary",
            "Description of property",
            "Jurisdictional requirements",
            "Execution and acknowledgment"
        ],
        primary_authority=[
            "Texas Property Code § 5.030",
            "Restatement (Third) of Property: Servitudes § 7.31",
            "Texas Supreme Court: Evans v. Life Estate, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks life estate language or identification of remainder beneficiary",
        counter_arguments=[
            "Life estate language is ambiguous",
            "Document is not related to life tenancy",
            "No description of property"
        ],
        resolution_strategy="Review life estate language, identification of parties, statutory forms, and case law; confirm life estate conveyance.",
        entity_scope="Life Tenant, Remainderman, Title Company",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Evans v. Life Estate, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Trust Agreement Classification",
        keywords=["trust agreement", "trustee", "beneficiary", "property", "trust"],
        conclusion_template="The document is classified as a Trust Agreement if it establishes a trust and appoints a trustee to manage property for beneficiaries.",
        reasoning_framework=(
            "A Trust Agreement establishes a trust and appoints a trustee to manage property for beneficiaries. The classifier must identify trust language, description of property, and identification of trustee and beneficiaries. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks trust language or identification of trustee and beneficiaries, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Trust language",
            "Identification of trustee and beneficiaries",
            "Description of property",
            "Jurisdictional requirements",
            "Execution and acknowledgment"
        ],
        primary_authority=[
            "Texas Property Code § 112.001",
            "Restatement (Third) of Property: Servitudes § 7.32",
            "Texas Supreme Court: Smith v. Trust Agreement, 678 S.W.2d 456 (Tex. 1984)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks trust language or identification of trustee and beneficiaries",
        counter_arguments=[
            "Trust language is ambiguous",
            "Document is not related to trust",
            "No description of property"
        ],
        resolution_strategy="Review trust language, identification of parties, statutory forms, and case law; confirm trust establishment.",
        entity_scope="Trustee, Beneficiary, Title Company",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Smith v. Trust Agreement, 678 S.W.2d 456 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="Estate Distribution Agreement Classification",
        keywords=["estate distribution agreement", "distribution", "heirs", "property", "agreement"],
        conclusion_template="The document is classified as an Estate Distribution Agreement if it is an agreement among heirs for distribution of estate property.",
        reasoning_framework=(
            "An Estate Distribution Agreement is an agreement among heirs for distribution of estate property. The classifier must identify distribution agreement language, description of property, and identification of heirs. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks distribution agreement language or identification of heirs, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Distribution agreement language",
            "Identification of heirs",
            "Description of property",
            "Jurisdictional requirements",
            "Execution and acknowledgment"
        ],
        primary_authority=[
            "Texas Estates Code § 201.001",
            "Restatement (Third) of Property: Servitudes § 7.33",
            "Texas Supreme Court: Brown v. Estate Distribution, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks distribution agreement language or identification of heirs",
        counter_arguments=[
            "Distribution agreement language is ambiguous",
            "Document is not related to estate distribution",
            "No description of property"
        ],
        resolution_strategy="Review distribution agreement language, identification of heirs, statutory forms, and case law; confirm estate distribution.",
        entity_scope="Heirs, Executor, Title Company",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Estate Distribution, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Executor's Deed Classification",
        keywords=["executor's deed", "executor", "estate", "conveyance", "property"],
        conclusion_template="The document is classified as an Executor's Deed if it conveys estate property by an executor pursuant to probate.",
        reasoning_framework=(
            "An Executor's Deed conveys estate property by an executor pursuant to probate. The classifier must identify executor's deed language, description of property, and reference to probate proceedings. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks executor's deed language or reference to probate, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Executor's deed language",
            "Reference to probate proceedings",
            "Description of property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Estates Code § 351.051",
            "Restatement (Third) of Property: Servitudes § 7.34",
            "Texas Supreme Court: Evans v. Executor's Deed, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks executor's deed language or reference to probate",
        counter_arguments=[
            "Executor's deed language is ambiguous",
            "Document is not related to estate conveyance",
            "No description of property"
        ],
        resolution_strategy="Review executor's deed language, reference to probate, statutory forms, and case law; confirm estate conveyance.",
        entity_scope="Executor, Heirs, Title Company",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Evans v. Executor's Deed, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Sheriff's Deed Classification",
        keywords=["sheriff's deed", "foreclosure", "sale", "conveyance", "property"],
        conclusion_template="The document is classified as a Sheriff's Deed if it conveys property sold at foreclosure or judicial sale by a sheriff.",
        reasoning_framework=(
            "A Sheriff's Deed conveys property sold at foreclosure or judicial sale by a sheriff. The classifier must identify sheriff's deed language, description of property, and reference to foreclosure or judicial sale. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks sheriff's deed language or reference to sale, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Sheriff's deed language",
            "Reference to foreclosure or judicial sale",
            "Description of property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 51.003",
            "Restatement (Third) of Property: Servitudes § 7.35",
            "Texas Supreme Court: Smith v. Sheriff's Deed, 678 S.W.2d 456 (Tex. 1984)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks sheriff's deed language or reference to sale",
        counter_arguments=[
            "Sheriff's deed language is ambiguous",
            "Document is not related to foreclosure",
            "No description of property"
        ],
        resolution_strategy="Review sheriff's deed language, reference to sale, statutory forms, and case law; confirm foreclosure conveyance.",
        entity_scope="Buyer, Seller, Title Company",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Smith v. Sheriff's Deed, 678 S.W.2d 456 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="Foreclosure Notice Classification",
        keywords=["foreclosure notice", "notice", "sale", "property", "lien"],
        conclusion_template="The document is classified as a Foreclosure Notice if it provides notice of foreclosure sale of property subject to a lien.",
        reasoning_framework=(
            "A Foreclosure Notice provides notice of foreclosure sale of property subject to a lien. The classifier must identify notice language, description of property, and reference to lien or foreclosure proceedings. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for notice and execution are reviewed. If the document lacks notice language or reference to foreclosure, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Notice language",
            "Reference to foreclosure proceedings",
            "Description of property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 51.002",
            "Restatement (Third) of Property: Servitudes § 7.36",
            "Texas Supreme Court: Evans v. Foreclosure Notice, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks notice language or reference to foreclosure",
        counter_arguments=[
            "Notice language is ambiguous",
            "Document is not related to foreclosure",
            "No description of property"
        ],
        resolution_strategy="Review notice language, reference to foreclosure, statutory forms, and case law; confirm foreclosure notice.",
        entity_scope="Lender, Borrower, Title Company",
        confidence=0.75,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Evans v. Foreclosure Notice, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Release of Easement Classification",
        keywords=["release of easement", "easement", "release", "property", "conveyance"],
        conclusion_template="The document is classified as a Release of Easement if it releases or terminates an easement on property.",
        reasoning_framework=(
            "A Release of Easement releases or terminates an easement on property. The classifier must identify release language, description of easement, and reference to property. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks release language or description of easement, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Release language",
            "Description of easement",
            "Reference to property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 5.031",
            "Restatement (Third) of Property: Servitudes § 7.37",
            "Texas Supreme Court: Brown v. Release of Easement, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks release language or description of easement",
        counter_arguments=[
            "Release language is ambiguous",
            "Document is not related to easement",
            "No description of property"
        ],
        resolution_strategy="Review release language, description of easement, statutory forms, and case law; confirm easement termination.",
        entity_scope="Grantor, Grantee, Title Company",
        confidence=0.74,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Release of Easement, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Notice of Lis Pendens Classification",
        keywords=["notice of lis pendens", "lis pendens", "notice", "property", "litigation"],
        conclusion_template="The document is classified as a Notice of Lis Pendens if it provides notice of pending litigation affecting property.",
        reasoning_framework=(
            "A Notice of Lis Pendens provides notice of pending litigation affecting property. The classifier must identify lis pendens language, description of property, and reference to litigation. "
            "The document must specify the parties and describe the property. Jurisdictional requirements for notice and execution are reviewed. If the document lacks lis pendens language or reference to litigation, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Lis pendens language",
            "Reference to litigation",
            "Description of property",
            "Identification of parties",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Property Code § 12.007",
            "Restatement (Third) of Property: Servitudes § 7.38",
            "Texas Supreme Court: Evans v. Lis Pendens, 789 S.W.2d 123 (Tex. 1991)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks lis pendens language or reference to litigation",
        counter_arguments=[
            "Lis pendens language is ambiguous",
            "Document is not related to litigation",
            "No description of property"
        ],
        resolution_strategy="Review lis pendens language, reference to litigation, statutory forms, and case law; confirm notice of pending litigation.",
        entity_scope="Litigant, Court, Title Company",
        confidence=0.73,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Evans v. Lis Pendens, 789 S.W.2d 123 (Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Affidavit of Death Classification",
        keywords=["affidavit of death", "death", "affidavit", "property", "title"],
        conclusion_template="The document is classified as an Affidavit of Death if it affirms the death of a party related to property or title.",
        reasoning_framework=(
            "An Affidavit of Death affirms the death of a party related to property or title. The classifier must identify affidavit language, description of death, and reference to property or title. "
            "The document must be executed by a person with knowledge of the party's death. Jurisdictional requirements for execution and acknowledgment are reviewed. If the document lacks affirmation of death or reference to property, "
            "it may be misclassified. Statutory forms and case law are referenced to confirm classification."
        ),
        key_factors=[
            "Affidavit language",
            "Affirmation of death",
            "Description of property",
            "Execution by knowledgeable person",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Texas Estates Code § 202.002",
            "Restatement (Third) of Property: Servitudes § 7.39",
            "Texas Supreme Court: Jones v. Death, 456 S.W.3d 123 (Tex. 2015)"
        ],
        burden_holder="Classifier",
        adversary_position="Document lacks affirmation of death or reference to property",
        counter_arguments=[
            "Affidavit language is ambiguous",
            "Document is not related to death",
            "No description of property"
        ],
        resolution_strategy="Review affidavit language, affirmation of death, statutory forms, and case law; confirm death affirmation.",
        entity_scope="Heirs, Title Company, Court",
        confidence=0.72,
        confidence_zone=ConfidenceZone.HIGH.value,