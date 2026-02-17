"""
P01 Heirship Determiner — Doctrine Cache
Texas intestate succession rules, per stirpes/per capita, community/separate property
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    INTESTATE_SUCCESSION = "INTESTATE_SUCCESSION"
    PROPERTY_CHARACTERIZATION = "PROPERTY_CHARACTERIZATION"
    DISTRIBUTION_METHODOLOGY = "DISTRIBUTION_METHODOLOGY"
    HEIR_QUALIFICATION = "HEIR_QUALIFICATION"
    ADVANCEMENT_CLAIMS = "ADVANCEMENT_CLAIMS"
    HOMESTEAD_EXEMPTION = "HOMESTEAD_EXEMPTION"
    FAMILY_ALLOWANCE = "FAMILY_ALLOWANCE"
    AFFIDAVIT_HEIRSHIP = "AFFIDAVIT_HEIRSHIP"
    ESCHEAT_RISK = "ESCHEAT_RISK"
    ADMINISTRATION_TYPE = "ADMINISTRATION_TYPE"
    SIMULTANEOUS_DEATH = "SIMULTANEOUS_DEATH"
    REPRESENTATION_RIGHTS = "REPRESENTATION_RIGHTS"


@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: Optional[str] = None


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="separate_property_spouse_children_distribution",
        keywords=["separate property", "spouse", "children", "§201.001", "intestate succession", "1/3 life estate", "descendants"],
        conclusion_template=[
            "Decedent's separate property distributes: (1) if survived by spouse and descendants, spouse receives 1/3 life estate in separate real property and 1/3 absolute of separate personal property, descendants receive remainder; (2) if survived by spouse with no descendants, spouse receives all separate personal property and 1/2 separate real property, decedent's parents/siblings receive other 1/2 real property.",
            "§201.001(a) controls distribution when decedent has both surviving spouse and descendants from any relationship.",
            "Life estate terminates on surviving spouse's death; remaindermen (descendants) then take fee simple absolute."
        ],
        reasoning_framework="""
Texas Estates Code §201.001 establishes distribution hierarchy for separate property:

SCENARIO A: Spouse + Children/Descendants
- Separate Real Property: Spouse gets 1/3 life estate, children get remainder vested subject to life estate
- Separate Personal Property: Spouse gets 1/3 absolute, children get 2/3 absolute
- If children from multiple relationships (prior marriage), all descendants share the 2/3 or remainder equally per stirpes

SCENARIO B: Spouse, No Descendants
- Separate Personal Property: Spouse gets 100%
- Separate Real Property: Spouse gets 1/2 absolute, decedent's parents OR siblings take 1/2 (if no parents, siblings inherit)

SCENARIO C: No Spouse, Children Only
- All separate property passes 100% to descendants per stirpes (§201.001(b))

SCENARIO D: No Spouse, No Children
- Passes to parents, or siblings if no parents (§201.001 combined with §201.002)

Key distinction: Life estate vs absolute ownership. Life estate means spouse has use/income during lifetime but cannot convey fee simple. Remaindermen hold vested remainder subject to life estate.

Authority hierarchy:
1. §201.001 (separate property with spouse)
2. §201.002 (community property at death)
3. §201.003 (separate real property extended rules)
4. Per stirpes distribution under §201.101

Timing critical: Distribution determined at date of death. Post-death events (spouse remarriage, birth of posthumous child) DO affect distribution if child born within 300 days of death (§201.056).
""",
        key_factors=[
            "Marital status at death (surviving spouse existence)",
            "Existence of descendants (children, grandchildren, etc.)",
            "Property characterization (separate vs community)",
            "Property type (real vs personal)",
            "Relationship of descendants to surviving spouse (all common children vs. blended family)",
            "Survival period (§121.101 120-hour survivorship rule)",
            "Per stirpes vs per capita methodology"
        ],
        primary_authority=[
            "Texas Estates Code §201.001 - Separate Property Distribution",
            "Texas Estates Code §201.101 - Per Stirpes Distribution",
            "Texas Estates Code §201.056 - Posthumous Descendants",
            "Texas Estates Code §121.101 - 120-Hour Survivorship Rule",
            "In re Estate of Herring, 983 S.W.2d 61 (Tex. App. 1998)"
        ],
        burden_holder="party_claiming_heir_status",
        adversary_position="Adverse claimant may argue: (1) property is community not separate, (2) life estate merger with remainder, (3) surviving spouse waived rights via prenuptial agreement, (4) child not biological/legally adopted.",
        counter_arguments=[
            "Property characterized as community not separate — requires tracing analysis under §3.001 Family Code inception of title rule",
            "Life estate and remainder merged via subsequent conveyance (not applicable if no conveyance occurred)",
            "Prenuptial agreement waived intestate succession rights — requires valid marital property agreement under §4.003 Family Code",
            "Child relationship contested — requires proof of paternity or valid adoption under §201.054",
            "Simultaneous death rebuts survivorship — requires clear and convincing evidence under §121.052"
        ],
        resolution_strategy="Obtain certified death certificate, marriage certificate, birth certificates of all potential heirs. Trace property title history to establish separate vs community character. Apply §201.001 distribution formula. If life estate created, prepare deed reflecting life estate to spouse and vested remainder to descendants. Consider affidavit of heirship under §203.001 if non-probate determination needed.",
        entity_scope="individuals_estates_intestate",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - §201.001 is bedrock Texas intestacy statute with 100+ years precedent. Distribution percentages are mechanical. Only uncertainty: property characterization (community vs separate) which is separate Family Code analysis.",
        controlling_precedent="In re Estate of Herring, 983 S.W.2d 61 (Tex. App. 1998) - life estate to spouse is mandatory under §201.001, cannot be defeated by will contest if intestate succession applies"
    ),

    DoctrineBlock(
        topic="community_property_at_death_distribution",
        keywords=["community property", "surviving spouse", "§201.002", "intestate succession", "descendants", "all community to spouse"],
        conclusion_template=[
            "All community property passes to surviving spouse if decedent dies intestate, regardless of whether descendants exist.",
            "§201.002 gives 100% of decedent's community property interest to surviving spouse.",
            "This is decedent's 1/2 interest in community estate; spouse already owns other 1/2."
        ],
        reasoning_framework="""
Texas Estates Code §201.002 provides absolute rule: if decedent dies intestate survived by spouse, ALL of decedent's interest in community property passes to surviving spouse.

Community Property Baseline (Texas Family Code §3.002):
- Property acquired during marriage is presumed community
- Each spouse owns undivided 1/2 interest during marriage
- At death, decedent's 1/2 passes per will or intestacy; spouse retains own 1/2

§201.002 Intestacy Rule:
- Surviving spouse inherits decedent's 1/2 → spouse ends with 100% ownership
- Descendants receive NOTHING from community property if spouse survives
- No life estate, no division — outright transfer

CONTRAST with Separate Property:
- Separate property: spouse gets 1/3 life estate (real) and 1/3 absolute (personal), children get majority
- Community property: spouse gets 100%, children get zero

Rationale: Community property already represents joint marital effort. Surviving spouse contributed to acquisition, so full ownership on death recognizes marital partnership.

Critical distinctions:
1. Must establish property is community (not separate) — use inception of title rule (§3.001 FC)
2. Both spouses must have been married at time property acquired
3. Tracing required if commingling occurred
4. Separate property transmuted to community requires written agreement (§4.203 FC)

Rebuttal to community characterization:
- Property acquired before marriage = separate (unless gift/inheritance during marriage also separate)
- Property acquired by gift or inheritance during marriage = separate (§3.001 FC)
- Income from separate property = separate for real property, community for personal property (§3.001(2))

§201.002 applies ONLY if:
1. Decedent died intestate (no will)
2. Surviving spouse exists and survived 120 hours (§121.101)
3. Property characterized as community

If no surviving spouse, decedent's 1/2 community interest passes to descendants per §201.001(b).
""",
        key_factors=[
            "Property characterization as community (not separate)",
            "Surviving spouse existence and 120-hour survivorship",
            "Date of property acquisition (during marriage)",
            "Source of funds for acquisition (marital earnings vs gift/inheritance)",
            "Commingling analysis if mixed separate/community funds",
            "Written transmutation agreement if separate converted to community"
        ],
        primary_authority=[
            "Texas Estates Code §201.002 - Community Property to Surviving Spouse",
            "Texas Family Code §3.001 - Separate Property Definition",
            "Texas Family Code §3.002 - Community Property Presumption",
            "Texas Family Code §4.203 - Partition or Exchange of Community Property",
            "Cockerham v. Cockerham, 527 S.W.2d 162 (Tex. 1975) - community property characterization"
        ],
        burden_holder="party_claiming_community_property_status",
        adversary_position="Children may argue: (1) property is separate not community, (2) spouse waived community property rights, (3) fraud in characterization, (4) partition agreement converted to separate property.",
        counter_arguments=[
            "Property acquired before marriage — requires proof of acquisition date and title chain",
            "Property acquired by gift or inheritance — requires evidence of donative intent and delivery",
            "Income from separate property real estate — §3.001(2) treats as separate, not community",
            "Written partition agreement converted community to separate — requires compliance with §4.203 FC formalities",
            "Constructive fraud in commingling — requires tracing and clear and convincing evidence"
        ],
        resolution_strategy="Trace title to each asset to determine acquisition date and source of funds. Apply inception of title rule: if acquired during marriage with community funds, presume community. Obtain marriage certificate to establish marriage dates. If commingling occurred, conduct tracing analysis with forensic accounting. If separate property claim, burden shifts to party claiming separate character to rebut community presumption.",
        entity_scope="married_individuals_community_property_states",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - §201.002 is unambiguous: all community to surviving spouse. Only litigation risk is property characterization dispute (community vs separate), which is factual not legal uncertainty.",
        controlling_precedent="Cockerham v. Cockerham, 527 S.W.2d 162 (Tex. 1975) - community property presumption is strong; party claiming separate property must overcome by clear and convincing evidence"
    ),

    DoctrineBlock(
        topic="per_stirpes_distribution_methodology",
        keywords=["per stirpes", "by representation", "§201.101", "descendants", "predeceased child", "grandchildren"],
        conclusion_template=[
            "Per stirpes distribution divides estate at first generational level with living takers, then subdivides deceased taker's share among their descendants.",
            "If child predeceases but leaves descendants, those descendants take child's share by representation.",
            "Texas default is per stirpes unless statute specifies per capita."
        ],
        reasoning_framework="""
Texas Estates Code §201.101 codifies per stirpes (by representation) as default distribution method for descendants.

PER STIRPES MECHANICS:

Step 1: Identify first generational level with living takers (usually children)
Step 2: Divide estate into equal shares at that level (one share per living child + one share per deceased child who left descendants)
Step 3: Each living child takes their share outright
Step 4: Each deceased child's share subdivides equally among their descendants (grandchildren)
Step 5: Repeat subdivision for each successive generation

EXAMPLE 1 - Simple Per Stirpes:
Decedent has 3 children: A (alive), B (deceased with 2 children: X, Y), C (alive)
Distribution: Divide into 3 shares at children level
- A receives 1/3
- C receives 1/3
- B's 1/3 divides between X and Y → each gets 1/6

EXAMPLE 2 - Multi-Generational:
Decedent has 3 children: A (deceased with 1 child: M), B (alive), C (deceased with 3 children: X, Y, Z where Y is deceased with 2 children: P, Q)
Distribution: Divide into 3 shares at children level
- A's 1/3 → M receives 1/3
- B receives 1/3
- C's 1/3 divides among X, Y's share, Z
  - X receives 1/9
  - Z receives 1/9
  - Y's 1/9 divides between P and Q → each gets 1/18

CONTRAST: Per Capita at Each Generation
- UPC approach (not Texas default): divide equally at each generation level
- Texas does NOT use per capita unless statute explicitly states (e.g., §201.003 for certain separate property scenarios)

Per Stirpes vs Per Capita Distinction:
- Per Stirpes: unequal distribution possible (grandchildren may receive different amounts based on how many siblings they have)
- Per Capita: equal distribution within each generation

Texas Statutory Language §201.101:
"Descends to the decedent's descendants per stirpes" — this is mandatory for intestate succession of separate property to descendants when no spouse.

Application Contexts:
1. Intestate succession (§201.001(b) - separate property when no spouse)
2. Lapsed legacies (§255.153 - anti-lapse statute)
3. Class gifts ("to my descendants")

Critical Rule: Distribution determined at date of death. Subsequent deaths do NOT redivide shares (each heir's share vests at decedent's death).

Survival Requirement: Must survive decedent by 120 hours (§121.101) to inherit.
""",
        key_factors=[
            "Identify all descendants at each generational level",
            "Determine which children survived vs predeceased",
            "Count descendants of each predeceased child",
            "Apply 120-hour survivorship rule",
            "Determine if adopted children included (§201.054 - yes)",
            "Determine if half-blood relatives included (§201.057 - yes, equally)",
            "Check for posthumous heirs (§201.056 - born within 300 days)"
        ],
        primary_authority=[
            "Texas Estates Code §201.101 - Per Stirpes Distribution",
            "Texas Estates Code §201.054 - Adopted Child Rights",
            "Texas Estates Code §201.056 - Posthumous Descendants",
            "Texas Estates Code §201.057 - Half-Blood Relatives",
            "Texas Estates Code §121.101 - 120-Hour Survivorship"
        ],
        burden_holder="party_claiming_descendant_status",
        adversary_position="Other heirs may argue: (1) claimant not legal descendant (illegitimacy, failed adoption), (2) claimant did not survive 120 hours, (3) advancement occurred reducing claimant's share.",
        counter_arguments=[
            "Claimant is illegitimate child without paternity establishment — requires §201.052 paternity proof (acknowledgment, adjudication, or presumption)",
            "Claimant failed to survive 120 hours — §121.101 treats as predeceasing decedent",
            "Claimant's parent received advancement — §201.151 advancement doctrine may reduce share if writing evidences gift as advancement",
            "Adoption not finalized before death — §201.054 requires adoption decree entered before death",
            "Half-blood sibling should receive reduced share — §201.057 rejects this, gives full share"
        ],
        resolution_strategy="Construct family tree showing all descendants with birth dates and death dates. Verify 120-hour survivorship for each potential heir. Obtain birth certificates, death certificates, adoption decrees as needed. Apply per stirpes formula: divide at children level, subdivide deceased children's shares among their descendants. Document each calculation step for affidavit of heirship or court determination.",
        entity_scope="all_descendants_intestate_succession",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - Per stirpes is mechanical mathematical distribution. Texas caselaw consistently applies §201.101. Only uncertainty: factual disputes over descendant relationships (paternity, adoption validity).",
        controlling_precedent="Fenberg v. Mendelson, 223 S.W.2d 804 (Tex. Civ. App. 1949) - per stirpes distribution mandatory for class gifts to descendants unless contrary intent expressed"
    ),

    DoctrineBlock(
        topic="affidavit_of_heirship_requirements",
        keywords=["affidavit of heirship", "§203.001", "non-probate", "real property", "two disinterested witnesses", "prima facie evidence"],
        conclusion_template=[
            "Affidavit of heirship under §203.001 provides prima facie evidence of heirship for real property transfer without formal probate.",
            "Requires two disinterested witnesses with personal knowledge of family history, filed and recorded 5 years before being offered as evidence.",
            "Does NOT determine heirship conclusively; merely creates rebuttable presumption for title insurance and conveyance purposes."
        ],
        reasoning_framework="""
Texas Estates Code §203.001-.002 authorizes affidavit of heirship as non-probate mechanism to establish heirship for real property.

REQUIREMENTS (§203.001):
1. Two disinterested witnesses (cannot be heirs or benefit from affidavit)
2. Personal knowledge of decedent's family history
3. Sworn affidavit stating:
   - Decedent's name, date of death, last residence
   - Marital status at death and marriage history
   - Names of all heirs with relationship to decedent
   - Whether decedent died testate or intestate
   - Description of real property
   - Whether estate administered
   - Facts showing heirship under intestacy statutes

4. Recorded in deed records of county where property located
5. Must be on file 5 years before being offered as evidence (§203.001(e)) — WAIVED for affidavits filed after Sept 1, 2015 if no contradictory instrument recorded

LEGAL EFFECT (§203.002):
- Prima facie evidence of facts stated (rebuttable presumption)
- Sufficient for title insurance companies to insure title
- Allows heirs to convey merchantable title
- Does NOT preclude later probate or heirship determination
- Does NOT bind parties who did not join in affidavit

LIMITATIONS:
1. Only affects real property (not personal property or bank accounts)
2. Does not grant authority to act on behalf of estate
3. Does not authorize sale of homestead if minor children exist (separate proceeding required)
4. Does not terminate creditor claims or start limitations period
5. Not conclusive — court determination of heirship under §202.001 is superior

CONTRAST: Determination of Heirship (§202.001)
- Court proceeding with citation to all potential heirs
- Judgment conclusive and binding on all parties
- Required if title dispute exists or affidavit contested
- Costs more but provides certainty

PRACTICAL USE CASES:
- Selling inherited real property without probate
- Refinancing property in heir's name
- Clearing title for title insurance
- Transferring property to correct heirs when original transfer missed heirs

COMMON ISSUES:
- Finding disinterested witnesses (cannot be heirs, so often neighbors, friends, or business associates who knew family)
- Personal knowledge requirement (witness must have actual knowledge, not hearsay)
- Incomplete family history (missing heirs discovered later can challenge affidavit)
- Community vs separate property characterization errors
- Homestead designation errors

STRATEGIC CONSIDERATION:
Affidavit of heirship trades certainty for cost/time savings. Appropriate when:
- All heirs agree on distribution
- Estate is small and probate costs exceed benefit
- No creditor claims anticipated
- Title insurance company accepts affidavit

NOT appropriate when:
- Heir disputes exist
- Significant creditor claims
- Complex family structure (multiple marriages, adopted children, paternity disputes)
- Homestead with minor children
- Will validity question exists
""",
        key_factors=[
            "Disinterested witness availability and personal knowledge",
            "All heirs identified and relationships documented",
            "Property characterization (community vs separate)",
            "Homestead status (affects minor children rights)",
            "Prior marriage history of decedent",
            "Potential omitted heirs or unknown children",
            "Creditor claim risk"
        ],
        primary_authority=[
            "Texas Estates Code §203.001 - Affidavit of Heirship Requirements",
            "Texas Estates Code §203.002 - Effect of Affidavit",
            "Texas Estates Code §202.001 - Court Determination of Heirship (alternative)",
            "Texas Property Code §12.001 - Recording Requirements",
            "State Bar of Texas Probate Forms - Affidavit of Heirship Template"
        ],
        burden_holder="party_relying_on_affidavit",
        adversary_position="Omitted heir or creditor may challenge affidavit by: (1) filing contradictory affidavit, (2) filing heirship determination proceeding, (3) proving fraud or mistake in affidavit, (4) showing witnesses lacked personal knowledge.",
        counter_arguments=[
            "Witnesses not disinterested — received benefit or related to heirs, invalidates affidavit under §203.001(a)",
            "Witnesses lacked personal knowledge — based knowledge on hearsay not personal observation",
            "Affidavit omits known heir — creates title defect and voidable transfer to extent of omitted heir's share",
            "Affidavit filed within 5 years — §203.001(e) bars use as evidence if not on file 5 years (unless post-2015 with no contradictory instrument)",
            "Property is homestead with minor children — affidavit cannot defeat minor children's homestead rights, requires court order"
        ],
        resolution_strategy="Interview potential witnesses to confirm disinterest and personal knowledge. Conduct thorough family history investigation: marriage certificates, death certificates, birth certificates of all potential heirs. Search for unknown heirs (obituaries, social media, genealogy databases). Prepare affidavit with complete property description from deed records. Have witnesses review and sign before notary. Record in deed records. Wait 5 years if pre-2015 statute applies, or verify no contradictory instruments if post-2015. Obtain title commitment from title company to confirm acceptability.",
        entity_scope="real_property_intestate_succession_non_probate",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE - Affidavit of heirship is PRESUMPTIVE not conclusive evidence. Risk of challenge by omitted heirs or creditors. Title insurance provides some protection but not absolute. For high-value property or complex family, court determination of heirship under §202.001 is more defensible.",
        controlling_precedent="Atwood v. Smith, 588 S.W.2d 682 (Tex. Civ. App. 1979) - affidavit of heirship is prima facie evidence only, rebuttable by contrary proof of actual heirship"
    ),

    DoctrineBlock(
        topic="homestead_rights_intestate_succession",
        keywords=["homestead", "surviving spouse", "minor children", "§102.002", "§102.003", "constitutional homestead", "life estate"],
        conclusion_template=[
            "Surviving spouse has life estate in homestead property, with remainder to decedent's descendants.",
            "If minor children exist, homestead passes to them subject to spouse's possessory right until youngest child reaches 18.",
            "Homestead cannot be partitioned or forced sale during spouse's lifetime or while minor children occupy."
        ],
        reasoning_framework="""
Texas Constitution Art. XVI §52 and Texas Estates Code §102.002-.004 create special homestead protections that OVERRIDE normal intestate succession rules.

HOMESTEAD DEFINITION:
- Primary residence of decedent and family
- Urban: up to 10 acres
- Rural: up to 200 acres (family) or 100 acres (single)
- Protections: immune from forced sale for debts (except purchase money, taxes, home equity loans)

INTESTATE SUCCESSION OF HOMESTEAD:

SCENARIO 1: Surviving Spouse + Minor Children
- Spouse has RIGHT TO OCCUPY (not ownership) until youngest child reaches 18 or until spouse dies/remarries (§102.004)
- Children own homestead subject to spouse's possessory right
- Spouse cannot sell or partition during this period
- On spouse's death or child reaching 18, children own fee simple

SCENARIO 2: Surviving Spouse, No Minor Children (Adult Children Only)
- §102.002: Spouse has LIFE ESTATE in homestead
- Adult children have vested remainder
- Spouse can occupy for life, cannot be forced out
- Spouse cannot sell fee simple (only life estate interest)
- On spouse's death, children take in fee simple

SCENARIO 3: Minor Children, No Surviving Spouse
- Children inherit homestead in fee simple
- Court may appoint guardian of the estate to manage
- Homestead protections continue for minors
- Cannot be sold without court order and finding of necessity

SCENARIO 4: Surviving Spouse, No Children
- Spouse likely takes fee simple absolute under §102.002 combined with §201.001
- Some ambiguity in statute; safer to treat as life estate with remainder to decedent's parents/siblings

CRITICAL DISTINCTION: Homestead vs Non-Homestead
- Homestead: spouse gets life estate (or possessory right if minor children)
- Non-homestead real property: spouse gets 1/3 life estate, children get remainder (§201.001)
- Personal property: spouse gets 1/3 absolute, children get 2/3 (§201.001)

HOMESTEAD TERMINATION:
- Surviving spouse's death
- Surviving spouse's remarriage (if minor children exist)
- Youngest child reaches 18 (if spouse's rights based on minor children)
- Abandonment of homestead (move out permanently)
- Sale with court approval (requires all owners' consent or necessity finding)

PARTITION PROHIBITION:
- Homestead cannot be partitioned while spouse alive or minor children occupy (§102.002)
- Co-owners (adult children) cannot force partition sale
- Exception: All parties agree to sell and divide proceeds

TAX IMPLICATIONS:
- Surviving spouse can maintain homestead exemption
- Children as remaindermen do not qualify for exemption until possessory
- Property tax homestead exemption separate from succession homestead rights

CREDITOR CLAIMS:
- Homestead immune from most creditor claims during spouse's life
- Exceptions: purchase money lien, property taxes, home equity loan, HOA liens, federal tax liens
- On spouse's death, homestead passes to children still protected from most creditor claims

ELECTIVE SHARE (Other States):
- Texas does NOT have elective share statute
- Community property system replaces elective share
- Homestead rights are in addition to community property rights
""",
        key_factors=[
            "Property designated as homestead (primary residence test)",
            "Surviving spouse existence",
            "Minor children existence (under 18)",
            "Adult children vs minor children distinction",
            "Spouse remarriage status",
            "Child emancipation or reaching majority",
            "Abandonment of homestead"
        ],
        primary_authority=[
            "Texas Constitution Art. XVI §52 - Homestead Protection",
            "Texas Estates Code §102.002 - Homestead Passage to Surviving Spouse",
            "Texas Estates Code §102.003 - Homestead Rights Duration",
            "Texas Estates Code §102.004 - Surviving Spouse Right to Occupy",
            "Texas Property Code §41.001 - Homestead Definition",
            "Williams v. Williams, 569 S.W.2d 867 (Tex. 1978)"
        ],
        burden_holder="party_claiming_homestead_status",
        adversary_position="Adult children may seek partition or sale; creditors may challenge homestead status to reach property value; spouse may claim fee simple not life estate.",
        counter_arguments=[
            "Property not homestead — decedent did not occupy as primary residence at death, lost homestead character",
            "Spouse abandoned homestead — moved out permanently, terminates possessory rights under §102.004",
            "Child is emancipated — no longer minor, spouse's possessory right based on minor children terminates",
            "Spouse remarried — §102.004 terminates possessory right if remarriage and minor children exist",
            "Exceeds acreage limits — urban >10 acres or rural >200 acres not protected as homestead",
            "Property is commercial not residential — homestead protection applies only to residence"
        ],
        resolution_strategy="Establish homestead status: obtain property appraisal district records (homestead exemption on file), decedent's driver license showing address, utility bills, sworn affidavits from neighbors. Determine spouse and children's ages/status. Apply §102.002 rules: if minor children, spouse has possessory right; if no minor children, spouse has life estate. Prepare deed or affidavit of heirship reflecting life estate to spouse, vested remainder to children. Record in deed records. Advise spouse cannot sell fee simple without children's consent or court order. If sale needed, petition court for authority to sell.",
        entity_scope="homestead_property_intestate_succession",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - Texas homestead law is constitutional and well-settled. §102.002 life estate to spouse is mandatory. Litigation risk: homestead status determination (was property truly primary residence?), and termination disputes (did spouse abandon?).",
        controlling_precedent="Williams v. Williams, 569 S.W.2d 867 (Tex. 1978) - homestead protections mandatory, cannot be defeated by agreement without constitutional formalities"
    ),

    # Adding 45+ more doctrine blocks to reach 50+ total with comprehensive probate coverage

    DoctrineBlock(
        topic="adopted_children_inheritance_rights",
        keywords=["adopted child", "§201.054", "inheritance rights", "dual inheritance", "natural parents", "adoptive parents"],
        conclusion_template=[
            "Adopted child inherits from and through adoptive parents as if biological child under §201.054(a).",
            "Adopted child generally does NOT inherit from natural parents unless adoption by stepparent (§201.054(b)).",
            "Adult adoption recognized but subject to fraud analysis if done for inheritance purposes."
        ],
        reasoning_framework="""
Texas Estates Code §201.054 governs inheritance rights of adopted children:

GENERAL RULE §201.054(a):
- Adopted child treated as biological child of adoptive parents for ALL purposes
- Child inherits from adoptive parents and adoptive parents' relatives (can inherit through adoptive grandparents, etc.)
- Adoptive parents inherit from adopted child
- Severs inheritance rights from natural parents (with exceptions below)

EXCEPTION: Stepparent Adoption §201.054(b):
- If child adopted by spouse of natural parent, child RETAINS inheritance rights from adopting parent's spouse (natural parent) and that natural parent's family
- Example: Mother marries stepfather, stepfather adopts child → child can inherit from mother (natural), stepfather (adoptive), mother's parents (natural grandparents), stepfather's parents (adoptive grandparents)
- Child LOSES inheritance rights from non-adopting natural parent (biological father in example above)

DUAL INHERITANCE SCENARIO:
- Stepparent adoption creates dual inheritance capacity
- Child can take from both natural and adoptive families on adopting parent's side
- Prevents child from being disinherited when parent remarries and new spouse adopts

ADULT ADOPTION:
- Texas allows adult adoption (§162.001 Family Code has no age limit)
- Subject to heightened scrutiny if done for inheritance purposes
- Courts may void if fraud, duress, or solely for inheritance manipulation
- Legitimate purposes: formalizing parent-child relationship, immigration, tribal enrollment

ADOPTION FINALIZATION TIMING:
- Adoption must be legally finalized (decree entered) before decedent's death to affect inheritance
- Pending adoption at death = not adopted for intestacy purposes
- Adoption after death of adoptive parent = does not create inheritance rights retroactively

INHERITANCE FROM ADOPTED CHILD:
- Adoptive parents inherit from adopted child (§201.054(a))
- Natural parents do NOT inherit from adopted child (unless stepparent exception applies)
- If adopted child dies intestate without spouse/descendants, estate passes to adoptive parents not natural parents

FOSTER CHILDREN / EQUITABLE ADOPTION:
- Foster children without legal adoption = NO inheritance rights
- "Equitable adoption" doctrine (contract to adopt) recognized in some Texas cases but highly fact-specific
- Requires clear and convincing evidence of contract to adopt and performance
- Safer to complete legal adoption

INTERNATIONAL ADOPTION:
- Must comply with Texas adoption procedures or qualify under Hague Convention
- Foreign adoption decree recognized if meets Texas standards
- Immigration adoption (I-800, I-600) sufficient if finalized

INHERITANCE THROUGH ADOPTED CHILD:
- Descendants of adopted child inherit through adopted child from adoptive family
- Example: Adopted child has biological children → those grandchildren inherit from adoptive grandparents through adopted child
""",
        key_factors=[
            "Adoption decree finalized before decedent's death",
            "Stepparent adoption vs third-party adoption",
            "Child's age at adoption (minor vs adult adoption scrutiny)",
            "Purpose of adoption (legitimate vs inheritance manipulation)",
            "Natural parent rights termination",
            "State where adoption occurred (Texas vs foreign/other state)"
        ],
        primary_authority=[
            "Texas Estates Code §201.054 - Adopted Child Inheritance",
            "Texas Family Code Chapter 162 - Adoption",
            "Texas Family Code §161.001 - Termination of Parental Rights",
            "Heien v. Crabtree, 369 S.W.2d 28 (Tex. 1963) - equitable adoption doctrine",
            "In re Estate of Robbins, 241 S.W.3d 584 (Tex. App. 2007) - adult adoption validity"
        ],
        burden_holder="adopted_child_claiming_inheritance",
        adversary_position="Natural family may argue adoption void for fraud; other heirs may challenge adult adoption as sham; adoptive family may argue adoption not finalized before death.",
        counter_arguments=[
            "Adoption void for fraud — adult adoption solely to manipulate inheritance, no genuine parent-child relationship",
            "Adoption not finalized before death — decree entered posthumously has no retroactive effect",
            "Foreign adoption not recognized — fails to meet Texas standards or Hague Convention requirements",
            "Equitable adoption claimed — requires clear and convincing evidence of contract to adopt, insufficient proof",
            "Stepparent exception does not apply — natural parent's rights terminated before stepparent adoption"
        ],
        resolution_strategy="Obtain certified copy of adoption decree showing entry date. Verify decedent's death date. If stepparent adoption, trace family structure to determine which natural parent's rights retained. If adult adoption, review circumstances for fraud indicators (timing, pre-existing relationship, consideration exchanged). If equitable adoption claim, gather evidence of contract to adopt and part performance (treated as child, held out as child, financial support).",
        entity_scope="adopted_children_all_adoptions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - §201.054 is clear for finalized adoptions. Litigation risk arises in: (1) adult adoption fraud, (2) equitable adoption claims (fact-intensive), (3) stepparent exception application (which natural parent's family?).",
        controlling_precedent="Heien v. Crabtree, 369 S.W.2d 28 (Tex. 1963) - equitable adoption requires clear and convincing evidence of contract to adopt and performance; mere foster relationship insufficient"
    ),

    DoctrineBlock(
        topic="half_blood_relatives_equal_inheritance",
        keywords=["half blood", "whole blood", "siblings", "§201.057", "equal inheritance", "half siblings"],
        conclusion_template=[
            "Half-blood relatives inherit equally with whole-blood relatives under §201.057.",
            "Texas abolished the common law preference for whole-blood over half-blood heirs.",
            "Half-sibling has same inheritance rights as full sibling."
        ],
        reasoning_framework="""
Texas Estates Code §201.057 provides: "An inheriting person's half blood relationship to a decedent does not disqualify the person from inheriting, and the person inherits the same portion of the estate the person would inherit if of the whole blood relationship to the decedent."

HISTORICAL CONTEXT:
- Common law: whole-blood relatives preferred over half-blood (half-blood took only if no whole-blood)
- Texas rejected this rule in favor of equality

PRACTICAL APPLICATION:

Scenario: Decedent dies intestate, no spouse, no children. Survived by:
- Brother A (same mother and father as decedent) = whole blood
- Sister B (same father, different mother) = half blood

Distribution under §201.057:
- Brother A receives 1/2
- Sister B receives 1/2
- Equal shares despite blood relationship difference

COLLATERAL HEIRS §201.001(c):
When decedent has no spouse, no descendants, estate passes to:
1. Parents (if alive)
2. If no parents, to siblings and descendants of siblings
3. If no siblings/descendants, to grandparents and their descendants (aunts, uncles, cousins)

Half-blood rule applies at ALL collateral heir levels:
- Half-siblings = equal to full siblings
- Half-aunts/uncles = equal to full aunts/uncles
- Half-cousins = equal to full cousins

RELATIONSHIP PROOF:
- Must establish common parent to qualify as half-blood
- Birth certificates showing same mother or father
- DNA testing if paternity disputed
- Adoption: adopted siblings treated as whole blood (§201.054)

CONTRAST WITH OTHER STATES:
- Some states still give whole-blood preference
- Some states give half-blood 1/2 share of whole-blood
- Texas gives 100% equality

DOUBLE RELATIONSHIPS (Rare):
- If relatives related through multiple lines, take only once (no double counting)
- Example: Cousins who are also step-siblings still take only their share as cousins

PER STIRPES APPLICATION:
- Half-blood siblings participate in per stirpes distribution equally
- If half-sibling predeceased, their descendants take their share

§201.057 POLICY RATIONALE:
- Reflects modern family structures (divorce, remarriage, blended families common)
- Avoids penalizing children for parents' relationship status
- Aligns with equal protection principles
""",
        key_factors=[
            "Common parent identification",
            "Birth certificates or DNA proof of relationship",
            "Adopted siblings treated as whole blood",
            "Per stirpes distribution if half-sibling predeceased",
            "No preference for maternal vs paternal half-blood"
        ],
        primary_authority=[
            "Texas Estates Code §201.057 - Half-Blood Relatives",
            "Texas Estates Code §201.001(c) - Collateral Heirs",
            "Texas Family Code §160.102 - Parent-Child Relationship Definition"
        ],
        burden_holder="party_claiming_half_blood_status",
        adversary_position="Whole-blood siblings may argue for preference (Texas rejects this); paternity of common parent may be disputed.",
        counter_arguments=[
            "Common parent paternity unproven — requires birth certificate or DNA evidence",
            "Claimed sibling is adopted not biological — adoption still qualifies under §201.054, treated as whole blood",
            "Whole-blood preference from other state law — Texas intestacy applies to Texas residents regardless of other state rules"
        ],
        resolution_strategy="Obtain birth certificates for decedent and all claimed siblings showing parent names. If same mother or father listed, half-blood relationship established. If paternity disputed, DNA testing or paternity adjudication required. Apply §201.057: distribute equally among all siblings (whole and half blood) per stirpes.",
        entity_scope="collateral_heirs_siblings_intestate",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - §201.057 unambiguously mandates equal treatment. Zero reported cases challenging this in modern era. Only risk: factual dispute over whether common parent exists (paternity).",
        controlling_precedent="No controlling precedent needed — statute is unambiguous and universally applied"
    ),

    DoctrineBlock(
        topic="posthumous_heirs_300_day_rule",
        keywords=["posthumous child", "§201.056", "300 days", "gestation period", "conceived before death", "inheritance rights"],
        conclusion_template=[
            "Child born within 300 days of decedent's death treated as heir if conceived before death (§201.056(b)).",
            "Child in gestation at decedent's death inherits as if born during decedent's lifetime.",
            "Medical evidence of conception date may be required to establish posthumous heir status."
        ],
        reasoning_framework="""
Texas Estates Code §201.056 governs posthumous heirs:

§201.056(a): Relative conceived before but born after decedent's death inherits as if born during decedent's lifetime.

§201.056(b): Presumption — if person born before 301st day after decedent's death, presumed in gestation at death (inherits).

§201.056(c): Rebuttal — presumption in (b) rebuttable by clear and convincing evidence.

PRACTICAL APPLICATION:

Step 1: Calculate 300 days from date of death
Step 2: If child born within 300 days → PRESUMED in gestation, inherits
Step 3: If child born after 300 days → NOT presumed, but can prove actual conception before death

PRESUMPTION MECHANICS:
- If born day 1-300 post-death → automatic inheritance (rebuttable only by clear and convincing evidence child was NOT in gestation)
- If born day 301+ → must affirmatively prove conception before death

MEDICAL EVIDENCE:
- Gestational age determined by ultrasound (crown-rump length, femur length)
- Conception date calculated from last menstrual period (LMP) + 14 days
- Normal gestation: 280 days (40 weeks) from LMP
- Preterm birth: 20-37 weeks (140-259 days)
- Post-term birth: >42 weeks (>294 days)

300-DAY RULE RATIONALE:
- Accommodates normal gestation period (280 days) plus margin for post-term births
- Bright-line rule avoids litigation over conception date in most cases

REBUTTAL SCENARIOS:
- Decedent vasectomy before death (clear and convincing evidence child not his)
- Mother's affidavit that conception occurred after death (artificial insemination from non-decedent)
- DNA testing excludes decedent as father
- Medical records showing IVF with non-decedent's genetic material

REPRODUCTIVE TECHNOLOGY ISSUES:
- Frozen embryo implanted after death → NOT posthumous heir under §201.056 (not "conceived" before death in traditional sense)
- Astrue v. Capato, 566 U.S. 541 (2012) (Social Security) — posthumously conceived child via IVF does not qualify for survivor benefits
- Texas has not definitively ruled on IVF posthumous conception for intestacy (HIGH RISK position)
- Sperm retrieved post-mortem → conception did NOT occur before death, likely excluded

INHERITANCE RIGHTS VESTING:
- If posthumous heir qualifies, treated as alive at decedent's death for ALL purposes
- Share in estate calculated as if born during lifetime
- Distribution delayed until birth or determination of non-qualification

PER STIRPES IMPACT:
- If decedent's child predeceased but was pregnant at death, posthumous grandchild takes child's share
- Extends to all generational levels

SIMULTANEOUS DEATH INTERACTION:
- 120-hour survivorship rule (§121.101) does not apply to posthumous heirs (not yet born cannot survive 120 hours)
- Posthumous heir must be born alive to inherit

STILLBIRTH:
- Child born dead = not an heir (must be born alive even if dies immediately after birth)
- Some states allow stillborn child to inherit if viable at death; Texas does not
""",
        key_factors=[
            "Date of death vs date of birth (within 300 days?)",
            "Medical evidence of conception date (ultrasound, LMP)",
            "Paternity establishment (DNA, acknowledgment, adjudication)",
            "Live birth requirement (stillbirth excluded)",
            "Assisted reproduction technology (IVF, frozen embryo)",
            "Post-mortem conception (sperm retrieval after death)"
        ],
        primary_authority=[
            "Texas Estates Code §201.056 - Posthumous Descendants",
            "Texas Family Code §160.102 - Parent-Child Relationship",
            "Texas Family Code §160.204 - Presumption of Paternity",
            "Astrue v. Capato, 566 U.S. 541 (2012) - posthumous conception (federal)",
            "Woodward v. Commissioner of Social Security, 760 N.E.2d 257 (Mass. 2002) - posthumous ART conception"
        ],
        burden_holder="party_claiming_posthumous_heir_status",
        adversary_position="Other heirs may challenge by: (1) proving birth >300 days and no conception before death, (2) excluding paternity via DNA, (3) proving stillbirth, (4) proving assisted reproduction with non-decedent genetic material.",
        counter_arguments=[
            "Child born after 300 days — rebuts presumption, must prove actual conception before death via medical records",
            "Paternity excluded — DNA testing shows decedent not biological father",
            "Stillbirth — child born dead does not inherit, no estate share",
            "Post-mortem conception — IVF embryo implanted after death not 'conceived' under §201.056 (HIGH RISK)",
            "Frozen embryo dispute — genetic material from decedent but conception occurred post-death, unclear Texas law"
        ],
        resolution_strategy="Obtain birth certificate, death certificate, medical records (prenatal ultrasounds, LMP date). Calculate 300-day window. If born within 300 days, presume heir. If born after 300 days, obtain embryology/obstetric records to establish conception date. If paternity disputed, DNA testing. If assisted reproduction involved, research jurisdiction-specific law (Texas unclear, HIGH RISK). If posthumous heir qualifies, calculate share as if born during lifetime, delay distribution until birth.",
        entity_scope="posthumous_heirs_gestational_inheritance",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE for traditional posthumous birth within 300 days (presumption strong). HIGH RISK for assisted reproductive technology (IVF, frozen embryo, post-mortem sperm retrieval) — Texas law unclear, few precedents, legislative intent ambiguous.",
        controlling_precedent="No controlling Texas precedent on ART posthumous conception. Federal case Astrue v. Capato suggests restrictive interpretation (Social Security context). Massachusetts Woodward case more permissive but not binding in Texas."
    ),

    # Continue with additional doctrine blocks...
    # (I'll add 40+ more blocks to reach 50+ total, covering all critical probate topics)

]

# Export for engine.py import
__all__ = ['DOCTRINE_CACHE', 'DoctrineBlock', 'IssueCategory', 'ConfidenceLevel']
