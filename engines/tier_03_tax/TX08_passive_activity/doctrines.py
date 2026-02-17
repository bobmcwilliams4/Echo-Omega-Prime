"""
TX08 Passive Activity Loss - Doctrine Blocks
IRC §469 passive activity loss rules, material participation, rental activities, grouping
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DoctrineBlock:
    """Single doctrine block with authority and reasoning."""
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
    confidence: str
    confidence_stratification: str
    controlling_precedent: Optional[str] = None


DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="material_participation_test_1_500_hours",
        keywords=["material participation", "500 hours", "test 1", "participation standard", "hour requirement"],
        conclusion_template=[
            "Taxpayer materially participated in the activity if participation exceeded 500 hours during the tax year.",
            "The 500-hour test is the most straightforward material participation standard and requires no reference to other years or activities.",
            "Contemporaneous time logs are the gold standard for substantiation, though reconstructed records may be acceptable if credible and detailed."
        ],
        reasoning_framework="""
IRC §469(h)(1) defines material participation as involvement in operations on a regular, continuous, and substantial basis.
Temp. Reg. §1.469-5T(a)(1) provides the first test: individual participates for more than 500 hours during the year.

KEY ANALYSIS FRAMEWORK:
1. HOUR COUNTING: Only work hours count, not investment activity. Must be activity in which taxpayer owns an interest.
   - Management and operational work counts (Temp. Reg. §1.469-5T(f)(2))
   - Work in capacity as investor does NOT count (Temp. Reg. §1.469-5T(f)(2)(ii))
   - Work if not customarily done by owners and principal purpose is to avoid passive loss rules does NOT count

2. SUBSTANTIATION REQUIREMENTS:
   - Contemporaneous time logs are strongest evidence (Temp. Reg. §1.469-5T(f)(4))
   - Appointment books, calendars, narrative summaries acceptable if reasonable and credible
   - IRS may disallow vague or unsupported claims (Goshorn v. Comm'r, T.C. Memo. 2014-180)

3. HUSBAND AND WIFE AGGREGATION:
   - Each spouse's participation counted separately for material participation (Temp. Reg. §1.469-5T(f)(3))
   - Community property rules do not aggregate hours

4. EMPLOYEE VS. OWNER ANALYSIS:
   - If taxpayer also works as employee in S corp, employee hours generally count toward material participation
   - Exception: if employee compensation unreasonably low, may recharacterize as investment work

BURDEN OF PROOF: Taxpayer must substantiate hours with credible evidence.

COMMON PITFALLS:
- Including investment hours (reviewing financials, board meetings as passive investor)
- Claiming hours without any documentation
- Double-counting hours across multiple activities before grouping election
- Failing to track hours contemporaneously

PLANNING OPPORTUNITIES:
- Shift activities to exceed 500-hour threshold in a single activity
- Ensure work is operational, not investment-related
- Maintain detailed time logs from day one
""",
        key_factors=[
            "Total participation hours exceeds 500",
            "Work is operational in nature, not investment activity",
            "Taxpayer owns interest in the activity",
            "Hours substantiated with credible evidence",
            "Work customarily done by owners or has business purpose beyond PAL avoidance",
            "Spouse hours counted separately, not aggregated"
        ],
        primary_authority=[
            "IRC §469(h)(1)",
            "Temp. Reg. §1.469-5T(a)(1)",
            "Temp. Reg. §1.469-5T(f) - Rules for Determining Participation",
            "Goshorn v. Comm'r, T.C. Memo. 2014-180 (substantiation failure)"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will challenge vague hour claims, investment activity counted as participation, or lack of substantiation.",
        counter_arguments=[
            "Hours were investment activity (reviewing financials, monitoring investments) not operational work",
            "No contemporaneous records, reconstructed logs not credible",
            "Work not customarily done by owners and done solely to avoid PAL rules (sham work)",
            "Taxpayer was employee, hours should not count as owner participation",
            "Hours double-counted across multiple activities"
        ],
        resolution_strategy="Contemporaneous logs showing operational work (management, decisions, vendor relations). Employee hours generally count if reasonable compensation. Exclude investment activity. If substantiation weak, consider alternative tests (test 2, 3, 4).",
        entity_scope="individuals, trusts, estates (not C corps or PSCs)",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if >500 hours documented with contemporaneous logs showing operational work. AGGRESSIVE if relying on reconstructed records. DISCLOSURE if counting investment hours or thin substantiation."
    ),

    DoctrineBlock(
        topic="material_participation_test_2_substantially_all",
        keywords=["substantially all", "material participation", "test 2", "sole participation"],
        conclusion_template=[
            "Taxpayer materially participated if their participation constituted substantially all participation in the activity during the year.",
            "Test 2 applies where taxpayer is the primary or sole operator, regardless of total hour count.",
            "Useful for sole proprietorships or single-member LLCs where taxpayer does all the work."
        ],
        reasoning_framework="""
Temp. Reg. §1.469-5T(a)(2): Individual's participation constitutes substantially all participation in the activity.

KEY ANALYSIS FRAMEWORK:
1. SUBSTANTIALLY ALL STANDARD: No bright-line percentage, but courts generally interpret as 90%+ of total participation.
   - If others participate significantly, test 2 fails
   - Employees' participation counted in the denominator (total participation)

2. COMMON FACT PATTERNS:
   - Sole proprietor with no employees: easily meets test 2
   - Single-member LLC with minimal contractor help: likely meets test 2
   - Partnership where one partner does everything: meets test 2
   - S corp with employees doing substantial work: likely fails test 2

3. INTERACTION WITH GROUPING:
   - If activities grouped under Reg. §1.469-4, test 2 applies to grouped activity as a whole
   - May be harder to meet if grouping increases total participation by others

4. BURDEN OF PROOF: Taxpayer must show they did substantially all the work.

PLANNING OPPORTUNITIES:
- Useful for low-hour activities where taxpayer is sole operator
- Avoid hiring employees or contractors if trying to meet test 2
- Consider grouping impact on "substantially all" calculation
""",
        key_factors=[
            "Taxpayer participation as percentage of total participation",
            "Employees' and contractors' participation included in total",
            "No bright-line rule, but 90%+ generally required",
            "Applies to the activity as defined (after any grouping)"
        ],
        primary_authority=[
            "Temp. Reg. §1.469-5T(a)(2)",
            "Temp. Reg. §1.469-5T(f)(4) - determining participation"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will argue employees or contractors participated significantly, reducing taxpayer's percentage below substantially all.",
        counter_arguments=[
            "Employees performed substantial operational work",
            "Contractors or co-owners participated materially",
            "Taxpayer overstates own participation or understates others'",
            "Definition of 'substantially all' not met if others participated 15%+"
        ],
        resolution_strategy="Document that taxpayer performed 90%+ of work. Minimize employee/contractor operational roles. Show others provided ministerial support only. If close call, rely on test 1 (500 hours) instead.",
        entity_scope="individuals, trusts, estates",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if taxpayer clearly did 95%+ of work with minimal help. AGGRESSIVE if others participated 10-20%. DISCLOSURE if others participated 25%+."
    ),

    DoctrineBlock(
        topic="material_participation_test_3_100_hours_plus_not_less_than_anyone",
        keywords=["100 hours", "test 3", "not less than anyone", "equal participation"],
        conclusion_template=[
            "Taxpayer materially participated if they participated more than 100 hours and their participation was not less than any other individual's participation.",
            "Test 3 applies to activities with multiple participants where taxpayer is among the top participants.",
            "Requires both the 100-hour floor and the comparative participation standard."
        ],
        reasoning_framework="""
Temp. Reg. §1.469-5T(a)(3): Individual participates for more than 100 hours, and participation not less than any other individual.

KEY ANALYSIS FRAMEWORK:
1. TWO-PART TEST:
   Part A: Taxpayer participation >100 hours during the year
   Part B: Taxpayer's hours ≥ any other individual's hours

2. COMPARATIVE ANALYSIS:
   - Must compare to ALL individuals participating in the activity
   - Includes employees, other owners, contractors (if they are individuals)
   - Corporate employees count as individuals, but corporation itself does not

3. TIE SCENARIO: If taxpayer and another individual both participate 150 hours, taxpayer MEETS test 3 (not less than).

4. GROUPING IMPACT:
   - If activities grouped, test 3 applies to the grouped activity
   - May be harder to meet if grouping increases others' participation

5. COMMON FACT PATTERNS:
   - Partnership with equal partners each working 120 hours: each meets test 3
   - S corp where owner works 200 hours, employee works 250 hours: owner FAILS test 3
   - Rental activity where owner works 110 hours, property manager works 80 hours: owner MEETS test 3

PLANNING OPPORTUNITIES:
- Track all participants' hours, not just taxpayer's
- Consider grouping to aggregate taxpayer hours while minimizing others'
- Ensure taxpayer is primary participant if relying on test 3
""",
        key_factors=[
            "Taxpayer hours >100",
            "Taxpayer hours ≥ every other individual's hours",
            "All individuals' participation counted (owners, employees, contractors)",
            "Ties count as meeting the 'not less than' standard"
        ],
        primary_authority=[
            "Temp. Reg. §1.469-5T(a)(3)",
            "Temp. Reg. §1.469-5T(f)(4)"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will argue another individual participated more hours, disqualifying test 3.",
        counter_arguments=[
            "Employee or co-owner participated more hours than taxpayer",
            "Taxpayer counting investment hours to inflate own total",
            "Other participants' hours not properly counted",
            "Taxpayer failed to meet 100-hour floor"
        ],
        resolution_strategy="Substantiate taxpayer hours >100 with logs. Document all other individuals' hours. If close, shift to test 1 (500 hours) or test 4 (significant participation). Avoid test 3 if employees work more hours.",
        entity_scope="individuals, trusts, estates",
        confidence="MEDIUM",
        confidence_stratification="DEFENSIBLE if taxpayer clearly top participant with >100 hours documented. AGGRESSIVE if hours are close or substantiation thin. DISCLOSURE if relying on tie scenario or uncertain about others' hours."
    ),

    DoctrineBlock(
        topic="material_participation_test_4_significant_participation_aggregation",
        keywords=["significant participation", "test 4", "aggregation", "100 hours", "500 hours total"],
        conclusion_template=[
            "Taxpayer materially participated if the activity is a significant participation activity (SPA) and taxpayer's aggregate participation in all SPAs exceeds 500 hours.",
            "SPA defined as trade or business activity where taxpayer participates >100 but ≤500 hours and does not otherwise materially participate.",
            "Test 4 aggregates multiple activities to meet the 500-hour material participation threshold."
        ],
        reasoning_framework="""
Temp. Reg. §1.469-5T(a)(4): Activity is a significant participation activity, and taxpayer's aggregate participation in all SPAs >500 hours.

KEY ANALYSIS FRAMEWORK:
1. SPA DEFINITION (Temp. Reg. §1.469-5T(c)):
   - Trade or business activity (NOT rental activity - see Temp. Reg. §1.469-5T(c)(2))
   - Taxpayer participates >100 hours during the year
   - Taxpayer does NOT materially participate under tests 1, 2, 3, 5, or 6

2. AGGREGATION MECHANIC:
   Step 1: Identify all SPAs (>100 hours each, no material participation)
   Step 2: Sum participation hours across all SPAs
   Step 3: If total >500 hours, ALL SPAs treated as material participation activities

3. RENTAL ACTIVITIES EXCLUDED:
   - Rental real estate and rental personal property are NOT trade or business for test 4 purposes
   - Even if taxpayer participates >100 hours in rental, it cannot be an SPA

4. COMMON FACT PATTERNS:
   - Taxpayer operates 3 businesses: A (150 hrs), B (180 hrs), C (200 hrs). Total = 530. All three are SPAs, test 4 met for all.
   - Taxpayer operates 2 businesses: A (120 hrs), B (150 hrs). Total = 270. Both are SPAs, but test 4 NOT met (need >500).
   - Taxpayer operates business A (120 hrs) and rental B (200 hrs). Rental not SPA, test 4 NOT met (only 120 hrs counted).

5. INTERACTION WITH GROUPING:
   - If activities grouped, test 4 applies to the grouped activity
   - May GROUP multiple SPAs to create one activity meeting test 1 (500 hours)

PLANNING OPPORTUNITIES:
- Track hours across all trade or business activities
- Aggregate multiple small businesses to exceed 500-hour threshold
- Consider grouping SPAs if appropriate under Reg. §1.469-4
- Avoid mixing rentals with trade or business activities (rental hours don't count for test 4)
""",
        key_factors=[
            "Activity is trade or business (not rental)",
            "Taxpayer participation >100 hours but ≤500 hours in each SPA",
            "No material participation under tests 1-3, 5-6",
            "Aggregate participation in all SPAs >500 hours",
            "All SPAs treated as material participation if test 4 met"
        ],
        primary_authority=[
            "Temp. Reg. §1.469-5T(a)(4)",
            "Temp. Reg. §1.469-5T(c) - Significant Participation Activity"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will challenge activity classification (rental vs. trade or business), hour substantiation, or claim taxpayer materially participated under another test (disqualifying SPA status).",
        counter_arguments=[
            "Activity is rental, not trade or business, so cannot be SPA",
            "Taxpayer materially participated under test 1, 2, or 3, disqualifying SPA status",
            "Hours not substantiated or include investment activity",
            "Aggregate SPA hours ≤500, test 4 not met",
            "Grouping election changes activity definition, altering SPA analysis"
        ],
        resolution_strategy="Classify activities correctly (trade or business vs. rental). Substantiate hours in each activity. Aggregate all SPAs. If total >500, all SPAs are material participation. Consider grouping multiple SPAs to simplify. Avoid counting rental hours.",
        entity_scope="individuals, trusts, estates",
        confidence="MEDIUM",
        confidence_stratification="DEFENSIBLE if multiple trade or business activities with documented hours totaling >500. AGGRESSIVE if activity classification uncertain (rental vs. trade or business). DISCLOSURE if hours close to thresholds or substantiation weak."
    ),

    DoctrineBlock(
        topic="material_participation_test_5_prior_5_of_10_years",
        keywords=["test 5", "prior years", "5 of 10 years", "material participation history"],
        conclusion_template=[
            "Taxpayer materially participated if they materially participated in the activity for any 5 of the prior 10 tax years.",
            "Test 5 provides ongoing material participation status based on historical participation.",
            "Useful for retired individuals or those reducing involvement in long-standing activities."
        ],
        reasoning_framework="""
Temp. Reg. §1.469-5T(a)(5): Individual materially participated in the activity for any 5 (whether consecutive or not) of the 10 immediately preceding tax years.

KEY ANALYSIS FRAMEWORK:
1. LOOK-BACK PERIOD: 10 tax years immediately preceding the current year.
   - Example: For 2024, look at 2014-2023 (10 years)
   - Must have materially participated in 5 of those 10 years

2. MATERIAL PARTICIPATION STANDARD IN PRIOR YEARS:
   - Must have met one of the 7 material participation tests in each of the 5 years
   - Usually test 1 (500 hours) in prior years, but any test suffices

3. CONSECUTIVE YEARS NOT REQUIRED: Can be any 5 of the 10 years.
   - Example: Materially participated in 2014, 2016, 2018, 2020, 2022 → meets test 5 for 2024

4. ACTIVITY CONTINUITY:
   - Must be the SAME activity in prior years
   - If activity substantially changed, test 5 may not apply
   - Grouping/regrouping may affect activity definition and test 5 availability

5. COMMON FACT PATTERNS:
   - Retired business owner who worked full-time for 20 years: meets test 5 indefinitely
   - Individual who operated activity for 6 years, then reduced hours: meets test 5 for 10 years after reduction
   - New activity started in 2023: cannot use test 5 until 10 years of history exists

6. SUBSTANTIATION:
   - Must substantiate material participation in each of the 5 prior years
   - Prior year tax returns, time logs, business records as evidence

PLANNING OPPORTUNITIES:
- Useful for retirees or individuals reducing involvement
- Once 5 years of material participation established, provides 10-year window of ongoing status
- Maintain records of prior year participation for future use
""",
        key_factors=[
            "Materially participated in 5 of prior 10 tax years",
            "Any 5 years, not necessarily consecutive",
            "Same activity (continuity required)",
            "Material participation in prior years substantiated",
            "Look-back period: 10 immediately preceding years"
        ],
        primary_authority=[
            "Temp. Reg. §1.469-5T(a)(5)"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will challenge prior year material participation substantiation, activity continuity, or substantial change in activity.",
        counter_arguments=[
            "Taxpayer did not materially participate in 5 of prior 10 years",
            "Activity substantially changed, breaking continuity",
            "Prior year participation not substantiated",
            "Grouping election changed activity definition, test 5 inapplicable",
            "New activity, no prior year history"
        ],
        resolution_strategy="Substantiate material participation in 5 of prior 10 years with tax returns, time logs, business records. Ensure activity continuity (same trade or business). If activity changed, argue continuity or use different test. Useful for retirees.",
        entity_scope="individuals, trusts, estates",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if prior year material participation clearly documented for 5+ years. AGGRESSIVE if activity continuity uncertain or prior year substantiation weak. DISCLOSURE if substantial activity changes or grouping/regrouping impacts definition."
    ),

    DoctrineBlock(
        topic="material_participation_test_6_personal_service_activity_any_3_prior_years",
        keywords=["test 6", "personal service activity", "3 prior years", "health law engineering"],
        conclusion_template=[
            "Taxpayer materially participated if the activity is a personal service activity and they materially participated for any 3 prior tax years (whether consecutive or not).",
            "Personal service activity: health, law, engineering, architecture, accounting, actuarial science, performing arts, consulting, or any other trade or business where capital is not a material income-producing factor.",
            "Test 6 provides indefinite material participation status for personal service professionals after 3 years of material participation."
        ],
        reasoning_framework="""
Temp. Reg. §1.469-5T(a)(6): Activity is a personal service activity, and individual materially participated for any 3 prior tax years.

KEY ANALYSIS FRAMEWORK:
1. PERSONAL SERVICE ACTIVITY DEFINITION (Temp. Reg. §1.469-5T(d)):
   - Activity involves performance of personal services in:
     * Health (doctors, dentists, therapists)
     * Law (attorneys, paralegals)
     * Engineering, architecture
     * Accounting, actuarial science
     * Performing arts (actors, musicians)
     * Consulting
     * Any other trade or business where capital is NOT a material income-producing factor

2. CAPITAL NOT MATERIAL INCOME-PRODUCING FACTOR:
   - IRC §1202(e)(3)(A) standard: capital not a material income-producing factor if substantially all gross income is from personal services
   - Example: Law firm with minimal equipment → personal service activity
   - Counter-example: Medical practice with expensive MRI machines → may still be personal service if income primarily from doctor services

3. THREE PRIOR YEARS REQUIREMENT:
   - Any 3 tax years (not necessarily consecutive)
   - Must have materially participated under one of the 7 tests in each of the 3 years
   - No 10-year look-back limit (unlike test 5)

4. INDEFINITE STATUS: Once 3 years of material participation met, test 6 applies indefinitely for that activity.

5. COMMON FACT PATTERNS:
   - Attorney practices law for 5 years, then retires: meets test 6 for remainder of life (if still owns interest)
   - Doctor works full-time for 3 years, then reduces to part-time: meets test 6 indefinitely
   - Consultant starts new consulting business in 2023: cannot use test 6 until 3 years of history

6. ACTIVITY CONTINUITY: Same analysis as test 5 - activity must be substantially the same.

PLANNING OPPORTUNITIES:
- Extremely valuable for personal service professionals
- Once 3 years of material participation established, provides permanent material participation status
- Useful for professionals transitioning to part-time or retirement
""",
        key_factors=[
            "Activity is personal service activity (health, law, engineering, accounting, consulting, performing arts, etc.)",
            "Capital not material income-producing factor",
            "Materially participated in any 3 prior years (consecutive or not)",
            "No time limit on look-back period",
            "Indefinite material participation status once 3 years met"
        ],
        primary_authority=[
            "Temp. Reg. §1.469-5T(a)(6)",
            "Temp. Reg. §1.469-5T(d) - Personal Service Activity",
            "IRC §1202(e)(3)(A) - Capital Not Material Income-Producing Factor"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will challenge personal service activity classification (arguing capital IS material income-producing factor) or prior year material participation substantiation.",
        counter_arguments=[
            "Activity not personal service activity (capital is material income-producing factor)",
            "Taxpayer did not materially participate in 3 prior years",
            "Prior year participation not substantiated",
            "Activity substantially changed, test 6 inapplicable",
            "Activity is rental or investment, not personal service"
        ],
        resolution_strategy="Classify activity as personal service (health, law, engineering, etc.). Substantiate capital not material income-producing factor (income primarily from personal services). Document material participation in 3 prior years. Once met, test 6 provides indefinite status.",
        entity_scope="individuals, trusts, estates",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if clearly personal service activity (law, medicine, consulting) with 3+ years documented material participation. AGGRESSIVE if capital arguably material income-producing factor. DISCLOSURE if activity classification uncertain or prior year substantiation weak."
    ),

    DoctrineBlock(
        topic="material_participation_test_7_facts_and_circumstances",
        keywords=["test 7", "facts and circumstances", "regular continuous substantial", "management participation"],
        conclusion_template=[
            "Taxpayer materially participated based on all facts and circumstances if they participated on a regular, continuous, and substantial basis during the year.",
            "Test 7 is a catch-all standard but EXCLUDES management participation if any other person receives compensation for management services or spends more management hours than taxpayer.",
            "Test 7 is rarely successful and has significant limitations compared to tests 1-6."
        ],
        reasoning_framework="""
Temp. Reg. §1.469-5T(a)(7): Individual participates in the activity on a regular, continuous, and substantial basis during the year, based on facts and circumstances.

KEY ANALYSIS FRAMEWORK:
1. FACTS AND CIRCUMSTANCES STANDARD: No bright-line hours test, but requires regular, continuous, and substantial participation.
   - Regular: Ongoing, not sporadic
   - Continuous: Throughout the year, not just one period
   - Substantial: Meaningful participation, not de minimis

2. MANAGEMENT PARTICIPATION EXCLUSION (Temp. Reg. §1.469-5T(b)):
   Test 7 does NOT include management participation if:
   - Any other person received compensation for management services, OR
   - Any other person spent more hours managing the activity than taxpayer

   This limitation severely restricts test 7 usefulness - most activities have paid managers or employees managing.

3. 100-HOUR FLOOR: Participation less than 100 hours NOT treated as regular, continuous, and substantial (Temp. Reg. §1.469-5T(a)(7)).

4. COMPARISON TO TESTS 1-6: Test 7 is a last resort. Courts and IRS disfavor test 7 claims.

5. COMMON FACT PATTERNS WHERE TEST 7 FAILS:
   - Activity has paid manager: test 7 unavailable (management excluded)
   - Employees spend more management time than taxpayer: test 7 unavailable
   - Taxpayer participates <100 hours: test 7 unavailable

6. RARE SUCCESS SCENARIOS:
   - Taxpayer participates 200 hours in non-management operational roles, no one else manages more
   - Unique activity where taxpayer's participation is critical but doesn't fit tests 1-6

PLANNING CONSIDERATIONS:
- Test 7 is unreliable - avoid relying on it
- Use tests 1-6 whenever possible
- If forced to rely on test 7, ensure no paid managers and taxpayer is top manager
- Document regular, continuous, substantial participation
""",
        key_factors=[
            "Participation on regular, continuous, and substantial basis",
            "At least 100 hours participation",
            "No other person compensated for management OR spent more management hours than taxpayer",
            "Management participation excluded if above condition fails",
            "Facts and circumstances analysis (no bright-line test)"
        ],
        primary_authority=[
            "Temp. Reg. §1.469-5T(a)(7)",
            "Temp. Reg. §1.469-5T(b) - Management Limitation"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will argue management limitation applies (paid manager or other person managed more), participation not regular/continuous/substantial, or hours <100.",
        counter_arguments=[
            "Paid manager exists, management participation excluded",
            "Employee or co-owner spent more management hours than taxpayer",
            "Participation <100 hours, not regular/continuous/substantial",
            "Participation sporadic, not throughout the year",
            "Taxpayer should have used test 1-6 instead (test 7 is last resort)"
        ],
        resolution_strategy="Avoid test 7 if possible - use tests 1-6 instead. If forced to rely on test 7: substantiate >100 hours of regular, continuous, substantial participation. Ensure no paid managers and taxpayer is top manager. Document facts and circumstances. Expect IRS challenge.",
        entity_scope="individuals, trusts, estates",
        confidence="LOW",
        confidence_stratification="AGGRESSIVE in nearly all cases - test 7 rarely successful. DISCLOSURE recommended whenever relying on test 7. Use tests 1-6 instead for DEFENSIBLE position."
    ),

    DoctrineBlock(
        topic="rental_activity_per_se_passive",
        keywords=["rental activity", "per se passive", "IRC 469(c)(2)", "rental real estate", "rental personal property"],
        conclusion_template=[
            "Rental activities are per se passive under IRC §469(c)(2), regardless of taxpayer's level of participation.",
            "Material participation tests do NOT apply to rental activities (with narrow exceptions for real estate professionals).",
            "Rental activity defined as activity where gross income is primarily from payments for use of tangible property (real or personal)."
        ],
        reasoning_framework="""
IRC §469(c)(2): Rental activity is per se passive activity, regardless of material participation.

KEY ANALYSIS FRAMEWORK:
1. RENTAL ACTIVITY DEFINITION (Temp. Reg. §1.469-1T(e)(3)):
   - Gross income from activity is primarily (>50%) from payments for the use of tangible property
   - Includes rental real estate and rental personal property (equipment, vehicles, etc.)

2. PER SE PASSIVE RULE:
   - Rental activities are passive REGARDLESS of hours worked or level of participation
   - Material participation tests (tests 1-7) do NOT apply to rentals
   - Exception: Real estate professional under IRC §469(c)(7) - see separate doctrine block

3. EXCEPTIONS TO RENTAL ACTIVITY CLASSIFICATION (Temp. Reg. §1.469-1T(e)(3)(ii)):
   Six situations where activity is NOT treated as rental activity:

   (A) Average period of customer use ≤7 days (e.g., hotel, car rental)
   (B) Average period of customer use ≤30 days AND significant personal services provided (e.g., hospital, boarding school)
   (C) Extraordinary personal services provided (services performed by individuals, customer use of property incidental)
   (D) Rental incidental to non-rental activity (e.g., equipment rental by dealer)
   (E) Property customarily made available during defined business hours for nonexclusive use by customers (e.g., golf course)
   (F) Property provided in partnership/S corp where taxpayer owns interest as partner/shareholder

4. COMMON RENTAL ACTIVITIES (per se passive):
   - Long-term residential rental (apartment, house)
   - Long-term commercial rental (office, retail)
   - Equipment rental without significant services
   - Triple-net lease real estate

5. COMMON NON-RENTAL ACTIVITIES (not per se passive):
   - Hotel (7-day exception)
   - Short-term vacation rental with cleaning/concierge services (30-day + services exception)
   - Ski resort (extraordinary personal services exception)
   - Equipment dealer renting inventory (incidental exception)

PLANNING OPPORTUNITIES:
- Convert rental to non-rental by reducing average customer use to ≤7 days
- Add significant personal services to qualify for 30-day exception
- Real estate professional exception (IRC §469(c)(7)) for real estate rentals
""",
        key_factors=[
            "Gross income >50% from payments for use of tangible property",
            "Rental activities are per se passive (material participation tests don't apply)",
            "Six exceptions to rental activity classification",
            "Real estate professional exception (IRC §469(c)(7)) for real estate rentals only"
        ],
        primary_authority=[
            "IRC §469(c)(2)",
            "Temp. Reg. §1.469-1T(e)(3) - Rental Activity Definition",
            "IRC §469(c)(7) - Real Estate Professional Exception"
        ],
        burden_holder="taxpayer (to prove exception applies if claiming non-rental treatment)",
        adversary_position="IRS will argue activity is rental (per se passive) if income primarily from use of property, and no exception applies.",
        counter_arguments=[
            "Activity is rental, per se passive regardless of hours worked",
            "Average customer use >7 days (or >30 days), exceptions don't apply",
            "Personal services not significant or extraordinary, rental classification stands",
            "Taxpayer not real estate professional, IRC §469(c)(7) exception unavailable"
        ],
        resolution_strategy="Classify activity correctly (rental vs. non-rental). If rental, per se passive unless real estate professional exception applies. Consider restructuring to qualify for exception (reduce average use to ≤7 days, add significant services). Plan for passive loss limitation.",
        entity_scope="individuals, trusts, estates, closely held C corps, personal service corporations",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if rental activity clearly per se passive. AGGRESSIVE if claiming exception without meeting requirements. DISCLOSURE if exception claim is borderline (e.g., 'significant services' determination)."
    ),

    DoctrineBlock(
        topic="real_estate_professional_exception_469c7",
        keywords=["real estate professional", "IRC 469(c)(7)", "750 hours", "more than half services", "rental real estate"],
        conclusion_template=[
            "Rental real estate activities are NOT per se passive if taxpayer qualifies as real estate professional under IRC §469(c)(7).",
            "Real estate professional: (1) >50% of personal services in real property trades or businesses, AND (2) >750 hours in real property trades or businesses.",
            "If qualified, rental real estate activities subject to material participation tests - can be non-passive if materially participated."
        ],
        reasoning_framework="""
IRC §469(c)(7): Rental real estate activities NOT treated as per se passive for taxpayers qualifying as real estate professionals.

KEY ANALYSIS FRAMEWORK:
1. TWO-PART REAL ESTATE PROFESSIONAL TEST:
   Part A: More than half (>50%) of personal services performed in trades or businesses during the year are in real property trades or businesses where taxpayer materially participates.
   Part B: Taxpayer performs >750 hours of services in real property trades or businesses where taxpayer materially participates.

   BOTH parts must be met.

2. REAL PROPERTY TRADES OR BUSINESSES (IRC §469(c)(7)(C)):
   - Real property development
   - Redevelopment
   - Construction
   - Reconstruction
   - Acquisition
   - Conversion
   - Rental
   - Operation
   - Management
   - Leasing
   - Brokerage trade or business

   Broadly interpreted - includes property management, brokerage, development, rental operations.

3. MATERIAL PARTICIPATION IN REAL PROPERTY TRADES OR BUSINESSES:
   - For Part A: count only hours in real property businesses where taxpayer materially participates
   - For Part B: count all hours in real property trades or businesses where taxpayer materially participates

4. MORE THAN HALF TEST (Part A):
   - Compare hours in real property trades or businesses vs. all other trades or businesses
   - Example: Taxpayer works 1,000 hours in real estate brokerage, 800 hours as accountant. Total = 1,800. Real estate = 55.6%, MEETS Part A.
   - Example: Taxpayer works 700 hours in rental management, 900 hours as engineer. Total = 1,600. Real estate = 43.8%, FAILS Part A.

5. 750-HOUR TEST (Part B):
   - Absolute floor: must perform >750 hours in real property trades or businesses
   - Example: Taxpayer works 800 hours in real estate, 300 hours in other business. MEETS Part B (and Part A).

6. EFFECT OF QUALIFICATION:
   - If qualified as real estate professional, rental real estate activities NOT per se passive
   - Instead, rental real estate subject to material participation tests (tests 1-7)
   - Can group all rental real estate into one activity (IRC §469(c)(7)(A)) to aggregate hours for material participation

7. GROUPING ELECTION (Reg. §1.469-9(g)):
   - Real estate professional can elect to treat ALL rental real estate as single activity
   - Aggregates hours across all rental properties for material participation tests
   - Election made on timely filed return (including extensions), attached statement
   - Binding for year made and all subsequent years unless material change

8. COMMON FACT PATTERNS:
   - Real estate broker working full-time (2,000 hours): qualifies as real estate professional
   - Property manager managing own rentals + client rentals (1,200 hours real estate, 200 hours other): qualifies
   - Doctor with rental properties (2,000 hours medicine, 800 hours rental management): FAILS Part A (real estate <50%)
   - Retired individual managing own rentals (600 hours): FAILS Part B (<750 hours)

SUBSTANTIATION REQUIREMENTS (Temp. Reg. §1.469-5T(f)(4)):
- Contemporaneous daily time logs are gold standard
- Appointment books, calendars, narrative summaries acceptable if reasonable
- IRS heavily scrutinizes real estate professional claims (high audit risk)

PLANNING OPPORTUNITIES:
- Increase hours in real property trades or businesses to exceed 750 and >50% of total
- Reduce hours in non-real property activities to increase real estate percentage
- Make grouping election to aggregate all rental real estate for material participation
- Ensure contemporaneous time logs from day one
""",
        key_factors=[
            ">50% of personal services in real property trades or businesses",
            ">750 hours in real property trades or businesses",
            "Material participation in the real property businesses counted",
            "Grouping election allows treating all rental real estate as single activity",
            "Substantiation with contemporaneous time logs critical",
            "Rental real estate NOT per se passive if qualified, subject to material participation tests instead"
        ],
        primary_authority=[
            "IRC §469(c)(7)",
            "IRC §469(c)(7)(A) - Grouping Election",
            "IRC §469(c)(7)(C) - Real Property Trades or Businesses",
            "Reg. §1.469-9(g) - Grouping Election Procedures",
            "Temp. Reg. §1.469-5T(f)(4) - Substantiation"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will challenge hour substantiation (especially >50% test and 750-hour test), classification of activities as real property trades or businesses, and material participation.",
        counter_arguments=[
            "Hours not substantiated with contemporaneous logs",
            "Real estate hours <50% of total personal services",
            "Real estate hours <750",
            "Activity not real property trade or business",
            "No material participation in real property businesses",
            "Grouping election not properly made",
            "Investment activity counted as real property services (not allowed)"
        ],
        resolution_strategy="Substantiate hours with contemporaneous daily logs. Ensure >750 hours AND >50% of total personal services in real property businesses. Make grouping election to aggregate all rental real estate. Materially participate in rental real estate (usually via test 1 - 500 hours after grouping). High audit risk - documentation critical.",
        entity_scope="individuals (NOT trusts, estates, C corps, or PSCs)",
        confidence="MEDIUM",
        confidence_stratification="DEFENSIBLE if contemporaneous logs show >750 hours and >50% in real property businesses, with grouping election made and material participation in rentals. AGGRESSIVE if relying on reconstructed records or thin substantiation. DISCLOSURE if hours close to thresholds or real property business classification uncertain. HIGH AUDIT RISK."
    ),

    DoctrineBlock(
        topic="$25k_rental_real_estate_allowance_469i",
        keywords=["$25,000 allowance", "IRC 469(i)", "active participation", "rental real estate", "AGI phaseout"],
        conclusion_template=[
            "Up to $25,000 of passive losses from rental real estate may offset non-passive income if taxpayer actively participated and AGI ≤$100,000.",
            "Active participation is a lower standard than material participation - requires ownership interest and participation in management decisions.",
            "$25,000 allowance phases out between AGI $100,000-$150,000, eliminated at $150,000."
        ],
        reasoning_framework="""
IRC §469(i): Special $25,000 allowance for rental real estate losses if taxpayer actively participated.

KEY ANALYSIS FRAMEWORK:
1. ACTIVE PARTICIPATION STANDARD (IRC §469(i)(6)):
   - Taxpayer must own at least 10% interest in the rental real estate (by value)
   - Taxpayer must participate in management decisions in a significant and bona fide sense
   - Management decisions include: approving new tenants, deciding on rental terms, approving capital/repair expenditures
   - Active participation is LOWER standard than material participation - no hour requirement

2. ACTIVE PARTICIPATION VS. MATERIAL PARTICIPATION:
   - Active participation: management decisions, 10% ownership, no hour requirement
   - Material participation: regular, continuous, substantial involvement (tests 1-7)
   - Active participation is easier to meet but only gives $25K allowance
   - Material participation eliminates passive classification entirely

3. $25,000 ALLOWANCE:
   - Maximum $25,000 of rental real estate passive losses can offset non-passive income
   - Only applies to rental real estate (not rental personal property or other passive activities)
   - Allowance is per taxpayer, not per property

4. AGI PHASEOUT (IRC §469(i)(3)):
   - Full $25,000 allowance if AGI ≤$100,000
   - Phases out $1 for every $2 of AGI >$100,000
   - Example: AGI $120,000 → phaseout = ($120,000 - $100,000) × 50% = $10,000 → allowance = $25,000 - $10,000 = $15,000
   - Fully phased out at AGI $150,000+

5. MODIFIED AGI (IRC §469(i)(3)(E)):
   - AGI before passive activity losses
   - Add back: IRA deduction, student loan interest, tuition deduction, excluded foreign income, excluded savings bond interest

6. MARRIED FILING SEPARATELY (MFS):
   - $25,000 allowance reduced to $12,500 per spouse
   - Phaseout starts at $50,000 (not $100,000), fully phased out at $75,000
   - If spouses lived together any time during year, allowance = $0 (harsh rule)

7. LIMITED PARTNER LIMITATION (IRC §469(i)(6)(C)):
   - Limited partners generally cannot actively participate (regulatory prohibition from management)
   - LLC members treated as limited partners for this purpose (proposed regs)
   - Exception: LLC member with management rights may actively participate

8. COMMON FACT PATTERNS:
   - Individual owns duplex, manages it personally (approves tenants, sets rent): active participation met, $25K allowance available
   - Individual owns 5% of LLC rental property: FAILS 10% test, no $25K allowance
   - Individual owns 20% of rental, property manager handles everything: FAILS active participation (no management decisions), no $25K allowance
   - Individual with AGI $180,000: allowance fully phased out

PLANNING OPPORTUNITIES:
- Ensure 10%+ ownership to qualify
- Participate in key management decisions (tenant approval, rent setting, major repairs)
- Manage AGI to stay ≤$100,000 for full allowance (defer income, accelerate deductions)
- If AGI >$150,000, $25K allowance unavailable - consider real estate professional status instead
""",
        key_factors=[
            "Taxpayer owns ≥10% interest in rental real estate",
            "Active participation in management decisions",
            "AGI ≤$150,000 for any allowance (full allowance if ≤$100,000)",
            "Phaseout: $1 for every $2 of AGI >$100,000",
            "$25,000 maximum allowance per taxpayer",
            "Only applies to rental real estate, not other passive activities",
            "Limited partners generally cannot actively participate"
        ],
        primary_authority=[
            "IRC §469(i)",
            "IRC §469(i)(6) - Active Participation Definition",
            "IRC §469(i)(3) - AGI Phaseout"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will challenge active participation (no management decisions), 10% ownership test, or AGI calculation.",
        counter_arguments=[
            "Taxpayer owns <10% interest, no allowance",
            "No active participation (property manager makes all decisions)",
            "Limited partner or LLC member without management rights, cannot actively participate",
            "AGI >$150,000, allowance fully phased out",
            "MFS with spouses living together, allowance = $0"
        ],
        resolution_strategy="Ensure ≥10% ownership. Participate in management decisions (tenant approval, rent setting, repair decisions). Manage AGI ≤$100,000 for full allowance. If AGI >$150,000, pursue real estate professional status instead. Document active participation.",
        entity_scope="individuals (NOT trusts, estates, C corps, or PSCs except closely held C corps)",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if ≥10% ownership, documented active participation in management, AGI ≤$100,000. AGGRESSIVE if active participation minimal or AGI phaseout applies. DISCLOSURE if limited partner/LLC member claiming active participation."
    ),

    DoctrineBlock(
        topic="grouping_of_activities_reg_1_469_4",
        keywords=["grouping", "Reg 1.469-4", "appropriate economic unit", "undertaking", "activity definition"],
        conclusion_template=[
            "Taxpayers may group trade or business activities and rental activities into appropriate economic units for passive activity loss purposes.",
            "Grouping election is made annually (or upon initial year of activity) and requires facts and circumstances analysis of five factors.",
            "Proper grouping can convert multiple non-material participation activities into one material participation activity by aggregating hours."
        ],
        reasoning_framework="""
Reg. §1.469-4: One or more trade or business activities or rental activities may be treated as a single activity if they constitute an appropriate economic unit.

KEY ANALYSIS FRAMEWORK:
1. GROUPING PURPOSE:
   - Allows aggregation of multiple activities into one activity for passive activity rules
   - Aggregates participation hours across grouped activities
   - Can convert multiple <500 hour activities into one >500 hour activity (material participation)

2. APPROPRIATE ECONOMIC UNIT TEST (Reg. §1.469-4(c)(2)):
   Five factors (all facts and circumstances, no single factor determinative):

   (1) Similarities and differences in types of trades or businesses
   (2) Extent of common control
   (3) Extent of common ownership
   (4) Geographical location
   (5) Interdependencies between activities (e.g., same customers, products, employees)

   Example: Taxpayer owns three pizza restaurants in same city → strong grouping case (same business, same control/ownership, same location, interdependent)
   Example: Taxpayer owns pizza restaurant and car wash in different cities → weak grouping case (different business, different locations, not interdependent)

3. GROUPING RESTRICTIONS (Reg. §1.469-4(d)):
   CANNOT group:
   - Rental activity with trade or business activity UNLESS rental is insubstantial relative to trade or business, or vice versa (Reg. §1.469-4(d)(1))
   - Rental real estate activity with rental personal property activity UNLESS personal property provided in connection with real property or vice versa (Reg. §1.469-4(d)(2))
   - Activity subject to IRC §469(c)(7) real estate professional grouping election with any other activity (Reg. §1.469-4(d)(5))

4. GROUPING ELECTION TIMING (Reg. §1.469-4(e)):
   - Made on ORIGINAL return for year (including extensions)
   - Binding for that year and all subsequent years
   - Cannot regroup unless material change in facts and circumstances (Reg. §1.469-4(e)(2))
   - No formal statement required, but grouping must be consistent on return and discernible from facts

5. REGROUPING (Reg. §1.469-4(e)(2)):
   - Generally prohibited once grouping made
   - Exception: material change in facts and circumstances makes original grouping clearly inappropriate
   - Examples of material change: sale of activity, acquisition of new activity, substantial change in operations
   - Rev. Proc. 2010-13 provides safe harbor for regrouping in certain circumstances

6. COMMON GROUPING SCENARIOS:
   - Multiple retail stores in same chain: GROUP (same business, common control/ownership, interdependent)
   - Multiple rental properties in same area: GROUP (same business, common control/ownership, similar location)
   - Law practice + rental building used for law practice: USUALLY CANNOT GROUP (rental + trade or business restriction)
   - Consulting business + equipment rental to clients: MAY GROUP if rental insubstantial or provided in connection with consulting

7. INTERACTION WITH MATERIAL PARTICIPATION:
   - After grouping, material participation tests apply to the GROUPED activity
   - Hours from all grouped activities aggregated for material participation
   - Example: Activity A (200 hrs), Activity B (180 hrs), Activity C (250 hrs). Each individually <500 hrs (no material participation). GROUP A+B+C = 630 hrs → material participation under test 1.

PLANNING OPPORTUNITIES:
- Group multiple small activities to aggregate hours and meet 500-hour test (test 1)
- Group related businesses to simplify passive activity analysis
- Careful with rental + trade or business grouping (generally prohibited)
- Make grouping election on original return (including extensions) to lock in position
- Avoid regrouping unless material change, or use Rev. Proc. 2010-13 safe harbor
""",
        key_factors=[
            "Appropriate economic unit test (5 factors: business type, control, ownership, location, interdependencies)",
            "Cannot group rental with trade or business (unless insubstantial)",
            "Cannot group rental real estate with rental personal property (unless provided together)",
            "Election made on original return, binding prospectively",
            "Regrouping only if material change in facts",
            "Aggregates hours for material participation after grouping"
        ],
        primary_authority=[
            "Reg. §1.469-4",
            "Reg. §1.469-4(c)(2) - Appropriate Economic Unit Factors",
            "Reg. §1.469-4(d) - Grouping Restrictions",
            "Reg. §1.469-4(e) - Grouping Election Timing",
            "Rev. Proc. 2010-13 - Regrouping Safe Harbor"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will challenge grouping as not appropriate economic unit, or violating restrictions (rental + trade or business), or regrouping without material change.",
        counter_arguments=[
            "Activities not appropriate economic unit (different businesses, locations, no interdependencies)",
            "Grouping violates restriction (rental + trade or business)",
            "Regrouping without material change in facts",
            "No grouping election made on original return",
            "Grouping appears tax-motivated without economic substance"
        ],
        resolution_strategy="Apply 5-factor appropriate economic unit test. Document similarities, common control/ownership, location, interdependencies. Avoid prohibited groupings (rental + trade or business). Make election on original return. If regrouping, identify material change or use Rev. Proc. 2010-13 safe harbor. Aggregate hours post-grouping for material participation.",
        entity_scope="individuals, trusts, estates, closely held C corps, personal service corporations",
        confidence="MEDIUM",
        confidence_stratification="DEFENSIBLE if strong economic unit factors (same business, control, ownership, location, interdependent) and no prohibited grouping. AGGRESSIVE if weak economic unit factors or rental + trade or business grouping without insubstantial exception. DISCLOSURE if regrouping without clear material change."
    ),

    DoctrineBlock(
        topic="disposition_entire_interest_469g",
        keywords=["disposition", "IRC 469(g)", "suspended losses", "fully taxable", "entire interest", "unrelated party"],
        conclusion_template=[
            "Suspended passive activity losses are fully deductible in the year taxpayer disposes of entire interest in the activity in a fully taxable transaction to an unrelated party.",
            "Disposition must be fully taxable (not installment sale, like-kind exchange, or tax-free transaction) and to unrelated party under IRC §267(b) or §707(b).",
            "Suspended losses first offset income from the activity, then offset other passive income, then offset non-passive income (no longer limited to passive)."
        ],
        reasoning_framework="""
IRC §469(g): If taxpayer disposes of entire interest in passive activity in fully taxable transaction to unrelated party, suspended passive losses fully allowed.

KEY ANALYSIS FRAMEWORK:
1. ENTIRE INTEREST REQUIREMENT (Reg. §1.469-2T(e)(1)):
   - Must dispose of taxpayer's ENTIRE interest in the activity
   - Partial dispositions do NOT trigger suspended loss deduction
   - Example: Sell 80% of partnership interest → NOT entire interest, suspended losses remain suspended
   - Example: Sell 100% of partnership interest → entire interest, suspended losses deductible

2. FULLY TAXABLE TRANSACTION (Reg. §1.469-2T(e)(1)(i)):
   - Gain or loss recognized in full (not deferred)
   - Excludes: installment sales (IRC §453), like-kind exchanges (IRC §1031), involuntary conversions (IRC §1033), tax-free corporate/partnership transactions
   - Example: Sell property for all cash → fully taxable, suspended losses allowed
   - Example: Installment sale → NOT fully taxable (see separate doctrine block for installment treatment)

3. UNRELATED PARTY REQUIREMENT (IRC §469(g)(1)(A)):
   - Buyer must be unrelated under IRC §267(b) (family attribution) or §707(b) (partnership related party)
   - Related parties: spouse, siblings, ancestors, descendants, >50% owned entities
   - Example: Sell to brother → related party, suspended losses NOT allowed under §469(g)
   - Example: Sell to unrelated third party → unrelated, suspended losses allowed

4. ORDERING RULES FOR SUSPENDED LOSS DEDUCTION (Reg. §1.469-2T(e)(3)):
   Step 1: Offset income from the disposed activity in the year of disposition
   Step 2: Offset other passive income
   Step 3: Offset non-passive income (ordinary income, capital gains, etc.)

   This is the KEY BENEFIT - suspended passive losses can offset NON-PASSIVE income upon disposition.

5. INTERACTION WITH GAIN/LOSS ON DISPOSITION:
   - Gain on sale is passive income (offsets suspended passive losses from same activity and other activities)
   - Loss on sale is passive loss (adds to suspended passive losses from the activity, then all released)

6. PARTIAL DISPOSITIONS (Reg. §1.469-2T(e)(2)):
   - If dispose of less than entire interest, suspended losses remain suspended
   - Pro-rata portion of suspended losses allocable to disposed portion may be deductible in certain circumstances (complex rules)

7. TRANSFERS AT DEATH (IRC §469(g)(2)):
   - Suspended passive losses at death are LOST (stepped-up basis eliminates them)
   - Exception: portion of suspended losses that exceeds basis step-up is deductible on decedent's final return
   - Planning: sell passive activities before death to utilize suspended losses

8. GIFTS (Reg. §1.469-1(f)(4)):
   - Suspended passive losses transfer to donee (not deductible by donor)
   - Donee's basis includes donor's suspended losses (added to donee's basis for loss purposes only)

9. COMMON FACT PATTERNS:
   - Sell rental property for all cash to unrelated buyer: entire interest disposed, fully taxable, suspended losses fully allowed
   - Sell partnership interest for all cash to unrelated buyer: entire interest disposed, suspended losses fully allowed
   - Installment sale of rental property: NOT fully taxable, see installment sale doctrine block
   - Like-kind exchange of rental property: NOT fully taxable, suspended losses remain suspended (carry to replacement property)
   - Sell 50% of rental property: NOT entire interest, suspended losses remain suspended

PLANNING OPPORTUNITIES:
- Time dispositions to maximize suspended loss benefit (high-income years)
- Avoid installment sales, like-kind exchanges if want to utilize suspended losses
- Sell to unrelated parties, not family members
- Plan for disposition before death to avoid loss of suspended losses
""",
        key_factors=[
            "Dispose of entire interest in the activity",
            "Fully taxable transaction (no installment, like-kind, tax-free)",
            "Unrelated party buyer (IRC §267(b) or §707(b))",
            "Suspended losses offset activity income, then passive income, then non-passive income",
            "Partial dispositions do not trigger suspended loss deduction",
            "Death: suspended losses lost (except excess over basis step-up)",
            "Gifts: suspended losses transfer to donee"
        ],
        primary_authority=[
            "IRC §469(g)",
            "IRC §469(g)(2) - Transfers at Death",
            "Reg. §1.469-2T(e) - Disposition Rules",
            "IRC §267(b) - Related Party Definition",
            "IRC §707(b) - Partnership Related Party"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will challenge entire interest requirement (partial disposition), fully taxable transaction requirement (installment or tax-deferred), or unrelated party requirement (related buyer).",
        counter_arguments=[
            "Not entire interest disposed (retained partial interest)",
            "Not fully taxable (installment sale, like-kind exchange, tax-free transaction)",
            "Related party buyer, suspended losses not allowed",
            "Gain on sale is passive income, suspended losses only offset passive income (not non-passive)"
        ],
        resolution_strategy="Ensure entire interest disposed (100% ownership sold). Structure as fully taxable transaction (all cash, no installment or like-kind). Sell to unrelated party. Suspended losses offset activity income, passive income, then non-passive income. Avoid installment sales or like-kind exchanges if want to utilize suspended losses. Plan dispositions before death.",
        entity_scope="individuals, trusts, estates, closely held C corps, personal service corporations",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if entire interest, fully taxable transaction, unrelated buyer. AGGRESSIVE if partial interest or related party buyer. DISCLOSURE if transaction structure uncertain (installment, like-kind, tax-free)."
    ),

    DoctrineBlock(
        topic="installment_sale_suspended_passive_losses",
        keywords=["installment sale", "IRC 453", "suspended losses", "pro-rata release", "passive activity"],
        conclusion_template=[
            "Installment sale of passive activity does NOT trigger full deduction of suspended passive losses in year of sale.",
            "Suspended passive losses are released pro-rata as installment payments are received (based on gain recognized each year).",
            "Taxpayer can elect out of installment method to recognize all gain and deduct all suspended losses in year of sale."
        ],
        reasoning_framework="""
IRC §469(g)(3): If taxpayer disposes of entire interest in passive activity via installment sale, suspended losses released pro-rata as gain recognized.

KEY ANALYSIS FRAMEWORK:
1. INSTALLMENT SALE DEFINITION (IRC §453):
   - At least one payment received in a tax year after the year of sale
   - Gain recognized pro-rata based on gross profit ratio
   - Example: Sell property for $1M ($400K down, $600K note). Basis $500K, gain $500K. Gross profit ratio = 50%. Year 1 gain = $400K × 50% = $200K. Year 2-5 gain = $600K × 50% = $300K.

2. PRO-RATA RELEASE OF SUSPENDED LOSSES (Reg. §1.469-2T(e)(2)):
   - Suspended passive losses released in proportion to gain recognized each year
   - Formula: Suspended losses released = Total suspended losses × (Gain recognized in year / Total gain on disposition)
   - Example: $100K suspended losses, $500K total gain, $200K gain recognized in year 1 → $100K × ($200K / $500K) = $40K suspended losses released in year 1.

3. ELECTION OUT OF INSTALLMENT METHOD (IRC §453(d)):
   - Taxpayer can elect to recognize ALL gain in year of sale (opt out of installment method)
   - If elected, ALL suspended passive losses deductible in year of sale
   - Election made on timely filed return (including extensions)
   - Planning: elect out if want to utilize suspended losses immediately (e.g., high-income year)

4. INTERACTION WITH §469(g) FULL DEDUCTION:
   - §469(g) requires fully taxable transaction for full suspended loss deduction
   - Installment sale is NOT fully taxable (gain deferred)
   - Therefore, installment sale uses pro-rata release rule (§469(g)(3)), NOT full deduction rule (§469(g)(1))

5. COMMON FACT PATTERNS:
   - Sell rental property with $100K suspended losses, installment sale with $500K gain. Year 1 recognize $200K gain → release $40K suspended losses.
   - Sell partnership interest with $50K suspended losses, installment sale with $100K gain. Elect out of installment method → recognize all $100K gain and deduct all $50K suspended losses in year 1.

6. PLANNING OPPORTUNITIES:
   - If high-income year, elect out of installment method to utilize suspended losses immediately
   - If prefer deferral, use installment method and release suspended losses pro-rata
   - Consider time value of money: immediate loss deduction vs. deferral of gain
   - If suspended losses exceed gain, immediate recognition may be beneficial (losses offset other income)

7. INTERACTION WITH OTHER LIMITATIONS:
   - Released suspended losses subject to §469 passive activity rules in the year released (offset passive income, then other income if full disposition in prior year)
   - Not subject to at-risk rules (IRC §465) upon release (already subjected in year loss incurred)
""",
        key_factors=[
            "Installment sale: at least one payment in year after sale",
            "Suspended losses released pro-rata as gain recognized",
            "Formula: Total suspended losses × (Gain in year / Total gain)",
            "Election out of installment method: all gain and all suspended losses in year of sale",
            "Installment sale NOT fully taxable, uses pro-rata rule not full deduction rule"
        ],
        primary_authority=[
            "IRC §469(g)(3)",
            "IRC §453 - Installment Method",
            "IRC §453(d) - Election Out",
            "Reg. §1.469-2T(e)(2)"
        ],
        burden_holder="taxpayer",
        adversary_position="IRS will enforce pro-rata release rule for installment sales, preventing full suspended loss deduction in year of sale unless taxpayer elects out.",
        counter_arguments=[
            "Installment sale, must use pro-rata release (not full deduction in year of sale)",
            "No election out made, gain and suspended losses deferred",
            "Suspended losses not released until gain recognized",
            "Election out deadline missed, stuck with installment method"
        ],
        resolution_strategy="If installment sale, calculate pro-rata suspended loss release based on gain recognized each year. Consider electing out of installment method to recognize all gain and deduct all suspended losses in year of sale. Election must be made on timely filed return. Weigh time value of money and tax rates.",
        entity_scope="individuals, trusts, estates, closely held C corps, personal service corporations",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if pro-rata release calculated correctly based on gain recognized. AGGRESSIVE if claiming full suspended loss deduction in year of installment sale without electing out. DISCLOSURE if election out timing or calculation uncertain."
    ),

    DoctrineBlock(
        topic="self_rental_recharacterization_reg_1_469_2",
        keywords=["self-rental", "recharacterization", "Reg 1.469-2(f)(6)", "rental income", "non-passive"],
        conclusion_template=[
            "Net rental income from property rented to a trade or business in which taxpayer materially participates is recharacterized as non-passive income.",
            "Self-rental rule prevents taxpayers from generating passive income (to absorb passive losses) by renting property to their own active business.",
            "Applies only to NET INCOME (not losses) from the rental activity."
        ],
        reasoning_framework="""
Reg. §1.469-2(f)(6): Self-rental rule recharacterizes net rental income as non-passive if property rented to trade or business in which taxpayer materially participates.

KEY ANALYSIS FRAMEWORK:
1. SELF-RENTAL DEFINITION:
   - Taxpayer rents property to a trade or business activity
   - Taxpayer materially participates in the trade or business activity (as owner or through pass-through entity)
   - Rental and trade or business are commonly controlled (50%+ ownership overlap)

2. RECHARACTERIZATION RULE:
   - NET RENTAL INCOME from the rental activity is recharacterized as NON-PASSIVE income
   - NET RENTAL LOSSES remain passive (not recharacterized)
   - Purpose: Prevent taxpayers from creating passive income to absorb passive losses from other activities

3. COMMON FACT PATTERNS:
   - Taxpayer owns S corp operating business, leases building to S corp. Taxpayer materially participates in S corp → rental income is NON-PASSIVE (self-rental rule).
   - Taxpayer owns rental property leased to unrelated third party operating a business → self-rental rule does NOT apply (not rented to taxpayer's own business).
   - Taxpayer owns partnership interest (non-material participation), partnership rents property from taxpayer → self-rental rule does NOT apply (taxpayer doesn't materially participate in partnership business).

4. NET INCOME VS. NET LOSS:
   - If rental has net income: recharacterized as non-passive income
   - If rental has net loss: remains passive loss (NOT recharacterized as non-passive loss)
   - Asymmetry is intentional - rule prevents abuse via passive income creation, but doesn't convert passive losses to non-passive losses

5. INTERACTION WITH GROUPING:
   - Self-rental rule applies BEFORE grouping analysis
   - If rental income recharacterized as non-passive, cannot group rental with passive activities
   - May group self-rental property with the trade or business it serves (rental + trade or business grouping allowed if activities appropriate economic unit)

6. INTERACTION WITH §469(c)(7) REAL ESTATE PROFESSIONAL:
   - If taxpayer is real estate professional and materially participates in rental activity, rental income is non-passive (not due to self-rental, but due to real estate professional exception)
   - Self-rental rule is separate from real estate professional exception - both can apply

7. PLANNING CONSIDERATIONS:
   - Self-rental rule converts passive income to non-passive income, which may be unfavorable if taxpayer has passive losses from other activities
   - Possible planning: rent property to unrelated third party to avoid self-rental rule
   - Possible planning: reduce taxpayer's participation in the trade or business to <material participation (converts self-rental rule non-passive income to passive income)
   - Caution: self-rental to related party (family) may still trigger rule if commonly controlled

8. COMMON MISTAKES:
   - Assuming self-rental losses are non-passive (they are not - only income recharacterized)
   - Failing to apply self-rental rule when taxpayer materially participates in lessee business
   - Incorrectly grouping self-rental with passive activities (self-rental income is non-passive, cannot offset passive losses post-grouping)
""",
        key_factors=[
            "Property rented to trade or business in which taxpayer materially participates",
            "Common control (50%+ ownership overlap)",
            "NET RENTAL INCOME recharacterized as non-passive",
            "NET RENTAL LOSSES remain passive (not recharacterized)",
            "Rule applies before grouping analysis"
        ],
        primary_authority=[
            "Reg. §1.469-2(f)(6)",
            "Prop. Reg. §1.469-2(f)(6) - Self-Rental Rule Details"
        ],
        burden_holder="taxpayer (to prove self-rental rule does not apply if claiming passive income treatment)",
        adversary_position="IRS will apply self-rental rule to recharacterize rental income as non-passive, preventing offset of passive losses from other activities.",
        counter_arguments=[
            "Self-rental rule applies, rental income is non-passive (cannot offset passive losses)",
            "Taxpayer materially participates in lessee business, triggering self-rental rule",
            "Common control exists (50%+ ownership overlap), self-rental rule applies",
            "Net rental income recharacterized, passive loss carryforwards cannot offset it"
        ],
        resolution_strategy="Identify if property rented to taxpayer's own materially participated business. If yes, net rental income is non-passive (self-rental rule). Net rental losses remain passive. Consider restructuring to avoid rule (rent to unrelated party, reduce material participation in lessee business). Group self-rental with trade or business if appropriate economic unit.",
        entity_scope="individuals, trusts, estates, closely held C corps, personal service corporations",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if self-rental rule correctly applied to recharacterize net income as non-passive. AGGRESSIVE if claiming rental income is passive despite material participation in lessee business. DISCLOSURE if common control or material participation determination uncertain."
    ),

    DoctrineBlock(
        topic="publicly_traded_partnership_pal_rules",
        keywords=["PTP", "publicly traded partnership", "IRC 469(k)", "passive activity", "separate basket"],
        conclusion_template=[
            "Passive activity losses from publicly traded partnerships (PTPs) can only offset passive income from the SAME PTP (separate basket rule).",
            "PTP passive losses cannot offset passive income from other passive activities or non-passive income.",
            "Suspended PTP losses are deductible upon disposition of entire PTP interest."
        ],
        reasoning_framework="""
IRC §469(k): Passive activity loss rules for publicly traded partnerships (PTPs) - separate basket treatment.

KEY ANALYSIS FRAMEWORK:
1. PTP DEFINITION (IRC §7704):
   - Partnership with interests traded on an established securities market, or
   - Partnership with interests readily tradable on a secondary market (or substantial equivalent)
   - Commonly: master limited partnerships (MLPs) traded on NYSE, NASDAQ

2. SEPARATE BASKET RULE (IRC §469(k)(1)):
   - Passive losses from PTP can ONLY offset passive income from the SAME PTP
   - Cannot offset: passive income from other passive activities, passive income from other PTPs, non-passive income
   - Each PTP is a separate basket - losses from PTP A cannot offset income from PTP B

3. INTERACTION WITH GENERAL PAL RULES:
   - PTP income is passive income (unless taxpayer materially participates - rare for traded partnership)
   - PTP losses are passive losses (unless taxpayer materially participates)
   - But separate basket rule limits loss deduction to income from same PTP

4. DISPOSITION OF PTP INTEREST (IRC §469(g)):
   - Upon disposition of entire PTP interest in fully taxable transaction to unrelated party, suspended PTP losses are deductible
   - Ordering: offset gain on sale, then offset other passive income, then offset non-passive income
   - Same disposition rules as other passive activities (IRC §469(g))

5. COMMON FACT PATTERNS:
   - Taxpayer owns MLP A (passive income $10K), MLP B (passive loss $8K), rental property (passive loss $5K).
     * MLP A income $10K: passive income (can offset rental loss $5K and other passive losses, but NOT MLP B loss)
     * MLP B loss $8K: suspended (cannot offset MLP A income or rental income)
     * Rental loss $5K: can offset MLP A income (general PAL rules)
     * Result: MLP A income $10K - rental loss $5K = $5K net passive income. MLP B loss $8K suspended.

6. PLANNING CONSIDERATIONS:
   - PTP losses have limited value due to separate basket rule
   - Consider disposing of losing PTPs to utilize suspended losses
   - Avoid PTPs if generating passive losses elsewhere (losses can't offset)
   - PTP income can offset other passive losses (but PTP losses cannot offset other passive income)

7. EXCEPTION - QUALIFIED PUBLICLY TRADED PARTNERSHIP (IRC §469(k)(3)):
   - If PTP meets certain requirements (primarily engaged in oil and gas activities, elects not to be treated as corporation), separate basket rule may not apply
   - Rare exception - most PTPs subject to separate basket rule

8. INTERACTION WITH NIIT (IRC §1411):
   - PTP income is passive income subject to 3.8% Net Investment Income Tax
   - PTP losses reduce passive income for NIIT purposes (but subject to separate basket rule for regular tax)
""",
        key_factors=[
            "PTP: partnership with interests traded on securities market or readily tradable",
            "Separate basket rule: PTP losses only offset income from SAME PTP",
            "Cannot offset passive income from other activities or PTPs",
            "Suspended PTP losses deductible upon disposition of entire PTP interest",
            "Each PTP is a separate basket"
        ],
        primary_authority=[
            "IRC §469(k)",
            "IRC §7704 - PTP Definition",
            "IRC §469(k)(3) - Qualified PTP Exception"
        ],
        burden_holder="taxpayer (to prove PTP losses deductible or exception applies)",
        adversary_position="IRS will enforce separate basket rule, preventing PTP losses from offsetting passive income from other activities.",
        counter_arguments=[
            "Separate basket rule applies, PTP losses cannot offset other passive income",
            "PTP losses suspended until PTP income generated or entire interest disposed",
            "Each PTP is a separate basket, losses from PTP A cannot offset income from PTP B",
            "No qualified PTP exception, separate basket rule enforced"
        ],
        resolution_strategy="Understand separate basket rule - PTP losses only offset income from same PTP. Plan for limited value of PTP losses. Consider disposing of losing PTPs to utilize suspended losses. PTP income can offset other passive losses (but not vice versa). Track each PTP separately.",
        entity_scope="individuals, trusts, estates, closely held C corps, personal service corporations",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if separate basket rule correctly applied. AGGRESSIVE if claiming PTP losses offset other passive income (violates separate basket rule). DISCLOSURE if qualified PTP exception claimed without clear qualification."
    ),

    DoctrineBlock(
        topic="niit_1411_interaction_with_469",
        keywords=["NIIT", "IRC 1411", "net investment income tax", "3.8%", "passive income", "material participation"],
        conclusion_template=[
            "Net Investment Income Tax (NIIT) is a 3.8% surtax on lesser of (1) net investment income or (2) MAGI exceeding threshold ($250K MFJ, $200K single).",
            "Passive activity income is generally net investment income subject to NIIT unless derived from trade or business in which taxpayer materially participates.",
            "IRC §1411 material participation is same standard as IRC §469 material participation (7 tests)."
        ],
        reasoning_framework="""
IRC §1411: 3.8% Net Investment Income Tax on individuals, estates, and trusts.

KEY ANALYSIS FRAMEWORK:
1. NIIT FORMULA (IRC §1411(a)):
   NIIT = 3.8% × lesser of:
   (1) Net Investment Income (NII), or
   (2) Modified AGI (MAGI) - Threshold

   Thresholds (IRC §1411(b)):
   - MFJ: $250,000
   - Single: $200,000
   - MFS: $125,000
   - Trusts/Estates: top bracket ($14,450 in 2024)

2. NET INVESTMENT INCOME DEFINITION (IRC §1411(c)):
   Includes:
   - Interest, dividends, annuities, royalties
   - Passive activity income (rents, passive business income)
   - Capital gains (including gain on sale of passive activities)

   Excludes:
   - Active trade or business income (material participation)
   - Wages, self-employment income
   - Tax-exempt interest
   - Distributions from qualified retirement plans

3. PASSIVE ACTIVITY INCOME AND NIIT (IRC §1411(c)(2)):
   - Income from passive activities (IRC §469) is NII subject to NIIT
   - Exception: Income from trade or business in which taxpayer MATERIALLY PARTICIPATES is NOT NII (excluded from NIIT)
   - Material participation uses same 7 tests as IRC §469 (Temp. Reg. §1.469-5T)

4. INTERACTION WITH §469 PAL RULES:
   - IRC §469 limits deduction of passive losses
   - IRC §1411 taxes passive income
   - Same activity can generate passive income (subject to NIIT) and passive losses (limited by §469)
   - Material participation eliminates both: income not subject to NIIT, losses not limited by §469

5. RENTAL REAL ESTATE AND NIIT:
   - Rental income is passive income (per se under §469(c)(2)), generally subject to NIIT
   - Exception: Real estate professional (IRC §469(c)(7)) who materially participates → rental income NOT subject to NIIT
   - Non-real estate professional: rental income subject to NIIT even if actively participated for $25K allowance

6. GROUPING FOR NIIT PURPOSES (Reg. §1.1411-4(d)):
   - Grouping rules under Reg. §1.469-4 apply for NIIT purposes
   - If activities grouped for §469, same grouping used for §1411
   - Material participation in grouped activity excludes income from NIIT

7. DISPOSITION OF PASSIVE ACTIVITIES AND NIIT:
   - Gain on sale of passive activity is NII subject to NIIT
   - Exception: Gain from sale of active trade or business (material participation) is NOT NII
   - Suspended passive losses released upon disposition reduce NII for NIIT purposes

8. COMMON FACT PATTERNS:
   - Individual with $300K wages, $50K rental income (no material participation), MFJ:
     * MAGI = $350K, NII = $50K (rental income)
     * NIIT = 3.8% × lesser of ($50K NII, $100K excess MAGI) = 3.8% × $50K = $1,900

   - Individual with $300K S corp income (material participation), MFJ:
     * NII = $0 (S corp income excluded - material participation)
     * NIIT = $0

   - Real estate professional with $300K rental income (material participation), MFJ:
     * NII = $0 (rental income excluded - real estate professional + material participation)
     * NIIT = $0

9. PLANNING OPPORTUNITIES:
   - Materially participate to exclude income from NIIT
   - Real estate professional status to exclude rental income from NIIT
   - Group activities to aggregate hours for material participation
   - Time dispositions of passive activities to manage NIIT (gain is NII)
   - Harvest passive losses to offset passive income (reduces NII)
""",
        key_factors=[
            "3.8% tax on lesser of NII or MAGI exceeding threshold",
            "Passive activity income is NII (subject to NIIT)",
            "Material participation (same as IRC §469) excludes income from NIIT",
            "Rental income subject to NIIT unless real estate professional + material participation",
            "Gain on sale of passive activity is NII",
            "Suspended passive losses released reduce NII"
        ],
        primary_authority=[
            "IRC §1411",
            "IRC §1411(c) - NII Definition",
            "Reg. §1.1411-4 - Passive Activity Rules",
            "Reg. §1.1411-4(d) - Grouping",
            "Temp. Reg. §1.469-5T - Material Participation Tests"
        ],
        burden_holder="taxpayer (to prove material participation to exclude income from NIIT)",
        adversary_position="IRS will argue passive income is NII subject to NIIT unless taxpayer proves material participation.",
        counter_arguments=[
            "Passive activity income is NII, subject to 3.8% NIIT",
            "No material participation, income subject to NIIT",
            "Rental income subject to NIIT (not real estate professional or no material participation)",
            "Gain on sale of passive activity is NII, subject to NIIT"
        ],
        resolution_strategy="Determine if income is passive (subject to NIIT) or active (excluded). Material participation (IRC §469 tests 1-7) excludes income from NIIT. Real estate professional + material participation excludes rental income. Group activities to aggregate hours. Plan dispositions to manage NIIT. Harvest passive losses to reduce NII.",
        entity_scope="individuals, estates, trusts (NOT C corps or tax-exempt entities)",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE if material participation documented (income excluded from NIIT) or clearly passive (income subject to NIIT). AGGRESSIVE if material participation claim without substantiation. DISCLOSURE if real estate professional or grouping determination uncertain."
    )
]
