"""
LG15 International Law Engine - Doctrine Cache
================================================
50+ doctrine blocks covering public international law, trade law,
humanitarian law, human rights, arbitration, sanctions, and more.

Engine: LG15 | Version: 2.0.0 | TIE Pattern
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from loguru import logger

ENGINE_ROOT = Path(__file__).parent
DOCTRINE_CACHE_DIR = ENGINE_ROOT / "doctrine_cache"
DOCTRINE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_VERSION = "2.0.0"
ENGINE_ID = "LG15"
HASH_SALT = "LG15_INTERNATIONAL_LAW_v2"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class DoctrineCacheBlock:
    """Single doctrine block in the LG15 international law cache."""

    topic: str
    category: str
    authority_weight: float
    citations: List[str]
    content: str
    related_topics: List[str]
    last_verified: str
    hash_key: str = ""

    def __post_init__(self) -> None:
        if not self.hash_key:
            self.hash_key = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = f"{HASH_SALT}:{self.topic}:{self.category}:{self.content}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DoctrineCacheBlock":
        return cls(**data)


@dataclass
class DoctrineCacheIndex:
    """Index structure for fast doctrine look-ups."""

    engine_id: str = ENGINE_ID
    version: str = CACHE_VERSION
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    block_count: int = 0
    categories: Dict[str, int] = field(default_factory=dict)
    topic_to_category: Dict[str, str] = field(default_factory=dict)
    topic_to_hash: Dict[str, str] = field(default_factory=dict)
    integrity_hash: str = ""

    def rebuild(self, blocks: Dict[str, DoctrineCacheBlock]) -> None:
        self.block_count = len(blocks)
        self.categories = {}
        self.topic_to_category = {}
        self.topic_to_hash = {}
        for key, blk in blocks.items():
            cat = blk.category
            self.categories[cat] = self.categories.get(cat, 0) + 1
            self.topic_to_category[key] = cat
            self.topic_to_hash[key] = blk.hash_key
        self.integrity_hash = self._compute_integrity(blocks)

    @staticmethod
    def _compute_integrity(blocks: Dict[str, DoctrineCacheBlock]) -> str:
        combined = "|".join(sorted(b.hash_key for b in blocks.values()))
        return hashlib.sha256(combined.encode()).hexdigest()[:24]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Doctrine Blocks  (50+ blocks)
# ---------------------------------------------------------------------------

DOCTRINE_BLOCKS: Dict[str, DoctrineCacheBlock] = {}

def _add(topic: str, category: str, weight: float, citations: List[str],
         content: str, related: List[str], verified: str = "2026-02-01") -> None:
    DOCTRINE_BLOCKS[topic] = DoctrineCacheBlock(
        topic=topic, category=category, authority_weight=weight,
        citations=citations, content=content,
        related_topics=related, last_verified=verified,
    )


# ===== 1. UN CHARTER - USE OF FORCE =====
_add(
    topic="un_charter_use_of_force",
    category="public_international_law",
    weight=0.98,
    citations=[
        "UN Charter Art. 2(4)",
        "ICJ, Military and Paramilitary Activities in and against Nicaragua "
        "(Nicaragua v. United States), [1986] ICJ Rep 14",
        "ICJ, Armed Activities on the Territory of the Congo "
        "(DRC v. Uganda), [2005] ICJ Rep 168",
        "UNGA Res 2625 (XXV), Declaration on Friendly Relations (1970)",
    ],
    content=(
        "Article 2(4) of the UN Charter prohibits the threat or use of force "
        "against the territorial integrity or political independence of any state. "
        "The International Court of Justice in Nicaragua v. United States (1986) "
        "confirmed that the prohibition reflects customary international law binding "
        "on all states regardless of treaty status. The Court held that arming and "
        "training the contras constituted a use of force, while funding alone did not "
        "rise to that threshold but still breached the non-intervention principle. "
        "The prohibition extends to indirect uses of force, including organizing or "
        "encouraging irregular forces for incursion into another state (UNGA Res 2625). "
        "Exceptions are limited to self-defense under Article 51 and Security Council "
        "authorization under Chapter VII. The DRC v. Uganda decision reinforced that "
        "even consent-based military presence becomes unlawful when it exceeds the "
        "scope of the invitation. The jus cogens character of the prohibition means "
        "it cannot be derogated from by treaty or persistent objection."
    ),
    related=["un_charter_self_defense", "un_charter_chapter_vii",
             "customary_international_law", "jus_cogens_norms"],
)

# ===== 2. UN CHARTER - SELF-DEFENSE =====
_add(
    topic="un_charter_self_defense",
    category="public_international_law",
    weight=0.97,
    citations=[
        "UN Charter Art. 51",
        "ICJ, Nicaragua v. United States, [1986] ICJ Rep 14, para 176",
        "ICJ, Oil Platforms (Iran v. United States), [2003] ICJ Rep 161",
        "ICJ, Legal Consequences of the Construction of a Wall in the "
        "Occupied Palestinian Territory, Advisory Opinion, [2004] ICJ Rep 136",
        "Caroline Incident, 29 BFSP 1137-1138 (1837)",
    ],
    content=(
        "Article 51 preserves the inherent right of individual or collective "
        "self-defense if an armed attack occurs against a UN Member. The Caroline "
        "test (1837) established that self-defense must be necessary, proportionate, "
        "and an immediate response to an imminent threat leaving no moment for "
        "deliberation. In Nicaragua, the ICJ held that an armed attack must reach a "
        "certain gravity to trigger self-defense; mere frontier incidents or provision "
        "of weapons do not qualify. The Oil Platforms case clarified that the defending "
        "state bears the burden of proving an armed attack occurred and that its "
        "response was necessary and proportionate. The Wall Advisory Opinion suggested "
        "self-defense under Article 51 applies only to attacks attributable to another "
        "state, raising questions about self-defense against non-state actors. States "
        "must report self-defense measures to the Security Council immediately, and "
        "such measures are provisional until the Council takes action."
    ),
    related=["un_charter_use_of_force", "un_charter_chapter_vii",
             "state_responsibility_attribution"],
)

# ===== 3. UN CHARTER - CHAPTER VII =====
_add(
    topic="un_charter_chapter_vii",
    category="public_international_law",
    weight=0.96,
    citations=[
        "UN Charter Arts. 39-51",
        "UNSC Res 678 (1990) (authorization of force, Iraq-Kuwait)",
        "UNSC Res 1973 (2011) (Libya no-fly zone)",
        "ICJ, Questions of Interpretation and Application of the 1971 "
        "Montreal Convention (Libya v. United States), [1992] ICJ Rep 114",
    ],
    content=(
        "Chapter VII empowers the Security Council to determine the existence of a "
        "threat to the peace, breach of the peace, or act of aggression (Art. 39), "
        "and to decide on measures including economic sanctions (Art. 41) and military "
        "force (Art. 42). Decisions under Chapter VII are binding on all UN Members "
        "(Art. 25). Resolution 678 authorized member states to use all necessary means "
        "to restore international peace following Iraq's invasion of Kuwait, establishing "
        "the precedent for delegation of enforcement authority. Resolution 1973 authorized "
        "member states to take all necessary measures to protect civilians in Libya, "
        "explicitly excluding a foreign occupation force. The veto power of the five "
        "permanent members (Art. 27(3)) can block any substantive decision. In the "
        "Lockerbie case, the ICJ acknowledged the primacy of Security Council decisions "
        "under Article 103 over other treaty obligations. Targeted sanctions (asset "
        "freezes, travel bans) have largely replaced comprehensive economic sanctions "
        "to minimize civilian harm."
    ),
    related=["un_charter_use_of_force", "un_charter_self_defense",
             "ofac_sanctions_overview"],
)

# ===== 4. VIENNA CONVENTION - TREATY INTERPRETATION =====
_add(
    topic="vclt_treaty_interpretation",
    category="treaty_law",
    weight=0.96,
    citations=[
        "Vienna Convention on the Law of Treaties, 1155 UNTS 331, Arts. 31-32",
        "ICJ, Territorial Dispute (Libya v. Chad), [1994] ICJ Rep 6",
        "WTO AB, Japan - Taxes on Alcoholic Beverages, WT/DS8/AB/R (1996)",
        "WTO AB, US - Standards for Reformulated and Conventional Gasoline, "
        "WT/DS2/AB/R (1996)",
    ],
    content=(
        "Article 31 VCLT sets the general rule: a treaty shall be interpreted in good "
        "faith in accordance with the ordinary meaning of its terms in their context and "
        "in light of the treaty's object and purpose. Context includes the preamble, "
        "annexes, and any agreement or instrument made in connection with conclusion. "
        "Subsequent agreement and practice of the parties regarding interpretation is "
        "taken into account, along with any relevant rules of international law applicable "
        "between the parties. Article 32 permits recourse to supplementary means of "
        "interpretation, including preparatory work (travaux preparatoires) and "
        "circumstances of conclusion, when Article 31 leaves meaning ambiguous or leads "
        "to a manifestly absurd or unreasonable result. The WTO Appellate Body in "
        "US - Gasoline established that VCLT Arts. 31-32 have attained customary "
        "international law status and apply to WTO covered agreements. In Japan - "
        "Alcoholic Beverages, the AB confirmed that adopted GATT panel reports create "
        "legitimate expectations among WTO Members and should be taken into account."
    ),
    related=["vclt_reservations", "vclt_jus_cogens",
             "wto_dispute_settlement", "treaty_termination"],
)

# ===== 5. VCLT - RESERVATIONS =====
_add(
    topic="vclt_reservations",
    category="treaty_law",
    weight=0.88,
    citations=[
        "VCLT Arts. 19-23",
        "ICJ, Reservations to the Convention on Genocide, Advisory Opinion, "
        "[1951] ICJ Rep 15",
        "ILC, Guide to Practice on Reservations to Treaties (2011)",
        "Belilos v. Switzerland, ECtHR App. No. 10328/83 (1988)",
    ],
    content=(
        "Under VCLT Article 19, a state may formulate a reservation upon signature, "
        "ratification, acceptance, approval, or accession unless the treaty prohibits "
        "it, allows only specified reservations, or the reservation is incompatible "
        "with the object and purpose of the treaty. The ICJ's 1951 Advisory Opinion "
        "on the Genocide Convention introduced the compatibility test: a reservation is "
        "permissible if it does not defeat the object and purpose of the treaty, even "
        "absent unanimous acceptance by other parties. Under Article 20, acceptance by "
        "another party establishes treaty relations with the reserving state, while "
        "objection does not preclude entry into force unless the objecting state "
        "definitely expresses that intention. The European Court of Human Rights in "
        "Belilos held that impermissible reservations are severable, meaning the state "
        "remains bound by the treaty without the benefit of the reservation. The ILC "
        "Guide to Practice (2011) codified detailed guidance on formulation, withdrawal, "
        "and effects of reservations and interpretive declarations."
    ),
    related=["vclt_treaty_interpretation", "vclt_jus_cogens",
             "iccpr_civil_political_rights"],
)

# ===== 6. JUS COGENS =====
_add(
    topic="vclt_jus_cogens",
    category="treaty_law",
    weight=0.97,
    citations=[
        "VCLT Arts. 53, 64",
        "ICJ, Barcelona Traction, Light and Power Company, Limited "
        "(Belgium v. Spain), [1970] ICJ Rep 3, paras 33-34",
        "ILC, Draft Articles on the Responsibility of States for "
        "Internationally Wrongful Acts (2001), Art. 26",
        "ILC, Draft Conclusions on Peremptory Norms (2022)",
    ],
    content=(
        "VCLT Article 53 defines a peremptory norm of general international law "
        "(jus cogens) as one accepted and recognized by the international community "
        "of states as a whole as a norm from which no derogation is permitted and "
        "which can only be modified by a subsequent norm of the same character. A "
        "treaty conflicting with jus cogens at the time of conclusion is void "
        "(Art. 53); if a new jus cogens norm emerges, any conflicting treaty becomes "
        "void and terminates (Art. 64). The Barcelona Traction case introduced "
        "obligations erga omnes, owed to the international community as a whole, "
        "closely linked to jus cogens norms. Widely recognized jus cogens norms "
        "include the prohibitions on genocide, slavery, racial discrimination, "
        "torture, aggression, and the right to self-determination. The ILC Articles "
        "on State Responsibility confirm that no circumstance precludes wrongfulness "
        "of an act not in conformity with a jus cogens obligation (Art. 26). The "
        "ILC Draft Conclusions on Peremptory Norms (2022) provided a non-exhaustive "
        "list and methodology for identifying jus cogens norms, requiring acceptance "
        "and recognition by a very large majority of states."
    ),
    related=["un_charter_use_of_force", "genocide_convention",
             "state_responsibility_attribution", "vclt_reservations"],
)

# ===== 7. ICJ STATUTE - JURISDICTION =====
_add(
    topic="icj_jurisdiction",
    category="international_adjudication",
    weight=0.94,
    citations=[
        "ICJ Statute Arts. 34-38",
        "ICJ, Case Concerning the Arrest Warrant of 11 April 2000 "
        "(DRC v. Belgium), [2002] ICJ Rep 3",
        "ICJ, Nottebohm Case (Liechtenstein v. Guatemala), "
        "[1955] ICJ Rep 4",
        "ICJ, Nuclear Tests (Australia v. France), [1974] ICJ Rep 253",
    ],
    content=(
        "Only states may be parties before the ICJ (Art. 34). Jurisdiction is based "
        "on consent, which may be expressed through special agreement (compromis), "
        "treaty compromissory clause, or optional clause declaration under Article "
        "36(2). The Court applies international conventions, international custom, "
        "general principles of law, and judicial decisions and teachings as subsidiary "
        "sources (Art. 38). In Nottebohm, the Court examined the genuine link "
        "requirement for nationality of claims, holding that Liechtenstein lacked "
        "standing because Nottebohm had no genuine connection to Liechtenstein despite "
        "formal naturalization. The Arrest Warrant case addressed sovereign immunity "
        "of incumbent foreign ministers, finding that international law grants full "
        "immunity from criminal jurisdiction and personal inviolability while in "
        "office. In Nuclear Tests, the Court held that a unilateral declaration by "
        "France to cease atmospheric testing was legally binding, rendering the case "
        "moot. Forum prorogatum permits jurisdiction where the respondent participates "
        "in proceedings without objecting to jurisdiction."
    ),
    related=["icj_advisory_opinions", "icj_provisional_measures",
             "state_responsibility_attribution"],
)

# ===== 8. ICJ ADVISORY OPINIONS =====
_add(
    topic="icj_advisory_opinions",
    category="international_adjudication",
    weight=0.90,
    citations=[
        "ICJ Statute Arts. 65-68",
        "ICJ, Legality of the Threat or Use of Nuclear Weapons, "
        "Advisory Opinion, [1996] ICJ Rep 226",
        "ICJ, Legal Consequences of the Construction of a Wall in the "
        "Occupied Palestinian Territory, [2004] ICJ Rep 136",
        "ICJ, Accordance with International Law of the Unilateral "
        "Declaration of Independence in Respect of Kosovo, [2010] ICJ Rep 403",
    ],
    content=(
        "The ICJ may give advisory opinions on any legal question at the request of "
        "the General Assembly, Security Council, or other authorized UN organs and "
        "specialized agencies (Art. 65). Advisory opinions are not binding but carry "
        "significant legal authority and are treated as authoritative statements of "
        "international law. In the Nuclear Weapons opinion, the Court found that the "
        "threat or use of nuclear weapons would generally be contrary to international "
        "humanitarian law but could not definitively conclude whether use in extreme "
        "circumstances of self-defense would be lawful. The Wall Advisory Opinion held "
        "that Israel's construction of the wall in occupied Palestinian territory "
        "violated international law, including the right of self-determination, "
        "international humanitarian law, and human rights law. The Kosovo opinion "
        "concluded that the declaration of independence did not violate general "
        "international law, as international law contained no applicable prohibition. "
        "The Court may decline a request for advisory opinion only for compelling "
        "reasons, and has never done so in practice."
    ),
    related=["icj_jurisdiction", "icj_provisional_measures",
             "un_charter_chapter_vii"],
)

# ===== 9. ICJ PROVISIONAL MEASURES =====
_add(
    topic="icj_provisional_measures",
    category="international_adjudication",
    weight=0.91,
    citations=[
        "ICJ Statute Art. 41",
        "ICJ, LaGrand (Germany v. United States), [2001] ICJ Rep 466",
        "ICJ, Application of the Convention on the Prevention and "
        "Punishment of the Crime of Genocide (Bosnia v. Serbia), "
        "Provisional Measures, [1993] ICJ Rep 3",
        "ICJ, Allegations of Genocide (Ukraine v. Russia), "
        "Provisional Measures, [2022] ICJ Rep 211",
    ],
    content=(
        "Article 41 of the ICJ Statute empowers the Court to indicate provisional "
        "measures to preserve the respective rights of the parties. In LaGrand, the "
        "Court held for the first time that provisional measures orders are legally "
        "binding, not merely hortatory as previously assumed by some states. The "
        "threshold requires prima facie jurisdiction, plausible rights that need "
        "protection, a link between the measures sought and the rights claimed, and "
        "a risk of irreparable prejudice and urgency. In the Bosnia Genocide case, "
        "the Court ordered Yugoslavia to take all measures within its power to prevent "
        "genocide, though this was not complied with (Srebrenica occurred subsequently). "
        "In Ukraine v. Russia (2022), the Court ordered Russia to immediately suspend "
        "military operations commenced on 24 February 2022. Non-compliance with "
        "provisional measures can itself constitute a breach of an international "
        "obligation giving rise to state responsibility."
    ),
    related=["icj_jurisdiction", "icj_advisory_opinions",
             "genocide_convention"],
)

# ===== 10. WTO/GATT - MOST-FAVORED-NATION =====
_add(
    topic="wto_mfn_principle",
    category="international_trade_law",
    weight=0.95,
    citations=[
        "GATT 1994 Art. I:1",
        "WTO AB, EC - Regime for the Importation, Sale and Distribution "
        "of Bananas, WT/DS27/AB/R (1997)",
        "WTO AB, Canada - Certain Measures Affecting the Automotive "
        "Industry, WT/DS139/AB/R (2000)",
        "GATS Art. II",
    ],
    content=(
        "The MFN principle under GATT Article I:1 requires that any advantage, favour, "
        "privilege, or immunity granted by a WTO Member to products originating in or "
        "destined for any other country shall be accorded immediately and unconditionally "
        "to like products originating in or destined for all other WTO Members. The test "
        "is whether a measure accords an advantage to products from one country that is "
        "not accorded to like products from all WTO Members. In EC - Bananas III, the "
        "Appellate Body confirmed MFN applies to both de jure and de facto discrimination "
        "and extends to rules governing importation, including licensing procedures. In "
        "Canada - Autos, the AB found that origin-neutral conditions can still violate "
        "MFN if in practice the advantage accrues predominantly to imports from specific "
        "countries due to the structure of the measure. The MFN obligation applies to "
        "customs duties, charges, rules, formalities, and internal taxes and regulations. "
        "Exceptions include preferential trade agreements (Art. XXIV), GSP schemes "
        "(Enabling Clause), and waivers."
    ),
    related=["wto_national_treatment", "wto_dispute_settlement",
             "gatt_general_exceptions"],
)

# ===== 11. WTO - NATIONAL TREATMENT =====
_add(
    topic="wto_national_treatment",
    category="international_trade_law",
    weight=0.94,
    citations=[
        "GATT 1994 Art. III",
        "WTO AB, Japan - Taxes on Alcoholic Beverages, WT/DS8/AB/R (1996)",
        "WTO AB, Korea - Taxes on Alcoholic Beverages, WT/DS75/AB/R (1999)",
        "WTO AB, EC - Measures Affecting Asbestos and Products Containing "
        "Asbestos, WT/DS135/AB/R (2001)",
    ],
    content=(
        "GATT Article III requires that internal taxes (III:2) and regulations (III:4) "
        "not be applied so as to afford protection to domestic production. Under Art. "
        "III:2 first sentence, imported and domestic products that are 'like' cannot be "
        "taxed in excess of domestic products. Under the second sentence, directly "
        "competitive or substitutable imported products cannot be taxed dissimilarly so "
        "as to afford protection. In Japan - Alcoholic Beverages, the Appellate Body "
        "established that 'likeness' under the first sentence is a narrow concept "
        "determined by physical characteristics, end-uses, consumer preferences, and "
        "tariff classification. Under Article III:4, the AB in EC - Asbestos held "
        "that a measure banning chrysotile asbestos did not violate national treatment "
        "because the health risks meant asbestos-containing products were not 'like' "
        "non-asbestos products, considering competitive relationship, physical properties, "
        "end-uses, and consumer tastes. The chapeau of Article III establishes the "
        "overarching principle that internal measures should not be applied to afford "
        "protection."
    ),
    related=["wto_mfn_principle", "wto_dispute_settlement",
             "gatt_general_exceptions"],
)

# ===== 12. WTO - DISPUTE SETTLEMENT =====
_add(
    topic="wto_dispute_settlement",
    category="international_trade_law",
    weight=0.94,
    citations=[
        "DSU (Understanding on Rules and Procedures Governing the "
        "Settlement of Disputes)",
        "WTO AB, United States - Import Prohibition of Certain Shrimp "
        "and Shrimp Products, WT/DS58/AB/R (1998)",
        "WTO AB, EC - Measures Concerning Meat and Meat Products "
        "(Hormones), WT/DS26/AB/R (1998)",
        "WTO AB, US - Continued Suspension of Obligations in the "
        "EC - Hormones Dispute, WT/DS320/AB/R (2008)",
    ],
    content=(
        "The WTO DSU establishes a binding dispute settlement system with mandatory "
        "jurisdiction over WTO Members. Consultations are required before panel "
        "establishment. Panels make findings of fact and law, subject to appeal to "
        "the Appellate Body on issues of law. The Appellate Body, currently non-"
        "functional due to blocked appointments since 2019, normally has seven members "
        "serving four-year terms. In US - Shrimp, the AB held that unilateral trade "
        "measures for environmental protection could be justified under GATT Article "
        "XX(g) if applied in a non-discriminatory manner, requiring good faith efforts "
        "to negotiate multilateral solutions. In EC - Hormones, the AB clarified the "
        "standard of review, holding that panels should make an objective assessment "
        "of facts under DSU Article 11 and that the SPS Agreement's precautionary "
        "principle does not override specific obligations. Compliance is monitored "
        "under DSU Article 21.5, and non-compliance can authorize suspension of "
        "concessions (retaliation) under Article 22."
    ),
    related=["wto_mfn_principle", "wto_national_treatment",
             "gatt_general_exceptions", "wto_subsidies_scm"],
)

# ===== 13. WTO - SUBSIDIES AND COUNTERVAILING MEASURES =====
_add(
    topic="wto_subsidies_scm",
    category="international_trade_law",
    weight=0.90,
    citations=[
        "Agreement on Subsidies and Countervailing Measures (SCM)",
        "WTO AB, US - Tax Treatment for Foreign Sales Corporations, "
        "WT/DS108/AB/R (2000)",
        "WTO AB, Canada - Measures Affecting the Export of Civilian "
        "Aircraft, WT/DS70/AB/R (1999)",
        "WTO AB, EC and certain Member States - Large Civil Aircraft, "
        "WT/DS316/AB/R (2011)",
    ],
    content=(
        "The SCM Agreement defines a subsidy as a financial contribution by a government "
        "or public body that confers a benefit. A subsidy must be specific (to an "
        "enterprise, industry, or group) to be actionable. Prohibited subsidies are "
        "those contingent on export performance (Art. 3.1(a)) or on the use of domestic "
        "over imported goods (Art. 3.1(b)). Actionable subsidies cause adverse effects: "
        "injury to the domestic industry of another Member, nullification or impairment "
        "of benefits, or serious prejudice including significant price undercutting or "
        "displacement. In US - FSC, the AB found that tax exemptions contingent on "
        "export can constitute prohibited export subsidies. The Canada - Aircraft case "
        "established that 'benefit' is determined by comparison to the marketplace, not "
        "cost to government. In Airbus (EC - Large Civil Aircraft), the AB confirmed "
        "that launch aid constituted specific subsidies causing serious prejudice through "
        "displacement and lost sales. Countervailing duties may be imposed following an "
        "investigation demonstrating subsidized imports cause material injury."
    ),
    related=["wto_dispute_settlement", "wto_antidumping",
             "wto_mfn_principle"],
)

# ===== 14. WTO - ANTI-DUMPING =====
_add(
    topic="wto_antidumping",
    category="international_trade_law",
    weight=0.89,
    citations=[
        "GATT Art. VI; Agreement on Implementation of Article VI (ADA)",
        "WTO AB, US - Anti-Dumping Measures on Certain Hot-Rolled Steel "
        "Products from Japan, WT/DS184/AB/R (2001)",
        "WTO AB, EC - Anti-Dumping Duties on Imports of Cotton-Type Bed "
        "Linen from India, WT/DS141/AB/R (2001)",
    ],
    content=(
        "Dumping occurs when a product is introduced into the commerce of another "
        "country at less than its normal value (export price below home market price "
        "or cost of production). The Anti-Dumping Agreement (ADA) permits imposition "
        "of anti-dumping duties not exceeding the margin of dumping, provided the "
        "investigating authority determines dumped imports cause material injury to "
        "the domestic industry producing the like product. In US - Hot-Rolled Steel, "
        "the AB emphasized that investigating authorities must ensure a fair comparison "
        "between normal value and export price, including proper adjustments for "
        "differences affecting price comparability. The duty of good faith and due "
        "process requires transparent proceedings with adequate opportunity for all "
        "interested parties to defend their interests. The 'zeroing' methodology "
        "(setting negative dumping margins to zero) was repeatedly found WTO-inconsistent. "
        "Sunset reviews are required every five years to determine whether expiry of "
        "the duty would likely lead to continuation or recurrence of dumping and injury."
    ),
    related=["wto_subsidies_scm", "wto_dispute_settlement",
             "gatt_general_exceptions"],
)

# ===== 15. GATT GENERAL EXCEPTIONS =====
_add(
    topic="gatt_general_exceptions",
    category="international_trade_law",
    weight=0.93,
    citations=[
        "GATT Art. XX",
        "WTO AB, US - Import Prohibition of Certain Shrimp and Shrimp "
        "Products, WT/DS58/AB/R (1998)",
        "WTO AB, Brazil - Measures Affecting Imports of Retreaded Tyres, "
        "WT/DS332/AB/R (2007)",
        "WTO AB, EC - Measures Affecting Asbestos and Products Containing "
        "Asbestos, WT/DS135/AB/R (2001)",
    ],
    content=(
        "GATT Article XX provides general exceptions permitting otherwise WTO-"
        "inconsistent measures if necessary to protect public morals (a), human, "
        "animal, or plant life or health (b), related to conservation of exhaustible "
        "natural resources (g), or other specified grounds. The two-tier analysis "
        "requires the measure to be provisionally justified under a subparagraph and "
        "then to satisfy the chapeau, which prohibits arbitrary or unjustifiable "
        "discrimination between countries where the same conditions prevail, or "
        "disguised restrictions on trade. In US - Shrimp, the AB held that sea "
        "turtles are exhaustible natural resources under Art. XX(g) but the US "
        "measure failed the chapeau because it applied rigidly without accounting for "
        "different conditions in exporting countries and without good faith negotiation "
        "efforts. On compliance, the US was found to have cured the deficiency by "
        "pursuing multilateral negotiations. In Brazil - Retreaded Tyres, the AB "
        "accepted that an import ban on retreaded tyres was necessary under Art. XX(b) "
        "for protection of human health and the environment."
    ),
    related=["wto_mfn_principle", "wto_national_treatment",
             "wto_dispute_settlement"],
)

# ===== 16. TRIPS =====
_add(
    topic="trips_ip_protection",
    category="international_trade_law",
    weight=0.91,
    citations=[
        "Agreement on Trade-Related Aspects of Intellectual Property Rights",
        "WTO Panel, Canada - Patent Protection of Pharmaceutical Products, "
        "WT/DS114/R (2000)",
        "WTO AB, US - Section 211 Omnibus Appropriations Act of 1998, "
        "WT/DS176/AB/R (2002)",
        "Doha Declaration on TRIPS and Public Health (2001)",
    ],
    content=(
        "TRIPS establishes minimum standards for IP protection across patents (Arts. "
        "27-34), copyright (Arts. 9-14), trademarks (Arts. 15-21), geographical "
        "indications (Arts. 22-24), industrial designs (Arts. 25-26), and trade "
        "secrets (Art. 39). Patent protection must be available for inventions in all "
        "fields of technology, with a minimum term of 20 years from filing. Compulsory "
        "licensing is permitted under Art. 31 subject to conditions including prior "
        "unsuccessful efforts to obtain voluntary licenses, adequate remuneration, and "
        "predominantly domestic supply. The Doha Declaration affirmed Members' right to "
        "grant compulsory licenses and the freedom to determine grounds. In Canada - "
        "Pharmaceutical Patents, the panel found that stockpiling provisions for generic "
        "drugs before patent expiry violated Art. 28 but regulatory review exceptions "
        "were justified under Art. 30's limited exceptions. Enforcement provisions "
        "(Part III) require civil judicial procedures, provisional measures, border "
        "measures, and criminal procedures for willful trademark counterfeiting and "
        "copyright piracy on a commercial scale."
    ),
    related=["wto_dispute_settlement", "wto_mfn_principle",
             "cisg_formation_contracts"],
)

# ===== 17. GENEVA CONVENTIONS - COMMON ARTICLE 3 =====
_add(
    topic="geneva_conventions_common_art3",
    category="international_humanitarian_law",
    weight=0.97,
    citations=[
        "Geneva Conventions of 1949, Common Article 3",
        "ICJ, Military and Paramilitary Activities (Nicaragua v. US), "
        "[1986] ICJ Rep 14, para 218",
        "ICTY, Prosecutor v. Tadic, Case No. IT-94-1-A, Appeals Chamber "
        "Judgment (1999)",
        "ICRC Commentary on Common Article 3 (2016 updated)",
    ],
    content=(
        "Common Article 3 applies in armed conflicts not of an international character "
        "occurring in the territory of a party to the Conventions. It establishes "
        "minimum standards of humane treatment for persons taking no active part in "
        "hostilities, including wounded, sick, and those placed hors de combat. "
        "Specifically prohibited are violence to life and person (murder, mutilation, "
        "cruel treatment, torture), taking of hostages, outrages upon personal dignity, "
        "and sentencing or execution without due process. In Nicaragua, the ICJ held "
        "that Common Article 3 reflects customary international law binding on all "
        "parties regardless of treaty status. The ICTY Appeals Chamber in Tadic "
        "established that the distinction between international and non-international "
        "armed conflicts has become less important for purposes of customary "
        "international humanitarian law, as many rules originally developed for "
        "international conflicts now apply equally to internal conflicts. Common "
        "Article 3 is often characterized as a 'convention in miniature' providing a "
        "humanitarian floor below which no party may descend."
    ),
    related=["geneva_conventions_pow", "geneva_conventions_civilian_protection",
             "icc_war_crimes", "hague_laws_of_war"],
)

# ===== 18. GENEVA CONVENTIONS - POW =====
_add(
    topic="geneva_conventions_pow",
    category="international_humanitarian_law",
    weight=0.93,
    citations=[
        "Geneva Convention III Relative to the Treatment of Prisoners of War (1949)",
        "Additional Protocol I, Art. 44",
        "ICRC, Commentary on Geneva Convention III (2020 updated)",
        "US Supreme Court, Hamdan v. Rumsfeld, 548 US 557 (2006)",
    ],
    content=(
        "Geneva Convention III governs the treatment of prisoners of war in "
        "international armed conflicts. POW status attaches to members of armed forces, "
        "militias meeting four conditions (command structure, distinctive sign, open "
        "arms bearing, compliance with laws of war), and certain civilians accompanying "
        "armed forces. POWs must be treated humanely, provided adequate food, shelter, "
        "clothing, and medical care, and may not be subjected to torture or coercion to "
        "obtain information. They need only provide name, rank, date of birth, and "
        "service number. Disciplinary and judicial proceedings must respect due process, "
        "and the detaining power must allow ICRC visits. Additional Protocol I relaxed "
        "combatant criteria for guerrilla fighters, requiring only that arms be carried "
        "openly during military engagement and deployment. In Hamdan v. Rumsfeld, the "
        "US Supreme Court held that military commissions established for Guantanamo "
        "detainees violated Common Article 3 by failing to provide basic procedural "
        "protections required by the laws of war."
    ),
    related=["geneva_conventions_common_art3", "geneva_conventions_civilian_protection",
             "hague_laws_of_war"],
)

# ===== 19. GENEVA CONVENTIONS - CIVILIAN PROTECTION =====
_add(
    topic="geneva_conventions_civilian_protection",
    category="international_humanitarian_law",
    weight=0.94,
    citations=[
        "Geneva Convention IV Relative to the Protection of Civilian Persons "
        "in Time of War (1949)",
        "Additional Protocol I, Arts. 48, 51-58",
        "ICJ, Wall Advisory Opinion, [2004] ICJ Rep 136",
        "ICTY, Prosecutor v. Galic, Case No. IT-98-29-A (2006)",
    ],
    content=(
        "Geneva Convention IV and Additional Protocol I establish the principle of "
        "distinction, requiring parties to an armed conflict to distinguish at all "
        "times between the civilian population and combatants, and between civilian "
        "objects and military objectives (AP I Art. 48). Attacks must be directed "
        "solely against military objectives. Indiscriminate attacks are prohibited, "
        "including those not directed at a specific military objective, employing "
        "methods or means that cannot be directed at a specific objective, or whose "
        "effects cannot be limited as required by the Protocol (AP I Art. 51(4)). The "
        "principle of proportionality prohibits attacks expected to cause incidental "
        "civilian loss excessive in relation to the concrete and direct military "
        "advantage anticipated (AP I Art. 51(5)(b)). Precautionary measures are "
        "required to minimize civilian casualties (AP I Art. 57). In Galic, the ICTY "
        "convicted the defendant for a campaign of sniping and shelling directed "
        "against civilians in Sarajevo, establishing that deliberate targeting of "
        "civilians in armed conflict constitutes both a war crime and a crime against "
        "humanity."
    ),
    related=["geneva_conventions_common_art3", "geneva_conventions_pow",
             "icc_war_crimes", "icc_crimes_against_humanity"],
)

# ===== 20. GRAVE BREACHES =====
_add(
    topic="geneva_conventions_grave_breaches",
    category="international_humanitarian_law",
    weight=0.92,
    citations=[
        "GC I Art. 50; GC II Art. 51; GC III Art. 130; GC IV Art. 147",
        "Additional Protocol I Art. 85",
        "ICTY, Prosecutor v. Delalic et al. (Celebici), Case No. IT-96-21-A (2001)",
    ],
    content=(
        "Each Geneva Convention enumerates specific grave breaches that parties must "
        "suppress and prosecute. These include willful killing, torture or inhuman "
        "treatment (including biological experiments), willfully causing great suffering "
        "or serious injury to body or health, extensive destruction and appropriation "
        "of property not justified by military necessity and carried out unlawfully "
        "and wantonly, compelling a POW or protected person to serve in hostile forces, "
        "willfully depriving a POW or protected person of the rights of fair trial, "
        "and unlawful deportation, transfer, or confinement. Additional Protocol I "
        "extends grave breaches to include making the civilian population or individual "
        "civilians the object of attack, launching indiscriminate attacks affecting "
        "civilians, making non-defended localities or demilitarized zones the object of "
        "attack, and perfidious use of distinctive emblems. States have universal "
        "jurisdiction over grave breaches and an obligation to search for and prosecute "
        "or extradite (aut dedere aut judicare) suspected perpetrators regardless of "
        "nationality or location of the offense."
    ),
    related=["geneva_conventions_common_art3", "icc_war_crimes",
             "icc_rome_statute_overview"],
)

# ===== 21. HAGUE CONVENTIONS - LAWS OF WAR =====
_add(
    topic="hague_laws_of_war",
    category="international_humanitarian_law",
    weight=0.88,
    citations=[
        "Hague Convention IV Respecting the Laws and Customs of War on Land (1907)",
        "Hague Regulations Annexed to Convention IV, Arts. 22-56",
        "Hague Convention for the Protection of Cultural Property (1954)",
        "ICJ, Legality of Nuclear Weapons, [1996] ICJ Rep 226, para 75",
    ],
    content=(
        "The Hague Conventions regulate the methods and means of warfare. The Hague "
        "Regulations annexed to Convention IV (1907) codified the laws and customs of "
        "war on land, including the prohibition on employing poison or poisoned weapons "
        "(Art. 23(a)), killing or wounding treacherously (Art. 23(b)), and declaring "
        "that no quarter will be given (Art. 23(d)). Article 25 prohibits bombardment "
        "of undefended towns, villages, or buildings. The Martens Clause provides that "
        "in cases not covered by specific treaty provisions, civilians and combatants "
        "remain under the protection of the principles of the laws of nations derived "
        "from established custom, principles of humanity, and dictates of public "
        "conscience. The 1954 Hague Convention for the Protection of Cultural Property "
        "prohibits targeting cultural property in armed conflict and requires parties "
        "to respect and safeguard cultural heritage. The ICJ in the Nuclear Weapons "
        "advisory opinion confirmed that the Hague rules reflect customary "
        "international law, including the fundamental principle that the right of "
        "belligerents to choose methods or means of warfare is not unlimited."
    ),
    related=["geneva_conventions_common_art3", "geneva_conventions_civilian_protection",
             "icc_war_crimes"],
)

# ===== 22. ICCPR =====
_add(
    topic="iccpr_civil_political_rights",
    category="international_human_rights",
    weight=0.93,
    citations=[
        "International Covenant on Civil and Political Rights, 999 UNTS 171",
        "Human Rights Committee, General Comment No. 31 (2004)",
        "Human Rights Committee, General Comment No. 36 (2018) on Art. 6",
        "HRC, Toonen v. Australia, Comm. No. 488/1992 (1994)",
    ],
    content=(
        "The ICCPR protects civil and political rights including the right to life "
        "(Art. 6), freedom from torture (Art. 7), freedom from slavery (Art. 8), "
        "liberty and security of person (Art. 9), humane treatment in detention "
        "(Art. 10), freedom of movement (Art. 12), fair trial (Art. 14), freedom of "
        "thought, conscience, and religion (Art. 18), freedom of expression (Art. 19), "
        "and freedom of assembly (Art. 21) and association (Art. 22). Non-derogable "
        "rights (Art. 4(2)) include the right to life, freedom from torture, freedom "
        "from slavery, prohibition on imprisonment for inability to fulfill a contract, "
        "the principle of legality in criminal law, recognition as a person before the "
        "law, and freedom of thought, conscience, and religion. General Comment 31 "
        "established that the Covenant applies to all individuals within a state's "
        "territory and subject to its jurisdiction, including occupied territories. "
        "The Optional Protocol allows individuals to submit communications to the "
        "Human Rights Committee alleging violations. In Toonen, the HRC found that "
        "Tasmania's criminalization of homosexual conduct violated the right to privacy "
        "under Article 17."
    ),
    related=["icescr_economic_social_rights", "echr_human_rights",
             "vclt_jus_cogens"],
)

# ===== 23. ICESCR =====
_add(
    topic="icescr_economic_social_rights",
    category="international_human_rights",
    weight=0.88,
    citations=[
        "International Covenant on Economic, Social and Cultural Rights, "
        "993 UNTS 3",
        "CESCR, General Comment No. 3 (1990) on Art. 2(1)",
        "CESCR, General Comment No. 14 (2000) on Art. 12 (right to health)",
        "CESCR, General Comment No. 15 (2002) on Art. 11 (right to water)",
    ],
    content=(
        "The ICESCR recognizes economic, social, and cultural rights including the "
        "right to work (Arts. 6-7), trade union rights (Art. 8), social security "
        "(Art. 9), family protection (Art. 10), adequate standard of living including "
        "food, clothing, and housing (Art. 11), health (Art. 12), education (Arts. "
        "13-14), and participation in cultural life (Art. 15). States undertake to "
        "achieve progressive realization of these rights to the maximum of available "
        "resources (Art. 2(1)). General Comment 3 identified minimum core obligations "
        "that states must ensure immediately regardless of resources, including freedom "
        "from hunger, essential primary health care, basic shelter, and basic education. "
        "The principle of non-retrogression means that any deliberately retrogressive "
        "measures must be fully justified by reference to the totality of rights and "
        "the full use of maximum available resources. General Comment 14 elaborated the "
        "right to health as encompassing availability, accessibility, acceptability, "
        "and quality of healthcare. The Optional Protocol (2008) established an "
        "individual complaints mechanism."
    ),
    related=["iccpr_civil_political_rights", "echr_human_rights",
             "paris_agreement_climate"],
)

# ===== 24. ECHR =====
_add(
    topic="echr_human_rights",
    category="international_human_rights",
    weight=0.92,
    citations=[
        "European Convention on Human Rights (1950)",
        "ECtHR, Handyside v. United Kingdom, App. No. 5493/72 (1976)",
        "ECtHR, Soering v. United Kingdom, App. No. 14038/88 (1989)",
        "ECtHR, Al-Skeini v. United Kingdom, App. No. 55721/07 (2011)",
    ],
    content=(
        "The ECHR establishes the European Court of Human Rights with compulsory "
        "jurisdiction over 46 Council of Europe member states. Key doctrines include "
        "the margin of appreciation, which grants states latitude in implementing "
        "Convention rights based on national circumstances and the absence of European "
        "consensus (Handyside established that freedom of expression extends to ideas "
        "that offend, shock, or disturb). The proportionality principle requires "
        "interferences with rights to be prescribed by law, pursue a legitimate aim, "
        "and be necessary in a democratic society. Exhaustion of domestic remedies is "
        "required before filing applications (Art. 35). In Soering, the Court held that "
        "extradition to a country where the applicant faced a real risk of treatment "
        "contrary to Article 3 (prohibition of torture) would violate the Convention, "
        "establishing the non-refoulement dimension of Article 3. In Al-Skeini, the "
        "Court extended the Convention's jurisdictional reach to state agents exercising "
        "authority and control outside the territory of the contracting state, applying "
        "it to UK forces in occupied Iraq."
    ),
    related=["iccpr_civil_political_rights", "icescr_economic_social_rights",
             "vclt_jus_cogens"],
)

# ===== 25. FSIA =====
_add(
    topic="fsia_sovereign_immunity",
    category="foreign_sovereign_immunity",
    weight=0.93,
    citations=[
        "28 USC 1602-1611 (Foreign Sovereign Immunities Act)",
        "US Supreme Court, Saudi Arabia v. Nelson, 507 US 349 (1993)",
        "US Supreme Court, Republic of Argentina v. Weltover, 504 US 607 (1992)",
        "US Supreme Court, Samantar v. Yousuf, 560 US 305 (2010)",
    ],
    content=(
        "The FSIA provides the sole basis for jurisdiction over foreign states in US "
        "courts and codifies the restrictive theory of sovereign immunity. Foreign "
        "states are presumptively immune from suit (Sec. 1604) unless an exception "
        "applies. The commercial activity exception (Sec. 1605(a)(2)) is the most "
        "frequently litigated: a foreign state is not immune in actions based upon a "
        "commercial activity carried on in the US, an act performed in the US in "
        "connection with commercial activity elsewhere, or an act outside the US in "
        "connection with commercial activity elsewhere causing a direct effect in the "
        "US. In Weltover, the Court held Argentina's unilateral rescheduling of bonds "
        "payable in New York was a commercial activity with a direct effect in the US. "
        "In Nelson, the Court found that Saudi Arabia's alleged wrongful detention and "
        "torture of an employee was a sovereign, not commercial, act. The terrorism "
        "exception (Sec. 1605A, added 2008) permits suits against designated state "
        "sponsors of terrorism for personal injury or death caused by torture, "
        "extrajudicial killing, aircraft sabotage, or hostage-taking. Samantar held "
        "that the FSIA does not apply to individual foreign officials, whose immunity "
        "is governed by common law."
    ),
    related=["fsia_commercial_activity", "fsia_terrorism_exception",
             "icj_jurisdiction"],
)

# ===== 26. FSIA - COMMERCIAL ACTIVITY =====
_add(
    topic="fsia_commercial_activity",
    category="foreign_sovereign_immunity",
    weight=0.91,
    citations=[
        "28 USC 1605(a)(2)",
        "US Supreme Court, Republic of Argentina v. Weltover, 504 US 607 (1992)",
        "US Supreme Court, OBB Personenverkehr AG v. Sachs, 577 US 27 (2015)",
        "US Ct. Appeals, Af-Cap v. Republic of Congo, 383 F.3d 361 (5th Cir. 2004)",
    ],
    content=(
        "The commercial activity exception removes immunity when a foreign state "
        "engages in conduct that a private party could similarly undertake. The FSIA "
        "defines commercial activity by reference to the nature of the conduct rather "
        "than its purpose (Sec. 1603(d)). Three clauses of Sec. 1605(a)(2) provide "
        "separate jurisdictional bases. The first clause requires the commercial "
        "activity to be carried on in the US by the foreign state. The second clause "
        "covers acts performed in the US in connection with commercial activity "
        "elsewhere. The third clause covers acts outside the US in connection with "
        "commercial activity that cause a direct effect in the US. In Weltover, the "
        "Court defined 'direct effect' as one that follows as an immediate consequence "
        "of the defendant's activity, without requiring the effect to be substantial "
        "or foreseeable. In OBB Personenverkehr, the Court applied a 'gravamen' test, "
        "looking at the core of the suit rather than peripheral elements. The issuance "
        "of sovereign debt, sale of goods, commercial contracts, and banking activities "
        "are consistently treated as commercial acts."
    ),
    related=["fsia_sovereign_immunity", "fsia_terrorism_exception",
             "ny_convention_arbitral_awards"],
)

# ===== 27. FSIA - TERRORISM EXCEPTION =====
_add(
    topic="fsia_terrorism_exception",
    category="foreign_sovereign_immunity",
    weight=0.89,
    citations=[
        "28 USC 1605A",
        "US Supreme Court, Opati v. Republic of Sudan, 590 US ___ (2020)",
        "US Supreme Court, Bank Markazi v. Peterson, 578 US 212 (2016)",
        "Justice Against Sponsors of Terrorism Act (JASTA), Pub. L. 114-222 (2016)",
    ],
    content=(
        "Section 1605A provides a cause of action against foreign states designated "
        "as state sponsors of terrorism for personal injury or death caused by acts "
        "of torture, extrajudicial killing, aircraft sabotage, or hostage-taking, or "
        "the provision of material support or resources for such acts. The plaintiff "
        "or victim must be a US national, member of the Armed Forces, or an employee "
        "of the US Government. The designated state must have been given a reasonable "
        "opportunity to arbitrate the claim. In Opati, the Supreme Court held that "
        "punitive damages under Sec. 1605A apply retroactively to conduct predating "
        "the statute. Bank Markazi upheld Congressional legislation directing that "
        "specific Iranian assets be available to satisfy terrorism-related judgments. "
        "JASTA (2016) amended the FSIA to permit suits against foreign states for "
        "injuries occurring in the US from acts of international terrorism, even absent "
        "a state sponsor of terrorism designation, if the foreign state or its agent "
        "committed a tortious act in the US. This was motivated by claims arising from "
        "the September 11 attacks against Saudi Arabia."
    ),
    related=["fsia_sovereign_immunity", "fsia_commercial_activity",
             "ofac_sanctions_overview"],
)

# ===== 28. UNCITRAL MODEL LAW =====
_add(
    topic="uncitral_model_law_arbitration",
    category="international_arbitration",
    weight=0.91,
    citations=[
        "UNCITRAL Model Law on International Commercial Arbitration (1985, "
        "as amended 2006)",
        "UNCITRAL Arbitration Rules (2021)",
        "US Supreme Court, Scherk v. Alberto-Culver Co., 417 US 506 (1974)",
    ],
    content=(
        "The UNCITRAL Model Law provides a uniform framework for international "
        "commercial arbitration adopted by over 80 states. Key provisions include "
        "the separability doctrine (Art. 16) - an arbitration clause is treated as "
        "independent from the underlying contract, so that the invalidity of the "
        "contract does not ipso jure invalidate the arbitration clause. Kompetenz-"
        "Kompetenz (Art. 16) empowers the tribunal to rule on its own jurisdiction. "
        "Courts may only set aside awards on limited grounds (Art. 34): invalidity of "
        "arbitration agreement, lack of proper notice, excess of tribunal's authority, "
        "improper composition of tribunal, non-arbitrability, or conflict with public "
        "policy. The 2006 amendments enhanced the form requirement for arbitration "
        "agreements (Art. 7), recognizing electronic communications, and strengthened "
        "interim measures (Art. 17). The UNCITRAL Arbitration Rules (2021) govern "
        "ad hoc arbitrations, with the PCA as default appointing authority. The "
        "principle of party autonomy is paramount: parties are free to agree on "
        "procedural rules, seat of arbitration, language, and applicable substantive "
        "law."
    ),
    related=["icc_rules_arbitration", "icsid_investment_arbitration",
             "ny_convention_arbitral_awards"],
)

# ===== 29. ICC RULES OF ARBITRATION =====
_add(
    topic="icc_rules_arbitration",
    category="international_arbitration",
    weight=0.90,
    citations=[
        "ICC Arbitration Rules (2021)",
        "ICC, Case No. 5989 (1989) (hardship and changed circumstances)",
        "ICC, Case No. 4131 (Dow Chemical) (1982) (group of companies doctrine)",
    ],
    content=(
        "The ICC International Court of Arbitration administers arbitrations under the "
        "ICC Rules (2021 edition). The ICC Court does not itself decide disputes but "
        "supervises the process, including scrutiny of draft awards (Art. 34). The "
        "arbitral tribunal has the power to order interim and conservatory measures "
        "(Art. 28). Emergency arbitrator provisions (Art. 29 and Appendix V) allow "
        "urgent relief before the tribunal is constituted. The ICC Rules require a "
        "Terms of Reference document (Art. 23) setting out the issues, claims, and "
        "procedural calendar. The expedited procedure (Art. 30 and Appendix VI) "
        "applies automatically to disputes under USD 3 million, with a sole arbitrator "
        "and abbreviated timelines. The group of companies doctrine (Dow Chemical) "
        "permits extension of an arbitration clause to non-signatory affiliates that "
        "participated in the negotiation, performance, or termination of the contract. "
        "Costs are determined by the ICC Court based on an ad valorem scale. The 2021 "
        "rules added provisions on joinder of additional parties (Art. 7), consolidation "
        "(Art. 10), and disclosure of third-party funding."
    ),
    related=["uncitral_model_law_arbitration", "icsid_investment_arbitration",
             "ny_convention_arbitral_awards"],
)

# ===== 30. ICSID CONVENTION =====
_add(
    topic="icsid_investment_arbitration",
    category="international_arbitration",
    weight=0.93,
    citations=[
        "ICSID Convention, 575 UNTS 159",
        "ICSID, Philip Morris Asia Ltd. v. The Commonwealth of Australia, "
        "PCA Case No. 2012-12 (2015)",
        "ICSID, Salini Costruttori v. Kingdom of Morocco, Case No. ARB/00/4 (2001)",
        "ICSID, CMS Gas Transmission v. Argentine Republic, Case No. ARB/01/8 (2005)",
    ],
    content=(
        "The ICSID Convention establishes a self-contained system for investor-state "
        "dispute settlement. Jurisdiction requires: (1) a legal dispute arising "
        "directly out of an investment, (2) between a contracting state and a national "
        "of another contracting state, (3) that both parties have consented in writing "
        "to submit to ICSID. The Salini test identified four elements of an investment: "
        "contribution, duration, risk, and contribution to the host state's economic "
        "development, though the fourth element is contested. Awards are binding and "
        "not subject to appeal or review by domestic courts (Art. 53). Annulment is "
        "available only on limited grounds (Art. 52): improper constitution, excess of "
        "powers, corruption, serious departure from a fundamental rule of procedure, "
        "or failure to state reasons. In Philip Morris v. Australia, the tribunal "
        "found it lacked jurisdiction because Philip Morris restructured its investment "
        "through Hong Kong after the dispute was foreseeable, constituting an abuse of "
        "process. CMS v. Argentina addressed the emergency/necessity defense under "
        "customary international law, finding it unavailable where Argentina's own "
        "policies contributed to the economic crisis."
    ),
    related=["bilateral_investment_treaties", "uncitral_model_law_arbitration",
             "ny_convention_arbitral_awards"],
)

# ===== 31. CISG =====
_add(
    topic="cisg_formation_contracts",
    category="international_commercial_law",
    weight=0.89,
    citations=[
        "United Nations Convention on Contracts for the International Sale "
        "of Goods, 1489 UNTS 3",
        "CISG Advisory Council Opinion No. 1 (Electronic Communications)",
        "Delchi Carrier SpA v. Rotorex Corp., 71 F.3d 1024 (2d Cir. 1995)",
        "MCC-Marble Ceramic Center v. Ceramica Nuova d'Agostino, "
        "144 F.3d 1384 (11th Cir. 1998)",
    ],
    content=(
        "The CISG governs international sale of goods contracts between parties whose "
        "places of business are in different contracting states (Art. 1). It applies "
        "automatically unless excluded by the parties (Art. 6). Formation requires an "
        "offer sufficiently definite (indicating goods, quantity, and price) addressed "
        "to specific persons (Art. 14) and acceptance (Art. 18). The battle of forms "
        "under the CISG follows the mirror image rule: a reply with material additions, "
        "limitations, or modifications is a counteroffer (Art. 19). A party must give "
        "notice of lack of conformity within a reasonable time after discovery or ought "
        "to have discovered it (Art. 39), with an absolute cut-off of two years (Art. "
        "39(2)). Fundamental breach exists where failure substantially deprives the "
        "aggrieved party of what it was entitled to expect under the contract (Art. 25), "
        "entitling avoidance. In Delchi Carrier v. Rotorex, the Second Circuit applied "
        "the CISG's damages provisions, awarding lost profits and consequential damages "
        "for delivery of non-conforming compressors. MCC-Marble established that the "
        "parol evidence rule does not apply under the CISG."
    ),
    related=["cisg_remedies_breach", "ny_convention_arbitral_awards",
             "conflict_of_laws_characterization"],
)

# ===== 32. CISG - REMEDIES =====
_add(
    topic="cisg_remedies_breach",
    category="international_commercial_law",
    weight=0.87,
    citations=[
        "CISG Arts. 45-52, 61-65, 71-77",
        "CISG Advisory Council Opinion No. 6 (Calculation of Damages, 2006)",
        "Delchi Carrier SpA v. Rotorex Corp., 71 F.3d 1024 (2d Cir. 1995)",
    ],
    content=(
        "The CISG provides comprehensive remedies for buyer and seller. The buyer may "
        "require performance (Art. 46), reduce the price (Art. 50), claim damages "
        "(Arts. 74-77), or avoid the contract upon fundamental breach (Art. 49). The "
        "seller may require the buyer to pay, take delivery, or perform obligations "
        "(Art. 62), and may avoid the contract upon fundamental breach (Art. 64). "
        "Article 74 provides that damages equal the loss including lost profits "
        "suffered as a consequence of the breach, limited to what was foreseeable at "
        "the time of contract conclusion as a possible consequence. Where the contract "
        "is avoided and the buyer makes a cover purchase (Art. 75) or the seller "
        "resells (Art. 75), damages are the difference between the contract price and "
        "the cover/resale price. Article 76 provides a market price differential where "
        "no cover purchase or resale was made. The duty to mitigate (Art. 77) requires "
        "the aggrieved party to take reasonable measures to reduce loss; failure reduces "
        "damages by the amount that should have been mitigated. The Nachfrist mechanism "
        "(Arts. 47, 63) allows fixing an additional reasonable period for performance, "
        "after which avoidance is permitted even absent fundamental breach."
    ),
    related=["cisg_formation_contracts", "conflict_of_laws_characterization",
             "icc_rules_arbitration"],
)

# ===== 33. OFAC SANCTIONS =====
_add(
    topic="ofac_sanctions_overview",
    category="sanctions_export_controls",
    weight=0.94,
    citations=[
        "International Emergency Economic Powers Act, 50 USC 1701-1707",
        "31 CFR Parts 500-599 (OFAC Regulations)",
        "OFAC, Economic Sanctions Enforcement Guidelines, 74 FR 57593 (2009)",
        "Dep't of Treasury, OFAC Compliance Commitments Framework (2019)",
    ],
    content=(
        "OFAC administers economic sanctions programs under the authority of the "
        "International Emergency Economic Powers Act (IEEPA) and the Trading with "
        "the Enemy Act (TWEA, for Cuba). Sanctions prohibit US persons from engaging "
        "in transactions with designated persons on the Specially Designated Nationals "
        "(SDN) list and with sanctioned countries, regions, and sectors. The SDN list "
        "includes individuals, entities, vessels, and aircraft subject to asset "
        "blocking (freezing). Comprehensive programs (Iran, Cuba, North Korea, Syria, "
        "Crimea) impose broad prohibitions on virtually all transactions. Sectoral "
        "sanctions (e.g., Russia Directive 1-4, China military-industrial complex) "
        "prohibit specific types of transactions such as debt or equity financing "
        "beyond specified maturities. General licenses authorize certain categories "
        "of otherwise prohibited transactions. Specific licenses may be requested for "
        "individual transactions. Penalties include civil monetary penalties up to the "
        "greater of $356,579 per violation or twice the amount of the underlying "
        "transaction. Criminal penalties for willful violations include up to $1 million "
        "and 20 years imprisonment. The OFAC Compliance Commitments Framework (2019) "
        "sets out five pillars: management commitment, risk assessment, internal "
        "controls, testing and auditing, and training."
    ),
    related=["ear_export_controls", "itar_defense_articles",
             "un_charter_chapter_vii", "fsia_terrorism_exception"],
)

# ===== 34. EAR EXPORT CONTROLS =====
_add(
    topic="ear_export_controls",
    category="sanctions_export_controls",
    weight=0.91,
    citations=[
        "Export Control Reform Act of 2018, 50 USC 4801-4852",
        "15 CFR Parts 730-774 (Export Administration Regulations)",
        "BIS Entity List, 15 CFR Part 744, Supplement No. 4",
        "BIS, Interim Final Rule on Advanced Computing and Semiconductor "
        "Manufacturing Items (2022)",
    ],
    content=(
        "The EAR govern the export, reexport, and in-country transfer of dual-use "
        "items (commercial items with potential military or proliferation applications). "
        "Items subject to the EAR are classified under the Commerce Control List (CCL), "
        "with Export Control Classification Numbers (ECCNs) specifying the applicable "
        "controls and license requirements based on the item's technical parameters and "
        "the destination country. License exceptions (Part 740) permit certain exports "
        "without individual licenses. The Entity List (Supplement No. 4 to Part 744) "
        "identifies foreign persons and entities subject to specific licensing "
        "requirements, typically with a presumption of denial. The De Minimis rule "
        "(Sec. 734.4) subjects foreign-made items to the EAR if US-origin controlled "
        "content exceeds 25% (10% for designated countries). The Foreign Direct Product "
        "Rule (Sec. 734.9) extends EAR jurisdiction to foreign-produced items that are "
        "the direct product of US-origin technology or produced by a plant that is "
        "itself the direct product of US technology. Recent rules significantly "
        "restricted exports of advanced computing semiconductors, supercomputer and "
        "semiconductor manufacturing equipment to China and designated entities."
    ),
    related=["ofac_sanctions_overview", "itar_defense_articles",
             "fcpa_anti_corruption"],
)

# ===== 35. ITAR =====
_add(
    topic="itar_defense_articles",
    category="sanctions_export_controls",
    weight=0.90,
    citations=[
        "Arms Export Control Act, 22 USC 2751-2799",
        "22 CFR Parts 120-130 (ITAR)",
        "US Munitions List, 22 CFR Part 121",
        "United States v. Liew, No. 14-cr-00139 (N.D. Cal. 2016)",
    ],
    content=(
        "The ITAR regulate the export and temporary import of defense articles and "
        "services listed on the United States Munitions List (USML). The Directorate "
        "of Defense Trade Controls (DDTC) within the State Department administers the "
        "ITAR. Any person or entity engaged in manufacturing, exporting, or brokering "
        "defense articles or services must register with DDTC. Export of USML items "
        "requires a license or agreement (Technical Assistance Agreement for services, "
        "Manufacturing License Agreement for production). Deemed export rules apply: "
        "disclosure of USML technical data to a foreign person within the US constitutes "
        "an export to that person's country of nationality. The USML covers 21 "
        "categories from firearms to spacecraft, satellites, classified articles, and "
        "military electronics. Violations carry penalties up to $1 million per violation "
        "or 20 years imprisonment. The Export Control Reform initiative (2013) moved "
        "many items from the USML to the CCL (EAR jurisdiction), narrowing ITAR coverage "
        "to items providing a significant military or intelligence advantage. Registration "
        "is mandatory even if no export is planned if the person manufactures or exports "
        "defense articles."
    ),
    related=["ear_export_controls", "ofac_sanctions_overview",
             "fcpa_anti_corruption"],
)

# ===== 36. FCPA =====
_add(
    topic="fcpa_anti_corruption",
    category="anti_corruption",
    weight=0.93,
    citations=[
        "15 USC 78dd-1 to 78dd-3 (anti-bribery); 15 USC 78m(b) (accounting)",
        "DOJ/SEC, FCPA Resource Guide (2nd ed., 2020)",
        "US v. Hoskins, 902 F.3d 69 (2d Cir. 2018)",
        "SEC v. Siemens AG, No. 08-cv-02167 (D.D.C. 2008) ($800M settlement)",
    ],
    content=(
        "The FCPA contains anti-bribery provisions prohibiting corrupt payments to "
        "foreign officials to obtain or retain business, and accounting provisions "
        "requiring issuers to maintain accurate books and records and a system of "
        "internal accounting controls. Anti-bribery jurisdiction extends to issuers, "
        "domestic concerns, and their officers, directors, employees, and agents, as "
        "well as any person who acts within US territory in furtherance of a corrupt "
        "payment. A 'foreign official' includes any officer or employee of a foreign "
        "government, department, agency, or instrumentality, or any public international "
        "organization. The corrupt payment must be made to obtain or retain business or "
        "secure any improper advantage. Affirmative defenses include payments lawful "
        "under the foreign official's country's written laws and reasonable and bona "
        "fide expenditures directly related to product promotion or contract "
        "performance. Penalties for anti-bribery violations include criminal fines up "
        "to $250,000 per violation (individuals) or $2 million (entities), and "
        "imprisonment up to 5 years. The Siemens case resulted in a combined "
        "$1.6 billion resolution, the largest FCPA settlement at the time. DPAs and "
        "NPAs are the primary enforcement mechanism."
    ),
    related=["uk_bribery_act", "ofac_sanctions_overview",
             "ear_export_controls"],
)

# ===== 37. UK BRIBERY ACT =====
_add(
    topic="uk_bribery_act",
    category="anti_corruption",
    weight=0.89,
    citations=[
        "UK Bribery Act 2010, c.23",
        "Ministry of Justice, Guidance about Procedures for Relevant "
        "Commercial Organisations (2011)",
        "SFO v. Rolls-Royce Holdings plc, DPA (2017)",
        "R v. Skansen Interiors Ltd [2018] EWCA Crim 2772",
    ],
    content=(
        "The UK Bribery Act 2010 creates four offenses: bribing another person "
        "(s.1), being bribed (s.2), bribery of foreign public officials (s.6), and "
        "failure of a commercial organization to prevent bribery (s.7). The s.7 "
        "corporate offense is strict liability; the only defense is that the "
        "organization had adequate procedures in place to prevent bribery. The "
        "Ministry of Justice Guidance identifies six principles for adequate "
        "procedures: proportionality, top-level commitment, risk assessment, due "
        "diligence, communication/training, and monitoring/review. Jurisdiction is "
        "broad: any body incorporated or formed in the UK or carrying on business in "
        "the UK can be prosecuted regardless of where the bribery occurred. Unlike "
        "the FCPA, the Act makes no exception for facilitation payments. The "
        "hospitality defense requires that the expenditure be reasonable and "
        "proportionate. Penalties for individuals include unlimited fines and up to "
        "10 years imprisonment. In Rolls-Royce, the Serious Fraud Office secured "
        "a DPA for over 550 million GBP covering bribery across multiple countries "
        "over decades."
    ),
    related=["fcpa_anti_corruption", "ofac_sanctions_overview",
             "icsid_investment_arbitration"],
)

# ===== 38. UNCLOS =====
_add(
    topic="unclos_law_of_the_sea",
    category="law_of_the_sea",
    weight=0.93,
    citations=[
        "United Nations Convention on the Law of the Sea, 1833 UNTS 3",
        "ITLOS, M/V Saiga (No. 2) (Saint Vincent v. Guinea), "
        "Judgment, ITLOS Reports 1999",
        "PCA, South China Sea Arbitration (Philippines v. China), "
        "PCA Case No. 2013-19 (2016)",
        "ICJ, Maritime Delimitation in the Black Sea (Romania v. Ukraine), "
        "[2009] ICJ Rep 61",
    ],
    content=(
        "UNCLOS establishes a comprehensive regime for the oceans. The territorial "
        "sea extends to 12 nautical miles from baselines (Art. 3), within which the "
        "coastal state exercises sovereignty subject to the right of innocent passage "
        "(Arts. 17-26). The contiguous zone extends to 24 nm (Art. 33). The exclusive "
        "economic zone extends to 200 nm, granting the coastal state sovereign rights "
        "over natural resources and jurisdiction over marine scientific research, "
        "environmental protection, and artificial islands (Arts. 55-75). The "
        "continental shelf extends to at least 200 nm or to the outer edge of the "
        "continental margin (Art. 76). The high seas are open to all states (Art. 87) "
        "with freedom of navigation, overflight, fishing, scientific research, laying "
        "cables and pipelines, and constructing artificial islands. The International "
        "Seabed Authority governs mineral resource activities in the Area beyond "
        "national jurisdiction (Part XI). In the South China Sea Arbitration, the "
        "tribunal held that China's nine-dash line claims had no legal basis under "
        "UNCLOS and that China had violated Philippines' sovereign rights in its EEZ."
    ),
    related=["unclos_eez", "unclos_continental_shelf", "unclos_deep_seabed",
             "icj_jurisdiction"],
)

# ===== 39. UNCLOS - EEZ =====
_add(
    topic="unclos_eez",
    category="law_of_the_sea",
    weight=0.88,
    citations=[
        "UNCLOS Arts. 55-75",
        "ICJ, Fisheries Jurisdiction (UK v. Iceland), [1974] ICJ Rep 3",
        "PCA, South China Sea Arbitration, Award on Merits (2016), paras 716-757",
    ],
    content=(
        "The EEZ is an area beyond and adjacent to the territorial sea extending up "
        "to 200 nm from baselines (Art. 57). Within the EEZ, the coastal state has "
        "sovereign rights for exploring, exploiting, conserving, and managing natural "
        "resources, both living and non-living, of the waters superjacent to the "
        "seabed, the seabed and its subsoil, and with regard to other economic "
        "activities such as energy production from water, currents, and winds (Art. "
        "56(1)(a)). The coastal state also has jurisdiction over artificial islands, "
        "marine scientific research, and environmental protection (Art. 56(1)(b)). "
        "Other states enjoy freedoms of navigation, overflight, and laying of "
        "submarine cables and pipelines (Art. 58). The coastal state must determine "
        "the allowable catch of living resources and ensure proper conservation and "
        "management (Arts. 61-62). Where the coastal state cannot harvest the entire "
        "allowable catch, it shall give other states access to the surplus (Art. 62(2)). "
        "Disputes concerning sovereign rights in the EEZ may be submitted to compulsory "
        "procedures under Part XV, though certain exceptions apply to discretionary "
        "decisions regarding living resources (Art. 297(3))."
    ),
    related=["unclos_law_of_the_sea", "unclos_continental_shelf",
             "paris_agreement_climate"],
)

# ===== 40. UNCLOS - CONTINENTAL SHELF =====
_add(
    topic="unclos_continental_shelf",
    category="law_of_the_sea",
    weight=0.87,
    citations=[
        "UNCLOS Arts. 76-85",
        "Commission on the Limits of the Continental Shelf, "
        "Scientific and Technical Guidelines (1999)",
        "ICJ, Maritime Delimitation in the Black Sea "
        "(Romania v. Ukraine), [2009] ICJ Rep 61",
    ],
    content=(
        "The continental shelf comprises the seabed and subsoil of submarine areas "
        "extending beyond the territorial sea to the outer edge of the continental "
        "margin or to 200 nm from baselines where the margin does not extend that far "
        "(Art. 76(1)). The continental margin consists of the shelf, slope, and rise "
        "(Art. 76(3)). Where the margin extends beyond 200 nm, the outer limits are "
        "delineated using the Gardiner formula (sediment thickness) or the Hedberg "
        "formula (60 nm from the foot of the slope), subject to a maximum of 350 nm "
        "from baselines or 100 nm beyond the 2,500-meter isobath (Art. 76(5)). States "
        "claiming an extended shelf must submit information to the Commission on the "
        "Limits of the Continental Shelf (CLCS) (Art. 76(8)). The coastal state "
        "exercises sovereign rights over the shelf for exploring and exploiting mineral "
        "and other non-living resources, together with living organisms belonging to "
        "sedentary species (Art. 77). These rights are inherent and do not depend on "
        "occupation or proclamation. The ICJ in Romania v. Ukraine applied a three-stage "
        "delimitation methodology: provisional equidistance line, relevant circumstances "
        "adjustment, and disproportionality check."
    ),
    related=["unclos_law_of_the_sea", "unclos_eez", "unclos_deep_seabed"],
)

# ===== 41. DEEP SEABED =====
_add(
    topic="unclos_deep_seabed",
    category="law_of_the_sea",
    weight=0.84,
    citations=[
        "UNCLOS Part XI (The Area), Arts. 133-191",
        "1994 Agreement Relating to the Implementation of Part XI",
        "ITLOS, Responsibilities and Obligations of States with Respect "
        "to Activities in the Area, Advisory Opinion (2011)",
    ],
    content=(
        "The Area and its resources are the common heritage of mankind (Art. 136). "
        "No state may claim sovereignty or sovereign rights over any part of the Area "
        "or its resources (Art. 137). The International Seabed Authority (ISA) "
        "organizes and controls activities in the Area on behalf of mankind as a "
        "whole (Art. 157). Exploration and exploitation require a contract with the "
        "ISA, subject to the Mining Code regulations. The parallel system requires "
        "applicants for exploration contracts to identify two sites of equivalent "
        "commercial value, one of which is reserved for the Enterprise (the ISA's "
        "mining arm) or developing states. The 1994 Implementation Agreement modified "
        "Part XI to address developed state concerns, including market-based approaches, "
        "streamlined decision-making, and elimination of mandatory technology transfer. "
        "The ITLOS Advisory Opinion established that sponsoring states have a due "
        "diligence obligation to ensure compliance by sponsored contractors with their "
        "obligations, adopting a precautionary approach, best environmental practices, "
        "and conducting environmental impact assessments. Current regulations cover "
        "polymetallic nodules, polymetallic sulphides, and cobalt-rich ferromanganese "
        "crusts."
    ),
    related=["unclos_law_of_the_sea", "unclos_eez", "unclos_continental_shelf"],
)

# ===== 42. PARIS AGREEMENT =====
_add(
    topic="paris_agreement_climate",
    category="international_environmental_law",
    weight=0.91,
    citations=[
        "Paris Agreement (2015), UNTC XXVII.7.d",
        "UNFCCC Art. 2; Paris Agreement Arts. 2, 4, 6, 8",
        "IPCC, Sixth Assessment Report (2021-2023)",
    ],
    content=(
        "The Paris Agreement aims to hold global average temperature increase to well "
        "below 2 degrees C above pre-industrial levels and to pursue efforts to limit "
        "it to 1.5 degrees C (Art. 2(1)(a)). It establishes a bottom-up system of "
        "nationally determined contributions (NDCs) communicated every five years with "
        "a progression requirement (Art. 4(3)). The global stocktake every five years "
        "assesses collective progress (Art. 14). Article 6 establishes cooperative "
        "approaches, including internationally transferred mitigation outcomes (Art. "
        "6.2) and a new mechanism for emission reductions (Art. 6.4) replacing the "
        "Kyoto Clean Development Mechanism. The Warsaw International Mechanism for Loss "
        "and Damage (Art. 8) addresses impacts of climate change that cannot be adapted "
        "to. Developed countries must provide financial resources (Art. 9), with a "
        "collective goal of USD 100 billion per year (subsequently increased). "
        "Transparency framework (Art. 13) requires biennial reporting on emissions, "
        "removals, support provided/received. The Agreement entered into force on "
        "November 4, 2016. NDCs are not legally binding targets, but the procedural "
        "obligations (preparation, communication, maintenance, progression) are binding."
    ),
    related=["unclos_law_of_the_sea", "icescr_economic_social_rights",
             "wto_dispute_settlement"],
)

# ===== 43. NEW YORK CONVENTION =====
_add(
    topic="ny_convention_arbitral_awards",
    category="international_arbitration",
    weight=0.94,
    citations=[
        "Convention on the Recognition and Enforcement of Foreign Arbitral "
        "Awards (1958), 330 UNTS 3",
        "US Supreme Court, Scherk v. Alberto-Culver Co., 417 US 506 (1974)",
        "Parsons & Whittemore Overseas v. Societe Generale, "
        "508 F.2d 969 (2d Cir. 1974)",
    ],
    content=(
        "The New York Convention requires contracting states to recognize and enforce "
        "arbitral awards made in other states, subject to limited grounds for refusal "
        "(Art. V). Grounds for refusal at the request of a party include: invalidity "
        "of the arbitration agreement, lack of proper notice, the award exceeding the "
        "scope of the submission, improper composition of the tribunal or non-compliance "
        "with the arbitration agreement regarding procedure (Art. V(1)). Courts may "
        "refuse recognition ex officio if the subject matter is not capable of "
        "settlement by arbitration or if recognition would be contrary to the public "
        "policy of the enforcing state (Art. V(2)). The public policy defense is "
        "construed narrowly: in Parsons & Whittemore, the Second Circuit held that "
        "enforcement of a foreign award should be denied on public policy grounds only "
        "where enforcement would violate the forum state's most basic notions of "
        "morality and justice. The pro-enforcement bias permeates the Convention. The "
        "more-favorable-right provision (Art. VII(1)) permits a party to rely on "
        "domestic law if it provides more favorable conditions for recognition. Over "
        "172 contracting states make this the most widely adopted private international "
        "law instrument."
    ),
    related=["uncitral_model_law_arbitration", "icc_rules_arbitration",
             "icsid_investment_arbitration"],
)

# ===== 44. BILATERAL INVESTMENT TREATIES =====
_add(
    topic="bilateral_investment_treaties",
    category="international_investment_law",
    weight=0.92,
    citations=[
        "ICSID, Tecnicas Medioambientales Tecmed v. Mexico, "
        "Case No. ARB(AF)/00/2 (2003)",
        "ICSID, Metalclad Corp. v. Mexico, Case No. ARB(AF)/97/1 (2000)",
        "ICSID, CME Czech Republic v. Czech Republic, UNCITRAL (2003)",
        "UNCTAD, World Investment Report 2023",
    ],
    content=(
        "Bilateral investment treaties (BITs) protect foreign investors from host "
        "state interference through substantive standards including fair and equitable "
        "treatment (FET), full protection and security, national treatment, MFN, "
        "protection against expropriation, and free transfer of funds. The umbrella "
        "clause elevates contractual obligations of the host state to treaty "
        "obligations. FET encompasses protection of legitimate expectations, due "
        "process, non-arbitrariness, non-discrimination, proportionality, and "
        "transparency. In Tecmed, the tribunal articulated that FET requires the host "
        "state to act consistently, free from ambiguity, and transparently so that the "
        "foreign investor can plan and act accordingly. Metalclad found indirect "
        "expropriation where regulatory action deprived the investor of the economic "
        "use and benefit of its investment, even without formal taking. Modern BITs "
        "increasingly include clarifications limiting FET to customary international "
        "law minimum standard, defining indirect expropriation, and preserving "
        "regulatory space for health, safety, and environmental measures. Investor-"
        "state dispute settlement (ISDS) clauses provide direct access to international "
        "arbitration, typically under ICSID or UNCITRAL rules."
    ),
    related=["icsid_investment_arbitration", "fsia_sovereign_immunity",
             "uncitral_model_law_arbitration"],
)

# ===== 45. ICC ROME STATUTE =====
_add(
    topic="icc_rome_statute_overview",
    category="international_criminal_law",
    weight=0.93,
    citations=[
        "Rome Statute of the International Criminal Court (1998)",
        "ICC, Prosecutor v. Lubanga, ICC-01/04-01/06 (2012)",
        "ICC, Prosecutor v. Al Bashir, ICC-02/05-01/09 (2009)",
        "ICC, Situation in Ukraine, ICC-01/22 (2022)",
    ],
    content=(
        "The Rome Statute establishes the International Criminal Court with "
        "jurisdiction over genocide (Art. 6), crimes against humanity (Art. 7), war "
        "crimes (Art. 8), and the crime of aggression (Art. 8bis, activated 2018). "
        "Jurisdiction is triggered by referral from a state party, the Security "
        "Council, or proprio motu investigation by the Prosecutor (Art. 13). The "
        "Court exercises jurisdiction where the crime occurred in the territory of a "
        "state party or was committed by a national of a state party, or when the "
        "Security Council refers a situation regardless of state party status. The "
        "principle of complementarity (Art. 17) means the Court acts only when states "
        "are unwilling or unable genuinely to investigate or prosecute. In Lubanga, "
        "the first ICC conviction, the Trial Chamber found the defendant guilty of "
        "conscripting and enlisting children under 15 and using them in hostilities. "
        "The Al Bashir arrest warrant (including genocide charges) against a sitting "
        "head of state generated significant controversy regarding immunity. The "
        "Ukraine situation demonstrates the Court's response to alleged crimes of "
        "aggression and war crimes in the context of the 2022 conflict."
    ),
    related=["icc_war_crimes", "icc_crimes_against_humanity",
             "genocide_convention", "geneva_conventions_grave_breaches"],
)

# ===== 46. GENOCIDE CONVENTION =====
_add(
    topic="genocide_convention",
    category="international_criminal_law",
    weight=0.96,
    citations=[
        "Convention on the Prevention and Punishment of the Crime of "
        "Genocide (1948)",
        "ICJ, Application of the Convention on Prevention and Punishment "
        "of the Crime of Genocide (Bosnia v. Serbia), [2007] ICJ Rep 43",
        "ICTR, Prosecutor v. Akayesu, Case No. ICTR-96-4-T (1998)",
        "ICJ, Application of the Convention on Prevention and Punishment "
        "of the Crime of Genocide (The Gambia v. Myanmar), [2020] ICJ Rep",
    ],
    content=(
        "Genocide means acts committed with intent to destroy, in whole or in part, a "
        "national, ethnical, racial, or religious group (Art. II). Enumerated acts "
        "include killing members of the group, causing serious bodily or mental harm, "
        "deliberately inflicting conditions of life calculated to bring about physical "
        "destruction, imposing measures intended to prevent births, and forcibly "
        "transferring children to another group. The specific intent (dolus specialis) "
        "to destroy the group as such distinguishes genocide from other crimes. In "
        "Akayesu, the first genocide conviction by an international tribunal, the "
        "ICTR held that rape and sexual violence can constitute genocide when committed "
        "with intent to destroy the group. The ICJ in Bosnia v. Serbia found that the "
        "Srebrenica massacre constituted genocide but that Serbia was not directly "
        "responsible; however, Serbia breached its obligation to prevent genocide. In "
        "Gambia v. Myanmar, the ICJ ordered provisional measures requiring Myanmar to "
        "take all measures within its power to prevent genocide against the Rohingya. "
        "The obligation to prevent genocide is erga omnes partes, meaning any state "
        "party has standing to invoke responsibility."
    ),
    related=["icc_rome_statute_overview", "icc_crimes_against_humanity",
             "vclt_jus_cogens", "icj_provisional_measures"],
)

# ===== 47. CONFLICT OF LAWS =====
_add(
    topic="conflict_of_laws_characterization",
    category="private_international_law",
    weight=0.88,
    citations=[
        "Restatement (Second) of Conflict of Laws (1971)",
        "Rome I Regulation (EC) No 593/2008",
        "Rome II Regulation (EC) No 864/2007",
        "Hague Conference on Private International Law, "
        "Principles on Choice of Law in International Commercial Contracts (2015)",
    ],
    content=(
        "Conflict of laws (private international law) addresses three core questions: "
        "jurisdiction, applicable law (choice of law), and recognition and enforcement "
        "of foreign judgments. Characterization (classification) determines which "
        "choice-of-law rule applies by classifying the legal issue into a category "
        "(contract, tort, property, status). Different legal systems may characterize "
        "the same facts differently (e.g., statute of limitations as substantive or "
        "procedural). Renvoi arises when a forum's choice-of-law rule points to "
        "foreign law, and the foreign choice-of-law rule points back to forum law "
        "(remission) or to a third country's law (transmission). Most modern codifications "
        "reject renvoi in contract (Rome I Art. 20) but may accept it in property or "
        "status matters. The public policy exception (ordre public) permits a court to "
        "refuse application of otherwise applicable foreign law if the result would be "
        "manifestly incompatible with the forum's fundamental values. The Hague "
        "Principles on Choice of Law affirm party autonomy as the paramount principle "
        "in international commercial contracts, including the ability to choose non-"
        "state rules such as the UNIDROIT Principles."
    ),
    related=["cisg_formation_contracts", "ny_convention_arbitral_awards",
             "hague_service_evidence"],
)

# ===== 48. STATE RESPONSIBILITY =====
_add(
    topic="state_responsibility_attribution",
    category="public_international_law",
    weight=0.93,
    citations=[
        "ILC, Articles on Responsibility of States for Internationally "
        "Wrongful Acts (2001)",
        "ICJ, Nicaragua v. US, [1986] ICJ Rep 14 (effective control test)",
        "ICTY, Prosecutor v. Tadic, Case No. IT-94-1-A (1999) "
        "(overall control test)",
        "ICJ, Genocide (Bosnia v. Serbia), [2007] ICJ Rep 43",
    ],
    content=(
        "The ILC Articles (2001) codify the law of state responsibility. An "
        "internationally wrongful act requires: (1) conduct attributable to the state "
        "under international law, and (2) breach of an international obligation (Art. "
        "2). Attribution extends to acts of state organs (Art. 4), persons exercising "
        "governmental authority (Art. 5), organs placed at disposal of a state (Art. "
        "6), conduct directed or controlled by a state (Art. 8), and conduct "
        "acknowledged and adopted by a state (Art. 11). In Nicaragua, the ICJ applied "
        "the 'effective control' test: the US was not responsible for specific acts of "
        "the contras because the US did not exercise effective control over their "
        "operations. The ICTY in Tadic adopted the lower 'overall control' test for "
        "determining whether armed forces are attributable to a state in armed conflict. "
        "In Bosnia v. Serbia, the ICJ reaffirmed the effective control test for state "
        "responsibility outside the context of armed conflict classification. "
        "Circumstances precluding wrongfulness include consent (Art. 20), self-defense "
        "(Art. 21), countermeasures (Art. 22), force majeure (Art. 23), distress "
        "(Art. 24), and necessity (Art. 25)."
    ),
    related=["un_charter_use_of_force", "un_charter_self_defense",
             "vclt_jus_cogens", "icj_jurisdiction"],
)

# ===== 49. CUSTOMARY INTERNATIONAL LAW =====
_add(
    topic="customary_international_law",
    category="public_international_law",
    weight=0.92,
    citations=[
        "ICJ Statute Art. 38(1)(b)",
        "ICJ, North Sea Continental Shelf Cases (Germany v. Denmark; "
        "Germany v. Netherlands), [1969] ICJ Rep 3",
        "ILC, Draft Conclusions on Identification of Customary "
        "International Law (2018)",
        "ICJ, Jurisdictional Immunities of the State "
        "(Germany v. Italy), [2012] ICJ Rep 99",
    ],
    content=(
        "Customary international law, as a source under ICJ Statute Art. 38(1)(b), "
        "requires two elements: a general practice of states (objective/material "
        "element) accompanied by a sense of legal obligation (opinio juris sive "
        "necessitatis) (subjective/psychological element). In the North Sea Continental "
        "Shelf Cases, the ICJ held that the equidistance principle had not achieved "
        "customary law status because state practice was insufficient and motivated "
        "by convenience rather than legal obligation. The ILC Draft Conclusions (2018) "
        "confirmed the two-element approach and elaborated that practice must be "
        "sufficiently general, meaning widespread and representative, including among "
        "specially affected states. Practice includes physical acts, legislation, "
        "diplomatic correspondence, and decisions of national courts. Opinio juris "
        "may be evidenced by public statements, government legal opinions, treaty "
        "provisions, resolutions of international organizations, and diplomatic "
        "correspondence. A persistent objector that consistently and openly objected "
        "to a rule during its formation is not bound by it. Specially affected states "
        "are those whose interests are particularly affected by the rule in question."
    ),
    related=["vclt_jus_cogens", "state_responsibility_attribution",
             "un_charter_use_of_force"],
)

# ===== 50. ICC WAR CRIMES =====
_add(
    topic="icc_war_crimes",
    category="international_criminal_law",
    weight=0.91,
    citations=[
        "Rome Statute Art. 8",
        "ICC, Prosecutor v. Ntaganda, ICC-01/04-02/06 (2019)",
        "ICTY, Prosecutor v. Blaskic, Case No. IT-95-14-A (2004)",
        "Elements of Crimes, ICC-ASP/1/3 (2002)",
    ],
    content=(
        "Rome Statute Article 8 enumerates war crimes in both international and "
        "non-international armed conflicts. In international armed conflicts, war "
        "crimes include grave breaches of the Geneva Conventions (Art. 8(2)(a)), "
        "serious violations of the laws and customs of war (Art. 8(2)(b)) including "
        "intentionally directing attacks against civilian populations, using prohibited "
        "weapons, pillaging, sexual violence, and conscripting children under 15. In "
        "non-international armed conflicts, war crimes include serious violations of "
        "Common Article 3 (Art. 8(2)(c)) and other serious violations of customs "
        "applicable in NIAC (Art. 8(2)(e)). The Court generally requires that war "
        "crimes be committed as part of a plan or policy or on a large scale (Art. "
        "8(1)). In Ntaganda, the ICC found the defendant guilty of 18 counts of war "
        "crimes and crimes against humanity including murder, rape, sexual slavery, "
        "persecution, pillaging, and conscription of child soldiers. The contextual "
        "element requires a nexus between the conduct and an armed conflict. Individual "
        "criminal responsibility extends to direct perpetration, ordering, soliciting, "
        "inducing, aiding/abetting, and contributing to group crimes (Art. 25), as "
        "well as command responsibility (Art. 28)."
    ),
    related=["icc_rome_statute_overview", "icc_crimes_against_humanity",
             "genocide_convention", "geneva_conventions_grave_breaches"],
)

# ===== 51. ICC CRIMES AGAINST HUMANITY =====
_add(
    topic="icc_crimes_against_humanity",
    category="international_criminal_law",
    weight=0.91,
    citations=[
        "Rome Statute Art. 7",
        "ICC, Prosecutor v. Katanga, ICC-01/04-01/07 (2014)",
        "ICTY, Prosecutor v. Kunarac et al., Case No. IT-96-23-A (2002)",
        "ILC, Draft Articles on Prevention and Punishment of Crimes "
        "Against Humanity (2019)",
    ],
    content=(
        "Crimes against humanity under Rome Statute Article 7 are acts committed as "
        "part of a widespread or systematic attack directed against any civilian "
        "population, with knowledge of the attack. Enumerated acts include murder, "
        "extermination, enslavement, deportation or forcible transfer, imprisonment, "
        "torture, sexual violence (rape, sexual slavery, enforced prostitution, forced "
        "pregnancy, enforced sterilization), persecution on political, racial, national, "
        "ethnic, cultural, religious, or gender grounds, enforced disappearance, "
        "apartheid, and other inhumane acts of similar character intentionally causing "
        "great suffering or serious injury. Unlike war crimes, crimes against humanity "
        "do not require a nexus to armed conflict and can be committed in peacetime. "
        "In Kunarac, the ICTY held that 'widespread' refers to a large-scale attack "
        "involving a multiplicity of victims, while 'systematic' refers to organized "
        "nature and improbability of random occurrence. The perpetrator need not share "
        "the purpose of the attack but must know the attack is occurring and that the "
        "acts form part of it. The ILC Draft Articles (2019) represent efforts to "
        "create a dedicated convention on crimes against humanity."
    ),
    related=["icc_rome_statute_overview", "icc_war_crimes",
             "genocide_convention", "vclt_jus_cogens"],
)

# ===== 52. HAGUE SERVICE AND EVIDENCE CONVENTIONS =====
_add(
    topic="hague_service_evidence",
    category="private_international_law",
    weight=0.86,
    citations=[
        "Hague Service Convention (1965)",
        "Hague Evidence Convention (1970)",
        "US Supreme Court, Volkswagenwerk AG v. Schlunk, 486 US 694 (1988)",
        "US Supreme Court, Societe Nationale Industrielle Aerospatiale "
        "v. US Dist. Court, 482 US 522 (1987)",
    ],
    content=(
        "The Hague Service Convention provides mechanisms for service of judicial "
        "documents abroad, primarily through Central Authorities designated by each "
        "contracting state. The Convention is mandatory where it applies but does not "
        "preclude alternative methods not prohibited by the receiving state. In "
        "Schlunk, the Supreme Court held that the Convention does not apply where "
        "service is effected on a domestic subsidiary as agent of the foreign parent, "
        "because the Convention applies only where there is occasion to transmit a "
        "document for service abroad. Service by mail under Article 10(a) is permitted "
        "unless the receiving state objects, though courts have split on whether 'send' "
        "encompasses 'serve.' The Hague Evidence Convention provides procedures for "
        "obtaining evidence abroad through Letters of Request to foreign judicial "
        "authorities (Chapter I) or through diplomatic officers and commissioners "
        "(Chapter II). In Aerospatiale, the Supreme Court held that the Evidence "
        "Convention does not provide exclusive or mandatory procedures for obtaining "
        "documents located abroad but is one option alongside domestic discovery rules, "
        "with courts conducting a comity analysis to determine the appropriate method."
    ),
    related=["conflict_of_laws_characterization", "fsia_sovereign_immunity",
             "cisg_formation_contracts"],
)

# ===== 53. DIPLOMATIC AND CONSULAR IMMUNITY =====
_add(
    topic="diplomatic_consular_immunity",
    category="public_international_law",
    weight=0.89,
    citations=[
        "Vienna Convention on Diplomatic Relations, 500 UNTS 95 (1961)",
        "Vienna Convention on Consular Relations, 596 UNTS 261 (1963)",
        "ICJ, United States Diplomatic and Consular Staff in Tehran "
        "(US v. Iran), [1980] ICJ Rep 3",
        "ICJ, Arrest Warrant of 11 April 2000 (DRC v. Belgium), "
        "[2002] ICJ Rep 3",
    ],
    content=(
        "The VCDR grants diplomatic agents immunity from criminal jurisdiction of the "
        "receiving state (Art. 31(1)) and immunity from civil and administrative "
        "jurisdiction except for real actions relating to private immovable property, "
        "succession matters, and professional or commercial activity outside official "
        "functions. The premises of the mission are inviolable (Art. 22) and the "
        "receiving state may not enter without consent. In the Tehran Hostages case, "
        "the ICJ held that Iran's failure to protect the US Embassy and its subsequent "
        "endorsement of the occupation constituted violations of the VCDR. Diplomatic "
        "immunity begins upon entry into the receiving state to take up post and ends "
        "when the diplomat leaves or after a reasonable period for departure following "
        "the end of functions. The VCCR provides functional immunity to consular "
        "officers for acts performed in the exercise of consular functions (Art. "
        "43(1)), which is narrower than diplomatic immunity. The sending state may "
        "waive immunity (Art. 32 VCDR), but waiver must be express. In the Arrest "
        "Warrant case, the ICJ held that incumbent foreign ministers enjoy full "
        "immunity from criminal jurisdiction abroad."
    ),
    related=["icj_jurisdiction", "state_responsibility_attribution",
             "fsia_sovereign_immunity"],
)

# ===== 54. INTERNATIONAL ORGANIZATIONS IMMUNITY =====
_add(
    topic="international_organizations_immunity",
    category="public_international_law",
    weight=0.85,
    citations=[
        "Convention on the Privileges and Immunities of the United Nations (1946)",
        "Convention on the Privileges and Immunities of the Specialized "
        "Agencies (1947)",
        "ICJ, Difference Relating to Immunity from Legal Process of a "
        "Special Rapporteur (Cumaraswamy), Advisory Opinion, [1999] ICJ Rep 62",
    ],
    content=(
        "International organizations enjoy immunity from jurisdiction under their "
        "constituent instruments, headquarters agreements, and general conventions on "
        "privileges and immunities. The 1946 UN Convention provides that the United "
        "Nations possesses juridical personality (Sec. 1), its premises are inviolable "
        "(Sec. 3), its property is immune from legal process (Sec. 2), and its "
        "officials enjoy functional immunity (Sec. 18). Representatives of member "
        "states enjoy immunity for acts performed in their official capacity (Sec. 11). "
        "The Secretary-General and Assistant Secretaries-General enjoy full diplomatic "
        "immunity (Sec. 19). In the Cumaraswamy Advisory Opinion, the ICJ held that "
        "UN experts on mission enjoy functional immunity for acts performed in their "
        "official capacity and that the determination of whether an act was performed "
        "in that capacity is made by the Secretary-General, whose determination has a "
        "presumptive evidentiary value before national courts. The scope of immunity "
        "for international organizations has been challenged on human rights grounds, "
        "particularly in employment disputes, but courts generally uphold immunity "
        "where alternative dispute resolution mechanisms exist."
    ),
    related=["diplomatic_consular_immunity", "icj_advisory_opinions",
             "un_charter_chapter_vii"],
)


# ---------------------------------------------------------------------------
# Cache Operations
# ---------------------------------------------------------------------------

_CACHE_INDEX: Optional[DoctrineCacheIndex] = None


def build_doctrine_cache() -> DoctrineCacheIndex:
    """Build or rebuild the doctrine cache index from DOCTRINE_BLOCKS."""
    global _CACHE_INDEX
    idx = DoctrineCacheIndex()
    idx.rebuild(DOCTRINE_BLOCKS)
    _CACHE_INDEX = idx

    cache_path = DOCTRINE_CACHE_DIR / "index.json"
    cache_path.write_text(json.dumps(idx.to_dict(), indent=2), encoding="utf-8")

    blocks_path = DOCTRINE_CACHE_DIR / "blocks.json"
    serialized = {k: v.to_dict() for k, v in DOCTRINE_BLOCKS.items()}
    blocks_path.write_text(json.dumps(serialized, indent=2), encoding="utf-8")

    logger.info(
        "Doctrine cache built: {} blocks, {} categories, integrity={}",
        idx.block_count, len(idx.categories), idx.integrity_hash,
    )
    return idx


def get_doctrine_cache() -> DoctrineCacheIndex:
    """Return the current cache index, building if needed."""
    global _CACHE_INDEX
    if _CACHE_INDEX is None:
        _CACHE_INDEX = build_doctrine_cache()
    return _CACHE_INDEX


def get_doctrine_cache_hash() -> str:
    """Return the integrity hash of the current cache."""
    return get_doctrine_cache().integrity_hash


def get_doctrine_cache_stats() -> Dict[str, Any]:
    """Return statistics about the doctrine cache."""
    idx = get_doctrine_cache()
    total_chars = sum(len(b.content) for b in DOCTRINE_BLOCKS.values())
    total_citations = sum(len(b.citations) for b in DOCTRINE_BLOCKS.values())
    avg_weight = (
        sum(b.authority_weight for b in DOCTRINE_BLOCKS.values()) / len(DOCTRINE_BLOCKS)
        if DOCTRINE_BLOCKS else 0.0
    )
    return {
        "engine_id": ENGINE_ID,
        "version": CACHE_VERSION,
        "block_count": idx.block_count,
        "category_count": len(idx.categories),
        "categories": dict(idx.categories),
        "total_content_chars": total_chars,
        "total_citations": total_citations,
        "average_authority_weight": round(avg_weight, 4),
        "integrity_hash": idx.integrity_hash,
        "created_at": idx.created_at,
    }


def get_doctrine_block(topic: str) -> Optional[DoctrineCacheBlock]:
    """Retrieve a single doctrine block by topic key."""
    return DOCTRINE_BLOCKS.get(topic)


def get_all_doctrine_topics() -> List[str]:
    """Return all doctrine topic keys."""
    return sorted(DOCTRINE_BLOCKS.keys())


def get_all_doctrine_categories() -> List[str]:
    """Return all unique categories."""
    return sorted({b.category for b in DOCTRINE_BLOCKS.values()})


def get_stale_doctrines(days_threshold: int = 90) -> List[DoctrineCacheBlock]:
    """Return doctrine blocks not verified within the given threshold."""
    now = datetime.now(timezone.utc)
    stale: List[DoctrineCacheBlock] = []
    for blk in DOCTRINE_BLOCKS.values():
        try:
            verified_dt = datetime.fromisoformat(blk.last_verified)
            if verified_dt.tzinfo is None:
                verified_dt = verified_dt.replace(tzinfo=timezone.utc)
            delta = (now - verified_dt).days
            if delta > days_threshold:
                stale.append(blk)
        except (ValueError, TypeError):
            stale.append(blk)
    return stale


def search_doctrines(
    query: str,
    category: Optional[str] = None,
    min_weight: float = 0.0,
    max_results: int = 10,
) -> List[Tuple[str, float, DoctrineCacheBlock]]:
    """
    Search doctrine blocks by keyword matching against topic, content,
    and citations. Returns (topic, relevance_score, block) tuples sorted
    by descending score.
    """
    query_lower = query.lower()
    query_terms = query_lower.split()
    results: List[Tuple[str, float, DoctrineCacheBlock]] = []

    for key, blk in DOCTRINE_BLOCKS.items():
        if category and blk.category != category:
            continue
        if blk.authority_weight < min_weight:
            continue

        score = 0.0
        searchable = (
            f"{blk.topic} {blk.content} {' '.join(blk.citations)} "
            f"{' '.join(blk.related_topics)} {blk.category}"
        ).lower()

        for term in query_terms:
            count = searchable.count(term)
            if count > 0:
                score += count * 1.0
                if term in blk.topic.lower():
                    score += 5.0
                if term in blk.category.lower():
                    score += 2.0

        if score > 0:
            score *= blk.authority_weight
            results.append((key, round(score, 4), blk))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:max_results]


def get_coverage_map() -> Dict[str, List[str]]:
    """Return a mapping of category -> list of topics for coverage analysis."""
    coverage: Dict[str, List[str]] = {}
    for key, blk in DOCTRINE_BLOCKS.items():
        coverage.setdefault(blk.category, []).append(key)
    for topics in coverage.values():
        topics.sort()
    return coverage


def verify_doctrine_integrity() -> Dict[str, Any]:
    """Verify all doctrine blocks have valid hashes and structure."""
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    for key, blk in DOCTRINE_BLOCKS.items():
        expected_hash = blk._compute_hash()
        if blk.hash_key != expected_hash:
            errors.append({
                "topic": key,
                "issue": "hash_mismatch",
                "expected": expected_hash,
                "actual": blk.hash_key,
            })

        if not blk.content or len(blk.content) < 50:
            errors.append({"topic": key, "issue": "content_too_short"})

        if not blk.citations:
            warnings.append({"topic": key, "issue": "no_citations"})

        if blk.authority_weight < 0.0 or blk.authority_weight > 1.0:
            errors.append({
                "topic": key,
                "issue": "invalid_authority_weight",
                "value": str(blk.authority_weight),
            })

        if not blk.related_topics:
            warnings.append({"topic": key, "issue": "no_related_topics"})

    idx = get_doctrine_cache()
    recomputed = DoctrineCacheIndex()
    recomputed.rebuild(DOCTRINE_BLOCKS)
    index_valid = recomputed.integrity_hash == idx.integrity_hash

    return {
        "total_blocks": len(DOCTRINE_BLOCKS),
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "index_integrity_valid": index_valid,
        "status": "PASS" if len(errors) == 0 and index_valid else "FAIL",
    }


# ---------------------------------------------------------------------------
# Module init
# ---------------------------------------------------------------------------

logger.info(
    "LG15 doctrines loaded: {} blocks across {} categories",
    len(DOCTRINE_BLOCKS),
    len({b.category for b in DOCTRINE_BLOCKS.values()}),
)
