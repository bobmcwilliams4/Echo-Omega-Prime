import math
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: str, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self._re_tokenize = re.compile(r'\w+')
    
    def add_document(self, doc: SearchDocument):
        if doc.id in self.documents:
            # Remove old frequencies
            old_doc = self.documents[doc.id]
            old_tokens = self._tokenize(old_doc.content)
            old_tf = Counter(old_tokens)
            for term in old_tf:
                self.doc_freqs[term] -= 1
                if self.doc_freqs[term] <= 0:
                    del self.doc_freqs[term]
                del self.term_freqs[term][doc.id]
                if not self.term_freqs[term]:
                    del self.term_freqs[term]
            self.N -= 1
            del self.doc_lengths[doc.id]
            del self.documents[doc.id]

        tokens = self._tokenize(doc.content)
        tf = Counter(tokens)
        self.documents[doc.id] = doc
        self.doc_lengths[doc.id] = len(tokens)
        self.N += 1
        for term in tf:
            if doc.id not in self.term_freqs[term]:
                self.doc_freqs[term] += 1
            self.term_freqs[term][doc.id] = tf[term]
        self._recalculate_avg_doc_length()
        self.idf_cache.clear()

    def _recalculate_avg_doc_length(self):
        if self.N == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N

    def _tokenize(self, text: str) -> List[str]:
        tokens = self._re_tokenize.findall(text.lower())
        return tokens

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

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            if doc_id not in self.term_freqs.get(term, {}):
                continue
            tf = self.term_freqs[term][doc_id]
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        # Apply document weight multiplier
        doc_weight = self.documents[doc_id].weight if doc_id in self.documents else 1.0
        return score * doc_weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_freqs.get(term, {}).keys())
        scored_docs: List[Tuple[str, float]] = []
        for doc_id in candidate_docs:
            score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scored_docs.append((doc_id, score))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        results: List[SearchResult] = []
        for doc_id, score in scored_docs[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + len(term)
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += "..."
            return snippet
        first_pos = min(positions)
        start_snip = max(0, first_pos - snippet_len // 4)
        end_snip = start_snip + snippet_len
        snippet = content[start_snip:end_snip].strip()
        if start_snip > 0:
            snippet = "..." + snippet
        if end_snip < len(content):
            snippet += "..."
        return snippet

    def get_stats(self) -> Dict[str, any]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "num_terms": len(self.doc_freqs),
        }

_singleton_index: Optional[SearchIndex] = None

def get_search_index() -> SearchIndex:
    global _singleton_index
    if _singleton_index is None:
        _singleton_index = SearchIndex()
        _preseed_documents(_singleton_index)
    return _singleton_index

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="doc001",
            title="Bloodline Origins and History",
            content=(
                "The origins of the bloodline trace back to ancient times, "
                "where lineage and heritage determined one's place in society. "
                "Understanding the history is crucial for authenticating bloodlines."
            ),
            tags=["history", "bloodline", "origin"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="doc002",
            title="Authentication Techniques for Bloodlines",
            content=(
                "Authentication of bloodlines involves genetic testing, "
                "historical record verification, and ritualistic practices. "
                "Each technique offers varying degrees of certainty."
            ),
            tags=["authentication", "techniques", "bloodline"],
            weight=1.5
        ),
        SearchDocument(
            doc_id="doc003",
            title="Genetic Markers in Bloodline Verification",
            content=(
                "Genetic markers such as SNPs and STRs provide a scientific basis "
                "for verifying bloodline authenticity. These markers are analyzed "
                "through DNA sequencing."
            ),
            tags=["genetics", "verification", "bloodline"],
            weight=1.4
        ),
        SearchDocument(
            doc_id="doc004",
            title="Rituals and Traditions in Bloodline Preservation",
            content=(
                "Many cultures preserve their bloodlines through rituals and traditions "
                "that reinforce lineage and heritage. These practices are symbolic "
                "and often legally recognized."
            ),
            tags=["rituals", "traditions", "preservation"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="doc005",
            title="Legal Implications of Bloodline Authentication",
            content=(
                "Bloodline authentication can have significant legal implications, "
                "especially in inheritance, citizenship, and tribal membership cases."
            ),
            tags=["legal", "implications", "bloodline"],
            weight=1.3
        ),
        SearchDocument(
            doc_id="doc006",
            title="Historical Records and Their Role in Bloodline Proof",
            content=(
                "Historical records such as birth certificates, marriage licenses, "
                "and census data are essential for establishing bloodline claims."
            ),
            tags=["historical", "records", "proof"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="doc007",
            title="Challenges in Bloodline Authentication",
            content=(
                "Challenges include incomplete records, genetic mutations, and "
                "forged documents that complicate the authentication process."
            ),
            tags=["challenges", "authentication", "bloodline"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="doc008",
            title="The Role of Anthropology in Bloodline Studies",
            content=(
                "Anthropology provides insights into human lineage and cultural "
                "heritage, aiding in the understanding of bloodline authenticity."
            ),
            tags=["anthropology", "studies", "bloodline"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="doc009",
            title="Modern Technologies in Bloodline Authentication",
            content=(
                "Technologies such as blockchain and biometric verification are "
                "emerging tools in the authentication of bloodlines."
            ),
            tags=["technology", "modern", "authentication"],
            weight=1.3
        ),
        SearchDocument(
            doc_id="doc010",
            title="Ethical Considerations in Bloodline Verification",
            content=(
                "Ethical issues arise regarding privacy, consent, and potential "
                "discrimination in bloodline verification processes."
            ),
            tags=["ethics", "considerations", "verification"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="doc011",
            title="Bloodline Authentication in Tribal Communities",
            content=(
                "Tribal communities often rely on oral histories and communal "
                "knowledge to authenticate bloodlines."
            ),
            tags=["tribal", "communities", "authentication"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="doc012",
            title="DNA Sequencing Methods for Lineage Analysis",
            content=(
                "Advanced DNA sequencing methods enable detailed lineage analysis "
                "and identification of ancestral origins."
            ),
            tags=["dna", "sequencing", "lineage"],
            weight=1.4
        ),
        SearchDocument(
            doc_id="doc013",
            title="Impact of Migration on Bloodline Integrity",
            content=(
                "Migration patterns can affect bloodline integrity by introducing "
                "new genetic variations and cultural influences."
            ),
            tags=["migration", "impact", "bloodline"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="doc014",
            title="Bloodline Authentication and Identity Verification",
            content=(
                "Bloodline authentication is a component of broader identity verification "
                "systems used in various institutions."
            ),
            tags=["identity", "verification", "bloodline"],
            weight=1.3
        ),
        SearchDocument(
            doc_id="doc015",
            title="Preserving Bloodline Records Digitally",
            content=(
                "Digital preservation of bloodline records ensures longevity and "
                "accessibility for future generations."
            ),
            tags=["digital", "preservation", "records"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="doc016",
            title="Bloodline Authentication in Royal Families",
            content=(
                "Royal families maintain meticulous records and employ strict "
                "authentication protocols to preserve their bloodlines."
            ),
            tags=["royal", "families", "authentication"],
            weight=1.4
        ),
        SearchDocument(
            doc_id="doc017",
            title="Forensic Applications of Bloodline Verification",
            content=(
                "Forensics uses bloodline verification to assist in criminal investigations "
                "and identification of remains."
            ),
            tags=["forensics", "applications", "verification"],
            weight=1.3
        ),
        SearchDocument(
            doc_id="doc018",
            title="Cultural Significance of Bloodlines",
            content=(
                "Bloodlines hold deep cultural significance, influencing social status, "
                "inheritance, and community roles."
            ),
            tags=["cultural", "significance", "bloodlines"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="doc019",
            title="Bloodline Authentication in Religious Contexts",
            content=(
                "Certain religions place importance on bloodline purity and use "
                "specific rituals for authentication."
            ),
            tags=["religion", "authentication", "bloodline"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="doc020",
            title="Statistical Models for Bloodline Analysis",
            content=(
                "Statistical models help predict and analyze bloodline relationships "
                "and inheritance patterns."
            ),
            tags=["statistical", "models", "bloodline"],
            weight=1.3
        ),
        SearchDocument(
            doc_id="doc021",
            title="Bloodline Authentication in Adoption Cases",
            content=(
                "Authentication can be critical in adoption cases to establish biological "
                "relationships."
            ),
            tags=["adoption", "authentication", "bloodline"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="doc022",
            title="Use of Blockchain for Bloodline Record Security",
            content=(
                "Blockchain technology offers secure and immutable storage for bloodline "
                "records."
            ),
            tags=["blockchain", "security", "records"],
            weight=1.3
        ),
        SearchDocument(
            doc_id="doc023",
            title="Bloodline Authentication and Privacy Laws",
            content=(
                "Privacy laws regulate the collection, storage, and use of bloodline "
                "authentication data."
            ),
            tags=["privacy", "laws", "authentication"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="doc024",
            title="Bloodline Authentication in Immigration Processes",
            content=(
                "Immigration authorities may require bloodline authentication for family "
                "reunification and citizenship."
            ),
            tags=["immigration", "authentication", "bloodline"],
            weight=1.3
        ),
        SearchDocument(
            doc_id="doc025",
            title="Future Trends in Bloodline Authentication",
            content=(
                "Emerging trends include AI-driven analysis, enhanced genetic testing, "
                "and global data sharing."
            ),
            tags=["future", "trends", "authentication"],
            weight=1.4
        ),
    ]
    for doc in docs:
        index.add_document(doc)