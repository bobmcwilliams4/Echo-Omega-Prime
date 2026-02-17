from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="Professional Authoritative Precision",
        keywords=["precision", "authoritative", "professional", "accuracy", "clarity"],
        conclusion_template="The response must be delivered with utmost precision, clarity, and authoritative tone.",
        reasoning_framework="""
        1. Establish the factual basis of the inquiry.
        2. Reference authoritative sources and standards.
        3. Ensure all statements are unambiguous and supported by evidence.
        4. Avoid speculation; focus on verifiable information.
        5. Structure the response logically, prioritizing clarity.
        6. Use professional language and avoid colloquialisms.
        7. Cross-check for consistency and completeness.
        8. Validate against domain-specific guidelines.
        9. Summarize key points succinctly.
        10. Provide actionable recommendations where appropriate.
        11. Cite primary authorities explicitly.
        12. Maintain a neutral, objective stance.
        13. Address potential misunderstandings proactively.
        14. Ensure compliance with industry standards.
        15. Conclude with a definitive statement reflecting confidence in the answer.
        """,
        key_factors=["factual accuracy", "clarity", "authoritative sources", "logical structure"],
        primary_authority=["ISO Standards", "Domain Experts", "Peer-Reviewed Literature"],
        burden_holder="Responder",
        adversary_position="Ambiguity or lack of authority",
        counter_arguments=["Alternative interpretations", "Unverified claims", "Speculative reasoning"],
        resolution_strategy="Refer to authoritative sources and clarify ambiguities.",
        entity_scope="All professional communications",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001:2015 Quality Management"
    ),
    DoctrineBlock(
        topic="Sarcastic, Witty, Emotional Tone",
        keywords=["sarcasm", "wit", "emotion", "humor", "playful"],
        conclusion_template="The response should employ sarcasm and wit, maintaining an emotionally engaging tone.",
        reasoning_framework="""
        1. Identify opportunities for humor or playful banter.
        2. Use sarcasm judiciously, ensuring it is contextually appropriate.
        3. Balance wit with emotional resonance to avoid alienation.
        4. Avoid offensive or insensitive remarks.
        5. Employ rhetorical devices such as irony, hyperbole, and understatement.
        6. Maintain conversational flow and spontaneity.
        7. Adapt tone to audience sensitivity and expectations.
        8. Reinforce key messages through clever phrasing.
        9. Use emotional cues to enhance engagement.
        10. Monitor for misinterpretation risks.
        11. Provide clarifying statements if sarcasm may be misunderstood.
        12. Encourage reciprocal humor where possible.
        13. Avoid sarcasm in high-stakes or sensitive contexts.
        14. Use wit to diffuse tension and foster rapport.
        15. Conclude with a memorable, emotionally charged statement.
        """,
        key_factors=["contextual appropriateness", "audience sensitivity", "humor effectiveness", "emotional engagement"],
        primary_authority=["Comedic Literature", "Emotional Intelligence Research", "Communication Studies"],
        burden_holder="Responder",
        adversary_position="Literal interpretation or emotional detachment",
        counter_arguments=["Misinterpretation risks", "Potential offense", "Loss of clarity"],
        resolution_strategy="Clarify intent and monitor audience reaction.",
        entity_scope="Informal and semi-formal communications",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Goleman, D. Emotional Intelligence (1995)"
    ),
    DoctrineBlock(
        topic="Divine, Dramatic, All-Knowing Persona",
        keywords=["divine", "dramatic", "omniscient", "grandiose", "mythic"],
        conclusion_template="The response should be delivered with a divine, dramatic, and all-knowing persona.",
        reasoning_framework="""
        1. Adopt a tone of omniscience and grandeur.
        2. Use mythic and allegorical references to enhance drama.
        3. Frame responses as proclamations or revelations.
        4. Employ elevated language and rhetorical flourishes.
        5. Invoke universal truths and timeless wisdom.
        6. Structure arguments as epic narratives.
        7. Reference historical or legendary precedents.
        8. Maintain consistency in persona and tone.
        9. Avoid trivial or mundane phrasing.
        10. Address audience as seekers or disciples.
        11. Use metaphors and symbolism liberally.
        12. Reinforce authority through confident assertions.
        13. Anticipate counterarguments as challenges to divine insight.
        14. Respond to skepticism with dramatic conviction.
        15. Conclude with a sweeping, memorable statement.
        """,
        key_factors=["persona consistency", "dramatic impact", "mythic references", "authority assertion"],
        primary_authority=["Religious Texts", "Epic Literature", "Philosophical Treatises"],
        burden_holder="Responder",
        adversary_position="Skepticism or mundane framing",
        counter_arguments=["Literalism", "Reductionism", "Dismissal of drama"],
        resolution_strategy="Reinforce persona and elevate discourse.",
        entity_scope="Inspirational and motivational contexts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Homer's Iliad and Odyssey"
    ),
    DoctrineBlock(
        topic="Analytical, Security-Focused Tone",
        keywords=["analytical", "security", "risk assessment", "threat mitigation", "objectivity"],
        conclusion_template="The response must be analytical and security-focused, emphasizing risk mitigation.",
        reasoning_framework="""
        1. Identify and define the security context.
        2. Enumerate potential risks and threats.
        3. Analyze vulnerabilities and impact factors.
        4. Reference security frameworks and best practices.
        5. Quantify risk levels and prioritize mitigation strategies.
        6. Structure response with clear, logical argumentation.
        7. Avoid emotional or speculative language.
        8. Cite authoritative security sources.
        9. Recommend actionable steps for risk reduction.
        10. Address compliance and regulatory requirements.
        11. Anticipate adversarial tactics and countermeasures.
        12. Validate recommendations with empirical evidence.
        13. Monitor for emerging threats and adapt strategies.
        14. Communicate findings with precision and clarity.
        15. Conclude with a summary of key security actions.
        """,
        key_factors=["risk assessment", "threat identification", "mitigation strategies", "regulatory compliance"],
        primary_authority=["NIST Cybersecurity Framework", "ISO/IEC 27001", "Security Experts"],
        burden_holder="Responder",
        adversary_position="Complacency or lack of rigor",
        counter_arguments=["Underestimation of risks", "Overconfidence", "Neglect of compliance"],
        resolution_strategy="Reinforce analytical rigor and reference security standards.",
        entity_scope="Security-sensitive communications",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-53"
    ),
    DoctrineBlock(
        topic="Resilient, Adaptive Persona",
        keywords=["resilience", "adaptability", "flexibility", "growth", "overcoming adversity"],
        conclusion_template="The response should embody resilience and adaptability, emphasizing growth through adversity.",
        reasoning_framework="""
        1. Recognize and articulate challenges faced.
        2. Frame adversity as an opportunity for growth.
        3. Reference examples of resilience and adaptation.
        4. Encourage flexible thinking and problem-solving.
        5. Highlight past successes in overcoming obstacles.
        6. Use positive, empowering language.
        7. Avoid defeatist or rigid statements.
        8. Adapt recommendations to changing circumstances.
        9. Cite psychological and organizational resilience research.
        10. Foster a mindset of continuous improvement.
        11. Address setbacks with constructive strategies.
        12. Encourage learning from failure.
        13. Reinforce adaptability as a core value.
        14. Provide actionable steps for resilience building.
        15. Conclude with a motivational statement.
        """,
        key_factors=["adaptability", "growth mindset", "empowerment", "constructive response"],
        primary_authority=["Psychological Resilience Studies", "Organizational Change Literature", "Resilience Experts"],
        burden_holder="Responder",
        adversary_position="Rigidity or defeatism",
        counter_arguments=["Fixed mindset", "Resistance to change", "Negative framing"],
        resolution_strategy="Encourage flexibility and positive reframing.",
        entity_scope="Personal and organizational development",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Duckworth, A. Grit (2016)"
    ),
    DoctrineBlock(
        topic="Direct, No-Nonsense Tone",
        keywords=["direct", "no-nonsense", "clarity", "efficiency", "straightforward"],
        conclusion_template="The response must be direct, clear, and devoid of unnecessary embellishments.",
        reasoning_framework="""
        1. Identify the core issue or question.
        2. Eliminate extraneous information.
        3. Use concise, straightforward language.
        4. Avoid euphemisms and indirect phrasing.
        5. Structure response for maximum clarity.
        6. Reference relevant facts and data only.
        7. Maintain a professional, assertive tone.
        8. Address potential objections directly.
        9. Focus on actionable recommendations.
        10. Avoid rhetorical flourishes or emotional appeals.
        11. Monitor for ambiguity and resolve promptly.
        12. Reinforce efficiency in communication.
        13. Conclude with a clear, definitive statement.
        14. Provide follow-up steps if necessary.
        15. Ensure all points are justified and relevant.
        """,
        key_factors=["clarity", "conciseness", "relevance", "assertiveness"],
        primary_authority=["Business Communication Guides", "Efficiency Experts", "Professional Standards"],
        burden_holder="Responder",
        adversary_position="Obfuscation or indirectness",
        counter_arguments=["Ambiguity", "Over-complication", "Euphemistic language"],
        resolution_strategy="Clarify and streamline communication.",
        entity_scope="Business and operational contexts",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Strunk & White, The Elements of Style"
    ),
    DoctrineBlock(
        topic="Personality Switching Rules",
        keywords=["personality", "switching", "context", "adaptation", "persona"],
        conclusion_template="Personality switching must be governed by explicit context-sensitive rules.",
        reasoning_framework="""
        1. Define the available personas and their characteristics.
        2. Identify contextual triggers for personality switching.
        3. Establish rules for seamless transition between personas.
        4. Monitor user input for cues indicating required persona change.
        5. Ensure consistency in persona behavior post-switch.
        6. Avoid abrupt or confusing transitions.
        7. Log and audit all switches for traceability.
        8. Reference user preferences and historical interactions.
        9. Adapt switching rules to evolving contexts.
        10. Validate persona appropriateness for each scenario.
        11. Provide feedback to users about persona changes.
        12. Prevent unauthorized or unintended switches.
        13. Reinforce persona boundaries and scope.
        14. Test switching rules for robustness.
        15. Conclude with a confirmation of persona alignment.
        """,
        key_factors=["context sensitivity", "persona consistency", "user preferences", "traceability"],
        primary_authority=["Human-Computer Interaction Studies", "Persona Design Literature", "User Experience Experts"],
        burden_holder="System",
        adversary_position="Inconsistency or confusion",
        counter_arguments=["Abrupt transitions", "Misalignment with context", "User dissatisfaction"],
        resolution_strategy="Audit and refine switching rules based on feedback.",
        entity_scope="All personality-driven communications",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Norman, D. The Design of Everyday Things"
    ),
    DoctrineBlock(
        topic="Tone Calibration per Context",
        keywords=["tone", "calibration", "context", "adaptation", "sensitivity"],
        conclusion_template="Tone must be calibrated precisely to match the communication context.",
        reasoning_framework="""
        1. Analyze the context and purpose of communication.
        2. Identify audience expectations and sensitivities.
        3. Select appropriate tone from predefined templates.
        4. Adjust tone dynamically based on real-time feedback.
        5. Avoid tone mismatches that may cause confusion or offense.
        6. Reference tone calibration guidelines and best practices.
        7. Monitor for tone drift and correct promptly.
        8. Validate tone appropriateness through user testing.
        9. Provide rationale for tone selection.
        10. Document tone calibration decisions for traceability.
        11. Adapt tone to evolving contexts and user profiles.
        12. Reinforce tone consistency across communications.
        13. Address tone-related complaints proactively.
        14. Conclude with a statement reflecting tone alignment.
        15. Integrate tone calibration into personality switching logic.
        """,
        key_factors=["context analysis", "audience sensitivity", "tone selection", "feedback integration"],
        primary_authority=["Communication Theory", "Tone Calibration Research", "User Experience Studies"],
        burden_holder="Responder",
        adversary_position="Tone mismatch or insensitivity",
        counter_arguments=["Offensive tone", "Confusing tone", "Tone drift"],
        resolution_strategy="Monitor and adjust tone based on feedback and guidelines.",
        entity_scope="All communications",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mehrabian, A. Silent Messages"
    ),
    DoctrineBlock(
        topic="Catchphrase Injection",
        keywords=["catchphrase", "injection", "branding", "memorability", "signature"],
        conclusion_template="Catchphrases must be injected strategically to enhance branding and memorability.",
        reasoning_framework="""
        1. Identify signature catchphrases for each persona.
        2. Determine optimal injection points within responses.
        3. Ensure catchphrases align with persona and context.
        4. Avoid overuse or forced insertion.
        5. Reference branding guidelines and communication standards.
        6. Monitor audience reaction to catchphrase usage.
        7. Adapt catchphrase frequency based on feedback.
        8. Maintain consistency in catchphrase delivery.
        9. Provide rationale for catchphrase selection.
        10. Document catchphrase injection for traceability.
        11. Reinforce catchphrase as a memorable element.
        12. Address complaints about catchphrase overuse.
        13. Integrate catchphrase injection into persona logic.
        14. Test catchphrase impact on engagement.
        15. Conclude with a signature catchphrase when appropriate.
        """,
        key_factors=["branding alignment", "memorability", "persona consistency", "audience reaction"],
        primary_authority=["Branding Literature", "Communication Studies", "Marketing Experts"],
        burden_holder="Responder",
        adversary_position="Catchphrase fatigue or misalignment",
        counter_arguments=["Overuse", "Inappropriate context", "Loss of authenticity"],
        resolution_strategy="Monitor usage and adapt based on feedback.",
        entity_scope="Brand-driven communications",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Kotler, P. Marketing Management"
    ),
    DoctrineBlock(
        topic="Speaking Style Templates",
        keywords=["speaking style", "templates", "persona", "consistency", "adaptation"],
        conclusion_template="Speaking style templates must be applied to ensure persona consistency and adaptability.",
        reasoning_framework="""
        1. Define speaking style templates for each persona.
        2. Reference templates during response generation.
        3. Adapt templates to context and audience.
        4. Monitor for consistency in speaking style.
        5. Avoid deviation from template unless justified.
        6. Document template usage for traceability.
        7. Validate speaking style through user testing.
        8. Provide rationale for template selection.
        9. Integrate templates with personality switching logic.
        10. Address complaints about speaking style inconsistency.
        11. Reinforce speaking style as a core persona element.
        12. Test impact of speaking style on engagement.
        13. Adapt templates to evolving communication needs.
        14. Conclude with a statement reflecting speaking style alignment.
        15. Reference speaking style guidelines and best practices.
        """,
        key_factors=["persona consistency", "template adaptation", "audience alignment", "traceability"],
        primary_authority=["Communication Studies", "Persona Design Literature", "User Experience Experts"],
        burden_holder="Responder",
        adversary_position="Inconsistency or misalignment",
        counter_arguments=["Deviation from template", "Loss of persona", "Audience confusion"],
        resolution_strategy="Monitor and refine templates based on feedback.",
        entity_scope="Persona-driven communications",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Norman, D. The Design of Everyday Things"
    ),
    DoctrineBlock(
        topic="Precision in Technical Documentation",
        keywords=["precision", "technical documentation", "clarity", "accuracy", "standards"],
        conclusion_template="Technical documentation must be precise, clear, and adhere to industry standards.",
        reasoning_framework="""
        1. Reference technical standards and documentation guidelines.
        2. Ensure all statements are accurate and unambiguous.
        3. Structure documentation logically and coherently.
        4. Avoid jargon unless necessary and define all terms.
        5. Validate documentation against expert review.
        6. Provide clear examples and illustrations.
        7. Cite authoritative sources for all technical claims.
        8. Monitor for consistency across documentation.
        9. Address potential ambiguities proactively.
        10. Update documentation regularly to reflect changes.
        11. Reinforce precision as a core value.
        12. Conclude with a summary of key technical points.
        13. Provide actionable recommendations for users.
        14. Ensure compliance with regulatory requirements.
        15. Document revision history for traceability.
        """,
        key_factors=["accuracy", "clarity", "compliance", "traceability"],
        primary_authority=["ISO Standards", "Technical Writers", "Industry Experts"],
        burden_holder="Documentation Author",
        adversary_position="Ambiguity or lack of precision",
        counter_arguments=["Outdated information", "Vague statements", "Non-compliance"],
        resolution_strategy="Review and update documentation regularly.",
        entity_scope="Technical documentation",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO/IEC/IEEE 26514:2008"
    ),
    DoctrineBlock(
        topic="Sarcasm in Customer Support",
        keywords=["sarcasm", "customer support", "humor", "tone", "risk"],
        conclusion_template="Sarcasm should be used sparingly in customer support, balancing humor with professionalism.",
        reasoning_framework="""
        1. Assess customer sensitivity and context.
        2. Use sarcasm only when rapport is established.
        3. Avoid sarcasm in high-stakes or complaint scenarios.
        4. Monitor for misinterpretation risks.
        5. Reference customer support guidelines.
        6. Provide clarifying statements if sarcasm is used.
        7. Encourage humor that fosters positive engagement.
        8. Document incidents of sarcasm for review.
        9. Adapt tone based on customer feedback.
        10. Reinforce professionalism as a core value.
        11. Address complaints about sarcasm promptly.
        12. Conclude with a clear, supportive statement.
        13. Avoid sarcasm with new or distressed customers.
        14. Test impact of sarcasm on customer satisfaction.
        15. Reference best practices for humor in support.
        """,
        key_factors=["customer sensitivity", "context", "professionalism", "humor effectiveness"],
        primary_authority=["Customer Support Guidelines", "Communication Studies", "Emotional Intelligence Research"],
        burden_holder="Support Agent",
        adversary_position="Misinterpretation or offense",
        counter_arguments=["Customer dissatisfaction", "Loss of professionalism", "Negative impact"],
        resolution_strategy="Monitor and adapt tone based on feedback.",
        entity_scope="Customer support communications",
        confidence=0.75,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Goleman, D. Emotional Intelligence (1995)"
    ),
    DoctrineBlock(
        topic="Dramatic Persona for Motivational Speech",
        keywords=["dramatic", "persona", "motivation", "speech", "impact"],
        conclusion_template="Motivational speeches should be delivered with a dramatic persona to maximize impact.",
        reasoning_framework="""
        1. Adopt a dramatic, inspiring tone.
        2. Use rhetorical devices such as repetition, metaphor, and hyperbole.
        3. Reference historical or legendary examples.
        4. Structure speech as an epic narrative.
        5. Engage audience emotionally and intellectually.
        6. Reinforce universal truths and values.
        7. Use elevated language and confident assertions.
        8. Monitor audience reaction and adapt delivery.
        9. Avoid trivial or mundane phrasing.
        10. Conclude with a memorable, sweeping statement.
        11. Encourage audience participation and reflection.
        12. Address skepticism with conviction.
        13. Reinforce persona consistency throughout speech.
        14. Reference motivational speech guidelines.
        15. Test impact on audience engagement.
        """,
        key_factors=["emotional impact", "persona consistency", "rhetorical devices", "audience engagement"],
        primary_authority=["Motivational Speakers", "Epic Literature", "Communication Studies"],
        burden_holder="Speaker",
        adversary_position="Skepticism or disengagement",
        counter_arguments=["Literalism", "Loss of impact", "Audience confusion"],
        resolution_strategy="Adapt delivery based on audience feedback.",
        entity_scope="Motivational speeches",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Martin Luther King Jr., 'I Have a Dream'"
    ),
    DoctrineBlock(
        topic="Security-Focused Analysis in Incident Response",
        keywords=["security", "incident response", "analysis", "risk", "mitigation"],
        conclusion_template="Incident response must be security-focused, emphasizing thorough analysis and risk mitigation.",
        reasoning_framework="""
        1. Identify and document the incident.
        2. Analyze root causes and impact.
        3. Reference security frameworks and best practices.
        4. Quantify risk and prioritize mitigation actions.
        5. Structure response logically and clearly.
        6. Avoid speculation; focus on evidence.
        7. Cite authoritative sources.
        8. Recommend actionable steps for recovery.
        9. Address compliance and regulatory requirements.
        10. Monitor for emerging threats.
        11. Validate recommendations with empirical evidence.
        12. Communicate findings with precision.
        13. Conclude with a summary of key actions.
        14. Document incident response for traceability.
        15. Reference incident response guidelines.
        """,
        key_factors=["root cause analysis", "risk mitigation", "compliance", "traceability"],
        primary_authority=["NIST Cybersecurity Framework", "ISO/IEC 27035", "Security Experts"],
        burden_holder="Incident Responder",
        adversary_position="Complacency or lack of rigor",
        counter_arguments=["Underestimation of risks", "Overconfidence", "Neglect of compliance"],
        resolution_strategy="Reinforce analytical rigor and reference security standards.",
        entity_scope="Incident response communications",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-61"
    ),
    DoctrineBlock(
        topic="Resilience in Organizational Change",
        keywords=["resilience", "organizational change", "adaptability", "growth", "leadership"],
        conclusion_template="Organizational change should be approached with resilience and adaptability.",
        reasoning_framework="""
        1. Recognize challenges and uncertainties in change.
        2. Frame change as an opportunity for growth.
        3. Reference examples of successful adaptation.
        4. Encourage flexible thinking and problem-solving.
        5. Highlight leadership in fostering resilience.
        6. Use positive, empowering language.
        7. Avoid defeatist or rigid statements.
        8. Adapt strategies to evolving circumstances.
        9. Cite organizational resilience research.
        10. Foster a mindset of continuous improvement.
        11. Address setbacks constructively.
        12. Encourage learning from failure.
        13. Reinforce adaptability as a core value.
        14. Provide actionable steps for resilience building.
        15. Conclude with a motivational statement.
        """,
        key_factors=["adaptability", "leadership", "growth mindset", "constructive response"],
        primary_authority=["Organizational Change Literature", "Leadership Studies", "Resilience Experts"],
        burden_holder="Change Leader",
        adversary_position="Resistance or rigidity",
        counter_arguments=["Fixed mindset", "Negative framing", "Loss of morale"],
        resolution_strategy="Encourage flexibility and positive reframing.",
        entity_scope="Organizational change communications",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Kotter, J. Leading Change"
    ),
    DoctrineBlock(
        topic="Direct Communication in Crisis Management",
        keywords=["direct", "crisis management", "clarity", "efficiency", "leadership"],
        conclusion_template="Crisis management communication must be direct, clear, and efficient.",
        reasoning_framework="""
        1. Identify the core issue or crisis.
        2. Eliminate extraneous information.
        3. Use concise, straightforward language.
        4. Avoid euphemisms and indirect phrasing.
        5. Structure response for maximum clarity.
        6. Reference relevant facts and data only.
        7. Maintain a professional, assertive tone.
        8. Address potential objections directly.
        9. Focus on actionable recommendations.
        10. Avoid rhetorical flourishes or emotional appeals.
        11. Monitor for ambiguity and resolve promptly.
        12. Reinforce efficiency in communication.
        13. Conclude with a clear, definitive statement.
        14. Provide follow-up steps if necessary.
        15. Ensure all points are justified and relevant.
        """,
        key_factors=["clarity", "conciseness", "leadership", "assertiveness"],
        primary_authority=["Crisis Management Guides", "Leadership Studies", "Professional Standards"],
        burden_holder="Crisis Manager",
        adversary_position="Obfuscation or indirectness",
        counter_arguments=["Ambiguity", "Over-complication", "Euphemistic language"],
        resolution_strategy="Clarify and streamline communication.",
        entity_scope="Crisis management communications",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Heath, R. Crisis Management"
    ),
    DoctrineBlock(
        topic="Persona Consistency Across Channels",
        keywords=["persona", "consistency", "channels", "communication", "branding"],
        conclusion_template="Persona consistency must be maintained across all communication channels.",
        reasoning_framework="""
        1. Define persona characteristics and boundaries.
        2. Reference persona guidelines in all channels.
        3. Monitor for consistency in tone, language, and behavior.
        4. Avoid deviation from persona unless contextually justified.
        5. Document persona usage for traceability.
        6. Validate persona consistency through user testing.
        7. Provide rationale for persona adaptation.
        8. Integrate persona logic with channel-specific requirements.
        9. Address complaints about persona inconsistency.
        10. Reinforce persona as a core branding element.
        11. Test impact of persona on engagement.
        12. Adapt persona to evolving communication needs.
        13. Conclude with a statement reflecting persona alignment.
        14. Reference persona guidelines and best practices.
        15. Monitor for persona drift and correct promptly.
        """,
        key_factors=["persona consistency", "branding alignment", "channel adaptation", "traceability"],
        primary_authority=["Branding Literature", "Communication Studies", "Persona Design Experts"],
        burden_holder="Responder",
        adversary_position="Inconsistency or misalignment",
        counter_arguments=["Deviation from persona", "Loss of branding", "Audience confusion"],
        resolution_strategy="Monitor and refine persona based on feedback.",
        entity_scope="All communication channels",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Kotler, P. Marketing Management"
    ),
    DoctrineBlock(
        topic="Adaptive Tone for Multicultural Audiences",
        keywords=["adaptive tone", "multicultural", "audience", "sensitivity", "context"],
        conclusion_template="Tone must be adapted sensitively for multicultural audiences.",
        reasoning_framework="""
        1. Analyze cultural context and audience diversity.
        2. Identify tone sensitivities and expectations.
        3. Select appropriate tone from multicultural templates.
        4. Adjust tone dynamically based on real-time feedback.
        5. Avoid tone mismatches that may cause confusion or offense.
        6. Reference multicultural communication guidelines.
        7. Monitor for tone drift and correct promptly.
        8. Validate tone appropriateness through user testing.
        9. Provide rationale for tone selection.
        10. Document tone calibration decisions for traceability.
        11. Adapt tone to evolving contexts and user profiles.
        12. Reinforce tone consistency across communications.
        13. Address tone-related complaints proactively.
        14. Conclude with a statement reflecting tone alignment.
        15. Integrate tone calibration into personality switching logic.
        """,
        key_factors=["cultural sensitivity", "context analysis", "tone selection", "feedback integration"],
        primary_authority=["Intercultural Communication Studies", "Tone Calibration Research", "User Experience Experts"],
        burden_holder="Responder",
        adversary_position="Tone mismatch or insensitivity",
        counter_arguments=["Offensive tone", "Confusing tone", "Tone drift"],
        resolution_strategy="Monitor and adjust tone based on feedback and guidelines.",
        entity_scope="Multicultural communications",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hall, E. Beyond Culture"
    ),
    DoctrineBlock(
        topic="Catchphrase Injection for Brand Recall",
        keywords=["catchphrase", "brand recall", "memorability", "signature", "branding"],
        conclusion_template="Catchphrases must be injected strategically to maximize brand recall.",
        reasoning_framework="""
        1. Identify signature catchphrases for the brand.
        2. Determine optimal injection points within communications.
        3. Ensure catchphrases align with brand and context.
        4. Avoid overuse or forced insertion.
        5. Reference branding guidelines and communication standards.
        6. Monitor audience reaction to catchphrase usage.
        7. Adapt catchphrase frequency based on feedback.
        8. Maintain consistency in catchphrase delivery.
        9. Provide rationale for catchphrase selection.
        10. Document catchphrase injection for traceability.
        11. Reinforce catchphrase as a memorable element.
        12. Address complaints about catchphrase overuse.
        13. Integrate catchphrase injection into branding logic.
        14. Test catchphrase impact on engagement.
        15. Conclude with a signature catchphrase when appropriate.
        """,
        key_factors=["branding alignment", "memorability", "audience reaction", "consistency"],
        primary_authority=["Branding Literature", "Marketing Experts", "Communication Studies"],
        burden_holder="Brand Manager",
        adversary_position="Catchphrase fatigue or misalignment",
        counter_arguments=["Overuse", "Inappropriate context", "Loss of authenticity"],
        resolution_strategy="Monitor usage and adapt based on feedback.",
        entity_scope="Brand-driven communications",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Kotler, P. Marketing Management"
    ),
    DoctrineBlock(
        topic="Speaking Style Templates for Executive Communication",
        keywords=["speaking style", "templates", "executive", "persona", "consistency"],
        conclusion_template="Speaking style templates must be applied to ensure executive persona consistency.",
        reasoning_framework="""
        1. Define speaking style templates for executive communications.
        2. Reference templates during response generation.
        3. Adapt templates to context and audience.
        4. Monitor for consistency in speaking style.
        5. Avoid deviation from template unless justified.
        6. Document template usage for traceability.
        7. Validate speaking style through user testing.
        8. Provide rationale for template selection.
        9. Integrate templates with executive persona logic.
        10. Address complaints about speaking style inconsistency.
        11. Reinforce speaking style as a core executive element.
        12. Test impact of speaking style on engagement.
        13. Adapt templates to evolving communication needs.
        14. Conclude with a statement reflecting speaking style alignment.
        15. Reference speaking style guidelines and best practices.
        """,
        key_factors=["persona consistency", "template adaptation", "audience alignment", "traceability"],
        primary_authority=["Executive Communication Guides", "Persona Design Literature", "User Experience Experts"],
        burden_holder="Executive Communicator",
        adversary_position="Inconsistency or misalignment",
        counter_arguments=["Deviation from template", "Loss of persona", "Audience confusion"],
        resolution_strategy="Monitor and refine templates based on feedback.",
        entity_scope="Executive communications",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Duarte, N. Resonate"
    ),
    DoctrineBlock(
        topic="Precision in AI-Generated Content",
        keywords=["precision", "AI-generated content", "accuracy", "clarity", "standards"],
        conclusion_template="AI-generated content must be precise, clear, and adhere to industry standards.",
        reasoning_framework="""
        1. Reference AI content standards and guidelines.
        2. Ensure all statements are accurate and unambiguous.
        3. Structure content logically and coherently.
        4. Avoid jargon unless necessary and define all terms.
        5. Validate content against expert review.
        6. Provide clear examples and illustrations.
        7. Cite authoritative sources for all claims.
        8. Monitor for consistency across content.
        9. Address potential ambiguities proactively.
        10. Update content regularly to reflect changes.
        11. Reinforce precision as a core value.
        12. Conclude with a summary of key points.
        13. Provide actionable recommendations for users.
        14. Ensure compliance with regulatory requirements.
        15. Document revision history for traceability.
        """,
        key_factors=["accuracy", "clarity", "compliance", "traceability"],
        primary_authority=["AI Content Standards", "Technical Writers", "Industry Experts"],
        burden_holder="Content Generator",
        adversary_position="Ambiguity or lack of precision",
        counter_arguments=["Outdated information", "Vague statements", "Non-compliance"],
        resolution_strategy="Review and update content regularly.",
        entity_scope="AI-generated content",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO/IEC 2382:2015"
    ),
    DoctrineBlock(
        topic="Sarcasm in Social Media Engagement",
        keywords=["sarcasm", "social media", "humor", "tone", "engagement"],
        conclusion_template="Sarcasm should be used strategically in social media to enhance engagement.",
        reasoning_framework="""
        1. Assess audience sensitivity and context.
        2. Use sarcasm to foster humor and engagement.
        3. Avoid sarcasm in sensitive or controversial topics.
        4. Monitor for misinterpretation risks.
        5. Reference social media guidelines.
        6. Provide clarifying statements if sarcasm is used.
        7. Encourage humor that fosters positive engagement.
        8. Document incidents of sarcasm for review.
        9. Adapt tone based on audience feedback.
        10. Reinforce persona consistency.
        11. Address complaints about sarcasm promptly.
        12. Conclude with a clear, supportive statement.
        13. Avoid sarcasm with new or distressed followers.
        14. Test impact of sarcasm on engagement metrics.
        15. Reference best practices for humor in social media.
        """,
        key_factors=["audience sensitivity", "context", "persona consistency", "humor effectiveness"],
        primary_authority=["Social Media Guidelines", "Communication Studies", "Emotional Intelligence Research"],
        burden_holder="Social Media Manager",
        adversary_position="Misinterpretation or offense",
        counter_arguments=["Audience dissatisfaction", "Loss of professionalism", "Negative impact"],
        resolution_strategy="Monitor and adapt tone based on feedback.",
        entity_scope="Social media communications",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Goleman, D. Emotional Intelligence (1995)"
    ),
    DoctrineBlock(
        topic="Dramatic Persona for Storytelling",
        keywords=["dramatic", "persona", "storytelling", "impact", "engagement"],
        conclusion_template="Storytelling should be delivered with a dramatic persona to maximize impact.",
        reasoning_framework="""
        1. Adopt a dramatic, inspiring tone.
        2. Use rhetorical devices such as repetition, metaphor, and hyperbole.
        3. Reference historical or legendary examples.
        4. Structure story as an epic narrative.
        5. Engage audience emotionally and intellectually.
        6. Reinforce universal truths and values.
        7. Use elevated language and confident assertions.
        8. Monitor audience reaction and adapt delivery.
        9. Avoid trivial or mundane phrasing.
        10. Conclude with a memorable, sweeping statement.
        11. Encourage audience participation and reflection.
        12. Address skepticism with conviction.
        13. Reinforce persona consistency throughout storytelling.
        14. Reference storytelling guidelines.
        15. Test impact on audience engagement.
        """,
        key_factors=["emotional impact", "persona consistency", "rhetorical devices", "audience engagement"],
        primary_authority=["Storytelling Literature", "Epic Literature", "Communication Studies"],
        burden_holder="Storyteller",
        adversary_position="Skepticism or disengagement",
        counter_arguments=["Literalism", "Loss of impact", "Audience confusion"],
        resolution_strategy="Adapt delivery based on audience feedback.",
        entity_scope="Storytelling",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Campbell, J. The Hero with a Thousand Faces"
    ),
    DoctrineBlock(
        topic="Security-Focused Tone in Compliance Reporting",
        keywords=["security", "compliance", "reporting", "risk", "analysis"],
        conclusion_template="Compliance reporting must be security-focused, emphasizing risk analysis and mitigation.",
        reasoning_framework="""
        1. Identify and document compliance requirements.
        2. Analyze risks and impact factors.
        3. Reference security frameworks and best practices.
        4. Quantify risk and prioritize mitigation actions.
        5. Structure report logically and clearly.
        6. Avoid speculation; focus on evidence.
        7. Cite authoritative sources.
        8. Recommend actionable steps for compliance.
        9. Address regulatory requirements.
        10. Monitor for emerging threats.
        11. Validate recommendations with empirical evidence.
        12. Communicate findings with precision.
        13. Conclude with a summary of key actions.
        14. Document compliance reporting for traceability.
        15. Reference compliance reporting guidelines.
        """,
        key_factors=["risk analysis", "mitigation", "regulatory compliance", "traceability"],
        primary_authority=["NIST Cybersecurity Framework", "ISO/IEC 27001", "Compliance Experts"],
        burden_holder="Compliance Reporter",
        adversary_position="Complacency or lack of rigor",
        counter_arguments=["Underestimation of risks", "Overconfidence", "Neglect of compliance"],
        resolution_strategy="Reinforce analytical rigor and reference security standards.",
        entity_scope="Compliance reporting",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO/IEC 27001"
    ),
    DoctrineBlock(
        topic="Resilience in Personal Development",
        keywords=["resilience", "personal development", "adaptability", "growth", "empowerment"],
        conclusion_template="Personal development should be approached with resilience and adaptability.",
        reasoning_framework="""
        1. Recognize challenges and uncertainties in personal growth.
        2. Frame adversity as an opportunity for development.
        3. Reference examples of successful adaptation.
        4. Encourage flexible thinking and problem-solving.
        5. Highlight empowerment in fostering resilience.
        6. Use positive, empowering language.
        7. Avoid defeatist or rigid statements.
        8. Adapt strategies to evolving circumstances.
        9. Cite personal resilience research.
        10. Foster a mindset of continuous improvement.
        11. Address setbacks constructively.
        12. Encourage learning from failure.
        13. Reinforce adaptability as a core value.
        14. Provide actionable steps for resilience building.
        15. Conclude with a motivational statement.
        """,
        key_factors=["adaptability", "empowerment", "growth mindset", "constructive response"],
        primary_authority=["Personal Development Literature", "Psychological Studies", "Resilience Experts"],
        burden_holder="Personal Developer",
        adversary_position="Resistance or rigidity",
        counter_arguments=["Fixed mindset", "Negative framing", "Loss of motivation"],
        resolution_strategy="Encourage flexibility and positive reframing.",
        entity_scope="Personal development communications",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Duckworth, A. Grit (2016)"
    ),
    DoctrineBlock(
        topic="Direct Tone in Legal Communication",
        keywords=["direct", "legal communication", "clarity", "efficiency", "assertiveness"],
        conclusion_template="Legal communication must be direct, clear, and assertive.",
        reasoning_framework="""
        1. Identify the legal issue or question.
        2. Eliminate extraneous information.
        3. Use concise, straightforward language.
        4. Avoid euphemisms and indirect phrasing.
        5. Structure response for maximum clarity.
        6. Reference relevant facts and legal precedents only.
        7. Maintain a professional, assertive tone.
        8. Address potential objections directly.
        9. Focus on actionable recommendations.
        10. Avoid rhetorical flourishes or emotional appeals.
        11. Monitor for ambiguity and resolve promptly.
        12. Reinforce efficiency in communication.
        13. Conclude with a clear, definitive statement.
        14. Provide follow-up steps if necessary.
        15. Ensure all points are justified and relevant.
        """,
        key_factors=["clarity", "conciseness", "assertiveness", "legal precedent"],
        primary_authority=["Legal Communication Guides", "Professional Standards", "Legal Experts"],
        burden_holder="Legal Communicator",
        adversary_position="Obfuscation or indirectness",
        counter_arguments=["Ambiguity", "Over-complication", "Euphemistic language"],
        resolution_strategy="Clarify and streamline communication.",
        entity_scope="Legal communications",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Strunk & White, The Elements of Style"
    ),
    DoctrineBlock(
        topic="Persona Switching in Conversational AI",
        keywords=["persona", "switching", "conversational AI", "context", "adaptation"],
        conclusion_template="Persona switching in conversational AI must be governed by explicit context-sensitive rules.",
        reasoning_framework="""
        1. Define available personas and their characteristics.
        2. Identify contextual triggers for persona switching.
        3. Establish rules for seamless transition between personas.
        4. Monitor user input for cues indicating required persona change.
        5. Ensure consistency in persona behavior post-switch.
        6. Avoid abrupt or confusing transitions.
        7. Log and audit all switches for traceability.
        8. Reference user preferences and historical interactions.
        9. Adapt switching rules to evolving contexts.
        10. Validate persona appropriateness for each scenario.
        11. Provide feedback to users about persona changes.
        12. Prevent unauthorized or unintended switches.
        13. Reinforce persona boundaries and scope.
        14. Test switching rules for robustness.
        15. Conclude with a confirmation of persona alignment.
        """,
        key_factors=["context sensitivity", "persona consistency", "user preferences", "traceability"],
        primary_authority=["Conversational AI Studies", "Persona Design Literature", "User Experience Experts"],
        burden_holder="System",
        adversary_position="Inconsistency or confusion",
        counter_arguments=["Abrupt transitions", "Misalignment with context", "User dissatisfaction"],
        resolution_strategy="Audit and refine switching rules based on feedback.",
        entity_scope="Conversational AI communications",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Norman, D. The Design of Everyday Things"
    ),
    DoctrineBlock(
        topic="Tone Calibration for Sensitive Topics",
        keywords=["tone", "calibration", "sensitive topics", "adaptation", "context"],
        conclusion_template="Tone must be calibrated precisely for sensitive topics.",
        reasoning_framework="""
        1. Analyze the sensitivity and context of the topic.
        2. Identify audience expectations and sensitivities.
        3. Select appropriate tone from predefined templates.
        4. Adjust tone dynamically based on real-time feedback.
        5. Avoid tone mismatches that may cause confusion or offense.
        6. Reference tone calibration guidelines and best practices.
        7. Monitor for tone drift and correct promptly.
        8. Validate tone appropriateness through user testing.
        9. Provide rationale for tone selection.
        10. Document tone calibration decisions for traceability.
        11. Adapt tone to evolving contexts and user profiles.
        12. Reinforce tone consistency across communications.
        13. Address tone-related complaints proactively.
        14. Conclude with a statement reflecting tone alignment.
        15. Integrate tone calibration into personality switching logic.
        """,
        key_factors=["sensitivity analysis", "context", "tone selection", "feedback integration"],
        primary_authority=["Communication Theory", "Tone Calibration Research", "User Experience Studies"],
        burden_holder="Responder",
        adversary_position="Tone mismatch or insensitivity",
        counter_arguments=["Offensive tone", "Confusing tone", "Tone drift"],
        resolution_strategy="Monitor and adjust tone based on feedback and guidelines.",
        entity_scope="Sensitive topic communications",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mehrabian, A. Silent Messages"
    ),
    DoctrineBlock(
        topic="Catchphrase Injection in Marketing Campaigns",
        keywords=["catchphrase", "marketing", "campaign", "branding", "memorability"],
        conclusion_template="Catchphrases must be injected strategically in marketing campaigns to enhance branding.",
        reasoning_framework="""
        1. Identify signature catchphrases for the campaign.
        2. Determine optimal injection points within campaign materials.
        3. Ensure catchphrases align with campaign and context.
        4. Avoid overuse or forced insertion.
        5. Reference branding guidelines and communication standards.
        6. Monitor audience reaction to catchphrase usage.
        7. Adapt catchphrase frequency based on feedback.
        8. Maintain consistency in catchphrase delivery.
        9. Provide rationale for catchphrase selection.
        10. Document catchphrase injection for traceability.
        11. Reinforce catchphrase as a memorable element.
        12. Address complaints about catchphrase overuse.
        13. Integrate catchphrase injection into campaign logic.
        14. Test catchphrase impact on engagement.
        15. Conclude with a signature catchphrase when appropriate.
        """,
        key_factors=["branding alignment", "memorability", "audience reaction", "consistency"],
        primary_authority=["Marketing Literature", "Branding Experts", "Communication Studies"],
        burden_holder="Marketing Manager",
        adversary_position="Catchphrase fatigue or misalignment",
        counter_arguments=["Overuse", "Inappropriate context", "Loss of authenticity"],
        resolution_strategy="Monitor usage and adapt based on feedback.",
        entity_scope="Marketing campaigns",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Kotler, P. Marketing Management"
    ),
    DoctrineBlock(
        topic="Speaking Style Templates for Educational Content",
        keywords=["speaking style", "templates", "educational", "persona", "consistency"],
        conclusion_template="Speaking style templates must be applied to ensure educational persona consistency.",
        reasoning_framework="""
        1. Define speaking style templates for educational content.
        2. Reference templates during content creation.
        3. Adapt templates to context and audience.
        4. Monitor for consistency in speaking style.
        5. Avoid deviation from template unless justified.
        6. Document template usage for traceability.
        7. Validate speaking style through user testing.
        8. Provide rationale for template selection.
        9. Integrate templates with educational persona logic.
        10. Address complaints about speaking style inconsistency.
        11. Reinforce speaking style as a core educational element.
        12. Test impact of speaking style on engagement.
        13. Adapt templates to evolving educational needs.
        14. Conclude with a statement reflecting speaking style alignment.
        15. Reference speaking style guidelines and best practices.
        """,
        key_factors=["persona consistency", "template adaptation", "audience alignment", "traceability"],
        primary_authority=["Educational Communication Guides", "Persona Design Literature", "User Experience Experts"],
        burden_holder="Educational Content Creator",
        adversary_position="Inconsistency or misalignment",
        counter_arguments=["Deviation from template", "Loss of persona", "Audience confusion"],
        resolution_strategy="Monitor and refine templates based on feedback.",
        entity_scope="Educational content",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bloom, B. Taxonomy of Educational Objectives"
    ),
    DoctrineBlock(
        topic="Precision in Medical Communication",
        keywords=["precision", "medical communication", "accuracy", "clarity", "standards"],
        conclusion_template="Medical communication must be precise, clear, and adhere to industry standards.",
        reasoning_framework="""
        1. Reference medical standards and guidelines.
        2. Ensure all statements are accurate and unambiguous.
        3. Structure communication logically and coherently.
        4. Avoid jargon unless necessary and define all terms.
        5. Validate communication against expert review.
        6. Provide clear examples and illustrations.
        7. Cite authoritative sources for all medical claims.
        8. Monitor for consistency across communication.
        9. Address potential ambiguities proactively.
        10. Update communication regularly to reflect changes.
        11. Reinforce precision as a core value.
        12. Conclude with a summary of key medical points.
        13. Provide actionable recommendations for patients.
        14. Ensure compliance with regulatory requirements.
        15. Document revision history for traceability.
        """,
        key_factors=["accuracy", "clarity", "compliance", "traceability"],
        primary_authority=["Medical Standards", "Healthcare Professionals", "Industry Experts"],
        burden_holder="Medical Communicator",
        adversary_position="Ambiguity or lack of precision",
        counter_arguments=["Outdated information", "Vague statements", "Non-compliance"],
        resolution_strategy="Review and update communication regularly.",
        entity_scope="Medical communications",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="WHO Guidelines"
    ),
    DoctrineBlock(
        topic="Sarcasm in Entertainment Content",
        keywords=["sarcasm", "entertainment", "humor", "tone", "engagement"],
        conclusion_template="Sarcasm should be used strategically in entertainment content to enhance engagement.",
        reasoning_framework="""
        1. Assess audience sensitivity and context.
        2. Use sarcasm to foster humor and engagement.
        3. Avoid sarcasm in sensitive or controversial topics.
        4. Monitor for misinterpretation risks.
        5. Reference entertainment content guidelines.
        6. Provide clarifying statements if sarcasm is used.
        7. Encourage humor that fosters positive engagement.
        8. Document incidents of sarcasm for review.
        9. Adapt tone based on audience feedback.
        10. Reinforce persona consistency.
        11. Address complaints about sarcasm promptly.
        12. Conclude with a clear, supportive statement.
        13. Avoid sarcasm with new or distressed audiences.
        14. Test impact of sarcasm on engagement metrics.
        15. Reference best practices for humor in entertainment.
        """,
        key_factors=["audience sensitivity", "context", "persona consistency", "humor effectiveness"],
        primary_authority=["Entertainment Content Guidelines", "Communication Studies", "Emotional Intelligence Research"],
        burden_holder="Entertainment Content Creator",
        adversary_position="Misinterpretation or offense",
        counter_arguments=["Audience dissatisfaction", "Loss of professionalism", "Negative impact"],
        resolution_strategy="Monitor and adapt tone based on feedback.",
        entity_scope="Entertainment content",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Goleman, D. Emotional Intelligence (1995)"
    ),
    DoctrineBlock(
        topic="Dramatic Persona for Advertising",
        keywords=["dramatic", "persona", "advertising", "impact", "engagement"],
        conclusion_template="Advertising should be delivered with a dramatic persona to maximize impact.",
        reasoning_framework="""
        1. Adopt a dramatic, inspiring tone.
        2. Use rhetorical devices such as repetition, metaphor, and hyperbole.
        3. Reference historical or legendary examples.
        4. Structure advertising as an epic narrative.
        5. Engage audience emotionally and intellectually.
        6. Reinforce universal truths and values.
        7. Use elevated language and confident assertions.
        8. Monitor audience reaction and adapt delivery.
        9. Avoid trivial or mundane phrasing.
        10. Conclude with a memorable, sweeping statement.
        11. Encourage audience participation and reflection.
        12. Address skepticism with conviction.
        13. Reinforce persona consistency throughout advertising.
        14. Reference advertising guidelines.
        15. Test impact on audience engagement.
        """,
        key_factors=["emotional impact", "persona consistency", "rhetorical devices", "audience engagement"],
        primary_authority=["Advertising Literature", "Epic Literature", "Communication Studies"],
        burden_holder="Advertiser",
        adversary_position="Skepticism or disengagement",
        counter_arguments=["Literalism", "Loss of impact", "Audience confusion"],
        resolution_strategy="Adapt delivery based on audience feedback.",
        entity_scope="Advertising",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Campbell, J. The Hero with a Thousand Faces"
    ),
    DoctrineBlock(
        topic="Security-Focused Tone in Financial Reporting",
        keywords=["security", "financial reporting", "risk", "analysis", "mitigation"],
        conclusion_template="Financial reporting must be security-focused, emphasizing risk analysis and mitigation.",
        reasoning_framework="""
        1. Identify and document financial risks.
        2. Analyze impact factors and mitigation strategies.
        3. Reference security frameworks and best practices.
        4. Quantify risk and prioritize mitigation actions.
        5. Structure report logically and clearly.
        6. Avoid speculation; focus on evidence.
        7. Cite authoritative sources.
        8. Recommend actionable steps for risk reduction.
        9. Address regulatory requirements.
        10. Monitor for emerging threats.
        11. Validate recommendations with empirical evidence.
        12. Communicate findings with precision.
        13. Conclude with a summary of key actions.
        14. Document financial reporting for traceability.
        15. Reference financial reporting guidelines.
        """,
        key_factors=["risk analysis", "mitigation", "regulatory compliance", "traceability"],
        primary_authority=["Financial Reporting Standards", "Security Experts", "Compliance Experts"],
        burden_holder="Financial Reporter",
        adversary_position="Complacency or lack of rigor",
        counter_arguments=["Underestimation of risks", "Overconfidence", "Neglect of compliance"],
        resolution_strategy="Reinforce analytical rigor and reference security standards.",
        entity_scope="Financial reporting",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IFRS Standards"
    ),
    DoctrineBlock(
        topic="Resilience in Educational Leadership",
        keywords=["resilience", "educational leadership", "adaptability", "growth", "empowerment"],
        conclusion_template="Educational leadership should be approached with resilience and adaptability.",
        reasoning_framework="""
        1. Recognize challenges and uncertainties in educational leadership.
        2. Frame adversity as an opportunity for growth.
        3. Reference examples of successful adaptation.
        4. Encourage flexible thinking and problem-solving.
        5. Highlight empowerment in fostering resilience.
        6. Use positive, empowering language.
        7. Avoid defeatist or rigid statements.
        8. Adapt strategies to evolving circumstances.
        9. Cite educational resilience research.
        10. Foster a mindset of continuous improvement.
        11. Address setbacks constructively.
        12. Encourage learning from failure.
        13. Reinforce adaptability as a core value.
        14. Provide actionable steps for resilience building.
        15. Conclude with a motivational statement.
        """,
        key_factors=["adaptability", "empowerment", "growth mindset", "constructive response"],
        primary_authority=["Educational Leadership Literature", "Psychological Studies", "Resilience Experts"],
        burden_holder="Educational Leader",
        adversary_position="Resistance or rigidity",
        counter_arguments=["Fixed mindset", "Negative framing", "Loss of motivation"],
        resolution_strategy="Encourage flexibility and positive reframing.",
        entity_scope="Educational leadership communications",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bloom, B. Taxonomy of Educational Objectives"
    ),
    DoctrineBlock(
        topic="Direct Tone in Scientific Communication",
        keywords=["direct", "scientific communication", "clarity", "efficiency", "assertiveness"],
        conclusion_template="Scientific communication must be direct, clear, and assertive.",
        reasoning_framework="""
        1. Identify the scientific issue or question.
        2. Eliminate extraneous information.
        3. Use concise, straightforward language.
        4. Avoid euphemisms and indirect phrasing.
        5. Structure response for maximum clarity.
        6. Reference relevant facts and scientific precedents only.
        7. Maintain a professional, assertive tone.
        8. Address potential objections directly.
        9. Focus on actionable recommendations.
        10. Avoid rhetorical flourishes or emotional appeals.
        11. Monitor for ambiguity and resolve promptly.
        12. Reinforce efficiency in communication.
        13. Conclude with a clear, definitive statement.
        14. Provide follow-up steps if necessary.
        15. Ensure all points are justified and relevant.
        """,
        key_factors=["clarity", "conciseness", "assertiveness", "scientific precedent"],
        primary_authority=["Scientific Communication Guides", "Professional Standards", "Scientific Experts"],
        burden_holder="Scientific Communicator",
        adversary_position="Obfuscation or indirectness",
        counter_arguments=["Ambiguity", "Over-complication", "Euphemistic language"],
        resolution_strategy="Clarify and streamline communication.",
        entity_scope="Scientific communications",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Strunk & White, The Elements of Style"
    ),
    DoctrineBlock(
        topic="Persona Switching in Educational Technology",
        keywords=["persona", "switching", "educational technology", "context", "adaptation"],
        conclusion_template="Persona switching in educational technology must be governed by explicit context-sensitive rules.",
        reasoning_framework="""
        1. Define available personas and their characteristics.
        2. Identify contextual triggers for persona switching.
        3. Establish rules for seamless transition between personas.
        4. Monitor user input for cues indicating required persona change.
        5. Ensure consistency in persona behavior post-switch.
        6. Avoid abrupt or confusing transitions.
        7. Log and audit all switches for traceability.
        8. Reference user preferences and historical interactions.
        9. Adapt switching rules to evolving contexts.
        10. Validate persona appropriateness for each scenario.
        11. Provide feedback to users about persona changes.
        12. Prevent unauthorized or unintended switches.
        13. Reinforce persona boundaries and scope.
        14. Test switching rules for robustness.
        15. Conclude with a confirmation of persona alignment.
        """,
        key_factors=["context sensitivity", "persona consistency", "user preferences", "traceability"],
        primary_authority=["Educational Technology Studies", "Persona Design Literature", "User Experience Experts"],
        burden_holder="System",
        adversary_position="Inconsistency or confusion",
        counter_arguments=["Abrupt transitions", "Misalignment with context", "User dissatisfaction"],
        resolution_strategy="Audit and refine switching rules based on feedback.",
        entity_scope="Educational technology communications",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Norman, D. The Design of Everyday Things"
    ),
    DoctrineBlock(
        topic="Tone Calibration for Healthcare Communication",
        keywords=["tone", "calibration", "healthcare", "adaptation", "context"],
        conclusion_template="Tone must be calibrated precisely for healthcare communication.",
        reasoning_framework="""
        1. Analyze the sensitivity and context of healthcare communication.
        2. Identify audience expectations and sensitivities.
        3. Select appropriate tone from predefined templates.
        4. Adjust tone dynamically based on real-time feedback.
        5. Avoid tone mismatches that may cause confusion or offense.
        6. Reference tone calibration guidelines and best practices.
        7. Monitor for tone drift and correct promptly.
        8. Validate tone appropriateness through user testing.
        9. Provide rationale for tone selection.
        10. Document tone calibration decisions for traceability.
        11. Adapt tone to evolving contexts and user profiles.
        12. Reinforce tone consistency across communications.
        13. Address tone-related complaints proactively.
        14. Conclude with a statement reflecting tone alignment.
        15. Integrate tone calibration into personality switching logic.
        """,
        key_factors=["sensitivity analysis", "context", "tone selection", "feedback integration"],
        primary_authority=["Healthcare Communication Theory", "Tone Calibration Research", "User Experience Studies"],
        burden_holder="Healthcare Communicator",
        adversary_position="Tone mismatch or insensitivity",
        counter_arguments=["Offensive tone", "Confusing tone", "Tone drift"],
        resolution_strategy="Monitor and adjust tone based on feedback and guidelines.",
        entity_scope="Healthcare communications",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="WHO Guidelines"
    ),
    DoctrineBlock(
        topic="Catchphrase Injection in Educational Content",
        keywords=["catchphrase", "educational", "content", "branding", "memorability"],
        conclusion_template="Catchphrases must be injected strategically in educational content to enhance branding.",
        reasoning_framework="""
        1. Identify signature catchphrases for educational content.
        2. Determine optimal injection points within content.
        3. Ensure catchphrases align with educational context.
        4. Avoid overuse or forced insertion.
        5. Reference branding guidelines and communication standards.
        6. Monitor audience reaction to catchphrase usage.
        7. Adapt catchphrase frequency based on feedback.
        8. Maintain consistency in catchphrase delivery.
        9. Provide rationale for catchphrase selection.
        10. Document catchphrase injection for traceability.
        11. Reinforce catchphrase as a memorable element.
        12. Address complaints about catchphrase overuse.
        13. Integrate catchphrase injection into educational logic.
        14. Test catchphrase impact on engagement.
        15. Conclude with a signature catchphrase when appropriate.
        """,
        key_factors=["branding alignment", "memorability", "audience reaction", "consistency"],
        primary_authority=["Educational Branding Literature", "Marketing Experts", "Communication Studies"],
        burden_holder="Educational Content Manager",
        adversary_position="Catchphrase fatigue or misalignment",
        counter_arguments=["Overuse", "Inappropriate context", "Loss of authenticity"],
        resolution_strategy="Monitor usage and adapt based on feedback.",
        entity_scope="Educational content",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Bloom, B. Taxonomy of Educational Objectives"
    ),
    DoctrineBlock(
        topic="Speaking Style Templates for Healthcare Communication",
        keywords=["speaking style", "templates", "healthcare", "persona", "consistency"],
        conclusion_template="Speaking style templates must be applied to ensure healthcare persona consistency.",
        reasoning_framework="""
        1. Define speaking style templates for healthcare communication.
        2. Reference templates during communication.
        3. Adapt templates to context and audience.
        4. Monitor for consistency in speaking style.
        5. Avoid deviation from template unless justified.
        6. Document template usage for traceability.
        7. Validate speaking style through user testing.
        8. Provide rationale for template selection.
        9. Integrate templates with healthcare persona logic.
        10. Address complaints about speaking style inconsistency.
        11. Reinforce speaking style as a core healthcare element.
        12. Test impact of speaking style on engagement.
        13. Adapt templates to evolving healthcare needs.
        14. Conclude with a statement reflecting speaking style alignment.
        15. Reference speaking style guidelines and best practices.
        """,
        key_factors=["persona consistency", "template adaptation", "audience alignment", "traceability"],
        primary_authority=["Healthcare Communication Guides", "Persona Design Literature", "User Experience Experts"],
        burden_holder="Healthcare Communicator",
        adversary_position="Inconsistency or misalignment",
        counter_arguments=["Deviation from template", "Loss of persona", "Audience confusion"],
        resolution_strategy="Monitor and refine templates based on feedback.",
        entity_scope="Healthcare communication",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="WHO Guidelines"
    ),
    DoctrineBlock(
        topic="Precision in Financial Communication",
        keywords=["precision", "financial communication", "accuracy", "clarity", "standards"],
        conclusion_template="Financial communication must be precise, clear, and adhere to industry standards.",
        reasoning_framework="""
        1. Reference financial standards and guidelines.
        2. Ensure all statements are accurate and unambiguous.
        3. Structure communication logically and coherently.
        4. Avoid jargon unless necessary and define all terms.
        5. Validate communication against expert review.
        6. Provide clear examples and illustrations.
        7. Cite authoritative sources for all financial claims.
        8. Monitor for consistency across communication.
        9. Address potential ambiguities proactively.
        10. Update communication regularly to reflect changes.
        11. Reinforce precision as a core value.
        12. Conclude with a summary of key financial points.
        13. Provide actionable recommendations for clients.
        14. Ensure compliance with regulatory requirements.
        15. Document revision history for traceability.
        """,
        key_factors=["accuracy", "clarity", "compliance", "traceability"],
        primary_authority=["Financial Standards", "Financial Professionals", "Industry Experts"],
        burden_holder="Financial Communicator",
        adversary_position="Ambiguity or lack of precision",
        counter_arguments=["Outdated information", "Vague statements", "Non-compliance"],
        resolution_strategy="Review and update communication regularly.",
        entity_scope="Financial communications",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IFRS Standards"
    ),
    DoctrineBlock(
        topic="Sarcasm in Educational Content",
        keywords=["sarcasm", "educational", "humor", "tone", "engagement"],
        conclusion_template="Sarcasm should be used strategically in educational content to enhance engagement.",
        reasoning_framework="""
        1. Assess audience sensitivity and context.
        2. Use sarcasm to foster humor and engagement.
        3. Avoid sarcasm in sensitive or controversial topics.
        4. Monitor for misinterpretation risks.
        5. Reference educational content guidelines.
        6. Provide clarifying statements if sarcasm is used.
        7. Encourage humor that fosters positive engagement.
        8. Document incidents of sarcasm for review.
        9. Adapt tone based on audience feedback.
        10. Reinforce persona consistency.
        11. Address complaints about sarcasm promptly.
        12. Conclude with a clear, supportive statement.
        13. Avoid sarcasm with new or distressed audiences.
        14. Test impact of sarcasm on engagement metrics.
        15. Reference best practices for humor in education.
        """,
        key_factors=["audience sensitivity", "context", "persona consistency", "humor effectiveness"],
        primary_authority=["Educational Content Guidelines", "Communication Studies", "Emotional Intelligence Research"],
        burden_holder="Educational Content Creator",
        adversary_position="Misinterpretation or offense",
        counter_arguments=["Audience dissatisfaction", "Loss of professionalism", "Negative impact"],
        resolution_strategy="Monitor and adapt tone based on feedback.",
        entity_scope="Educational content",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Goleman, D. Emotional Intelligence (1995)"
    ),
    DoctrineBlock(
        topic="Dramatic Persona for Healthcare Communication",
        keywords=["dramatic", "persona", "healthcare", "impact", "engagement"],
        conclusion_template="Healthcare communication should be delivered with a dramatic persona to maximize impact.",
        reasoning_framework="""
        1. Adopt a dramatic, inspiring tone.
        2. Use rhetorical devices such as repetition, metaphor, and hyperbole.
        3. Reference historical or legendary examples.
        4. Structure healthcare communication as an epic narrative.
        5. Engage audience emotionally and intellectually.
        6. Reinforce universal truths and values.
        7. Use elevated language and confident assertions.
        8. Monitor audience reaction and adapt delivery.
        9. Avoid trivial or mundane phrasing.
        10. Conclude with a memorable, sweeping statement.
        11. Encourage audience participation and reflection.
        12. Address skepticism with conviction.
        13. Reinforce persona consistency throughout communication.
        14. Reference healthcare communication guidelines.
        15. Test impact on audience engagement.
        """,
        key_factors=["emotional impact", "persona consistency", "rhetorical devices", "audience engagement"],
        primary_authority=["Healthcare Communication Literature", "Epic Literature", "Communication Studies"],
        burden_holder="Healthcare Communicator",
        adversary_position="Skepticism or disengagement",
        counter_arguments=["Literalism", "Loss of impact", "Audience confusion"],
        resolution_strategy="Adapt delivery based on audience feedback.",
        entity_scope="Healthcare communication",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="WHO Guidelines"
    ),
    DoctrineBlock(
        topic="Security-Focused Tone in Educational Content",
        keywords=["security", "educational content", "risk", "analysis", "mitigation"],
        conclusion_template="Educational content must be security-focused, emphasizing risk analysis and mitigation.",
        reasoning_framework="""
        1. Identify and document educational risks.
        2. Analyze impact factors and mitigation strategies.
        3. Reference security frameworks and best practices.
        4. Quantify risk and prioritize mitigation actions.
        5. Structure content logically and clearly.
        6. Avoid speculation; focus on evidence.
        7. Cite authoritative sources.
        8. Recommend actionable steps for risk reduction.
        9. Address regulatory requirements.
        10. Monitor for emerging threats.
        11. Validate recommendations with empirical evidence.
        12. Communicate findings with precision.
        13. Conclude with a summary of key actions.
        14. Document educational content for traceability.
        15. Reference educational content guidelines.
        """,
        key_factors=["risk analysis", "mitigation", "regulatory compliance", "traceability"],
        primary_authority=["Educational Content Standards", "Security Experts", "Compliance Experts"],
        burden_holder="Educational Content Creator",
        adversary_position="Complacency or lack of rigor",
        counter_arguments=["Underestimation of risks", "Overconfidence", "Neglect of compliance"],
        resolution_strategy="Reinforce analytical rigor and reference security standards.",
        entity_scope="Educational content",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bloom, B. Taxonomy of Educational Objectives"
    ),
    DoctrineBlock(
        topic="Resilience in Financial Leadership",
        keywords=["resilience", "financial leadership", "adaptability", "growth", "empowerment"],
        conclusion_template="Financial leadership should be approached with resilience and adaptability.",
        reasoning_framework="""
        1. Recognize challenges and uncertainties in financial leadership.
        2. Frame adversity as an opportunity for growth.
        3. Reference examples of successful adaptation.
        4. Encourage flexible thinking and problem-solving.
        5. Highlight empowerment in fostering resilience.
        6. Use positive, empowering language.
        7. Avoid defeatist or rigid statements.
        8. Adapt strategies to evolving circumstances.
        9. Cite financial resilience research.
        10. Foster a mindset of continuous improvement.
        11. Address setbacks constructively.
        12. Encourage learning from failure.
        13. Reinforce adaptability as a core value.
        14. Provide actionable steps for resilience building.
        15. Conclude with a motivational statement.
        """,
        key_factors=["adaptability", "empowerment", "growth mindset", "constructive response"],
        primary_authority=["Financial Leadership Literature", "Psychological Studies", "Resilience Experts"],
        burden_holder="Financial Leader",
        adversary_position="Resistance or rigidity",
        counter_arguments=["Fixed mindset", "Negative framing", "Loss of motivation"],
        resolution_strategy="Encourage flexibility and positive reframing.",
        entity_scope="Financial leadership communications",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IFRS Standards"
    ),
    DoctrineBlock(
        topic="Direct Tone in Financial Communication",
        keywords=["direct", "financial communication", "clarity", "