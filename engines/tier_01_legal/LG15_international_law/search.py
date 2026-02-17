"""
LG15 International Law Engine - Search Module
================================================
TF-IDF inverted index, treaty search, arbitration rules search,
sanctions screening, and trade compliance checking.

Engine: LG15 International Law
Version: 2.0.0
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Pydantic result model
# ---------------------------------------------------------------------------

class SearchResult(BaseModel):
    """Single search result with score and provenance."""

    doc_id: str = Field(..., description="Unique document / doctrine identifier")
    title: str = Field(..., description="Human-readable title")
    snippet: str = Field("", description="Matching excerpt")
    score: float = Field(0.0, description="Relevance score 0-1")
    source: str = Field("doctrine_index", description="Which searcher produced this")
    category: str = Field("general", description="Domain category")
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ---------------------------------------------------------------------------
# Query hashing
# ---------------------------------------------------------------------------

def compute_query_hash(query: str, salt: str = "LG15_INTERNATIONAL_LAW_v2") -> str:
    """Deterministic SHA-256 hash of a query for caching/audit."""
    payload = f"{salt}::{query.strip().lower()}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# TF-IDF Inverted Index
# ---------------------------------------------------------------------------

_STOP_WORDS: set[str] = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "shall", "should", "may", "might", "can", "could", "not",
    "no", "nor", "so", "if", "then", "than", "too", "very", "just",
    "about", "above", "after", "again", "all", "also", "am", "any",
    "because", "before", "between", "both", "each", "few", "further",
    "here", "how", "into", "it", "its", "more", "most", "my", "other",
    "our", "out", "over", "own", "same", "some", "such", "that", "their",
    "them", "there", "these", "this", "those", "through", "under",
    "until", "up", "us", "we", "what", "when", "where", "which", "while",
    "who", "whom", "why", "you", "your",
}

_TOKEN_RE = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")


def _tokenize(text: str) -> list[str]:
    """Lowercase tokenize, remove stop words."""
    return [t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOP_WORDS]


@dataclass
class _DocRecord:
    doc_id: str
    title: str
    text: str
    category: str
    metadata: dict[str, Any] = field(default_factory=dict)
    tokens: list[str] = field(default_factory=list)
    tf: dict[str, float] = field(default_factory=dict)


class DoctrineSearchIndex:
    """TF-IDF inverted index over doctrine blocks and legal instruments."""

    def __init__(self) -> None:
        self._docs: dict[str, _DocRecord] = {}
        self._inverted: dict[str, set[str]] = defaultdict(set)
        self._idf: dict[str, float] = {}
        self._dirty: bool = False
        logger.info("DoctrineSearchIndex initialised")

    # -- index management ---------------------------------------------------

    def add_document(
        self,
        doc_id: str,
        title: str,
        text: str,
        category: str = "general",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Index a document."""
        tokens = _tokenize(f"{title} {text}")
        tf: dict[str, float] = {}
        if tokens:
            counts: dict[str, int] = defaultdict(int)
            for t in tokens:
                counts[t] += 1
            max_count = max(counts.values())
            for term, cnt in counts.items():
                tf[term] = 0.5 + 0.5 * (cnt / max_count)
        rec = _DocRecord(
            doc_id=doc_id,
            title=title,
            text=text,
            category=category,
            metadata=metadata or {},
            tokens=tokens,
            tf=tf,
        )
        self._docs[doc_id] = rec
        for term in tf:
            self._inverted[term].add(doc_id)
        self._dirty = True

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from the index."""
        rec = self._docs.pop(doc_id, None)
        if rec is None:
            return False
        for term in rec.tf:
            self._inverted[term].discard(doc_id)
            if not self._inverted[term]:
                del self._inverted[term]
        self._dirty = True
        return True

    def _rebuild_idf(self) -> None:
        """Recompute IDF values across the corpus."""
        n = len(self._docs)
        if n == 0:
            self._idf = {}
            self._dirty = False
            return
        self._idf = {}
        for term, doc_ids in self._inverted.items():
            df = len(doc_ids)
            self._idf[term] = math.log((n - df + 0.5) / (df + 0.5) + 1.0)
        self._dirty = False

    # -- query --------------------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 10,
        category_filter: str | None = None,
        min_score: float = 0.01,
    ) -> list[SearchResult]:
        """TF-IDF ranked search."""
        if self._dirty:
            self._rebuild_idf()

        q_tokens = _tokenize(query)
        if not q_tokens:
            return []

        candidate_ids: set[str] = set()
        for t in q_tokens:
            candidate_ids.update(self._inverted.get(t, set()))

        scored: list[tuple[float, str]] = []
        for doc_id in candidate_ids:
            rec = self._docs[doc_id]
            if category_filter and rec.category != category_filter:
                continue
            score = 0.0
            for t in q_tokens:
                tf_val = rec.tf.get(t, 0.0)
                idf_val = self._idf.get(t, 0.0)
                score += tf_val * idf_val
            if score >= min_score:
                scored.append((score, doc_id))

        scored.sort(key=lambda x: x[0], reverse=True)
        results: list[SearchResult] = []
        max_score = scored[0][0] if scored else 1.0
        for raw_score, doc_id in scored[:top_k]:
            rec = self._docs[doc_id]
            snippet = rec.text[:300]
            results.append(
                SearchResult(
                    doc_id=doc_id,
                    title=rec.title,
                    snippet=snippet,
                    score=round(raw_score / max_score, 4) if max_score > 0 else 0.0,
                    source="doctrine_index",
                    category=rec.category,
                    metadata=rec.metadata,
                )
            )
        return results

    @property
    def document_count(self) -> int:
        return len(self._docs)

    @property
    def term_count(self) -> int:
        return len(self._inverted)

    def get_stats(self) -> dict[str, Any]:
        return {
            "documents": self.document_count,
            "terms": self.term_count,
            "dirty": self._dirty,
        }


# ---------------------------------------------------------------------------
# Treaty status enum
# ---------------------------------------------------------------------------

class TreatyStatus(str, Enum):
    IN_FORCE = "in_force"
    SIGNED_NOT_RATIFIED = "signed_not_ratified"
    SUPERSEDED = "superseded"
    TERMINATED = "terminated"
    PROVISIONAL = "provisional_application"


# ---------------------------------------------------------------------------
# Treaty Searcher
# ---------------------------------------------------------------------------

@dataclass
class _TreatyRecord:
    treaty_id: str
    name: str
    short_name: str
    subject: str
    date_adopted: str
    date_in_force: str
    parties_count: int
    depositary: str
    citation: str
    status: TreatyStatus
    topics: list[str]
    key_articles: dict[str, str]
    notable_reservations: list[str]


# Canonical treaty database
_TREATIES: list[_TreatyRecord] = [
    _TreatyRecord(
        treaty_id="VCLT",
        name="Vienna Convention on the Law of Treaties",
        short_name="VCLT",
        subject="treaty_law",
        date_adopted="1969-05-23",
        date_in_force="1980-01-27",
        parties_count=116,
        depositary="UN Secretary-General",
        citation="1155 UNTS 331",
        status=TreatyStatus.IN_FORCE,
        topics=["treaty_interpretation", "treaty_reservations", "treaty_termination", "pacta_sunt_servanda", "jus_cogens"],
        key_articles={
            "Art.26": "Pacta sunt servanda - every treaty in force is binding and must be performed in good faith",
            "Art.31": "General rule of interpretation - good faith, ordinary meaning, context, object and purpose",
            "Art.32": "Supplementary means of interpretation - travaux preparatoires, circumstances of conclusion",
            "Art.53": "Jus cogens - treaty void if conflicts with peremptory norm of general international law",
            "Art.60": "Termination or suspension as consequence of breach",
            "Art.62": "Fundamental change of circumstances (rebus sic stantibus)",
        },
        notable_reservations=["US has not ratified but considers most provisions as codifying customary international law"],
    ),
    _TreatyRecord(
        treaty_id="UN_CHARTER",
        name="Charter of the United Nations",
        short_name="UN Charter",
        subject="international_organizations",
        date_adopted="1945-06-26",
        date_in_force="1945-10-24",
        parties_count=193,
        depositary="UN Secretary-General",
        citation="1 UNTS XVI",
        status=TreatyStatus.IN_FORCE,
        topics=["state_sovereignty", "use_of_force", "self_defense", "un_security_council", "peaceful_settlement", "self_determination", "human_rights"],
        key_articles={
            "Art.1": "Purposes - maintain peace, develop friendly relations, achieve cooperation, harmonize actions",
            "Art.2(4)": "Prohibition on use of force against territorial integrity or political independence of any state",
            "Art.33": "Parties to a dispute shall seek solution by negotiation, mediation, arbitration, judicial settlement",
            "Art.39": "Security Council determines threats to peace and decides on measures under Arts 41/42",
            "Art.51": "Inherent right of individual or collective self-defence if armed attack occurs",
            "Art.103": "Charter obligations prevail over obligations under any other international agreement",
        },
        notable_reservations=["No reservations permitted to the Charter"],
    ),
    _TreatyRecord(
        treaty_id="UNCLOS",
        name="United Nations Convention on the Law of the Sea",
        short_name="UNCLOS",
        subject="law_of_the_sea",
        date_adopted="1982-12-10",
        date_in_force="1994-11-16",
        parties_count=168,
        depositary="UN Secretary-General",
        citation="1833 UNTS 3",
        status=TreatyStatus.IN_FORCE,
        topics=["territorial_sea", "exclusive_economic_zone", "continental_shelf", "high_seas", "deep_seabed", "marine_environment", "dispute_settlement"],
        key_articles={
            "Art.3": "Breadth of territorial sea - up to 12 nautical miles from baseline",
            "Art.57": "Breadth of EEZ - up to 200 nautical miles from baseline",
            "Art.76": "Continental shelf - natural prolongation or 200 NM",
            "Art.87": "Freedom of the high seas - navigation, overflight, fishing, scientific research",
            "Art.136": "Common heritage of mankind - Area and its resources",
            "Art.287": "Choice of procedure - ITLOS, ICJ, Annex VII arbitral tribunal, Annex VIII special tribunal",
        },
        notable_reservations=["US has not ratified; applies many provisions as customary law"],
    ),
    _TreatyRecord(
        treaty_id="CISG",
        name="United Nations Convention on Contracts for the International Sale of Goods",
        short_name="CISG",
        subject="international_trade",
        date_adopted="1980-04-11",
        date_in_force="1988-01-01",
        parties_count=97,
        depositary="UN Secretary-General",
        citation="1489 UNTS 3",
        status=TreatyStatus.IN_FORCE,
        topics=["contract_formation", "obligations_seller", "obligations_buyer", "risk_of_loss", "remedies_breach", "fundamental_breach"],
        key_articles={
            "Art.1": "Applies to contracts for sale of goods between parties in different Contracting States",
            "Art.6": "Parties may exclude or derogate from any provision of CISG",
            "Art.25": "Fundamental breach - deprives party of substantially what entitled to expect",
            "Art.35": "Seller must deliver goods conforming in quantity, quality, description, packaging",
            "Art.49": "Buyer may declare contract avoided if fundamental breach or non-delivery",
            "Art.74": "Damages - loss including loss of profit suffered as consequence of breach",
        },
        notable_reservations=["US ratified with Art.1(1)(b) reservation; UK has not ratified"],
    ),
    _TreatyRecord(
        treaty_id="NY_CONVENTION",
        name="Convention on the Recognition and Enforcement of Foreign Arbitral Awards",
        short_name="New York Convention",
        subject="international_arbitration",
        date_adopted="1958-06-10",
        date_in_force="1959-06-07",
        parties_count=172,
        depositary="UN Secretary-General",
        citation="330 UNTS 38",
        status=TreatyStatus.IN_FORCE,
        topics=["arbitral_awards", "recognition_enforcement", "arbitration_agreement", "public_policy", "arbitrability"],
        key_articles={
            "Art.I": "Applies to arbitral awards made in another state or non-domestic awards",
            "Art.II": "Written agreement to arbitrate shall be recognized; court shall refer to arbitration",
            "Art.III": "Each state shall recognize awards as binding and enforce per procedural rules",
            "Art.V(1)": "Grounds for refusal: incapacity, no notice, excess of mandate, irregular composition, not binding",
            "Art.V(2)": "Refusal if subject not arbitrable or enforcement contrary to public policy",
            "Art.VII": "More-favourable-right provision - may rely on domestic law if more favourable",
        },
        notable_reservations=["US reciprocity and commercial reservations under Art.I(3)"],
    ),
    _TreatyRecord(
        treaty_id="ICCPR",
        name="International Covenant on Civil and Political Rights",
        short_name="ICCPR",
        subject="human_rights",
        date_adopted="1966-12-16",
        date_in_force="1976-03-23",
        parties_count=173,
        depositary="UN Secretary-General",
        citation="999 UNTS 171",
        status=TreatyStatus.IN_FORCE,
        topics=["civil_rights", "political_rights", "self_determination", "non_discrimination", "fair_trial", "freedom_expression", "right_to_life"],
        key_articles={
            "Art.1": "Right of self-determination of peoples",
            "Art.2": "Non-discrimination and effective remedy",
            "Art.6": "Right to life - inherent right, not arbitrarily deprived",
            "Art.7": "Prohibition of torture, cruel, inhuman or degrading treatment",
            "Art.14": "Right to fair trial, presumption of innocence",
            "Art.19": "Freedom of expression, subject to Art.19(3) restrictions",
        },
        notable_reservations=["US RUDs: declarations non-self-executing; reservations on Art.6(5) juvenile death penalty (since moot), Art.7 CIDT"],
    ),
    _TreatyRecord(
        treaty_id="ROME_STATUTE",
        name="Rome Statute of the International Criminal Court",
        short_name="Rome Statute",
        subject="international_criminal_law",
        date_adopted="1998-07-17",
        date_in_force="2002-07-01",
        parties_count=124,
        depositary="UN Secretary-General",
        citation="2187 UNTS 3",
        status=TreatyStatus.IN_FORCE,
        topics=["genocide", "crimes_against_humanity", "war_crimes", "crime_of_aggression", "complementarity", "individual_criminal_responsibility"],
        key_articles={
            "Art.5": "Jurisdiction: genocide, crimes against humanity, war crimes, aggression",
            "Art.7": "Crimes against humanity - widespread or systematic attack directed against civilian population",
            "Art.8": "War crimes - grave breaches of Geneva Conventions and other serious violations",
            "Art.17": "Complementarity - inadmissible if state genuinely investigating/prosecuting",
            "Art.25": "Individual criminal responsibility - commits, orders, solicits, induces, aids",
            "Art.27": "No immunity for heads of state or government",
        },
        notable_reservations=["US unsigned (Clinton signed, Bush unsigned); Russia unsigned; China, India, Israel not party"],
    ),
    _TreatyRecord(
        treaty_id="ICSID_CONVENTION",
        name="Convention on the Settlement of Investment Disputes Between States and Nationals of Other States",
        short_name="ICSID Convention",
        subject="investment_arbitration",
        date_adopted="1965-03-18",
        date_in_force="1966-10-14",
        parties_count=163,
        depositary="World Bank",
        citation="575 UNTS 159",
        status=TreatyStatus.IN_FORCE,
        topics=["investor_state_dispute_settlement", "bilateral_investment_treaties", "expropriation", "fair_equitable_treatment", "most_favoured_nation"],
        key_articles={
            "Art.25": "Jurisdiction - legal dispute arising directly out of an investment between Contracting State and national of another",
            "Art.26": "Consent to arbitration - deemed exclusive; no need to exhaust local remedies unless required",
            "Art.36": "Request for arbitration - written, identifying dispute and parties' consent",
            "Art.42": "Applicable law - law agreed by parties; failing agreement, host state law + applicable rules of international law",
            "Art.52": "Annulment - manifest excess of powers, corruption, departure from fundamental rule, failure to state reasons, improper constitution",
            "Art.54": "Enforcement - pecuniary obligations of award enforced as final judgment in any Contracting State",
        },
        notable_reservations=["Bolivia, Ecuador, Venezuela denounced (2007-12); some states denoting only certain disputes"],
    ),
    _TreatyRecord(
        treaty_id="GATT_1994",
        name="General Agreement on Tariffs and Trade 1994",
        short_name="GATT 1994",
        subject="international_trade",
        date_adopted="1994-04-15",
        date_in_force="1995-01-01",
        parties_count=164,
        depositary="WTO Director-General",
        citation="Marrakesh Agreement Annex 1A",
        status=TreatyStatus.IN_FORCE,
        topics=["most_favoured_nation", "national_treatment", "tariff_bindings", "quantitative_restrictions", "general_exceptions", "security_exceptions"],
        key_articles={
            "Art.I": "Most-Favoured-Nation - any advantage granted to any country extended to all WTO members",
            "Art.III": "National Treatment - imported products treated no less favourably than domestic products",
            "Art.VI": "Anti-dumping and countervailing duties",
            "Art.XI": "General elimination of quantitative restrictions",
            "Art.XX": "General exceptions - public morals, health, conservation, etc. (subject to chapeau)",
            "Art.XXI": "Security exceptions - essential security interests",
        },
        notable_reservations=["WTO membership package - no reservations; single undertaking"],
    ),
    _TreatyRecord(
        treaty_id="PARIS_AGREEMENT",
        name="Paris Agreement under the UNFCCC",
        short_name="Paris Agreement",
        subject="international_environmental_law",
        date_adopted="2015-12-12",
        date_in_force="2016-11-04",
        parties_count=195,
        depositary="UN Secretary-General",
        citation="TIAS 16-1104",
        status=TreatyStatus.IN_FORCE,
        topics=["climate_change", "nationally_determined_contributions", "global_temperature", "carbon_neutrality", "loss_and_damage", "climate_finance"],
        key_articles={
            "Art.2": "Hold temperature increase well below 2C, pursue 1.5C above pre-industrial levels",
            "Art.3": "Nationally determined contributions (NDCs) represent highest possible ambition",
            "Art.4": "Aim to reach global peaking ASAP; balance emissions and removals second half of century",
            "Art.6": "Cooperative approaches - voluntary cooperation, ITMOs, sustainable development mechanism",
            "Art.8": "Loss and damage associated with climate change impacts",
            "Art.13": "Enhanced transparency framework - biennial reports on emissions and progress",
        },
        notable_reservations=["US withdrew under Trump (eff. 2020-11-04), rejoined under Biden (2021-02-19), withdrew again under Trump (2025)"],
    ),
    _TreatyRecord(
        treaty_id="ECHR",
        name="European Convention on Human Rights",
        short_name="ECHR",
        subject="human_rights",
        date_adopted="1950-11-04",
        date_in_force="1953-09-03",
        parties_count=46,
        depositary="Council of Europe Secretary-General",
        citation="ETS No. 005",
        status=TreatyStatus.IN_FORCE,
        topics=["right_to_life", "prohibition_torture", "right_liberty", "fair_trial", "private_life", "freedom_expression", "freedom_religion", "prohibition_discrimination"],
        key_articles={
            "Art.2": "Right to life",
            "Art.3": "Prohibition of torture - no derogation permitted",
            "Art.5": "Right to liberty and security",
            "Art.6": "Right to a fair trial - civil rights and criminal charges",
            "Art.8": "Right to respect for private and family life",
            "Art.10": "Freedom of expression, subject to Art.10(2) restrictions",
        },
        notable_reservations=["UK Human Rights Act 1998 incorporates domestically; Russia expelled from CoE March 2022"],
    ),
    _TreatyRecord(
        treaty_id="TRIPS",
        name="Agreement on Trade-Related Aspects of Intellectual Property Rights",
        short_name="TRIPS",
        subject="intellectual_property",
        date_adopted="1994-04-15",
        date_in_force="1995-01-01",
        parties_count=164,
        depositary="WTO Director-General",
        citation="Marrakesh Agreement Annex 1C",
        status=TreatyStatus.IN_FORCE,
        topics=["copyright", "trademarks", "patents", "trade_secrets", "geographical_indications", "enforcement_ip", "compulsory_licensing"],
        key_articles={
            "Art.3": "National treatment - each Member shall accord to nationals of other Members treatment no less favourable",
            "Art.9": "Copyright - compliance with Berne Convention Arts 1-21",
            "Art.27": "Patentable subject matter - inventions in all fields of technology, subject to Art.27(2)/(3) exclusions",
            "Art.28": "Patent rights - prevent third parties from making, using, selling without consent",
            "Art.31": "Compulsory licensing - other use without authorization of right holder (subject to conditions)",
            "Art.41": "Enforcement - fair, equitable, not unnecessarily complicated, not create barriers to legitimate trade",
        },
        notable_reservations=["Doha Declaration on TRIPS and Public Health (2001) - compulsory licensing flexibility"],
    ),
    _TreatyRecord(
        treaty_id="GENEVA_III",
        name="Geneva Convention Relative to the Treatment of Prisoners of War",
        short_name="Geneva III (POW)",
        subject="international_humanitarian_law",
        date_adopted="1949-08-12",
        date_in_force="1950-10-21",
        parties_count=196,
        depositary="Swiss Federal Council",
        citation="75 UNTS 135",
        status=TreatyStatus.IN_FORCE,
        topics=["prisoners_of_war", "combatant_status", "humane_treatment", "judicial_guarantees", "repatriation", "protecting_powers"],
        key_articles={
            "Art.4": "Definition of prisoners of war - members of armed forces, militia, resistance movements",
            "Art.13": "Humane treatment - protected against violence, intimidation, insults, public curiosity",
            "Art.17": "Interrogation - name, rank, date of birth, serial number only; no coercion",
            "Art.25-28": "Quarters, food, clothing - conditions not inferior to those of detaining power's forces",
            "Art.82-88": "Penal and disciplinary sanctions - judicial guarantees",
            "Art.118": "Repatriation - without delay after cessation of active hostilities",
        },
        notable_reservations=["Universally ratified - all 196 states party; Common Article 3 applies to non-international conflicts"],
    ),
]


class TreatySearcher:
    """Search treaties by subject, parties, date, status, and keywords."""

    def __init__(self) -> None:
        self._treaties: list[_TreatyRecord] = list(_TREATIES)
        self._index = DoctrineSearchIndex()
        self._build_index()
        logger.info("TreatySearcher initialised with {} treaties", len(self._treaties))

    def _build_index(self) -> None:
        for t in self._treaties:
            articles_text = " ".join(f"{k}: {v}" for k, v in t.key_articles.items())
            topics_text = " ".join(t.topics)
            full_text = f"{t.name} {t.short_name} {t.subject} {topics_text} {articles_text} {' '.join(t.notable_reservations)}"
            self._index.add_document(
                doc_id=t.treaty_id,
                title=t.name,
                text=full_text,
                category=t.subject,
                metadata={
                    "date_adopted": t.date_adopted,
                    "date_in_force": t.date_in_force,
                    "parties_count": t.parties_count,
                    "status": t.status.value,
                    "citation": t.citation,
                },
            )

    def search_by_subject(self, subject: str, top_k: int = 5) -> list[SearchResult]:
        """Search treaties by subject area."""
        return self._index.search(subject, top_k=top_k)

    def search_by_keyword(self, keyword: str, top_k: int = 5) -> list[SearchResult]:
        """Full text keyword search across treaties."""
        return self._index.search(keyword, top_k=top_k)

    def search_by_status(self, status: TreatyStatus) -> list[SearchResult]:
        """Filter treaties by status."""
        results: list[SearchResult] = []
        for t in self._treaties:
            if t.status == status:
                results.append(
                    SearchResult(
                        doc_id=t.treaty_id,
                        title=t.name,
                        snippet=f"Status: {t.status.value}, Parties: {t.parties_count}, In force: {t.date_in_force}",
                        score=1.0,
                        source="treaty_searcher",
                        category=t.subject,
                        metadata={"status": t.status.value, "parties_count": t.parties_count},
                    )
                )
        return results

    def search_by_date_range(self, start_year: int, end_year: int) -> list[SearchResult]:
        """Find treaties adopted within a date range."""
        results: list[SearchResult] = []
        for t in self._treaties:
            adopted_year = int(t.date_adopted[:4])
            if start_year <= adopted_year <= end_year:
                results.append(
                    SearchResult(
                        doc_id=t.treaty_id,
                        title=t.name,
                        snippet=f"Adopted: {t.date_adopted}, In force: {t.date_in_force}, Parties: {t.parties_count}",
                        score=1.0 - abs(adopted_year - (start_year + end_year) / 2) / max(end_year - start_year, 1),
                        source="treaty_searcher",
                        category=t.subject,
                        metadata={"date_adopted": t.date_adopted, "date_in_force": t.date_in_force},
                    )
                )
        results.sort(key=lambda r: r.score, reverse=True)
        return results

    def search_by_parties_count(self, min_parties: int = 100) -> list[SearchResult]:
        """Find widely ratified treaties."""
        results: list[SearchResult] = []
        for t in self._treaties:
            if t.parties_count >= min_parties:
                results.append(
                    SearchResult(
                        doc_id=t.treaty_id,
                        title=t.name,
                        snippet=f"Parties: {t.parties_count}, Status: {t.status.value}",
                        score=t.parties_count / 200.0,
                        source="treaty_searcher",
                        category=t.subject,
                        metadata={"parties_count": t.parties_count, "status": t.status.value},
                    )
                )
        results.sort(key=lambda r: r.score, reverse=True)
        return results

    def get_treaty(self, treaty_id: str) -> _TreatyRecord | None:
        """Retrieve a specific treaty record."""
        for t in self._treaties:
            if t.treaty_id == treaty_id:
                return t
        return None

    def get_all_treaty_ids(self) -> list[str]:
        return [t.treaty_id for t in self._treaties]


# ---------------------------------------------------------------------------
# Arbitration Rules Searcher
# ---------------------------------------------------------------------------

@dataclass
class _ArbitrationRule:
    rule_id: str
    institution: str
    name: str
    year: int
    topic: str
    rule_number: str
    text: str
    keywords: list[str]


_ARBITRATION_RULES: list[_ArbitrationRule] = [
    _ArbitrationRule("UNCITRAL_1", "UNCITRAL", "Notice and Calculation of Periods of Time", 2021, "procedure", "Art.2", "Notice or communication is deemed received on the day it is delivered to the addressee, or to the addressee's habitual residence, place of business, or mailing address.", ["notice", "communication", "delivery", "time_periods"]),
    _ArbitrationRule("UNCITRAL_2", "UNCITRAL", "Notice of Arbitration", 2021, "commencement", "Art.3", "The party initiating arbitration shall communicate a notice of arbitration including the request for dispute to be referred to arbitration, names and contact details of parties, identification of arbitration agreement, a brief description of the claim and amount involved.", ["notice_of_arbitration", "commencement", "claim", "request"]),
    _ArbitrationRule("UNCITRAL_3", "UNCITRAL", "Appointment of Arbitrators", 2021, "tribunal_constitution", "Arts.7-10", "If parties have not agreed on number, three arbitrators shall be appointed. Each party appoints one; the two appointed designate the third (presiding). Failing agreement, appointing authority (PCA) designates.", ["appointment", "arbitrators", "presiding", "appointing_authority", "pca"]),
    _ArbitrationRule("UNCITRAL_4", "UNCITRAL", "Interim Measures", 2021, "interim_measures", "Art.26", "Tribunal may grant interim measures to maintain status quo, prevent action that would prejudice arbitral process, provide means of preserving assets, or preserve evidence material and relevant to dispute.", ["interim_measures", "preservation", "status_quo", "injunction"]),
    _ArbitrationRule("UNCITRAL_5", "UNCITRAL", "Award", 2021, "award", "Arts.33-35", "Award shall be made in writing, state reasons upon which it is based, date and place of arbitration. It is final and binding. The tribunal may make an interim, interlocutory, or partial award.", ["award", "final", "binding", "reasons", "partial_award"]),
    _ArbitrationRule("ICC_1", "ICC", "Arbitration Agreement", 2021, "jurisdiction", "Art.6", "Where parties agree to submit disputes to ICC arbitration, they shall be deemed to have submitted to ICC Rules in effect on date of commencement. The Court determines prima facie existence of arbitration agreement.", ["arbitration_agreement", "jurisdiction", "prima_facie", "icc_court"]),
    _ArbitrationRule("ICC_2", "ICC", "Case Management Conference", 2021, "procedure", "Art.24", "Tribunal shall convene a case management conference to consult parties on procedural measures and establish procedural timetable. Conference may be conducted by any means.", ["case_management", "conference", "timetable", "procedure"]),
    _ArbitrationRule("ICC_3", "ICC", "Emergency Arbitrator", 2021, "interim_measures", "Art.29 + Appendix V", "A party needing urgent interim or conservatory measures before constitution of tribunal may apply for emergency arbitrator. Application decided within 15 days. EA order is binding.", ["emergency_arbitrator", "urgent", "conservatory_measures", "interim"]),
    _ArbitrationRule("ICC_4", "ICC", "Scrutiny of Award", 2021, "award", "Art.34", "Before signing any award, tribunal shall submit draft to the ICC Court. Court may lay down modifications to form and draw attention to points of substance without affecting tribunal's liberty of decision.", ["scrutiny", "icc_court", "draft_award", "modifications"]),
    _ArbitrationRule("ICC_5", "ICC", "Costs", 2021, "costs", "Art.38", "Costs include ICC administrative expenses and arbitrator fees (fixed by Court), reasonable legal costs, and expenses of parties and witnesses. Costs may be provisionally advanced.", ["costs", "fees", "administrative_expenses", "advance_on_costs"]),
    _ArbitrationRule("ICSID_1", "ICSID", "Jurisdiction Requirements", 2022, "jurisdiction", "Rule 1/Art.25", "Jurisdiction requires: (a) legal dispute, (b) arising directly out of an investment, (c) between a Contracting State and a national of another Contracting State, (d) consent in writing.", ["jurisdiction", "investment", "consent", "contracting_state", "national"]),
    _ArbitrationRule("ICSID_2", "ICSID", "Constitution of Tribunal", 2022, "tribunal_constitution", "Rules 15-22", "Tribunal consists of sole arbitrator or any uneven number (default 3). Each party appoints one; president designated by agreement or by Chairman of Administrative Council.", ["constitution", "tribunal", "sole_arbitrator", "appointment"]),
    _ArbitrationRule("ICSID_3", "ICSID", "Provisional Measures", 2022, "interim_measures", "Rule 47", "Party may request tribunal to recommend provisional measures for preservation of its rights. Tribunal may recommend measures at any time after constitution. Measures may be modified or revoked.", ["provisional_measures", "preservation", "rights", "recommendation"]),
    _ArbitrationRule("ICSID_4", "ICSID", "Award and Annulment", 2022, "award", "Rules 58-62/Art.52", "Award is final and binding, not subject to any appeal. Annulment on limited grounds: manifest excess of powers, corruption, serious departure from fundamental rule of procedure, failure to state reasons, improper constitution.", ["award", "annulment", "final", "binding", "manifest_excess"]),
    _ArbitrationRule("ICSID_5", "ICSID", "Enforcement", 2022, "enforcement", "Art.54", "Each Contracting State shall recognize an ICSID award as binding and enforce pecuniary obligations as if it were a final judgment of a court in that State. Sovereign immunity from execution not waived.", ["enforcement", "recognition", "pecuniary", "sovereign_immunity"]),
    _ArbitrationRule("AAA_ICDR_1", "AAA/ICDR", "Filing and Commencement", 2021, "commencement", "Art.2", "Filing of a Notice of Arbitration with ICDR commences arbitration. Notice shall include a statement of the nature of the dispute, claim amount, agreement to arbitrate, and requested relief.", ["filing", "commencement", "notice", "claim"]),
    _ArbitrationRule("AAA_ICDR_2", "AAA/ICDR", "Emergency Measures of Protection", 2021, "interim_measures", "Art.6", "A party may apply for emergency measures before constitution of tribunal. Emergency arbitrator shall establish a schedule for consideration within two business days. Decision within the shortest time practicable.", ["emergency", "protection", "interim", "urgent"]),
    _ArbitrationRule("AAA_ICDR_3", "AAA/ICDR", "Applicable Law", 2021, "applicable_law", "Art.35", "Tribunal shall apply law or rules of law designated by the parties. Failing designation, tribunal shall apply law or rules of law it determines appropriate. Tribunal may decide as amiable compositeur or ex aequo et bono only if parties have authorized.", ["applicable_law", "choice_of_law", "amiable_compositeur", "ex_aequo"]),
    _ArbitrationRule("AAA_ICDR_4", "AAA/ICDR", "Confidentiality", 2021, "confidentiality", "Art.37", "Unless parties agree otherwise, confidential information disclosed during proceedings shall not be divulged. Awards may be made public only with consent of all parties or as required by law.", ["confidentiality", "disclosure", "privacy", "awards"]),
]


class ArbitrationRulesSearcher:
    """Search UNCITRAL, ICC, ICSID, AAA/ICDR arbitration rules by topic."""

    def __init__(self) -> None:
        self._rules: list[_ArbitrationRule] = list(_ARBITRATION_RULES)
        self._index = DoctrineSearchIndex()
        self._build_index()
        logger.info("ArbitrationRulesSearcher initialised with {} rules", len(self._rules))

    def _build_index(self) -> None:
        for r in self._rules:
            full_text = f"{r.institution} {r.name} {r.topic} {r.text} {' '.join(r.keywords)}"
            self._index.add_document(
                doc_id=r.rule_id,
                title=f"{r.institution} - {r.name}",
                text=full_text,
                category=r.topic,
                metadata={"institution": r.institution, "year": r.year, "rule_number": r.rule_number},
            )

    def search_by_topic(self, topic: str, top_k: int = 10) -> list[SearchResult]:
        """Search rules by topic keyword."""
        return self._index.search(topic, top_k=top_k)

    def search_by_institution(self, institution: str, top_k: int = 10) -> list[SearchResult]:
        """Filter rules by institution name."""
        results: list[SearchResult] = []
        inst_upper = institution.upper()
        for r in self._rules:
            if inst_upper in r.institution.upper():
                results.append(
                    SearchResult(
                        doc_id=r.rule_id,
                        title=f"{r.institution} - {r.name}",
                        snippet=r.text[:300],
                        score=1.0,
                        source="arbitration_rules_searcher",
                        category=r.topic,
                        metadata={"institution": r.institution, "rule_number": r.rule_number, "year": r.year},
                    )
                )
        return results[:top_k]

    def compare_institutions(self, topic: str) -> dict[str, list[SearchResult]]:
        """Compare rules on a topic across all institutions."""
        grouped: dict[str, list[SearchResult]] = defaultdict(list)
        results = self._index.search(topic, top_k=50)
        for r in results:
            inst = r.metadata.get("institution", "unknown")
            grouped[inst].append(r)
        return dict(grouped)

    def get_rule(self, rule_id: str) -> _ArbitrationRule | None:
        for r in self._rules:
            if r.rule_id == rule_id:
                return r
        return None


# ---------------------------------------------------------------------------
# Sanctions Screener (OFAC SDN pattern matching)
# ---------------------------------------------------------------------------

@dataclass
class _SanctionsProgram:
    program_id: str
    name: str
    authority: str
    countries: list[str]
    description: str
    general_licenses: list[str]
    primary_sanctions: bool
    secondary_sanctions: bool


_SANCTIONS_PROGRAMS: list[_SanctionsProgram] = [
    _SanctionsProgram("IRAN", "Iran Sanctions", "IEEPA, CISADA, IFCA, ITRA", ["IR"], "Comprehensive sanctions on Iran covering trade, financial transactions, energy sector, shipping, and designated persons.", ["GL-D (personal remittances)", "GL-H (humanitarian goods)", "GL-I (internet communications)", "GL-F (certain legal services)"], primary_sanctions=True, secondary_sanctions=True),
    _SanctionsProgram("CUBA", "Cuba Sanctions", "TWEA, Libertad Act (Helms-Burton), CACR", ["CU"], "Comprehensive embargo on Cuba with limited exceptions for travel, remittances, humanitarian trade, and informational materials.", ["GL-SUPPORT-1 (support for Cuban people)", "GL-OFAC-4 (journalistic activities)", "GL-TSR-3 (certain travel)"], primary_sanctions=True, secondary_sanctions=False),
    _SanctionsProgram("DPRK", "North Korea Sanctions", "IEEPA, NKSPEA, Otto Warmbier Act", ["KP"], "Comprehensive sanctions prohibiting trade, financial transactions, and dealings with DPRK government and designated entities.", ["GL-1 (personal communications)", "GL-2 (certain humanitarian)"], primary_sanctions=True, secondary_sanctions=True),
    _SanctionsProgram("SYRIA", "Syria Sanctions", "IEEPA, Syria Accountability Act, Caesar Act", ["SY"], "Comprehensive sanctions targeting Syrian government, military, and designated persons. Caesar Act adds secondary sanctions.", ["GL-SYRIA-2 (humanitarian activities)", "GL-SYRIA-5 (NGO activities)"], primary_sanctions=True, secondary_sanctions=True),
    _SanctionsProgram("RUSSIA", "Russia/Ukraine Sanctions", "IEEPA, CAATSA, Ukraine Freedom Support Act", ["RU"], "Targeted sanctions on Russian individuals, entities, financial institutions, energy sector, defense sector, and Crimea region. Comprehensive on Crimea/DNR/LNR.", ["GL-8C (wind-down)", "GL-13C (energy transactions)"], primary_sanctions=True, secondary_sanctions=True),
    _SanctionsProgram("VENEZUELA", "Venezuela Sanctions", "IEEPA, EOs 13692, 13808, 13850", ["VE"], "Targeted sanctions on Venezuelan government officials, PdVSA, gold sector, and designated persons.", ["GL-5E (humanitarian goods)", "GL-7F (PdVSA wind-down)", "GL-40B (certain transactions)"], primary_sanctions=True, secondary_sanctions=True),
    _SanctionsProgram("SDGT", "Global Terrorism Sanctions", "IEEPA, EO 13224", [], "Designation of Specially Designated Global Terrorists (SDGTs) blocking assets and prohibiting transactions.", ["GL-A (authorized offices)", "GL-I (legal fees)"], primary_sanctions=True, secondary_sanctions=True),
    _SanctionsProgram("SDN", "SDN List General", "Various authorities", [], "The Specially Designated Nationals and Blocked Persons List compiles individuals and entities with blocked assets and with whom US persons generally cannot deal.", [], primary_sanctions=True, secondary_sanctions=False),
]

_SDN_PATTERNS: list[dict[str, str]] = [
    {"pattern": "ISLAMIC REVOLUTIONARY GUARD CORPS", "program": "IRAN", "type": "entity", "alias": "IRGC"},
    {"pattern": "CENTRAL BANK OF IRAN", "program": "IRAN", "type": "entity", "alias": "CBI, Bank Markazi"},
    {"pattern": "ROSNEFT", "program": "RUSSIA", "type": "entity", "alias": "Rosneft Oil Company"},
    {"pattern": "PDVSA", "program": "VENEZUELA", "type": "entity", "alias": "Petroleos de Venezuela"},
    {"pattern": "KOREA MINING DEVELOPMENT", "program": "DPRK", "type": "entity", "alias": "KOMID"},
    {"pattern": "WAGNER GROUP", "program": "RUSSIA", "type": "entity", "alias": "PMC Wagner"},
    {"pattern": "HEZBOLLAH", "program": "SDGT", "type": "entity", "alias": "Hizballah"},
    {"pattern": "HAMAS", "program": "SDGT", "type": "entity", "alias": "Islamic Resistance Movement"},
    {"pattern": "AL-QAEDA", "program": "SDGT", "type": "entity", "alias": "AQ, Al-Qa'ida"},
    {"pattern": "SBERBANK", "program": "RUSSIA", "type": "entity", "alias": "Sberbank of Russia"},
    {"pattern": "VTB BANK", "program": "RUSSIA", "type": "entity", "alias": "VTB"},
    {"pattern": "GAZPROM", "program": "RUSSIA", "type": "entity", "alias": "Gazprom PJSC"},
    {"pattern": "MILITARY INDUSTRY", "program": "IRAN", "type": "sector", "alias": "Defense Industries Organization (DIO)"},
    {"pattern": "SCIENTIFIC STUDIES AND RESEARCH CENTER", "program": "SYRIA", "type": "entity", "alias": "SSRC, CERS"},
]


class SanctionsScreener:
    """Screen entities against OFAC SDN patterns, country programs, and general licenses."""

    def __init__(self) -> None:
        self._programs: list[_SanctionsProgram] = list(_SANCTIONS_PROGRAMS)
        self._sdn_patterns: list[dict[str, str]] = list(_SDN_PATTERNS)
        logger.info("SanctionsScreener initialised with {} programs, {} SDN patterns", len(self._programs), len(self._sdn_patterns))

    def screen_entity(self, entity_name: str, country_code: str = "") -> dict[str, Any]:
        """Screen an entity name against SDN patterns and country programs."""
        entity_upper = entity_name.upper().strip()
        country_upper = country_code.upper().strip()

        hits: list[dict[str, Any]] = []
        risk_score = 0.0

        # Check SDN patterns
        for pat in self._sdn_patterns:
            pattern_upper = pat["pattern"]
            alias_parts = [a.strip().upper() for a in pat.get("alias", "").split(",") if a.strip()]
            all_names = [pattern_upper] + alias_parts

            for name in all_names:
                if name in entity_upper or entity_upper in name:
                    hits.append({
                        "match_type": "sdn_pattern",
                        "matched_name": pat["pattern"],
                        "alias": pat.get("alias", ""),
                        "program": pat["program"],
                        "entity_type": pat["type"],
                        "confidence": 0.95 if entity_upper == name else 0.70,
                    })
                    risk_score = max(risk_score, 0.95 if entity_upper == name else 0.70)
                    break

        # Check country programs
        country_programs: list[dict[str, Any]] = []
        for prog in self._programs:
            if country_upper in prog.countries:
                country_programs.append({
                    "program_id": prog.program_id,
                    "name": prog.name,
                    "authority": prog.authority,
                    "primary_sanctions": prog.primary_sanctions,
                    "secondary_sanctions": prog.secondary_sanctions,
                    "general_licenses": prog.general_licenses,
                })
                risk_score = max(risk_score, 0.80)

        risk_level = "CLEAR"
        if risk_score >= 0.90:
            risk_level = "BLOCKED"
        elif risk_score >= 0.70:
            risk_level = "HIGH_RISK"
        elif risk_score >= 0.50:
            risk_level = "ELEVATED"
        elif risk_score >= 0.20:
            risk_level = "CAUTION"

        return {
            "entity_screened": entity_name,
            "country_code": country_code,
            "risk_level": risk_level,
            "risk_score": round(risk_score, 4),
            "sdn_hits": hits,
            "country_programs": country_programs,
            "total_hits": len(hits) + len(country_programs),
            "screened_at": datetime.utcnow().isoformat(),
            "disclaimer": "This screening uses pattern matching against known SDN entries. It is NOT a substitute for full OFAC SDN list screening via official OFAC tools. Consult legal counsel for compliance decisions.",
        }

    def get_program(self, program_id: str) -> _SanctionsProgram | None:
        for prog in self._programs:
            if prog.program_id == program_id.upper():
                return prog
        return None

    def list_programs(self) -> list[dict[str, Any]]:
        return [
            {
                "program_id": p.program_id,
                "name": p.name,
                "countries": p.countries,
                "primary_sanctions": p.primary_sanctions,
                "secondary_sanctions": p.secondary_sanctions,
            }
            for p in self._programs
        ]

    def get_general_licenses(self, program_id: str) -> list[str]:
        prog = self.get_program(program_id)
        if prog is None:
            return []
        return prog.general_licenses

    def check_country_risk(self, country_code: str) -> dict[str, Any]:
        """Check all sanctions programs applicable to a country."""
        applicable: list[dict[str, Any]] = []
        for prog in self._programs:
            if country_code.upper() in prog.countries:
                applicable.append({
                    "program_id": prog.program_id,
                    "name": prog.name,
                    "authority": prog.authority,
                    "description": prog.description,
                    "primary_sanctions": prog.primary_sanctions,
                    "secondary_sanctions": prog.secondary_sanctions,
                    "general_licenses_count": len(prog.general_licenses),
                })
        comprehensive = any(p["program_id"] in ("IRAN", "CUBA", "DPRK", "SYRIA") for p in applicable)
        return {
            "country_code": country_code.upper(),
            "programs_applicable": len(applicable),
            "comprehensive_sanctions": comprehensive,
            "programs": applicable,
            "risk_level": "COMPREHENSIVE_EMBARGO" if comprehensive else ("TARGETED_SANCTIONS" if applicable else "NO_PROGRAM"),
        }


# ---------------------------------------------------------------------------
# Trade Compliance Checker
# ---------------------------------------------------------------------------

@dataclass
class _WTODiscipline:
    discipline_id: str
    name: str
    gatt_article: str
    description: str
    key_tests: list[str]
    exceptions: list[str]
    landmark_cases: list[str]


_WTO_DISCIPLINES: list[_WTODiscipline] = [
    _WTODiscipline(
        discipline_id="MFN",
        name="Most-Favoured-Nation Treatment",
        gatt_article="GATT Art.I",
        description="Any advantage, favour, privilege or immunity granted by any WTO Member to any product originating in or destined for any other country shall be accorded immediately and unconditionally to the like product originating in or destined for the territories of all other WTO Members.",
        key_tests=["Like product analysis (physical properties, end uses, tariff classification, consumer preferences)", "Advantage/favour/privilege/immunity granted", "Immediately and unconditionally extended to all Members"],
        exceptions=["Art.XXIV (customs unions, free trade areas)", "Enabling Clause (GSP for developing countries)", "Waivers under Art.IX:3"],
        landmark_cases=["Canada - Autos (DS139)", "EC - Bananas III (DS27)", "Indonesia - Autos (DS54)"],
    ),
    _WTODiscipline(
        discipline_id="NT",
        name="National Treatment",
        gatt_article="GATT Art.III",
        description="Imported products shall not be subject to internal taxes or regulations in excess of or less favourable than those applied to like domestic products. Applies to laws, regulations, and requirements affecting internal sale, offering, purchase, transportation, distribution, or use.",
        key_tests=["Like product determination (border tax adjustment test for Art.III:2; aims-and-effects for Art.III:4)", "Tax/regulation 'in excess of' or 'less favourable' than applied to domestic", "So as to afford protection to domestic production (Art.III:1 context)"],
        exceptions=["Art.III:8(a) (government procurement)", "Art.III:8(b) (subsidies to domestic producers)", "Art.XX general exceptions"],
        landmark_cases=["Japan - Alcoholic Beverages II (DS8)", "Korea - Alcoholic Beverages (DS75)", "EC - Asbestos (DS135)"],
    ),
    _WTODiscipline(
        discipline_id="TBT",
        name="Technical Barriers to Trade",
        gatt_article="TBT Agreement",
        description="Technical regulations and standards shall not create unnecessary obstacles to international trade. Measures must not be more trade-restrictive than necessary to fulfil a legitimate objective (e.g., national security, prevention of deceptive practices, protection of human health/safety, environment).",
        key_tests=["Is the measure a 'technical regulation' (mandatory) or 'standard' (voluntary)?", "Does it create unnecessary obstacle to trade?", "Is it more trade-restrictive than necessary to fulfil legitimate objective?", "Is it based on relevant international standards (Art.2.4)?"],
        exceptions=["Legitimate objectives: security, prevention of deceptive practices, health, safety, environment", "Art.2.5 rebuttable presumption if based on international standard"],
        landmark_cases=["US - Clove Cigarettes (DS406)", "US - Tuna II (Mexico) (DS381)", "EC - Seal Products (DS400)"],
    ),
    _WTODiscipline(
        discipline_id="SPS",
        name="Sanitary and Phytosanitary Measures",
        gatt_article="SPS Agreement",
        description="Measures to protect human, animal, or plant life or health must be based on scientific principles and risk assessment. Must not be maintained without sufficient scientific evidence (Art.2.2) except provisionally under Art.5.7. Must not arbitrarily or unjustifiably discriminate.",
        key_tests=["Is the measure an SPS measure (protects against pest/disease/contaminant risk)?", "Is it based on scientific principles and risk assessment (Art.2.2, Art.5.1)?", "Is it maintained without sufficient scientific evidence?", "Does it conform to international standards (Codex, OIE, IPPC)?"],
        exceptions=["Art.5.7 provisional measures (insufficient scientific evidence)", "Appropriate level of protection (ALOP) is sovereign choice", "Based on Codex/OIE/IPPC standard = presumed WTO-consistent"],
        landmark_cases=["EC - Hormones (DS26)", "Australia - Salmon (DS18)", "Japan - Apples (DS245)", "EC - Biotech Products (DS291)"],
    ),
    _WTODiscipline(
        discipline_id="SUBSIDIES",
        name="Subsidies and Countervailing Measures",
        gatt_article="SCM Agreement",
        description="A subsidy exists when there is a financial contribution by a government that confers a benefit. Prohibited subsidies: export subsidies and import substitution subsidies. Actionable subsidies: those causing adverse effects (injury, serious prejudice, nullification/impairment).",
        key_tests=["Financial contribution (grant, loan, equity, tax credit, goods/services) by government?", "Benefit conferred (compared to market benchmark)?", "Specificity (de jure or de facto limited access)?", "If prohibited (Art.3): export contingent or import substitution", "If actionable: adverse effects on other Members (Art.5)?"],
        exceptions=["Art.8 non-actionable subsidies (expired but indicative): R&D, disadvantaged regions, environment (never implemented)", "De minimis: developing countries thresholds higher"],
        landmark_cases=["US - Softwood Lumber IV (DS257)", "EC - Large Civil Aircraft (DS316)", "US - Large Civil Aircraft (DS353)", "Brazil - Aircraft (DS46)"],
    ),
    _WTODiscipline(
        discipline_id="AD",
        name="Anti-Dumping",
        gatt_article="GATT Art.VI + AD Agreement",
        description="A product is dumped if its export price is less than normal value (price in exporter's domestic market or constructed value). Anti-dumping duty may be imposed if dumping causes material injury to domestic industry. Detailed procedural requirements for investigation.",
        key_tests=["Normal value determination (domestic price, third-country price, constructed value)", "Export price determination (transaction price or constructed)", "Dumping margin calculation (fair comparison, Art.2.4)", "Material injury to domestic industry (volume, price, impact)", "Causal link between dumping and injury (non-attribution Art.3.5)"],
        exceptions=["De minimis margin (<2%) or negligible import volume (<3%)", "Lesser duty rule (Art.9.1 - 'desirable')", "Sunset review: duty expires after 5 years unless review shows continuation likely"],
        landmark_cases=["EC - Bed Linen (DS141)", "US - Zeroing (EC) (DS294)", "US - Hot-Rolled Steel (DS184)", "Mexico - Anti-Dumping Measures on Rice (DS295)"],
    ),
]


class TradeComplianceChecker:
    """WTO compliance check against MFN, national treatment, TBT/SPS, subsidies disciplines."""

    def __init__(self) -> None:
        self._disciplines: list[_WTODiscipline] = list(_WTO_DISCIPLINES)
        self._index = DoctrineSearchIndex()
        self._build_index()
        logger.info("TradeComplianceChecker initialised with {} disciplines", len(self._disciplines))

    def _build_index(self) -> None:
        for d in self._disciplines:
            full_text = f"{d.name} {d.gatt_article} {d.description} {' '.join(d.key_tests)} {' '.join(d.exceptions)} {' '.join(d.landmark_cases)}"
            self._index.add_document(
                doc_id=d.discipline_id,
                title=d.name,
                text=full_text,
                category="wto_compliance",
                metadata={"gatt_article": d.gatt_article},
            )

    def check_compliance(self, measure_description: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Identify WTO disciplines potentially implicated by a trade measure."""
        results = self._index.search(measure_description, top_k=top_k)
        findings: list[dict[str, Any]] = []
        for r in results:
            disc = self._get_discipline(r.doc_id)
            if disc is None:
                continue
            findings.append({
                "discipline_id": disc.discipline_id,
                "name": disc.name,
                "gatt_article": disc.gatt_article,
                "relevance_score": r.score,
                "description": disc.description,
                "key_tests": disc.key_tests,
                "potential_exceptions": disc.exceptions,
                "landmark_cases": disc.landmark_cases,
            })
        return findings

    def _get_discipline(self, discipline_id: str) -> _WTODiscipline | None:
        for d in self._disciplines:
            if d.discipline_id == discipline_id:
                return d
        return None

    def analyze_tariff_measure(self, description: str, affected_countries: list[str] | None = None) -> dict[str, Any]:
        """Analyze a tariff measure for MFN and national treatment compliance."""
        mfn_risk = False
        nt_risk = False
        tariff_keywords = {"tariff", "duty", "customs", "import", "levy", "surcharge", "additional"}
        desc_lower = description.lower()
        tokens_set = set(desc_lower.split())

        if tariff_keywords & tokens_set:
            if affected_countries and len(affected_countries) < 164:
                mfn_risk = True
            if any(w in desc_lower for w in ("domestic", "local", "internal", "national")):
                nt_risk = True

        disciplines_triggered = self.check_compliance(description, top_k=3)

        return {
            "measure_description": description,
            "affected_countries": affected_countries or [],
            "mfn_risk": mfn_risk,
            "national_treatment_risk": nt_risk,
            "disciplines_implicated": disciplines_triggered,
            "recommendation": self._generate_recommendation(mfn_risk, nt_risk, disciplines_triggered),
            "analyzed_at": datetime.utcnow().isoformat(),
            "disclaimer": "This analysis identifies potential WTO compliance issues based on keyword and discipline matching. It is NOT a substitute for formal WTO legal analysis. Consult trade counsel.",
        }

    def _generate_recommendation(self, mfn_risk: bool, nt_risk: bool, disciplines: list[dict[str, Any]]) -> str:
        parts: list[str] = []
        if mfn_risk:
            parts.append("MFN risk detected: measure appears to discriminate among WTO Members. Verify Art.I compliance or ensure an applicable exception (Art.XXIV FTA, GSP Enabling Clause, or waiver).")
        if nt_risk:
            parts.append("National Treatment risk detected: measure may treat imported products less favourably than domestic like products. Verify Art.III compliance or applicable exception (Art.III:8, Art.XX).")
        if not mfn_risk and not nt_risk and not disciplines:
            parts.append("No immediate WTO compliance risks detected based on the description provided. Consider detailed legal review for non-obvious implications.")
        for d in disciplines:
            if d["discipline_id"] in ("TBT", "SPS", "SUBSIDIES", "AD"):
                parts.append(f"{d['name']} ({d['gatt_article']}) may be implicated (relevance: {d['relevance_score']:.2f}). Review key tests and exceptions.")
        return " ".join(parts) if parts else "Analysis inconclusive."

    def get_discipline_info(self, discipline_id: str) -> dict[str, Any] | None:
        disc = self._get_discipline(discipline_id)
        if disc is None:
            return None
        return {
            "discipline_id": disc.discipline_id,
            "name": disc.name,
            "gatt_article": disc.gatt_article,
            "description": disc.description,
            "key_tests": disc.key_tests,
            "exceptions": disc.exceptions,
            "landmark_cases": disc.landmark_cases,
        }

    def list_disciplines(self) -> list[dict[str, str]]:
        return [
            {"discipline_id": d.discipline_id, "name": d.name, "gatt_article": d.gatt_article}
            for d in self._disciplines
        ]
