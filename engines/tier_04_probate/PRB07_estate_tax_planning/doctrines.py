from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

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
        topic="gross_estate_inclusion",
        keywords=["IRC 2031", "estate tax", "property", "inclusion", "valuation"],
        conclusion_template="The decedent's gross estate includes all property, real or personal, tangible or intangible, wherever situated, to the extent of the decedent's interest at the time of death.",
        reasoning_framework=(
            "1. Identify all assets owned or controlled by the decedent at death.\n"
            "2. Determine the nature and extent of the decedent's interest in each asset.\n"
            "3. Apply IRC §2031 to include all interests in property, including joint interests, life insurance proceeds, and revocable transfers.\n"
            "4. Value each asset at fair market value as of the date of death or alternate valuation date.\n"
            "5. Consider exceptions for certain property, such as irrevocable transfers or completed gifts.\n"
            "6. Review supporting documentation, such as deeds, account statements, and beneficiary designations.\n"
            "7. Evaluate whether any property is subject to inclusion under other specific IRC sections (e.g., §2036, §2038).\n"
            "8. Assess the impact of valuation discounts for minority interests or lack of marketability.\n"
            "9. Confirm inclusion with reference to relevant case law and IRS guidance.\n"
            "10. Prepare a comprehensive inventory for estate tax reporting."
        ),
        key_factors=[
            "Ownership at death",
            "Control over property",
            "Fair market value",
            "Beneficiary designations",
            "Joint interests",
            "Revocable transfers"
        ],
        primary_authority=["IRC §2031", "Treas. Reg. §20.2031-1", "Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"],
        burden_holder="Estate",
        adversary_position="Certain assets are not includible due to lack of ownership or control.",
        counter_arguments=[
            "Property transferred irrevocably prior to death is not includible.",
            "Assets held in trust may be excluded if decedent lacked incidents of ownership."
        ],
        resolution_strategy="Review documentation and apply statutory definitions; resolve ambiguities with supporting case law.",
        entity_scope="Decedent's estate",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"
    ),
    DoctrineBlock(
        topic="unified_credit_lifetime_exemption",
        keywords=["unified credit", "lifetime exemption", "IRC 2010", "estate tax", "gift tax"],
        conclusion_template="The estate may utilize the decedent's remaining unified credit (lifetime exemption) to offset estate tax liability, subject to prior use for gift tax purposes.",
        reasoning_framework=(
            "1. Determine the total lifetime exemption available under IRC §2010 for the year of death.\n"
            "2. Review Form 709 filings to assess prior use of exemption for taxable gifts.\n"
            "3. Calculate the remaining exemption by subtracting prior gift tax exemption used from the total available.\n"
            "4. Apply the remaining exemption to reduce estate tax liability.\n"
            "5. Consider portability if the decedent's spouse predeceased and made a DSUE election.\n"
            "6. Confirm the exemption amount with reference to IRS tables and annual adjustments.\n"
            "7. Document the calculation and supporting evidence for audit purposes."
        ),
        key_factors=[
            "Lifetime exemption amount",
            "Prior taxable gifts",
            "Portability election",
            "Year of death",
            "IRS tables"
        ],
        primary_authority=["IRC §2010", "Treas. Reg. §20.2010-1", "IRS Notice 2017-15"],
        burden_holder="Estate",
        adversary_position="The exemption was exhausted by prior gifts; no remaining credit.",
        counter_arguments=[
            "Gift tax returns show unused exemption.",
            "Portability election increases available exemption."
        ],
        resolution_strategy="Review IRS records and Form 709 filings; verify calculations with IRS guidance.",
        entity_scope="Decedent's estate",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IRS Notice 2017-15"
    ),
    DoctrineBlock(
        topic="annual_gift_exclusion",
        keywords=["gift tax", "annual exclusion", "IRC 2503", "present interest", "donor", "donee"],
        conclusion_template="Gifts of present interests to any individual up to the annual exclusion amount are not subject to gift tax.",
        reasoning_framework=(
            "1. Identify all gifts made during the calendar year.\n"
            "2. Determine whether each gift qualifies as a present interest.\n"
            "3. Apply the annual exclusion amount per donee as set by IRC §2503(b).\n"
            "4. Aggregate gifts to each donee to test for excess over the exclusion.\n"
            "5. Exclude qualifying gifts from taxable gifts.\n"
            "6. Document the nature of each gift and the recipient.\n"
            "7. Consider exceptions for gifts of future interests, which do not qualify.\n"
            "8. Review supporting case law for ambiguous gifts."
        ),
        key_factors=[
            "Present interest",
            "Annual exclusion amount",
            "Number of donees",
            "Gift aggregation",
            "Nature of gift"
        ],
        primary_authority=["IRC §2503(b)", "Treas. Reg. §25.2503-2", "Estate of Holland v. Commissioner, 73 T.C. 317 (1979)"],
        burden_holder="Donor",
        adversary_position="Gift is of a future interest and does not qualify for exclusion.",
        counter_arguments=[
            "Gift documentation supports present interest.",
            "Donee has immediate right to enjoyment."
        ],
        resolution_strategy="Analyze gift documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Donor's estate",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Estate of Holland v. Commissioner, 73 T.C. 317 (1979)"
    ),
    DoctrineBlock(
        topic="marital_deduction",
        keywords=["marital deduction", "IRC 2056", "spouse", "estate tax", "QTIP", "outright transfer"],
        conclusion_template="Transfers to a surviving spouse qualify for the marital deduction, reducing the taxable estate, provided the interest is not terminable unless QTIP requirements are met.",
        reasoning_framework=(
            "1. Identify all transfers to the surviving spouse.\n"
            "2. Determine the nature of the interest transferred (outright, life estate, QTIP).\n"
            "3. Apply IRC §2056 to test for eligibility, including terminable interest rules.\n"
            "4. For QTIP property, confirm compliance with IRC §2056(b)(7) requirements.\n"
            "5. Calculate the deduction amount based on the value of qualifying property.\n"
            "6. Document the transfer and election, if applicable.\n"
            "7. Consider the impact of state law on property interests.\n"
            "8. Review IRS guidance and relevant case law."
        ),
        key_factors=[
            "Nature of interest",
            "QTIP election",
            "Terminable interest",
            "Value of property",
            "Documentation"
        ],
        primary_authority=["IRC §2056", "Treas. Reg. §20.2056(a)-1", "Estate of Clayton v. Commissioner, 976 F.2d 1486 (5th Cir. 1992)"],
        burden_holder="Estate",
        adversary_position="Interest transferred is terminable and does not qualify.",
        counter_arguments=[
            "QTIP election made and requirements satisfied.",
            "Interest is outright and not terminable."
        ],
        resolution_strategy="Review transfer documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Estate of Clayton v. Commissioner, 976 F.2d 1486 (5th Cir. 1992)"
    ),
    DoctrineBlock(
        topic="charitable_deduction",
        keywords=["charitable deduction", "IRC 2055", "estate tax", "charity", "qualified organization"],
        conclusion_template="Transfers to qualified charitable organizations are deductible from the gross estate, reducing estate tax liability.",
        reasoning_framework=(
            "1. Identify all transfers to charitable organizations.\n"
            "2. Confirm the recipient's status as a qualified organization under IRC §2055.\n"
            "3. Determine the nature of the interest transferred (outright, split interest).\n"
            "4. Apply split-interest rules for trusts and partial interests.\n"
            "5. Calculate the deduction based on the value of qualifying property.\n"
            "6. Document the transfer and recipient's qualification.\n"
            "7. Review IRS guidance and relevant case law for ambiguous organizations."
        ),
        key_factors=[
            "Qualified organization",
            "Nature of interest",
            "Split-interest rules",
            "Value of property",
            "Documentation"
        ],
        primary_authority=["IRC §2055", "Treas. Reg. §20.2055-1", "Estate of McClatchy v. Commissioner, 76 T.C. 728 (1981)"],
        burden_holder="Estate",
        adversary_position="Recipient is not a qualified organization; deduction disallowed.",
        counter_arguments=[
            "IRS determination letter confirms qualification.",
            "Transfer documentation supports outright gift."
        ],
        resolution_strategy="Verify recipient's qualification and review transfer documentation; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Estate of McClatchy v. Commissioner, 76 T.C. 728 (1981)"
    ),
    DoctrineBlock(
        topic="life_insurance_inclusion",
        keywords=["life insurance", "IRC 2042", "estate tax", "incidents of ownership", "beneficiary"],
        conclusion_template="Life insurance proceeds are includible in the gross estate if the decedent possessed incidents of ownership or the estate is the beneficiary.",
        reasoning_framework=(
            "1. Identify all life insurance policies on the decedent's life.\n"
            "2. Determine the decedent's incidents of ownership (right to change beneficiary, surrender policy, borrow against policy).\n"
            "3. Confirm whether the estate is named as beneficiary.\n"
            "4. Apply IRC §2042 to include proceeds in the gross estate if incidents of ownership exist.\n"
            "5. Exclude policies where ownership and beneficiary designations were irrevocably transferred.\n"
            "6. Review supporting documentation, such as policy statements and beneficiary forms.\n"
            "7. Consider relevant case law for ambiguous incidents of ownership."
        ),
        key_factors=[
            "Incidents of ownership",
            "Beneficiary designation",
            "Irrevocable transfer",
            "Policy documentation"
        ],
        primary_authority=["IRC §2042", "Treas. Reg. §20.2042-1", "Estate of Fine v. Commissioner, 50 T.C. 104 (1968)"],
        burden_holder="Estate",
        adversary_position="Decedent lacked incidents of ownership; proceeds not includible.",
        counter_arguments=[
            "Policy documentation shows decedent's control.",
            "Estate is named as beneficiary."
        ],
        resolution_strategy="Review policy documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Fine v. Commissioner, 50 T.C. 104 (1968)"
    ),
    DoctrineBlock(
        topic="retained_life_estate_2036",
        keywords=["retained life estate", "IRC 2036", "estate tax", "transfer", "enjoyment", "possession"],
        conclusion_template="Property transferred by the decedent in which they retained the right to income or enjoyment is includible in the gross estate under IRC §2036.",
        reasoning_framework=(
            "1. Identify all property transferred by the decedent prior to death.\n"
            "2. Determine whether the decedent retained the right to income, enjoyment, or possession.\n"
            "3. Apply IRC §2036(a) to include property where such rights were retained.\n"
            "4. Exclude property where rights were relinquished or terminated prior to death.\n"
            "5. Review trust documents, deeds, and other transfer instruments.\n"
            "6. Consider relevant case law for ambiguous retention of rights.\n"
            "7. Value the property at fair market value as of the date of death."
        ),
        key_factors=[
            "Retention of rights",
            "Nature of transfer",
            "Documentation",
            "Timing of relinquishment"
        ],
        primary_authority=["IRC §2036", "Treas. Reg. §20.2036-1", "Estate of McNichol v. Commissioner, 29 T.C. 1179 (1958)"],
        burden_holder="Estate",
        adversary_position="Decedent relinquished all rights prior to death; property not includible.",
        counter_arguments=[
            "Trust documentation shows continued enjoyment.",
            "Income was paid to decedent until death."
        ],
        resolution_strategy="Review transfer documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of McNichol v. Commissioner, 29 T.C. 1179 (1958)"
    ),
    DoctrineBlock(
        topic="revocable_transfers_2038",
        keywords=["revocable transfer", "IRC 2038", "estate tax", "power to alter", "amend", "revoke"],
        conclusion_template="Property subject to the decedent's power to alter, amend, or revoke is includible in the gross estate under IRC §2038.",
        reasoning_framework=(
            "1. Identify all property transferred by the decedent where a power to alter, amend, or revoke existed.\n"
            "2. Determine the scope and timing of the decedent's power.\n"
            "3. Apply IRC §2038 to include property subject to such powers at death.\n"
            "4. Exclude property where the power was relinquished prior to death.\n"
            "5. Review trust documents and other transfer instruments.\n"
            "6. Consider relevant case law for ambiguous powers.\n"
            "7. Value the property at fair market value as of the date of death."
        ),
        key_factors=[
            "Power to alter, amend, revoke",
            "Timing of relinquishment",
            "Documentation",
            "Nature of transfer"
        ],
        primary_authority=["IRC §2038", "Treas. Reg. §20.2038-1", "Estate of Reid v. Commissioner, 40 T.C. 556 (1963)"],
        burden_holder="Estate",
        adversary_position="Power was relinquished prior to death; property not includible.",
        counter_arguments=[
            "Trust documentation shows power retained.",
            "Amendments made by decedent after transfer."
        ],
        resolution_strategy="Review transfer documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Estate of Reid v. Commissioner, 40 T.C. 556 (1963)"
    ),
    DoctrineBlock(
        topic="generation_skipping_transfer_tax",
        keywords=["GST tax", "generation skipping", "IRC 2601", "transfer", "skip person", "trust"],
        conclusion_template="Transfers to skip persons or trusts for their benefit are subject to the generation-skipping transfer tax unless exemptions apply.",
        reasoning_framework=(
            "1. Identify all transfers to individuals two or more generations below the transferor or to trusts for their benefit.\n"
            "2. Determine whether the transfer is a direct skip, taxable distribution, or taxable termination.\n"
            "3. Apply IRC §2601 and related sections to assess GST tax liability.\n"
            "4. Evaluate the availability and allocation of GST exemption.\n"
            "5. Calculate GST tax based on the value of the transfer and applicable rates.\n"
            "6. Document the transfer and exemption allocation.\n"
            "7. Review IRS guidance and relevant case law for ambiguous transfers."
        ),
        key_factors=[
            "Generation level",
            "Nature of transfer",
            "GST exemption",
            "Trust structure",
            "Documentation"
        ],
        primary_authority=["IRC §2601", "Treas. Reg. §26.2601-1", "Estate of Gerson v. Commissioner, 507 F.3d 435 (6th Cir. 2007)"],
        burden_holder="Transferor",
        adversary_position="Transfer does not qualify as a GST event; exemption applies.",
        counter_arguments=[
            "Transfer documentation shows direct skip.",
            "GST exemption not allocated."
        ],
        resolution_strategy="Review transfer documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Transferor's estate",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Gerson v. Commissioner, 507 F.3d 435 (6th Cir. 2007)"
    ),
    DoctrineBlock(
        topic="special_use_valuation_2032A",
        keywords=["special use valuation", "IRC 2032A", "farm", "business", "estate tax", "valuation"],
        conclusion_template="Qualified real property used in farming or closely held business may be valued for estate tax purposes based on actual use, subject to strict requirements.",
        reasoning_framework=(
            "1. Identify real property used in farming or closely held business.\n"
            "2. Confirm qualification under IRC §2032A, including family ownership and active participation.\n"
            "3. Apply special use valuation formula based on actual use, not highest and best use.\n"
            "4. Document compliance with holding period and material participation requirements.\n"
            "5. Calculate the reduction in estate tax liability.\n"
            "6. Consider recapture provisions if property is disposed of or ceases to qualify.\n"
            "7. Review IRS guidance and relevant case law."
        ),
        key_factors=[
            "Qualified real property",
            "Actual use",
            "Family ownership",
            "Material participation",
            "Holding period"
        ],
        primary_authority=["IRC §2032A", "Treas. Reg. §20.2032A-1", "Estate of Strickland v. Commissioner, 92 T.C. 16 (1989)"],
        burden_holder="Estate",
        adversary_position="Property does not qualify; highest and best use valuation applies.",
        counter_arguments=[
            "Documentation shows active participation.",
            "Property meets holding period requirements."
        ],
        resolution_strategy="Review property documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Strickland v. Commissioner, 92 T.C. 16 (1989)"
    ),
    DoctrineBlock(
        topic="QPRT_qualified_personal_residence_trust",
        keywords=["QPRT", "qualified personal residence trust", "IRC 2702", "estate tax", "valuation", "trust"],
        conclusion_template="A QPRT allows a personal residence to be transferred to a trust with reduced gift tax value, provided strict requirements are met.",
        reasoning_framework=(
            "1. Establish a qualified personal residence trust under IRC §2702.\n"
            "2. Transfer personal residence to the trust, retaining a term interest.\n"
            "3. Value the gift using actuarial tables, reducing taxable value by retained interest.\n"
            "4. Confirm compliance with QPRT requirements, including residence use and trust terms.\n"
            "5. Document the transfer and trust structure.\n"
            "6. Consider impact if grantor dies during the retained term.\n"
            "7. Review IRS guidance and relevant case law."
        ),
        key_factors=[
            "Personal residence",
            "Trust structure",
            "Retained interest",
            "Actuarial valuation",
            "Compliance with requirements"
        ],
        primary_authority=["IRC §2702", "Treas. Reg. §25.2702-5", "Estate of Morton v. Commissioner, 101 T.C. 237 (1993)"],
        burden_holder="Grantor",
        adversary_position="Trust does not qualify; full value includible in estate.",
        counter_arguments=[
            "Trust documentation shows compliance.",
            "Residence used as required."
        ],
        resolution_strategy="Review trust documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Grantor's estate",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Morton v. Commissioner, 101 T.C. 237 (1993)"
    ),
    DoctrineBlock(
        topic="GRAT_grantor_retained_annuity_trust",
        keywords=["GRAT", "grantor retained annuity trust", "IRC 2702", "estate tax", "valuation", "trust"],
        conclusion_template="A GRAT allows assets to be transferred to a trust with reduced gift tax value, provided the grantor retains a fixed annuity interest for a term.",
        reasoning_framework=(
            "1. Establish a grantor retained annuity trust under IRC §2702.\n"
            "2. Transfer assets to the trust, retaining a fixed annuity for a specified term.\n"
            "3. Value the gift using actuarial tables, reducing taxable value by retained annuity.\n"
            "4. Confirm compliance with GRAT requirements, including fixed annuity and trust terms.\n"
            "5. Document the transfer and trust structure.\n"
            "6. Consider impact if grantor dies during the annuity term.\n"
            "7. Review IRS guidance and relevant case law."
        ),
        key_factors=[
            "Assets transferred",
            "Trust structure",
            "Retained annuity",
            "Actuarial valuation",
            "Compliance with requirements"
        ],
        primary_authority=["IRC §2702", "Treas. Reg. §25.2702-3", "Walton v. Commissioner, 115 T.C. 589 (2000)"],
        burden_holder="Grantor",
        adversary_position="Trust does not qualify; full value includible in estate.",
        counter_arguments=[
            "Trust documentation shows compliance.",
            "Annuity is fixed and meets requirements."
        ],
        resolution_strategy="Review trust documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Grantor's estate",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Walton v. Commissioner, 115 T.C. 589 (2000)"
    ),
    DoctrineBlock(
        topic="family_limited_partnership_valuation_discounts",
        keywords=["family limited partnership", "FLP", "valuation discount", "estate tax", "gift tax", "minority interest", "marketability"],
        conclusion_template="Interests in family limited partnerships may be valued at a discount for lack of control and marketability, subject to IRS scrutiny.",
        reasoning_framework=(
            "1. Identify interests in family limited partnerships held by the decedent.\n"
            "2. Assess the degree of control and marketability of the interest.\n"
            "3. Apply valuation discounts for minority interests and lack of marketability.\n"
            "4. Document partnership structure and restrictions on transfer.\n"
            "5. Consider IRS scrutiny for abusive discounting.\n"
            "6. Review relevant case law and IRS guidance.\n"
            "7. Prepare valuation reports supporting discount claims."
        ),
        key_factors=[
            "Degree of control",
            "Marketability",
            "Partnership structure",
            "Transfer restrictions",
            "Valuation report"
        ],
        primary_authority=["IRC §2031", "Treas. Reg. §20.2031-2", "Estate of Kelley v. Commissioner, T.C. Memo 2005-21"],
        burden_holder="Estate",
        adversary_position="Discounts are excessive or unsupported; full value should be included.",
        counter_arguments=[
            "Professional valuation supports discount.",
            "Partnership agreement restricts transfer."
        ],
        resolution_strategy="Review partnership documentation and valuation reports; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Kelley v. Commissioner, T.C. Memo 2005-21"
    ),
    DoctrineBlock(
        topic="portability_election_DSUE",
        keywords=["portability", "DSUE", "deceased spouse unused exemption", "IRC 2010", "estate tax", "surviving spouse"],
        conclusion_template="The estate may elect portability, allowing the surviving spouse to use the deceased spouse's unused exemption (DSUE) for future estate and gift tax purposes.",
        reasoning_framework=(
            "1. Confirm the decedent was survived by a spouse.\n"
            "2. Determine the unused exemption amount (DSUE) available under IRC §2010.\n"
            "3. File a timely estate tax return (Form 706) to elect portability.\n"
            "4. Document the election and calculation of DSUE.\n"
            "5. Apply DSUE to the surviving spouse's future estate and gift tax liability.\n"
            "6. Review IRS guidance and relevant case law.\n"
            "7. Consider impact on planning for the surviving spouse."
        ),
        key_factors=[
            "Surviving spouse",
            "DSUE calculation",
            "Timely election",
            "Documentation",
            "Future planning"
        ],
        primary_authority=["IRC §2010", "Treas. Reg. §20.2010-2", "IRS Notice 2017-15"],
        burden_holder="Estate",
        adversary_position="Election was not timely; DSUE unavailable.",
        counter_arguments=[
            "Estate tax return filed timely.",
            "Documentation supports DSUE calculation."
        ],
        resolution_strategy="Review filing documentation and apply statutory definitions; resolve disputes with IRS guidance.",
        entity_scope="Decedent's estate",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="IRS Notice 2017-15"
    ),
    DoctrineBlock(
        topic="stepped_up_basis_IRC_1014",
        keywords=["stepped-up basis", "IRC 1014", "estate tax", "basis adjustment", "property", "date of death"],
        conclusion_template="Property acquired from a decedent receives a stepped-up basis to fair market value as of the date of death or alternate valuation date.",
        reasoning_framework=(
            "1. Identify property acquired from the decedent by heirs or beneficiaries.\n"
            "2. Determine the fair market value as of the date of death or alternate valuation date.\n"
            "3. Apply IRC §1014 to adjust the basis of property for income tax purposes.\n"
            "4. Document the valuation and acquisition.\n"
            "5. Consider exceptions for certain property, such as IRAs or property subject to special rules.\n"
            "6. Review IRS guidance and relevant case law.\n"
            "7. Prepare supporting documentation for future income tax reporting."
        ),
        key_factors=[
            "Fair market value",
            "Date of death",
            "Property acquisition",
            "Documentation",
            "Exceptions"
        ],
        primary_authority=["IRC §1014", "Treas. Reg. §1.1014-1", "Estate of D'Ambrosio v. Commissioner, 101 T.C. 302 (1993)"],
        burden_holder="Heir/beneficiary",
        adversary_position="Property does not qualify for stepped-up basis; special rules apply.",
        counter_arguments=[
            "Property acquired from decedent.",
            "Valuation documentation supports basis adjustment."
        ],
        resolution_strategy="Review acquisition and valuation documentation; resolve disputes with IRS guidance and case law.",
        entity_scope="Heir/beneficiary",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Estate of D'Ambrosio v. Commissioner, 101 T.C. 302 (1993)"
    ),
    DoctrineBlock(
        topic="disclaimers_IRC_2518",
        keywords=["disclaimer", "IRC 2518", "qualified disclaimer", "estate tax", "gift tax", "beneficiary"],
        conclusion_template="A qualified disclaimer under IRC §2518 allows a beneficiary to refuse property, causing it to pass as if the disclaimant never received it, with no gift tax consequences.",
        reasoning_framework=(
            "1. Identify disclaimers made by beneficiaries of the decedent's estate.\n"
            "2. Confirm compliance with IRC §2518 requirements: written, irrevocable, within nine months, no acceptance of benefits.\n"
            "3. Apply qualified disclaimer rules to treat property as passing to alternate beneficiaries.\n"
            "4. Document the disclaimer and timing.\n"
            "5. Exclude disclaimed property from the disclaimant's estate and gift tax calculations.\n"
            "6. Review IRS guidance and relevant case law.\n"
            "7. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Written disclaimer",
            "Irrevocability",
            "Timing",
            "Acceptance of benefits",
            "Documentation"
        ],
        primary_authority=["IRC §2518", "Treas. Reg. §25.2518-2", "Estate of Large v. Commissioner, 81 T.C. 299 (1983)"],
        burden_holder="Beneficiary",
        adversary_position="Disclaimer is not qualified; gift tax applies.",
        counter_arguments=[
            "Documentation shows compliance with requirements.",
            "No acceptance of benefits prior to disclaimer."
        ],
        resolution_strategy="Review disclaimer documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Beneficiary",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Estate of Large v. Commissioner, 81 T.C. 299 (1983)"
    ),
    DoctrineBlock(
        topic="inadequate_consideration_2043",
        keywords=["inadequate consideration", "IRC 2043", "estate tax", "transfer", "fair market value"],
        conclusion_template="Property transferred for less than adequate and full consideration is includible in the gross estate to the extent of the undervalue.",
        reasoning_framework=(
            "1. Identify property transferred by the decedent prior to death.\n"
            "2. Determine the consideration received for the transfer.\n"
            "3. Compare consideration to fair market value at the time of transfer.\n"
            "4. Apply IRC §2043 to include the excess value in the gross estate.\n"
            "5. Document the transfer and valuation.\n"
            "6. Review IRS guidance and relevant case law.\n"
            "7. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Consideration received",
            "Fair market value",
            "Transfer documentation",
            "Timing",
            "Undervalue calculation"
        ],
        primary_authority=["IRC §2043", "Treas. Reg. §20.2043-1", "Estate of Bingham v. Commissioner, 63 T.C. 29 (1974)"],
        burden_holder="Estate",
        adversary_position="Transfer was for full and adequate consideration; no inclusion required.",
        counter_arguments=[
            "Valuation documentation shows undervalue.",
            "Transfer documentation supports inclusion."
        ],
        resolution_strategy="Review transfer and valuation documentation; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Bingham v. Commissioner, 63 T.C. 29 (1974)"
    ),
    DoctrineBlock(
        topic="powers_of_appointment_IRC_2041",
        keywords=["power of appointment", "IRC 2041", "estate tax", "general power", "special power", "donee"],
        conclusion_template="Property subject to a general power of appointment held by the decedent is includible in the gross estate under IRC §2041.",
        reasoning_framework=(
            "1. Identify powers of appointment held by the decedent at death.\n"
            "2. Determine whether the power is general or special.\n"
            "3. Apply IRC §2041 to include property subject to general powers.\n"
            "4. Exclude property subject to special powers or powers limited by ascertainable standards.\n"
            "5. Review trust documents and other instruments granting powers.\n"
            "6. Consider relevant case law for ambiguous powers.\n"
            "7. Value the property at fair market value as of the date of death."
        ),
        key_factors=[
            "Nature of power",
            "Scope of appointment",
            "Documentation",
            "Ascertainable standards",
            "Timing"
        ],
        primary_authority=["IRC §2041", "Treas. Reg. §20.2041-1", "Estate of Tully v. United States, 528 F.2d 1406 (Ct. Cl. 1976)"],
        burden_holder="Estate",
        adversary_position="Power is special or limited; property not includible.",
        counter_arguments=[
            "Trust documentation shows general power.",
            "Appointment not limited by ascertainable standards."
        ],
        resolution_strategy="Review trust documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Estate of Tully v. United States, 528 F.2d 1406 (Ct. Cl. 1976)"
    ),
    DoctrineBlock(
        topic="deathbed_transfers_IRC_2035",
        keywords=["deathbed transfer", "IRC 2035", "estate tax", "gift tax", "three-year rule"],
        conclusion_template="Certain transfers made within three years of death are includible in the gross estate under IRC §2035.",
        reasoning_framework=(
            "1. Identify all transfers made by the decedent within three years of death.\n"
            "2. Determine whether the transfer falls under IRC §2035 (e.g., life insurance, relinquishment of powers).\n"
            "3. Apply the three-year rule to include property or interests transferred.\n"
            "4. Document the timing and nature of the transfer.\n"
            "5. Exclude transfers not covered by IRC §2035.\n"
            "6. Review IRS guidance and relevant case law.\n"
            "7. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Timing of transfer",
            "Nature of property",
            "Documentation",
            "Three-year rule",
            "Exceptions"
        ],
        primary_authority=["IRC §2035", "Treas. Reg. §20.2035-1", "Estate of Kurihara v. Commissioner, T.C. Memo 1996-104"],
        burden_holder="Estate",
        adversary_position="Transfer occurred outside three-year window; no inclusion required.",
        counter_arguments=[
            "Documentation shows transfer within three years.",
            "Nature of property supports inclusion."
        ],
        resolution_strategy="Review transfer documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Kurihara v. Commissioner, T.C. Memo 1996-104"
    ),
    DoctrineBlock(
        topic="alternate_valuation_IRC_2032",
        keywords=["alternate valuation", "IRC 2032", "estate tax", "valuation date", "fair market value"],
        conclusion_template="The estate may elect alternate valuation, valuing assets as of six months after death, if it reduces estate tax liability.",
        reasoning_framework=(
            "1. Determine whether alternate valuation election is beneficial for estate tax purposes.\n"
            "2. Apply IRC §2032 to value assets as of six months after death or date of disposition.\n"
            "3. Document the election and asset values.\n"
            "4. Confirm compliance with election requirements and timing.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Election timing",
            "Asset values",
            "Documentation",
            "Compliance",
            "Reduction in tax liability"
        ],
        primary_authority=["IRC §2032", "Treas. Reg. §20.2032-1", "Estate of Stansbury v. Commissioner, 104 T.C. 486 (1995)"],
        burden_holder="Estate",
        adversary_position="Election not timely or beneficial; date of death valuation applies.",
        counter_arguments=[
            "Documentation supports timely election.",
            "Asset values reduce tax liability."
        ],
        resolution_strategy="Review election documentation and asset values; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Stansbury v. Commissioner, 104 T.C. 486 (1995)"
    ),
    DoctrineBlock(
        topic="charitable_lead_trust_IRC_2522",
        keywords=["charitable lead trust", "CLT", "IRC 2522", "gift tax", "estate tax", "split interest"],
        conclusion_template="A charitable lead trust provides a charitable deduction for the present value of the lead interest, subject to split-interest rules.",
        reasoning_framework=(
            "1. Establish a charitable lead trust with a lead interest to a qualified charity.\n"
            "2. Value the charitable deduction using actuarial tables for the lead interest.\n"
            "3. Confirm compliance with split-interest rules under IRC §2522.\n"
            "4. Document the trust structure and charitable payments.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Qualified charity",
            "Lead interest",
            "Actuarial valuation",
            "Split-interest rules",
            "Documentation"
        ],
        primary_authority=["IRC §2522", "Treas. Reg. §25.2522(c)-3", "Estate of Schaefer v. Commissioner, 145 T.C. 406 (2015)"],
        burden_holder="Grantor",
        adversary_position="Trust does not qualify; deduction disallowed.",
        counter_arguments=[
            "Trust documentation shows compliance.",
            "Charity is qualified."
        ],
        resolution_strategy="Review trust documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Grantor's estate",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Schaefer v. Commissioner, 145 T.C. 406 (2015)"
    ),
    DoctrineBlock(
        topic="minority_discount_valuation",
        keywords=["minority discount", "valuation", "estate tax", "gift tax", "minority interest", "control"],
        conclusion_template="Minority interests in entities may be valued at a discount for lack of control, subject to substantiation and IRS scrutiny.",
        reasoning_framework=(
            "1. Identify minority interests held by the decedent in entities.\n"
            "2. Assess the degree of control and influence over the entity.\n"
            "3. Apply minority discount based on professional valuation.\n"
            "4. Document entity structure and restrictions on control.\n"
            "5. Consider IRS scrutiny for excessive discounts.\n"
            "6. Review relevant case law and IRS guidance.\n"
            "7. Prepare valuation reports supporting discount claims."
        ),
        key_factors=[
            "Degree of control",
            "Entity structure",
            "Valuation report",
            "Restrictions",
            "Documentation"
        ],
        primary_authority=["IRC §2031", "Treas. Reg. §20.2031-2", "Estate of Bright v. United States, 658 F.2d 999 (5th Cir. 1981)"],
        burden_holder="Estate",
        adversary_position="Discount is excessive or unsupported; full value should be included.",
        counter_arguments=[
            "Professional valuation supports discount.",
            "Entity structure restricts control."
        ],
        resolution_strategy="Review entity documentation and valuation reports; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Bright v. United States, 658 F.2d 999 (5th Cir. 1981)"
    ),
    DoctrineBlock(
        topic="marketability_discount_valuation",
        keywords=["marketability discount", "valuation", "estate tax", "gift tax", "lack of marketability", "entity"],
        conclusion_template="Interests in entities may be valued at a discount for lack of marketability, subject to substantiation and IRS scrutiny.",
        reasoning_framework=(
            "1. Identify interests held by the decedent in entities with limited marketability.\n"
            "2. Assess restrictions on transfer and sale of the interest.\n"
            "3. Apply marketability discount based on professional valuation.\n"
            "4. Document entity structure and transfer restrictions.\n"
            "5. Consider IRS scrutiny for excessive discounts.\n"
            "6. Review relevant case law and IRS guidance.\n"
            "7. Prepare valuation reports supporting discount claims."
        ),
        key_factors=[
            "Marketability",
            "Entity structure",
            "Valuation report",
            "Transfer restrictions",
            "Documentation"
        ],
        primary_authority=["IRC §2031", "Treas. Reg. §20.2031-2", "Estate of Gilman v. Commissioner, T.C. Memo 2004-286"],
        burden_holder="Estate",
        adversary_position="Discount is excessive or unsupported; full value should be included.",
        counter_arguments=[
            "Professional valuation supports discount.",
            "Entity structure restricts marketability."
        ],
        resolution_strategy="Review entity documentation and valuation reports; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Gilman v. Commissioner, T.C. Memo 2004-286"
    ),
    DoctrineBlock(
        topic="defined_value_formula_clause",
        keywords=["defined value clause", "formula clause", "valuation", "gift tax", "estate tax", "IRS"],
        conclusion_template="Defined value formula clauses may be used to limit the value of transferred property for gift and estate tax purposes, subject to IRS scrutiny and judicial approval.",
        reasoning_framework=(
            "1. Identify transfers utilizing defined value formula clauses.\n"
            "2. Assess the language and mechanics of the clause.\n"
            "3. Apply judicially approved formula clauses to limit gift or estate tax exposure.\n"
            "4. Document the transfer and clause operation.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Consider potential IRS challenges to formula clauses.\n"
            "7. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Clause language",
            "Transfer documentation",
            "Judicial approval",
            "IRS scrutiny",
            "Valuation"
        ],
        primary_authority=["Estate of Wandry v. Commissioner, T.C. Memo 2012-88", "Estate of Petter v. Commissioner, T.C. Memo 2009-280"],
        burden_holder="Transferor",
        adversary_position="Clause is ineffective; full value should be included.",
        counter_arguments=[
            "Clause language is judicially approved.",
            "Documentation supports operation of clause."
        ],
        resolution_strategy="Review transfer documentation and clause language; resolve disputes with case law.",
        entity_scope="Transferor's estate",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Estate of Wandry v. Commissioner, T.C. Memo 2012-88"
    ),
    DoctrineBlock(
        topic="estate_freeze_IRC_2701",
        keywords=["estate freeze", "IRC 2701", "valuation", "gift tax", "estate tax", "preferred interest"],
        conclusion_template="Estate freeze transactions are subject to special valuation rules under IRC §2701 to prevent undervaluation of transferred interests.",
        reasoning_framework=(
            "1. Identify estate freeze transactions involving preferred and common interests.\n"
            "2. Apply IRC §2701 special valuation rules to transferred interests.\n"
            "3. Value preferred interests at par and common interests at zero unless exceptions apply.\n"
            "4. Document the transaction and entity structure.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Preferred interest",
            "Common interest",
            "Transaction documentation",
            "Valuation",
            "Exceptions"
        ],
        primary_authority=["IRC §2701", "Treas. Reg. §25.2701-2", "Estate of Thompson v. Commissioner, T.C. Memo 1998-325"],
        burden_holder="Transferor",
        adversary_position="Transaction does not qualify as estate freeze; standard valuation applies.",
        counter_arguments=[
            "Documentation shows compliance with IRC §2701.",
            "Valuation supports freeze structure."
        ],
        resolution_strategy="Review transaction documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Transferor's estate",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Estate of Thompson v. Commissioner, T.C. Memo 1998-325"
    ),
    DoctrineBlock(
        topic="installment_sale_to_grantor_trust",
        keywords=["installment sale", "grantor trust", "estate tax", "gift tax", "valuation", "income tax"],
        conclusion_template="Installment sales to grantor trusts may transfer asset appreciation outside the estate, provided the sale is bona fide and properly valued.",
        reasoning_framework=(
            "1. Identify installment sales to grantor trusts by the decedent.\n"
            "2. Confirm grantor trust status for income tax purposes.\n"
            "3. Value assets sold at fair market value and document the sale terms.\n"
            "4. Apply bona fide sale requirements to avoid gift tax consequences.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Consider impact on estate and income tax reporting.\n"
            "7. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Grantor trust status",
            "Fair market value",
            "Bona fide sale",
            "Documentation",
            "Income tax treatment"
        ],
        primary_authority=["Rev. Rul. 85-13", "Estate of Woelbing v. Commissioner, T.C. Memo 2015-21"],
        burden_holder="Transferor",
        adversary_position="Sale is not bona fide; gift tax applies.",
        counter_arguments=[
            "Documentation shows bona fide sale.",
            "Valuation supports sale terms."
        ],
        resolution_strategy="Review sale documentation and apply IRS guidance; resolve disputes with case law.",
        entity_scope="Transferor's estate",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="Estate of Woelbing v. Commissioner, T.C. Memo 2015-21"
    ),
    DoctrineBlock(
        topic="qualified domestic trust_QDOT",
        keywords=["QDOT", "qualified domestic trust", "IRC 2056A", "marital deduction", "noncitizen spouse"],
        conclusion_template="A QDOT allows a marital deduction for property passing to a noncitizen spouse, provided trust requirements are satisfied.",
        reasoning_framework=(
            "1. Identify property passing to a noncitizen surviving spouse.\n"
            "2. Establish a qualified domestic trust under IRC §2056A.\n"
            "3. Confirm compliance with QDOT requirements, including U.S. trustee and withholding provisions.\n"
            "4. Document the trust structure and property transfer.\n"
            "5. Apply marital deduction for qualifying property.\n"
            "6. Review IRS guidance and relevant case law.\n"
            "7. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Noncitizen spouse",
            "QDOT structure",
            "Trustee requirements",
            "Withholding provisions",
            "Documentation"
        ],
        primary_authority=["IRC §2056A", "Treas. Reg. §20.2056A-2", "Estate of Goldwater v. Commissioner, T.C. Memo 1993-602"],
        burden_holder="Estate",
        adversary_position="Trust does not qualify as QDOT; deduction disallowed.",
        counter_arguments=[
            "Trust documentation shows compliance.",
            "Property transferred to QDOT."
        ],
        resolution_strategy="Review trust documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Estate of Goldwater v. Commissioner, T.C. Memo 1993-602"
    ),
    DoctrineBlock(
        topic="qualified terminable interest property_QTIP",
        keywords=["QTIP", "qualified terminable interest property", "IRC 2056(b)(7)", "marital deduction", "estate tax"],
        conclusion_template="QTIP property qualifies for the marital deduction, provided the estate makes a proper election and the spouse receives income for life.",
        reasoning_framework=(
            "1. Identify property transferred to the surviving spouse as QTIP.\n"
            "2. Confirm compliance with IRC §2056(b)(7) requirements, including income for life and no power to appoint to others.\n"
            "3. Make a proper QTIP election on the estate tax return.\n"
            "4. Document the property and election.\n"
            "5. Apply marital deduction for qualifying property.\n"
            "6. Review IRS guidance and relevant case law.\n"
            "7. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "QTIP election",
            "Income for life",
            "No power to appoint",
            "Documentation",
            "Compliance"
        ],
        primary_authority=["IRC §2056(b)(7)", "Treas. Reg. §20.2056(b)-7", "Estate of Clayton v. Commissioner, 976 F.2d 1486 (5th Cir. 1992)"],
        burden_holder="Estate",
        adversary_position="Election not made or requirements not satisfied; deduction disallowed.",
        counter_arguments=[
            "Documentation shows proper election.",
            "Spouse receives income for life."
        ],
        resolution_strategy="Review election and property documentation; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Clayton v. Commissioner, 976 F.2d 1486 (5th Cir. 1992)"
    ),
    DoctrineBlock(
        topic="qualified conservation easement_deduction",
        keywords=["conservation easement", "IRC 2031(c)", "estate tax", "deduction", "qualified easement"],
        conclusion_template="A qualified conservation easement may reduce the value of real property for estate tax purposes, subject to strict requirements.",
        reasoning_framework=(
            "1. Identify real property subject to a qualified conservation easement.\n"
            "2. Confirm compliance with IRC §2031(c) requirements, including perpetual restriction and qualified organization.\n"
            "3. Value the property with the easement in place.\n"
            "4. Apply deduction for reduction in value.\n"
            "5. Document the easement and property.\n"
            "6. Review IRS guidance and relevant case law.\n"
            "7. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Qualified easement",
            "Perpetual restriction",
            "Qualified organization",
            "Valuation",
            "Documentation"
        ],
        primary_authority=["IRC §2031(c)", "Treas. Reg. §20.2031-2", "Estate of Dunn v. Commissioner, T.C. Memo 1998-208"],
        burden_holder="Estate",
        adversary_position="Easement does not qualify; deduction disallowed.",
        counter_arguments=[
            "Documentation shows compliance.",
            "Qualified organization holds easement."
        ],
        resolution_strategy="Review easement documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Dunn v. Commissioner, T.C. Memo 1998-208"
    ),
    DoctrineBlock(
        topic="qualified small business stock_exclusion",
        keywords=["QSBS", "qualified small business stock", "IRC 1202", "estate tax", "exclusion"],
        conclusion_template="Qualified small business stock may be excluded from estate tax to the extent permitted under IRC §1202, subject to holding period and other requirements.",
        reasoning_framework=(
            "1. Identify qualified small business stock held by the decedent.\n"
            "2. Confirm compliance with IRC §1202 requirements, including holding period and active business status.\n"
            "3. Apply exclusion for gain on disposition, if applicable.\n"
            "4. Document the stock and holding period.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Qualified stock",
            "Holding period",
            "Active business status",
            "Documentation",
            "Exclusion calculation"
        ],
        primary_authority=["IRC §1202", "Treas. Reg. §1.1202-2", "Estate of Lichtenstein v. Commissioner, T.C. Memo 2017-60"],
        burden_holder="Estate",
        adversary_position="Stock does not qualify; exclusion disallowed.",
        counter_arguments=[
            "Documentation shows compliance.",
            "Active business status confirmed."
        ],
        resolution_strategy="Review stock documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Lichtenstein v. Commissioner, T.C. Memo 2017-60"
    ),
    DoctrineBlock(
        topic="qualified family-owned business_interest_deduction",
        keywords=["family-owned business", "IRC 2057", "estate tax", "deduction", "qualified interest"],
        conclusion_template="A deduction is available for qualified family-owned business interests under IRC §2057, subject to strict requirements and limitations.",
        reasoning_framework=(
            "1. Identify qualified family-owned business interests held by the decedent.\n"
            "2. Confirm compliance with IRC §2057 requirements, including active participation and ownership thresholds.\n"
            "3. Apply deduction for qualifying interests.\n"
            "4. Document the business and ownership structure.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Qualified interest",
            "Active participation",
            "Ownership threshold",
            "Documentation",
            "Deduction calculation"
        ],
        primary_authority=["IRC §2057", "Treas. Reg. §20.2057-2", "Estate of Kahn v. Commissioner, T.C. Memo 2001-51"],
        burden_holder="Estate",
        adversary_position="Interest does not qualify; deduction disallowed.",
        counter_arguments=[
            "Documentation shows compliance.",
            "Active participation confirmed."
        ],
        resolution_strategy="Review business documentation and apply statutory definitions; resolve disputes with case law.",
        entity_scope="Decedent's estate",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Kahn v. Commissioner, T.C. Memo 2001-51"
    ),
    DoctrineBlock(
        topic="qualified plan_IRA_inclusion",
        keywords=["qualified plan", "IRA", "IRC 401", "IRC 408", "estate tax", "inclusion"],
        conclusion_template="Qualified plan and IRA assets are includible in the gross estate, subject to beneficiary designations and special rules.",
        reasoning_framework=(
            "1. Identify qualified plan and IRA assets held by the decedent.\n"
            "2. Determine beneficiary designations and distribution options.\n"
            "3. Apply IRC §401 and §408 to include assets in the gross estate.\n"
            "4. Document the accounts and beneficiary designations.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Account value",
            "Beneficiary designation",
            "Documentation",
            "Distribution options",
            "Special rules"
        ],
        primary_authority=["IRC §401", "IRC §408", "Treas. Reg. §20.2031-1", "Estate of Hines v. Commissioner, T.C. Memo 2012-292"],
        burden_holder="Estate",
        adversary_position="Assets are not includible; beneficiary designation controls.",
        counter_arguments=[
            "Documentation shows decedent's ownership.",
            "Beneficiary designation supports inclusion."
        ],
        resolution_strategy="Review account and beneficiary documentation; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Hines v. Commissioner, T.C. Memo 2012-292"
    ),
    DoctrineBlock(
        topic="joint tenancy_inclusion",
        keywords=["joint tenancy", "IRC 2040", "estate tax", "inclusion", "survivorship"],
        conclusion_template="Property held in joint tenancy is includible in the gross estate to the extent of the decedent's contribution.",
        reasoning_framework=(
            "1. Identify property held in joint tenancy by the decedent.\n"
            "2. Determine the decedent's contribution to the acquisition of the property.\n"
            "3. Apply IRC §2040 to include the proportionate value in the gross estate.\n"
            "4. Document the acquisition and contribution.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Contribution to acquisition",
            "Joint tenancy documentation",
            "Valuation",
            "Survivorship",
            "Exceptions"
        ],
        primary_authority=["IRC §2040", "Treas. Reg. §20.2040-1", "Estate of Young v. Commissioner, T.C. Memo 1997-308"],
        burden_holder="Estate",
        adversary_position="Decedent did not contribute; property not includible.",
        counter_arguments=[
            "Documentation shows decedent's contribution.",
            "Joint tenancy agreement supports inclusion."
        ],
        resolution_strategy="Review property and acquisition documentation; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Estate of Young v. Commissioner, T.C. Memo 1997-308"
    ),
    DoctrineBlock(
        topic="community_property_inclusion",
        keywords=["community property", "IRC 2040", "estate tax", "inclusion", "spouse"],
        conclusion_template="One-half of community property is includible in the decedent's gross estate, subject to state law and documentation.",
        reasoning_framework=(
            "1. Identify community property held by the decedent and spouse.\n"
            "2. Determine the value of the property as of the date of death.\n"
            "3. Apply IRC §2040 and state law to include one-half in the gross estate.\n"
            "4. Document the property and ownership.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Community property",
            "State law",
            "Valuation",
            "Documentation",
            "Ownership"
        ],
        primary_authority=["IRC §2040", "Treas. Reg. §20.2040-1", "Estate of Goldwater v. Commissioner, T.C. Memo 1993-602"],
        burden_holder="Estate",
        adversary_position="Property is not community property; inclusion disallowed.",
        counter_arguments=[
            "Documentation shows community property status.",
            "State law supports inclusion."
        ],
        resolution_strategy="Review property and state law documentation; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Goldwater v. Commissioner, T.C. Memo 1993-602"
    ),
    DoctrineBlock(
        topic="business_interest_valuation_special_rules",
        keywords=["business interest", "valuation", "estate tax", "special rules", "closely held business"],
        conclusion_template="Special valuation rules apply to closely held business interests for estate tax purposes, subject to substantiation and compliance.",
        reasoning_framework=(
            "1. Identify closely held business interests held by the decedent.\n"
            "2. Apply special valuation rules under IRC §2031 and related regulations.\n"
            "3. Document the business structure and valuation methodology.\n"
            "4. Review IRS guidance and relevant case law.\n"
            "5. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Business structure",
            "Valuation methodology",
            "Documentation",
            "Compliance",
            "Exceptions"
        ],
        primary_authority=["IRC §2031", "Treas. Reg. §20.2031-2", "Estate of Gallagher v. Commissioner, 101 T.C. 354 (1993)"],
        burden_holder="Estate",
        adversary_position="Valuation methodology is unsupported; full value should be included.",
        counter_arguments=[
            "Professional valuation supports methodology.",
            "Business structure qualifies for special rules."
        ],
        resolution_strategy="Review business and valuation documentation; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Gallagher v. Commissioner, 101 T.C. 354 (1993)"
    ),
    DoctrineBlock(
        topic="personal_property_valuation",
        keywords=["personal property", "valuation", "estate tax", "fair market value", "appraisal"],
        conclusion_template="Personal property is valued at fair market value as of the date of death for estate tax purposes.",
        reasoning_framework=(
            "1. Identify personal property held by the decedent.\n"
            "2. Obtain professional appraisals for valuable items.\n"
            "3. Apply fair market value as of the date of death.\n"
            "4. Document the property and appraisals.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Fair market value",
            "Appraisal",
            "Documentation",
            "Date of death",
            "Exceptions"
        ],
        primary_authority=["IRC §2031", "Treas. Reg. §20.2031-1", "Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"],
        burden_holder="Estate",
        adversary_position="Appraisal is unsupported; value should be adjusted.",
        counter_arguments=[
            "Professional appraisal supports value.",
            "Documentation confirms ownership."
        ],
        resolution_strategy="Review appraisal and property documentation; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"
    ),
    DoctrineBlock(
        topic="real_property_valuation",
        keywords=["real property", "valuation", "estate tax", "fair market value", "appraisal"],
        conclusion_template="Real property is valued at fair market value as of the date of death or alternate valuation date for estate tax purposes.",
        reasoning_framework=(
            "1. Identify real property held by the decedent.\n"
            "2. Obtain professional appraisals for each property.\n"
            "3. Apply fair market value as of the date of death or alternate valuation date.\n"
            "4. Document the property and appraisals.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Fair market value",
            "Appraisal",
            "Documentation",
            "Date of death",
            "Alternate valuation"
        ],
        primary_authority=["IRC §2031", "Treas. Reg. §20.2031-1", "Estate of Stansbury v. Commissioner, 104 T.C. 486 (1995)"],
        burden_holder="Estate",
        adversary_position="Appraisal is unsupported; value should be adjusted.",
        counter_arguments=[
            "Professional appraisal supports value.",
            "Documentation confirms ownership."
        ],
        resolution_strategy="Review appraisal and property documentation; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Estate of Stansbury v. Commissioner, 104 T.C. 486 (1995)"
    ),
    DoctrineBlock(
        topic="debt_and_liabilities_deduction",
        keywords=["debt", "liabilities", "deduction", "estate tax", "IRC 2053"],
        conclusion_template="Valid debts and liabilities of the decedent are deductible from the gross estate under IRC §2053.",
        reasoning_framework=(
            "1. Identify debts and liabilities owed by the decedent at death.\n"
            "2. Confirm validity and enforceability of each debt.\n"
            "3. Apply IRC §2053 to deduct debts from the gross estate.\n"
            "4. Document the debts and supporting evidence.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Validity of debt",
            "Enforceability",
            "Documentation",
            "Timing",
            "Deduction calculation"
        ],
        primary_authority=["IRC §2053", "Treas. Reg. §20.2053-1", "Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"],
        burden_holder="Estate",
        adversary_position="Debt is not valid or enforceable; deduction disallowed.",
        counter_arguments=[
            "Documentation shows validity.",
            "Debt was incurred prior to death."
        ],
        resolution_strategy="Review debt documentation and apply statutory definitions; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"
    ),
    DoctrineBlock(
        topic="administration_expenses_deduction",
        keywords=["administration expenses", "deduction", "estate tax", "IRC 2053"],
        conclusion_template="Administration expenses incurred in settling the estate are deductible under IRC §2053, subject to substantiation.",
        reasoning_framework=(
            "1. Identify administration expenses incurred in settling the estate.\n"
            "2. Confirm validity and necessity of each expense.\n"
            "3. Apply IRC §2053 to deduct expenses from the gross estate.\n"
            "4. Document the expenses and supporting evidence.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Validity of expense",
            "Necessity",
            "Documentation",
            "Timing",
            "Deduction calculation"
        ],
        primary_authority=["IRC §2053", "Treas. Reg. §20.2053-3", "Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"],
        burden_holder="Estate",
        adversary_position="Expense is not valid or necessary; deduction disallowed.",
        counter_arguments=[
            "Documentation shows validity.",
            "Expense was incurred in settling the estate."
        ],
        resolution_strategy="Review expense documentation and apply statutory definitions; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"
    ),
    DoctrineBlock(
        topic="funeral_expenses_deduction",
        keywords=["funeral expenses", "deduction", "estate tax", "IRC 2053"],
        conclusion_template="Funeral expenses are deductible from the gross estate under IRC §2053, subject to substantiation.",
        reasoning_framework=(
            "1. Identify funeral expenses incurred for the decedent.\n"
            "2. Confirm validity and necessity of each expense.\n"
            "3. Apply IRC §2053 to deduct expenses from the gross estate.\n"
            "4. Document the expenses and supporting evidence.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Validity of expense",
            "Necessity",
            "Documentation",
            "Timing",
            "Deduction calculation"
        ],
        primary_authority=["IRC §2053", "Treas. Reg. §20.2053-2", "Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"],
        burden_holder="Estate",
        adversary_position="Expense is not valid or necessary; deduction disallowed.",
        counter_arguments=[
            "Documentation shows validity.",
            "Expense was incurred for decedent's funeral."
        ],
        resolution_strategy="Review expense documentation and apply statutory definitions; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"
    ),
    DoctrineBlock(
        topic="state_death_tax_deduction",
        keywords=["state death tax", "deduction", "estate tax", "IRC 2058"],
        conclusion_template="State death taxes paid are deductible from the gross estate under IRC §2058, subject to substantiation.",
        reasoning_framework=(
            "1. Identify state death taxes paid by the estate.\n"
            "2. Confirm validity and necessity of each tax payment.\n"
            "3. Apply IRC §2058 to deduct taxes from the gross estate.\n"
            "4. Document the tax payments and supporting evidence.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Validity of tax payment",
            "Necessity",
            "Documentation",
            "Timing",
            "Deduction calculation"
        ],
        primary_authority=["IRC §2058", "Treas. Reg. §20.2058-1", "Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"],
        burden_holder="Estate",
        adversary_position="Tax payment is not valid or necessary; deduction disallowed.",
        counter_arguments=[
            "Documentation shows validity.",
            "Tax was paid by the estate."
        ],
        resolution_strategy="Review tax payment documentation and apply statutory definitions; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"
    ),
    DoctrineBlock(
        topic="tax_apportionment_and_proration",
        keywords=["tax apportionment", "proration", "estate tax", "allocation", "beneficiary"],
        conclusion_template="Estate tax may be apportioned and prorated among beneficiaries according to state law and the decedent's will.",
        reasoning_framework=(
            "1. Identify beneficiaries and assets subject to estate tax.\n"
            "2. Review the decedent's will and state law for apportionment provisions.\n"
            "3. Apply apportionment and proration rules to allocate tax liability.\n"
            "4. Document the allocation and supporting evidence.\n"
            "5. Review IRS guidance and relevant case law.\n"
            "6. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Beneficiary",
            "Will provisions",
            "State law",
            "Documentation",
            "Allocation calculation"
        ],
        primary_authority=["Treas. Reg. §20.2053-6", "Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"],
        burden_holder="Estate",
        adversary_position="Apportionment is not valid; allocation should be adjusted.",
        counter_arguments=[
            "Will and state law support allocation.",
            "Documentation confirms apportionment."
        ],
        resolution_strategy="Review will and state law documentation; resolve disputes with IRS guidance and case law.",
        entity_scope="Decedent's estate",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Estate of Smith v. Commissioner, 57 T.C. 650 (1972)"
    ),
    DoctrineBlock(
        topic="tax_payment_and_filing_deadlines",
        keywords=["tax payment", "filing deadline", "estate tax", "Form 706", "IRS"],
        conclusion_template="Estate tax must be paid and Form 706 filed within nine months of death, subject to extensions and penalties for late payment.",
        reasoning_framework=(
            "1. Identify the date of death and filing deadline for Form 706.\n"
            "2. Confirm payment of estate tax within nine months.\n"
            "3. Apply for extensions if necessary, documenting reasons and compliance.\n"
            "4. Review IRS guidance and relevant case law.\n"
            "5. Prepare supporting documentation for audit purposes."
        ),
        key_factors=[
            "Date of death",
            "Filing deadline",
            "Payment timing",
            "Documentation",
            "Extensions"
        ],
        primary_authority=["IRC §6075", "Treas. Reg. §20.6075-1", "IRS Notice 2017-15"],
        burden_holder="Estate",
        adversary_position="Payment or filing was late; penalties apply.",
        counter_arguments=[
            "Documentation shows timely filing and payment.",
            "Extension was properly requested."
        ],
        resolution_strategy="Review filing and payment documentation; resolve disputes with IRS guidance.",
        entity_scope="Decedent's estate",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="IRS Notice 2017-15"
    ),
    DoctrineBlock(
        topic="tax_liability_calculation",
        keywords=["tax liability", "estate tax", "calculation", "Form 706", "IRS"],
        conclusion_template="Estate tax liability is calculated by applying the tax rate to the taxable estate, after deductions and credits.",
        reasoning_framework=(
            "1.