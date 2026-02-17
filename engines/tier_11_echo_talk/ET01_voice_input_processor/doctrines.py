from dataclasses import dataclass, field
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
        topic="Voice Input Classification Rules",
        keywords=["voice input", "classification", "input type", "audio analysis"],
        conclusion_template="Classify incoming voice input as command, query, or chit-chat based on linguistic and acoustic features.",
        reasoning_framework="""
        1. Extract linguistic features from the transcribed text.
        2. Analyze prosodic and paralinguistic cues from the audio signal.
        3. Apply a multi-layer classifier trained on labeled datasets to distinguish between commands, queries, and casual conversation.
        4. Use context from previous turns to disambiguate ambiguous utterances.
        5. Default to 'query' if classification confidence is below threshold.
        """,
        key_factors=[
            "Linguistic structure",
            "Prosodic features",
            "Contextual history",
            "Classifier confidence",
            "Ambiguity resolution"
        ],
        primary_authority=[
            "ISO/IEC 30122-1:2015",
            "ETSI ES 202 076",
            "ET01_engine.py"
        ],
        burden_holder="System",
        adversary_position="All voice input should be treated uniformly without classification.",
        counter_arguments=[
            "Uniform treatment reduces accuracy.",
            "Classification enables tailored downstream processing.",
            "Ambiguity can be resolved with context."
        ],
        resolution_strategy="Apply classifier with fallback to default; log low-confidence cases for review.",
        entity_scope="All voice input processors in ET01",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ET01-2022-VoiceClass-01"
    ),
    DoctrineBlock(
        topic="STT Output Normalization",
        keywords=["speech-to-text", "normalization", "text processing", "output cleaning"],
        conclusion_template="Normalize STT output to standard orthography, punctuation, and casing before downstream processing.",
        reasoning_framework="""
        1. Remove extraneous whitespace and non-speech artifacts.
        2. Restore punctuation using a trained model or rule-based system.
        3. Apply language-specific casing rules.
        4. Normalize numerals, dates, and common abbreviations.
        5. Ensure output conforms to UTF-8 encoding and system standards.
        """,
        key_factors=[
            "Punctuation restoration",
            "Casing normalization",
            "Numeral and date formatting",
            "Language-specific conventions"
        ],
        primary_authority=[
            "Whisper STT Documentation",
            "ISO/IEC 30122-2:2017",
            "ET01_engine.py"
        ],
        burden_holder="STT Integration Layer",
        adversary_position="Raw STT output should be used for maximum fidelity.",
        counter_arguments=[
            "Raw output impairs downstream NLP accuracy.",
            "Normalization improves user experience.",
            "Standardization is required for multi-language support."
        ],
        resolution_strategy="Normalize all STT output with language-aware pipelines.",
        entity_scope="STT output handlers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET01-2021-STTNorm-03"
    ),
    DoctrineBlock(
        topic="Conversation Mode Selection",
        keywords=["conversation mode", "mode selection", "dialogue management", "context"],
        conclusion_template="Select conversation mode (deterministic, hybrid, LLM) based on input intent, context, and system state.",
        reasoning_framework="""
        1. Analyze input intent using intent classifier.
        2. Check for active deterministic triggers or ongoing tasks.
        3. Evaluate context for multi-turn continuity.
        4. If input is ambiguous, prefer hybrid mode for fallback.
        5. Escalate to LLM mode for open-ended or unhandled queries.
        """,
        key_factors=[
            "Input intent",
            "Active triggers",
            "Multi-turn context",
            "System state"
        ],
        primary_authority=[
            "ET01_engine.py",
            "ISO/IEC 30122-3:2018"
        ],
        burden_holder="Dialogue Manager",
        adversary_position="Always use a single conversation mode for simplicity.",
        counter_arguments=[
            "Single mode reduces flexibility.",
            "Mode selection optimizes accuracy and resource usage.",
            "Hybrid mode provides robust fallback."
        ],
        resolution_strategy="Implement mode selection policy with override for admin commands.",
        entity_scope="Dialogue management subsystem",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET01-2022-ConvMode-02"
    ),
    DoctrineBlock(
        topic="Deterministic Mode Triggers",
        keywords=["deterministic mode", "trigger", "rule-based", "activation"],
        conclusion_template="Activate deterministic mode when input matches predefined command patterns or critical system tasks.",
        reasoning_framework="""
        1. Maintain a registry of deterministic command patterns.
        2. On input, perform pattern matching against registry.
        3. Prioritize deterministic mode for system-critical or safety-related commands.
        4. Log all deterministic activations for audit.
        5. Fallback to hybrid mode if pattern match confidence is low.
        """,
        key_factors=[
            "Pattern registry",
            "Critical command identification",
            "Pattern match confidence"
        ],
        primary_authority=[
            "ET01_engine.py",
            "ETSI ES 202 076"
        ],
        burden_holder="Command Handler",
        adversary_position="Pattern matching is too rigid for natural language.",
        counter_arguments=[
            "Deterministic mode ensures safety and reliability.",
            "Pattern registry can be updated for coverage.",
            "Hybrid fallback mitigates rigidity."
        ],
        resolution_strategy="Update registry regularly; monitor for false negatives.",
        entity_scope="Command processing pipeline",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-DetMode-01"
    ),
    DoctrineBlock(
        topic="Hybrid Mode Triggers",
        keywords=["hybrid mode", "trigger", "fallback", "uncertainty"],
        conclusion_template="Engage hybrid mode when input is ambiguous or classifier confidence is below threshold.",
        reasoning_framework="""
        1. Monitor classifier confidence score for each input.
        2. If confidence < 0.8, route input to both deterministic and LLM subsystems.
        3. Aggregate responses, preferring deterministic output if available.
        4. Log hybrid activations for analysis.
        5. Tune threshold based on empirical data.
        """,
        key_factors=[
            "Classifier confidence",
            "Ambiguity detection",
            "Response aggregation"
        ],
        primary_authority=[
            "ET01_engine.py",
            "ISO/IEC 30122-3:2018"
        ],
        burden_holder="Dialogue Manager",
        adversary_position="Hybrid mode increases latency and complexity.",
        counter_arguments=[
            "Hybrid mode improves robustness.",
            "Latency tradeoff is justified for ambiguous cases.",
            "Empirical tuning reduces unnecessary activations."
        ],
        resolution_strategy="Monitor latency; optimize aggregation logic.",
        entity_scope="Dialogue management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-HybridMode-01"
    ),
    DoctrineBlock(
        topic="LLM Mode Triggers",
        keywords=["LLM mode", "trigger", "large language model", "open-ended"],
        conclusion_template="Invoke LLM mode for open-ended queries, creative tasks, or when deterministic/hybrid modes fail.",
        reasoning_framework="""
        1. Detect open-ended or creative intent using intent classifier.
        2. If deterministic and hybrid modes return 'no match', escalate to LLM.
        3. Monitor resource usage and apply rate limiting as needed.
        4. Log LLM activations for review.
        5. Provide user feedback on mode escalation.
        """,
        key_factors=[
            "Intent classification",
            "Fallback escalation",
            "Resource management"
        ],
        primary_authority=[
            "ET01_engine.py",
            "OpenAI LLM Integration Guide"
        ],
        burden_holder="Dialogue Manager",
        adversary_position="LLM mode is resource-intensive and should be avoided.",
        counter_arguments=[
            "LLM mode is necessary for unhandled queries.",
            "Escalation is controlled and logged.",
            "Rate limiting prevents abuse."
        ],
        resolution_strategy="Escalate only after deterministic/hybrid failure; monitor usage.",
        entity_scope="Dialogue management",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ET01-2022-LLMMode-01"
    ),
    DoctrineBlock(
        topic="Input Intent Classification",
        keywords=["intent classification", "input analysis", "NLP", "intent detection"],
        conclusion_template="Classify input intent using supervised models trained on domain-specific utterances.",
        reasoning_framework="""
        1. Preprocess input text for normalization.
        2. Extract features using NLP pipelines (tokenization, embeddings).
        3. Apply supervised intent classifier (e.g., SVM, neural net).
        4. Use domain-specific training data for accuracy.
        5. Update models regularly with new labeled data.
        """,
        key_factors=[
            "Model accuracy",
            "Domain adaptation",
            "Feature extraction"
        ],
        primary_authority=[
            "ET01_engine.py",
            "ISO/IEC 30122-4:2019"
        ],
        burden_holder="NLP Subsystem",
        adversary_position="Intent classification is unnecessary; use keyword matching.",
        counter_arguments=[
            "Keyword matching is brittle.",
            "Supervised models adapt to natural language.",
            "Regular updates maintain accuracy."
        ],
        resolution_strategy="Deploy supervised models; monitor for drift.",
        entity_scope="NLP pipeline",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET01-2022-IntentClass-01"
    ),
    DoctrineBlock(
        topic="Command vs Query Detection",
        keywords=["command detection", "query detection", "input type", "speech acts"],
        conclusion_template="Distinguish commands from queries using syntactic and semantic analysis.",
        reasoning_framework="""
        1. Parse input for imperative vs interrogative structures.
        2. Analyze verb tense and modality.
        3. Use semantic role labeling to identify action requests.
        4. Apply context from previous turns.
        5. Default to query if ambiguous.
        """,
        key_factors=[
            "Syntactic parsing",
            "Semantic analysis",
            "Contextual cues"
        ],
        primary_authority=[
            "ET01_engine.py",
            "ISO/IEC 30122-3:2018"
        ],
        burden_holder="NLP Subsystem",
        adversary_position="Distinction is unnecessary; treat all as queries.",
        counter_arguments=[
            "Commands require different handling.",
            "Semantic analysis improves accuracy.",
            "Context resolves ambiguity."
        ],
        resolution_strategy="Implement dual-path processing for commands and queries.",
        entity_scope="NLP pipeline",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET01-2022-CmdQuery-01"
    ),
    DoctrineBlock(
        topic="Voice Activity Detection (VAD)",
        keywords=["VAD", "voice activity detection", "audio segmentation", "speech boundary"],
        conclusion_template="Apply VAD to segment speech from silence and background noise before STT processing.",
        reasoning_framework="""
        1. Analyze audio signal for energy, zero-crossing rate, and spectral features.
        2. Use a VAD model (e.g., WebRTC VAD) to mark speech segments.
        3. Discard non-speech frames to reduce STT load.
        4. Tune VAD sensitivity for environment.
        5. Log VAD errors for analysis.
        """,
        key_factors=[
            "Energy threshold",
            "Spectral analysis",
            "Model selection"
        ],
        primary_authority=[
            "WebRTC VAD",
            "ET01_engine.py"
        ],
        burden_holder="Audio Preprocessing Layer",
        adversary_position="VAD may cut off low-volume speech.",
        counter_arguments=[
            "Tuning mitigates cutoff risk.",
            "VAD reduces false positives.",
            "Manual override is available."
        ],
        resolution_strategy="Tune VAD per deployment; monitor for missed speech.",
        entity_scope="Audio preprocessing",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-VAD-01"
    ),
    DoctrineBlock(
        topic="Wakeword Handling",
        keywords=["wakeword", "activation", "hotword", "wake word detection"],
        conclusion_template="Detect and verify wakeword before activating processing pipeline.",
        reasoning_framework="""
        1. Use a wakeword detection model trained on target vocabulary.
        2. Require minimum confidence threshold for activation.
        3. Implement anti-spoofing measures (e.g., speaker verification).
        4. Log all wakeword detections.
        5. Allow user customization of wakeword.
        """,
        key_factors=[
            "Wakeword model accuracy",
            "Confidence threshold",
            "Anti-spoofing"
        ],
        primary_authority=[
            "Porcupine Wakeword Engine",
            "ET01_engine.py"
        ],
        burden_holder="Wakeword Detector",
        adversary_position="Wakeword detection adds latency.",
        counter_arguments=[
            "Wakeword is essential for privacy.",
            "Model optimization reduces latency.",
            "User customization increases acceptance."
        ],
        resolution_strategy="Optimize model; support user configuration.",
        entity_scope="Wakeword subsystem",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Wakeword-01"
    ),
    DoctrineBlock(
        topic="Multi-Turn Context Tracking",
        keywords=["multi-turn", "context tracking", "dialogue history", "conversation memory"],
        conclusion_template="Maintain context across multiple turns to support coherent conversations.",
        reasoning_framework="""
        1. Store dialogue history in a context buffer.
        2. Update buffer with each new turn.
        3. Use context for reference resolution and intent disambiguation.
        4. Limit buffer size to recent N turns for efficiency.
        5. Expire context on session end or explicit user command.
        """,
        key_factors=[
            "Context buffer size",
            "Reference resolution",
            "Session management"
        ],
        primary_authority=[
            "ET01_engine.py",
            "ISO/IEC 30122-3:2018"
        ],
        burden_holder="Dialogue Manager",
        adversary_position="Context tracking increases memory usage.",
        counter_arguments=[
            "Buffer size is configurable.",
            "Context is essential for natural dialogue.",
            "Session expiry prevents bloat."
        ],
        resolution_strategy="Tune buffer size; clear on session end.",
        entity_scope="Dialogue management",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-MultiTurn-01"
    ),
    DoctrineBlock(
        topic="Language Detection",
        keywords=["language detection", "multi-language", "input language", "language ID"],
        conclusion_template="Detect input language before STT and NLP processing to select appropriate models.",
        reasoning_framework="""
        1. Analyze audio and/or text for language-specific features.
        2. Use a language identification model (e.g., fastText, langid.py).
        3. Route input to language-specific STT and NLP pipelines.
        4. Log language detection errors.
        5. Allow user override of detected language.
        """,
        key_factors=[
            "Language ID model accuracy",
            "Audio/text analysis",
            "Pipeline routing"
        ],
        primary_authority=[
            "fastText Language ID",
            "ET01_engine.py"
        ],
        burden_holder="Preprocessing Layer",
        adversary_position="Language detection adds processing overhead.",
        counter_arguments=[
            "Overhead is minimal with optimized models.",
            "Correct language selection is critical.",
            "User override handles edge cases."
        ],
        resolution_strategy="Optimize detection; support user override.",
        entity_scope="Preprocessing pipeline",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET01-2022-LangDetect-01"
    ),
    DoctrineBlock(
        topic="Profanity Filtering",
        keywords=["profanity", "filtering", "content moderation", "offensive language"],
        conclusion_template="Filter profanity from input and output to maintain user safety and compliance.",
        reasoning_framework="""
        1. Maintain a profanity lexicon for all supported languages.
        2. Apply filtering to both STT output and system responses.
        3. Allow user to configure strictness level.
        4. Log filtered events for compliance.
        5. Update lexicon regularly.
        """,
        key_factors=[
            "Lexicon coverage",
            "Multi-language support",
            "User configuration"
        ],
        primary_authority=[
            "ISO/IEC 30122-5:2020",
            "ET01_engine.py"
        ],
        burden_holder="Content Moderation Subsystem",
        adversary_position="Profanity filtering may over-censor harmless speech.",
        counter_arguments=[
            "Strictness is user-configurable.",
            "Compliance requires filtering.",
            "Lexicon updates reduce false positives."
        ],
        resolution_strategy="Allow user tuning; review logs for over-censorship.",
        entity_scope="Content moderation",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Profanity-01"
    ),
    DoctrineBlock(
        topic="Input Length Validation",
        keywords=["input length", "validation", "input constraints", "buffer overflow"],
        conclusion_template="Validate input length to prevent buffer overflows and ensure system stability.",
        reasoning_framework="""
        1. Set maximum input length for both audio and text.
        2. Reject or truncate inputs exceeding limits.
        3. Log validation failures.
        4. Notify user of truncation or rejection.
        5. Adjust limits based on hardware capacity.
        """,
        key_factors=[
            "Max input length",
            "System capacity",
            "User notification"
        ],
        primary_authority=[
            "ET01_engine.py",
            "CWE-120"
        ],
        burden_holder="Input Validator",
        adversary_position="Strict limits may frustrate users.",
        counter_arguments=[
            "Limits prevent system crashes.",
            "User notification mitigates frustration.",
            "Limits are configurable."
        ],
        resolution_strategy="Set reasonable defaults; allow admin override.",
        entity_scope="Input validation",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-InputLen-01"
    ),
    DoctrineBlock(
        topic="Urgency Detection",
        keywords=["urgency detection", "priority", "emergency", "input analysis"],
        conclusion_template="Detect urgent or emergency inputs and escalate processing priority.",
        reasoning_framework="""
        1. Analyze input for urgency markers (e.g., 'help', 'emergency').
        2. Use supervised urgency classifier.
        3. Escalate urgent inputs to high-priority processing queue.
        4. Log all urgent detections.
        5. Notify user of escalation.
        """,
        key_factors=[
            "Urgency markers",
            "Classifier accuracy",
            "Priority escalation"
        ],
        primary_authority=[
            "ET01_engine.py",
            "ISO/IEC 30122-3:2018"
        ],
        burden_holder="Input Analysis Layer",
        adversary_position="Urgency detection may generate false positives.",
        counter_arguments=[
            "Classifier is tuned for precision.",
            "Escalation is logged for review.",
            "User notification allows correction."
        ],
        resolution_strategy="Tune classifier; monitor for false positives.",
        entity_scope="Input analysis",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Urgency-01"
    ),
    DoctrineBlock(
        topic="PII Detection in Voice",
        keywords=["PII", "personal data", "privacy", "voice input"],
        conclusion_template="Detect and redact PII in voice input to ensure privacy compliance.",
        reasoning_framework="""
        1. Transcribe audio to text.
        2. Apply PII detection models to identify names, addresses, numbers, etc.
        3. Redact or mask detected PII in logs and outputs.
        4. Log PII detection events for compliance.
        5. Allow user to request data deletion.
        """,
        key_factors=[
            "PII detection accuracy",
            "Redaction mechanism",
            "Compliance logging"
        ],
        primary_authority=[
            "GDPR",
            "ISO/IEC 27001",
            "ET01_engine.py"
        ],
        burden_holder="Privacy Layer",
        adversary_position="PII detection may over-mask benign data.",
        counter_arguments=[
            "Models are tuned for precision.",
            "User can request review.",
            "Compliance requires conservative approach."
        ],
        resolution_strategy="Tune models; support user review.",
        entity_scope="Privacy and compliance",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET01-2022-PII-01"
    ),
    DoctrineBlock(
        topic="Whisper STT Integration",
        keywords=["Whisper", "STT", "speech-to-text", "integration"],
        conclusion_template="Integrate Whisper STT for high-accuracy transcription across supported languages.",
        reasoning_framework="""
        1. Route audio input to Whisper STT engine.
        2. Configure model size and language options per deployment.
        3. Monitor transcription latency and accuracy.
        4. Log STT errors and performance metrics.
        5. Update Whisper version as needed.
        """,
        key_factors=[
            "Model configuration",
            "Latency",
            "Accuracy"
        ],
        primary_authority=[
            "Whisper STT Documentation",
            "ET01_engine.py"
        ],
        burden_holder="STT Integration Layer",
        adversary_position="Whisper may be resource-intensive.",
        counter_arguments=[
            "Model size is configurable.",
            "Accuracy justifies resource use.",
            "Monitor and optimize deployment."
        ],
        resolution_strategy="Tune model parameters; monitor resource usage.",
        entity_scope="STT subsystem",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Whisper-01"
    ),
    DoctrineBlock(
        topic="Noise Handling",
        keywords=["noise", "audio quality", "denoising", "background noise"],
        conclusion_template="Apply noise suppression and filtering to improve STT accuracy.",
        reasoning_framework="""
        1. Analyze input audio for noise profile.
        2. Apply denoising algorithms (e.g., spectral subtraction, RNNoise).
        3. Monitor SNR (signal-to-noise ratio) and log poor quality inputs.
        4. Allow user to adjust sensitivity.
        5. Fallback to manual review for persistent noise issues.
        """,
        key_factors=[
            "Noise profile analysis",
            "Denoising algorithm",
            "SNR monitoring"
        ],
        primary_authority=[
            "RNNoise",
            "ET01_engine.py"
        ],
        burden_holder="Audio Preprocessing Layer",
        adversary_position="Denoising may distort speech.",
        counter_arguments=[
            "Algorithms are tuned for minimal distortion.",
            "User can adjust sensitivity.",
            "Manual review is available."
        ],
        resolution_strategy="Tune denoising; monitor for artifacts.",
        entity_scope="Audio preprocessing",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Noise-01"
    ),
    DoctrineBlock(
        topic="Multi-Speaker Diarization",
        keywords=["diarization", "multi-speaker", "speaker separation", "audio analysis"],
        conclusion_template="Apply speaker diarization to segment and label speech by speaker in multi-party conversations.",
        reasoning_framework="""
        1. Extract speaker embeddings from audio.
        2. Cluster embeddings to identify unique speakers.
        3. Label each segment with speaker ID.
        4. Use diarization results to improve context tracking.
        5. Log diarization errors for review.
        """,
        key_factors=[
            "Speaker embedding accuracy",
            "Clustering algorithm",
            "Segment labeling"
        ],
        primary_authority=[
            "pyAudioAnalysis",
            "ET01_engine.py"
        ],
        burden_holder="Audio Analysis Layer",
        adversary_position="Diarization adds processing overhead.",
        counter_arguments=[
            "Overhead is justified for multi-party conversations.",
            "Improves context and accuracy.",
            "Can be disabled for single-speaker use cases."
        ],
        resolution_strategy="Enable diarization for multi-party; monitor performance.",
        entity_scope="Audio analysis",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Diarization-01"
    ),
    DoctrineBlock(
        topic="Input Confidence Scoring",
        keywords=["confidence scoring", "input quality", "classifier confidence", "threshold"],
        conclusion_template="Score input confidence and use thresholds to guide processing decisions.",
        reasoning_framework="""
        1. Assign confidence score to each input using classifier output.
        2. Set thresholds for routing to deterministic, hybrid, or LLM modes.
        3. Log low-confidence cases for review.
        4. Allow admin to adjust thresholds.
        5. Use confidence for user feedback.
        """,
        key_factors=[
            "Classifier output",
            "Threshold tuning",
            "Logging"
        ],
        primary_authority=[
            "ET01_engine.py",
            "ISO/IEC 30122-3:2018"
        ],
        burden_holder="Dialogue Manager",
        adversary_position="Confidence scoring adds complexity.",
        counter_arguments=[
            "Thresholds improve accuracy.",
            "Logging enables tuning.",
            "User feedback increases transparency."
        ],
        resolution_strategy="Tune thresholds; monitor logs.",
        entity_scope="Dialogue management",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Confidence-01"
    ),
    DoctrineBlock(
        topic="No Doctrine Match",
        keywords=["fallback", "no match", "default handling", "unhandled input"],
        conclusion_template="Apply default fallback handling for inputs not matching any doctrine.",
        reasoning_framework="""
        1. Detect when input does not match any specific doctrine.
        2. Route to default fallback handler.
        3. Log all no-match cases for analysis.
        4. Notify user of fallback.
        5. Review logs to identify gaps in doctrine coverage.
        """,
        key_factors=[
            "Fallback handler",
            "Logging",
            "Coverage analysis"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System",
        adversary_position="Unhandled inputs should be dropped.",
        counter_arguments=[
            "Fallback improves user experience.",
            "Logging identifies coverage gaps.",
            "Dropping inputs loses data."
        ],
        resolution_strategy="Implement robust fallback; review logs regularly.",
        entity_scope="System-wide",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="ET01-2022-NoMatch-01"
    ),
    # Additional doctrines for coverage
    DoctrineBlock(
        topic="Accent Robustness",
        keywords=["accent", "robustness", "speech recognition", "variation"],
        conclusion_template="Ensure STT and intent models are robust to common accent variations.",
        reasoning_framework="""
        1. Train models on diverse accent datasets.
        2. Evaluate performance on accented speech.
        3. Tune models to reduce bias toward standard accents.
        4. Log accent-related errors.
        5. Allow user feedback to improve coverage.
        """,
        key_factors=[
            "Accent dataset coverage",
            "Model tuning",
            "Error logging"
        ],
        primary_authority=[
            "Mozilla Common Voice",
            "ET01_engine.py"
        ],
        burden_holder="Model Trainer",
        adversary_position="Accent handling increases model size.",
        counter_arguments=[
            "Diversity improves accessibility.",
            "Model pruning mitigates size increase.",
            "User feedback guides tuning."
        ],
        resolution_strategy="Balance size and coverage; prioritize accessibility.",
        entity_scope="STT and NLP models",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Accent-01"
    ),
    DoctrineBlock(
        topic="Custom Vocabulary Injection",
        keywords=["custom vocabulary", "user dictionary", "STT", "domain terms"],
        conclusion_template="Allow injection of custom vocabulary to improve recognition of domain-specific terms.",
        reasoning_framework="""
        1. Provide API for user or admin to add custom terms.
        2. Update STT and NLP models with new vocabulary.
        3. Validate and sanitize custom entries.
        4. Log vocabulary injections.
        5. Allow rollback of problematic terms.
        """,
        key_factors=[
            "API design",
            "Model update mechanism",
            "Validation"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System Admin",
        adversary_position="Custom vocabulary may introduce errors.",
        counter_arguments=[
            "Validation prevents errors.",
            "Improves domain accuracy.",
            "Rollback is supported."
        ],
        resolution_strategy="Validate all entries; monitor impact.",
        entity_scope="STT and NLP pipeline",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ET01-2022-CustomVocab-01"
    ),
    DoctrineBlock(
        topic="Session Timeout Handling",
        keywords=["session timeout", "session management", "user inactivity", "dialogue"],
        conclusion_template="Expire session context after configurable period of user inactivity.",
        reasoning_framework="""
        1. Track last user activity timestamp.
        2. If inactivity exceeds threshold, clear session context.
        3. Notify user of session expiry.
        4. Allow admin to configure timeout period.
        5. Log all session expiries.
        """,
        key_factors=[
            "Timeout threshold",
            "Session context management",
            "User notification"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Session Manager",
        adversary_position="Timeouts may disrupt ongoing conversations.",
        counter_arguments=[
            "Timeout is configurable.",
            "Prevents context bloat.",
            "User is notified."
        ],
        resolution_strategy="Set reasonable defaults; allow user override.",
        entity_scope="Session management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-SessionTimeout-01"
    ),
    DoctrineBlock(
        topic="User Personalization",
        keywords=["personalization", "user profile", "customization", "preferences"],
        conclusion_template="Support user personalization for language, wakeword, and response style.",
        reasoning_framework="""
        1. Store user preferences in secure profile.
        2. Apply preferences to language, wakeword, and system responses.
        3. Allow user to update preferences at any time.
        4. Log preference changes.
        5. Respect privacy and data retention policies.
        """,
        key_factors=[
            "Preference storage",
            "Privacy compliance",
            "Customization options"
        ],
        primary_authority=[
            "GDPR",
            "ET01_engine.py"
        ],
        burden_holder="User Profile Manager",
        adversary_position="Personalization increases complexity.",
        counter_arguments=[
            "Improves user experience.",
            "Privacy is maintained.",
            "Options are user-driven."
        ],
        resolution_strategy="Modularize personalization; enforce privacy.",
        entity_scope="User profile subsystem",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Personalization-01"
    ),
    DoctrineBlock(
        topic="Input Language Switching",
        keywords=["language switching", "multi-language", "user command", "input language"],
        conclusion_template="Allow user to switch input language via explicit command.",
        reasoning_framework="""
        1. Detect language switch commands in input.
        2. Update session language context.
        3. Route subsequent inputs to new language pipeline.
        4. Notify user of switch.
        5. Log all language switches.
        """,
        key_factors=[
            "Command detection",
            "Session context update",
            "User notification"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Dialogue Manager",
        adversary_position="Frequent switching may confuse the system.",
        counter_arguments=[
            "Session context prevents confusion.",
            "User is notified of changes.",
            "Logs enable troubleshooting."
        ],
        resolution_strategy="Enforce clear switch commands; monitor logs.",
        entity_scope="Dialogue management",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-LangSwitch-01"
    ),
    DoctrineBlock(
        topic="Audio Format Validation",
        keywords=["audio format", "validation", "input constraints", "compatibility"],
        conclusion_template="Validate audio format before processing to ensure compatibility.",
        reasoning_framework="""
        1. Check input audio for supported format (e.g., WAV, 16kHz, mono).
        2. Reject or convert unsupported formats.
        3. Log validation failures.
        4. Notify user of format issues.
        5. Update supported formats as needed.
        """,
        key_factors=[
            "Format compatibility",
            "Conversion mechanism",
            "User notification"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Audio Input Handler",
        adversary_position="Strict format checking may exclude valid inputs.",
        counter_arguments=[
            "Conversion supports flexibility.",
            "Notifying user prevents confusion.",
            "Supported formats are updated regularly."
        ],
        resolution_strategy="Support conversion; update format list.",
        entity_scope="Audio input pipeline",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-AudioFormat-01"
    ),
    DoctrineBlock(
        topic="User Feedback Integration",
        keywords=["user feedback", "system improvement", "feedback loop", "user experience"],
        conclusion_template="Integrate user feedback to improve system accuracy and user satisfaction.",
        reasoning_framework="""
        1. Provide mechanism for users to submit feedback on recognition and responses.
        2. Log and categorize feedback.
        3. Use feedback to retrain models and update doctrines.
        4. Notify users of feedback impact where appropriate.
        5. Ensure feedback privacy.
        """,
        key_factors=[
            "Feedback mechanism",
            "Model retraining",
            "Privacy"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System Admin",
        adversary_position="Feedback integration adds overhead.",
        counter_arguments=[
            "Improves accuracy and satisfaction.",
            "Feedback is optional.",
            "Privacy is enforced."
        ],
        resolution_strategy="Automate feedback processing; monitor for abuse.",
        entity_scope="System-wide",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Feedback-01"
    ),
    DoctrineBlock(
        topic="Real-Time Processing Guarantee",
        keywords=["real-time", "latency", "processing guarantee", "performance"],
        conclusion_template="Guarantee real-time response for inputs within system-defined latency bounds.",
        reasoning_framework="""
        1. Set maximum processing latency for each pipeline stage.
        2. Monitor and log latency for all inputs.
        3. Prioritize real-time tasks in processing queue.
        4. Notify admin of latency violations.
        5. Optimize pipeline for low-latency operation.
        """,
        key_factors=[
            "Latency monitoring",
            "Queue prioritization",
            "Pipeline optimization"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System",
        adversary_position="Real-time guarantee may reduce accuracy.",
        counter_arguments=[
            "Balance latency and accuracy.",
            "Optimize for common cases.",
            "Notify admin for edge cases."
        ],
        resolution_strategy="Tune pipeline; monitor trade-offs.",
        entity_scope="System-wide",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="ET01-2022-RealTime-01"
    ),
    DoctrineBlock(
        topic="Admin Override Mechanism",
        keywords=["admin override", "manual control", "system override", "emergency"],
        conclusion_template="Allow admin to override doctrine-based decisions in critical situations.",
        reasoning_framework="""
        1. Provide secure interface for admin override.
        2. Log all override events with rationale.
        3. Notify users of override where applicable.
        4. Revert to doctrine-based processing after override expires.
        5. Review overrides for policy updates.
        """,
        key_factors=[
            "Override interface",
            "Logging",
            "Policy review"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System Admin",
        adversary_position="Manual overrides may cause inconsistency.",
        counter_arguments=[
            "Overrides are logged and reviewed.",
            "Critical for emergencies.",
            "Reversion ensures consistency."
        ],
        resolution_strategy="Restrict override access; review regularly.",
        entity_scope="System-wide",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-AdminOverride-01"
    ),
    DoctrineBlock(
        topic="Session Continuity Across Devices",
        keywords=["session continuity", "multi-device", "cross-device", "user experience"],
        conclusion_template="Support session continuity for users switching between devices.",
        reasoning_framework="""
        1. Store session context in a cloud-accessible profile.
        2. Sync context on device switch.
        3. Notify user of session transfer.
        4. Secure session data in transit and at rest.
        5. Expire context after inactivity or logout.
        """,
        key_factors=[
            "Cloud profile",
            "Session sync",
            "Security"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Session Manager",
        adversary_position="Cross-device sync increases privacy risk.",
        counter_arguments=[
            "Data is encrypted.",
            "User can opt out.",
            "Session expiry mitigates risk."
        ],
        resolution_strategy="Encrypt data; provide opt-out.",
        entity_scope="Session management",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ET01-2022-SessionContinuity-01"
    ),
    DoctrineBlock(
        topic="Model Versioning and Rollback",
        keywords=["model versioning", "rollback", "deployment", "model management"],
        conclusion_template="Version all deployed models and support rollback on performance regression.",
        reasoning_framework="""
        1. Assign unique version to each deployed model.
        2. Log model performance metrics.
        3. Rollback to previous version on regression.
        4. Notify admin of rollbacks.
        5. Document all version changes.
        """,
        key_factors=[
            "Version control",
            "Performance monitoring",
            "Rollback mechanism"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Model Manager",
        adversary_position="Versioning adds deployment overhead.",
        counter_arguments=[
            "Prevents long-term regressions.",
            "Rollback is automated.",
            "Documentation aids troubleshooting."
        ],
        resolution_strategy="Automate versioning; monitor performance.",
        entity_scope="Model management",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-ModelVersion-01"
    ),
    DoctrineBlock(
        topic="Data Retention Policy",
        keywords=["data retention", "privacy", "logs", "compliance"],
        conclusion_template="Retain input and processing logs only as long as required by policy and law.",
        reasoning_framework="""
        1. Define retention periods for all data types.
        2. Automatically delete data after expiry.
        3. Allow user to request deletion.
        4. Log all deletions for audit.
        5. Review policy regularly for compliance.
        """,
        key_factors=[
            "Retention period",
            "Automatic deletion",
            "User rights"
        ],
        primary_authority=[
            "GDPR",
            "ET01_engine.py"
        ],
        burden_holder="Data Controller",
        adversary_position="Short retention may hinder troubleshooting.",
        counter_arguments=[
            "Policy balances privacy and support.",
            "Audit logs are retained.",
            "User rights are prioritized."
        ],
        resolution_strategy="Review policy; adjust as needed.",
        entity_scope="Data management",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-DataRetention-01"
    ),
    DoctrineBlock(
        topic="Privacy by Design",
        keywords=["privacy", "design", "compliance", "data minimization"],
        conclusion_template="Implement privacy by design principles in all voice input processing.",
        reasoning_framework="""
        1. Minimize collection of personal data.
        2. Anonymize or pseudonymize data where possible.
        3. Secure data at rest and in transit.
        4. Provide user controls for data access and deletion.
        5. Review design for privacy compliance regularly.
        """,
        key_factors=[
            "Data minimization",
            "Anonymization",
            "Security"
        ],
        primary_authority=[
            "GDPR",
            "ISO/IEC 27001",
            "ET01_engine.py"
        ],
        burden_holder="System Designer",
        adversary_position="Privacy measures may reduce functionality.",
        counter_arguments=[
            "Design balances privacy and utility.",
            "User controls mitigate risk.",
            "Compliance is mandatory."
        ],
        resolution_strategy="Review and update design; monitor compliance.",
        entity_scope="System-wide",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET01-2022-PrivacyDesign-01"
    ),
    DoctrineBlock(
        topic="Fallback to Text Input",
        keywords=["fallback", "text input", "voice failure", "user experience"],
        conclusion_template="Allow user to switch to text input if voice processing fails.",
        reasoning_framework="""
        1. Detect repeated voice processing failures.
        2. Prompt user to switch to text input.
        3. Route text input through same NLP pipeline.
        4. Log all fallback events.
        5. Restore voice input when available.
        """,
        key_factors=[
            "Failure detection",
            "User prompt",
            "Pipeline compatibility"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System",
        adversary_position="Fallback may disrupt user flow.",
        counter_arguments=[
            "Improves accessibility.",
            "Fallback is optional.",
            "Voice is restored automatically."
        ],
        resolution_strategy="Prompt user; monitor fallback usage.",
        entity_scope="System-wide",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-TextFallback-01"
    ),
    DoctrineBlock(
        topic="User Consent Management",
        keywords=["user consent", "privacy", "compliance", "data collection"],
        conclusion_template="Obtain and manage user consent for voice data processing.",
        reasoning_framework="""
        1. Present clear consent forms to users.
        2. Store consent records securely.
        3. Allow users to withdraw consent at any time.
        4. Cease data processing on withdrawal.
        5. Log all consent changes.
        """,
        key_factors=[
            "Consent form clarity",
            "Record storage",
            "Withdrawal process"
        ],
        primary_authority=[
            "GDPR",
            "ET01_engine.py"
        ],
        burden_holder="Data Controller",
        adversary_position="Consent management adds friction.",
        counter_arguments=[
            "Required for compliance.",
            "Process is streamlined.",
            "User rights are protected."
        ],
        resolution_strategy="Automate consent management; review regularly.",
        entity_scope="Privacy and compliance",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Consent-01"
    ),
    DoctrineBlock(
        topic="System Health Monitoring",
        keywords=["system health", "monitoring", "uptime", "diagnostics"],
        conclusion_template="Monitor system health and alert on critical failures.",
        reasoning_framework="""
        1. Track uptime and error rates for all subsystems.
        2. Alert admin on threshold breaches.
        3. Log all health events.
        4. Provide dashboard for real-time monitoring.
        5. Review logs for preventative maintenance.
        """,
        key_factors=[
            "Uptime tracking",
            "Alerting",
            "Dashboard"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System Admin",
        adversary_position="Monitoring adds resource overhead.",
        counter_arguments=[
            "Prevents downtime.",
            "Dashboard aids troubleshooting.",
            "Overhead is minimal."
        ],
        resolution_strategy="Optimize monitoring; prioritize critical metrics.",
        entity_scope="System-wide",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Health-01"
    ),
    DoctrineBlock(
        topic="Anomaly Detection in Input",
        keywords=["anomaly detection", "input validation", "security", "outlier"],
        conclusion_template="Detect anomalous or outlier inputs to prevent abuse or attacks.",
        reasoning_framework="""
        1. Analyze input for statistical outliers.
        2. Use anomaly detection models for known attack patterns.
        3. Flag and log anomalies.
        4. Escalate to admin for review.
        5. Update models with new threats.
        """,
        key_factors=[
            "Statistical analysis",
            "Model tuning",
            "Escalation"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Security Layer",
        adversary_position="Anomaly detection may block valid inputs.",
        counter_arguments=[
            "False positives are reviewed.",
            "Models are tuned for precision.",
            "Security is prioritized."
        ],
        resolution_strategy="Monitor false positives; update models.",
        entity_scope="Security",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Anomaly-01"
    ),
    DoctrineBlock(
        topic="User Identity Verification",
        keywords=["identity verification", "user authentication", "security", "voice biometrics"],
        conclusion_template="Verify user identity for sensitive actions using voice biometrics or multi-factor authentication.",
        reasoning_framework="""
        1. Enroll user voiceprint during setup.
        2. Verify identity on sensitive commands.
        3. Support fallback to multi-factor authentication.
        4. Log all verification attempts.
        5. Allow user to update or reset voiceprint.
        """,
        key_factors=[
            "Voiceprint accuracy",
            "Multi-factor support",
            "Logging"
        ],
        primary_authority=[
            "ISO/IEC 30107-3:2017",
            "ET01_engine.py"
        ],
        burden_holder="Authentication Layer",
        adversary_position="Voice biometrics may be spoofed.",
        counter_arguments=[
            "Anti-spoofing is implemented.",
            "Fallback to multi-factor is available.",
            "Logs enable review."
        ],
        resolution_strategy="Combine biometrics with multi-factor; monitor for attacks.",
        entity_scope="Authentication",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Identity-01"
    ),
    DoctrineBlock(
        topic="Model Explainability",
        keywords=["explainability", "model transparency", "AI ethics", "user trust"],
        conclusion_template="Provide explanations for model decisions on user request.",
        reasoning_framework="""
        1. Log key features influencing model output.
        2. Summarize decision process in user-friendly terms.
        3. Allow user to request explanation for specific actions.
        4. Review explanations for clarity and accuracy.
        5. Update explanation mechanisms with model changes.
        """,
        key_factors=[
            "Feature logging",
            "User interface",
            "Explanation clarity"
        ],
        primary_authority=[
            "EU AI Act",
            "ET01_engine.py"
        ],
        burden_holder="Model Owner",
        adversary_position="Explainability may expose model internals.",
        counter_arguments=[
            "Explanations are abstracted.",
            "User trust is improved.",
            "Compliance requires transparency."
        ],
        resolution_strategy="Balance detail and abstraction; monitor requests.",
        entity_scope="Model management",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Explainability-01"
    ),
    DoctrineBlock(
        topic="Edge Case Handling",
        keywords=["edge case", "exception handling", "robustness", "input anomalies"],
        conclusion_template="Define and handle edge cases explicitly to ensure system robustness.",
        reasoning_framework="""
        1. Identify common and rare edge cases from logs.
        2. Implement explicit handling logic for each case.
        3. Test edge case handling in QA.
        4. Log all edge case activations.
        5. Update handling as new cases are discovered.
        """,
        key_factors=[
            "Case identification",
            "Handling logic",
            "Testing"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System",
        adversary_position="Explicit handling increases code complexity.",
        counter_arguments=[
            "Prevents system failures.",
            "Complexity is managed via modularization.",
            "Logs aid maintenance."
        ],
        resolution_strategy="Modularize logic; review logs.",
        entity_scope="System-wide",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-EdgeCase-01"
    ),
    DoctrineBlock(
        topic="Test Coverage Requirements",
        keywords=["test coverage", "QA", "unit testing", "integration testing"],
        conclusion_template="Maintain high test coverage for all doctrine logic and processing pipelines.",
        reasoning_framework="""
        1. Write unit and integration tests for all modules.
        2. Track coverage metrics.
        3. Require minimum 90% coverage for production deployment.
        4. Review and update tests with code changes.
        5. Log coverage reports.
        """,
        key_factors=[
            "Test suite",
            "Coverage metrics",
            "Review process"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="QA Team",
        adversary_position="High coverage increases development time.",
        counter_arguments=[
            "Prevents regressions.",
            "Improves reliability.",
            "Coverage is balanced with velocity."
        ],
        resolution_strategy="Automate testing; review coverage regularly.",
        entity_scope="QA",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET01-2022-TestCoverage-01"
    ),
    DoctrineBlock(
        topic="Model Drift Detection",
        keywords=["model drift", "monitoring", "retraining", "accuracy"],
        conclusion_template="Monitor for model drift and retrain as needed to maintain accuracy.",
        reasoning_framework="""
        1. Track model performance metrics over time.
        2. Detect significant drops in accuracy or precision.
        3. Retrain models with new data on drift detection.
        4. Log all drift events and retrainings.
        5. Notify admin of drift and retraining.
        """,
        key_factors=[
            "Performance tracking",
            "Retraining",
            "Logging"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Model Owner",
        adversary_position="Frequent retraining is resource-intensive.",
        counter_arguments=[
            "Retraining is triggered only on drift.",
            "Maintains long-term accuracy.",
            "Admin is notified."
        ],
        resolution_strategy="Automate drift detection; schedule retraining.",
        entity_scope="Model management",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-ModelDrift-01"
    ),
    DoctrineBlock(
        topic="Resource Usage Limiting",
        keywords=["resource usage", "rate limiting", "system stability", "abuse prevention"],
        conclusion_template="Limit resource usage per user and per session to maintain system stability.",
        reasoning_framework="""
        1. Set quotas for CPU, memory, and API calls.
        2. Enforce rate limits on resource-intensive operations.
        3. Notify user on approaching limits.
        4. Log all limit breaches.
        5. Allow admin to adjust quotas.
        """,
        key_factors=[
            "Quota setting",
            "Rate limiting",
            "User notification"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System",
        adversary_position="Limits may frustrate power users.",
        counter_arguments=[
            "Stability is prioritized.",
            "Limits are configurable.",
            "User is notified."
        ],
        resolution_strategy="Balance limits and flexibility; monitor usage.",
        entity_scope="System-wide",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-ResourceLimit-01"
    ),
    DoctrineBlock(
        topic="User Error Recovery",
        keywords=["error recovery", "user correction", "input errors", "robustness"],
        conclusion_template="Support user correction and recovery from input errors.",
        reasoning_framework="""
        1. Detect user corrections (e.g., 'no, I meant ...').
        2. Update context and intent accordingly.
        3. Confirm correction with user.
        4. Log all recovery events.
        5. Tune recovery logic based on user feedback.
        """,
        key_factors=[
            "Correction detection",
            "Context update",
            "User confirmation"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Dialogue Manager",
        adversary_position="Recovery logic adds complexity.",
        counter_arguments=[
            "Improves user experience.",
            "Complexity is modularized.",
            "Feedback guides tuning."
        ],
        resolution_strategy="Modularize logic; monitor feedback.",
        entity_scope="Dialogue management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-UserRecovery-01"
    ),
    DoctrineBlock(
        topic="Input Replay Protection",
        keywords=["replay protection", "security", "input duplication", "attack prevention"],
        conclusion_template="Detect and block replayed or duplicated inputs to prevent abuse.",
        reasoning_framework="""
        1. Hash and store recent input signatures.
        2. Reject inputs matching recent signatures within time window.
        3. Log all replay attempts.
        4. Notify admin of repeated attacks.
        5. Tune window size for balance.
        """,
        key_factors=[
            "Signature hashing",
            "Window size",
            "Logging"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="Security Layer",
        adversary_position="Replay protection may block legitimate repeats.",
        counter_arguments=[
            "Window size is tuned.",
            "Admin is notified of false positives.",
            "Security is prioritized."
        ],
        resolution_strategy="Monitor logs; adjust window size.",
        entity_scope="Security",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-Replay-01"
    ),
    DoctrineBlock(
        topic="Input Rate Limiting",
        keywords=["rate limiting", "input throttling", "abuse prevention", "system stability"],
        conclusion_template="Throttle input rate per user to prevent system overload and abuse.",
        reasoning_framework="""
        1. Track input rate per user/session.
        2. Enforce maximum rate (e.g., N inputs/minute).
        3. Notify user on rate limit breach.
        4. Log all throttling events.
        5. Allow admin to adjust rate limits.
        """,
        key_factors=[
            "Rate tracking",
            "Throttling",
            "User notification"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="System",
        adversary_position="Throttling may slow down power users.",
        counter_arguments=[
            "Prevents abuse.",
            "Limits are configurable.",
            "User is notified."
        ],
        resolution_strategy="Balance limits and flexibility; monitor logs.",
        entity_scope="System-wide",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET01-2022-InputRate-01"
    ),
    DoctrineBlock(
        topic="Input Language Model Selection",
        keywords=["language model", "model selection", "multi-language", "NLP"],
        conclusion_template="Select appropriate language model for input based on detected language and context.",
        reasoning_framework="""
        1. Detect input language.
        2. Match to available language models.
        3. Route input to best-fit model.
        4. Log model selection events.
        5. Update model selection logic as new models are added.
        """,
        key_factors=[
            "Language detection",
            "Model matching",
            "Logging"
        ],
        primary_authority=[
            "ET01_engine.py"
        ],
        burden_holder="NLP Pipeline",
        adversary_position="Model selection adds overhead.",
        counter_arguments=[
            "Ensures high accuracy.",
            "Overhead is minimal.",
            "Logs enable tuning."
        ],
        resolution_strategy="Optimize selection logic; monitor logs.",
        entity_scope="NLP pipeline",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET01-2022-LMSelect-01"
    ),
    DoctrineBlock(
        topic="User Data Export",
        keywords=["data export", "user rights", "privacy", "compliance"],
        conclusion_template="Allow users to export their data in a machine-readable format.",
        reasoning_framework="""
        1. Provide export option in user interface.
        2. Package data in standard format (e.g., JSON).
        3. Secure export with authentication.
        4. Log all export events.
        5. Comply with legal requirements for export.
        """,
        key_factors=[
            "Export format",
            "Authentication",
            "Compliance"
        ],
        primary_authority=[
            "GDPR",
            "ET01_engine.py"
        ],
        burden_holder="Data Controller",
        adversary_position="Export may expose sensitive data.",
        counter_arguments=[
            "Authentication is required.",
            "Export is logged.",
            "Compliance is mandatory."
        ],
        resolution_strategy="Secure export; monitor logs.",
        entity_scope="Privacy and compliance",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET01-2022-DataExport-01"
    ),
    DoctrineBlock(
        topic="User Data Deletion",
        keywords=["data deletion", "user rights", "privacy", "compliance"],
        conclusion_template="Allow users to request deletion of their data in compliance with regulations.",
        reasoning_framework="""
        1. Provide deletion option in user interface.
        2. Delete all user data from system and backups.
        3. Log deletion events for audit.
        4. Notify user of completion.
        5. Comply with legal requirements for deletion.
        """,
        key_factors=[
            "Deletion mechanism",
            "Audit logging",
            "Compliance"
        ],
        primary_authority=[
            "GDPR",
            "ET01_engine.py"
        ],
        burden_holder="Data Controller",
        adversary_position="Deletion may hinder troubleshooting.",
        counter_arguments=[
            "Compliance is mandatory.",
            "Audit logs are retained.",
            "User is notified."
        ],
        resolution_strategy="Automate deletion; review logs.",
        entity_scope="Privacy and compliance",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET01-2022-DataDelete-01"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if (
            keyword_lower in doctrine.topic.lower()
            or any(keyword_lower in k.lower() for k in doctrine.keywords)
            or keyword_lower in doctrine.reasoning_framework.lower()
            or keyword_lower in doctrine.conclusion_template.lower()
        ):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]