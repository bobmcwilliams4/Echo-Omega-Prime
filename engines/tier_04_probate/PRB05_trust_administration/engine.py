"""
PRB05 Trust Administration Engine v1.0.0
Full TIE-grade trust law expertise - trustee duties, fiduciary obligations, trust modification
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
from contextlib import asynccontextmanager

ENGINE_ID = "PRB05"
ENGINE_NAME = "Trust Administration Engine"
VERSION = "1.0.0"
PORT = 9115

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    TRUSTEE_DUTY = "TRUSTEE_DUTY"
    FIDUCIARY_OBLIGATION = "FIDUCIARY_OBLIGATION"
    TRUST_MODIFICATION = "TRUST_MODIFICATION"
    DISTRIBUTION = "DISTRIBUTION"
    ACCOUNTING = "ACCOUNTING"
    INVESTMENT = "INVESTMENT"
    TERMINATION = "TERMINATION"
    BREACH = "BREACH"
    ADMINISTRATION = "ADMINISTRATION"
    BENEFICIARY_RIGHTS = "BENEFICIARY_RIGHTS"

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    controlling_precedent: Optional[str] = None
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    issue_category: IssueCategory

class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    answer: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    sources: List[str]
    triggered_doctrines: List[str]
    latency_ms: float
    determinism_hash: str
    timestamp: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Duty of Loyalty - Self-Dealing Prohibition",
        keywords=["duty of loyalty", "self-dealing", "conflict of interest", "interested transaction", "trustee benefit"],
        conclusion_template="Trustee must not engage in self-dealing. Any transaction where trustee benefits personally is voidable regardless of fairness. UTC 802(a), Restatement Third Trusts 78.",
        reasoning_framework="""1. Duty of loyalty is fundamental fiduciary obligation
2. No-further-inquiry rule applies to self-dealing
3. Transaction voidable even if fair to trust
4. Burden on trustee to prove exception (e.g., court approval, full disclosure + consent)
5. Constructive trust or disgorgement of profits as remedy
6. Exceptions: trustee compensation per trust terms, court-approved transactions""",
        key_factors=["trustee derived personal benefit", "conflict of interest present", "beneficiaries gave informed consent", "court approved transaction", "trust instrument authorized"],
        primary_authority=["UTC 802", "Restatement (Third) of Trusts 78", "Texas Property Code 117.007-117.008", "Bogert on Trusts"],
        controlling_precedent="Hartman v. Hartle, 95 S.W.3d 605 (Tex. 2002) - trustee liable for profit from self-dealing",
        burden_holder="Trustee must prove exception to no-further-inquiry rule",
        adversary_position="Transaction was fair and reasonable to trust",
        counter_arguments=["fairness of transaction", "market-rate pricing", "no harm to beneficiaries", "necessity of transaction", "common practice"],
        resolution_strategy="Apply no-further-inquiry rule strictly. Void transaction and require disgorgement unless narrow exception proven.",
        entity_scope="all trustees - individual, corporate, professional",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FIDUCIARY_OBLIGATION
    ),
    DoctrineBlock(
        topic="Prudent Investor Rule - Modern Portfolio Theory",
        keywords=["prudent investor", "investment standard", "diversification", "total return", "UPIA", "portfolio theory"],
        conclusion_template="Trustee must invest as prudent investor would, considering total portfolio return and risk/return objectives. UPIA abandons categorical prohibitions. Diversification required unless special circumstances.",
        reasoning_framework="""1. Modern portfolio theory replaces old prudent man rule
2. Focus on total return (income + appreciation) not just income
3. Diversification presumptively required (UPIA 3)
4. Consider risk/return appropriate to trust purposes
5. Delegation to investment advisors permitted
6. Review entire portfolio, not individual investments
7. Document investment strategy and decisions""",
        key_factors=["portfolio diversified", "risk appropriate to beneficiaries", "investment strategy documented", "delegation to qualified advisors", "costs reasonable", "duty to review delegated decisions"],
        primary_authority=["Uniform Prudent Investor Act", "Restatement (Third) of Trusts 90-92", "Texas Property Code Ch. 117", "UPIA Official Comments"],
        controlling_precedent="Matter of Janes, 681 N.E.2d 332 (N.Y. 1997) - total return investing approved",
        burden_holder="Trustee must show compliance with prudent investor standard",
        adversary_position="Concentrated position or risky investment was appropriate",
        counter_arguments=["trust instrument authorized investment", "beneficiaries consented", "high returns achieved", "temporary lack of diversification", "transition period"],
        resolution_strategy="Apply modern portfolio theory. Require diversification unless documented reasons support concentration.",
        entity_scope="all investment trustees",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.INVESTMENT
    ),
    DoctrineBlock(
        topic="Duty to Inform - Regular Reporting Requirements",
        keywords=["duty to inform", "trust accounting", "beneficiary reports", "notice", "transparency", "UTC 813"],
        conclusion_template="Trustee must keep beneficiaries reasonably informed of trust administration. Annual reports required. UTC 813, Restatement Third Trusts 82.",
        reasoning_framework="""1. Duty to inform derived from fiduciary relationship
2. UTC requires annual reports to qualified beneficiaries
3. Report must include trust property, liabilities, receipts, disbursements
4. Must respond promptly to beneficiary requests
5. Beneficiaries entitled to trust instrument copy
6. Notice required for major decisions (termination, modification)
7. Silence can constitute breach in some circumstances""",
        key_factors=["annual report provided", "financial information disclosed", "trust terms disclosed", "beneficiary requests answered", "major decisions disclosed", "report timely"],
        primary_authority=["UTC 813", "Restatement (Third) of Trusts 82", "Texas Property Code 113.060", "Uniform Trust Code Official Comments"],
        controlling_precedent="Fletcher v. Fletcher, 253 S.W.3d 903 (Tex. App. 2008) - trustee must provide accountings",
        burden_holder="Trustee must prove adequate disclosure",
        adversary_position="Information was not material or beneficiary had actual knowledge",
        counter_arguments=["beneficiary did not request", "commercially sensitive information", "confidentiality concerns", "frequent informal updates given"],
        resolution_strategy="Require annual written reports at minimum. Respond to reasonable requests within 30 days.",
        entity_scope="all trustees with current beneficiaries",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FIDUCIARY_OBLIGATION
    ),
    DoctrineBlock(
        topic="HEMS Distribution Standard - Ascertainable Standard",
        keywords=["HEMS", "health education maintenance support", "ascertainable standard", "discretionary distribution", "trustee discretion"],
        conclusion_template="HEMS (health, education, maintenance, support) is ascertainable standard limiting trustee discretion. Prevents inclusion in beneficiary gross estate under IRC 2041. Objective needs-based test.",
        reasoning_framework="""1. HEMS defined: health, education, maintenance, support
2. Ascertainable standard = objective measurable test
3. Limits trustee absolute discretion
4. Tax benefit: prevents estate inclusion as general power
5. Trustee must make distributions for HEMS purposes
6. Beneficiary standard of living determines 'maintenance'
7. Emergency medical is health, private school is education
8. Support = basic living expenses at accustomed standard""",
        key_factors=["trust uses HEMS language", "beneficiary has actual HEMS need", "distribution matches beneficiary standard of living", "no other resources available", "amount reasonable for purpose"],
        primary_authority=["Treas. Reg. 20.2041-1(c)(2)", "Restatement (Third) of Trusts 50", "Texas Property Code 113.029", "IRS Revenue Rulings"],
        controlling_precedent="Rev. Rul. 77-60 - ascertainable standard examples",
        burden_holder="Beneficiary requesting distribution must show HEMS need",
        adversary_position="Request exceeds HEMS standard or is luxury not necessity",
        counter_arguments=["beneficiary has other resources", "amount excessive", "not true need", "comfort vs necessity", "prior lifestyle irrelevant"],
        resolution_strategy="Apply objective needs test. Consider beneficiary's accustomed standard of living. Require documentation of need.",
        entity_scope="trusts with HEMS distribution standards",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.DISTRIBUTION
    ),
    DoctrineBlock(
        topic="Spendthrift Clause - Creditor Protection",
        keywords=["spendthrift", "creditor protection", "asset protection", "transfer restriction", "alienation", "judgment creditor"],
        conclusion_template="Valid spendthrift clause prevents creditors from reaching beneficiary's trust interest. Exceptions: alimony, child support, government claims, excess distributions. UTC 502-503.",
        reasoning_framework="""1. Spendthrift clause restricts voluntary and involuntary transfers
2. Creditors cannot attach beneficiary's interest before distribution
3. Mandatory exceptions: child support, alimony, government claims
4. Excess distribution doctrine in some states
5. Self-settled trusts generally invalid for creditor protection
6. Distribution in trustee discretion enhances protection
7. Once distributed, creditors can reach actual receipt""",
        key_factors=["spendthrift language in trust", "claim type (mandatory exception vs ordinary creditor)", "distribution made vs future interest", "self-settled trust", "excess distribution analysis"],
        primary_authority=["UTC 502-503", "Restatement (Third) of Trusts 58-59", "Texas Property Code 112.035", "Sligh v. First Nat'l Bank, 704 S.W.2d 390 (Tex. 1986)"],
        controlling_precedent="Schoneberger v. Oelze, 208 S.W.3d 872 (Tex. App. 2006) - spendthrift trust protects against creditors",
        burden_holder="Creditor seeking to pierce spendthrift trust must prove exception applies",
        adversary_position="Creditor claim falls within mandatory exception or trust is self-settled",
        counter_arguments=["child support claim", "alimony claim", "federal tax lien", "settlor is beneficiary", "fraudulent transfer", "excess distribution"],
        resolution_strategy="Enforce spendthrift clause unless mandatory exception proven. Distinguish self-settled trusts (no protection).",
        entity_scope="third-party created trusts with spendthrift provisions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.BENEFICIARY_RIGHTS
    ),
    DoctrineBlock(
        topic="Trust Modification - Changed Circumstances Doctrine",
        keywords=["trust modification", "changed circumstances", "cy pres", "equitable deviation", "UTC 412", "unforeseen circumstances"],
        conclusion_template="Court may modify trust administrative or dispositive terms if circumstances not anticipated by settlor make compliance impracticable or wasteful. UTC 412. Settlor's intent remains paramount.",
        reasoning_framework="""1. Changed circumstances must be unforeseen by settlor
2. Compliance with original terms must be impracticable/wasteful
3. Modification must further trust purposes
4. Administrative terms easier to modify than dispositive
5. Cy pres applies to charitable trusts (impossible/impracticable)
6. Tax considerations may prevent modification
7. All beneficiaries can consent to modification if not material purpose""",
        key_factors=["circumstances unforeseen", "compliance impracticable or wasteful", "modification furthers purposes", "settlor intent preserved", "all beneficiaries consent", "no material purpose frustrated"],
        primary_authority=["UTC 412", "Restatement (Third) of Trusts 66-67", "Texas Property Code 112.054", "In re Estate of Spencer, 232 N.W.2d 491 (Iowa 1975)"],
        controlling_precedent="Stuchell v. Crary, 238 N.W.2d 600 (Mich. 1976) - unforeseen circumstances permit modification",
        burden_holder="Party seeking modification must prove changed circumstances and impracticability",
        adversary_position="Modification violates settlor intent or frustrates material purpose",
        counter_arguments=["circumstances were foreseeable", "compliance still possible", "defeats tax planning", "violates material purpose", "not all beneficiaries consent"],
        resolution_strategy="Require clear proof of unforeseen change making compliance impracticable. Preserve core purposes.",
        entity_scope="irrevocable trusts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TRUST_MODIFICATION
    ),
    DoctrineBlock(
        topic="Trustee Removal - Cause Standard",
        keywords=["trustee removal", "removal for cause", "serious breach", "substantial change", "UTC 706", "hostility"],
        conclusion_template="Court may remove trustee for serious breach of trust, lack of cooperation, unfitness, or substantial change in circumstances. UTC 706. Mere friction or inefficiency insufficient.",
        reasoning_framework="""1. Removal requires serious cause, not minor disputes
2. Grounds: breach of trust, unfitness, hostility, changed circumstances
3. Beneficiary hostility alone insufficient
4. Best interests of beneficiaries is key consideration
5. Successor trustee availability relevant
6. Trust administration costs and delays weigh against removal
7. Settlor's choice of trustee entitled to deference""",
        key_factors=["serious breach occurred", "beneficiaries endangered", "trustee unfit or hostile", "substantial change in circumstances", "better alternative available", "removal serves beneficiaries"],
        primary_authority=["UTC 706", "Restatement (Third) of Trusts 37", "Texas Property Code 113.082", "Clift v. Moses, 116 A.2d 54 (Del. 1955)"],
        controlling_precedent="Matter of Huber, 493 N.Y.S.2d 551 (Sur. Ct. 1985) - hostility and conflict permit removal",
        burden_holder="Party seeking removal must prove serious cause",
        adversary_position="Trustee performing adequately, friction normal in trust administration",
        counter_arguments=["no breach proven", "beneficiary unreasonable", "mere personality conflict", "costly to change trustees", "settlor chose this trustee"],
        resolution_strategy="Require proof of serious breach or unfitness. Balance beneficiary interests against settlor intent and costs.",
        entity_scope="all trust types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Duty of Impartiality - Income vs Remainder Beneficiaries",
        keywords=["duty of impartiality", "income beneficiary", "remainder beneficiary", "principal and income", "UPIA", "total return trust"],
        conclusion_template="Trustee must act impartially in investing and managing trust, considering interests of both income and remainder beneficiaries. UPIA permits total return approach. UTC 803.",
        reasoning_framework="""1. Traditional rule required balancing income vs growth
2. UPIA allows total return investing + unitrust conversion
3. Impartiality does not mean equal treatment, but fair consideration
4. Can favor income or remainder if trust terms direct
5. Power to adjust between principal and income (UPIA 104)
6. Document reasons for allocation decisions
7. Consider tax consequences to both classes""",
        key_factors=["trust terms specify allocation", "UPIA adopted in jurisdiction", "power to adjust exercised fairly", "total return unitrust used", "both classes considered", "adjustment documented"],
        primary_authority=["Uniform Principal and Income Act", "UTC 803", "Restatement (Third) of Trusts 79", "Texas Property Code Ch. 116"],
        controlling_precedent="Dennis v. Rhode Island Hospital Trust Co., 744 F.2d 893 (1st Cir. 1984) - impartiality required",
        burden_holder="Trustee must prove fair consideration of both classes",
        adversary_position="Allocation unfairly favors one class of beneficiaries",
        counter_arguments=["trust terms authorize preference", "UPIA adjustment proper", "total return benefits all", "income needs greater", "remainder far in future"],
        resolution_strategy="Allow total return approach under UPIA. Require documentation of allocation decisions.",
        entity_scope="trusts with income and remainder beneficiaries",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FIDUCIARY_OBLIGATION
    ),
    DoctrineBlock(
        topic="Crummey Powers - Annual Exclusion Gifts",
        keywords=["Crummey power", "annual exclusion", "demand right", "lapse", "5 and 5 power", "gift tax", "IRC 2503"],
        conclusion_template="Crummey withdrawal power gives beneficiary temporary right to demand distribution, converting future interest to present interest for gift tax annual exclusion. Must give notice. IRC 2503(b).",
        reasoning_framework="""1. Crummey power creates present interest for gift tax purposes
2. Beneficiary must have meaningful opportunity to withdraw
3. Notice required - typically 30-60 days
4. Lapse treated as release - 5 and 5 safe harbor (IRC 2514)
5. Hanging powers prevent taxable lapse
6. Beneficiary need not exercise to qualify for exclusion
7. Trustee must track Crummey windows and give proper notice""",
        key_factors=["withdrawal right given", "notice properly provided", "reasonable withdrawal period", "lapse within 5 and 5 safe harbor", "beneficiary legally competent", "no understanding not to withdraw"],
        primary_authority=["IRC 2503(b)", "IRC 2514(e)", "Crummey v. Commissioner, 397 F.2d 82 (9th Cir. 1968)", "Treas. Reg. 25.2514-3"],
        controlling_precedent="Crummey v. Commissioner - withdrawal right creates present interest",
        burden_holder="Trustee must prove valid Crummey power and proper notice",
        adversary_position="IRS may challenge if no real opportunity to withdraw or beneficiaries agreed not to withdraw",
        counter_arguments=["notice inadequate", "withdrawal period too short", "illusory power", "prearranged understanding", "minor beneficiary", "lapse exceeds 5 and 5"],
        resolution_strategy="Provide written notice, allow reasonable withdrawal period, document in trust records.",
        entity_scope="irrevocable life insurance trusts, generation-skipping trusts",
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Generation-Skipping Transfer Tax - Dynasty Trust Planning",
        keywords=["GST tax", "generation-skipping", "dynasty trust", "exemption allocation", "skip person", "IRC 2601", "perpetual trust"],
        conclusion_template="GST tax applies to transfers to skip persons (grandchildren or later generations). GST exemption ($13.61M in 2024) allows dynasty trusts. Automatic allocation rules apply. IRC 2601-2664.",
        reasoning_framework="""1. GST tax is flat 40% tax on generation-skipping transfers
2. Skip person = 2+ generations below transferor
3. Three types: direct skip, taxable distribution, taxable termination
4. GST exemption allocation critical - automatic or manual election
5. Inclusion ratio determines GST tax due (1 - exemption/transfer value)
6. Dynasty trusts use exemption to avoid tax for multiple generations
7. Rule against perpetuities repealed in many states (AK, DE, SD, NV)""",
        key_factors=["skip person identified", "GST exemption allocated", "inclusion ratio calculated", "automatic allocation applies", "state allows perpetual trusts", "trustee aware of GST consequences"],
        primary_authority=["IRC 2601-2664", "Treas. Reg. 26.2632-1", "Texas Property Code 112.036 (RAP abolished)", "GST Tax Regulations"],
        controlling_precedent="PLR 200241002 - dynasty trust with GST exemption approved",
        burden_holder="Trustee must track GST exemption and inclusion ratio",
        adversary_position="IRS may challenge late allocation or argue exemption wasted",
        counter_arguments=["exemption not timely allocated", "inclusion ratio miscalculated", "state RAP still applies", "no skip persons exist", "exemption allocated to wrong trust"],
        resolution_strategy="Allocate GST exemption on timely filed gift tax return. Use dynasty trust in perpetuities-friendly state.",
        entity_scope="trusts for grandchildren or later generations",
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Trust Decanting - Trustee Power to Modify",
        keywords=["decanting", "trustee modification", "distribution power", "UTC 417", "new trust", "second trust"],
        conclusion_template="Decanting allows trustee with discretionary distribution power to distribute to new trust with modified terms. UTC 417 or state decanting statute required. Cannot reduce beneficiary interests.",
        reasoning_framework="""1. Decanting = pour trust assets into new trust with different terms
2. Requires discretionary distribution power in original trust
3. Cannot eliminate mandatory income beneficiary
4. Cannot extend vesting beyond original perpetuities period
5. Can change administrative provisions freely
6. Notice to beneficiaries required in most states
7. Tax consequences must be considered (grantor trust status, etc.)""",
        key_factors=["trustee has discretionary power", "new trust terms permissible", "beneficiary interests preserved", "notice given", "tax status maintained", "state allows decanting"],
        primary_authority=["UTC 417", "Restatement (Third) of Trusts 75", "Texas Property Code 112.071-112.087", "Uniform Trust Decanting Act"],
        controlling_precedent="Morse v. Kraft, 992 N.E.2d 1021 (Mass. 2013) - decanting approved under common law",
        burden_holder="Trustee must prove authority to decant and compliance with restrictions",
        adversary_position="Decanting violates settlor intent or impermissibly modifies beneficiary rights",
        counter_arguments=["no discretionary power exists", "mandatory income eliminated", "vesting extended", "notice inadequate", "tax consequences adverse", "settlor intent violated"],
        resolution_strategy="Confirm discretionary power exists. Preserve mandatory beneficiary rights. Give notice. Document tax analysis.",
        entity_scope="trusts with discretionary distribution provisions",
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.TRUST_MODIFICATION
    ),
    DoctrineBlock(
        topic="Virtual Representation - Binding Absent Beneficiaries",
        keywords=["virtual representation", "representation", "unborn beneficiaries", "minors", "UTC 304", "adequate representation"],
        conclusion_template="Virtual representation allows one beneficiary to represent and bind another with substantially identical interests. UTC 304. Avoids need for guardian ad litem in many proceedings.",
        reasoning_framework="""1. Virtual rep binds those with same interests (e.g., parent represents minor children)
2. Interests must be substantially identical, not conflicting
3. No conflict of interest between representative and represented
4. Adequate representation required - representative must act reasonably
5. Unborn beneficiaries can be represented
6. Court may appoint guardian ad litem if conflict exists
7. All interested parties must be represented for binding judgment""",
        key_factors=["interests substantially identical", "no conflict of interest", "representative adequately protecting interests", "all parties represented", "court approves representation"],
        primary_authority=["UTC 304", "Restatement (Third) of Trusts 73", "Texas Property Code 115.013", "Texas Estates Code Ch. 1301"],
        controlling_precedent="Terrell v. Terrell, 44 S.W.3d 632 (Tex. App. 2001) - virtual representation approved",
        burden_holder="Party invoking virtual representation must prove identical interests and adequate representation",
        adversary_position="Interests actually conflict or representation inadequate",
        counter_arguments=["conflict of interest exists", "interests not identical", "representative not acting reasonably", "unborn class too remote", "guardian ad litem required"],
        resolution_strategy="Carefully analyze whether interests truly identical. Appoint GAL if any doubt about conflict.",
        entity_scope="trust proceedings with minors or unborn beneficiaries",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Trustee Compensation - Reasonable Fees",
        keywords=["trustee compensation", "fees", "reasonable compensation", "corporate trustee", "UTC 708", "fee dispute"],
        conclusion_template="Trustee entitled to reasonable compensation. Trust terms control if specified. Corporate trustees use published fee schedules. UTC 708. Court reviews for reasonableness.",
        reasoning_framework="""1. Trust instrument controls compensation if specified
2. If silent, trustee entitled to reasonable compensation
3. Reasonableness factors: time spent, difficulty, skill required, results
4. Corporate trustees typically use published fee schedules
5. Family members may serve without compensation
6. Dual compensation for lawyer-trustees limited
7. Court may reduce excessive fees or deny fees for breach""",
        key_factors=["trust specifies compensation", "fees reasonable for services", "corporate vs individual trustee", "time and effort expended", "complexity of administration", "results achieved"],
        primary_authority=["UTC 708", "Restatement (Third) of Trusts 38", "Texas Property Code 114.061", "Matter of Brock, 18 N.Y.3d 257 (2011)"],
        controlling_precedent="In re Hunter, 4 N.Y.3d 260 (2005) - corporate trustee fee schedule reasonable",
        burden_holder="Trustee seeking fees must justify reasonableness",
        adversary_position="Fees excessive for services rendered or breach occurred",
        counter_arguments=["trust terms specify different amount", "services unnecessary", "poor results", "breach of duty", "fees excessive", "dual compensation improper"],
        resolution_strategy="Apply trust terms if clear. Use fee schedules for corporate trustees. Consider results and difficulty.",
        entity_scope="all compensated trustees",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Revocable Trust - Settlor Rights and Control",
        keywords=["revocable trust", "settlor control", "amendment", "revocation", "living trust", "UTC 603"],
        conclusion_template="Settlor of revocable trust retains full control - can amend, revoke, or terminate. During settlor's life, beneficiaries have no enforceable rights. UTC 603. Becomes irrevocable on death.",
        reasoning_framework="""1. Revocable trust = will substitute, no gift on creation
2. Settlor can modify or revoke at any time while competent
3. Beneficiaries have no standing to sue during settlor's life
4. Trustee owes duties to settlor, not beneficiaries
5. Trust becomes irrevocable on settlor's death (if not revoked)
6. Method of revocation must comply with trust terms
7. Presumption of revocability under UTC if not specified""",
        key_factors=["trust expressly revocable", "settlor competent", "proper revocation method used", "settlor still alive", "amendment in writing", "trustee notified"],
        primary_authority=["UTC 603", "Restatement (Third) of Trusts 63", "Texas Property Code 112.051", "Farkas v. Williams, 125 N.E.2d 600 (Ill. 1955)"],
        controlling_precedent="Trosch v. Maryland Nat'l Bank, 32 A.2d 249 (Md. 1943) - settlor retains control of revocable trust",
        burden_holder="Party challenging revocation must prove invalidity (incapacity, undue influence, improper method)",
        adversary_position="Settlor lacked capacity or amendment improper",
        counter_arguments=["settlor incapacitated", "undue influence", "revocation method improper", "trust irrevocable by terms", "amendment conflicts with intent"],
        resolution_strategy="Uphold settlor amendments unless incapacity or undue influence proven. Follow trust terms for method.",
        entity_scope="revocable living trusts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Trust Protector - Third-Party Oversight Powers",
        keywords=["trust protector", "trust advisor", "directed trustee", "third party powers", "UTC 808", "oversight"],
        conclusion_template="Trust protector holds powers over trust that settlor does not wish to grant trustee or beneficiaries. Can modify terms, remove trustee, direct investments. UTC 808 recognizes directed trusts.",
        reasoning_framework="""1. Trust protector = independent third party with specified powers
2. Common powers: modify terms, remove/appoint trustees, direct investments
3. Directed trustee follows protector directions (no liability if reasonable)
4. Protector is fiduciary with duties to beneficiaries
5. UTC 808 permits division of trustee responsibilities
6. Useful for dynasty trusts needing flexibility
7. Must clearly define powers and duties in trust instrument""",
        key_factors=["trust instrument grants powers", "protector acts within authority", "protector is fiduciary", "directions reasonable", "directed trustee follows directions", "no self-dealing"],
        primary_authority=["UTC 808", "Restatement (Third) of Trusts 75", "Texas Property Code 114.0031", "Minassian v. Rachins, 152 So.3d 719 (Fla. App. 2014)"],
        controlling_precedent="Rollins v. Branch Banking & Trust Co., 56 A.3d 719 (Md. 2012) - trust protector powers enforceable",
        burden_holder="Trust protector must prove authority and reasonableness of action",
        adversary_position="Protector exceeded authority or breached fiduciary duty",
        counter_arguments=["powers not granted by trust", "protector breached duty", "direction unreasonable", "self-dealing", "conflict of interest", "beneficiaries should consent"],
        resolution_strategy="Enforce protector powers as specified in trust. Apply fiduciary standards to protector actions.",
        entity_scope="trusts with trust protector provisions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Breach of Trust - Remedies and Surcharge",
        keywords=["breach of trust", "surcharge", "damages", "removal", "constructive trust", "UTC 1001", "remedies"],
        conclusion_template="Beneficiary may sue for breach of trust seeking damages, accounting, removal, or constructive trust. Measure of damages: loss to trust or trustee's gain. UTC 1001-1003.",
        reasoning_framework="""1. Breach of trust = violation of fiduciary duty
2. Remedies: surcharge (damages), removal, accounting, constructive trust, tracing
3. Damages = greater of loss to trust or profit to trustee
4. Causation required - breach must cause loss
5. Trustee liable for co-trustee breach if participated or failed to prevent
6. Statute of limitations: typically 1 year from report, 5 years from breach
7. Exculpatory clauses valid only if not inserted by trustee""",
        key_factors=["breach proven", "loss or gain quantified", "causation shown", "statute of limitations not expired", "exculpatory clause absent", "demand for accounting made"],
        primary_authority=["UTC 1001-1003", "Restatement (Third) of Trusts 100-103", "Texas Property Code 114.008", "Slay v. Burnett Trust, 143 S.W.2d 700 (Tex. 1940)"],
        controlling_precedent="Gibbs v. Gibbs, 210 S.W.3d 511 (Tex. App. 2006) - measure of damages for breach",
        burden_holder="Beneficiary must prove breach, causation, and damages",
        adversary_position="No breach occurred or no damages resulted",
        counter_arguments=["actions within discretion", "business judgment protected", "no causation", "exculpatory clause applies", "statute of limitations bars claim", "beneficiary consented"],
        resolution_strategy="Measure damages carefully. Use trustee's profit if greater than trust's loss. Remove trustee for serious breach.",
        entity_scope="all breach of trust claims",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.BREACH
    ),
    DoctrineBlock(
        topic="Trust Accounting - Principal and Income Allocation",
        keywords=["trust accounting", "principal", "income", "receipts", "disbursements", "UPIA", "allocation", "fiduciary accounting"],
        conclusion_template="Trust accounting must separately account for principal and income. UPIA provides default allocation rules. Trustee must maintain clear records and provide annual accountings. Texas Property Code Ch. 116.",
        reasoning_framework="""1. Principal = corpus of trust (original assets + capital gains)
2. Income = rents, interest, dividends, royalties
3. UPIA provides detailed allocation rules for receipts and expenses
4. Trustee may adjust between principal and income if prudent
5. Fiduciary accounting differs from tax or GAAP accounting
6. Regular accountings required - annual or per trust terms
7. Beneficiaries can demand informal or formal accounting""",
        key_factors=["receipts properly allocated", "expenses properly charged", "adjustments documented", "UPIA rules followed", "accounting provided to beneficiaries", "records maintained"],
        primary_authority=["Uniform Principal and Income Act", "Texas Property Code Ch. 116", "UTC 813", "Restatement (Third) of Trusts 85"],
        controlling_precedent="Wood v. U.S. Bank, 828 N.E.2d 1072 (Ohio App. 2005) - proper allocation under UPIA",
        burden_holder="Trustee must prove proper accounting and allocation",
        adversary_position="Allocations improper or records inadequate",
        counter_arguments=["UPIA not followed", "power to adjust abused", "records incomplete", "income improperly charged to principal", "capital gains allocated wrong"],
        resolution_strategy="Follow UPIA default rules unless trust provides otherwise. Document all adjustments. Maintain detailed records.",
        entity_scope="all trusts with income beneficiaries",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ACCOUNTING
    ),
    DoctrineBlock(
        topic="Special Needs Trust - Preserving Government Benefits",
        keywords=["special needs trust", "supplemental needs", "SSI", "Medicaid", "disability benefits", "d4A trust", "third party SNT"],
        conclusion_template="Special needs trust (SNT) provides for disabled beneficiary without disqualifying from SSI/Medicaid. Must be supplemental to government benefits, not substitute. Trustee discretion critical.",
        reasoning_framework="""1. SNT preserves eligibility for means-tested benefits (SSI, Medicaid)
2. Two types: third-party SNT (no payback) and self-settled d4A (Medicaid payback)
3. Distributions must supplement, not supplant government benefits
4. Food and shelter reduce SSI dollar-for-dollar (in-kind support)
5. Sole benefit rule for self-settled trusts
6. Trustee must understand benefit programs and distribution rules
7. Pooled trusts available if no individual trustee""",
        key_factors=["trust properly drafted", "distributions supplemental only", "avoid food/shelter if possible", "trustee understands SSI rules", "self-settled trust has payback", "under age 65 if self-settled"],
        primary_authority=["42 U.S.C. 1396p(d)(4)(A)", "20 CFR 416.1201", "POMS SI 01120.200", "Texas Human Resources Code 142.005"],
        controlling_precedent="Lewis v. Alexander, 685 F.3d 325 (3d Cir. 2012) - SNT interpretation",
        burden_holder="Trustee must prove distributions do not violate benefit rules",
        adversary_position="SSA/Medicaid may argue trust is available resource or distributions are income",
        counter_arguments=["trust assets countable resource", "distributions constitute income", "food/shelter provided", "not solely for benefit", "trustee is beneficiary", "age over 65"],
        resolution_strategy="Draft trust to comply with statutory safe harbor. Avoid food/shelter distributions. Use professional SNT trustee.",
        entity_scope="trusts for disabled beneficiaries receiving government benefits",
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Charitable Remainder Trust - Split Interest Requirements",
        keywords=["charitable remainder trust", "CRT", "CRUT", "CRAT", "split interest", "IRC 664", "charitable deduction"],
        conclusion_template="Charitable remainder trust pays income to non-charitable beneficiaries for term, then remainder to charity. Must meet IRC 664 requirements: 5-50% payout, 10% remainder value, no additional contributions (CRAT).",
        reasoning_framework="""1. CRT = split interest trust with income to individual, remainder to charity
2. Two types: CRAT (annuity) pays fixed dollar amount, CRUT (unitrust) pays % of FMV
3. Payout rate: 5% minimum, 50% maximum
4. 10% probability test: remainder must be at least 10% of initial FMV
5. Income tax deduction for PV of remainder interest
6. Trust is tax-exempt, no capital gains on sale of assets
7. Strict compliance with IRC 664 required - no substantial deviation""",
        key_factors=["trust meets IRC 664 requirements", "qualified charity named", "payout rate 5-50%", "10% remainder test satisfied", "no additional contributions to CRAT", "proper payout calculation"],
        primary_authority=["IRC 664", "Treas. Reg. 1.664-1 to 1.664-4", "Rev. Proc. 2005-52 (sample forms)", "PLR 200537031"],
        controlling_precedent="Estate of Atkinson v. Commissioner, 115 T.C. 26 (2000) - strict compliance required",
        burden_holder="Taxpayer claiming deduction must prove IRC 664 compliance",
        adversary_position="IRS may disqualify CRT for technical defects",
        counter_arguments=["payout rate exceeds 50%", "10% test failed", "additional contributions made", "non-qualified charity", "deviation from requirements", "impermissible provisions"],
        resolution_strategy="Use IRS sample forms. Calculate 10% test carefully. No modifications unless specifically permitted.",
        entity_scope="charitable remainder trusts",
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Dynasty Trust - Perpetuities and Asset Protection",
        keywords=["dynasty trust", "perpetual trust", "rule against perpetuities", "asset protection", "multi-generational", "Alaska Delaware Nevada"],
        conclusion_template="Dynasty trust avoids estate tax for multiple generations by allocating GST exemption. Many states (AK, DE, SD, NV, TX) repealed Rule Against Perpetuities allowing perpetual trusts.",
        reasoning_framework="""1. Dynasty trust designed to last multiple generations (perpetually if allowed)
2. GST exemption allocated to avoid generation-skipping tax
3. Many states repealed or extended RAP (lives in being + 21 years)
4. Discretionary distributions and spendthrift clauses protect from creditors
5. Trust protector provides flexibility over long term
6. State selection important - favorable trust laws (AK, DE, SD, NV, WY)
7. Must consider state income tax on trusts""",
        key_factors=["state allows perpetual trusts", "GST exemption allocated", "spendthrift clause included", "discretionary distributions", "trust protector appointed", "favorable situs state"],
        primary_authority=["Texas Property Code 112.036 (RAP abolished)", "Alaska Stat. 34.27.051", "Delaware Code Title 25 503", "Restatement (Third) of Property (Wills)"],
        controlling_precedent="Cook v. Horn, 104 S.W.3d 233 (Tex. 2003) - RAP analysis",
        burden_holder="Trust proponent must prove compliance with applicable perpetuities rule",
        adversary_position="Trust violates RAP or GST exemption not properly allocated",
        counter_arguments=["state RAP still applies", "no GST exemption allocated", "inclusion ratio > 0", "tax apportionment issues", "state income tax burden"],
        resolution_strategy="Use perpetuities-friendly state. Allocate GST exemption timely. Include flexibility provisions (protector, decanting).",
        entity_scope="multi-generational wealth transfer trusts",
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Unitrust Conversion - UPIA Power to Adjust",
        keywords=["unitrust", "total return", "unitrust conversion", "UPIA 104", "power to adjust", "income definition"],
        conclusion_template="UPIA 104 allows trustee to adjust between principal and income to be fair to both income and remainder beneficiaries. Unitrust conversion defines income as fixed % of trust value (e.g., 4%).",
        reasoning_framework="""1. Traditional trusts allocate actual income (dividends, interest, rents)
2. Total return investing may produce low income but high appreciation
3. UPIA 104 power to adjust allows transfer from principal to income
4. Unitrust conversion defines income as % of FMV (typically 3-5%)
5. Factors for adjustment: trust purposes, income/remainder needs, other resources
6. Cannot adjust if contrary to trust terms or tax status
7. Notice to beneficiaries and documentation required""",
        key_factors=["UPIA adopted", "trust does not prohibit adjustment", "adjustment fair to all beneficiaries", "tax status preserved", "notice given", "reasons documented"],
        primary_authority=["Uniform Principal and Income Act 104", "Texas Property Code 116.005", "Restatement (Third) of Trusts 79", "Matter of Heller, 6 Misc.3d 284 (N.Y. Sur. 2004)"],
        controlling_precedent="In re Tuttle, 223 P.3d 1146 (Kan. 2010) - unitrust conversion approved",
        burden_holder="Trustee must prove adjustment fair and within statutory criteria",
        adversary_position="Adjustment unfair or not permitted by trust terms",
        counter_arguments=["trust prohibits adjustment", "tax status jeopardized", "unfair to one class", "not necessary", "percentage too high/low", "notice inadequate"],
        resolution_strategy="Follow UPIA criteria. Document reasons. Give notice. Consider tax consequences. Use reasonable percentage (3-5%).",
        entity_scope="trusts governed by UPIA",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Trust Termination - Uneconomic to Continue",
        keywords=["trust termination", "uneconomic trust", "small trust", "UTC 414", "administrative expense", "cost exceeds benefit"],
        conclusion_template="Court may terminate trust if value less than $50,000 and continuation would defeat or substantially impair trust purposes. UTC 414. Trustee may terminate trust under $50K if costs exceed benefits.",
        reasoning_framework="""1. Small trust termination if value < $50K (UTC 414)
2. Trustee may terminate without court approval if uneconomic
3. Must give notice to beneficiaries
4. Distribute in manner consistent with trust purposes
5. Weighs administrative costs against benefit to beneficiaries
6. Higher threshold possible if trust terms or state law allows
7. Alternative: consolidate with other trusts to reduce costs""",
        key_factors=["trust value under $50K", "administrative costs excessive", "termination consistent with purposes", "notice given to beneficiaries", "no objection from beneficiaries", "distribution plan reasonable"],
        primary_authority=["UTC 414", "Restatement (Third) of Trusts 66", "Texas Property Code 112.059", "In re Estate of Brown, 528 A.2d 752 (Vt. 1987)"],
        controlling_precedent="In re McCauley's Estate, 565 S.W.2d 88 (Tex. Civ. App. 1978) - trust terminated as uneconomic",
        burden_holder="Trustee must prove trust uneconomic to continue",
        adversary_position="Beneficiary may object if trust serves important non-financial purpose",
        counter_arguments=["trust value sufficient", "costs reasonable", "non-financial purposes important", "beneficiaries object", "improper distribution plan"],
        resolution_strategy="Calculate annual costs vs benefits. Give notice. Distribute to further purposes. Consider consolidation alternative.",
        entity_scope="small trusts with high administrative costs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TERMINATION
    ),
    DoctrineBlock(
        topic="Trustee Delegation - Investment and Administrative Functions",
        keywords=["delegation", "investment advisor", "agent", "UTC 807", "prudent delegation", "directed trustee", "outsourcing"],
        conclusion_template="Trustee may delegate investment and administrative functions to agents. Must exercise reasonable care in selecting, instructing, and monitoring agents. UTC 807. Prudent investor rule permits delegation.",
        reasoning_framework="""1. Modern rule permits delegation of investment and administrative functions
2. Non-delegable: decisions on distribution to beneficiaries
3. Trustee must use reasonable care in selecting agent
4. Must give agent clear instructions and appropriate authority
5. Duty to periodically review agent performance
6. Trustee liable for agent if improper selection/supervision
7. Agent owes duties to trustee, not beneficiaries (unless directed trust)""",
        key_factors=["agent properly selected", "instructions clear", "authority appropriate", "periodic review conducted", "agent qualified", "costs reasonable"],
        primary_authority=["UTC 807", "Uniform Prudent Investor Act 9", "Restatement (Third) of Trusts 80-81", "Texas Property Code 117.006"],
        controlling_precedent="Estate of Collins v. Geist, 83 Cal.Rptr.3d 382 (Cal. App. 2008) - proper delegation",
        burden_holder="Trustee must prove reasonable care in delegation",
        adversary_position="Trustee improperly delegated or failed to supervise",
        counter_arguments=["duty non-delegable", "agent improperly selected", "no supervision", "costs excessive", "instructions inadequate", "trustee abdicated responsibility"],
        resolution_strategy="Use qualified professionals. Document selection process. Establish monitoring procedures. Review performance regularly.",
        entity_scope="all trustees delegating functions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TRUSTEE_DUTY
    ),
    DoctrineBlock(
        topic="Qualified Personal Residence Trust - Estate Tax Reduction",
        keywords=["QPRT", "personal residence trust", "IRC 2702", "residence", "gift tax", "estate freeze", "retained interest"],
        conclusion_template="Qualified Personal Residence Trust (QPRT) allows transfer of residence to trust, retaining right to live there for term of years. Reduces gift tax value. IRC 2702 exception to retained interest rules.",
        reasoning_framework="""1. QPRT = grantor trust holding personal residence
2. Grantor retains right to live in residence for term of years
3. Remainder passes to beneficiaries at end of term
4. Gift value = FMV of residence - PV of retained interest
5. If grantor survives term, residence out of estate
6. If grantor dies during term, residence included in estate
7. Can convert to regular trust or sell residence with reinvestment period""",
        key_factors=["qualified personal residence", "term of years specified", "grantor survives term", "no sale during term (or proper reinvestment)", "IRC 2702 requirements met", "proper valuation"],
        primary_authority=["IRC 2702", "Treas. Reg. 25.2702-5", "Rev. Proc. 2003-42 (sample forms)", "PLR 200426008"],
        controlling_precedent="Estate of Magnin v. Commissioner, T.C. Memo 2001-31 - QPRT valuation",
        burden_holder="Taxpayer must prove IRC 2702 compliance",
        adversary_position="IRS may challenge if requirements not met or residence disqualified",
        counter_arguments=["not qualified personal residence", "term exceeded life expectancy", "sale improper", "grantor died during term", "defective trust provisions"],
        resolution_strategy="Use IRS sample form. Choose term based on life expectancy. Plan for contingency if grantor survives term.",
        entity_scope="estate planning for high-value residences",
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Alaska Self-Settled Asset Protection Trust - Creditor Shield",
        keywords=["self-settled trust", "asset protection", "Alaska trust", "creditor protection", "domestic asset protection trust", "DAPT", "fraudulent transfer"],
        conclusion_template="Alaska and other states (DE, NV, SD) allow self-settled asset protection trusts. Settlor can be discretionary beneficiary while protecting assets from creditors. Subject to fraudulent transfer attack.",
        reasoning_framework="""1. Traditional rule: self-settled trusts provide no creditor protection
2. Alaska (1997), Delaware, Nevada, others allow exception
3. Requirements: spendthrift clause, independent trustee, discretionary distributions
4. Trust must be irrevocable, situs in Alaska with Alaska trustee
5. Fraudulent transfer look-back period (typically 4 years Alaska)
6. Exception creditors: pre-existing creditors, alimony/child support, government
7. Full faith and credit issue - other states may not recognize""",
        key_factors=["trust situs in DAPT state", "independent trustee", "discretionary distributions only", "no fraudulent transfer", "beyond look-back period", "spendthrift clause"],
        primary_authority=["Alaska Stat. 34.40.110", "Delaware Code Title 12 3570-3576", "Restatement (Third) of Trusts 58 cmt. e", "Toni 1 Trust v. Wacker, 413 P.3d 1199 (Alaska 2018)"],
        controlling_precedent="Battley v. Mortensen, 2004 WL 1746194 (Alaska Super. 2004) - Alaska DAPT upheld",
        burden_holder="Creditor must prove fraudulent transfer or exception applies",
        adversary_position="Creditor argues trust is fraudulent transfer or home state law applies",
        counter_arguments=["fraudulent transfer", "pre-existing creditor", "badges of fraud", "home state won't recognize", "child support claim", "bankruptcy trustee"],
        resolution_strategy="Establish trust before creditor issues arise. Use proper situs state. Independent trustee. Wait out look-back period.",
        entity_scope="self-settled asset protection planning",
        confidence=ConfidenceLevel.HIGH_RISK,
        issue_category=IssueCategory.ADMINISTRATION
    ),
    DoctrineBlock(
        topic="Nonjudicial Settlement Agreement - Consent Modification",
        keywords=["nonjudicial settlement", "NSA", "UTC 111", "beneficiary consent", "modification without court", "interested persons"],
        conclusion_template="UTC 111 permits nonjudicial settlement agreements among interested persons to resolve trust matters without court approval. Cannot violate material purpose or rights of non-consenting beneficiaries.",
        reasoning_framework="""1. Nonjudicial settlement can approve/disapprove trustee reports, direct trustee, modify terms
2. Requires agreement of all interested persons or their representatives
3. Cannot violate material purpose of trust
4. Cannot reduce fixed or ascertainable beneficial interests without consent
5. Binding on all parties including those represented
6. Faster and cheaper than court proceedings
7. Some matters still require court (contested removal, surcharge)""",
        key_factors=["all interested persons agree", "no material purpose violated", "no impairment of fixed interests", "virtual representation proper", "settlement in writing", "no fraud or duress"],
        primary_authority=["UTC 111", "Restatement (Third) of Trusts 73", "Texas Property Code 115.001-115.018", "Uniform Trust Code Official Comments"],
        controlling_precedent="Ferris v. Ferris, 239 P.3d 934 (Okla. Civ. App. 2010) - NSA approved under UTC",
        burden_holder="Party seeking to enforce NSA must prove all interested persons agreed",
        adversary_position="Non-consenting party argues material purpose violated or inadequate representation",
        counter_arguments=["not all interested persons agreed", "material purpose violated", "fixed interest impaired", "virtual representation improper", "fraud or duress"],
        resolution_strategy="Identify all interested persons. Obtain written consent. Ensure no material purpose frustrated. Use virtual representation properly.",
        entity_scope="all UTC trusts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TRUST_MODIFICATION
    )
]

METRICS = {
    "total_queries": 0,
    "cache_hits": 0,
    "semantic_retrievals": 0,
    "deep_analyses": 0,
    "avg_latency_ms": 0.0,
    "error_count": 0
}

AUDIT_LOG = []

def query_doctrine_cache(query: str, top_k: int = 3) -> List[DoctrineBlock]:
    """Layer 1: Fast doctrine cache lookup"""
    query_lower = query.lower()
    scored = []
    for block in DOCTRINE_CACHE:
        score = sum(1 for kw in block.keywords if kw.lower() in query_lower)
        if score > 0:
            scored.append((score, block))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [block for _, block in scored[:top_k]]

def semantic_retrieval(query: str, top_k: int = 2) -> List[DoctrineBlock]:
    """Layer 2: Semantic search fallback"""
    query_words = set(query.lower().split())
    scored = []
    for block in DOCTRINE_CACHE:
        topic_words = set(block.topic.lower().split())
        framework_words = set(block.reasoning_framework.lower().split())
        overlap = len(query_words & (topic_words | framework_words))
        if overlap > 0:
            scored.append((overlap, block))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [block for _, block in scored[:top_k]]

def deep_analysis(query: str, doctrines: List[DoctrineBlock]) -> str:
    """Layer 3: Multi-doctrine synthesis"""
    if not doctrines:
        return "No applicable doctrine found. This may require specialized trust analysis outside standard UTC framework."

    sections = []
    sections.append(f"TRUST ADMINISTRATION ANALYSIS - {len(doctrines)} doctrines apply\n")

    for i, d in enumerate(doctrines, 1):
        sections.append(f"\n{i}. {d.topic.upper()}")
        sections.append(f"   Authority: {', '.join(d.primary_authority[:2])}")
        sections.append(f"   {d.conclusion_template}")
        sections.append(f"\n   Key Factors:")
        for factor in d.key_factors[:3]:
            sections.append(f"   - {factor}")
        if d.controlling_precedent:
            sections.append(f"\n   Controlling: {d.controlling_precedent}")

    sections.append("\n\nRESOLUTION STRATEGY:")
    sections.append(doctrines[0].resolution_strategy)

    sections.append("\n\nFIDUCIARY DUTY CONSIDERATIONS:")
    sections.append("Trustee must act with utmost good faith, exercise reasonable care and skill, and avoid conflicts of interest.")

    return "\n".join(sections)

def generate_response(query: str, mode: ResponseMode, context: Optional[Dict] = None) -> QueryResponse:
    """Three-layer response generation"""
    start_time = time.time()

    METRICS["total_queries"] += 1

    # Layer 1: Doctrine cache
    cache_results = query_doctrine_cache(query, top_k=3)
    if cache_results:
        METRICS["cache_hits"] += 1

    # Layer 2: Semantic retrieval if cache weak
    if len(cache_results) < 2:
        semantic_results = semantic_retrieval(query, top_k=2)
        METRICS["semantic_retrievals"] += 1
        cache_results.extend(semantic_results)

    # Remove duplicates
    seen = set()
    unique_results = []
    for d in cache_results:
        if d.topic not in seen:
            seen.add(d.topic)
            unique_results.append(d)

    # Layer 3: Deep analysis
    if mode == ResponseMode.FAST:
        answer = unique_results[0].conclusion_template if unique_results else "Insufficient doctrine coverage for this trust issue."
    elif mode == ResponseMode.DEFENSE:
        answer = deep_analysis(query, unique_results[:2])
        METRICS["deep_analyses"] += 1
    else:  # MEMO
        answer = deep_analysis(query, unique_results[:4])
        answer += "\n\nFULL REASONING:\n" + unique_results[0].reasoning_framework if unique_results else ""
        METRICS["deep_analyses"] += 1

    latency_ms = (time.time() - start_time) * 1000

    # Update rolling average latency
    total = METRICS["total_queries"]
    METRICS["avg_latency_ms"] = ((METRICS["avg_latency_ms"] * (total - 1)) + latency_ms) / total

    response = QueryResponse(
        query=query,
        answer=answer,
        mode=mode,
        confidence=unique_results[0].confidence if unique_results else ConfidenceLevel.DISCLOSURE,
        sources=[d.topic for d in unique_results[:3]],
        triggered_doctrines=[d.topic for d in unique_results],
        latency_ms=round(latency_ms, 2),
        determinism_hash=hashlib.sha256(answer.encode()).hexdigest()[:16],
        timestamp=datetime.utcnow().isoformat()
    )

    # Audit trail
    AUDIT_LOG.append({
        "timestamp": response.timestamp,
        "query": query,
        "mode": mode.value,
        "doctrines": response.triggered_doctrines,
        "latency_ms": response.latency_ms,
        "hash": response.determinism_hash
    })

    return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} trust law doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down - {METRICS['total_queries']} queries processed")

app = FastAPI(title=ENGINE_NAME, version=VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "metrics": METRICS,
        "uptime_queries": METRICS["total_queries"]
    }

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - three-layer trust analysis"""
    try:
        response = generate_response(request.query, request.mode, request.context)
        logger.info(f"Query processed: {request.query[:50]}... | Mode: {request.mode} | Latency: {response.latency_ms}ms")
        return response
    except Exception as e:
        METRICS["error_count"] += 1
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "category": d.issue_category.value,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/metrics")
async def get_metrics():
    """Telemetry metrics"""
    cache_hit_rate = (METRICS["cache_hits"] / METRICS["total_queries"] * 100) if METRICS["total_queries"] > 0 else 0
    return {
        "engine_id": ENGINE_ID,
        "total_queries": METRICS["total_queries"],
        "cache_hits": METRICS["cache_hits"],
        "cache_hit_rate_pct": round(cache_hit_rate, 2),
        "semantic_retrievals": METRICS["semantic_retrievals"],
        "deep_analyses": METRICS["deep_analyses"],
        "avg_latency_ms": round(METRICS["avg_latency_ms"], 2),
        "error_count": METRICS["error_count"],
        "error_rate_pct": round((METRICS["error_count"] / METRICS["total_queries"] * 100), 2) if METRICS["total_queries"] > 0 else 0
    }

@app.get("/audit")
async def get_audit_log(limit: int = 50):
    """Retrieve audit trail"""
    return {
        "total_entries": len(AUDIT_LOG),
        "entries": AUDIT_LOG[-limit:]
    }

if __name__ == "__main__":
    import uvicorn
    logger.add(f"prb05_trust_administration_{datetime.now().strftime('%Y%m%d')}.log", rotation="100 MB")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
