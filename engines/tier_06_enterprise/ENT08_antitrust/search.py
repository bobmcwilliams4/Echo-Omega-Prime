import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: int, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[Tuple[int, str], float] = {}
        self._re_token = re.compile(r'\b\w+\b')

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            for term in tf:
                self.doc_freqs[term] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()
            self.tf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, tf in self.term_freqs.items():
                if term in tf:
                    bm25_score = self._score_bm25(term, doc_id, idf)
                    doc_scores[doc_id] += bm25_score * self.documents[doc_id].weight
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self):
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avgdl,
                'vocab_size': len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._re_token.findall(text)]

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: int, idf: Optional[float] = None) -> float:
        cache_key = (doc_id, term)
        if cache_key in self.tf_cache:
            return self.tf_cache[cache_key]
        tf = self.term_freqs[doc_id][term]
        dl = self.doc_lengths[doc_id]
        avgdl = self.avgdl if self.avgdl > 0 else 1.0
        if idf is None:
            idf = self._compute_idf(term)
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * dl / avgdl)
        score = idf * numerator / denominator
        self.tf_cache[cache_key] = score
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = tokens[start:end]
        return ' '.join(snippet) + ('...' if end < len(tokens) else '')

    # TF-IDF scoring (normalized)
    def score_tfidf(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, tf in self.term_freqs.items():
                tf_norm = tf[term] / self.doc_lengths[doc_id] if self.doc_lengths[doc_id] > 0 else 0.0
                doc_scores[doc_id] += tf_norm * idf * self.documents[doc_id].weight
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

# Singleton factory for SearchIndex
_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Sherman Act Section 1 - Horizontal Price Fixing",
            "Horizontal price fixing is a per se violation of Section 1 of the Sherman Act. It occurs when competitors agree to raise, lower, or stabilize prices or price components. No elaborate analysis is required to show anticompetitive effect.",
            ["Sherman Act", "Section 1", "Price Fixing", "Per Se"],
            1.0
        ),
        SearchDocument(
            2,
            "Sherman Act Section 1 - Bid Rigging",
            "Bid rigging involves competitors conspiring to manipulate the bidding process, such as by rotating winning bids or agreeing on bid amounts. Like price fixing, it is treated as a per se illegal restraint of trade.",
            ["Sherman Act", "Section 1", "Bid Rigging", "Per Se"],
            1.0
        ),
        SearchDocument(
            3,
            "Sherman Act Section 1 - Market Allocation",
            "Market allocation agreements among competitors, dividing customers, territories, or products, are per se unlawful under Section 1. Such conduct eliminates competition in the allocated markets.",
            ["Sherman Act", "Section 1", "Market Allocation", "Per Se"],
            1.0
        ),
        SearchDocument(
            4,
            "Sherman Act Section 1 - Rule of Reason Framework",
            "The Rule of Reason applies to most Section 1 cases not subject to per se treatment. Courts evaluate the purpose, effects, and market context of the restraint to determine its reasonableness and competitive impact.",
            ["Sherman Act", "Section 1", "Rule of Reason"],
            1.0
        ),
        SearchDocument(
            5,
            "Sherman Act Section 2 - Monopolization Elements",
            "To prove monopolization under Section 2, the plaintiff must show (1) monopoly power in a relevant market and (2) willful acquisition or maintenance of that power, as distinguished from growth due to a superior product, business acumen, or historic accident.",
            ["Sherman Act", "Section 2", "Monopolization"],
            1.0
        ),
        SearchDocument(
            6,
            "Sherman Act Section 2 - Attempted Monopolization",
            "Attempted monopolization requires proof of (1) anticompetitive or exclusionary conduct, (2) specific intent to monopolize, and (3) a dangerous probability of achieving monopoly power in the relevant market.",
            ["Sherman Act", "Section 2", "Attempted Monopolization"],
            1.0
        ),
        SearchDocument(
            7,
            "Clayton Act Section 7 - Merger Analysis Framework",
            "Section 7 of the Clayton Act prohibits mergers and acquisitions where the effect may be substantially to lessen competition or tend to create a monopoly. Agencies analyze market definition, concentration, entry barriers, and competitive effects.",
            ["Clayton Act", "Section 7", "Merger", "Analysis"],
            1.0
        ),
        SearchDocument(
            8,
            "Vertical Merger Analysis - Foreclosure Concerns",
            "Vertical mergers are evaluated for their potential to foreclose rivals from key inputs or customers. Agencies assess whether the merged firm can and will restrict access in a way that harms competition.",
            ["Vertical Merger", "Foreclosure", "Clayton Act"],
            1.0
        ),
        SearchDocument(
            9,
            "Tying Arrangements - Jefferson Parish Test",
            "A tying arrangement involves conditioning the sale of one product on the purchase of another. Under Jefferson Parish, plaintiffs must show (1) two distinct products, (2) conditioning, (3) market power in the tying product, and (4) substantial commerce affected.",
            ["Tying", "Jefferson Parish", "Section 1"],
            1.0
        ),
        SearchDocument(
            10,
            "Exclusive Dealing - Anticompetitive Foreclosure Standard",
            "Exclusive dealing arrangements are evaluated under the rule of reason. The key concern is whether the arrangement forecloses a substantial share of the market to rivals and harms competition.",
            ["Exclusive Dealing", "Foreclosure", "Rule of Reason"],
            1.0
        ),
        SearchDocument(
            11,
            "Robinson-Patman Act - Price Discrimination",
            "The Robinson-Patman Act prohibits certain forms of price discrimination among competing purchasers where the effect may be to substantially lessen competition or tend to create a monopoly.",
            ["Robinson-Patman Act", "Price Discrimination"],
            1.0
        ),
        SearchDocument(
            12,
            "Resale Price Maintenance - Leegin Analysis",
            "Resale price maintenance (RPM) agreements are analyzed under the rule of reason after Leegin. Courts consider procompetitive justifications and actual or likely competitive effects.",
            ["Resale Price Maintenance", "Leegin", "Rule of Reason"],
            1.0
        ),
        SearchDocument(
            13,
            "State Action Immunity - Parker Doctrine",
            "The Parker Doctrine provides immunity from antitrust liability for anticompetitive conduct that is (1) clearly articulated and affirmatively expressed as state policy and (2) actively supervised by the state.",
            ["State Action Immunity", "Parker Doctrine"],
            1.0
        ),
        SearchDocument(
            14,
            "Noerr-Pennington Immunity - Petitioning Government",
            "The Noerr-Pennington doctrine immunizes genuine efforts to petition the government from antitrust liability, even if the outcome is anticompetitive. Sham petitioning is not protected.",
            ["Noerr-Pennington", "Immunity", "Petitioning"],
            1.0
        ),
        SearchDocument(
            15,
            "Market Definition - SSNIP Test and HHI",
            "Market definition often uses the SSNIP (Small but Significant and Non-transitory Increase in Price) test. Market concentration is measured by the Herfindahl-Hirschman Index (HHI).",
            ["Market Definition", "SSNIP", "HHI"],
            1.0
        ),
        SearchDocument(
            16,
            "Conscious Parallelism - Plus Factors for Agreement",
            "Conscious parallelism is not itself unlawful. Plaintiffs must show plus factors—evidence of agreement beyond mere parallel conduct—to establish a Section 1 violation.",
            ["Conscious Parallelism", "Plus Factors", "Section 1"],
            1.0
        ),
        SearchDocument(
            17,
            "Predatory Pricing - Brooke Group Standard",
            "Predatory pricing claims require proof that (1) prices were below an appropriate measure of cost and (2) the defendant had a dangerous probability of recouping the investment in below-cost prices.",
            ["Predatory Pricing", "Brooke Group", "Section 2"],
            1.0
        ),
        SearchDocument(
            18,
            "FTC Act Section 5 - Unfair Methods of Competition",
            "Section 5 of the FTC Act prohibits unfair methods of competition, which may include conduct not covered by the Sherman or Clayton Acts. The FTC has authority to define and enforce this standard.",
            ["FTC Act", "Section 5", "Unfair Competition"],
            1.0
        ),
        SearchDocument(
            19,
            "Joint Ventures - Rule of Reason and Integration Analysis",
            "Joint ventures among competitors are analyzed under the rule of reason. Courts assess whether the venture is a bona fide integration that enhances efficiency or a mere vehicle for collusion.",
            ["Joint Venture", "Rule of Reason", "Integration"],
            1.0
        ),
        SearchDocument(
            20,
            "Refusal to Deal - Aspen Skiing and Trinko Limits",
            "A monopolist's refusal to deal with rivals is generally lawful unless it sacrifices short-term profits to harm competition, as in Aspen Skiing. Trinko limits the scope of Section 2 liability for refusals to deal.",
            ["Refusal to Deal", "Aspen Skiing", "Trinko", "Section 2"],
            1.0
        ),
        SearchDocument(
            21,
            "Hart-Scott-Rodino Act - Merger Notification Thresholds",
            "The Hart-Scott-Rodino Act requires parties to certain mergers and acquisitions to file premerger notifications with the FTC and DOJ if the value exceeds specified thresholds.",
            ["Hart-Scott-Rodino", "Merger Notification", "Thresholds"],
            1.0
        ),
        SearchDocument(
            22,
            "2023 Merger Guidelines - Key Shifts and Presumptions",
            "The 2023 Merger Guidelines emphasize structural presumptions, lower HHI thresholds for concern, and greater scrutiny of serial acquisitions and labor market effects.",
            ["Merger Guidelines", "2023", "Presumptions"],
            1.0
        ),
        SearchDocument(
            23,
            "Sherman Act Section 1 - Ancillary Restraints Doctrine",
            "The ancillary restraints doctrine allows restraints that are subordinate and collateral to a legitimate transaction or collaboration, analyzed under the rule of reason.",
            ["Sherman Act", "Section 1", "Ancillary Restraints"],
            1.0
        ),
        SearchDocument(
            24,
            "Sherman Act Section 1 - Information Exchanges",
            "Information exchanges among competitors are not per se illegal but may violate Section 1 if they facilitate collusion or harm competition, depending on the nature and context of the exchange.",
            ["Sherman Act", "Section 1", "Information Exchange"],
            1.0
        ),
        SearchDocument(
            25,
            "Clayton Act Section 7 - Potential Competition Doctrine",
            "Potential competition doctrine considers whether a merger eliminates a firm that could have entered the market and increased competition, even if it was not an actual competitor.",
            ["Clayton Act", "Section 7", "Potential Competition"],
            1.0
        ),
        SearchDocument(
            26,
            "Sherman Act Section 2 - Essential Facilities Doctrine",
            "The essential facilities doctrine imposes a duty to deal when a monopolist controls a facility essential for competition and denial cannot be reasonably justified.",
            ["Sherman Act", "Section 2", "Essential Facilities"],
            1.0
        ),
        SearchDocument(
            27,
            "Vertical Restraints - Dual Distribution",
            "Dual distribution occurs when a supplier sells both directly to consumers and through independent distributors. Antitrust analysis considers the competitive effects and potential for collusion.",
            ["Vertical Restraints", "Dual Distribution"],
            1.0
        ),
        SearchDocument(
            28,
            "Merger Remedies - Structural and Behavioral",
            "Merger remedies may be structural (divestitures) or behavioral (conduct commitments). Agencies prefer structural remedies for their effectiveness and ease of monitoring.",
            ["Merger Remedies", "Structural", "Behavioral"],
            1.0
        ),
        SearchDocument(
            29,
            "Efficiencies Defense in Merger Review",
            "Merging parties may argue that efficiencies outweigh potential anticompetitive effects. Efficiencies must be merger-specific, verifiable, and likely to benefit consumers.",
            ["Merger", "Efficiencies", "Defense"],
            1.0
        ),
        SearchDocument(
            30,
            "Labor Markets in Antitrust Analysis",
            "Recent enforcement emphasizes labor market effects, including wage suppression and no-poach agreements. The 2023 Merger Guidelines highlight labor market concentration.",
            ["Labor Markets", "Antitrust", "Merger Guidelines"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)