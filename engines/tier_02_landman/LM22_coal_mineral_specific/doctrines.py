"""
LM22 Coal/Mineral Specific — Doctrine Library
Pre-compiled expert reasoning blocks for coal, hard rock, and specialty mineral operations.

Each DoctrineBlock contains real domain expertise:
- topic: canonical doctrine identifier
- keywords: 5-8 trigger terms for cache matching
- conclusion_template: 3-5 sentence expert summary
- reasoning_framework: 20-40 lines of analytical steps
- key_factors: 5+ determinative elements
- primary_authority: 3-5 citations (statutes, cases, regulations)
- burden_holder: who bears proof burden
- adversary_position: opposing argument
- counter_arguments: 5+ rebuttal points
- resolution_strategy: path to resolution
- entity_scope: affected parties
- confidence: DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK
- controlling_precedent: lead case or statute

Author: ECHO OMEGA PRIME
Engine: LM22 Coal/Mineral Specific
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DoctrineBlock:
    """Single pre-compiled doctrine reasoning block."""
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
    entity_scope: List[str]
    confidence: str
    confidence_stratification: str
    controlling_precedent: str


# =============================================================================
# DOCTRINE BLOCK 1: SMCRA FEDERAL FRAMEWORK
# =============================================================================
SMCRA_FEDERAL_FRAMEWORK = DoctrineBlock(
    topic="smcra_federal_framework",
    keywords=["smcra", "surface mining", "reclamation", "osmre", "federal coal", "30 usc 1201", "coal regulation"],
    conclusion_template=(
        "The Surface Mining Control and Reclamation Act of 1977 (30 USC 1201-1328) establishes the "
        "comprehensive federal framework for regulating surface coal mining and reclamation. OSMRE "
        "administers the Act, but states with approved regulatory programs exercise primary enforcement "
        "authority (primacy). Operators must obtain permits demonstrating ability to reclaim mined land "
        "to approximate original contour and restore it to a condition capable of supporting prior uses "
        "or higher or better uses. Violations trigger cessation orders, civil penalties up to $5,000 "
        "per day, and potential criminal sanctions."
    ),
    reasoning_framework=(
        "Step 1: Determine whether the operation constitutes 'surface coal mining operations' under "
        "30 USC 1291(28) — includes surface mining, auger mining, and surface impacts of underground mining.\n"
        "Step 2: Identify the primacy state. If the state has an approved regulatory program under "
        "30 USC 1253, the state regulatory authority (SRA) is the primary regulator. If not, OSMRE "
        "regulates directly under a federal program (30 USC 1254).\n"
        "Step 3: Evaluate permit requirements under 30 USC 1256-1260. The permit application must include "
        "a mining and reclamation plan, hydrologic assessment, blasting plan, and proof of insurance.\n"
        "Step 4: Assess performance standards under 30 USC 1265 (surface mining) or 1266 (underground). "
        "Key standards: approximate original contour restoration, topsoil preservation, hydrologic "
        "protection, and revegetation with native species.\n"
        "Step 5: Evaluate bonding adequacy under 30 USC 1259. Performance bond must be sufficient to "
        "cover complete reclamation by a third party if the operator defaults.\n"
        "Step 6: Check for prohibited operations — lands unsuitable for mining (30 USC 1272), including "
        "national parks, wildlife refuges, historic sites, and alluvial valley floors in arid regions.\n"
        "Step 7: Assess enforcement exposure — pattern of violations triggers permit revocation, "
        "and corporate officers face personal liability under the 'permit block' provision.\n"
        "Step 8: Consider interaction with NEPA — federal permits require environmental assessment or "
        "environmental impact statement depending on scope of disturbance."
    ),
    key_factors=[
        "Whether the state has primacy (approved regulatory program)",
        "Acreage of proposed disturbance and proximity to protected areas",
        "Adequacy of reclamation bond amount relative to estimated reclamation costs",
        "Operator compliance history and applicant violator system (AVS) status",
        "Hydrologic impact assessment and acid mine drainage potential",
        "Presence of alluvial valley floors, endangered species habitat, or cultural resources",
        "Whether operation triggers 'valid existing rights' (VER) analysis on protected lands"
    ],
    primary_authority=[
        "30 USC 1201-1328 (Surface Mining Control and Reclamation Act)",
        "30 CFR Parts 700-955 (OSMRE implementing regulations)",
        "Hodel v. Virginia Surface Mining & Reclamation Assn., 452 U.S. 264 (1981)",
        "30 USC 1253 (State primacy programs)",
        "30 USC 1259 (Performance bonds and deposit requirements)"
    ],
    burden_holder="Permit applicant bears burden to demonstrate compliance capability",
    adversary_position=(
        "Surface owners and environmental groups argue that SMCRA performance standards "
        "are inadequate to prevent long-term environmental damage, particularly regarding "
        "acid mine drainage, mountaintop removal impacts, and stream buffer zone violations."
    ),
    counter_arguments=[
        "SMCRA explicitly preempts less stringent state regulation under 30 USC 1255",
        "Approximate original contour requirement has been upheld as constitutional under Commerce Clause",
        "Bonding requirements have been strengthened through pool mechanisms for operators unable to obtain surety bonds",
        "OSMRE oversight inspections supplement state enforcement where primacy states underperform",
        "Citizen suit provisions (30 USC 1270) provide independent enforcement mechanism",
        "Permit block system prevents operators with outstanding violations from obtaining new permits"
    ],
    resolution_strategy=(
        "Secure primacy state permit with comprehensive reclamation plan. Ensure bond covers "
        "full third-party reclamation cost. Clear AVS system of any outstanding violations before "
        "applying. Engage OSMRE early if federal lands or oversight issues are anticipated."
    ),
    entity_scope=["coal mining operators", "surface owners", "OSMRE", "state regulatory authorities", "surety companies"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — well-established federal framework with extensive case law",
    controlling_precedent="Hodel v. Virginia Surface Mining & Reclamation Assn., 452 U.S. 264 (1981)"
)

# =============================================================================
# DOCTRINE BLOCK 2: STATE PRIMACY PROGRAMS
# =============================================================================
STATE_PRIMACY_PROGRAMS = DoctrineBlock(
    topic="state_primacy_coal_programs",
    keywords=["primacy", "state program", "approved program", "sra", "state coal regulation", "delegation", "cooperative federalism"],
    conclusion_template=(
        "Under SMCRA Section 503 (30 USC 1253), states may assume primary regulatory authority "
        "(primacy) for surface coal mining by submitting a program that is at least as effective as "
        "the federal program. Currently 24 states have approved primacy programs. OSMRE retains "
        "oversight authority and may intervene through federal inspections or partial program "
        "substitution. State programs must be at least as stringent as federal standards but may "
        "impose more protective requirements."
    ),
    reasoning_framework=(
        "Step 1: Identify whether the relevant state has an approved primacy program. "
        "Major coal states with primacy: WV, KY, PA, VA, WY, MT, CO, IL, IN, OH, AL, TX.\n"
        "Step 2: Compare state performance standards with federal minimums under 30 CFR 816/817. "
        "States cannot be less stringent but may be more protective.\n"
        "Step 3: Evaluate whether OSMRE has issued ten-day notices (TDNs) to the state for "
        "enforcement deficiencies — indicates potential federal intervention.\n"
        "Step 4: Check state-specific bonding requirements. Some states use conventional surety "
        "bonds; others have alternative bonding systems (pool bonds, self-bonding).\n"
        "Step 5: Assess state permit processing timelines — varies from 6 months (WY) to 18+ months (WV).\n"
        "Step 6: Determine fee structures — annual permit fees, per-acre reclamation fees, "
        "and abandoned mine land (AML) fees vary by state.\n"
        "Step 7: Review state citizen participation requirements — some states provide more "
        "expansive intervention rights than federal minimum."
    ),
    key_factors=[
        "Whether state has approved primacy program under 30 USC 1253",
        "State bonding system type (conventional, pool, self-bond, combination)",
        "State enforcement track record and OSMRE oversight evaluations",
        "State-specific permit processing timeline and backlog",
        "Whether state has supplemental environmental review requirements beyond SMCRA",
        "State reclamation fee rates and abandoned mine land fund status"
    ],
    primary_authority=[
        "30 USC 1253 (State program approval)",
        "30 USC 1254 (Federal programs for non-primacy states)",
        "30 USC 1271 (Federal enforcement in primacy states)",
        "30 CFR Part 732 (Criteria for state program approval)",
        "Bragg v. West Virginia Coal Assn., 248 F.3d 275 (4th Cir. 2001)"
    ],
    burden_holder="State bears burden to demonstrate program is at least as effective as federal program",
    adversary_position=(
        "Critics argue state primacy creates a 'race to the bottom' where coal-dependent states "
        "under-enforce to attract mining investment. OSMRE oversight has been characterized as "
        "insufficient, with ten-day notice provisions rarely resulting in federal takeover."
    ),
    counter_arguments=[
        "OSMRE annual oversight reports provide accountability mechanism",
        "Federal inspection authority under 30 USC 1267 supplements state enforcement",
        "Citizen suit provisions operate independently of state enforcement decisions",
        "Several states (PA, WV) have adopted standards exceeding federal minimums",
        "OSMRE can substitute federal enforcement for specific areas if state program fails",
        "State primacy preserves local expertise and responsiveness to regional conditions"
    ],
    resolution_strategy=(
        "Work with state regulatory authority as primary contact. Monitor OSMRE oversight "
        "evaluations for the state. Ensure compliance with both state and any supplemental "
        "federal requirements. Maintain awareness of state-specific bonding and fee structures."
    ),
    entity_scope=["state regulatory authorities", "OSMRE", "coal operators", "citizen intervenors"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — cooperative federalism framework well-established",
    controlling_precedent="Bragg v. West Virginia Coal Assn., 248 F.3d 275 (4th Cir. 2001)"
)

# =============================================================================
# DOCTRINE BLOCK 3: BROAD FORM DEED INTERPRETATION
# =============================================================================
BROAD_FORM_DEED = DoctrineBlock(
    topic="broad_form_deed_interpretation",
    keywords=["broad form deed", "mineral estate", "surface estate", "dominant estate", "implied rights", "mineral severance", "surface destruction"],
    conclusion_template=(
        "Broad form deeds historically granted mineral owners expansive rights to use the surface "
        "for extraction, often with minimal or no compensation to surface owners. The legal landscape "
        "shifted dramatically when Kentucky adopted a constitutional amendment in 1988 requiring surface "
        "owner consent for surface mining under broad form deeds. Many Appalachian states now apply a "
        "'reasonable use' or 'accommodation' doctrine rather than the 'broad form deed' doctrine that "
        "gave mineral owners virtually unlimited surface rights. The critical inquiry is whether the "
        "deed language, the extraction method contemplated at the time of severance, and the applicable "
        "state doctrine permit the specific mining method proposed."
    ),
    reasoning_framework=(
        "Step 1: Examine the deed language verbatim. Broad form deeds typically convey 'all coal and "
        "minerals' with 'the right to mine and remove the same by any and all methods.' Determine "
        "the specific conveyance language and any express limitations.\n"
        "Step 2: Identify the date of mineral severance. Courts often distinguish between severances "
        "before and after the advent of surface mining technology. If the deed predates strip mining, "
        "a 'contemplation of the parties' analysis may limit implied surface rights.\n"
        "Step 3: Apply the relevant state doctrine:\n"
        "  - Kentucky: Post-1988 amendment, surface owner consent required for surface mining under "
        "    broad form deeds (Ky. Const. § 19(2)).\n"
        "  - West Virginia: Applies 'reasonable use' doctrine (Buffalo Mining Co. v. Martin).\n"
        "  - Virginia: Still applies 'broad form deed' doctrine giving mineral owner extensive rights.\n"
        "  - Pennsylvania: Accommodation doctrine applies (Penn Coal v. Mahon context).\n"
        "Step 4: Evaluate whether the proposed extraction method was 'contemplated' at the time of "
        "severance. Surface mining methods not contemplated at the time of an 1880s severance may "
        "not be authorized by general 'right to mine' language.\n"
        "Step 5: Assess surface damage provisions — some deeds require compensation for surface "
        "damage, others waive surface owner rights entirely.\n"
        "Step 6: Check for statutory modifications — several states have enacted surface owner "
        "protection statutes that modify common law interpretations of mineral deeds."
    ),
    key_factors=[
        "Exact deed language — express vs implied surface use rights",
        "Date of mineral severance and mining technology available at that time",
        "Applicable state doctrine (broad form, reasonable use, accommodation)",
        "Whether proposed extraction method was contemplated at time of severance",
        "Presence of express surface damage waiver or compensation provisions",
        "Statutory modifications to common law mineral estate rights",
        "Whether deed conveys 'all minerals' or specifies particular minerals"
    ],
    primary_authority=[
        "Ky. Const. § 19(2) (1988 amendment — broad form deed reform)",
        "Ward v. Harding, 860 S.W.2d 280 (Ky. 1993)",
        "Buffalo Mining Co. v. Martin, 165 W.Va. 10 (1980)",
        "Pennsylvania Coal Co. v. Mahon, 260 U.S. 393 (1922)",
        "Willms v. Hess, 383 S.E.2d 75 (W.Va. 1989)"
    ],
    burden_holder="Mineral owner bears burden to prove right to specific extraction method if challenged",
    adversary_position=(
        "Surface owners argue that broad form deeds are unconscionable relics of an era when "
        "surface mining was unknown, and that the mineral owner's implied rights should not extend "
        "to total surface destruction methods not contemplated by the original grantor."
    ),
    counter_arguments=[
        "Express language granting 'all methods' of extraction has been upheld in Virginia",
        "Mineral estate traditionally dominant under common law — surface estate is servient",
        "Retroactive application of surface owner consent requirements raises takings concerns",
        "Kentucky amendment applies only prospectively to mining operations, not to deed construction",
        "Accommodation doctrine balances interests without eliminating mineral estate value",
        "Modern severance deeds typically include explicit surface use provisions, mooting the issue"
    ],
    resolution_strategy=(
        "Obtain complete chain of title back to original severance deed. Analyze exact grant language. "
        "Apply correct state doctrine. If broad form deed state, verify whether statutory reform "
        "applies. If contemplation analysis required, engage mining historian to establish extraction "
        "methods known at date of severance. Negotiate surface use agreement where possible."
    ),
    entity_scope=["mineral estate owners", "surface estate owners", "coal operators", "title examiners"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE — state-by-state variation creates uncertainty; outcome depends heavily on jurisdiction and deed language",
    controlling_precedent="Ward v. Harding, 860 S.W.2d 280 (Ky. 1993)"
)

# =============================================================================
# DOCTRINE BLOCK 4: COAL BED METHANE OWNERSHIP
# =============================================================================
CBM_OWNERSHIP = DoctrineBlock(
    topic="coal_bed_methane_ownership",
    keywords=["cbm", "coal bed methane", "coalbed methane", "coal seam gas", "methane ownership", "gas in coal", "cbm rights"],
    conclusion_template=(
        "Coal bed methane (CBM) ownership disputes arise from the split nature of subsurface estates "
        "— the coal estate and the oil/gas estate often have different owners. The critical question "
        "is whether CBM is owned by the coal estate owner (as gas within the coal) or the oil/gas "
        "estate owner (as a hydrocarbon gas). The U.S. Supreme Court in Amoco Production Co. v. "
        "Southern Ute Indian Tribe (1999) held that CBM is part of the gas estate, not the coal "
        "estate, for federal reservations. State courts have reached varying conclusions, with "
        "Virginia, West Virginia, Pennsylvania, and Wyoming each applying different analytical "
        "frameworks."
    ),
    reasoning_framework=(
        "Step 1: Identify the severance deed or reservation language. Does it convey 'coal,' "
        "'oil and gas,' 'all minerals,' or specific mineral categories?\n"
        "Step 2: Determine whether the deed predates commercial CBM production. If so, apply "
        "the 'contemplation of the parties' test — was CBM a known, commercially recoverable "
        "resource at the time of severance?\n"
        "Step 3: Apply jurisdiction-specific precedent:\n"
        "  - Federal: Amoco v. Southern Ute — CBM is gas, not coal (for federal coal reservations).\n"
        "  - Virginia: CONSOL Energy v. Virginia Crews — generally follows Amoco rationale.\n"
        "  - West Virginia: Continental Resources v. Howard — CBM presumed part of gas estate.\n"
        "  - Pennsylvania: US Steel Mining v. Hoge — CBM owned by coal estate while in coal seam.\n"
        "  - Wyoming: Newman v. RAG Wyoming — CBM is gas for purposes of oil/gas lease.\n"
        "Step 4: Evaluate whether the coal owner or gas owner has the superior right to extract "
        "CBM. Even if gas owner owns CBM, coal owner may have right to vent methane for mine "
        "safety (mine degasification) without paying royalties.\n"
        "Step 5: Assess operational conflicts — CBM extraction may interfere with coal mining "
        "operations and vice versa. Evaluate duty to accommodate and potential damages.\n"
        "Step 6: Check for statutory frameworks — some states (WV, VA) have enacted CBM pooling "
        "and force-pooling statutes to resolve ownership disputes."
    ),
    key_factors=[
        "Exact deed language conveying 'coal' vs 'oil and gas' vs 'all minerals'",
        "Date of severance relative to commercial CBM development (~1980s)",
        "Jurisdiction-specific case law on CBM characterization",
        "Whether CBM is still adsorbed in coal seam or has migrated to conventional reservoir",
        "Mine safety degasification rights of coal operator",
        "Existence of state CBM pooling or force-pooling statutes",
        "Federal vs state land ownership affecting applicable precedent"
    ],
    primary_authority=[
        "Amoco Production Co. v. Southern Ute Indian Tribe, 526 U.S. 865 (1999)",
        "US Steel Mining Co. v. Hoge, 468 A.2d 1380 (Pa. 1983)",
        "Continental Resources of Illinois v. Howard, 218 W.Va. 313 (2005)",
        "CONSOL Energy Inc. v. Virginia Crews, 285 Va. 131 (2013)",
        "Newman v. RAG Wyoming Land Co., 53 P.3d 540 (Wyo. 2002)"
    ],
    burden_holder="Claimant asserting CBM ownership bears burden of proof under deed construction",
    adversary_position=(
        "Coal estate owners argue CBM is integral to the coal and was never separately "
        "severed. They contend CBM exists only because of the coal seam and should be an "
        "incident of coal ownership, particularly where the gas has commercial value only "
        "because it can be extracted from coal."
    ),
    counter_arguments=[
        "Amoco establishes federal default that CBM is gas, not coal",
        "CBM is chemically identical to conventional natural gas (methane CH4)",
        "Commercial CBM extraction postdates most severance deeds — parties could not have contemplated it",
        "Coal operators may vent methane for safety without owning it commercially",
        "State force-pooling statutes resolve ownership disputes without relitigating deed construction",
        "Modern severance deeds now routinely address CBM ownership explicitly"
    ],
    resolution_strategy=(
        "Examine severance deed for explicit CBM provisions. If silent, apply jurisdiction-specific "
        "precedent. If on federal land, Amoco controls. Advise parties to negotiate CBM development "
        "agreement addressing extraction sequencing, ventilation rights, and royalty sharing. "
        "If dispute irresolvable, evaluate state force-pooling mechanisms."
    ),
    entity_scope=["coal estate owners", "oil/gas estate owners", "CBM operators", "surface owners"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE — jurisdiction-dependent; Amoco provides federal baseline but state courts diverge",
    controlling_precedent="Amoco Production Co. v. Southern Ute Indian Tribe, 526 U.S. 865 (1999)"
)

# =============================================================================
# DOCTRINE BLOCK 5: GENERAL MINING LAW OF 1872
# =============================================================================
GENERAL_MINING_LAW_1872 = DoctrineBlock(
    topic="general_mining_law_1872",
    keywords=["mining law 1872", "hard rock mining", "unpatented claims", "30 usc 22", "locatable minerals", "discovery", "open public lands"],
    conclusion_template=(
        "The General Mining Law of 1872 (30 USC 22-54) remains the foundational framework for "
        "locating and developing hardrock mineral deposits on federal public lands. Citizens may "
        "locate mining claims on open public domain lands by discovering a valuable mineral deposit "
        "and marking and recording the claim. Locatable minerals include gold, silver, copper, lead, "
        "zinc, uranium, and most metallic and certain nonmetallic minerals not subject to the Mineral "
        "Leasing Act. Despite periodic reform proposals, the 1872 Act remains in force with no "
        "federal royalty on hardrock production from public lands, making it one of the most "
        "favorable mineral development frameworks in the world."
    ),
    reasoning_framework=(
        "Step 1: Confirm the land is open to mineral entry. Public domain lands managed by BLM or "
        "USFS are generally open unless withdrawn. Check for mineral withdrawals, wilderness "
        "designations, military reservations, or other segregations.\n"
        "Step 2: Determine if the mineral is 'locatable' — metallic minerals (gold, silver, copper, "
        "lead, zinc, uranium) and certain nonmetallic minerals not covered by the Mineral Leasing "
        "Act (coal, oil, gas, phosphate, sodium, potassium, sulfur are NOT locatable).\n"
        "Step 3: Evaluate the 'discovery' requirement. A valuable mineral deposit must be discovered "
        "within the claim boundaries. The 'prudent man' test (Castle v. Womble) asks whether a "
        "person of ordinary prudence would be justified in further expenditure with a reasonable "
        "prospect of success.\n"
        "Step 4: Verify claim type:\n"
        "  - Lode claim: For minerals in veins or lodes (rock in place). Max 1,500 ft × 600 ft.\n"
        "  - Placer claim: For minerals in loose, unconsolidated material. Max 20 acres per locator.\n"
        "  - Mill site: Up to 5 acres for processing facilities, no mineral discovery required.\n"
        "  - Tunnel site: Right to develop veins discovered by tunnel on public land.\n"
        "Step 5: Confirm recording and maintenance. Claims must be recorded with county and BLM. "
        "Annual maintenance fees ($165/claim) or assessment work ($100/claim) required to maintain.\n"
        "Step 6: Evaluate patent eligibility — $2.50/acre (placer) or $5.00/acre (lode) for fee "
        "simple patent. Congressional moratorium on patent processing since 1994.\n"
        "Step 7: Assess surface management requirements under 43 CFR 3809 — plan of operations "
        "required for disturbance >5 acres or >1,000 tons of material."
    ),
    key_factors=[
        "Whether land is open to mineral entry (not withdrawn or segregated)",
        "Whether mineral is 'locatable' (not subject to Mineral Leasing Act)",
        "Validity of discovery under prudent man test",
        "Proper claim type selection (lode vs placer vs mill site)",
        "Timely recording with county and BLM",
        "Annual maintenance fee payment or assessment work completion",
        "Surface management compliance under 43 CFR 3809"
    ],
    primary_authority=[
        "30 USC 22-54 (General Mining Law of 1872)",
        "43 CFR Part 3800 (BLM mining claims regulations)",
        "Castle v. Womble, 19 L.D. 455 (1894) — prudent man discovery test",
        "United States v. Coleman, 390 U.S. 599 (1968) — marketability test",
        "Andrus v. Shell Oil Co., 446 U.S. 657 (1980)"
    ],
    burden_holder="Mining claimant bears burden to prove valid discovery and compliance",
    adversary_position=(
        "Environmental groups and reform advocates argue the 1872 Mining Law is an anachronistic "
        "giveaway of public resources, allowing mining without royalties and inadequate environmental "
        "protection. They seek imposition of federal royalties, stricter reclamation standards, and "
        "authority to withdraw more lands from mineral entry."
    ),
    counter_arguments=[
        "1872 Act has survived 150+ years of reform attempts, demonstrating congressional intent",
        "No federal royalty incentivizes domestic mineral production critical for national security",
        "State environmental laws (NEPA, Clean Water Act, etc.) provide substantial environmental protection",
        "BLM surface management regulations (43 CFR 3809) require financial guarantees for reclamation",
        "Patent moratorium since 1994 effectively blocks fee-simple transfers",
        "Annual maintenance fees ($165/claim) replaced or supplemented assessment work requirement"
    ],
    resolution_strategy=(
        "Verify land status through BLM LR2000 system. Conduct geological assessment to confirm "
        "discovery. Locate and record claims properly with county and BLM. Pay annual maintenance "
        "fees timely. Submit notice-level (≤5 acres) or plan-level (>5 acres) surface management "
        "plan. Engage with NEPA process for plan-level operations."
    ),
    entity_scope=["mining claimants", "BLM", "USFS", "surface management agencies"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — well-settled statutory framework with extensive administrative precedent",
    controlling_precedent="Castle v. Womble, 19 L.D. 455 (1894)"
)

# =============================================================================
# DOCTRINE BLOCK 6: LODE VS PLACER CLAIMS
# =============================================================================
LODE_VS_PLACER_CLAIMS = DoctrineBlock(
    topic="lode_vs_placer_claims",
    keywords=["lode claim", "placer claim", "vein", "rock in place", "alluvial", "detrital", "mineral deposit type"],
    conclusion_template=(
        "The distinction between lode and placer claims is fundamental to the 1872 Mining Law. "
        "Lode claims cover minerals found in veins, lodes, or ledges within rock in place — i.e., "
        "mineralized material in its original geological position. Placer claims cover all deposits "
        "not in rock in place, including alluvial, detrital, eluvial, and certain disseminated "
        "deposits. The distinction affects claim dimensions, patent price, annual maintenance, and "
        "locator rights. Misclassification can void the claim entirely."
    ),
    reasoning_framework=(
        "Step 1: Examine the geological character of the deposit. Is the mineral in a defined vein, "
        "lode, or ledge within competent rock? If yes, lode claim. Is the mineral in loose, "
        "unconsolidated, or decomposed material? If yes, placer claim.\n"
        "Step 2: Apply the 'rock in place' test. Minerals in their original geological formation are "
        "lode. Minerals that have been eroded, transported, or weathered from their source are placer.\n"
        "Step 3: Consider edge cases — disseminated mineral deposits (porphyry copper, disseminated "
        "gold) are generally lode claims because the mineral is within rock in place, even though "
        "not in a defined vein structure.\n"
        "Step 4: Verify claim dimensions:\n"
        "  - Lode: Max 1,500 ft along the vein × 600 ft (300 ft each side of vein centerline).\n"
        "  - Placer: Max 20 acres per individual locator; 160 acres for association (8 persons).\n"
        "Step 5: Assess extralateral rights — lode claimants have the right to follow a vein on its "
        "dip beyond the claim's vertical side boundaries (extralateral rights). Placer claimants "
        "have NO extralateral rights.\n"
        "Step 6: Verify patent pricing — lode: $5.00/acre; placer: $2.50/acre (though patent "
        "processing is under congressional moratorium)."
    ),
    key_factors=[
        "Geological character — vein/lode in rock in place vs unconsolidated deposit",
        "Whether deposit has been transported from its original formation",
        "Disseminated vs vein-type mineralization",
        "Claim dimensions relative to deposit type",
        "Whether extralateral rights are needed to follow the vein on its dip",
        "Correct classification to avoid claim invalidity"
    ],
    primary_authority=[
        "30 USC 23 (Lode claims — veins or lodes of quartz or other rock in place)",
        "30 USC 35 (Placer claims — other forms of deposit)",
        "Webb v. American Asphaltum Mining Co., 157 F. 203 (8th Cir. 1907)",
        "Titanium Actynite Industries v. McLane, 12 IBLA 195 (1973)",
        "Iron Silver Mining Co. v. Cheesman, 116 U.S. 529 (1886)"
    ],
    burden_holder="Claimant bears burden to correctly classify and locate the appropriate claim type",
    adversary_position=(
        "Competing claimants or BLM may challenge classification as a means to invalidate claims. "
        "A lode claim located on a placer deposit (or vice versa) is void ab initio."
    ),
    counter_arguments=[
        "Disseminated deposits in rock in place are validly located as lode claims",
        "Dual location (both lode and placer) is permissible as protective measure",
        "Courts apply geological reality, not formalistic vein/lode definitions",
        "Amended locations can cure classification errors in some jurisdictions",
        "BLM mineral examiners apply practical geological tests, not theoretical standards"
    ],
    resolution_strategy=(
        "Engage qualified geologist to characterize the deposit. If doubt exists about classification, "
        "consider dual location (both lode and placer claims). Record both with county and BLM. "
        "Document geological basis for classification in location notice."
    ),
    entity_scope=["mining claimants", "BLM", "competing claimants", "geological consultants"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — well-established geological distinction with extensive case law",
    controlling_precedent="Iron Silver Mining Co. v. Cheesman, 116 U.S. 529 (1886)"
)

# =============================================================================
# DOCTRINE BLOCK 7: SPLIT MINERAL ESTATE
# =============================================================================
SPLIT_MINERAL_ESTATE = DoctrineBlock(
    topic="split_mineral_estate",
    keywords=["split estate", "mineral severance", "severed minerals", "coal vs oil gas", "mineral reservation", "fractional interest", "mineral ownership"],
    conclusion_template=(
        "A split mineral estate exists when the subsurface mineral rights have been severed and "
        "different minerals are owned by different parties. The most common configuration separates "
        "coal from oil and gas, but estates can be further fractionated to separate specific minerals "
        "(coal, oil, gas, uranium, limestone, sand/gravel, etc.). Each severed mineral estate is an "
        "independent property right with its own implied surface use rights. Conflicts arise when "
        "multiple mineral estate owners assert competing surface use rights or when extraction of "
        "one mineral interferes with recovery of another."
    ),
    reasoning_framework=(
        "Step 1: Trace the chain of title to identify all mineral severances. Each conveyance or "
        "reservation that separates specific minerals creates a new estate.\n"
        "Step 2: Determine the hierarchy of mineral estates. Under common law, earlier-severed "
        "mineral estates generally have priority surface use rights. The 'prior appropriation' "
        "concept may apply to surface use conflicts.\n"
        "Step 3: Evaluate the 'dominant mineral' doctrine — in some jurisdictions, the first mineral "
        "being actively developed has priority over later development of other minerals.\n"
        "Step 4: Assess implied easement rights for each mineral estate. Each estate has an implied "
        "right to use so much of the surface as is reasonably necessary for extraction.\n"
        "Step 5: Determine whether a 'subjacent support' obligation exists — the coal estate owner "
        "typically owes a duty of subjacent support to the surface estate and other mineral estates.\n"
        "Step 6: Evaluate potential for waste — extraction of one mineral may permanently prevent "
        "or impair recovery of another mineral, creating an actionable waste claim.\n"
        "Step 7: Assess unitization or pooling potential — statutory mechanisms may resolve conflicts "
        "by combining mineral estates for coordinated development."
    ),
    key_factors=[
        "Complete chain of title identifying all severances and reservations",
        "Chronological priority of mineral severances",
        "Whether specific minerals are named or 'all minerals' language is used",
        "Active development status of each mineral estate",
        "Subjacent support obligations between mineral estates",
        "Potential waste from conflicting extraction methods",
        "Availability of statutory unitization or pooling mechanisms"
    ],
    primary_authority=[
        "Acker v. Guinn, 464 S.W.2d 348 (Tex. 1971) — mineral estate dominance",
        "Pennsylvania Coal Co. v. Mahon, 260 U.S. 393 (1922) — subjacent support waiver",
        "Armstrong v. Maryland Coal Co., 67 W.Va. 589 (1910) — subjacent support",
        "Chartiers Block Coal Co. v. Mellon, 25 A. 597 (Pa. 1893)",
        "Restatement (Third) of Property: Servitudes § 4.10"
    ],
    burden_holder="Party asserting priority surface use right bears burden of proof",
    adversary_position=(
        "Later mineral estate owners argue that all mineral estates have co-equal surface use "
        "rights and that priority based solely on chronology of severance is inequitable, "
        "particularly when the later-severed mineral has become more commercially valuable."
    ),
    counter_arguments=[
        "Prior severance creates vested property rights that cannot be diminished by subsequent severance",
        "Dominant mineral doctrine accommodates changing economic values",
        "Modern coordination agreements can resolve conflicts without litigation",
        "Subjacent support obligations protect all estates from destruction",
        "Statutory pooling mechanisms available in most mineral-producing states"
    ],
    resolution_strategy=(
        "Complete thorough title examination identifying all mineral severances. Map each estate "
        "with its associated surface use rights. Negotiate mineral coordination agreement among "
        "all estate owners. If coordination fails, pursue statutory unitization. Ensure subjacent "
        "support obligations are documented and enforceable."
    ),
    entity_scope=["mineral estate owners", "surface owners", "title examiners", "courts"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE — outcomes vary significantly by jurisdiction and specific deed language",
    controlling_precedent="Acker v. Guinn, 464 S.W.2d 348 (Tex. 1971)"
)

# =============================================================================
# DOCTRINE BLOCK 8: SUBSURFACE TRESPASS
# =============================================================================
SUBSURFACE_TRESPASS = DoctrineBlock(
    topic="subsurface_trespass_mining",
    keywords=["subsurface trespass", "underground trespass", "mining beyond boundaries", "extraction trespass", "mineral trespass", "good faith bad faith"],
    conclusion_template=(
        "Subsurface trespass in mining occurs when an operator extracts minerals from land owned "
        "by another party, either by mining beyond the boundaries of the owned or leased premises "
        "or by extracting minerals not included in the grant. The measure of damages depends on "
        "whether the trespass was in good faith (innocent) or bad faith (willful). Good faith "
        "trespassers pay the value of minerals in place (pre-extraction). Bad faith trespassers "
        "pay the full value of minerals at the surface (post-extraction), which includes the value "
        "added by the trespasser's labor and capital. The distinction can result in damages differing "
        "by orders of magnitude."
    ),
    reasoning_framework=(
        "Step 1: Establish the property boundary — subsurface boundaries follow the vertical projection "
        "of surface boundaries unless modified by extralateral rights (lode claims) or specific "
        "deed provisions.\n"
        "Step 2: Determine whether extraction occurred beyond the boundary. Survey evidence, mine "
        "maps, and geological testimony establish the extent of trespass.\n"
        "Step 3: Classify the trespass as good faith or bad faith:\n"
        "  - Good faith: Trespasser honestly believed they had the right to extract (e.g., boundary "
        "    survey error, good faith interpretation of ambiguous deed).\n"
        "  - Bad faith: Trespasser knew or should have known they were mining on another's land.\n"
        "Step 4: Calculate damages:\n"
        "  - Good faith: Value of minerals in place (royalty interest method or comparable sales).\n"
        "  - Bad faith: Gross value at the surface less nothing — trespasser forfeits all value of "
        "    labor, capital, and processing costs.\n"
        "Step 5: Evaluate additional remedies — injunctive relief, accounting of profits, punitive "
        "damages (available in bad faith cases in some jurisdictions).\n"
        "Step 6: Assess statute of limitations — discovery rule may toll the limitations period for "
        "underground trespass because the surface owner may not know mining occurred below."
    ),
    key_factors=[
        "Accurate survey of subsurface property boundaries",
        "Extent of mineral extraction beyond boundaries (volume, tonnage, value)",
        "Good faith vs bad faith classification of the trespass",
        "Whether trespasser consulted surveys or title before mining",
        "Applicable damages measure in the jurisdiction",
        "Statute of limitations and discovery rule applicability",
        "Availability of punitive damages for willful trespass"
    ],
    primary_authority=[
        "Vines v. McKenzie Methane Corp., 619 So.2d 1305 (Ala. 1993)",
        "Martin v. Kentucky Oak Mining Co., 429 S.W.2d 395 (Ky. 1968)",
        "Restatement (Second) of Torts § 158 (trespass to land)",
        "Cowell v. Colorado Springs Co., 100 U.S. 55 (1879)",
        "McCoy v. Arkansas Natural Gas Co., 184 La. 101 (1936)"
    ],
    burden_holder="Landowner bears initial burden to prove trespass; trespasser bears burden to prove good faith",
    adversary_position=(
        "Mining operators argue that subsurface boundaries are inherently difficult to determine, "
        "that good faith reliance on professional surveys should protect against bad faith classification, "
        "and that the severe penalty for bad faith trespass (forfeiture of all improvement value) is "
        "punitive and unconstitutional."
    ),
    counter_arguments=[
        "Good faith classification protects operators who rely on professional surveys",
        "Modern surveying technology (GPS, lidar) makes boundary determination more precise",
        "Bad faith damages are not unconstitutional — they restore unjust enrichment",
        "Discovery rule protects surface owners who cannot observe underground operations",
        "Injunctive relief available without proving bad faith"
    ],
    resolution_strategy=(
        "Engage licensed surveyor to establish subsurface boundaries before mining begins. Maintain "
        "contemporaneous mine maps showing extraction boundaries. If trespass discovered, immediately "
        "cease operations and engage counsel. Document all pre-mining diligence to support good faith defense."
    ),
    entity_scope=["mining operators", "mineral owners", "surface owners", "surveyors"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — good faith/bad faith distinction well-established across jurisdictions",
    controlling_precedent="Cowell v. Colorado Springs Co., 100 U.S. 55 (1879)"
)

# =============================================================================
# DOCTRINE BLOCK 9: LATERAL SUPPORT
# =============================================================================
LATERAL_SUPPORT = DoctrineBlock(
    topic="lateral_support_doctrine",
    keywords=["lateral support", "subjacent support", "mine subsidence", "surface support", "ground stability", "undermining", "pillar removal"],
    conclusion_template=(
        "The lateral and subjacent support doctrines impose duties on mining operators to prevent "
        "surface subsidence from underground extraction. Lateral support protects adjacent land from "
        "collapse caused by excavation on neighboring property. Subjacent support protects the surface "
        "estate from collapse caused by underground mining directly below. The duty of subjacent "
        "support is absolute at common law — strict liability applies without requiring proof of "
        "negligence. However, the duty can be waived by express deed provisions, and Pennsylvania "
        "Coal v. Mahon established that compelled support can constitute a regulatory taking."
    ),
    reasoning_framework=(
        "Step 1: Distinguish lateral from subjacent support:\n"
        "  - Lateral: Adjacent land support — mining on Parcel A cannot cause collapse on Parcel B.\n"
        "  - Subjacent: Vertical support — underground mining cannot cause surface collapse above.\n"
        "Step 2: Determine whether the support duty has been waived. Many coal deeds include express "
        "waiver of support rights, particularly in Appalachian states.\n"
        "Step 3: If no waiver, strict liability applies at common law. The surface owner need only "
        "prove: (a) subsidence occurred, (b) mining was the proximate cause.\n"
        "Step 4: If waiver exists, evaluate validity:\n"
        "  - Was the waiver knowing and voluntary?\n"
        "  - Does state law permit support waivers? (Some states have restricted or eliminated waivers.)\n"
        "  - Pennsylvania Bituminous Mine Subsidence Act limits support waivers for occupied structures.\n"
        "Step 5: Assess regulatory framework — SMCRA Section 720 (30 USC 1309a) addresses subsidence "
        "from underground coal mining, requiring operators to repair or compensate for damage to "
        "occupied dwellings and structures.\n"
        "Step 6: Evaluate damages — structural damage, loss of use, diminution of property value, "
        "and in some cases, the cost of complete restoration."
    ),
    key_factors=[
        "Whether duty arises from lateral or subjacent support obligation",
        "Existence and validity of express support waiver in mineral deed",
        "State law treatment of support waivers",
        "Proximity of mining to surface structures",
        "Mining method and pillar removal plans",
        "SMCRA Section 720 applicability for underground coal mining",
        "Proof of causation between mining and surface damage"
    ],
    primary_authority=[
        "Pennsylvania Coal Co. v. Mahon, 260 U.S. 393 (1922)",
        "Keystone Bituminous Coal Assn. v. DeBenedictis, 480 U.S. 470 (1987)",
        "30 USC 1309a (SMCRA subsidence provisions)",
        "PA Bituminous Mine Subsidence and Land Conservation Act (52 P.S. § 1406.1)",
        "Armstrong v. Maryland Coal Co., 67 W.Va. 589 (1910)"
    ],
    burden_holder="Surface owner bears burden to prove subsidence and mining causation; operator must prove valid waiver if asserted",
    adversary_position=(
        "Mining operators argue that support waivers are valid contractual provisions, that the "
        "mineral estate buyer paid value for the right to extract without support obligation, and "
        "that compelled support effectively deprives the mineral owner of the right to mine."
    ),
    counter_arguments=[
        "Keystone distinguished Mahon — subsidence regulation is a valid exercise of police power",
        "SMCRA Section 720 imposes federal minimum protection regardless of deed provisions",
        "Public safety rationale supports restrictions on support waivers",
        "Modern long-wall mining causes more extensive subsidence than room-and-pillar methods",
        "Insurance and bonding mechanisms can distribute subsidence costs equitably"
    ],
    resolution_strategy=(
        "Review mineral deed for express support waiver. Check state law validity of waiver. "
        "If valid waiver exists, ensure SMCRA Section 720 compliance for occupied structures. "
        "Implement subsidence monitoring program. Purchase subsidence insurance where available. "
        "Design mining plan to minimize surface impact in populated areas."
    ),
    entity_scope=["coal operators", "surface owners", "regulatory agencies", "insurance companies"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — well-developed doctrine with both constitutional and statutory dimensions",
    controlling_precedent="Keystone Bituminous Coal Assn. v. DeBenedictis, 480 U.S. 470 (1987)"
)

# =============================================================================
# DOCTRINE BLOCK 10: URANIUM MINING AND NRC LICENSING
# =============================================================================
URANIUM_MINING_NRC = DoctrineBlock(
    topic="uranium_mining_nrc_licensing",
    keywords=["uranium", "nrc", "nuclear regulatory", "source material", "yellowcake", "in situ", "isl", "uranium leasing"],
    conclusion_template=(
        "Uranium mining operates under a dual regulatory framework: the Atomic Energy Act of 1954 "
        "governs NRC licensing for source material (uranium, thorium), while the General Mining Law "
        "of 1872 governs the initial location of uranium mining claims on public lands. The NRC "
        "issues source material licenses for uranium recovery operations, with the choice between "
        "conventional mining/milling and in-situ leaching (ISL/ISR) having profound regulatory "
        "implications. ISR operations, which extract uranium using injection wells, are also subject "
        "to EPA Underground Injection Control (UIC) requirements. State agreements may transfer "
        "NRC regulatory authority to 'agreement states' for certain activities."
    ),
    reasoning_framework=(
        "Step 1: Determine if uranium is a locatable mineral — yes, uranium is locatable under the "
        "1872 Mining Law when found on public domain lands not withdrawn from mineral entry.\n"
        "Step 2: Evaluate land status — many uranium-rich areas are on public lands subject to BLM "
        "surface management, USFS management, or tribal lands requiring BIA approval.\n"
        "Step 3: Determine extraction method:\n"
        "  - Conventional mining: Open pit or underground excavation followed by milling.\n"
        "  - In-situ recovery (ISR): Chemical leaching through injection/recovery wells.\n"
        "  - Heap leaching: Surface leaching of mined ore.\n"
        "Step 4: Identify NRC licensing requirements:\n"
        "  - 10 CFR Part 40 — Domestic licensing of source material.\n"
        "  - NUREG-1569 — Standard Review Plan for ISR facilities.\n"
        "  - Environmental review under NEPA (EIS typically required).\n"
        "Step 5: Check for 'agreement state' status — if the state has an agreement with NRC under "
        "Section 274 of the Atomic Energy Act, the state issues the source material license.\n"
        "Step 6: Evaluate financial assurance requirements — NRC requires decommissioning financial "
        "assurance sufficient to cover complete site restoration."
    ),
    key_factors=[
        "Land status — public domain, tribal, state, or private",
        "Extraction method — conventional, ISR, or heap leach",
        "NRC vs agreement state licensing jurisdiction",
        "NEPA compliance — EIS vs EA determination",
        "EPA UIC permit requirements for ISR operations",
        "Financial assurance for decommissioning",
        "Proximity to tribal lands, national parks, or groundwater resources"
    ],
    primary_authority=[
        "42 USC 2011 et seq. (Atomic Energy Act of 1954)",
        "10 CFR Part 40 (NRC source material licensing)",
        "NUREG-1569 (Standard Review Plan for ISR facilities)",
        "42 USC 300h (Safe Drinking Water Act — UIC program)",
        "Kerr-McGee Corp. v. NRC, 903 F.2d 1 (D.C. Cir. 1990)"
    ],
    burden_holder="Applicant bears burden to demonstrate compliance with all NRC licensing criteria",
    adversary_position=(
        "Environmental and tribal groups oppose uranium mining due to legacy contamination from "
        "Cold War-era operations, particularly on Navajo Nation lands. They argue ISR operations "
        "risk groundwater contamination that cannot be remediated."
    ),
    counter_arguments=[
        "Modern ISR technology has significantly lower environmental impact than conventional mining",
        "NRC licensing process includes comprehensive environmental review",
        "Financial assurance requirements ensure funding for complete site restoration",
        "Groundwater monitoring and restoration requirements protect aquifers",
        "Domestic uranium production supports energy independence and national security",
        "Agreement state programs provide local oversight and accountability"
    ],
    resolution_strategy=(
        "Conduct baseline environmental assessment. Engage NRC (or agreement state) early in process. "
        "If ISR, secure EPA UIC permit concurrently with NRC license. Develop comprehensive groundwater "
        "monitoring plan. Post adequate financial assurance. Engage tribal consultation if on or near "
        "tribal lands. Budget 3-5 years for full licensing process."
    ),
    entity_scope=["uranium mining companies", "NRC", "EPA", "BLM", "tribal governments", "agreement states"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — well-defined regulatory framework, though political and environmental opposition adds uncertainty",
    controlling_precedent="Kerr-McGee Corp. v. NRC, 903 F.2d 1 (D.C. Cir. 1990)"
)

# =============================================================================
# DOCTRINE BLOCK 11: RECLAMATION BONDING
# =============================================================================
RECLAMATION_BONDING = DoctrineBlock(
    topic="reclamation_bonding_performance",
    keywords=["reclamation bond", "performance bond", "surety bond", "self-bonding", "bond pool", "bond release", "reclamation liability"],
    conclusion_template=(
        "Reclamation bonding under SMCRA requires coal mining operators to post financial assurance "
        "sufficient to cover the cost of reclamation if the operator fails to complete it. Bond forms "
        "include surety bonds, collateral bonds, self-bonds (for operators meeting net worth "
        "requirements), and alternative bonding systems (state pool bonds). The bond amount must equal "
        "the estimated cost for a third-party contractor to complete reclamation. Bond release occurs "
        "in phases as reclamation milestones are achieved. The collapse of Alpha Natural Resources and "
        "Patriot Coal demonstrated catastrophic risks of self-bonding, prompting regulatory reforms."
    ),
    reasoning_framework=(
        "Step 1: Determine the applicable bonding system — federal (30 CFR Part 800) or state primacy "
        "program bonding rules.\n"
        "Step 2: Calculate required bond amount — must cover third-party reclamation cost including "
        "backfilling, regrading, topsoil replacement, revegetation, and hydrologic restoration.\n"
        "Step 3: Select bond form:\n"
        "  - Surety bond: Corporate surety issues bond; most common and reliable.\n"
        "  - Collateral bond: Cash, securities, or real property pledged.\n"
        "  - Self-bond: Operator pledges own net worth (restricted after coal industry bankruptcies).\n"
        "  - Pool bond: State-administered pool funded by per-ton fees (PA, WV alternatives).\n"
        "Step 4: Evaluate phase release schedule:\n"
        "  - Phase I: Backfilling, regrading, drainage control complete.\n"
        "  - Phase II: Revegetation established successfully.\n"
        "  - Phase III: Full bond release after revegetation responsibility period (5-10 years).\n"
        "Step 5: Assess supplemental bonding requirements — some states require additional bonds for "
        "acid mine drainage treatment, water replacement, or post-mining discharges.\n"
        "Step 6: Monitor self-bonding restrictions — post-2016 OSMRE guidance significantly restricted "
        "self-bonding eligibility due to coal industry financial distress."
    ),
    key_factors=[
        "Accurate third-party reclamation cost estimate",
        "Bond form selection and surety availability",
        "Self-bonding eligibility (financial tests, investment grade rating)",
        "State-specific alternative bonding system availability",
        "Phase release milestones and revegetation success criteria",
        "Acid mine drainage potential requiring supplemental bonding",
        "Operator compliance history affecting bond adjustment"
    ],
    primary_authority=[
        "30 USC 1259 (SMCRA bonding requirements)",
        "30 CFR Part 800 (Federal bonding regulations)",
        "OSMRE Directive REG-8 (Self-bonding policy)",
        "National Mining Assn. v. Zinke (self-bonding challenges)",
        "30 USC 1269 (Bond release procedures)"
    ],
    burden_holder="Operator bears burden to demonstrate adequate bond and reclamation compliance for release",
    adversary_position=(
        "Environmental groups argue that bonds are systematically underfunded, that self-bonding "
        "shifts reclamation costs to taxpayers when operators go bankrupt, and that bond release "
        "occurs too readily before long-term reclamation success is demonstrated."
    ),
    counter_arguments=[
        "Bond amounts are required to cover full third-party reclamation costs",
        "OSMRE post-2016 guidance effectively eliminated self-bonding for most operators",
        "Phase release system provides incremental verification of reclamation success",
        "State pool bond systems socialize risk across the industry",
        "Bond forfeiture funds are dedicated to completing reclamation"
    ],
    resolution_strategy=(
        "Obtain independent reclamation cost estimate from qualified engineer. Secure surety bond "
        "from rated surety company. Avoid self-bonding unless financial condition is exceptionally "
        "strong. Implement progressive reclamation to achieve earliest possible phase releases. "
        "Maintain bonding reserve for potential supplemental requirements."
    ),
    entity_scope=["coal operators", "surety companies", "regulatory authorities", "reclamation contractors"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — bonding framework well-established; self-bonding restrictions tightened post-2016",
    controlling_precedent="30 USC 1259 and 30 CFR Part 800"
)

# =============================================================================
# DOCTRINE BLOCK 12: SURFACE OWNER CONSENT FOR MINING
# =============================================================================
SURFACE_OWNER_CONSENT = DoctrineBlock(
    topic="surface_owner_consent_mining",
    keywords=["surface consent", "surface owner", "mining consent", "surface rights", "entry rights", "surface damage", "accommodation"],
    conclusion_template=(
        "Surface owner consent requirements for mining operations vary dramatically by jurisdiction "
        "and mineral type. For federal coal leasing, SMCRA Section 714 (30 USC 1304) requires written "
        "consent or ownership of the surface for operations on non-federal surface overlying federal "
        "coal. For hardrock mining on private split estates, the mineral owner's implied right of "
        "reasonable surface use generally does not require surface owner consent, but the accommodation "
        "doctrine in some states requires the mineral owner to use the least intrusive extraction "
        "method that is commercially feasible. State surface damage acts (ND, MT, WY, SD, OK) may "
        "require notice, negotiation, or compensation before surface entry."
    ),
    reasoning_framework=(
        "Step 1: Identify the mineral type and land ownership pattern:\n"
        "  - Federal minerals under private surface: SMCRA consent provisions apply.\n"
        "  - Private minerals under private surface: Common law and state statutes apply.\n"
        "  - State minerals: State leasing act provisions apply.\n"
        "Step 2: For federal coal under non-federal surface, apply 30 USC 1304:\n"
        "  - Written consent from surface owner, OR\n"
        "  - Execution of a bond or deposit to protect surface owner interests.\n"
        "Step 3: For private mineral estates, evaluate state doctrine:\n"
        "  - Accommodation doctrine states: TX, ND, SD, WY, NM.\n"
        "  - Reasonable use states: WV, PA, VA.\n"
        "  - Surface damage act states: ND, MT, WY, SD, OK, IL.\n"
        "Step 4: If surface damage act applies, comply with notice requirements — typically 30-90 "
        "days advance notice with description of planned operations.\n"
        "Step 5: Negotiate surface use agreement covering: access routes, well pad locations, "
        "pipeline corridors, reclamation standards, and compensation.\n"
        "Step 6: If negotiation fails, evaluate statutory alternatives — some states provide "
        "administrative proceedings or arbitration for surface use disputes."
    ),
    key_factors=[
        "Federal vs private mineral ownership",
        "Whether surface and minerals are commonly owned or split",
        "Applicable state accommodation or surface damage act",
        "Type of mining operation (surface vs underground)",
        "Extent of proposed surface disturbance",
        "Existing surface use and improvements",
        "Availability of less intrusive alternative extraction methods"
    ],
    primary_authority=[
        "30 USC 1304 (SMCRA — consent for surface mining of federal coal)",
        "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) — accommodation doctrine",
        "N.D. Cent. Code § 38-11.1 (Surface Owner Protection Act)",
        "Mont. Code Ann. § 82-10-504 (Surface owner notification)",
        "Hunt Oil Co. v. Kerbaugh, 283 N.W.2d 131 (N.D. 1979)"
    ],
    burden_holder="Mineral owner bears burden to demonstrate reasonable surface use; surface owner bears burden to show less intrusive alternatives exist",
    adversary_position=(
        "Surface owners argue that mineral development destroys agricultural productivity, "
        "diminishes property values, and imposes costs (dust, noise, traffic) that are never "
        "fully compensated by surface damage payments."
    ),
    counter_arguments=[
        "Mineral estate is dominant estate under common law with implied access rights",
        "Accommodation doctrine balances interests without eliminating mineral development",
        "Surface damage acts provide compensation framework without blocking development",
        "Progressive reclamation restores surface to productive use after mining",
        "Surface use agreements can provide substantial compensation exceeding agricultural value"
    ],
    resolution_strategy=(
        "Negotiate surface use agreement before operations begin. If on federal coal, secure "
        "written surface owner consent or post adequate bond under 30 USC 1304. Comply with all "
        "state notice requirements. Document due diligence in selecting least intrusive feasible "
        "method. Implement progressive reclamation plan."
    ),
    entity_scope=["mineral owners", "surface owners", "mining operators", "BLM"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — surface owner protections well-established but vary by state",
    controlling_precedent="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)"
)

# =============================================================================
# DOCTRINE BLOCK 13: GEOTHERMAL RESOURCE LEASING
# =============================================================================
GEOTHERMAL_LEASING = DoctrineBlock(
    topic="geothermal_resource_leasing",
    keywords=["geothermal", "steam act", "geothermal lease", "hot springs", "geothermal energy", "blm lease", "30 usc 1001"],
    conclusion_template=(
        "Geothermal resources on federal lands are leased under the Geothermal Steam Act of 1970 "
        "(30 USC 1001-1028), as amended by the Energy Policy Act of 2005. BLM administers the "
        "leasing program through competitive and noncompetitive leasing processes. Geothermal "
        "resources are defined as products of geothermal processes including indigenous steam, hot "
        "water, and associated energy. They are NOT locatable under the 1872 Mining Law. Lease terms "
        "are 10 years with continuation for production. Royalty rates are set by BLM regulation, "
        "currently at 1.75% for electricity generation and 10% for direct use."
    ),
    reasoning_framework=(
        "Step 1: Confirm the land is available for geothermal leasing. Public domain managed by BLM "
        "or USFS is generally available unless withdrawn. National parks and wilderness areas are excluded.\n"
        "Step 2: Determine leasing process:\n"
        "  - Competitive: Lands nominated in areas of known geothermal resource area (KGRA).\n"
        "  - Noncompetitive: Lands not in KGRA available by application.\n"
        "  - Direct use: Simplified leasing for small-scale direct use projects.\n"
        "Step 3: Evaluate lease terms — 10-year primary term, continuation for production, maximum "
        "lease size 5,120 acres, state maximum acreage 51,200 acres.\n"
        "Step 4: Assess royalty structure:\n"
        "  - Electricity generation: 1.75% of gross proceeds for first 10 years, then 3.5%.\n"
        "  - Direct use: 10% of gross proceeds.\n"
        "Step 5: Evaluate environmental compliance — NEPA review required for lease issuance and "
        "plan of development. ESA Section 7 consultation if endangered species present.\n"
        "Step 6: Assess conflicts with mineral leasing and water rights — geothermal resources may "
        "conflict with groundwater rights, mineral leases, or hot springs protections."
    ),
    key_factors=[
        "Land availability for geothermal leasing",
        "Known Geothermal Resource Area (KGRA) designation",
        "Competitive vs noncompetitive leasing process",
        "Royalty rate applicable to intended use",
        "Environmental compliance requirements",
        "Conflict with existing water rights or mineral leases",
        "State geothermal regulatory requirements in addition to federal"
    ],
    primary_authority=[
        "30 USC 1001-1028 (Geothermal Steam Act of 1970)",
        "43 CFR Part 3200 (BLM geothermal leasing regulations)",
        "Energy Policy Act of 2005, Title II (geothermal amendments)",
        "Ottoboni v. United States, 549 F.2d 1271 (9th Cir. 1977)",
        "30 USC 1005 (Geothermal lease terms and conditions)"
    ],
    burden_holder="Lease applicant bears burden to demonstrate resource potential and environmental compliance",
    adversary_position=(
        "Environmental groups and water rights holders argue that geothermal extraction depletes "
        "shared groundwater resources, that subsurface injection can induce seismicity, and that "
        "development in volcanic/geothermal areas can damage unique geological features."
    ),
    counter_arguments=[
        "Geothermal energy is renewable and produces minimal greenhouse gas emissions",
        "Modern closed-loop systems minimize water consumption and induced seismicity",
        "BLM environmental review process addresses resource conflicts before lease issuance",
        "Geothermal royalty rates provide fair return to public while incentivizing development",
        "Energy Policy Act of 2005 streamlined leasing to encourage domestic clean energy"
    ],
    resolution_strategy=(
        "Conduct geothermal resource assessment with qualified geoscientist. Apply for competitive "
        "or noncompetitive lease through BLM. Develop comprehensive environmental assessment. "
        "Coordinate with state water engineer regarding potential groundwater conflicts. "
        "Submit plan of development with induced seismicity monitoring protocol."
    ),
    entity_scope=["geothermal developers", "BLM", "USFS", "state water engineers"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — statutory framework well-established; resource characterization adds technical uncertainty",
    controlling_precedent="Ottoboni v. United States, 549 F.2d 1271 (9th Cir. 1977)"
)

# =============================================================================
# DOCTRINE BLOCK 14: LITHIUM AND RARE EARTH RIGHTS
# =============================================================================
LITHIUM_RARE_EARTH = DoctrineBlock(
    topic="lithium_rare_earth_mineral_rights",
    keywords=["lithium", "rare earth", "critical minerals", "ree", "lithium brine", "spodumene", "defense production act", "critical mineral"],
    conclusion_template=(
        "Lithium and rare earth elements (REEs) represent the fastest-growing segment of mineral "
        "rights law, driven by demand for batteries, electric vehicles, and defense applications. "
        "Lithium ownership is complicated by its occurrence in both hardrock deposits (spodumene, "
        "lepidolite) locatable under the 1872 Mining Law and brine deposits that may be classified "
        "as water or mineral depending on jurisdiction. REEs are locatable minerals on federal "
        "public lands. The Defense Production Act, Infrastructure Investment and Jobs Act, and "
        "Inflation Reduction Act have created substantial federal incentives for domestic critical "
        "mineral production, including expedited permitting under Title 41 of the FAST Act."
    ),
    reasoning_framework=(
        "Step 1: Classify the lithium deposit type:\n"
        "  - Hardrock (spodumene, lepidolite): Clearly a locatable mineral under 1872 Mining Law.\n"
        "  - Brine: Ambiguous — some jurisdictions classify as mineral, others as water resource.\n"
        "  - Claystones (hectorite): Locatable mineral, similar to other industrial minerals.\n"
        "  - Geothermal brine: May fall under Geothermal Steam Act, not 1872 Mining Law.\n"
        "Step 2: For brine lithium, determine state classification:\n"
        "  - Nevada: Lithium in brine is a mineral subject to mining claims.\n"
        "  - California: Geothermal brine lithium may be subject to geothermal lease.\n"
        "  - Arkansas: Smackover brine lithium subject to mineral rights, not water rights.\n"
        "Step 3: Evaluate federal incentives:\n"
        "  - Defense Production Act Title III: Direct investment in critical mineral processing.\n"
        "  - IIJA Section 40206: $3B for battery material processing.\n"
        "  - IRA Section 45X: Advanced manufacturing tax credit for critical minerals.\n"
        "Step 4: Assess permitting pathway — BLM critical mineral expedited review under "
        "Secretarial Order 3399 and FAST-41 process for designated critical minerals.\n"
        "Step 5: Evaluate export restrictions — certain rare earths may be subject to export "
        "controls under national security provisions.\n"
        "Step 6: Assess tribal and environmental opposition — major lithium deposits at Thacker "
        "Pass (NV) and others face significant legal challenges."
    ),
    key_factors=[
        "Lithium deposit type (hardrock, brine, claystone, geothermal)",
        "State classification of brine lithium (mineral vs water)",
        "Availability of federal incentive programs",
        "Critical mineral designation under USGS list",
        "Permitting timeline under expedited vs standard review",
        "Environmental and tribal opposition to specific projects",
        "Supply chain implications for defense and EV applications"
    ],
    primary_authority=[
        "50 USC 4501 et seq. (Defense Production Act)",
        "Infrastructure Investment and Jobs Act, Pub. L. 117-58, § 40206",
        "Inflation Reduction Act, Pub. L. 117-169, § 45X",
        "Secretarial Order 3399 (Critical mineral development)",
        "DOI USGS Critical Minerals List (2022 final list, 50 minerals)"
    ],
    burden_holder="Applicant bears burden to demonstrate resource characterization and environmental compliance",
    adversary_position=(
        "Environmental and tribal groups argue that lithium and REE mining causes severe "
        "environmental damage including water depletion, dust contamination, and destruction "
        "of culturally significant landscapes, and that domestic production cannot be scaled "
        "fast enough to meet demand without unacceptable environmental sacrifice."
    ),
    counter_arguments=[
        "Critical mineral supply chain security is a national defense priority",
        "Domestic production reduces dependence on adversarial foreign suppliers (China)",
        "Modern direct lithium extraction (DLE) technology significantly reduces environmental footprint",
        "Federal incentives and expedited permitting accelerate responsible development",
        "Recycling programs will supplement primary production over time",
        "NEPA review ensures environmental impacts are evaluated and mitigated"
    ],
    resolution_strategy=(
        "Characterize deposit type and confirm mineral vs water classification. Locate mining "
        "claims or apply for leases as appropriate. Apply for critical mineral designation "
        "benefits and FAST-41 expedited review. Engage tribal consultation early. Develop "
        "comprehensive environmental mitigation plan. Secure offtake agreements with battery "
        "manufacturers or defense contractors."
    ),
    entity_scope=["lithium/REE developers", "BLM", "DOD", "DOE", "tribal governments", "EV manufacturers"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE — rapidly evolving regulatory landscape with significant political and legal uncertainty",
    controlling_precedent="Defense Production Act (50 USC 4501) as applied to critical minerals"
)

# =============================================================================
# DOCTRINE BLOCK 15: CARBON SEQUESTRATION PORE SPACE
# =============================================================================
CARBON_SEQUESTRATION_PORE_SPACE = DoctrineBlock(
    topic="carbon_sequestration_pore_space",
    keywords=["pore space", "carbon sequestration", "ccs", "ccus", "co2 storage", "subsurface storage", "45q", "class vi well"],
    conclusion_template=(
        "Carbon capture and sequestration (CCS) has created a new frontier in mineral and subsurface "
        "rights: who owns the pore space for CO2 storage? The emerging consensus is that pore space "
        "rights belong to the surface estate owner, not the mineral estate owner, as the pore space "
        "is analogous to the physical structure of the land rather than a mineral substance. At least "
        "10 states have enacted pore space ownership statutes. The 45Q tax credit provides up to "
        "$85/ton for geologic sequestration, creating enormous economic incentives. EPA administers "
        "Class VI underground injection control permits for CO2 wells, while some states have "
        "obtained primacy to issue Class VI permits."
    ),
    reasoning_framework=(
        "Step 1: Identify pore space ownership under applicable state law:\n"
        "  - Statutory states: WY, MT, ND, LA, TX, OK, WV, IL, IN, KS have pore space statutes.\n"
        "  - Common law states: Apply ad coelum doctrine — surface owner owns to center of earth.\n"
        "  - Split estate analysis: If minerals severed, pore space typically remains with surface.\n"
        "Step 2: Evaluate mineral estate conflicts:\n"
        "  - CO2 injection may interfere with mineral extraction (oil/gas, coal, brine minerals).\n"
        "  - Mineral estate owner's paramount right to extract may limit CO2 injection zones.\n"
        "  - Priority of use conflicts require careful analysis of severance deed language.\n"
        "Step 3: Determine permitting requirements:\n"
        "  - EPA Class VI UIC permit for CO2 injection wells.\n"
        "  - State primacy: ND, WY, LA have Class VI primacy (as of 2024).\n"
        "  - NEPA review if federal lands or federal funding involved.\n"
        "Step 4: Evaluate 45Q tax credit qualification:\n"
        "  - $85/ton for geologic sequestration (dedicated storage).\n"
        "  - $60/ton for enhanced oil recovery utilization.\n"
        "  - Secure storage requirements and monitoring obligations.\n"
        "Step 5: Assess long-term liability — post-injection site care and monitoring period "
        "(minimum 50 years under EPA rules), followed by potential transfer to federal or state oversight.\n"
        "Step 6: Evaluate unitization mechanisms — some states allow forced unitization of pore "
        "space for CO2 storage, similar to oil/gas unitization."
    ),
    key_factors=[
        "State pore space ownership statute or common law position",
        "Relationship between pore space and severed mineral estates",
        "EPA Class VI permit requirements and state primacy",
        "45Q tax credit qualification and secure storage requirements",
        "Long-term liability and post-injection monitoring obligations",
        "Conflict with existing mineral extraction operations",
        "Availability of forced unitization for pore space aggregation"
    ],
    primary_authority=[
        "Wyo. Stat. § 34-1-152 (Pore space ownership)",
        "26 USC 45Q (Carbon oxide sequestration tax credit)",
        "40 CFR Part 146, Subpart H (Class VI UIC requirements)",
        "N.D. Cent. Code § 38-22 (Carbon dioxide storage)",
        "IRS Notice 2020-12 (45Q credit guidance)"
    ],
    burden_holder="CCS project developer bears burden to demonstrate pore space rights, secure permits, and meet 45Q requirements",
    adversary_position=(
        "Mineral estate owners argue that CO2 injection into formations containing minerals "
        "interferes with mineral recovery rights and constitutes a subsurface trespass. "
        "Environmental groups question the permanence of geologic storage and the adequacy "
        "of long-term monitoring requirements."
    ),
    counter_arguments=[
        "Pore space statutes explicitly vest ownership in surface estate",
        "CO2 injection can coexist with mineral operations through careful zoning",
        "45Q tax credit creates economic alignment between CCS and mineral development",
        "EPA Class VI permits require comprehensive monitoring and financial assurance",
        "Post-injection monitoring periods (50+ years) address permanence concerns",
        "Forced unitization resolves holdout problems in pore space aggregation"
    ],
    resolution_strategy=(
        "Confirm pore space ownership through title examination and state statute analysis. "
        "Aggregate pore space rights through lease or unitization. Secure Class VI UIC permit. "
        "Qualify for 45Q tax credits. Negotiate mineral accommodation agreements with mineral "
        "estate owners. Establish long-term monitoring and financial assurance plan."
    ),
    entity_scope=["CCS developers", "surface owners", "mineral owners", "EPA", "state oil/gas commissions"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE — rapidly evolving area with limited case law and significant regulatory uncertainty",
    controlling_precedent="Wyo. Stat. § 34-1-152 (first pore space ownership statute)"
)

# =============================================================================
# DOCTRINE BLOCK 16: HELIUM EXTRACTION RIGHTS
# =============================================================================
HELIUM_EXTRACTION = DoctrineBlock(
    topic="helium_extraction_rights",
    keywords=["helium", "helium rights", "federal helium reserve", "helium privatization", "noble gas", "helium lease", "blm helium"],
    conclusion_template=(
        "Helium presents a unique mineral rights challenge because it is a non-hydrocarbon gas "
        "commonly found with natural gas but subject to distinct ownership rules. On federal lands, "
        "helium was reserved to the United States under the Mineral Leasing Act and subsequent "
        "legislation. The Helium Stewardship Act of 2013 directed privatization of the Federal "
        "Helium Reserve near Amarillo, TX. On private lands, helium ownership depends on whether "
        "the severance deed conveys 'all minerals,' 'oil and gas,' or specifically names helium. "
        "Several courts have held helium is NOT included in an 'oil and gas' conveyance because it "
        "is neither oil nor gas in the petroleum sense."
    ),
    reasoning_framework=(
        "Step 1: Determine land ownership — federal, state, or private.\n"
        "Step 2: For federal lands, helium rights are typically reserved to the United States:\n"
        "  - Mineral Leasing Act reservations specifically reserve helium.\n"
        "  - BLM oil/gas leases may or may not convey helium rights.\n"
        "  - Federal Helium Reserve privatization affects specific reserves.\n"
        "Step 3: For private lands, examine deed language:\n"
        "  - 'All minerals': Generally includes helium.\n"
        "  - 'Oil and gas': May NOT include helium (jurisdiction-dependent).\n"
        "  - 'Oil, gas, and other minerals': Stronger argument for helium inclusion.\n"
        "  - Specific helium reservation: Controls.\n"
        "Step 4: Apply state-specific precedent:\n"
        "  - Kansas: Helium may be excluded from 'oil and gas' grants.\n"
        "  - Texas: Under Acker v. Guinn analysis, helium likely a 'mineral' in 'all minerals' grant.\n"
        "Step 5: Evaluate commercial viability — helium concentrations below ~0.3% are generally "
        "not commercially recoverable. Higher concentrations (>0.5%) are commercially significant.\n"
        "Step 6: Assess extraction infrastructure — helium extraction requires cryogenic processing "
        "equipment. Only a handful of domestic processing plants exist."
    ),
    key_factors=[
        "Federal vs private land ownership",
        "Exact deed language regarding mineral conveyance",
        "Whether helium is classified as a mineral in the applicable jurisdiction",
        "Helium concentration in associated gas stream",
        "Proximity to helium processing infrastructure",
        "Federal Helium Reserve status and allocation",
        "Strategic importance for defense and technology applications"
    ],
    primary_authority=[
        "50 USC 167 et seq. (Helium Act, as amended)",
        "Helium Stewardship Act of 2013 (Pub. L. 113-40)",
        "Acker v. Guinn, 464 S.W.2d 348 (Tex. 1971) — mineral classification",
        "Northern Natural Gas Co. v. Grounds, 292 F. Supp. 619 (D. Kan. 1968)",
        "30 USC 181 (Mineral Leasing Act helium provisions)"
    ],
    burden_holder="Party claiming helium rights bears burden to establish ownership through deed construction",
    adversary_position=(
        "Gas estate owners argue that helium is a component of the gas stream and is necessarily "
        "included in an 'oil and gas' conveyance. Separating helium from the gas estate creates "
        "impractical fractional interests."
    ),
    counter_arguments=[
        "Helium is chemically distinct from petroleum hydrocarbons — it is a noble gas",
        "Federal helium reservation demonstrates legislative intent to treat helium separately",
        "Helium's strategic value exceeds its proportional volume in the gas stream",
        "Modern deed drafting should specifically address helium to avoid ambiguity",
        "Processing technology can economically separate helium at the wellhead"
    ],
    resolution_strategy=(
        "Examine chain of title for helium-specific provisions. If deed is ambiguous, analyze "
        "under applicable state mineral classification doctrine. If on federal land, check BLM "
        "lease for helium reservation. Negotiate helium processing agreement with gas plant "
        "operator. Consider joint development agreement if ownership split."
    ),
    entity_scope=["gas estate owners", "helium processors", "BLM", "defense contractors"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE — limited case law; most deeds silent on helium specifically",
    controlling_precedent="Northern Natural Gas Co. v. Grounds, 292 F. Supp. 619 (D. Kan. 1968)"
)

# =============================================================================
# DOCTRINE BLOCK 17: AGGREGATE AND SAND/GRAVEL EXTRACTION
# =============================================================================
AGGREGATE_EXTRACTION = DoctrineBlock(
    topic="aggregate_sand_gravel_extraction",
    keywords=["aggregate", "sand", "gravel", "quarry", "surface minerals", "construction materials", "mineral classification"],
    conclusion_template=(
        "Aggregate, sand, and gravel extraction rights present a persistent mineral classification "
        "problem: are these substances 'minerals' within the meaning of a mineral severance deed? "
        "The answer varies dramatically by jurisdiction. Texas, under Reed v. Wylie, holds that "
        "surface substances like sand, gravel, and caliche are part of the surface estate unless "
        "specifically conveyed. Pennsylvania and several Appalachian states may include them in the "
        "mineral estate. On federal lands, common varieties of sand, gravel, and stone are subject "
        "to the Materials Act of 1947, not the 1872 Mining Law, and are sold through BLM materials "
        "contracts rather than mining claims."
    ),
    reasoning_framework=(
        "Step 1: Determine land ownership type — federal, state, or private.\n"
        "Step 2: For federal lands, apply the Materials Act of 1947 (30 USC 601-604):\n"
        "  - Common varieties of sand, stone, gravel, pumice, cinder, and clay are NOT locatable.\n"
        "  - BLM sells these through competitive or noncompetitive materials contracts.\n"
        "  - Uncommon varieties (rare gemstones, unique building stone) remain locatable.\n"
        "Step 3: For private lands, apply state mineral classification doctrine:\n"
        "  - Texas (surface estate presumption): Reed v. Wylie — surface substances belong to surface.\n"
        "  - Pennsylvania: May be mineral estate depending on commercial value.\n"
        "  - Kentucky: Surface minerals generally belong to surface estate.\n"
        "Step 4: Examine the severance deed — does it convey 'all minerals,' 'coal and minerals,' "
        "or specifically name sand, gravel, limestone, etc.?\n"
        "Step 5: Evaluate the 'ordinary and natural meaning' test — at the time of severance, "
        "would a reasonable person have understood 'minerals' to include sand and gravel?\n"
        "Step 6: Assess zoning and environmental permits — aggregate extraction typically requires "
        "local zoning approval, air quality permits, stormwater permits, and sometimes reclamation bonds."
    ),
    key_factors=[
        "Federal vs private land ownership",
        "Common variety vs uncommon variety classification (federal lands)",
        "State mineral classification doctrine",
        "Exact deed language and date of severance",
        "Commercial value and intended use of the aggregate",
        "Local zoning and permit requirements",
        "Proximity to markets (transportation costs dominate aggregate economics)"
    ],
    primary_authority=[
        "30 USC 601-604 (Materials Act of 1947)",
        "Reed v. Wylie, 597 S.W.2d 743 (Tex. 1980)",
        "United States v. McClarty, 17 IBLA 68 (1974) — common variety test",
        "Acker v. Guinn, 464 S.W.2d 348 (Tex. 1971)",
        "Heinatz v. Allen, 217 S.W.2d 994 (Tex. 1949)"
    ],
    burden_holder="Party claiming aggregate rights bears burden to establish ownership under applicable doctrine",
    adversary_position=(
        "Mineral estate owners argue that all substances beneath the surface are 'minerals' and "
        "that excluding commercially valuable sand, gravel, and limestone from the mineral estate "
        "is an artificial limitation that diminishes the mineral estate's value."
    ),
    counter_arguments=[
        "Surface substance doctrine prevents destruction of surface estate for low-value extraction",
        "Texas surface estate presumption is well-established and protects landowners",
        "Materials Act provides orderly disposal of common varieties on federal lands",
        "Modern deeds should specifically address aggregate rights if intended to convey",
        "Economic nexus to surface use (construction, roads) supports surface estate classification"
    ],
    resolution_strategy=(
        "Examine deed for specific sand/gravel/aggregate provisions. Apply applicable state "
        "classification doctrine. If on federal land, pursue BLM materials contract. Secure local "
        "zoning approval and environmental permits. Negotiate surface use agreement if split estate."
    ),
    entity_scope=["aggregate producers", "surface owners", "mineral owners", "BLM", "local planning authorities"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE — classification varies significantly by jurisdiction; outcome depends on deed language and state doctrine",
    controlling_precedent="Reed v. Wylie, 597 S.W.2d 743 (Tex. 1980)"
)

# =============================================================================
# DOCTRINE BLOCK 18: MINING LEASE VS MINING CLAIM
# =============================================================================
MINING_LEASE_VS_CLAIM = DoctrineBlock(
    topic="mining_lease_vs_mining_claim",
    keywords=["mining lease", "mining claim", "leasable mineral", "locatable mineral", "mineral leasing act", "blm lease", "federal mineral"],
    conclusion_template=(
        "The distinction between mining leases and mining claims is fundamental to federal mineral "
        "law. Locatable minerals (gold, silver, copper, uranium, etc.) are acquired through mining "
        "claims under the 1872 Mining Law — self-initiated, no government approval needed for "
        "location. Leasable minerals (coal, oil, gas, phosphate, sodium, potassium, sulfur, "
        "geothermal) are acquired through competitive or noncompetitive leases under the Mineral "
        "Leasing Act of 1920 — government-issued, with royalties, rental, and bonding requirements. "
        "Salable minerals (common varieties of sand, gravel, stone) are sold through Materials Act "
        "contracts. Misclassifying a mineral can result in invalid claims or improper leases."
    ),
    reasoning_framework=(
        "Step 1: Classify the target mineral:\n"
        "  - Locatable: Metallic minerals, uncommon nonmetallics → 1872 Mining Law claims.\n"
        "  - Leasable: Coal, oil, gas, phosphate, sodium, potassium, sulfur, geothermal → MLA leases.\n"
        "  - Salable: Common varieties of sand, gravel, stone, pumice → Materials Act contracts.\n"
        "Step 2: For locatable minerals, initiate mining claim location:\n"
        "  - No government approval needed to locate claim.\n"
        "  - Must discover valuable mineral deposit.\n"
        "  - Record with county and BLM. Pay $165 annual maintenance.\n"
        "  - No royalty to federal government (unique among mineral frameworks).\n"
        "Step 3: For leasable minerals, apply through BLM:\n"
        "  - Competitive leasing: Parcels offered at BLM lease sale, bonus bid.\n"
        "  - Noncompetitive: Available if competitive lease sale receives no bids.\n"
        "  - Royalty rates: Coal 12.5% (surface), 8% (underground); oil/gas 12.5-16.67%.\n"
        "  - Lease terms: Coal 20 years + production; oil/gas 10 years + production.\n"
        "Step 4: For salable minerals, obtain materials contract from BLM:\n"
        "  - Community pits: Small quantity, low-cost.\n"
        "  - Competitive sales: Larger commercial operations.\n"
        "  - Free use permits: Government entities and nonprofits.\n"
        "Step 5: Evaluate dual-character minerals — some minerals may be both locatable and "
        "leasable depending on occurrence and association."
    ),
    key_factors=[
        "Correct classification of target mineral (locatable, leasable, salable)",
        "Land status and availability for mineral disposition",
        "Competitive vs noncompetitive disposition process",
        "Royalty, rental, and bonding obligations",
        "Term of right and continuation requirements",
        "Environmental compliance obligations by disposition type",
        "Unique advantages of mining claims (no royalty, self-initiated)"
    ],
    primary_authority=[
        "30 USC 22-54 (General Mining Law of 1872 — locatable minerals)",
        "30 USC 181-287 (Mineral Leasing Act of 1920 — leasable minerals)",
        "30 USC 601-604 (Materials Act of 1947 — salable minerals)",
        "Andrus v. Charlestone Stone Products Co., 436 U.S. 604 (1978)",
        "43 CFR Parts 3100-3500 (BLM leasing regulations)"
    ],
    burden_holder="Mineral claimant/lessee bears burden to use correct disposition mechanism for the mineral type",
    adversary_position=(
        "Reform advocates argue the three-tiered system is incoherent and that all federal minerals "
        "should be subject to leasing with royalties, eliminating the 1872 Mining Law's royalty-free "
        "mining claims for hardrock minerals."
    ),
    counter_arguments=[
        "Three-tiered system reflects different economic characteristics of mineral types",
        "Mining claims incentivize exploration and development of metallic minerals",
        "Leasing system provides government revenue while controlling development pace",
        "Materials Act handles high-volume, low-value construction minerals efficiently",
        "Congressional intent maintained through 150+ years of legislative action"
    ],
    resolution_strategy=(
        "Correctly classify the target mineral. If locatable, initiate mining claims with proper "
        "recording and maintenance. If leasable, apply through BLM lease process. If salable, "
        "request materials contract. Engage mineral law attorney for edge cases where "
        "classification is ambiguous. Ensure all environmental compliance requirements met."
    ),
    entity_scope=["mining operators", "BLM", "mineral law attorneys", "geological consultants"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — well-established three-tiered statutory framework",
    controlling_precedent="Andrus v. Charlestone Stone Products Co., 436 U.S. 604 (1978)"
)

# =============================================================================
# DOCTRINE BLOCK 19: STATE MINERAL SEVERANCE TAXES
# =============================================================================
STATE_SEVERANCE_TAXES = DoctrineBlock(
    topic="state_mineral_severance_taxes",
    keywords=["severance tax", "mineral tax", "production tax", "coal severance", "mining tax", "extraction tax", "state tax mineral"],
    conclusion_template=(
        "State mineral severance taxes are imposed on the extraction of minerals from the earth, "
        "typically calculated as a percentage of gross value or a per-unit rate. Every major "
        "mineral-producing state imposes some form of severance tax. Rates and structures vary "
        "widely: Wyoming imposes 7% on surface coal; West Virginia imposes 5% on coal; Montana "
        "imposes variable rates depending on coal type and mining method. The Commerce Clause "
        "limits discriminatory state taxation of minerals destined for interstate commerce, as "
        "established in Commonwealth Edison Co. v. Montana. Severance taxes directly affect mineral "
        "valuation, lease economics, and investment decisions."
    ),
    reasoning_framework=(
        "Step 1: Identify all applicable state severance taxes for the mineral type:\n"
        "  - Coal: WY 7% surface/3.75% underground; WV 5%; MT variable; PA none (but Act 54 impact fee).\n"
        "  - Metallic minerals: NV 5% net proceeds; AZ 2.5%; MN taconite production tax.\n"
        "  - Sand/gravel: Generally lower rates or exempt.\n"
        "  - Uranium: NM 3.5%; WY 4%.\n"
        "Step 2: Determine the tax base — gross value, net value (after deductions), or per-unit.\n"
        "Step 3: Identify available deductions and credits:\n"
        "  - Transportation cost deductions (mine mouth to market).\n"
        "  - Processing cost deductions (beneficiation, washing).\n"
        "  - Tax credits for reclamation expenditures.\n"
        "  - Small producer exemptions.\n"
        "Step 4: Evaluate Commerce Clause limitations — tax must: (1) apply to activity with "
        "substantial nexus; (2) be fairly apportioned; (3) not discriminate against interstate "
        "commerce; (4) be fairly related to services provided by the state (Complete Auto Transit).\n"
        "Step 5: Assess impact on mineral valuation — severance tax is typically deducted before "
        "calculating royalty or net revenue interest payments.\n"
        "Step 6: Evaluate multi-state taxation risks if minerals are processed in a different state "
        "from extraction — avoid double taxation."
    ),
    key_factors=[
        "Applicable state severance tax rate and base",
        "Available deductions (transportation, processing, royalties)",
        "Tax credits and small producer exemptions",
        "Commerce Clause compliance",
        "Impact on mineral valuation and lease economics",
        "Multi-state taxation risks",
        "Local government production taxes in addition to state severance"
    ],
    primary_authority=[
        "Commonwealth Edison Co. v. Montana, 453 U.S. 609 (1981)",
        "Complete Auto Transit v. Brady, 430 U.S. 274 (1977) — four-part tax test",
        "Wyo. Stat. § 39-14-101 et seq. (Wyoming mineral severance tax)",
        "W.Va. Code § 11-13A (West Virginia severance tax)",
        "Mont. Code Ann. § 15-35 (Montana coal severance tax)"
    ],
    burden_holder="Taxpayer bears burden to claim deductions and credits; state bears burden to show tax is not discriminatory",
    adversary_position=(
        "Mining companies argue that high severance tax rates make domestic production "
        "uncompetitive with foreign imports, particularly for coal competing with natural gas, "
        "and that severance taxes are effectively exported to consuming states."
    ),
    counter_arguments=[
        "Commonwealth Edison upheld Montana's 30% coal severance tax as constitutional",
        "Severance taxes compensate states for depletion of non-renewable resources",
        "States providing infrastructure (roads, utilities, emergency services) for mining deserve revenue",
        "Tax competition among states prevents truly confiscatory rates",
        "Deductions for transportation and processing reduce effective tax rate significantly"
    ],
    resolution_strategy=(
        "Map all applicable severance taxes before committing to development. Model net economics "
        "including all tax obligations. Maximize available deductions and credits. Structure "
        "operations to avoid multi-state double taxation. Factor severance taxes into mineral "
        "valuation for acquisitions and divestitures."
    ),
    entity_scope=["mining companies", "state tax authorities", "mineral appraisers", "royalty owners"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — well-established tax frameworks; Commerce Clause limits well-defined",
    controlling_precedent="Commonwealth Edison Co. v. Montana, 453 U.S. 609 (1981)"
)

# =============================================================================
# DOCTRINE BLOCK 20: ANNUAL ASSESSMENT WORK AND MAINTENANCE FEES
# =============================================================================
ANNUAL_ASSESSMENT_MAINTENANCE = DoctrineBlock(
    topic="annual_assessment_work_maintenance_fees",
    keywords=["assessment work", "maintenance fee", "annual work", "claim maintenance", "blm fee", "165 dollar", "labor requirement"],
    conclusion_template=(
        "Maintaining unpatented mining claims requires annual compliance with either the $165 "
        "per-claim maintenance fee payment to BLM (30 USC 28f) or performance of $100 per-claim "
        "assessment work (30 USC 28). The maintenance fee system was established in 1993 as an "
        "alternative to physical assessment work. Claims for which neither the fee is paid nor "
        "assessment work is performed by September 1 of each year are deemed abandoned and void. "
        "Small miners holding 10 or fewer claims may file a waiver certifying assessment work "
        "performance in lieu of paying the fee. Failure to timely comply is jurisdictionally "
        "fatal — the claim is automatically forfeited, and relocation by a third party is permitted."
    ),
    reasoning_framework=(
        "Step 1: Determine claim count — if 10 or fewer claims, eligible for small miner waiver.\n"
        "Step 2: Choose maintenance method:\n"
        "  - Maintenance fee: $165/claim/year, paid to BLM by September 1.\n"
        "  - Assessment work: $100/claim/year, physical work on or for benefit of the claim.\n"
        "  - Small miner waiver: Certify assessment work in lieu of fee (≤10 claims).\n"
        "Step 3: If paying maintenance fees, ensure timely payment:\n"
        "  - Due by September 1 (noon assessment year).\n"
        "  - NO grace period. Late payment = claim forfeiture.\n"
        "  - Online payment available through BLM mining claim portal.\n"
        "Step 4: If performing assessment work, document thoroughly:\n"
        "  - Work must tend to develop or facilitate development of the mineral deposit.\n"
        "  - File affidavit of assessment work with county and BLM by December 30.\n"
        "  - Work must be performed between September 1 and September 1 of the assessment year.\n"
        "Step 5: Verify BLM records match claim records — discrepancies can cause automatic forfeiture.\n"
        "Step 6: Calendar all deadlines with multiple reminders — this is the single most common "
        "cause of mining claim loss."
    ),
    key_factors=[
        "Number of claims held (determines small miner waiver eligibility)",
        "Timely payment of maintenance fees by September 1 deadline",
        "Adequate documentation of assessment work if work performed",
        "BLM record accuracy for claim status",
        "State-specific recording requirements in addition to BLM",
        "No grace period — deadline is jurisdictionally absolute",
        "Risk of adverse relocation by third parties on forfeited claims"
    ],
    primary_authority=[
        "30 USC 28 (Assessment work requirement)",
        "30 USC 28f-28k (Maintenance fee provisions)",
        "43 CFR 3834 (BLM maintenance fee regulations)",
        "Kunkes v. United States, 78 Fed. Cl. 209 (2007)",
        "Locke v. United States (claim forfeiture for untimely filing)"
    ],
    burden_holder="Mining claimant bears absolute burden to maintain claims through timely fee payment or assessment work",
    adversary_position=(
        "Competing claimants and BLM argue that the maintenance requirement is clear, mandatory, "
        "and without exception — any failure to comply, regardless of hardship, results in "
        "automatic forfeiture with no right of reinstatement."
    ),
    counter_arguments=[
        "Maintenance fee system simplifies compliance compared to assessment work",
        "Online payment portal reduces risk of delivery failures",
        "$165/claim fee is modest relative to mineral claim value",
        "Small miner waiver preserves traditional assessment work option",
        "Calendar management systems eliminate the most common cause of forfeiture"
    ],
    resolution_strategy=(
        "Implement calendar system with multiple reminders 60, 30, and 7 days before September 1 "
        "deadline. Use BLM online payment portal. Verify BLM claim records annually for accuracy. "
        "If performing assessment work, document thoroughly with photos, invoices, and affidavit "
        "filed with both county and BLM. For large claim portfolios, consider retaining mining "
        "claim service company to manage maintenance compliance."
    ),
    entity_scope=["mining claimants", "BLM", "claim service companies", "competing claimants"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — absolute deadline requirement with no discretion or grace period",
    controlling_precedent="30 USC 28f (Maintenance fee requirement)"
)

# =============================================================================
# DOCTRINE BLOCK 21: PATENT VS UNPATENTED MINING CLAIMS
# =============================================================================
PATENT_VS_UNPATENTED = DoctrineBlock(
    topic="patent_vs_unpatented_mining_claims",
    keywords=["patent", "unpatented claim", "fee simple", "mineral patent", "congressional moratorium", "patenting", "perfected claim"],
    conclusion_template=(
        "A patented mining claim is one for which the federal government has issued a patent (deed) "
        "conveying fee simple title to the claimant, including both surface and mineral rights. An "
        "unpatented claim grants the claimant only possessory rights — the exclusive right to mine "
        "the mineral but not ownership of the land itself. Since 1994, Congress has imposed annual "
        "moratoriums on processing new mineral patents through Interior appropriations riders, "
        "effectively freezing the patent system. Existing patented claims are private property with "
        "full fee simple ownership. Unpatented claims require annual maintenance but can be held "
        "indefinitely as long as maintenance is performed and a valid discovery exists."
    ),
    reasoning_framework=(
        "Step 1: Determine claim status — patented or unpatented.\n"
        "  - Patented: Fee simple title issued by federal government. Full private property rights.\n"
        "  - Unpatented: Possessory right to mine. Land remains federal.\n"
        "Step 2: For patented claims:\n"
        "  - Owner has fee simple title to surface and minerals.\n"
        "  - No annual maintenance fees or assessment work required.\n"
        "  - Subject to local property taxes.\n"
        "  - Can be sold, mortgaged, devised like any real property.\n"
        "Step 3: For unpatented claims:\n"
        "  - Possessory right only — no fee simple title.\n"
        "  - Annual maintenance fee ($165) or assessment work required.\n"
        "  - Must maintain valid mineral discovery.\n"
        "  - BLM retains authority to contest validity.\n"
        "  - Subject to withdrawal, environmental regulation, and surface management.\n"
        "Step 4: Evaluate patent moratorium impact:\n"
        "  - Congressional moratorium since 1994 prevents new patent applications.\n"
        "  - Applications filed before moratorium may still be pending (grandfathered).\n"
        "  - Moratorium could be lifted by Congress at any time.\n"
        "Step 5: Assess financing implications — unpatented claims cannot be mortgaged as easily "
        "as patented claims because the claimant does not hold fee simple title."
    ),
    key_factors=[
        "Whether claim has been patented (fee simple) or remains unpatented (possessory)",
        "Status of congressional patent moratorium",
        "Whether patent application was filed before moratorium",
        "Annual maintenance obligations for unpatented claims",
        "Ability to finance, mortgage, or transfer the claim",
        "Vulnerability of unpatented claims to withdrawal or validity challenge",
        "Tax treatment differences between patented and unpatented claims"
    ],
    primary_authority=[
        "30 USC 29 (Patent application procedures)",
        "Interior Appropriations Act annual riders (patent moratorium since 1994)",
        "Best v. Humboldt Placer Mining Co., 371 U.S. 334 (1963)",
        "Wilbur v. United States ex rel. Krushnic, 280 U.S. 306 (1930)",
        "Cameron v. United States, 252 U.S. 450 (1920)"
    ],
    burden_holder="Patent applicant must demonstrate valid discovery, compliance with all statutory requirements, and payment of patent fee",
    adversary_position=(
        "Environmental groups support making the patent moratorium permanent, arguing that "
        "privatization of public lands through mineral patents at $2.50-$5.00 per acre is a "
        "giveaway of public resources."
    ),
    counter_arguments=[
        "Existing patented claims are fully vested private property rights protected by 5th Amendment",
        "Unpatented claims provide adequate mineral development rights for most purposes",
        "Patent moratorium has not significantly impacted mining operations",
        "Possessory rights under unpatented claims are sufficient for financing with specialized lenders",
        "Congressional moratorium can be lifted if policy considerations change"
    ],
    resolution_strategy=(
        "Verify claim status through BLM LR2000 records and county records. If patented, confirm "
        "chain of title like any real property. If unpatented, maintain annual maintenance and "
        "ensure valid discovery is maintained. For financing, work with lenders experienced in "
        "mining claim transactions. Document all maintenance compliance for title insurance purposes."
    ),
    entity_scope=["mining claimants", "BLM", "real estate attorneys", "mining lenders"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE — well-established distinction with clear statutory framework",
    controlling_precedent="Best v. Humboldt Placer Mining Co., 371 U.S. 334 (1963)"
)

# =============================================================================
# DOCTRINE BLOCK 22: LIMESTONE AND CALICHE QUARRYING
# =============================================================================
LIMESTONE_QUARRYING = DoctrineBlock(
    topic="limestone_caliche_quarrying_rights",
    keywords=["limestone", "caliche", "quarry", "quarrying rights", "building stone", "cement", "crushed stone", "surface mineral"],
    conclusion_template=(
        "Limestone and caliche quarrying rights occupy a contested space between surface and mineral "
        "estates. In Texas, the landmark Heinatz v. Allen (1949) established that substances near "
        "the surface (like limestone and caliche) used for road building or fill are surface estate "
        "property, but limestone of unusual commercial value (building stone, chemical-grade) may "
        "qualify as a 'mineral.' On federal lands, common limestone is a salable material under "
        "the Materials Act; uncommon varieties (rare building stone, specialty chemical grade) may "
        "be locatable. The distinction turns on whether the limestone has characteristics giving it "
        "distinct and special value compared to common limestone deposits."
    ),
    reasoning_framework=(
        "Step 1: Characterize the limestone deposit:\n"
        "  - Common limestone: Road base, aggregate, general construction → surface estate or Materials Act.\n"
        "  - Specialty limestone: Dimension stone, chemical-grade, ornamental → potentially mineral estate.\n"
        "  - Caliche: Almost universally surface estate (road base, fill material).\n"
        "Step 2: Apply state mineral classification:\n"
        "  - Texas: Heinatz test — substance in place vs surface use distinction.\n"
        "  - Oklahoma: Surface substances generally belong to surface estate.\n"
        "  - Pennsylvania: Limestone may be mineral estate under broad conveyance.\n"
        "Step 3: For federal lands, apply common variety test (McClarty):\n"
        "  - Common variety: Materials Act contract from BLM.\n"
        "  - Uncommon variety: Locatable under 1872 Mining Law.\n"
        "  - Test: Does the deposit have unique properties giving it special value?\n"
        "Step 4: Evaluate zoning and environmental permits:\n"
        "  - Quarrying requires local zoning approval in most jurisdictions.\n"
        "  - Air quality permit for dust emissions.\n"
        "  - Stormwater pollution prevention plan (SWPPP).\n"
        "  - Blasting permits where explosives used.\n"
        "Step 5: Assess reclamation requirements — state and local requirements for quarry "
        "reclamation vary widely. Some require progressive backfill; others allow water-filled "
        "quarries as end land use.\n"
        "Step 6: Evaluate water resource impacts — quarrying often intersects groundwater table, "
        "requiring dewatering permits and aquifer impact assessment."
    ),
    key_factors=[
        "Limestone quality and intended commercial use",
        "State mineral classification doctrine",
        "Common vs uncommon variety (federal lands)",
        "Deed language regarding surface minerals and substances",
        "Local zoning and environmental permit requirements",
        "Groundwater impact and dewatering requirements",
        "Reclamation standards and end land use plans"
    ],
    primary_authority=[
        "Heinatz v. Allen, 217 S.W.2d 994 (Tex. 1949)",
        "Reed v. Wylie, 597 S.W.2d 743 (Tex. 1980)",
        "30 USC 601 (Materials Act of 1947)",
        "United States v. McClarty, 17 IBLA 68 (1974)",
        "Moser v. United States Steel Corp., 676 S.W.2d 99 (Tex. 1984)"
    ],
    burden_holder="Party claiming limestone as mineral (not surface estate) bears burden to demonstrate special characteristics",
    adversary_position=(
        "Mineral estate owners argue that any commercially valuable substance beneath the surface "
        "is a mineral regardless of its composition, and that excluding limestone from mineral "
        "conveyances based on its 'common' nature is arbitrary."
    ),
    counter_arguments=[
        "Surface substances doctrine prevents mineral estate from consuming the surface estate",
        "Common limestone lacks the unique characteristics that define a mineral under most states' tests",
        "Texas surface-destruction test (Moser) protects surface estate from total consumption",
        "Federal Materials Act specifically addresses disposition of common stone varieties",
        "Quality-based distinction (common vs uncommon) provides workable classification standard"
    ],
    resolution_strategy=(
        "Characterize the limestone deposit through geological and chemical analysis. Apply "
        "applicable state classification doctrine. If on federal land, submit to BLM common "
        "variety determination. Secure all local zoning and environmental permits. Negotiate "
        "surface use agreement if split estate. Plan quarry development with progressive "
        "reclamation to satisfy regulatory requirements."
    ),
    entity_scope=["quarry operators", "surface owners", "mineral owners", "BLM", "local planning authorities"],
    confidence="AGGRESSIVE",
    confidence_stratification="AGGRESSIVE — classification depends on quality characterization and state doctrine variations",
    controlling_precedent="Heinatz v. Allen, 217 S.W.2d 994 (Tex. 1949)"
)


# =============================================================================
# MASTER DOCTRINE REGISTRY
# =============================================================================
ALL_DOCTRINES: list[DoctrineBlock] = [
    SMCRA_FEDERAL_FRAMEWORK,
    STATE_PRIMACY_PROGRAMS,
    BROAD_FORM_DEED,
    CBM_OWNERSHIP,
    GENERAL_MINING_LAW_1872,
    LODE_VS_PLACER_CLAIMS,
    SPLIT_MINERAL_ESTATE,
    SUBSURFACE_TRESPASS,
    LATERAL_SUPPORT,
    URANIUM_MINING_NRC,
    RECLAMATION_BONDING,
    SURFACE_OWNER_CONSENT,
    GEOTHERMAL_LEASING,
    LITHIUM_RARE_EARTH,
    CARBON_SEQUESTRATION_PORE_SPACE,
    HELIUM_EXTRACTION,
    AGGREGATE_EXTRACTION,
    MINING_LEASE_VS_CLAIM,
    STATE_SEVERANCE_TAXES,
    ANNUAL_ASSESSMENT_MAINTENANCE,
    PATENT_VS_UNPATENTED,
    LIMESTONE_QUARRYING,
]


def get_all_doctrines() -> list[DoctrineBlock]:
    """Return all doctrine blocks."""
    return ALL_DOCTRINES


def get_doctrine_by_topic(topic: str) -> DoctrineBlock | None:
    """Retrieve a specific doctrine block by topic identifier."""
    for doctrine in ALL_DOCTRINES:
        if doctrine.topic == topic:
            return doctrine
    return None


def search_doctrines(query: str) -> list[DoctrineBlock]:
    """Search doctrines by keyword match against topic and keywords list."""
    query_lower = query.lower().strip()
    results: list[DoctrineBlock] = []
    for doctrine in ALL_DOCTRINES:
        score = 0
        if query_lower in doctrine.topic.lower():
            score += 10
        for kw in doctrine.keywords:
            if query_lower in kw.lower():
                score += 5
            elif kw.lower() in query_lower:
                score += 3
        if query_lower in doctrine.conclusion_template.lower():
            score += 2
        if score > 0:
            results.append(doctrine)
    return results


def get_doctrine_topics() -> list[str]:
    """Return list of all doctrine topic identifiers."""
    return [d.topic for d in ALL_DOCTRINES]


def get_doctrine_count() -> int:
    """Return total number of doctrine blocks."""
    return len(ALL_DOCTRINES)
