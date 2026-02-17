"""
TX14 Crypto Tax Engine — Semantic Normalization Layer
Deterministic preprocessing for cryptocurrency and digital asset tax queries.

This module normalizes raw user queries into canonical terms that map to doctrine
cache topics. It handles the wild variation in crypto terminology — users might say
"ETH swap on Uniswap," "traded my Ethereum on a DEX," or "exchanged tokens via
decentralized protocol" and all must resolve to the same doctrine topic.

GOVERNANCE NOTICE:
    Semantic normalization is a deterministic preprocessing layer.
    No probabilistic models. No embeddings. No auto-learning.
    Every normalization rule is explicit and auditable.

Engine: TX14 Crypto Tax Intelligence Engine
Port: 8464
Author: ECHO OMEGA PRIME
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# ==============================================================================
# NORMALIZATION RESULT
# ==============================================================================

@dataclass
class NormalizationResult:
    """Output of the semantic normalization pipeline."""
    original_query: str
    normalized_query: str
    detected_topics: List[str]
    detected_entities: List[str]
    detected_assets: List[str]
    detected_actions: List[str]
    detected_forms: List[str]
    jurisdiction: str = "US"
    entity_type: Optional[str] = None
    tax_year: Optional[int] = None
    confidence: float = 1.0
    normalization_steps: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging and response inclusion."""
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "detected_topics": self.detected_topics,
            "detected_entities": self.detected_entities,
            "detected_assets": self.detected_assets,
            "detected_actions": self.detected_actions,
            "detected_forms": self.detected_forms,
            "jurisdiction": self.jurisdiction,
            "entity_type": self.entity_type,
            "tax_year": self.tax_year,
            "confidence": round(self.confidence, 3),
            "normalization_steps": self.normalization_steps,
        }


# ==============================================================================
# TERM NORMALIZATION MAPS
# ==============================================================================

# Crypto asset synonyms → canonical names
ASSET_SYNONYMS: Dict[str, str] = {
    "bitcoin": "BTC", "btc": "BTC", "satoshi": "BTC", "sats": "BTC",
    "ethereum": "ETH", "eth": "ETH", "ether": "ETH",
    "wrapped ethereum": "WETH", "weth": "WETH", "wrapped eth": "WETH",
    "wrapped bitcoin": "WBTC", "wbtc": "WBTC",
    "usdt": "USDT", "tether": "USDT",
    "usdc": "USDC", "usd coin": "USDC",
    "dai": "DAI", "makerdao dai": "DAI",
    "solana": "SOL", "sol": "SOL",
    "cardano": "ADA", "ada": "ADA",
    "polkadot": "DOT", "dot": "DOT",
    "avalanche": "AVAX", "avax": "AVAX",
    "polygon": "MATIC", "matic": "MATIC",
    "chainlink": "LINK", "link": "LINK",
    "uniswap": "UNI", "uni": "UNI",
    "aave": "AAVE",
    "compound": "COMP", "comp": "COMP",
    "dogecoin": "DOGE", "doge": "DOGE",
    "shiba inu": "SHIB", "shib": "SHIB",
    "ripple": "XRP", "xrp": "XRP",
    "litecoin": "LTC", "ltc": "LTC",
    "binance coin": "BNB", "bnb": "BNB",
    "stablecoin": "STABLECOIN", "stable coin": "STABLECOIN",
    "nft": "NFT", "non-fungible token": "NFT", "non fungible token": "NFT",
    "lp token": "LP_TOKEN", "liquidity provider token": "LP_TOKEN",
    "governance token": "GOV_TOKEN", "governance tokens": "GOV_TOKEN",
}

# Action synonyms → canonical actions
ACTION_SYNONYMS: Dict[str, str] = {
    "sell": "DISPOSE", "sold": "DISPOSE", "selling": "DISPOSE",
    "trade": "DISPOSE", "traded": "DISPOSE", "trading": "DISPOSE",
    "swap": "SWAP", "swapped": "SWAP", "swapping": "SWAP", "exchange": "SWAP",
    "exchanged": "SWAP", "convert": "SWAP", "converted": "SWAP",
    "buy": "ACQUIRE", "bought": "ACQUIRE", "purchase": "ACQUIRE",
    "purchased": "ACQUIRE", "acquire": "ACQUIRE", "acquired": "ACQUIRE",
    "mine": "MINE", "mined": "MINE", "mining": "MINE",
    "stake": "STAKE", "staked": "STAKE", "staking": "STAKE",
    "unstake": "UNSTAKE", "unstaked": "UNSTAKE", "unstaking": "UNSTAKE",
    "lend": "LEND", "lent": "LEND", "lending": "LEND",
    "borrow": "BORROW", "borrowed": "BORROW", "borrowing": "BORROW",
    "airdrop": "AIRDROP", "airdropped": "AIRDROP", "air drop": "AIRDROP",
    "fork": "FORK", "forked": "FORK", "hard fork": "HARD_FORK",
    "hard-fork": "HARD_FORK", "hardfork": "HARD_FORK",
    "wrap": "WRAP", "wrapped": "WRAP", "wrapping": "WRAP",
    "unwrap": "UNWRAP", "unwrapped": "UNWRAP", "unwrapping": "UNWRAP",
    "bridge": "BRIDGE", "bridged": "BRIDGE", "bridging": "BRIDGE",
    "farm": "YIELD_FARM", "farming": "YIELD_FARM", "yield farm": "YIELD_FARM",
    "yield farming": "YIELD_FARM",
    "provide liquidity": "PROVIDE_LIQUIDITY", "liquidity provision": "PROVIDE_LIQUIDITY",
    "add liquidity": "PROVIDE_LIQUIDITY", "LP": "PROVIDE_LIQUIDITY",
    "remove liquidity": "REMOVE_LIQUIDITY", "withdraw liquidity": "REMOVE_LIQUIDITY",
    "donate": "DONATE", "donated": "DONATE", "charitable": "DONATE",
    "gift": "GIFT", "gifted": "GIFT", "gifting": "GIFT",
    "lost": "LOST", "lose": "LOST", "stolen": "STOLEN", "hacked": "STOLEN",
    "hack": "STOLEN", "scam": "STOLEN", "rug pull": "STOLEN", "rugpull": "STOLEN",
    "receive": "RECEIVE", "received": "RECEIVE", "receiving": "RECEIVE",
    "transfer": "TRANSFER", "transferred": "TRANSFER", "send": "TRANSFER",
    "sent": "TRANSFER",
    "pay": "PAY", "paid": "PAY", "payment": "PAY",
    "ico": "ICO", "ido": "IDO", "token sale": "TOKEN_SALE",
    "margin": "MARGIN_TRADE", "margin trade": "MARGIN_TRADE",
    "leverage": "MARGIN_TRADE", "leveraged": "MARGIN_TRADE",
    "futures": "DERIVATIVES", "options": "DERIVATIVES", "perpetual": "DERIVATIVES",
    "perp": "DERIVATIVES", "derivative": "DERIVATIVES",
}

# Platform/protocol synonyms → canonical names
PLATFORM_SYNONYMS: Dict[str, str] = {
    "uniswap": "DEX", "sushiswap": "DEX", "pancakeswap": "DEX",
    "curve": "DEX", "balancer": "DEX", "1inch": "DEX_AGGREGATOR",
    "dex": "DEX", "decentralized exchange": "DEX",
    "coinbase": "CEX", "binance": "CEX", "kraken": "CEX",
    "gemini": "CEX", "ftx": "CEX", "crypto.com": "CEX",
    "cex": "CEX", "centralized exchange": "CEX",
    "metamask": "WALLET", "ledger": "HARDWARE_WALLET",
    "trezor": "HARDWARE_WALLET", "phantom": "WALLET",
    "aave": "DEFI_LENDING", "compound": "DEFI_LENDING",
    "maker": "DEFI_LENDING", "makerdao": "DEFI_LENDING",
    "opensea": "NFT_MARKETPLACE", "rarible": "NFT_MARKETPLACE",
    "looksrare": "NFT_MARKETPLACE", "blur": "NFT_MARKETPLACE",
    "dao": "DAO", "governance": "DAO",
}

# Form references
FORM_PATTERNS: Dict[str, str] = {
    r"form\s*8949": "Form 8949",
    r"8949": "Form 8949",
    r"schedule\s*d": "Schedule D",
    r"form\s*1040": "Form 1040",
    r"1040": "Form 1040",
    r"schedule\s*c": "Schedule C",
    r"schedule\s*se": "Schedule SE",
    r"form\s*8283": "Form 8283",
    r"form\s*8275": "Form 8275",
    r"fbar": "FinCEN 114 (FBAR)",
    r"fincen\s*114": "FinCEN 114 (FBAR)",
    r"form\s*8938": "Form 8938 (FATCA)",
    r"fatca": "Form 8938 (FATCA)",
    r"form\s*1099": "Form 1099",
    r"1099[\-\s]*da": "Form 1099-DA",
    r"1099[\-\s]*misc": "Form 1099-MISC",
    r"1099[\-\s]*b": "Form 1099-B",
    r"1099[\-\s]*k": "Form 1099-K",
    r"form\s*w[\-\s]*2": "Form W-2",
    r"form\s*1099[\-\s]*nec": "Form 1099-NEC",
    r"6050i": "IRC 6050I (Cash Reporting)",
}

# Topic detection patterns — map query patterns to doctrine topics
TOPIC_PATTERNS: List[Tuple[str, List[str]]] = [
    ("crypto_as_property", [r"property\s+treatment", r"notice\s*2014[\-\s]*21", r"virtual\s+currency\s+guidance",
                            r"crypto(?:currency)?\s+(?:is|as)\s+property", r"not\s+currency"]),
    ("cost_basis_methods", [r"cost\s+basis", r"fifo", r"lifo", r"specific\s+id", r"average\s+cost",
                            r"basis\s+method", r"basis\s+tracking", r"tax\s+lot"]),
    ("capital_gains_crypto", [r"capital\s+gain", r"capital\s+loss", r"long[\-\s]*term", r"short[\-\s]*term",
                              r"holding\s+period", r"netting\s+(?:gain|loss)", r"tax\s+rate\s+(?:on|for)\s+crypto"]),
    ("mining_income_taxation", [r"mining\s+(?:income|tax|reward)", r"block\s+reward", r"proof\s+of\s+work",
                                r"self[\-\s]*employment\s+(?:tax|income).*min", r"mining\s+pool"]),
    ("staking_rewards", [r"staking?\s+(?:reward|income|tax)", r"proof\s+of\s+stake", r"validator\s+reward",
                         r"jarrett", r"block\s+creation\s+theory", r"delegat(?:e|ion)\s+stak"]),
    ("defi_swap_taxation", [r"defi\s+(?:swap|trade|tax)", r"token\s+swap", r"dex\s+(?:swap|trade|tax)",
                            r"swap(?:ped|ping)?\s+(?:token|crypto)", r"decentralized\s+exchange\s+tax"]),
    ("liquidity_provision", [r"liquidity\s+(?:pool|provision|provider|mining)", r"(?:add|remove)\s+liquidity",
                             r"impermanent\s+loss", r"lp\s+token", r"amm\s+(?:tax|pool)"]),
    ("yield_farming", [r"yield\s+farm", r"farming\s+(?:reward|income|tax)", r"defi\s+yield",
                       r"compound(?:ing)?\s+(?:reward|position)"]),
    ("nft_taxation", [r"nft\s+tax", r"non[\-\s]*fungible\s+token\s+tax", r"nft\s+(?:sale|mint|create|buy|sell)",
                      r"digital\s+art\s+tax", r"nft\s+(?:creator|artist|investor)"]),
    ("nft_collectible_rate", [r"28\s*%\s*(?:rate|collectible)", r"collectible\s+(?:rate|tax)",
                              r"nft\s+collectible", r"nft\s+long[\-\s]*term\s+(?:capital\s+)?gain"]),
    ("wrapped_token_treatment", [r"wrapped?\s+(?:token|eth|btc)", r"weth\s+tax", r"eth\s+to\s+weth",
                                 r"wrapping\s+(?:token|crypto)", r"unwrap"]),
    ("cross_chain_bridge", [r"(?:cross[\-\s]*chain|bridge)\s+(?:transfer|tax|transaction)",
                            r"bridging?\s+(?:crypto|token|asset)", r"layer\s*2\s+(?:bridge|transfer)"]),
    ("crypto_lending", [r"(?:crypto|defi)\s+lend", r"(?:crypto|defi)\s+borrow", r"collateral\s+(?:crypto|post)",
                        r"interest\s+(?:income|earned).*crypto", r"cefi\s+lend"]),
    ("dao_token_taxation", [r"dao\s+(?:token|tax|governance)", r"governance\s+token\s+(?:tax|income)",
                            r"voting\s+(?:token|right)\s+tax", r"decentralized\s+autonomous\s+org"]),
    ("fbar_crypto", [r"fbar.*crypto", r"crypto.*fbar", r"foreign\s+(?:account|exchange).*crypto",
                     r"fincen\s+114", r"\$10[,\.]?000\s+threshold.*(?:crypto|exchange)"]),
    ("fatca_crypto", [r"fatca.*crypto", r"crypto.*fatca", r"form\s*8938.*crypto",
                      r"specified\s+foreign\s+financial\s+asset.*crypto"]),
    ("form_8949_reporting", [r"form\s*8949", r"8949\s+report", r"disposition\s+report",
                             r"report(?:ing)?\s+crypto\s+(?:sale|trade|gain|loss)"]),
    ("wash_sale_crypto", [r"wash\s+sale.*crypto", r"crypto.*wash\s+sale", r"(?:irc|section)\s*1091.*crypto",
                          r"repurchas(?:e|ing)\s+(?:after|within)\s+30\s+day"]),
    ("charitable_donation_crypto", [r"donat(?:e|ion|ing)\s+crypto", r"charitab(?:le|ly).*crypto",
                                    r"crypto.*charit", r"form\s*8283.*crypto", r"(?:irc|section)\s*170.*crypto"]),
    ("lost_stolen_crypto", [r"(?:lost|stolen|hacked|scam)\s+crypto", r"crypto\s+(?:theft|loss|hack|scam)",
                            r"casualty\s+loss.*crypto", r"(?:irc|section)\s*165.*crypto"]),
    ("broker_reporting_1099da", [r"1099[\-\s]*da", r"broker\s+report.*crypto", r"digital\s+asset\s+broker",
                                 r"iija\s*2021", r"infrastructure\s+(?:act|bill).*crypto"]),
    ("hard_fork_airdrop", [r"(?:hard|soft)\s+fork.*tax", r"airdrop.*(?:tax|income)", r"rev[\.\s]*rul[\.\s]*2019[\-\s]*24",
                           r"fork(?:ed)?\s+(?:coin|token).*tax"]),
    ("gas_fees_treatment", [r"gas\s+fee.*(?:tax|deduct|basis)", r"transaction\s+fee.*(?:tax|deduct|basis)",
                            r"ethereum\s+gas\s+(?:cost|fee)", r"network\s+fee.*(?:tax|basis)"]),
    ("token_generation_event", [r"(?:ico|ido|ieo)\s+(?:tax|participation)", r"token\s+(?:sale|launch|generation)",
                                r"(?:initial\s+coin|initial\s+dex)\s+offering\s+tax"]),
    ("crypto_ira_retirement", [r"crypto\s+ira", r"(?:bitcoin|crypto)\s+(?:401k|retirement|roth)",
                               r"self[\-\s]*directed\s+ira.*crypto"]),
    ("crypto_estate_planning", [r"(?:crypto|bitcoin)\s+(?:estate|inheritance|death)", r"step[\-\s]*up\s+basis.*crypto",
                                r"inherited\s+crypto", r"crypto\s+(?:will|trust|probate)"]),
    ("crypto_payroll", [r"(?:paid|salary|wages|compensation)\s+(?:in|with)\s+crypto",
                        r"crypto\s+(?:payroll|salary|wages|compensation)", r"employee\s+crypto"]),
    ("stablecoin_taxation", [r"stablecoin\s+(?:tax|gain|loss)", r"(?:usdt|usdc|dai)\s+(?:tax|gain|loss)",
                             r"stablecoin\s+(?:swap|conversion|interest)"]),
    ("crypto_derivatives", [r"(?:crypto|bitcoin)\s+(?:futures|options|derivative|perpetual)",
                            r"(?:perp|perpetual)\s+(?:swap|contract)\s+tax",
                            r"(?:section|irc)\s*1256.*crypto"]),
    ("crypto_margin_trading", [r"margin\s+(?:trad|call|interest).*crypto", r"crypto\s+(?:margin|leverage)",
                               r"leveraged\s+(?:trad|position).*crypto"]),
    ("crypto_trader_vs_investor", [r"trader\s+(?:vs|versus|or)\s+investor.*crypto",
                                   r"crypto\s+(?:trader|day\s+trad)", r"(?:section|irc)\s*475.*crypto",
                                   r"mark[\-\s]*to[\-\s]*market.*crypto"]),
    ("crypto_gift_tax", [r"gift(?:ing|ed)?\s+crypto", r"crypto\s+gift\s+(?:tax|exclusion)",
                         r"annual\s+exclusion.*crypto", r"form\s*709.*crypto"]),
    ("crypto_business_use", [r"business\s+(?:use|accept|payment).*crypto",
                             r"(?:accept|receiv)(?:ing|e)?\s+crypto\s+(?:payment|for\s+service)",
                             r"crypto\s+(?:for|as)\s+(?:business|payment)"]),
    ("crypto_penalties", [r"(?:penalty|penalties).*crypto", r"crypto.*(?:penalty|penalties)",
                          r"accuracy[\-\s]*related\s+penalty.*crypto", r"(?:irc|section)\s*6662.*crypto",
                          r"failure\s+to\s+(?:report|file).*crypto"]),
    ("crypto_information_reporting", [r"information\s+reporting.*crypto", r"crypto.*information\s+reporting",
                                      r"(?:irc|section)\s*6045.*crypto", r"broker\s+(?:definition|reporting).*crypto"]),
]


# ==============================================================================
# NORMALIZATION FUNCTIONS
# ==============================================================================

def _normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into single spaces."""
    return re.sub(r'\s+', ' ', text.strip())


def _detect_assets(query_lower: str) -> List[str]:
    """Detect cryptocurrency assets mentioned in the query."""
    detected: List[str] = []
    seen: Set[str] = set()
    for synonym, canonical in ASSET_SYNONYMS.items():
        if synonym in query_lower and canonical not in seen:
            detected.append(canonical)
            seen.add(canonical)
    return sorted(detected)


def _detect_actions(query_lower: str) -> List[str]:
    """Detect transaction actions mentioned in the query."""
    detected: List[str] = []
    seen: Set[str] = set()
    for synonym, canonical in ACTION_SYNONYMS.items():
        pattern = r'\b' + re.escape(synonym) + r'\b'
        if re.search(pattern, query_lower) and canonical not in seen:
            detected.append(canonical)
            seen.add(canonical)
    return sorted(detected)


def _detect_platforms(query_lower: str) -> List[str]:
    """Detect platforms/protocols mentioned in the query."""
    detected: List[str] = []
    seen: Set[str] = set()
    for synonym, canonical in PLATFORM_SYNONYMS.items():
        if synonym in query_lower and canonical not in seen:
            detected.append(canonical)
            seen.add(canonical)
    return sorted(detected)


def _detect_forms(query_lower: str) -> List[str]:
    """Detect IRS form references in the query."""
    detected: List[str] = []
    seen: Set[str] = set()
    for pattern, form_name in FORM_PATTERNS.items():
        if re.search(pattern, query_lower, re.IGNORECASE) and form_name not in seen:
            detected.append(form_name)
            seen.add(form_name)
    return sorted(detected)


def _detect_topics(query_lower: str) -> List[str]:
    """Match query against known doctrine topics using regex patterns."""
    matched: List[str] = []
    for topic, patterns in TOPIC_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                if topic not in matched:
                    matched.append(topic)
                break
    return matched


def _detect_tax_year(query: str) -> Optional[int]:
    """Extract tax year from query if mentioned."""
    year_match = re.search(r'(?:tax\s+year|for\s+year|in\s+)\s*(\d{4})', query, re.IGNORECASE)
    if year_match:
        year = int(year_match.group(1))
        if 2009 <= year <= 2030:
            return year
    standalone_year = re.search(r'\b(20[1-3]\d)\b', query)
    if standalone_year:
        year = int(standalone_year.group(1))
        if 2014 <= year <= 2030:
            return year
    return None


def _detect_entity_type(query_lower: str) -> Optional[str]:
    """Detect entity type from query context."""
    entity_patterns: Dict[str, List[str]] = {
        "individual": [r"\bindividual\b", r"\bpersonal\b", r"\bmy\s+(?:crypto|bitcoin|tax)", r"\bi\s+(?:sold|bought|mined|staked)"],
        "sole_proprietorship": [r"sole\s+prop", r"schedule\s*c\s+(?:for|report)", r"self[\-\s]*employ"],
        "partnership": [r"\bpartnership\b", r"\bform\s*1065\b", r"\bk[\-\s]*1\b"],
        "llc": [r"\bllc\b", r"limited\s+liability"],
        "s_corporation": [r"s[\-\s]*corp", r"\bform\s*1120[\-\s]*s\b"],
        "c_corporation": [r"c[\-\s]*corp", r"\bform\s*1120\b(?![\-\s]*s)"],
        "trust": [r"\btrust\b(?!\s*(?:wallet|less))", r"\bfiduciary\b", r"\bform\s*1041\b"],
        "estate": [r"\bestate\b(?!\s+plan)", r"\bdecedent\b"],
        "tax_exempt_organization": [r"tax[\-\s]*exempt", r"\b501[\(\s]*c\b", r"\bform\s*990\b"],
    }
    for entity_type, patterns in entity_patterns.items():
        for pattern in patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return entity_type
    return None


def _detect_jurisdiction(query_lower: str) -> str:
    """Detect jurisdiction from query — defaults to US federal."""
    state_patterns: Dict[str, str] = {
        "california": "US-CA", "new york": "US-NY", "texas": "US-TX",
        "florida": "US-FL", "wyoming": "US-WY", "colorado": "US-CO",
        "new jersey": "US-NJ", "washington": "US-WA", "illinois": "US-IL",
        "ohio": "US-OH", "georgia": "US-GA", "minnesota": "US-MN",
    }
    for state, code in state_patterns.items():
        if state in query_lower:
            return code
    international_patterns: Dict[str, str] = {
        "uk": "UK", "united kingdom": "UK", "canada": "CA",
        "australia": "AU", "germany": "DE", "japan": "JP",
        "singapore": "SG", "portugal": "PT", "el salvador": "SV",
    }
    for country, code in international_patterns.items():
        if country in query_lower:
            return code
    return "US"


def normalize_crypto_query(query: str) -> NormalizationResult:
    """Run the full semantic normalization pipeline on a crypto tax query.

    This is the main entry point for query preprocessing. It:
    1. Normalizes whitespace and case
    2. Detects mentioned crypto assets
    3. Detects transaction actions
    4. Detects relevant IRS forms
    5. Matches to doctrine topics
    6. Detects entity type and jurisdiction
    7. Extracts tax year if mentioned

    All operations are deterministic and auditable.
    """
    steps: List[str] = []
    normalized = _normalize_whitespace(query)
    steps.append("whitespace_normalized")

    query_lower = normalized.lower()

    assets = _detect_assets(query_lower)
    if assets:
        steps.append(f"assets_detected: {','.join(assets)}")

    actions = _detect_actions(query_lower)
    if actions:
        steps.append(f"actions_detected: {','.join(actions)}")

    platforms = _detect_platforms(query_lower)
    if platforms:
        steps.append(f"platforms_detected: {','.join(platforms)}")

    forms = _detect_forms(query_lower)
    if forms:
        steps.append(f"forms_detected: {','.join(forms)}")

    topics = _detect_topics(query_lower)
    if topics:
        steps.append(f"topics_matched: {','.join(topics)}")

    tax_year = _detect_tax_year(query)
    if tax_year:
        steps.append(f"tax_year_detected: {tax_year}")

    entity_type = _detect_entity_type(query_lower)
    if entity_type:
        steps.append(f"entity_type_detected: {entity_type}")

    jurisdiction = _detect_jurisdiction(query_lower)
    if jurisdiction != "US":
        steps.append(f"jurisdiction_detected: {jurisdiction}")

    entities = platforms  # Platform references serve as entity detections

    confidence = 1.0
    if not topics:
        confidence = 0.5
        steps.append("no_topic_match_confidence_reduced")
    elif len(topics) > 3:
        confidence = 0.85
        steps.append("multi_topic_confidence_reduced")

    logger.debug(f"Normalized query: {len(topics)} topics, {len(assets)} assets, {len(actions)} actions")

    return NormalizationResult(
        original_query=query,
        normalized_query=normalized,
        detected_topics=topics,
        detected_entities=entities,
        detected_assets=assets,
        detected_actions=actions,
        detected_forms=forms,
        jurisdiction=jurisdiction,
        entity_type=entity_type,
        tax_year=tax_year,
        confidence=confidence,
        normalization_steps=steps,
    )


def normalize_semantics(query: str) -> NormalizationResult:
    """Alias for normalize_crypto_query — matches TIE interface contract."""
    return normalize_crypto_query(query)


def compute_topic_relevance(norm_result: NormalizationResult, keywords: List[str]) -> float:
    """Compute relevance score between a normalization result and doctrine keywords.

    Deterministic keyword-overlap scoring. No ML, no embeddings.

    Args:
        norm_result: The normalized query result.
        keywords: Doctrine keyword list to match against.

    Returns:
        Float 0.0-1.0 relevance score.
    """
    if not keywords:
        return 0.0

    query_lower = norm_result.normalized_query.lower()
    query_tokens = set(query_lower.split())

    # Combine all detected signals into a match pool
    match_pool: Set[str] = set()
    match_pool.update(t.lower() for t in norm_result.detected_topics)
    match_pool.update(a.lower() for a in norm_result.detected_assets)
    match_pool.update(a.lower() for a in norm_result.detected_actions)
    match_pool.update(e.lower() for e in norm_result.detected_entities)
    match_pool.update(query_tokens)

    hits = 0
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in match_pool or kw_lower in query_lower:
            hits += 1

    return min(1.0, hits / len(keywords))


def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from a text string.

    Deterministic extraction — splits on whitespace and filters stopwords.

    Args:
        text: Input text to extract keywords from.

    Returns:
        List of lowercase keyword strings.
    """
    _STOPWORDS = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "and", "but", "or", "nor", "not", "so", "yet",
        "both", "either", "neither", "each", "every", "all", "any", "few",
        "more", "most", "other", "some", "such", "no", "only", "own", "same",
        "than", "too", "very", "just", "about", "above", "below", "between",
        "if", "then", "else", "when", "where", "how", "what", "which", "who",
        "whom", "this", "that", "these", "those", "i", "me", "my", "we", "our",
        "you", "your", "he", "him", "his", "she", "her", "it", "its", "they",
        "them", "their",
    }
    tokens = re.split(r"[\s,;:!?.()\[\]{}/]+", text.lower())
    return [t for t in tokens if t and len(t) > 1 and t not in _STOPWORDS]


def detect_question_type(query: str) -> str:
    """Detect the type of question being asked.

    Categories: compliance, planning, reporting, dispute, general.

    Args:
        query: Raw or normalized query string.

    Returns:
        Question type string.
    """
    q = query.lower()
    if any(w in q for w in ("report", "form", "file", "filing", "1099", "8949", "schedule")):
        return "reporting"
    if any(w in q for w in ("owe", "liable", "penalty", "compliance", "required", "must")):
        return "compliance"
    if any(w in q for w in ("plan", "strategy", "minimize", "optimize", "reduce", "avoid")):
        return "planning"
    if any(w in q for w in ("audit", "dispute", "appeal", "notice", "irs letter")):
        return "dispute"
    return "general"
