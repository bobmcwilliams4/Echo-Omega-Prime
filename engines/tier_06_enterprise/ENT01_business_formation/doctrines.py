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
        topic="LLC Formation Requirements Under TBOC",
        keywords=["LLC", "formation", "Texas", "TBOC", "certificate of formation", "organizational documents"],
        conclusion_template="An LLC is properly formed under the Texas Business Organizations Code (TBOC) if the certificate of formation is filed with the Texas Secretary of State and complies with statutory requirements.",
        reasoning_framework="""
        The Texas Business Organizations Code (TBOC) governs the formation of limited liability companies (LLCs) in Texas. The process requires filing a certificate of formation with the Secretary of State, which must include the LLC's name, duration, purpose, address, registered agent, and management structure. The certificate must comply with TBOC §§ 101.101–101.105. The LLC becomes a legal entity upon acceptance of the filing. Failure to comply with statutory requirements may result in rejection or defective formation, impacting liability and enforceability of contracts. The doctrine considers whether all statutory elements are satisfied, and whether any defects are curable under TBOC § 4.007. The burden is on the party asserting proper formation, and challenges may arise from creditors or members disputing validity. Resolution involves reviewing the filed certificate, statutory compliance, and any curative amendments.
        """,
        key_factors=[
            "Certificate of formation filed",
            "Compliance with TBOC §§ 101.101–101.105",
            "Registered agent designation",
            "Management structure disclosure",
            "Acceptance by Secretary of State"
        ],
        primary_authority=[
            "Texas Business Organizations Code §§ 101.101–101.105",
            "TBOC § 4.007",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC organizer or proponent",
        adversary_position="Challenger claims defective formation or non-compliance",
        counter_arguments=[
            "Defective certificate can be amended",
            "Substantial compliance doctrine",
            "De facto LLC status"
        ],
        resolution_strategy="Review certificate, statutory compliance, and curative amendments; apply substantial compliance doctrine if appropriate.",
        entity_scope="LLC",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re First Multi-Family Ltd. Co., 122 S.W.3d 823 (Tex. App. 2003)"
    ),
    DoctrineBlock(
        topic="LLC Member-Managed vs Manager-Managed",
        keywords=["LLC", "management", "member-managed", "manager-managed", "governance", "operating agreement"],
        conclusion_template="An LLC is member-managed unless the certificate of formation or operating agreement expressly provides for manager-management.",
        reasoning_framework="""
        Under TBOC §§ 101.251–101.254, the management structure of an LLC is determined by the certificate of formation and the operating agreement. By default, Texas LLCs are member-managed unless the certificate or operating agreement designates manager-management. The distinction affects authority to bind the LLC, fiduciary duties, and liability. Member-managed LLCs grant management rights to all members; manager-managed LLCs restrict management to designated managers. The doctrine evaluates the governing documents, statutory defaults, and any amendments. The burden is on the party asserting manager-management to show express designation. Disputes may arise over implied authority or ambiguous documents. Resolution involves interpreting the certificate and operating agreement, applying statutory defaults, and considering extrinsic evidence if necessary.
        """,
        key_factors=[
            "Certificate of formation designation",
            "Operating agreement provisions",
            "Statutory default",
            "Member consent",
            "Authority to bind LLC"
        ],
        primary_authority=[
            "TBOC §§ 101.251–101.254",
            "TBOC § 101.101",
            "Texas case law on LLC management"
        ],
        burden_holder="Party asserting manager-management",
        adversary_position="Opposing party claims member-management or ambiguous designation",
        counter_arguments=[
            "Implied authority from conduct",
            "Ambiguity resolved in favor of member-management",
            "Extrinsic evidence admissible"
        ],
        resolution_strategy="Interpret governing documents; apply statutory default; consider extrinsic evidence if ambiguity exists.",
        entity_scope="LLC",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Tex. Bus. Org. Code § 101.251; Ritchie v. Rupe, 443 S.W.3d 856 (Tex. 2014)"
    ),
    DoctrineBlock(
        topic="Corporation Formation C-Corp vs S-Corp",
        keywords=["corporation", "C-Corp", "S-Corp", "formation", "IRS election", "certificate of formation"],
        conclusion_template="A Texas corporation is formed as a C-Corp by default; S-Corp status requires IRS election after formation.",
        reasoning_framework="""
        The Texas Business Organizations Code governs the formation of corporations, requiring a certificate of formation filed with the Secretary of State. By default, corporations are taxed as C-Corps. S-Corp status is not a state law entity type but a federal tax election under IRC § 1362. To qualify, the corporation must meet IRS requirements, including shareholder limits, domestic status, and single class of stock. The doctrine distinguishes between state law formation and federal tax classification. The burden is on the party asserting S-Corp status to show valid IRS election and compliance. Disputes may arise over eligibility or improper election. Resolution involves reviewing formation documents, IRS filings, and shareholder structure.
        """,
        key_factors=[
            "Certificate of formation filed",
            "IRS Form 2553 election",
            "Shareholder eligibility",
            "Single class of stock",
            "Compliance with IRC § 1361"
        ],
        primary_authority=[
            "TBOC §§ 21.101–21.105",
            "Internal Revenue Code §§ 1361–1362",
            "IRS Form 2553 instructions"
        ],
        burden_holder="Corporation seeking S-Corp status",
        adversary_position="IRS or challenger disputes S-Corp eligibility",
        counter_arguments=[
            "Failure to meet shareholder requirements",
            "Improper or late election",
            "Multiple classes of stock"
        ],
        resolution_strategy="Review formation documents, IRS filings, and shareholder structure; cure defects if possible.",
        entity_scope="Corporation",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRC § 1362; TBOC § 21.101"
    ),
    DoctrineBlock(
        topic="General Partnership Formation by Operation of Law",
        keywords=["general partnership", "operation of law", "formation", "joint business", "profit sharing"],
        conclusion_template="A general partnership is formed by operation of law when two or more persons associate to carry on a business for profit, regardless of formal agreement.",
        reasoning_framework="""
        Under TBOC §§ 152.051–152.052, a general partnership arises by operation of law when two or more persons agree to carry on a business for profit, sharing profits and losses. No filing or formal agreement is required. The doctrine evaluates conduct, profit sharing, and mutual agency. The burden is on the party asserting partnership existence to show requisite elements. Disputes may arise over intent, profit sharing, or exclusion of partnership status. Resolution involves analyzing conduct, agreements, and statutory factors, including the "partnership by estoppel" doctrine.
        """,
        key_factors=[
            "Association of two or more persons",
            "Business for profit",
            "Profit sharing",
            "Mutual agency",
            "Intent to form partnership"
        ],
        primary_authority=[
            "TBOC §§ 152.051–152.052",
            "Texas case law on partnership formation"
        ],
        burden_holder="Party asserting partnership existence",
        adversary_position="Opposing party denies partnership or claims lack of intent",
        counter_arguments=[
            "No profit sharing",
            "No mutual agency",
            "Express exclusion of partnership"
        ],
        resolution_strategy="Analyze conduct, agreements, and statutory factors; apply partnership by estoppel if appropriate.",
        entity_scope="General Partnership",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ingram v. Deere, 288 S.W.3d 886 (Tex. 2009)"
    ),
    DoctrineBlock(
        topic="Limited Partnership Formation Requirements",
        keywords=["limited partnership", "formation", "certificate of formation", "general partner", "limited partner"],
        conclusion_template="A limited partnership is formed in Texas upon filing a certificate of formation with the Secretary of State, naming at least one general and one limited partner.",
        reasoning_framework="""
        TBOC §§ 153.051–153.054 require a certificate of formation for limited partnerships, identifying the partnership name, registered agent, address, and the names and addresses of general partners. The limited partnership is not formed until the certificate is accepted by the Secretary of State. The doctrine considers statutory compliance, partner designation, and curative amendments. The burden is on the party asserting proper formation. Disputes may arise over defective filings or misdesignation of partners. Resolution involves reviewing the certificate, statutory requirements, and any amendments or corrections.
        """,
        key_factors=[
            "Certificate of formation filed",
            "General partner identified",
            "Limited partner identified",
            "Registered agent designation",
            "Acceptance by Secretary of State"
        ],
        primary_authority=[
            "TBOC §§ 153.051–153.054",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Limited partnership organizer or proponent",
        adversary_position="Challenger claims defective formation or misdesignation",
        counter_arguments=[
            "Defective certificate can be amended",
            "Substantial compliance doctrine",
            "De facto limited partnership status"
        ],
        resolution_strategy="Review certificate, statutory compliance, and curative amendments; apply substantial compliance doctrine if appropriate.",
        entity_scope="Limited Partnership",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 153.051"
    ),
    DoctrineBlock(
        topic="Series LLC Structure and Liability Segregation",
        keywords=["series LLC", "structure", "liability segregation", "asset protection", "internal series"],
        conclusion_template="A properly structured Texas Series LLC can segregate assets and liabilities among internal series if statutory requirements are met.",
        reasoning_framework="""
        TBOC §§ 101.601–101.621 authorize Series LLCs, allowing internal series with separate assets, liabilities, and business purposes. Liability segregation is effective only if the certificate of formation and operating agreement provide for series, and records are maintained for each series. The doctrine examines statutory compliance, recordkeeping, and notice requirements. The burden is on the party asserting liability segregation. Disputes may arise from creditors challenging segregation or improper recordkeeping. Resolution involves reviewing formation documents, operating agreement, and records; courts may pierce segregation if requirements are not met.
        """,
        key_factors=[
            "Certificate of formation authorizes series",
            "Operating agreement provides for series",
            "Separate records maintained",
            "Notice of series in formation documents",
            "Compliance with TBOC §§ 101.601–101.621"
        ],
        primary_authority=[
            "TBOC §§ 101.601–101.621",
            "Texas Secretary of State guidance",
            "Texas case law on Series LLCs"
        ],
        burden_holder="Series LLC organizer or proponent",
        adversary_position="Creditor or challenger disputes liability segregation",
        counter_arguments=[
            "Improper recordkeeping",
            "Failure to provide notice",
            "Commingling of assets"
        ],
        resolution_strategy="Review formation documents, operating agreement, and records; apply statutory requirements strictly.",
        entity_scope="Series LLC",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 101.602"
    ),
    DoctrineBlock(
        topic="Benefit Corporation Social Purpose Requirements",
        keywords=["benefit corporation", "social purpose", "formation", "certificate of formation", "public benefit"],
        conclusion_template="A Texas benefit corporation must state its social purpose in the certificate of formation and comply with annual reporting requirements.",
        reasoning_framework="""
        TBOC §§ 21.952–21.959 govern benefit corporations, requiring a statement of social purpose in the certificate of formation. Directors must consider public benefit in decision-making, and annual benefit reports must be provided to shareholders. The doctrine evaluates statutory compliance, director duties, and reporting. The burden is on the corporation to show compliance. Disputes may arise over adequacy of purpose statement or failure to report. Resolution involves reviewing formation documents, director actions, and benefit reports.
        """,
        key_factors=[
            "Social purpose stated in certificate",
            "Annual benefit report provided",
            "Director consideration of public benefit",
            "Shareholder access to reports",
            "Compliance with TBOC §§ 21.952–21.959"
        ],
        primary_authority=[
            "TBOC §§ 21.952–21.959",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Benefit corporation",
        adversary_position="Challenger claims inadequate purpose or reporting",
        counter_arguments=[
            "Failure to provide annual report",
            "Purpose statement too vague",
            "Directors failed to consider public benefit"
        ],
        resolution_strategy="Review certificate, director actions, and benefit reports; cure defects if possible.",
        entity_scope="Benefit Corporation",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.952"
    ),
    DoctrineBlock(
        topic="Professional Entity Restrictions and Requirements",
        keywords=["professional entity", "formation", "restrictions", "licensed professionals", "certificate of formation"],
        conclusion_template="A Texas professional entity must comply with licensing requirements and restrict ownership to licensed professionals as required by statute.",
        reasoning_framework="""
        TBOC §§ 301.003–301.007 govern professional entities, requiring that only licensed professionals may own and manage the entity. The certificate of formation must state the professional purpose and identify licensed owners. The doctrine examines statutory compliance, licensing, and ownership restrictions. The burden is on the entity to show compliance. Disputes may arise from non-licensed ownership or improper management. Resolution involves reviewing formation documents, licensing records, and ownership structure.
        """,
        key_factors=[
            "Licensed professionals as owners",
            "Professional purpose stated",
            "Compliance with licensing board rules",
            "Certificate of formation requirements",
            "Management by licensed professionals"
        ],
        primary_authority=[
            "TBOC §§ 301.003–301.007",
            "Texas licensing board rules"
        ],
        burden_holder="Professional entity",
        adversary_position="Challenger claims non-compliance with licensing or ownership restrictions",
        counter_arguments=[
            "Non-licensed owner or manager",
            "Failure to state professional purpose",
            "Non-compliance with board rules"
        ],
        resolution_strategy="Review certificate, licensing records, and ownership structure; cure defects if possible.",
        entity_scope="Professional Entity",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 301.003"
    ),
    DoctrineBlock(
        topic="Check-the-Box Entity Classification Election",
        keywords=["check-the-box", "entity classification", "IRS", "tax election", "Form 8832"],
        conclusion_template="A Texas entity may elect its federal tax classification by filing IRS Form 8832 under the check-the-box regulations.",
        reasoning_framework="""
        The check-the-box regulations (Treas. Reg. § 301.7701-3) allow eligible entities to elect federal tax classification as corporation, partnership, or disregarded entity. Texas entities must file IRS Form 8832 to make the election. The doctrine distinguishes state law entity type from federal tax classification. The burden is on the entity to show proper election and eligibility. Disputes may arise over eligibility, improper election, or default classification. Resolution involves reviewing formation documents, IRS filings, and entity structure.
        """,
        key_factors=[
            "Eligibility for election",
            "IRS Form 8832 filed",
            "Entity structure",
            "Default classification",
            "Compliance with Treas. Reg. § 301.7701-3"
        ],
        primary_authority=[
            "Treas. Reg. § 301.7701-3",
            "IRS Form 8832 instructions"
        ],
        burden_holder="Entity making election",
        adversary_position="IRS or challenger disputes classification or eligibility",
        counter_arguments=[
            "Improper or late election",
            "Ineligible entity",
            "Default classification applies"
        ],
        resolution_strategy="Review formation documents, IRS filings, and entity structure; cure defects if possible.",
        entity_scope="LLC, Partnership, Corporation",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Treas. Reg. § 301.7701-3"
    ),
    DoctrineBlock(
        topic="Registered Agent Requirements and Consequences of Non-Compliance",
        keywords=["registered agent", "service of process", "formation", "non-compliance", "Secretary of State"],
        conclusion_template="Texas entities must maintain a registered agent; failure to do so may result in administrative dissolution and loss of liability protection.",
        reasoning_framework="""
        TBOC §§ 5.201–5.206 require Texas entities to designate and maintain a registered agent for service of process. Failure to maintain a registered agent may result in administrative dissolution, loss of liability protection, and inability to receive legal notices. The doctrine examines statutory requirements, consequences of non-compliance, and curative procedures. The burden is on the entity to show compliance. Disputes may arise from failure to maintain agent or improper designation. Resolution involves reviewing formation documents, agent records, and statutory procedures for reinstatement.
        """,
        key_factors=[
            "Registered agent designated",
            "Agent address maintained",
            "Compliance with TBOC §§ 5.201–5.206",
            "Service of process capability",
            "Administrative dissolution procedures"
        ],
        primary_authority=[
            "TBOC §§ 5.201–5.206",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Entity",
        adversary_position="Challenger claims failure to maintain registered agent",
        counter_arguments=[
            "Agent resigned or address changed",
            "Failure to update records",
            "Entity dissolved for non-compliance"
        ],
        resolution_strategy="Review agent records, formation documents, and statutory procedures; cure defects if possible.",
        entity_scope="All Texas entities",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 5.201"
    ),
    DoctrineBlock(
        topic="Annual Franchise Tax and Public Information Report Requirements",
        keywords=["franchise tax", "annual report", "public information report", "Texas Comptroller", "compliance"],
        conclusion_template="Texas entities must file annual franchise tax and public information reports; failure to do so may result in forfeiture of privileges.",
        reasoning_framework="""
        Texas Tax Code §§ 171.001–171.302 require most Texas entities to file annual franchise tax and public information reports with the Texas Comptroller. Failure to file may result in forfeiture of entity privileges, loss of liability protection, and administrative dissolution. The doctrine examines statutory requirements, deadlines, and consequences of non-compliance. The burden is on the entity to show compliance. Disputes may arise from late or missing filings. Resolution involves reviewing Comptroller records, entity status, and statutory procedures for reinstatement.
        """,
        key_factors=[
            "Annual franchise tax report filed",
            "Public information report filed",
            "Compliance with Texas Tax Code §§ 171.001–171.302",
            "Entity status with Comptroller",
            "Administrative dissolution procedures"
        ],
        primary_authority=[
            "Texas Tax Code §§ 171.001–171.302",
            "Texas Comptroller guidance"
        ],
        burden_holder="Entity",
        adversary_position="Challenger claims failure to file reports",
        counter_arguments=[
            "Late filing",
            "Failure to file",
            "Entity privileges forfeited"
        ],
        resolution_strategy="Review Comptroller records, entity status, and statutory procedures; cure defects if possible.",
        entity_scope="All Texas entities",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Tax Code § 171.302"
    ),
    DoctrineBlock(
        topic="Sole Proprietorship No Filing Required",
        keywords=["sole proprietorship", "formation", "no filing", "individual business", "informal entity"],
        conclusion_template="A sole proprietorship is formed by an individual conducting business; no filing or formal requirements apply.",
        reasoning_framework="""
        Texas law recognizes sole proprietorships as informal entities formed when an individual conducts business for profit. No filing, certificate, or formal requirements apply. The doctrine distinguishes sole proprietorships from formal entities, focusing on conduct and business activity. The burden is on the party asserting sole proprietorship status. Disputes may arise over liability, business name, or mistaken entity classification. Resolution involves analyzing business activity, ownership, and absence of filings.
        """,
        key_factors=[
            "Individual conducts business",
            "No formal filing",
            "Business activity",
            "Ownership by individual",
            "No statutory requirements"
        ],
        primary_authority=[
            "Texas case law on sole proprietorships",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Individual asserting sole proprietorship",
        adversary_position="Challenger claims formal entity or mistaken classification",
        counter_arguments=[
            "Business operated under assumed name",
            "Multiple owners",
            "Mistaken entity classification"
        ],
        resolution_strategy="Analyze business activity, ownership, and absence of filings; clarify entity status.",
        entity_scope="Sole Proprietorship",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas case law on sole proprietorships"
    ),
    DoctrineBlock(
        topic="LLP Formation and Limited Liability for Partners",
        keywords=["LLP", "limited liability partnership", "formation", "registration", "partner liability"],
        conclusion_template="A Texas LLP is formed upon registration with the Secretary of State; partners enjoy limited liability for partnership obligations.",
        reasoning_framework="""
        TBOC §§ 152.801–152.805 govern LLP formation, requiring registration with the Secretary of State and payment of fees. Partners in an LLP are not liable for partnership obligations incurred while the LLP registration is effective. The doctrine examines statutory compliance, registration status, and liability protection. The burden is on the LLP to show compliance. Disputes may arise from defective registration or liability for pre-registration obligations. Resolution involves reviewing registration records, partnership agreements, and statutory requirements.
        """,
        key_factors=[
            "LLP registration filed",
            "Fees paid",
            "Effective registration",
            "Compliance with TBOC §§ 152.801–152.805",
            "Partner liability protection"
        ],
        primary_authority=[
            "TBOC §§ 152.801–152.805",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLP",
        adversary_position="Challenger claims defective registration or liability for pre-registration obligations",
        counter_arguments=[
            "Registration defective",
            "Obligations incurred before registration",
            "Failure to comply with statutory requirements"
        ],
        resolution_strategy="Review registration records, partnership agreements, and statutory requirements; cure defects if possible.",
        entity_scope="LLP",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 152.801"
    ),
    DoctrineBlock(
        topic="Joint Venture Versus Partnership Distinction",
        keywords=["joint venture", "partnership", "distinction", "business purpose", "duration"],
        conclusion_template="A joint venture is a partnership for a limited purpose or duration; Texas law applies partnership principles unless otherwise agreed.",
        reasoning_framework="""
        Texas law treats joint ventures as partnerships for a specific purpose or limited duration. The doctrine distinguishes joint ventures from general partnerships based on scope, duration, and intent. Partnership principles apply unless the parties agree otherwise. The burden is on the party asserting joint venture status. Disputes may arise over liability, profit sharing, or mistaken classification. Resolution involves analyzing agreements, conduct, and statutory factors.
        """,
        key_factors=[
            "Limited purpose or duration",
            "Agreement among parties",
            "Profit sharing",
            "Mutual agency",
            "Intent to form joint venture"
        ],
        primary_authority=[
            "TBOC §§ 152.051–152.052",
            "Texas case law on joint ventures"
        ],
        burden_holder="Party asserting joint venture status",
        adversary_position="Opposing party claims general partnership or mistaken classification",
        counter_arguments=[
            "No limited purpose",
            "No mutual agency",
            "Express exclusion of joint venture"
        ],
        resolution_strategy="Analyze agreements, conduct, and statutory factors; clarify entity status.",
        entity_scope="Joint Venture, Partnership",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Tex. Oil Co. v. Tenneco, Inc., 706 S.W.2d 829 (Tex. App. 1986)"
    ),
    DoctrineBlock(
        topic="Delaware vs Texas Formation Comparison",
        keywords=["Delaware", "Texas", "formation", "entity comparison", "statutory differences"],
        conclusion_template="Delaware and Texas entities differ in formation requirements, statutory flexibility, and liability protection; choice of jurisdiction impacts governance and litigation.",
        reasoning_framework="""
        Delaware and Texas offer distinct statutory frameworks for entity formation. Delaware is known for flexible corporate statutes, business court expertise, and strong liability protection. Texas offers lower fees and simpler procedures but less statutory flexibility. The doctrine compares formation requirements, governance, liability, and litigation environment. The burden is on the party choosing jurisdiction to justify the choice. Disputes may arise over forum selection, statutory compliance, or liability protection. Resolution involves reviewing statutes, formation documents, and business objectives.
        """,
        key_factors=[
            "Formation requirements",
            "Statutory flexibility",
            "Liability protection",
            "Governance provisions",
            "Litigation environment"
        ],
        primary_authority=[
            "Delaware General Corporation Law",
            "TBOC",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Party choosing jurisdiction",
        adversary_position="Opposing party challenges jurisdiction or statutory compliance",
        counter_arguments=[
            "Delaware fees higher",
            "Texas less flexible",
            "Forum selection disputes"
        ],
        resolution_strategy="Compare statutes, formation documents, and business objectives; resolve forum selection issues contractually.",
        entity_scope="Corporation, LLC",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Delaware General Corporation Law; TBOC"
    ),
    DoctrineBlock(
        topic="Close Corporation Election and Shareholder Agreements",
        keywords=["close corporation", "election", "shareholder agreement", "formation", "TBOC"],
        conclusion_template="A Texas corporation may elect close corporation status in its certificate of formation and adopt shareholder agreements to restrict governance.",
        reasoning_framework="""
        TBOC §§ 21.701–21.711 allow corporations to elect close corporation status, restricting governance and transferability of shares. The certificate of formation must state the election, and shareholder agreements may restrict management, voting, and share transfers. The doctrine examines statutory compliance, shareholder agreements, and governance restrictions. The burden is on the corporation to show proper election and agreement adoption. Disputes may arise over enforceability or ambiguity. Resolution involves reviewing formation documents, agreements, and statutory requirements.
        """,
        key_factors=[
            "Close corporation election in certificate",
            "Shareholder agreement adopted",
            "Governance restrictions",
            "Transferability of shares",
            "Compliance with TBOC §§ 21.701–21.711"
        ],
        primary_authority=[
            "TBOC §§ 21.701–21.711",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Close corporation",
        adversary_position="Challenger claims improper election or unenforceable agreement",
        counter_arguments=[
            "Ambiguous agreement",
            "Failure to comply with statutory requirements",
            "Shareholder disputes"
        ],
        resolution_strategy="Review certificate, shareholder agreements, and statutory requirements; cure defects if possible.",
        entity_scope="Close Corporation",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.701"
    ),
    DoctrineBlock(
        topic="Certificate of Formation Amendment Procedures",
        keywords=["certificate of formation", "amendment", "procedures", "Secretary of State", "entity governance"],
        conclusion_template="Texas entities may amend their certificate of formation by filing an amendment with the Secretary of State and complying with statutory procedures.",
        reasoning_framework="""
        TBOC §§ 3.051–3.058 govern amendment procedures for certificates of formation. Amendments must be approved by the entity's governing body and filed with the Secretary of State. The doctrine examines statutory requirements, approval procedures, and filing. The burden is on the entity to show compliance. Disputes may arise from defective amendments or lack of approval. Resolution involves reviewing governing documents, approval records, and statutory compliance.
        """,
        key_factors=[
            "Approval by governing body",
            "Amendment filed with Secretary of State",
            "Compliance with TBOC §§ 3.051–3.058",
            "Proper notice and consent",
            "Effective date of amendment"
        ],
        primary_authority=[
            "TBOC §§ 3.051–3.058",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Entity",
        adversary_position="Challenger claims defective amendment or lack of approval",
        counter_arguments=[
            "Lack of proper approval",
            "Defective filing",
            "Failure to comply with statutory requirements"
        ],
        resolution_strategy="Review governing documents, approval records, and statutory compliance; cure defects if possible.",
        entity_scope="All Texas entities",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 3.051"
    ),
    DoctrineBlock(
        topic="Foreign Entity Registration Requirements",
        keywords=["foreign entity", "registration", "Texas", "certificate of authority", "Secretary of State"],
        conclusion_template="Foreign entities must register with the Texas Secretary of State before transacting business in Texas; failure to do so limits legal rights.",
        reasoning_framework="""
        TBOC §§ 9.001–9.005 require foreign entities to register and obtain a certificate of authority before transacting business in Texas. Failure to register limits the entity's ability to sue in Texas courts and may result in penalties. The doctrine examines statutory requirements, business activity, and consequences of non-compliance. The burden is on the foreign entity to show compliance. Disputes may arise over registration status or legal capacity. Resolution involves reviewing registration records, business activity, and statutory requirements.
        """,
        key_factors=[
            "Business activity in Texas",
            "Certificate of authority obtained",
            "Compliance with TBOC §§ 9.001–9.005",
            "Legal capacity to sue",
            "Penalties for non-compliance"
        ],
        primary_authority=[
            "TBOC §§ 9.001–9.005",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Foreign entity",
        adversary_position="Challenger claims failure to register or lack of legal capacity",
        counter_arguments=[
            "Business activity not sufficient for registration",
            "Entity not transacting business",
            "Registration pending"
        ],
        resolution_strategy="Review registration records, business activity, and statutory requirements; cure defects if possible.",
        entity_scope="Foreign entities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 9.001"
    ),
    DoctrineBlock(
        topic="Operating Agreement Governance and Enforceability",
        keywords=["operating agreement", "LLC", "governance", "enforceability", "contract law"],
        conclusion_template="A Texas LLC operating agreement governs internal affairs and is enforceable as a contract if it complies with statutory and common law requirements.",
        reasoning_framework="""
        TBOC §§ 101.053–101.054 recognize operating agreements as governing documents for LLCs. Operating agreements are enforceable as contracts if they comply with statutory requirements and general contract law. The doctrine examines agreement terms, statutory compliance, and enforceability. The burden is on the party seeking enforcement. Disputes may arise over ambiguity, unconscionability, or statutory conflicts. Resolution involves interpreting agreement terms, applying contract law, and reviewing statutory requirements.
        """,
        key_factors=[
            "Operating agreement executed",
            "Compliance with TBOC §§ 101.053–101.054",
            "Contract law principles",
            "Ambiguity or unconscionability",
            "Internal governance provisions"
        ],
        primary_authority=[
            "TBOC §§ 101.053–101.054",
            "Texas contract law",
            "Texas case law on operating agreements"
        ],
        burden_holder="Party seeking enforcement",
        adversary_position="Opposing party claims ambiguity or statutory conflict",
        counter_arguments=[
            "Ambiguous terms",
            "Unconscionable provisions",
            "Statutory conflict"
        ],
        resolution_strategy="Interpret agreement terms, apply contract law, and review statutory requirements; resolve ambiguity in favor of enforceability.",
        entity_scope="LLC",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 101.053; Ritchie v. Rupe, 443 S.W.3d 856 (Tex. 2014)"
    ),
    DoctrineBlock(
        topic="Member/Shareholder Approval for Fundamental Transactions",
        keywords=["member approval", "shareholder approval", "fundamental transaction", "merger", "conversion"],
        conclusion_template="Texas entities must obtain member or shareholder approval for fundamental transactions such as mergers, conversions, or sales of assets.",
        reasoning_framework="""
        TBOC §§ 10.001–10.109 require member or shareholder approval for fundamental transactions, including mergers, conversions, and sales of substantially all assets. Approval thresholds and procedures are set by statute and governing documents. The doctrine examines statutory requirements, approval procedures, and notice. The burden is on the entity to show compliance. Disputes may arise from lack of approval or defective procedures. Resolution involves reviewing governing documents, approval records, and statutory requirements.
        """,
        key_factors=[
            "Approval by members or shareholders",
            "Notice and consent procedures",
            "Compliance with TBOC §§ 10.001–10.109",
            "Governing document provisions",
            "Effective date of transaction"
        ],
        primary_authority=[
            "TBOC §§ 10.001–10.109",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Entity",
        adversary_position="Challenger claims lack of approval or defective procedures",
        counter_arguments=[
            "Failure to obtain required approval",
            "Defective notice",
            "Statutory conflict"
        ],
        resolution_strategy="Review governing documents, approval records, and statutory requirements; cure defects if possible.",
        entity_scope="LLC, Corporation",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 10.001"
    ),
    DoctrineBlock(
        topic="Pre-Formation Contracts and Promoter Liability",
        keywords=["pre-formation contract", "promoter", "liability", "entity formation", "ratification"],
        conclusion_template="Promoters are personally liable for pre-formation contracts unless the entity adopts and releases the promoter from liability.",
        reasoning_framework="""
        Texas law holds promoters personally liable for contracts entered before entity formation unless the entity adopts the contract and releases the promoter. The doctrine examines contract terms, adoption, and release procedures. The burden is on the promoter to show release. Disputes may arise from failure to adopt or ambiguous release. Resolution involves reviewing contract terms, entity actions, and statutory requirements.
        """,
        key_factors=[
            "Pre-formation contract executed",
            "Promoter involvement",
            "Entity adoption of contract",
            "Release of promoter liability",
            "Compliance with contract law"
        ],
        primary_authority=[
            "Texas case law on promoter liability",
            "TBOC",
            "General contract law"
        ],
        burden_holder="Promoter",
        adversary_position="Opposing party claims promoter liability",
        counter_arguments=[
            "Entity failed to adopt contract",
            "No release of promoter",
            "Ambiguous contract terms"
        ],
        resolution_strategy="Review contract terms, entity actions, and statutory requirements; clarify adoption and release.",
        entity_scope="All Texas entities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Pacific Coast Engineering Co. v. State, 173 S.W.2d 620 (Tex. 1943)"
    ),
    DoctrineBlock(
        topic="Entity Name Reservation and Availability",
        keywords=["entity name", "reservation", "availability", "Secretary of State", "formation"],
        conclusion_template="Texas entities may reserve a name with the Secretary of State; the name must be distinguishable and comply with statutory requirements.",
        reasoning_framework="""
        TBOC §§ 5.101–5.106 allow entities to reserve a name before formation. The name must be distinguishable from existing entities and comply with statutory requirements. The doctrine examines reservation procedures, name availability, and statutory compliance. The burden is on the entity to show compliance. Disputes may arise from name conflicts or statutory violations. Resolution involves reviewing reservation records, Secretary of State database, and statutory requirements.
        """,
        key_factors=[
            "Name distinguishable from existing entities",
            "Reservation filed with Secretary of State",
            "Compliance with TBOC §§ 5.101–5.106",
            "Name not misleading or prohibited",
            "Effective period of reservation"
        ],
        primary_authority=[
            "TBOC §§ 5.101–5.106",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Entity",
        adversary_position="Challenger claims name conflict or statutory violation",
        counter_arguments=[
            "Name not distinguishable",
            "Name misleading or prohibited",
            "Reservation expired"
        ],
        resolution_strategy="Review reservation records, Secretary of State database, and statutory requirements; cure defects if possible.",
        entity_scope="All Texas entities",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 5.101"
    ),
    DoctrineBlock(
        topic="Piercing the Corporate Veil Alter Ego Doctrine",
        keywords=["piercing the corporate veil", "alter ego", "liability", "corporation", "LLC"],
        conclusion_template="Texas courts may pierce the corporate veil and impose personal liability if the entity is used as an alter ego or to perpetrate fraud.",
        reasoning_framework="""
        Texas courts apply the alter ego doctrine to pierce the corporate veil and impose personal liability on owners if the entity is used to perpetrate fraud, evade obligations, or as an alter ego. TBOC §§ 21.223–21.225 limit veil piercing to cases of actual fraud for personal benefit. The doctrine examines ownership, control, commingling of assets, and fraudulent conduct. The burden is on the party seeking to pierce the veil. Disputes may arise over evidence of fraud or alter ego status. Resolution involves reviewing entity records, ownership, and conduct.
        """,
        key_factors=[
            "Ownership and control",
            "Commingling of assets",
            "Fraudulent conduct",
            "Actual fraud for personal benefit",
            "Compliance with TBOC §§ 21.223–21.225"
        ],
        primary_authority=[
            "TBOC §§ 21.223–21.225",
            "Texas case law on veil piercing"
        ],
        burden_holder="Party seeking to pierce the veil",
        adversary_position="Entity owner denies alter ego or fraud",
        counter_arguments=[
            "No evidence of fraud",
            "Separate entity formalities observed",
            "No personal benefit"
        ],
        resolution_strategy="Review entity records, ownership, and conduct; apply statutory and common law requirements strictly.",
        entity_scope="Corporation, LLC",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Tex. Bus. Corp. Act art. 2.21; TBOC § 21.223; Castleberry v. Branscum, 721 S.W.2d 270 (Tex. 1986)"
    ),
    DoctrineBlock(
        topic="Entity Dissolution and Winding Up Procedures",
        keywords=["dissolution", "winding up", "procedures", "Secretary of State", "entity termination"],
        conclusion_template="Texas entities may dissolve and wind up affairs by following statutory procedures and filing termination documents with the Secretary of State.",
        reasoning_framework="""
        TBOC §§ 11.001–11.101 govern dissolution and winding up procedures. Entities must approve dissolution, wind up affairs, settle debts, distribute assets, and file termination documents with the Secretary of State. The doctrine examines statutory requirements, approval procedures, and asset distribution. The burden is on the entity to show compliance. Disputes may arise from defective dissolution or asset distribution. Resolution involves reviewing governing documents, dissolution records, and statutory requirements.
        """,
        key_factors=[
            "Approval of dissolution",
            "Winding up affairs",
            "Settlement of debts",
            "Distribution of assets",
            "Filing termination documents"
        ],
        primary_authority=[
            "TBOC §§ 11.001–11.101",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Entity",
        adversary_position="Challenger claims defective dissolution or improper asset distribution",
        counter_arguments=[
            "Failure to settle debts",
            "Defective filing",
            "Improper distribution"
        ],
        resolution_strategy="Review governing documents, dissolution records, and statutory requirements; cure defects if possible.",
        entity_scope="All Texas entities",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 11.001"
    ),
    DoctrineBlock(
        topic="Single-Member LLC Liability Protection and Formalities",
        keywords=["single-member LLC", "liability protection", "formalities", "Texas", "piercing the veil"],
        conclusion_template="A single-member LLC enjoys liability protection if statutory formalities are observed; failure to do so may expose the member to personal liability.",
        reasoning_framework="""
        TBOC §§ 101.101–101.106 and §§ 21.223–21.225 provide liability protection for single-member LLCs if statutory formalities are observed. Failure to maintain separate records, commingle assets, or observe formalities may result in veil piercing. The doctrine examines statutory compliance, recordkeeping, and conduct. The burden is on the member to show compliance. Disputes may arise from creditor claims or allegations of alter ego. Resolution involves reviewing records, conduct, and statutory requirements.
        """,
        key_factors=[
            "Separate records maintained",
            "No commingling of assets",
            "Statutory formalities observed",
            "Compliance with TBOC §§ 101.101–101.106",
            "No fraudulent conduct"
        ],
        primary_authority=[
            "TBOC §§ 101.101–101.106",
            "TBOC §§ 21.223–21.225",
            "Texas case law on single-member LLCs"
        ],
        burden_holder="Single-member LLC",
        adversary_position="Creditor claims alter ego or veil piercing",
        counter_arguments=[
            "Failure to observe formalities",
            "Commingling of assets",
            "Fraudulent conduct"
        ],
        resolution_strategy="Review records, conduct, and statutory requirements; cure defects if possible.",
        entity_scope="Single-member LLC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.223"
    ),
    DoctrineBlock(
        topic="LLC Conversion to Corporation Procedures",
        keywords=["LLC conversion", "corporation", "procedures", "TBOC", "Secretary of State"],
        conclusion_template="A Texas LLC may convert to a corporation by following statutory procedures and filing a certificate of conversion with the Secretary of State.",
        reasoning_framework="""
        TBOC §§ 10.101–10.109 govern entity conversions. An LLC may convert to a corporation by approving a plan of conversion, obtaining member approval, and filing a certificate of conversion and certificate of formation for the corporation. The doctrine examines statutory requirements, approval procedures, and filing. The burden is on the LLC to show compliance. Disputes may arise from defective conversion or lack of approval. Resolution involves reviewing governing documents, approval records, and statutory requirements.
        """,
        key_factors=[
            "Plan of conversion approved",
            "Member approval obtained",
            "Certificate of conversion filed",
            "Certificate of formation for corporation filed",
            "Compliance with TBOC §§ 10.101–10.109"
        ],
        primary_authority=[
            "TBOC §§ 10.101–10.109",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC",
        adversary_position="Challenger claims defective conversion or lack of approval",
        counter_arguments=[
            "Failure to obtain required approval",
            "Defective filing",
            "Statutory conflict"
        ],
        resolution_strategy="Review governing documents, approval records, and statutory requirements; cure defects if possible.",
        entity_scope="LLC, Corporation",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 10.101"
    ),
    DoctrineBlock(
        topic="LLC Asset Purchase vs Merger Distinction",
        keywords=["LLC", "asset purchase", "merger", "distinction", "fundamental transaction"],
        conclusion_template="An asset purchase transfers selected assets and liabilities; a merger combines entities and transfers all assets and liabilities by operation of law.",
        reasoning_framework="""
        TBOC §§ 10.001–10.109 distinguish asset purchases from mergers. Asset purchases transfer selected assets and liabilities, requiring consent and assignment. Mergers combine entities, transferring all assets and liabilities by operation of law. The doctrine examines transaction structure, statutory requirements, and approval procedures. The burden is on the party structuring the transaction to show compliance. Disputes may arise from liability allocation or defective procedures. Resolution involves reviewing transaction documents, statutory requirements, and approval records.
        """,
        key_factors=[
            "Transaction structure",
            "Asset and liability allocation",
            "Approval procedures",
            "Compliance with TBOC §§ 10.001–10.109",
            "Effective date of transaction"
        ],
        primary_authority=[
            "TBOC §§ 10.001–10.109",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Party structuring transaction",
        adversary_position="Challenger claims defective allocation or procedures",
        counter_arguments=[
            "Failure to obtain required approval",
            "Defective assignment",
            "Statutory conflict"
        ],
        resolution_strategy="Review transaction documents, statutory requirements, and approval records; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 10.001"
    ),
    DoctrineBlock(
        topic="LLC Admission of New Members Procedures",
        keywords=["LLC", "admission", "new member", "procedures", "operating agreement"],
        conclusion_template="Admission of new members to a Texas LLC requires compliance with the operating agreement and statutory procedures.",
        reasoning_framework="""
        TBOC §§ 101.103–101.106 govern admission of new members. The operating agreement may set procedures and consent requirements. The doctrine examines statutory requirements, agreement terms, and consent. The burden is on the LLC to show compliance. Disputes may arise from defective admission or lack of consent. Resolution involves reviewing operating agreement, consent records, and statutory requirements.
        """,
        key_factors=[
            "Operating agreement provisions",
            "Member consent",
            "Compliance with TBOC §§ 101.103–101.106",
            "Admission procedures",
            "Effective date of admission"
        ],
        primary_authority=[
            "TBOC §§ 101.103–101.106",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC",
        adversary_position="Challenger claims defective admission or lack of consent",
        counter_arguments=[
            "Failure to obtain required consent",
            "Defective procedures",
            "Statutory conflict"
        ],
        resolution_strategy="Review operating agreement, consent records, and statutory requirements; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 101.103"
    ),
    DoctrineBlock(
        topic="Corporation Shareholder Derivative Action Procedures",
        keywords=["corporation", "shareholder", "derivative action", "procedures", "TBOC"],
        conclusion_template="Texas shareholders may bring derivative actions if statutory procedures are followed, including demand on the board and compliance with TBOC.",
        reasoning_framework="""
        TBOC §§ 21.551–21.563 govern shareholder derivative actions. Shareholders must make a demand on the board, comply with statutory procedures, and show standing. The doctrine examines statutory requirements, demand procedures, and standing. The burden is on the shareholder to show compliance. Disputes may arise from defective demand or lack of standing. Resolution involves reviewing demand records, statutory requirements, and board actions.
        """,
        key_factors=[
            "Demand on board made",
            "Standing to sue",
            "Compliance with TBOC §§ 21.551–21.563",
            "Board response",
            "Approval procedures"
        ],
        primary_authority=[
            "TBOC §§ 21.551–21.563",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Shareholder",
        adversary_position="Corporation claims defective demand or lack of standing",
        counter_arguments=[
            "Failure to make demand",
            "Lack of standing",
            "Statutory conflict"
        ],
        resolution_strategy="Review demand records, statutory requirements, and board actions; cure defects if possible.",
        entity_scope="Corporation",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.551"
    ),
    DoctrineBlock(
        topic="LLC Distribution of Profits and Losses",
        keywords=["LLC", "distribution", "profits", "losses", "operating agreement"],
        conclusion_template="Texas LLCs distribute profits and losses according to the operating agreement; absent agreement, distributions are made in proportion to capital contributions.",
        reasoning_framework="""
        TBOC §§ 101.201–101.206 govern distribution of profits and losses. The operating agreement may set allocation procedures; absent agreement, distributions are made in proportion to capital contributions. The doctrine examines agreement terms, statutory requirements, and capital records. The burden is on the LLC to show compliance. Disputes may arise from ambiguous agreements or defective records. Resolution involves reviewing operating agreement, capital records, and statutory requirements.
        """,
        key_factors=[
            "Operating agreement provisions",
            "Capital contributions",
            "Compliance with TBOC §§ 101.201–101.206",
            "Distribution procedures",
            "Effective date of distribution"
        ],
        primary_authority=[
            "TBOC §§ 101.201–101.206",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC",
        adversary_position="Challenger claims defective distribution or ambiguous agreement",
        counter_arguments=[
            "Ambiguous agreement",
            "Defective capital records",
            "Statutory conflict"
        ],
        resolution_strategy="Review operating agreement, capital records, and statutory requirements; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 101.201"
    ),
    DoctrineBlock(
        topic="Corporation Director Fiduciary Duties",
        keywords=["corporation", "director", "fiduciary duty", "business judgment rule", "TBOC"],
        conclusion_template="Texas corporation directors owe fiduciary duties of care and loyalty; the business judgment rule protects directors absent fraud or self-dealing.",
        reasoning_framework="""
        TBOC §§ 21.401–21.408 and Texas case law impose fiduciary duties of care and loyalty on directors. The business judgment rule protects directors from liability absent fraud, self-dealing, or gross negligence. The doctrine examines statutory requirements, director conduct, and judicial review. The burden is on the party alleging breach. Disputes may arise from alleged breach or conflicts of interest. Resolution involves reviewing director actions, board records, and statutory requirements.
        """,
        key_factors=[
            "Director conduct",
            "Board records",
            "Compliance with TBOC §§ 21.401–21.408",
            "Business judgment rule",
            "Fraud or self-dealing"
        ],
        primary_authority=[
            "TBOC §§ 21.401–21.408",
            "Texas case law on fiduciary duties"
        ],
        burden_holder="Party alleging breach",
        adversary_position="Director claims business judgment rule protection",
        counter_arguments=[
            "Fraud or self-dealing",
            "Gross negligence",
            "Statutory conflict"
        ],
        resolution_strategy="Review director actions, board records, and statutory requirements; apply business judgment rule.",
        entity_scope="Corporation",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gearhart Indus., Inc. v. Smith Int'l, Inc., 741 F.2d 707 (5th Cir. 1984)"
    ),
    DoctrineBlock(
        topic="LLC Indemnification of Members and Managers",
        keywords=["LLC", "indemnification", "members", "managers", "operating agreement"],
        conclusion_template="Texas LLCs may indemnify members and managers if authorized by the operating agreement and consistent with statutory requirements.",
        reasoning_framework="""
        TBOC §§ 101.401–101.406 allow LLCs to indemnify members and managers for liabilities incurred in the course of business, subject to operating agreement provisions and statutory limits. The doctrine examines agreement terms, statutory requirements, and indemnification procedures. The burden is on the LLC to show compliance. Disputes may arise from defective indemnification or statutory conflicts. Resolution involves reviewing operating agreement, indemnification records, and statutory requirements.
        """,
        key_factors=[
            "Operating agreement provisions",
            "Compliance with TBOC §§ 101.401–101.406",
            "Indemnification procedures",
            "Statutory limits",
            "Effective date of indemnification"
        ],
        primary_authority=[
            "TBOC §§ 101.401–101.406",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC",
        adversary_position="Challenger claims defective indemnification or statutory conflict",
        counter_arguments=[
            "Ambiguous agreement",
            "Statutory conflict",
            "Defective procedures"
        ],
        resolution_strategy="Review operating agreement, indemnification records, and statutory requirements; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 101.401"
    ),
    DoctrineBlock(
        topic="Corporation Issuance of Shares and Capitalization",
        keywords=["corporation", "issuance of shares", "capitalization", "certificate of formation", "TBOC"],
        conclusion_template="Texas corporations may issue shares as authorized by the certificate of formation and board approval, subject to statutory requirements.",
        reasoning_framework="""
        TBOC §§ 21.151–21.155 govern issuance of shares and capitalization. The certificate of formation and board resolutions must authorize issuance, and statutory requirements must be met. The doctrine examines certificate terms, board approval, and statutory compliance. The burden is on the corporation to show compliance. Disputes may arise from defective issuance or statutory conflicts. Resolution involves reviewing certificate, board records, and statutory requirements.
        """,
        key_factors=[
            "Certificate of formation authorization",
            "Board approval",
            "Compliance with TBOC §§ 21.151–21.155",
            "Issuance procedures",
            "Effective date of issuance"
        ],
        primary_authority=[
            "TBOC §§ 21.151–21.155",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Corporation",
        adversary_position="Challenger claims defective issuance or statutory conflict",
        counter_arguments=[
            "Failure to obtain board approval",
            "Defective procedures",
            "Statutory conflict"
        ],
        resolution_strategy="Review certificate, board records, and statutory requirements; cure defects if possible.",
        entity_scope="Corporation",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.151"
    ),
    DoctrineBlock(
        topic="LLC Reinstatement After Administrative Dissolution",
        keywords=["LLC", "reinstatement", "administrative dissolution", "Secretary of State", "statutory procedures"],
        conclusion_template="A Texas LLC may be reinstated after administrative dissolution by curing defects and filing for reinstatement with the Secretary of State.",
        reasoning_framework="""
        TBOC §§ 11.201–11.206 govern reinstatement procedures for LLCs after administrative dissolution. The LLC must cure defects, pay fees, and file for reinstatement with the Secretary of State. The doctrine examines statutory requirements, defect cure, and filing procedures. The burden is on the LLC to show compliance. Disputes may arise from defective reinstatement or statutory conflicts. Resolution involves reviewing records, defect cure, and statutory requirements.
        """,
        key_factors=[
            "Defects cured",
            "Fees paid",
            "Reinstatement filed with Secretary of State",
            "Compliance with TBOC §§ 11.201–11.206",
            "Effective date of reinstatement"
        ],
        primary_authority=[
            "TBOC §§ 11.201–11.206",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC",
        adversary_position="Challenger claims defective reinstatement or statutory conflict",
        counter_arguments=[
            "Failure to cure defects",
            "Defective filing",
            "Statutory conflict"
        ],
        resolution_strategy="Review records, defect cure, and statutory requirements; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 11.201"
    ),
    DoctrineBlock(
        topic="Corporation Amendment of Bylaws Procedures",
        keywords=["corporation", "amendment", "bylaws", "procedures", "board approval"],
        conclusion_template="Texas corporations may amend bylaws by board or shareholder approval, subject to certificate of formation and statutory requirements.",
        reasoning_framework="""
        TBOC §§ 21.057–21.058 govern amendment of bylaws. The certificate of formation and bylaws may set amendment procedures; board or shareholder approval is required. The doctrine examines certificate terms, bylaws, and statutory requirements. The burden is on the corporation to show compliance. Disputes may arise from defective amendment or statutory conflicts. Resolution involves reviewing certificate, bylaws, and approval records.
        """,
        key_factors=[
            "Certificate of formation terms",
            "Bylaws provisions",
            "Board or shareholder approval",
            "Compliance with TBOC §§ 21.057–21.058",
            "Effective date of amendment"
        ],
        primary_authority=[
            "TBOC §§ 21.057–21.058",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Corporation",
        adversary_position="Challenger claims defective amendment or statutory conflict",
        counter_arguments=[
            "Failure to obtain approval",
            "Defective procedures",
            "Statutory conflict"
        ],
        resolution_strategy="Review certificate, bylaws, and approval records; cure defects if possible.",
        entity_scope="Corporation",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.057"
    ),
    DoctrineBlock(
        topic="LLC Dissociation of Members Procedures",
        keywords=["LLC", "dissociation", "members", "procedures", "operating agreement"],
        conclusion_template="Dissociation of members from a Texas LLC is governed by the operating agreement and statutory procedures; dissociated members lose management rights.",
        reasoning_framework="""
        TBOC §§ 101.201–101.206 govern dissociation of members. The operating agreement may set procedures and consequences. Dissociated members lose management rights and may retain economic interests. The doctrine examines agreement terms, statutory requirements, and dissociation procedures. The burden is on the LLC to show compliance. Disputes may arise from defective dissociation or statutory conflicts. Resolution involves reviewing operating agreement, dissociation records, and statutory requirements.
        """,
        key_factors=[
            "Operating agreement provisions",
            "Compliance with TBOC §§ 101.201–101.206",
            "Dissociation procedures",
            "Loss of management rights",
            "Effective date of dissociation"
        ],
        primary_authority=[
            "TBOC §§ 101.201–101.206",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC",
        adversary_position="Challenger claims defective dissociation or statutory conflict",
        counter_arguments=[
            "Failure to comply with agreement",
            "Defective procedures",
            "Statutory conflict"
        ],
        resolution_strategy="Review operating agreement, dissociation records, and statutory requirements; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 101.201"
    ),
    DoctrineBlock(
        topic="Partnership Withdrawal and Continuation Procedures",
        keywords=["partnership", "withdrawal", "continuation", "procedures", "TBOC"],
        conclusion_template="Texas partnerships may continue after partner withdrawal if the partnership agreement or statutory procedures permit continuation.",
        reasoning_framework="""
        TBOC §§ 152.501–152.507 govern partner withdrawal and continuation. The partnership agreement may set procedures; absent agreement, statutory procedures apply. The doctrine examines agreement terms, statutory requirements, and continuation procedures. The burden is on the partnership to show compliance. Disputes may arise from defective withdrawal or statutory conflicts. Resolution involves reviewing agreement, withdrawal records, and statutory requirements.
        """,
        key_factors=[
            "Partnership agreement provisions",
            "Compliance with TBOC §§ 152.501–152.507",
            "Withdrawal procedures",
            "Continuation procedures",
            "Effective date of withdrawal"
        ],
        primary_authority=[
            "TBOC §§ 152.501–152.507",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Partnership",
        adversary_position="Challenger claims defective withdrawal or statutory conflict",
        counter_arguments=[
            "Failure to comply with agreement",
            "Defective procedures",
            "Statutory conflict"
        ],
        resolution_strategy="Review agreement, withdrawal records, and statutory requirements; cure defects if possible.",
        entity_scope="Partnership",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 152.501"
    ),
    DoctrineBlock(
        topic="Corporation Shareholder Voting Procedures",
        keywords=["corporation", "shareholder", "voting", "procedures", "TBOC"],
        conclusion_template="Texas corporations must follow statutory and bylaw procedures for shareholder voting; failure to comply may invalidate votes.",
        reasoning_framework="""
        TBOC §§ 21.351–21.355 govern shareholder voting procedures. The certificate of formation and bylaws may set procedures; statutory requirements must be met. The doctrine examines certificate terms, bylaws, and statutory requirements. The burden is on the corporation to show compliance. Disputes may arise from defective voting or statutory conflicts. Resolution involves reviewing certificate, bylaws, voting records, and statutory requirements.
        """,
        key_factors=[
            "Certificate of formation terms",
            "Bylaws provisions",
            "Compliance with TBOC §§ 21.351–21.355",
            "Voting procedures",
            "Effective date of vote"
        ],
        primary_authority=[
            "TBOC §§ 21.351–21.355",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Corporation",
        adversary_position="Challenger claims defective voting or statutory conflict",
        counter_arguments=[
            "Failure to comply with procedures",
            "Defective records",
            "Statutory conflict"
        ],
        resolution_strategy="Review certificate, bylaws, voting records, and statutory requirements; cure defects if possible.",
        entity_scope="Corporation",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.351"
    ),
    DoctrineBlock(
        topic="LLC Tax Classification and Reporting Requirements",
        keywords=["LLC", "tax classification", "reporting", "IRS", "Texas Comptroller"],
        conclusion_template="Texas LLCs must comply with federal and state tax classification and reporting requirements; failure to do so may result in penalties.",
        reasoning_framework="""
        Texas LLCs are classified for federal tax purposes under the check-the-box regulations and must file appropriate IRS and Texas Comptroller reports. The doctrine examines tax classification, reporting requirements, and compliance. The burden is on the LLC to show compliance. Disputes may arise from defective classification or reporting. Resolution involves reviewing IRS and Comptroller records, entity structure, and statutory requirements.
        """,
        key_factors=[
            "Federal tax classification",
            "IRS reporting requirements",
            "Texas Comptroller reporting",
            "Compliance with Treas. Reg. § 301.7701-3",
            "Effective date of classification"
        ],
        primary_authority=[
            "Treas. Reg. § 301.7701-3",
            "Texas Tax Code",
            "IRS guidance"
        ],
        burden_holder="LLC",
        adversary_position="IRS or Comptroller claims defective classification or reporting",
        counter_arguments=[
            "Improper or late election",
            "Defective reporting",
            "Statutory conflict"
        ],
        resolution_strategy="Review IRS and Comptroller records, entity structure, and statutory requirements; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Treas. Reg. § 301.7701-3"
    ),
    DoctrineBlock(
        topic="Corporation Annual Meeting and Recordkeeping Requirements",
        keywords=["corporation", "annual meeting", "recordkeeping", "TBOC", "Secretary of State"],
        conclusion_template="Texas corporations must hold annual meetings and maintain records as required by statute; failure to do so may result in penalties.",
        reasoning_framework="""
        TBOC §§ 21.351–21.355 and §§ 21.401–21.408 require corporations to hold annual meetings and maintain records. The doctrine examines statutory requirements, meeting procedures, and recordkeeping. The burden is on the corporation to show compliance. Disputes may arise from defective meetings or recordkeeping. Resolution involves reviewing meeting records, statutory requirements, and board actions.
        """,
        key_factors=[
            "Annual meeting held",
            "Recordkeeping procedures",
            "Compliance with TBOC §§ 21.351–21.355 and §§ 21.401–21.408",
            "Board actions",
            "Effective date of meeting"
        ],
        primary_authority=[
            "TBOC §§ 21.351–21.355",
            "TBOC §§ 21.401–21.408",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Corporation",
        adversary_position="Challenger claims defective meeting or recordkeeping",
        counter_arguments=[
            "Failure to hold meeting",
            "Defective records",
            "Statutory conflict"
        ],
        resolution_strategy="Review meeting records, statutory requirements, and board actions; cure defects if possible.",
        entity_scope="Corporation",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.351"
    ),
    DoctrineBlock(
        topic="LLC Member Expulsion Procedures",
        keywords=["LLC", "member expulsion", "procedures", "operating agreement", "statutory requirements"],
        conclusion_template="Expulsion of members from a Texas LLC requires compliance with the operating agreement and statutory procedures; expelled members lose management rights.",
        reasoning_framework="""
        TBOC §§ 101.201–101.206 govern member expulsion. The operating agreement may set procedures and consequences. Expelled members lose management rights and may retain economic interests. The doctrine examines agreement terms, statutory requirements, and expulsion procedures. The burden is on the LLC to show compliance. Disputes may arise from defective expulsion or statutory conflicts. Resolution involves reviewing operating agreement, expulsion records, and statutory requirements.
        """,
        key_factors=[
            "Operating agreement provisions",
            "Compliance with TBOC §§ 101.201–101.206",
            "Expulsion procedures",
            "Loss of management rights",
            "Effective date of expulsion"
        ],
        primary_authority=[
            "TBOC §§ 101.201–101.206",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC",
        adversary_position="Challenger claims defective expulsion or statutory conflict",
        counter_arguments=[
            "Failure to comply with agreement",
            "Defective procedures",
            "Statutory conflict"
        ],
        resolution_strategy="Review operating agreement, expulsion records, and statutory requirements; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 101.201"
    ),
    DoctrineBlock(
        topic="Corporation Share Transfer Restrictions",
        keywords=["corporation", "share transfer", "restrictions", "certificate of formation", "bylaws"],
        conclusion_template="Texas corporations may restrict share transfers by certificate of formation or bylaws; restrictions must comply with statutory requirements.",
        reasoning_framework="""
        TBOC §§ 21.210–21.213 govern share transfer restrictions. The certificate of formation and bylaws may set restrictions; statutory requirements must be met. The doctrine examines certificate terms, bylaws, and statutory requirements. The burden is on the corporation to show compliance. Disputes may arise from defective restrictions or statutory conflicts. Resolution involves reviewing certificate, bylaws, and transfer records.
        """,
        key_factors=[
            "Certificate of formation terms",
            "Bylaws provisions",
            "Compliance with TBOC §§ 21.210–21.213",
            "Transfer procedures",
            "Effective date of restriction"
        ],
        primary_authority=[
            "TBOC §§ 21.210–21.213",
            "Texas Secretary of State guidance"
        ],
        burden_holder="Corporation",
        adversary_position="Challenger claims defective restriction or statutory conflict",
        counter_arguments=[
            "Failure to comply with procedures",
            "Defective records",
            "Statutory conflict"
        ],
        resolution_strategy="Review certificate, bylaws, and transfer records; cure defects if possible.",
        entity_scope="Corporation",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 21.210"
    ),
    DoctrineBlock(
        topic="LLC Member Withdrawal and Buyout Procedures",
        keywords=["LLC", "member withdrawal", "buyout", "procedures", "operating agreement"],
        conclusion_template="Member withdrawal and buyout from a Texas LLC is governed by the operating agreement and statutory procedures; buyout price must be determined by agreement or appraisal.",
        reasoning_framework="""
        TBOC §§ 101.201–101.206 govern member withdrawal and buyout. The operating agreement may set procedures and buyout price; absent agreement, statutory procedures and appraisal may apply. The doctrine examines agreement terms, statutory requirements, and buyout procedures. The burden is on the LLC to show compliance. Disputes may arise from defective withdrawal or price determination. Resolution involves reviewing operating agreement, buyout records, and statutory requirements.
        """,
        key_factors=[
            "Operating agreement provisions",
            "Buyout price determination",
            "Compliance with TBOC §§ 101.201–101.206",
            "Withdrawal procedures",
            "Effective date of withdrawal"
        ],
        primary_authority=[
            "TBOC §§ 101.201–101.206",
            "Texas Secretary of State guidance"
        ],
        burden_holder="LLC",
        adversary_position="Challenger claims defective withdrawal or price determination",
        counter_arguments=[
            "Failure to comply with agreement",
            "Defective procedures",
            "Statutory conflict"
        ],
        resolution_strategy="Review operating agreement, buyout records, and statutory requirements; cure defects if possible.",
        entity_scope="LLC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TBOC § 101.201"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]