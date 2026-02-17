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
        topic="Executive Summary Structure",
        keywords=["summary", "structure", "organization", "overview", "clarity"],
        conclusion_template="The executive summary should present a concise overview, highlighting key findings, risks, and recommendations in a logical sequence.",
        reasoning_framework=(
            "Begin by identifying the document's purpose and intended audience. "
            "Outline the main findings, ensuring that each point is supported by evidence from the source material. "
            "Prioritize clarity and brevity, using bullet points or short paragraphs for readability. "
            "Conclude with actionable recommendations and a summary of potential risks. "
            "Ensure the structure follows a logical flow: context, findings, risks, recommendations. "
            "Review for coherence and completeness, confirming that all critical points are addressed without extraneous detail. "
            "Adapt the structure as needed for specific domains (e.g., financial, legal, technical), maintaining the core principles of clarity and conciseness."
        ),
        key_factors=[
            "Document purpose",
            "Audience needs",
            "Logical flow",
            "Clarity of language",
            "Brevity"
        ],
        primary_authority=[
            "Harvard Business Review: Writing Executive Summaries",
            "Purdue OWL: Executive Summary Guidelines"
        ],
        burden_holder="Summary author",
        adversary_position="Overly detailed or disorganized summaries reduce impact and clarity.",
        counter_arguments=[
            "Some audiences require more detail.",
            "Context may necessitate deviation from standard structure."
        ],
        resolution_strategy="Balance detail with brevity, adapt structure to audience while adhering to best practices.",
        entity_scope="All summary documents",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="HBR Executive Summary Framework"
    ),
    DoctrineBlock(
        topic="Key Findings Extraction",
        keywords=["findings", "extraction", "salience", "evidence", "main points"],
        conclusion_template="Key findings should be extracted based on relevance, materiality, and evidentiary support.",
        reasoning_framework=(
            "Review the source material thoroughly, identifying statements or data points that directly impact the document's objectives. "
            "Apply criteria for materiality and relevance, discarding tangential or unsupported claims. "
            "Cross-reference findings with supporting evidence, ensuring accuracy and credibility. "
            "Rank findings by their impact on the overall conclusions. "
            "Summarize each finding succinctly, avoiding technical jargon unless appropriate for the audience."
        ),
        key_factors=[
            "Relevance to objectives",
            "Materiality",
            "Evidentiary support",
            "Clarity",
            "Impact ranking"
        ],
        primary_authority=[
            "Association of Proposal Management Professionals: Key Findings Guidelines",
            "Gartner Research: Effective Summary Techniques"
        ],
        burden_holder="Summary generator",
        adversary_position="Including all findings dilutes focus and overwhelms the reader.",
        counter_arguments=[
            "Comprehensive lists may be required for regulatory compliance.",
            "Omission of minor findings could be seen as selective reporting."
        ],
        resolution_strategy="Prioritize findings by impact and relevance, include comprehensive lists in appendices if needed.",
        entity_scope="Findings sections",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="APMP Best Practices"
    ),
    DoctrineBlock(
        topic="Risk Highlight Formatting",
        keywords=["risk", "highlight", "formatting", "emphasis", "alert"],
        conclusion_template="Risks should be clearly highlighted using consistent formatting to ensure visibility and comprehension.",
        reasoning_framework=(
            "Identify all significant risks associated with the findings or recommendations. "
            "Use formatting tools such as bold text, color coding, or callout boxes to distinguish risk statements from other content. "
            "Ensure that the formatting is consistent throughout the document. "
            "Provide a brief explanation of each risk, its likelihood, and potential impact. "
            "Position risk highlights near related findings or in a dedicated section for easy reference."
        ),
        key_factors=[
            "Risk significance",
            "Formatting consistency",
            "Visibility",
            "Clarity of explanation"
        ],
        primary_authority=[
            "COSO Enterprise Risk Management Framework",
            "ISO 31000: Risk Management"
        ],
        burden_holder="Summary preparer",
        adversary_position="Overuse of formatting may distract or confuse readers.",
        counter_arguments=[
            "Subtle formatting may not sufficiently highlight critical risks.",
            "Readers may have accessibility needs that limit formatting options."
        ],
        resolution_strategy="Apply formatting judiciously, ensure accessibility compliance, and provide alternative text descriptions.",
        entity_scope="Risk sections",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="COSO ERM Guidelines"
    ),
    DoctrineBlock(
        topic="Recommendation Synthesis",
        keywords=["recommendation", "synthesis", "actionable", "next steps", "solution"],
        conclusion_template="Recommendations should synthesize findings into clear, actionable steps tailored to the audience's needs.",
        reasoning_framework=(
            "Analyze the extracted findings and identified risks to determine logical next steps. "
            "Formulate recommendations that are specific, measurable, achievable, relevant, and time-bound (SMART). "
            "Ensure that each recommendation directly addresses a finding or mitigates a risk. "
            "Tailor the tone and detail of recommendations to the audience's expertise and authority. "
            "Prioritize recommendations based on impact and feasibility."
        ),
        key_factors=[
            "Relevance to findings",
            "Actionability",
            "Audience appropriateness",
            "Feasibility",
            "Prioritization"
        ],
        primary_authority=[
            "McKinsey & Company: Recommendation Writing",
            "SMART Criteria (Doran, 1981)"
        ],
        burden_holder="Summary author",
        adversary_position="Generic or vague recommendations lack value.",
        counter_arguments=[
            "Highly specific recommendations may not be universally applicable.",
            "Some recommendations may require additional context."
        ],
        resolution_strategy="Balance specificity with generalizability, provide context where necessary.",
        entity_scope="Recommendation sections",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="McKinsey Synthesis Model"
    ),
    DoctrineBlock(
        topic="Multi-Source Aggregation",
        keywords=["aggregation", "multi-source", "synthesis", "integration", "cross-reference"],
        conclusion_template="Information from multiple sources should be aggregated to provide a comprehensive and balanced summary.",
        reasoning_framework=(
            "Identify all relevant sources, ensuring a diversity of perspectives and data. "
            "Assess the credibility and relevance of each source. "
            "Synthesize information by identifying common themes, contradictions, and gaps. "
            "Cross-reference findings to ensure consistency and completeness. "
            "Document any significant discrepancies and explain their implications."
        ),
        key_factors=[
            "Source credibility",
            "Relevance",
            "Theme identification",
            "Consistency",
            "Gap analysis"
        ],
        primary_authority=[
            "APA Guidelines for Literature Reviews",
            "Cochrane Handbook for Systematic Reviews"
        ],
        burden_holder="Summary compiler",
        adversary_position="Over-aggregation may obscure important nuances.",
        counter_arguments=[
            "Detailed source attribution may be necessary for transparency.",
            "Conflicting sources may require explicit reconciliation."
        ],
        resolution_strategy="Maintain a balance between synthesis and source attribution, document conflicts transparently.",
        entity_scope="Aggregated summaries",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Cochrane Synthesis Standards"
    ),
    DoctrineBlock(
        topic="Document Abstract Generation",
        keywords=["abstract", "generation", "overview", "summary", "condensation"],
        conclusion_template="Document abstracts should provide a succinct overview, capturing the essence of the full document in 150-300 words.",
        reasoning_framework=(
            "Identify the document's main objectives, scope, and conclusions. "
            "Condense these elements into a brief narrative that omits detailed evidence but preserves key messages. "
            "Avoid technical jargon unless essential for the target audience. "
            "Review for completeness and coherence, ensuring the abstract stands alone as an accurate representation."
        ),
        key_factors=[
            "Main objectives",
            "Scope",
            "Key conclusions",
            "Brevity",
            "Clarity"
        ],
        primary_authority=[
            "APA Publication Manual",
            "Elsevier Author Guidelines"
        ],
        burden_holder="Abstract author",
        adversary_position="Overly brief abstracts may omit critical context.",
        counter_arguments=[
            "Longer abstracts may be justified for complex documents.",
            "Some audiences prefer technical detail."
        ],
        resolution_strategy="Adjust abstract length and detail to document complexity and audience needs.",
        entity_scope="Abstract sections",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="APA Abstract Standards"
    ),
    DoctrineBlock(
        topic="Findings Prioritization",
        keywords=["prioritization", "findings", "ranking", "impact", "materiality"],
        conclusion_template="Findings should be prioritized based on impact, materiality, and relevance to the document's objectives.",
        reasoning_framework=(
            "List all extracted findings. "
            "Assign an impact score based on potential consequences or benefits. "
            "Assess materiality by considering the finding's significance to stakeholders. "
            "Rank findings in descending order of importance. "
            "Present high-priority findings first in the summary."
        ),
        key_factors=[
            "Impact score",
            "Materiality",
            "Stakeholder relevance",
            "Ranking methodology"
        ],
        primary_authority=[
            "IFRS Materiality Guidelines",
            "Gartner Research: Prioritization Frameworks"
        ],
        burden_holder="Summary generator",
        adversary_position="Equal presentation of all findings may mislead readers about importance.",
        counter_arguments=[
            "Some findings may be interdependent.",
            "Stakeholder priorities may vary."
        ],
        resolution_strategy="Document prioritization criteria and provide rationale for ranking.",
        entity_scope="Findings sections",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IFRS Materiality Framework"
    ),
    DoctrineBlock(
        topic="Materiality Filtering",
        keywords=["materiality", "filtering", "significance", "threshold", "relevance"],
        conclusion_template="Only findings and details that meet materiality thresholds should be included in the executive summary.",
        reasoning_framework=(
            "Define materiality criteria based on stakeholder needs, regulatory requirements, and document objectives. "
            "Evaluate each potential finding or detail against these criteria. "
            "Exclude immaterial information to maintain focus and brevity. "
            "Document the rationale for inclusion or exclusion of borderline items."
        ),
        key_factors=[
            "Materiality threshold",
            "Stakeholder needs",
            "Regulatory requirements",
            "Relevance"
        ],
        primary_authority=[
            "SEC Staff Accounting Bulletin No. 99",
            "IFRS Materiality Practice Statement"
        ],
        burden_holder="Summary author",
        adversary_position="Excluding minor details may overlook cumulative effects.",
        counter_arguments=[
            "Immaterial details may become significant in aggregate.",
            "Some audiences expect comprehensive coverage."
        ],
        resolution_strategy="Aggregate minor items where appropriate, disclose filtering criteria.",
        entity_scope="Summary content",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SEC SAB No. 99"
    ),
    DoctrineBlock(
        topic="Audience-Appropriate Language",
        keywords=["audience", "language", "tone", "jargon", "readability"],
        conclusion_template="Language should be tailored to the audience's expertise, avoiding unnecessary jargon and ensuring clarity.",
        reasoning_framework=(
            "Identify the primary audience and assess their familiarity with the subject matter. "
            "Adjust vocabulary, tone, and sentence structure to match audience expectations. "
            "Use plain language for general audiences and technical terms only when necessary for experts. "
            "Test readability using established metrics (e.g., Flesch-Kincaid). "
            "Solicit feedback from representative readers where possible."
        ),
        key_factors=[
            "Audience expertise",
            "Vocabulary choice",
            "Tone",
            "Readability metrics"
        ],
        primary_authority=[
            "Plain Language Act (2010)",
            "NIH Clear Communication Guidelines"
        ],
        burden_holder="Summary author",
        adversary_position="Over-simplification may omit critical nuance.",
        counter_arguments=[
            "Technical audiences may require precise terminology.",
            "Some jargon may be unavoidable."
        ],
        resolution_strategy="Balance clarity with necessary technical detail, define terms as needed.",
        entity_scope="All summary content",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Plain Language Act"
    ),
    DoctrineBlock(
        topic="Summary Length Optimization",
        keywords=["length", "optimization", "brevity", "conciseness", "word count"],
        conclusion_template="Summaries should be as brief as possible while preserving essential information, typically 1-2 pages or 10% of the full document.",
        reasoning_framework=(
            "Determine the appropriate summary length based on document complexity and audience needs. "
            "Set a word or page limit in accordance with best practices or organizational guidelines. "
            "Edit content to remove redundancy and non-essential detail. "
            "Ensure that all key findings, risks, and recommendations are included. "
            "Review for readability and completeness."
        ),
        key_factors=[
            "Document complexity",
            "Audience requirements",
            "Essential information",
            "Redundancy elimination"
        ],
        primary_authority=[
            "Harvard Business Review: Summary Guidelines",
            "APA Publication Manual"
        ],
        burden_holder="Summary preparer",
        adversary_position="Overly brief summaries may omit critical content.",
        counter_arguments=[
            "Longer summaries may be justified for complex or regulatory documents.",
            "Some organizations have strict length requirements."
        ],
        resolution_strategy="Adjust length to context, document rationale for deviations.",
        entity_scope="All summaries",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="HBR Summary Standards"
    ),
    DoctrineBlock(
        topic="Bullet Point Distillation",
        keywords=["bullet points", "distillation", "clarity", "brevity", "organization"],
        conclusion_template="Key points should be distilled into concise bullet points for clarity and ease of reference.",
        reasoning_framework=(
            "Identify the most important findings, risks, and recommendations. "
            "Condense each into a single, clear sentence or phrase. "
            "Organize bullet points logically, grouping related items. "
            "Limit the number of bullet points to avoid overwhelming the reader. "
            "Use parallel structure for consistency."
        ),
        key_factors=[
            "Key point identification",
            "Conciseness",
            "Logical grouping",
            "Parallel structure"
        ],
        primary_authority=[
            "Purdue OWL: Bullet Point Guidelines",
            "Gartner Research: Effective Summaries"
        ],
        burden_holder="Summary author",
        adversary_position="Excessive bullet points reduce readability.",
        counter_arguments=[
            "Some topics require detailed explanation.",
            "Narrative structure may be more appropriate in some contexts."
        ],
        resolution_strategy="Balance bullet points with narrative, use sub-bullets for complex items.",
        entity_scope="Summary sections",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Purdue OWL Bullet Standards"
    ),
    DoctrineBlock(
        topic="Thematic Grouping of Findings",
        keywords=["thematic", "grouping", "findings", "organization", "structure"],
        conclusion_template="Findings should be grouped thematically to enhance comprehension and logical flow.",
        reasoning_framework=(
            "Review all extracted findings and identify common themes or categories. "
            "Group related findings together under clear headings. "
            "Present thematic groups in an order that reflects their relative importance or logical progression. "
            "Ensure that each group is clearly labeled and internally consistent."
        ),
        key_factors=[
            "Theme identification",
            "Logical order",
            "Clear labeling",
            "Internal consistency"
        ],
        primary_authority=[
            "Gartner Research: Thematic Analysis",
            "APA Publication Manual"
        ],
        burden_holder="Summary compiler",
        adversary_position="Over-grouping may obscure individual finding significance.",
        counter_arguments=[
            "Some findings may fit multiple themes.",
            "Uncategorized findings may be overlooked."
        ],
        resolution_strategy="Document grouping rationale, use cross-references for multi-theme findings.",
        entity_scope="Findings sections",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Gartner Thematic Analysis"
    ),
    DoctrineBlock(
        topic="Visual Summary Enhancement",
        keywords=["visual", "summary", "charts", "tables", "infographics"],
        conclusion_template="Visual elements should be used to enhance summary clarity and retention, where appropriate.",
        reasoning_framework=(
            "Identify data or findings that can be effectively communicated visually. "
            "Select appropriate visual formats (e.g., tables, charts, infographics) based on the content and audience. "
            "Ensure visuals are clear, labeled, and accessible. "
            "Integrate visuals into the summary at relevant points, referencing them in the text. "
            "Provide alternative text for accessibility."
        ),
        key_factors=[
            "Data suitability",
            "Visual clarity",
            "Labeling",
            "Accessibility"
        ],
        primary_authority=[
            "Edward Tufte: Visual Display of Quantitative Information",
            "WCAG Accessibility Guidelines"
        ],
        burden_holder="Summary designer",
        adversary_position="Overuse of visuals may distract from key messages.",
        counter_arguments=[
            "Some audiences prefer text-only summaries.",
            "Visuals may not be accessible to all users."
        ],
        resolution_strategy="Use visuals judiciously, provide text alternatives.",
        entity_scope="Summary documents",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Tufte Visualization Principles"
    ),
    DoctrineBlock(
        topic="Executive Summary for Regulatory Compliance",
        keywords=["regulatory", "compliance", "summary", "standards", "requirements"],
        conclusion_template="Executive summaries must meet all applicable regulatory standards for content, structure, and disclosure.",
        reasoning_framework=(
            "Identify relevant regulatory requirements for the document type and jurisdiction. "
            "Ensure that all mandated content elements are included in the summary. "
            "Document the rationale for any deviations from standard structure. "
            "Maintain records of compliance checks and approvals."
        ),
        key_factors=[
            "Regulatory requirements",
            "Jurisdiction",
            "Content completeness",
            "Documentation"
        ],
        primary_authority=[
            "SEC EDGAR Filing Manual",
            "EU Prospectus Regulation"
        ],
        burden_holder="Summary preparer",
        adversary_position="Non-compliance may result in legal or financial penalties.",
        counter_arguments=[
            "Some requirements may be ambiguous or conflicting.",
            "Regulations may change over time."
        ],
        resolution_strategy="Consult legal counsel, document compliance process.",
        entity_scope="Regulated summaries",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SEC Filing Standards"
    ),
    DoctrineBlock(
        topic="Stakeholder-Specific Summaries",
        keywords=["stakeholder", "customization", "audience", "summary", "tailoring"],
        conclusion_template="Summaries should be tailored to address the specific interests and concerns of key stakeholders.",
        reasoning_framework=(
            "Identify all key stakeholders and their information needs. "
            "Customize summary content, tone, and structure to address these needs. "
            "Highlight findings and recommendations most relevant to each stakeholder group. "
            "Provide separate summary sections if necessary."
        ),
        key_factors=[
            "Stakeholder analysis",
            "Customization",
            "Relevance",
            "Clarity"
        ],
        primary_authority=[
            "PMI Stakeholder Management Guidelines",
            "Harvard Business Review: Stakeholder Communication"
        ],
        burden_holder="Summary author",
        adversary_position="Over-customization may fragment the summary.",
        counter_arguments=[
            "Resource constraints may limit customization.",
            "Some stakeholders may have conflicting interests."
        ],
        resolution_strategy="Balance customization with overall coherence, document rationale.",
        entity_scope="Stakeholder communications",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="PMI Stakeholder Guidelines"
    ),
    DoctrineBlock(
        topic="Executive Summary for Board Reporting",
        keywords=["board", "reporting", "summary", "governance", "decision-making"],
        conclusion_template="Board-level executive summaries should focus on strategic issues, high-impact risks, and actionable recommendations.",
        reasoning_framework=(
            "Identify strategic findings and risks relevant to board oversight. "
            "Summarize key performance indicators and trends. "
            "Highlight decisions required and recommended actions. "
            "Use clear, concise language suitable for senior executives."
        ),
        key_factors=[
            "Strategic relevance",
            "Risk significance",
            "Actionability",
            "Clarity"
        ],
        primary_authority=[
            "NACD Board Reporting Guidelines",
            "Harvard Business Review: Board Communication"
        ],
        burden_holder="Summary author",
        adversary_position="Excessive operational detail may distract from strategic focus.",
        counter_arguments=[
            "Some boards require operational context.",
            "Legal or regulatory requirements may dictate content."
        ],
        resolution_strategy="Balance strategic and operational content, document rationale.",
        entity_scope="Board reports",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NACD Board Reporting Standards"
    ),
    DoctrineBlock(
        topic="Summary for Investor Communications",
        keywords=["investor", "summary", "communications", "financial", "performance"],
        conclusion_template="Investor summaries should emphasize financial performance, growth prospects, and risk factors.",
        reasoning_framework=(
            "Identify key financial metrics and trends. "
            "Summarize growth drivers and strategic initiatives. "
            "Highlight material risks and mitigation strategies. "
            "Use language and visuals appropriate for investor audiences."
        ),
        key_factors=[
            "Financial metrics",
            "Growth prospects",
            "Risk disclosure",
            "Investor relevance"
        ],
        primary_authority=[
            "SEC Regulation FD",
            "CFA Institute: Investor Communication Standards"
        ],
        burden_holder="Summary author",
        adversary_position="Omission of risks may mislead investors.",
        counter_arguments=[
            "Some risks may be confidential or speculative.",
            "Disclosure requirements vary by jurisdiction."
        ],
        resolution_strategy="Disclose all material risks, consult legal counsel as needed.",
        entity_scope="Investor communications",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SEC Regulation FD"
    ),
    DoctrineBlock(
        topic="Summary for Technical Audiences",
        keywords=["technical", "summary", "audience", "jargon", "detail"],
        conclusion_template="Summaries for technical audiences should include necessary technical detail and terminology.",
        reasoning_framework=(
            "Identify the technical expertise of the audience. "
            "Include relevant technical data, methodologies, and terminology. "
            "Avoid oversimplification that could obscure critical information. "
            "Provide definitions or references for specialized terms where necessary."
        ),
        key_factors=[
            "Technical detail",
            "Terminology",
            "Audience expertise",
            "Clarity"
        ],
        primary_authority=[
            "IEEE Technical Writing Guidelines",
            "ACM Author Guidelines"
        ],
        burden_holder="Summary author",
        adversary_position="Excessive technical detail may alienate non-experts.",
        counter_arguments=[
            "Some audiences require comprehensive technical background.",
            "Technical summaries may be used by multiple stakeholder groups."
        ],
        resolution_strategy="Tailor technical detail to primary audience, provide appendices for additional information.",
        entity_scope="Technical summaries",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEEE Technical Writing Standards"
    ),
    DoctrineBlock(
        topic="Summary for Non-Technical Audiences",
        keywords=["non-technical", "summary", "audience", "plain language", "accessibility"],
        conclusion_template="Summaries for non-technical audiences should use plain language and avoid technical jargon.",
        reasoning_framework=(
            "Assess the technical background of the audience. "
            "Translate technical findings into plain language. "
            "Use analogies or examples to clarify complex concepts. "
            "Test readability and solicit feedback from representative users."
        ),
        key_factors=[
            "Plain language",
            "Clarity",
            "Audience understanding",
            "Readability"
        ],
        primary_authority=[
            "Plain Language Act (2010)",
            "NIH Clear Communication Guidelines"
        ],
        burden_holder="Summary author",
        adversary_position="Oversimplification may lead to misunderstanding.",
        counter_arguments=[
            "Some technical terms may be unavoidable.",
            "Non-technical summaries may omit critical detail."
        ],
        resolution_strategy="Define necessary technical terms, provide references for further reading.",
        entity_scope="Non-technical summaries",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Plain Language Act"
    ),
    DoctrineBlock(
        topic="Summary for Legal Documents",
        keywords=["legal", "summary", "compliance", "precedent", "disclosure"],
        conclusion_template="Legal document summaries must accurately reflect key legal findings, obligations, and precedents.",
        reasoning_framework=(
            "Identify all relevant legal findings and obligations. "
            "Summarize controlling precedents and statutory requirements. "
            "Ensure accuracy and completeness to avoid misrepresentation. "
            "Consult legal counsel for complex or ambiguous issues."
        ),
        key_factors=[
            "Legal accuracy",
            "Precedent identification",
            "Obligation disclosure",
            "Completeness"
        ],
        primary_authority=[
            "ABA Model Rules of Professional Conduct",
            "Bluebook Citation Manual"
        ],
        burden_holder="Summary author",
        adversary_position="Omission or misstatement may result in legal liability.",
        counter_arguments=[
            "Some legal issues may be unsettled.",
            "Confidentiality may limit disclosure."
        ],
        resolution_strategy="Disclose limitations, consult legal counsel as needed.",
        entity_scope="Legal summaries",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ABA Model Rules"
    ),
    DoctrineBlock(
        topic="Summary for Scientific Reports",
        keywords=["scientific", "summary", "abstract", "methodology", "results"],
        conclusion_template="Scientific report summaries should concisely present objectives, methods, results, and conclusions.",
        reasoning_framework=(
            "Identify the research question and objectives. "
            "Summarize the methodology, highlighting key experimental or analytical techniques. "
            "Present main results with supporting data. "
            "Conclude with implications and recommendations for further research."
        ),
        key_factors=[
            "Research objectives",
            "Methodology",
            "Results",
            "Implications"
        ],
        primary_authority=[
            "ICMJE Recommendations",
            "Nature Author Guidelines"
        ],
        burden_holder="Summary author",
        adversary_position="Overly technical summaries may limit accessibility.",
        counter_arguments=[
            "Scientific audiences expect technical detail.",
            "Some findings may be preliminary."
        ],
        resolution_strategy="Balance technical detail with clarity, disclose limitations.",
        entity_scope="Scientific summaries",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ICMJE Recommendations"
    ),
    DoctrineBlock(
        topic="Summary for Project Management Reports",
        keywords=["project management", "summary", "status", "milestones", "risks"],
        conclusion_template="Project management summaries should highlight status, milestones, risks, and next steps.",
        reasoning_framework=(
            "Summarize project objectives and current status. "
            "Highlight completed and upcoming milestones. "
            "Identify key risks and mitigation strategies. "
            "Present next steps and action items."
        ),
        key_factors=[
            "Project status",
            "Milestones",
            "Risks",
            "Next steps"
        ],
        primary_authority=[
            "PMI Project Management Body of Knowledge",
            "PRINCE2 Guidelines"
        ],
        burden_holder="Project manager",
        adversary_position="Omission of risks may lead to project failure.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Project status may be subject to rapid change."
        ],
        resolution_strategy="Update summaries regularly, disclose risk assessment methodology.",
        entity_scope="Project management reports",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="PMBOK"
    ),
    DoctrineBlock(
        topic="Summary for Policy Briefs",
        keywords=["policy", "brief", "summary", "recommendations", "implications"],
        conclusion_template="Policy brief summaries should present key issues, policy options, and recommendations.",
        reasoning_framework=(
            "Identify the policy issue and its context. "
            "Summarize key findings and evidence. "
            "Present policy options with pros and cons. "
            "Conclude with clear, actionable recommendations."
        ),
        key_factors=[
            "Issue identification",
            "Evidence summary",
            "Policy options",
            "Recommendations"
        ],
        primary_authority=[
            "OECD Policy Brief Guidelines",
            "Brookings Institution: Policy Briefs"
        ],
        burden_holder="Policy analyst",
        adversary_position="Lack of options may limit decision-maker flexibility.",
        counter_arguments=[
            "Some issues may have only one viable option.",
            "Recommendations may be politically sensitive."
        ],
        resolution_strategy="Present all viable options, document rationale for recommendations.",
        entity_scope="Policy briefs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OECD Policy Brief Standards"
    ),
    DoctrineBlock(
        topic="Summary for Grant Proposals",
        keywords=["grant", "proposal", "summary", "objectives", "impact"],
        conclusion_template="Grant proposal summaries should clearly state objectives, significance, and expected impact.",
        reasoning_framework=(
            "Summarize the project's objectives and significance. "
            "Highlight the expected outcomes and impact. "
            "Present key personnel and organizational capabilities. "
            "Align summary content with grantor priorities."
        ),
        key_factors=[
            "Objectives",
            "Significance",
            "Impact",
            "Alignment with grantor priorities"
        ],
        primary_authority=[
            "NSF Grant Proposal Guide",
            "NIH Grant Writing Tips"
        ],
        burden_holder="Principal investigator",
        adversary_position="Vague objectives may reduce funding likelihood.",
        counter_arguments=[
            "Some projects are exploratory by nature.",
            "Impact may be difficult to quantify."
        ],
        resolution_strategy="Provide best estimates, document uncertainties.",
        entity_scope="Grant proposals",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NSF Proposal Standards"
    ),
    DoctrineBlock(
        topic="Summary for Annual Reports",
        keywords=["annual report", "summary", "performance", "trends", "outlook"],
        conclusion_template="Annual report summaries should highlight financial performance, key trends, and future outlook.",
        reasoning_framework=(
            "Summarize financial results and key performance indicators. "
            "Highlight major achievements and challenges. "
            "Discuss trends affecting the organization. "
            "Present management's outlook for the future."
        ),
        key_factors=[
            "Financial performance",
            "Achievements",
            "Trends",
            "Outlook"
        ],
        primary_authority=[
            "SEC Form 10-K Instructions",
            "IFRS Annual Reporting Standards"
        ],
        burden_holder="Report preparer",
        adversary_position="Omission of challenges may mislead stakeholders.",
        counter_arguments=[
            "Some challenges may be confidential.",
            "Disclosure requirements vary."
        ],
        resolution_strategy="Disclose all material challenges, consult legal counsel as needed.",
        entity_scope="Annual reports",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SEC Form 10-K"
    ),
    DoctrineBlock(
        topic="Summary for Audit Reports",
        keywords=["audit", "summary", "findings", "recommendations", "compliance"],
        conclusion_template="Audit report summaries should present key findings, compliance status, and recommendations.",
        reasoning_framework=(
            "Summarize audit objectives and scope. "
            "Highlight key findings and areas of non-compliance. "
            "Present recommendations for remediation. "
            "Disclose limitations and methodology."
        ),
        key_factors=[
            "Findings",
            "Compliance status",
            "Recommendations",
            "Limitations"
        ],
        primary_authority=[
            "AICPA Audit Guide",
            "IIA International Standards"
        ],
        burden_holder="Lead auditor",
        adversary_position="Omission of non-compliance may result in regulatory penalties.",
        counter_arguments=[
            "Some findings may be under investigation.",
            "Recommendations may require management approval."
        ],
        resolution_strategy="Disclose all material findings, update as new information becomes available.",
        entity_scope="Audit reports",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AICPA Audit Standards"
    ),
    DoctrineBlock(
        topic="Summary for Environmental Impact Assessments",
        keywords=["environmental", "impact", "assessment", "summary", "mitigation"],
        conclusion_template="Environmental impact assessment summaries should present key impacts, mitigation measures, and regulatory compliance.",
        reasoning_framework=(
            "Summarize the project's scope and objectives. "
            "Identify key environmental impacts and affected resources. "
            "Present proposed mitigation measures. "
            "Document compliance with relevant regulations."
        ),
        key_factors=[
            "Impacts",
            "Mitigation",
            "Regulatory compliance",
            "Affected resources"
        ],
        primary_authority=[
            "EPA NEPA Guidelines",
            "EU EIA Directive"
        ],
        burden_holder="Environmental consultant",
        adversary_position="Omission of impacts may result in legal challenges.",
        counter_arguments=[
            "Some impacts may be uncertain.",
            "Mitigation effectiveness may vary."
        ],
        resolution_strategy="Disclose uncertainties, provide evidence for mitigation effectiveness.",
        entity_scope="Environmental assessments",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA NEPA Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Risk Assessments",
        keywords=["risk", "assessment", "summary", "likelihood", "impact"],
        conclusion_template="Risk assessment summaries should present key risks, likelihood, impact, and mitigation strategies.",
        reasoning_framework=(
            "Identify and describe all significant risks. "
            "Assess the likelihood and potential impact of each risk. "
            "Present mitigation strategies and residual risk. "
            "Summarize overall risk profile."
        ),
        key_factors=[
            "Risk identification",
            "Likelihood",
            "Impact",
            "Mitigation"
        ],
        primary_authority=[
            "ISO 31000: Risk Management",
            "COSO ERM Framework"
        ],
        burden_holder="Risk manager",
        adversary_position="Understating risks may lead to inadequate mitigation.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Mitigation may be outside organizational control."
        ],
        resolution_strategy="Disclose risk assessment methodology, update as new information arises.",
        entity_scope="Risk assessments",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 31000"
    ),
    DoctrineBlock(
        topic="Summary for Due Diligence Reports",
        keywords=["due diligence", "summary", "findings", "risks", "recommendations"],
        conclusion_template="Due diligence report summaries should highlight key findings, risks, and recommendations for decision-makers.",
        reasoning_framework=(
            "Summarize the scope and objectives of the due diligence. "
            "Highlight material findings and associated risks. "
            "Present actionable recommendations. "
            "Disclose limitations and assumptions."
        ),
        key_factors=[
            "Material findings",
            "Risks",
            "Recommendations",
            "Limitations"
        ],
        primary_authority=[
            "ACFE Due Diligence Guidelines",
            "ABA M&A Due Diligence Standards"
        ],
        burden_holder="Due diligence lead",
        adversary_position="Omission of material risks may result in poor decisions.",
        counter_arguments=[
            "Some findings may be preliminary.",
            "Recommendations may require further validation."
        ],
        resolution_strategy="Disclose all material findings, update as new information becomes available.",
        entity_scope="Due diligence reports",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ACFE Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Strategic Plans",
        keywords=["strategic plan", "summary", "objectives", "initiatives", "outcomes"],
        conclusion_template="Strategic plan summaries should present objectives, key initiatives, and expected outcomes.",
        reasoning_framework=(
            "Summarize the organization's vision and strategic objectives. "
            "Highlight key initiatives and milestones. "
            "Present expected outcomes and performance metrics. "
            "Align summary with organizational priorities."
        ),
        key_factors=[
            "Objectives",
            "Initiatives",
            "Outcomes",
            "Alignment"
        ],
        primary_authority=[
            "Balanced Scorecard Institute",
            "Harvard Business Review: Strategic Planning"
        ],
        burden_holder="Strategy lead",
        adversary_position="Omission of risks may undermine credibility.",
        counter_arguments=[
            "Some risks may be confidential.",
            "Outcomes may be uncertain."
        ],
        resolution_strategy="Disclose key risks, document assumptions.",
        entity_scope="Strategic plans",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Balanced Scorecard Standards"
    ),
    DoctrineBlock(
        topic="Summary for Compliance Reports",
        keywords=["compliance", "report", "summary", "regulatory", "status"],
        conclusion_template="Compliance report summaries should present compliance status, key findings, and remediation steps.",
        reasoning_framework=(
            "Summarize the scope and objectives of the compliance review. "
            "Highlight areas of compliance and non-compliance. "
            "Present recommendations for remediation. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Compliance status",
            "Findings",
            "Remediation",
            "Methodology"
        ],
        primary_authority=[
            "ISO 19600: Compliance Management",
            "DOJ Evaluation of Corporate Compliance Programs"
        ],
        burden_holder="Compliance officer",
        adversary_position="Incomplete disclosure may result in regulatory penalties.",
        counter_arguments=[
            "Some issues may be under investigation.",
            "Remediation may be ongoing."
        ],
        resolution_strategy="Update summaries as new information becomes available, disclose limitations.",
        entity_scope="Compliance reports",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 19600"
    ),
    DoctrineBlock(
        topic="Summary for Incident Reports",
        keywords=["incident", "report", "summary", "cause", "response"],
        conclusion_template="Incident report summaries should present the incident, root cause, response, and lessons learned.",
        reasoning_framework=(
            "Summarize the incident and its impact. "
            "Identify root cause and contributing factors. "
            "Present response actions and outcomes. "
            "Highlight lessons learned and recommendations for prevention."
        ),
        key_factors=[
            "Incident description",
            "Root cause",
            "Response",
            "Lessons learned"
        ],
        primary_authority=[
            "NTSB Accident Reporting Guidelines",
            "OSHA Incident Investigation Procedures"
        ],
        burden_holder="Incident investigator",
        adversary_position="Omission of lessons learned may lead to repeat incidents.",
        counter_arguments=[
            "Some causes may be unknown.",
            "Response may be ongoing."
        ],
        resolution_strategy="Update as new information becomes available, disclose uncertainties.",
        entity_scope="Incident reports",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NTSB Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Market Research Reports",
        keywords=["market research", "summary", "trends", "opportunities", "threats"],
        conclusion_template="Market research summaries should present key trends, opportunities, threats, and recommendations.",
        reasoning_framework=(
            "Summarize market size, growth, and key trends. "
            "Identify opportunities and threats. "
            "Present actionable recommendations for market entry or expansion. "
            "Document data sources and methodology."
        ),
        key_factors=[
            "Market trends",
            "Opportunities",
            "Threats",
            "Recommendations"
        ],
        primary_authority=[
            "ESOMAR Market Research Guidelines",
            "AMA Market Research Standards"
        ],
        burden_holder="Market analyst",
        adversary_position="Omission of threats may mislead decision-makers.",
        counter_arguments=[
            "Some threats may be speculative.",
            "Opportunities may be uncertain."
        ],
        resolution_strategy="Disclose uncertainties, document data sources.",
        entity_scope="Market research reports",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ESOMAR Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Business Cases",
        keywords=["business case", "summary", "justification", "ROI", "risks"],
        conclusion_template="Business case summaries should present justification, ROI, risks, and recommendations.",
        reasoning_framework=(
            "Summarize the business need and proposed solution. "
            "Present expected ROI and supporting data. "
            "Highlight key risks and mitigation strategies. "
            "Conclude with recommendations for approval or next steps."
        ),
        key_factors=[
            "Justification",
            "ROI",
            "Risks",
            "Recommendations"
        ],
        primary_authority=[
            "Harvard Business Review: Business Case Writing",
            "PMI Business Case Guidelines"
        ],
        burden_holder="Business analyst",
        adversary_position="Omission of risks may result in poor investment decisions.",
        counter_arguments=[
            "Some risks may be unknown.",
            "ROI may be difficult to quantify."
        ],
        resolution_strategy="Disclose assumptions and uncertainties, provide sensitivity analysis.",
        entity_scope="Business cases",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="PMI Business Case Standards"
    ),
    DoctrineBlock(
        topic="Summary for Change Management Reports",
        keywords=["change management", "summary", "objectives", "impacts", "stakeholders"],
        conclusion_template="Change management summaries should present objectives, impacts, stakeholder analysis, and recommendations.",
        reasoning_framework=(
            "Summarize the change initiative and its objectives. "
            "Identify key impacts on people, processes, and technology. "
            "Present stakeholder analysis and engagement strategies. "
            "Conclude with recommendations for implementation."
        ),
        key_factors=[
            "Objectives",
            "Impacts",
            "Stakeholder analysis",
            "Recommendations"
        ],
        primary_authority=[
            "Prosci Change Management Methodology",
            "Kotter's 8-Step Change Model"
        ],
        burden_holder="Change manager",
        adversary_position="Omission of stakeholder impacts may result in resistance.",
        counter_arguments=[
            "Some impacts may be unknown.",
            "Stakeholder analysis may be incomplete."
        ],
        resolution_strategy="Update as new information becomes available, document assumptions.",
        entity_scope="Change management reports",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Prosci Methodology"
    ),
    DoctrineBlock(
        topic="Summary for IT Security Assessments",
        keywords=["IT security", "assessment", "summary", "vulnerabilities", "controls"],
        conclusion_template="IT security assessment summaries should present key vulnerabilities, risks, and recommended controls.",
        reasoning_framework=(
            "Summarize the scope and methodology of the assessment. "
            "Highlight critical vulnerabilities and associated risks. "
            "Present recommended controls and remediation steps. "
            "Document limitations and residual risks."
        ),
        key_factors=[
            "Vulnerabilities",
            "Risks",
            "Controls",
            "Limitations"
        ],
        primary_authority=[
            "NIST Cybersecurity Framework",
            "ISO/IEC 27001"
        ],
        burden_holder="IT security assessor",
        adversary_position="Omission of vulnerabilities may result in breaches.",
        counter_arguments=[
            "Some vulnerabilities may be unknown.",
            "Controls may be resource-intensive."
        ],
        resolution_strategy="Disclose all known vulnerabilities, prioritize controls.",
        entity_scope="IT security assessments",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST Cybersecurity Framework"
    ),
    DoctrineBlock(
        topic="Summary for Procurement Reports",
        keywords=["procurement", "summary", "findings", "risks", "recommendations"],
        conclusion_template="Procurement report summaries should present key findings, risks, and recommendations for process improvement.",
        reasoning_framework=(
            "Summarize procurement objectives and scope. "
            "Highlight key findings and process inefficiencies. "
            "Present risks and recommended improvements. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Findings",
            "Risks",
            "Recommendations",
            "Process improvement"
        ],
        primary_authority=[
            "CIPS Procurement Guidelines",
            "World Bank Procurement Framework"
        ],
        burden_holder="Procurement lead",
        adversary_position="Omission of inefficiencies may result in missed savings.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Recommendations may require management approval."
        ],
        resolution_strategy="Disclose all material findings, update as new information becomes available.",
        entity_scope="Procurement reports",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="CIPS Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Human Resources Reports",
        keywords=["human resources", "summary", "workforce", "trends", "recommendations"],
        conclusion_template="HR report summaries should present workforce trends, key findings, and recommendations.",
        reasoning_framework=(
            "Summarize workforce demographics and trends. "
            "Highlight key findings related to recruitment, retention, and diversity. "
            "Present actionable recommendations for improvement. "
            "Document data sources and limitations."
        ),
        key_factors=[
            "Workforce trends",
            "Findings",
            "Recommendations",
            "Data sources"
        ],
        primary_authority=[
            "SHRM HR Reporting Standards",
            "EEOC Reporting Guidelines"
        ],
        burden_holder="HR manager",
        adversary_position="Omission of diversity issues may result in reputational risk.",
        counter_arguments=[
            "Some data may be confidential.",
            "Recommendations may require leadership approval."
        ],
        resolution_strategy="Disclose all material findings, update as new information becomes available.",
        entity_scope="HR reports",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SHRM Standards"
    ),
    DoctrineBlock(
        topic="Summary for Customer Feedback Reports",
        keywords=["customer feedback", "summary", "trends", "satisfaction", "recommendations"],
        conclusion_template="Customer feedback summaries should present key trends, satisfaction drivers, and recommendations.",
        reasoning_framework=(
            "Summarize customer feedback sources and methodology. "
            "Highlight key trends and satisfaction drivers. "
            "Present actionable recommendations for improvement. "
            "Document limitations and response strategies."
        ),
        key_factors=[
            "Trends",
            "Satisfaction drivers",
            "Recommendations",
            "Limitations"
        ],
        primary_authority=[
            "Net Promoter System Guidelines",
            "CXPA Customer Experience Standards"
        ],
        burden_holder="Customer experience lead",
        adversary_position="Omission of negative feedback may bias results.",
        counter_arguments=[
            "Some feedback may be unrepresentative.",
            "Recommendations may require cross-functional support."
        ],
        resolution_strategy="Disclose all material feedback, document response strategies.",
        entity_scope="Customer feedback reports",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Net Promoter System"
    ),
    DoctrineBlock(
        topic="Summary for Training Evaluation Reports",
        keywords=["training", "evaluation", "summary", "outcomes", "recommendations"],
        conclusion_template="Training evaluation summaries should present outcomes, effectiveness, and recommendations for improvement.",
        reasoning_framework=(
            "Summarize training objectives and participant demographics. "
            "Highlight key outcomes and effectiveness measures. "
            "Present recommendations for improvement. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Outcomes",
            "Effectiveness",
            "Recommendations",
            "Methodology"
        ],
        primary_authority=[
            "Kirkpatrick Model",
            "ASTD Training Evaluation Guidelines"
        ],
        burden_holder="Training manager",
        adversary_position="Omission of negative outcomes may bias results.",
        counter_arguments=[
            "Some outcomes may be subjective.",
            "Recommendations may require resource allocation."
        ],
        resolution_strategy="Disclose all material outcomes, document limitations.",
        entity_scope="Training evaluation reports",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Kirkpatrick Model"
    ),
    DoctrineBlock(
        topic="Summary for Internal Investigations",
        keywords=["internal investigation", "summary", "findings", "disciplinary", "recommendations"],
        conclusion_template="Internal investigation summaries should present findings, disciplinary actions, and recommendations.",
        reasoning_framework=(
            "Summarize the scope and objectives of the investigation. "
            "Highlight key findings and evidence. "
            "Present disciplinary actions taken or recommended. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Findings",
            "Disciplinary actions",
            "Recommendations",
            "Methodology"
        ],
        primary_authority=[
            "ACFE Investigation Standards",
            "DOJ Investigation Guidelines"
        ],
        burden_holder="Investigation lead",
        adversary_position="Omission of findings may result in legal liability.",
        counter_arguments=[
            "Some findings may be confidential.",
            "Disciplinary actions may be pending."
        ],
        resolution_strategy="Disclose all material findings, update as new information becomes available.",
        entity_scope="Internal investigations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ACFE Standards"
    ),
    DoctrineBlock(
        topic="Summary for Mergers & Acquisitions Reports",
        keywords=["M&A", "mergers", "acquisitions", "summary", "risks", "synergies"],
        conclusion_template="M&A report summaries should present key findings, risks, synergies, and recommendations.",
        reasoning_framework=(
            "Summarize the scope and objectives of the transaction. "
            "Highlight key findings and risks. "
            "Present identified synergies and value drivers. "
            "Conclude with recommendations for next steps."
        ),
        key_factors=[
            "Findings",
            "Risks",
            "Synergies",
            "Recommendations"
        ],
        primary_authority=[
            "ABA M&A Due Diligence Standards",
            "PwC M&A Integration Guidelines"
        ],
        burden_holder="M&A lead",
        adversary_position="Omission of risks may result in failed transactions.",
        counter_arguments=[
            "Some synergies may be speculative.",
            "Risks may be unknown."
        ],
        resolution_strategy="Disclose all material findings and risks, update as new information becomes available.",
        entity_scope="M&A reports",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ABA Standards"
    ),
    DoctrineBlock(
        topic="Summary for Product Launch Reports",
        keywords=["product launch", "summary", "market readiness", "risks", "recommendations"],
        conclusion_template="Product launch report summaries should present market readiness, risks, and recommendations.",
        reasoning_framework=(
            "Summarize product features and market readiness. "
            "Highlight key risks and mitigation strategies. "
            "Present recommendations for launch and post-launch monitoring. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Market readiness",
            "Risks",
            "Recommendations",
            "Methodology"
        ],
        primary_authority=[
            "Product Development and Management Association (PDMA) Guidelines",
            "Gartner Product Launch Framework"
        ],
        burden_holder="Product manager",
        adversary_position="Omission of risks may result in failed launches.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Recommendations may require cross-functional support."
        ],
        resolution_strategy="Disclose all material risks, update as new information becomes available.",
        entity_scope="Product launch reports",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="PDMA Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Sustainability Reports",
        keywords=["sustainability", "summary", "ESG", "impacts", "initiatives"],
        conclusion_template="Sustainability report summaries should present ESG impacts, initiatives, and progress toward goals.",
        reasoning_framework=(
            "Summarize the organization's ESG objectives and initiatives. "
            "Highlight key impacts and progress toward goals. "
            "Present challenges and opportunities. "
            "Document data sources and methodology."
        ),
        key_factors=[
            "ESG impacts",
            "Initiatives",
            "Progress",
            "Challenges"
        ],
        primary_authority=[
            "Global Reporting Initiative (GRI) Standards",
            "SASB Sustainability Reporting Guidelines"
        ],
        burden_holder="Sustainability officer",
        adversary_position="Omission of challenges may undermine credibility.",
        counter_arguments=[
            "Some data may be unavailable.",
            "Progress may be difficult to quantify."
        ],
        resolution_strategy="Disclose all material challenges, document data sources.",
        entity_scope="Sustainability reports",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="GRI Standards"
    ),
    DoctrineBlock(
        topic="Summary for Diversity & Inclusion Reports",
        keywords=["diversity", "inclusion", "summary", "trends", "initiatives"],
        conclusion_template="D&I report summaries should present workforce trends, initiatives, and progress toward goals.",
        reasoning_framework=(
            "Summarize workforce diversity metrics and trends. "
            "Highlight key D&I initiatives and outcomes. "
            "Present progress toward stated goals. "
            "Document data sources and methodology."
        ),
        key_factors=[
            "Diversity metrics",
            "Initiatives",
            "Progress",
            "Data sources"
        ],
        primary_authority=[
            "EEOC Reporting Guidelines",
            "SHRM D&I Standards"
        ],
        burden_holder="D&I officer",
        adversary_position="Omission of challenges may undermine credibility.",
        counter_arguments=[
            "Some data may be confidential.",
            "Progress may be difficult to quantify."
        ],
        resolution_strategy="Disclose all material challenges, document data sources.",
        entity_scope="D&I reports",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EEOC Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Crisis Management Reports",
        keywords=["crisis management", "summary", "response", "lessons learned", "recommendations"],
        conclusion_template="Crisis management summaries should present response actions, lessons learned, and recommendations.",
        reasoning_framework=(
            "Summarize the crisis event and organizational response. "
            "Highlight key lessons learned and best practices. "
            "Present recommendations for future preparedness. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Response actions",
            "Lessons learned",
            "Recommendations",
            "Limitations"
        ],
        primary_authority=[
            "FEMA Crisis Management Guidelines",
            "ISO 22301: Business Continuity"
        ],
        burden_holder="Crisis manager",
        adversary_position="Omission of lessons learned may result in repeat crises.",
        counter_arguments=[
            "Some lessons may be context-specific.",
            "Recommendations may require resource allocation."
        ],
        resolution_strategy="Disclose all material lessons, update as new information becomes available.",
        entity_scope="Crisis management reports",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FEMA Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Research Proposals",
        keywords=["research proposal", "summary", "objectives", "significance", "methodology"],
        conclusion_template="Research proposal summaries should present objectives, significance, and proposed methodology.",
        reasoning_framework=(
            "Summarize the research question and objectives. "
            "Highlight the significance and expected impact. "
            "Present the proposed methodology and timeline. "
            "Align summary content with funding agency priorities."
        ),
        key_factors=[
            "Objectives",
            "Significance",
            "Methodology",
            "Alignment"
        ],
        primary_authority=[
            "NSF Proposal Guidelines",
            "NIH Grant Writing Tips"
        ],
        burden_holder="Principal investigator",
        adversary_position="Vague objectives may reduce funding likelihood.",
        counter_arguments=[
            "Some projects are exploratory by nature.",
            "Methodology may be subject to change."
        ],
        resolution_strategy="Provide best estimates, document uncertainties.",
        entity_scope="Research proposals",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NSF Proposal Standards"
    ),
    DoctrineBlock(
        topic="Summary for Financial Statements",
        keywords=["financial statements", "summary", "performance", "trends", "risks"],
        conclusion_template="Financial statement summaries should present key performance metrics, trends, and risks.",
        reasoning_framework=(
            "Summarize key financial metrics and trends. "
            "Highlight material risks and uncertainties. "
            "Present management's discussion and analysis. "
            "Document data sources and assumptions."
        ),
        key_factors=[
            "Performance metrics",
            "Trends",
            "Risks",
            "Assumptions"
        ],
        primary_authority=[
            "SEC Regulation S-K",
            "IFRS Financial Reporting Standards"
        ],
        burden_holder="Financial officer",
        adversary_position="Omission of risks may mislead stakeholders.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Disclosure requirements vary."
        ],
        resolution_strategy="Disclose all material risks, consult legal counsel as needed.",
        entity_scope="Financial statements",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SEC Regulation S-K"
    ),
    DoctrineBlock(
        topic="Summary for Operational Reviews",
        keywords=["operational review", "summary", "findings", "efficiency", "recommendations"],
        conclusion_template="Operational review summaries should present key findings, efficiency opportunities, and recommendations.",
        reasoning_framework=(
            "Summarize the scope and objectives of the review. "
            "Highlight key findings and process inefficiencies. "
            "Present recommendations for improvement. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Findings",
            "Efficiency",
            "Recommendations",
            "Methodology"
        ],
        primary_authority=[
            "APQC Process Improvement Guidelines",
            "Lean Six Sigma Standards"
        ],
        burden_holder="Operations manager",
        adversary_position="Omission of inefficiencies may result in missed savings.",
        counter_arguments=[
            "Some findings may be preliminary.",
            "Recommendations may require management approval."
        ],
        resolution_strategy="Disclose all material findings, update as new information becomes available.",
        entity_scope="Operational reviews",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="APQC Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Strategic Risk Reports",
        keywords=["strategic risk", "summary", "findings", "impact", "mitigation"],
        conclusion_template="Strategic risk summaries should present key risks, potential impacts, and mitigation strategies.",
        reasoning_framework=(
            "Summarize the organization's strategic objectives. "
            "Identify and describe key strategic risks. "
            "Assess potential impacts and likelihood. "
            "Present mitigation strategies and monitoring plans."
        ),
        key_factors=[
            "Strategic objectives",
            "Risks",
            "Impacts",
            "Mitigation"
        ],
        primary_authority=[
            "COSO ERM Framework",
            "ISO 31000: Risk Management"
        ],
        burden_holder="Risk officer",
        adversary_position="Omission of strategic risks may result in missed opportunities.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Mitigation may be outside organizational control."
        ],
        resolution_strategy="Disclose all material risks, update as new information becomes available.",
        entity_scope="Strategic risk reports",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="COSO ERM Framework"
    ),
    DoctrineBlock(
        topic="Summary for Technology Assessments",
        keywords=["technology assessment", "summary", "capabilities", "risks", "recommendations"],
        conclusion_template="Technology assessment summaries should present capabilities, risks, and recommendations.",
        reasoning_framework=(
            "Summarize the technology's capabilities and limitations. "
            "Highlight key risks and opportunities. "
            "Present recommendations for adoption or improvement. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Capabilities",
            "Risks",
            "Recommendations",
            "Methodology"
        ],
        primary_authority=[
            "Gartner Hype Cycle",
            "IEEE Technology Assessment Guidelines"
        ],
        burden_holder="Technology analyst",
        adversary_position="Omission of limitations may result in unrealistic expectations.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Capabilities may be evolving."
        ],
        resolution_strategy="Disclose all material limitations, update as new information becomes available.",
        entity_scope="Technology assessments",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Gartner Hype Cycle"
    ),
    DoctrineBlock(
        topic="Summary for Intellectual Property Reports",
        keywords=["intellectual property", "summary", "patents", "risks", "recommendations"],
        conclusion_template="IP report summaries should present key assets, risks, and recommendations.",
        reasoning_framework=(
            "Summarize key IP assets and their status. "
            "Highlight risks related to infringement, expiration, or litigation. "
            "Present recommendations for protection or monetization. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "IP assets",
            "Risks",
            "Recommendations",
            "Limitations"
        ],
        primary_authority=[
            "WIPO IP Reporting Guidelines",
            "USPTO Reporting Standards"
        ],
        burden_holder="IP counsel",
        adversary_position="Omission of risks may result in legal liability.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Recommendations may require management approval."
        ],
        resolution_strategy="Disclose all material risks, update as new information becomes available.",
        entity_scope="IP reports",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="WIPO Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Data Privacy Assessments",
        keywords=["data privacy", "assessment", "summary", "risks", "compliance"],
        conclusion_template="Data privacy assessment summaries should present key risks, compliance status, and recommendations.",
        reasoning_framework=(
            "Summarize the scope and objectives of the assessment. "
            "Highlight key privacy risks and compliance gaps. "
            "Present recommendations for remediation. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Privacy risks",
            "Compliance",
            "Recommendations",
            "Methodology"
        ],
        primary_authority=[
            "GDPR Guidelines",
            "NIST Privacy Framework"
        ],
        burden_holder="Privacy officer",
        adversary_position="Omission of risks may result in regulatory penalties.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Compliance requirements may change."
        ],
        resolution_strategy="Disclose all material risks, update as new information becomes available.",
        entity_scope="Data privacy assessments",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GDPR Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Supply Chain Reports",
        keywords=["supply chain", "summary", "risks", "efficiency", "recommendations"],
        conclusion_template="Supply chain report summaries should present key risks, efficiency opportunities, and recommendations.",
        reasoning_framework=(
            "Summarize supply chain objectives and scope. "
            "Highlight key risks and inefficiencies. "
            "Present recommendations for improvement. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Risks",
            "Efficiency",
            "Recommendations",
            "Methodology"
        ],
        primary_authority=[
            "APICS Supply Chain Council Guidelines",
            "Gartner Supply Chain Standards"
        ],
        burden_holder="Supply chain manager",
        adversary_position="Omission of risks may result in disruptions.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Recommendations may require cross-functional support."
        ],
        resolution_strategy="Disclose all material risks, update as new information becomes available.",
        entity_scope="Supply chain reports",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="APICS Guidelines"
    ),
    DoctrineBlock(
        topic="Summary for Business Continuity Plans",
        keywords=["business continuity", "summary", "risks", "preparedness", "recommendations"],
        conclusion_template="Business continuity plan summaries should present key risks, preparedness measures, and recommendations.",
        reasoning_framework=(
            "Summarize the organization's continuity objectives and scope. "
            "Highlight key risks and preparedness measures. "
            "Present recommendations for improvement. "
            "Document methodology and limitations."
        ),
        key_factors=[
            "Risks",
            "Preparedness",
            "Recommendations",
            "Methodology"
        ],
        primary_authority=[
            "ISO 22301: Business Continuity",
            "FEMA Continuity Guidelines"
        ],
        burden_holder="Continuity manager",
        adversary_position="Omission of risks may result in inadequate preparedness.",
        counter_arguments=[
            "Some risks may be speculative.",
            "Preparedness measures may be resource-intensive."
        ],
        resolution_strategy="Disclose all material risks, update as new information becomes available.",
        entity_scope="Business continuity plans",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 22301"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in k.lower() for k in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]