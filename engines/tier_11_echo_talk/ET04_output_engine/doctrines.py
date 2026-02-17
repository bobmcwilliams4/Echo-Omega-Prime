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
        topic="ElevenLabs v3 API Integration",
        keywords=["ElevenLabs", "API", "v3", "integration", "TTS", "endpoint"],
        conclusion_template="The ET04 engine must integrate with the ElevenLabs v3 API for all TTS requests.",
        reasoning_framework=(
            "1. Evaluate the ElevenLabs v3 API documentation for endpoint specifications and authentication requirements.\n"
            "2. Ensure all TTS requests are routed via the v3 endpoints, utilizing secure API keys.\n"
            "3. Handle error responses and rate limits as defined by ElevenLabs.\n"
            "4. Maintain backward compatibility with legacy endpoints only as a fallback.\n"
            "5. Log all integration errors for audit and debugging.\n"
            "6. Regularly update integration code to match ElevenLabs v3 API changes.\n"
            "7. Implement robust retry logic for transient failures.\n"
            "8. Validate audio payloads and metadata returned from the API.\n"
            "9. Ensure all network traffic is encrypted (HTTPS).\n"
            "10. Monitor for deprecation notices from ElevenLabs and plan migrations accordingly."
        ),
        key_factors=[
            "API endpoint stability",
            "Authentication method",
            "Error handling",
            "API versioning",
            "Security compliance"
        ],
        primary_authority=["ElevenLabs API Documentation", "ET04 Integration Guide"],
        burden_holder="ET04 Output Engine Integration Layer",
        adversary_position="Direct integration with ElevenLabs v3 API is unnecessary; local TTS suffices.",
        counter_arguments=[
            "Local TTS lacks the quality and features of ElevenLabs.",
            "API integration introduces external dependencies and latency."
        ],
        resolution_strategy="Demonstrate feature parity and superior quality via ElevenLabs; mitigate latency with caching.",
        entity_scope="TTS Output Subsystem",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ET03 adopted ElevenLabs v2 API as mandatory."
    ),
    DoctrineBlock(
        topic="Voice ID Mapping: Echo",
        keywords=["voice", "ID", "mapping", "Echo", "speaker", "profile"],
        conclusion_template="The Echo voice must be mapped to the canonical ElevenLabs Echo Voice ID.",
        reasoning_framework=(
            "1. Retrieve the official Echo Voice ID from the ElevenLabs voice catalog.\n"
            "2. Store the mapping in the ET04 voice registry for reference by the TTS subsystem.\n"
            "3. Validate the mapping during system startup and on voice selection requests.\n"
            "4. If the Echo Voice ID changes in ElevenLabs, update the mapping and notify dependent services.\n"
            "5. Ensure fallback to a default voice if the Echo mapping is unavailable.\n"
            "6. Document the mapping in the engine's configuration files.\n"
            "7. Test the mapping with sample utterances to confirm correct voice rendering."
        ),
        key_factors=[
            "Voice registry accuracy",
            "Mapping persistence",
            "Voice catalog updates"
        ],
        primary_authority=["ElevenLabs Voice Catalog", "ET04 Voice Registry"],
        burden_holder="Voice Mapping Subsystem",
        adversary_position="Echo mapping is unnecessary; dynamic lookup suffices.",
        counter_arguments=[
            "Dynamic lookup may introduce latency and inconsistency.",
            "Hardcoded mapping risks obsolescence."
        ],
        resolution_strategy="Implement periodic validation and allow for dynamic overrides.",
        entity_scope="Voice Selection Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 static mapping for Echo voice."
    ),
    DoctrineBlock(
        topic="Voice ID Mapping: Bree",
        keywords=["voice", "ID", "mapping", "Bree", "speaker", "profile"],
        conclusion_template="The Bree voice must be mapped to the canonical ElevenLabs Bree Voice ID.",
        reasoning_framework=(
            "1. Obtain the Bree Voice ID from the ElevenLabs catalog and verify its validity.\n"
            "2. Update the ET04 voice registry with the Bree mapping.\n"
            "3. Ensure the mapping is referenced in all TTS requests for Bree.\n"
            "4. Monitor for catalog changes and update as necessary.\n"
            "5. Provide fallback to a default female voice if Bree is unavailable.\n"
            "6. Log all mapping changes for audit purposes."
        ),
        key_factors=[
            "Voice catalog accuracy",
            "Mapping update process"
        ],
        primary_authority=["ElevenLabs Voice Catalog"],
        burden_holder="Voice Mapping Subsystem",
        adversary_position="Bree mapping can be resolved at runtime.",
        counter_arguments=[
            "Runtime resolution may cause delays.",
            "Persistent mapping ensures consistency."
        ],
        resolution_strategy="Use persistent mapping with scheduled runtime validation.",
        entity_scope="Voice Selection Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 static mapping for Bree voice."
    ),
    DoctrineBlock(
        topic="Voice ID Mapping: GS343",
        keywords=["voice", "ID", "mapping", "GS343", "speaker", "profile"],
        conclusion_template="The GS343 voice must be mapped to the Cartesia GS343 Voice Personality via API.",
        reasoning_framework=(
            "1. Query the Cartesia API for the GS343 voice personality metadata.\n"
            "2. Store the GS343 mapping in the ET04 voice registry.\n"
            "3. Ensure the mapping is used for all GS343 TTS requests.\n"
            "4. Validate the mapping on system startup and periodically.\n"
            "5. Provide fallback to a similar voice if GS343 is unavailable.\n"
            "6. Document the mapping and update procedures."
        ),
        key_factors=[
            "Cartesia API reliability",
            "Voice registry synchronization"
        ],
        primary_authority=["Cartesia API Documentation"],
        burden_holder="Voice Mapping Subsystem",
        adversary_position="Direct Cartesia mapping is unnecessary; use ElevenLabs fallback.",
        counter_arguments=[
            "Cartesia provides unique GS343 personality features.",
            "Fallback may lack required characteristics."
        ],
        resolution_strategy="Prioritize Cartesia mapping with fallback to ElevenLabs only on failure.",
        entity_scope="Voice Selection Layer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET03 GS343 mapping via Cartesia API."
    ),
    DoctrineBlock(
        topic="Voice ID Mapping: Prometheus",
        keywords=["voice", "ID", "mapping", "Prometheus", "speaker", "profile"],
        conclusion_template="The Prometheus voice must be mapped to the official ElevenLabs Prometheus Voice ID.",
        reasoning_framework=(
            "1. Retrieve Prometheus Voice ID from the ElevenLabs catalog.\n"
            "2. Update the ET04 voice registry accordingly.\n"
            "3. Validate the mapping on each TTS request for Prometheus.\n"
            "4. Provide fallback to a similar male voice if Prometheus is unavailable.\n"
            "5. Log mapping changes and errors."
        ),
        key_factors=[
            "Voice catalog updates",
            "Fallback handling"
        ],
        primary_authority=["ElevenLabs Voice Catalog"],
        burden_holder="Voice Mapping Subsystem",
        adversary_position="Prometheus mapping can be resolved dynamically.",
        counter_arguments=[
            "Dynamic resolution may cause inconsistencies.",
            "Persistent mapping ensures reliability."
        ],
        resolution_strategy="Use persistent mapping with runtime validation.",
        entity_scope="Voice Selection Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 static mapping for Prometheus voice."
    ),
    DoctrineBlock(
        topic="Voice ID Mapping: Phoenix",
        keywords=["voice", "ID", "mapping", "Phoenix", "speaker", "profile"],
        conclusion_template="The Phoenix voice must be mapped to the official ElevenLabs Phoenix Voice ID.",
        reasoning_framework=(
            "1. Obtain Phoenix Voice ID from the ElevenLabs catalog.\n"
            "2. Store the mapping in the ET04 voice registry.\n"
            "3. Ensure all TTS requests for Phoenix use the mapped ID.\n"
            "4. Provide fallback to a similar voice if Phoenix is unavailable.\n"
            "5. Document and log mapping changes."
        ),
        key_factors=[
            "Voice catalog synchronization",
            "Fallback strategy"
        ],
        primary_authority=["ElevenLabs Voice Catalog"],
        burden_holder="Voice Mapping Subsystem",
        adversary_position="Phoenix mapping can be resolved at runtime.",
        counter_arguments=[
            "Runtime resolution may introduce latency.",
            "Persistent mapping ensures consistency."
        ],
        resolution_strategy="Persist mapping with scheduled validation.",
        entity_scope="Voice Selection Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 static mapping for Phoenix voice."
    ),
    DoctrineBlock(
        topic="Voice ID Mapping: Commander",
        keywords=["voice", "ID", "mapping", "Commander", "speaker", "profile"],
        conclusion_template="The Commander voice must be mapped to the official ElevenLabs Commander Voice ID.",
        reasoning_framework=(
            "1. Retrieve Commander Voice ID from the ElevenLabs catalog.\n"
            "2. Update the ET04 voice registry with the mapping.\n"
            "3. Validate the mapping on TTS requests for Commander.\n"
            "4. Provide fallback to a similar authoritative voice if Commander is unavailable.\n"
            "5. Log mapping changes and errors."
        ),
        key_factors=[
            "Voice catalog updates",
            "Fallback handling"
        ],
        primary_authority=["ElevenLabs Voice Catalog"],
        burden_holder="Voice Mapping Subsystem",
        adversary_position="Commander mapping can be resolved dynamically.",
        counter_arguments=[
            "Dynamic resolution may cause inconsistencies.",
            "Persistent mapping ensures reliability."
        ],
        resolution_strategy="Use persistent mapping with runtime validation.",
        entity_scope="Voice Selection Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 static mapping for Commander voice."
    ),
    DoctrineBlock(
        topic="Emotion Tag Processing: Laughs",
        keywords=["emotion", "tag", "processing", "laugh", "SSML", "TTS"],
        conclusion_template="The ET04 engine must process <laugh> tags and render corresponding laughter audio.",
        reasoning_framework=(
            "1. Parse SSML input for <laugh> tags.\n"
            "2. Map <laugh> tags to the appropriate ElevenLabs emotion parameter or audio sample.\n"
            "3. If ElevenLabs does not support direct laughter, insert a pre-recorded laughter audio segment.\n"
            "4. Ensure timing and context are preserved in the output audio.\n"
            "5. Log all emotion tag processing for debugging and analytics.\n"
            "6. Provide fallback to neutral voice if laughter cannot be rendered."
        ),
        key_factors=[
            "SSML parsing accuracy",
            "ElevenLabs emotion support",
            "Audio timing"
        ],
        primary_authority=["SSML Specification", "ElevenLabs API Documentation"],
        burden_holder="Emotion Tag Processor",
        adversary_position="Laughter can be ignored or replaced with neutral speech.",
        counter_arguments=[
            "Ignoring laughter reduces expressiveness.",
            "Neutral speech cannot convey intended humor."
        ],
        resolution_strategy="Prioritize expressive rendering; fallback only if technically infeasible.",
        entity_scope="Emotion Processing Layer",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET03 emotion tag handling for laughs."
    ),
    DoctrineBlock(
        topic="Emotion Tag Processing: Whispers",
        keywords=["emotion", "tag", "processing", "whisper", "SSML", "TTS"],
        conclusion_template="The ET04 engine must process <whisper> tags and render corresponding whispered audio.",
        reasoning_framework=(
            "1. Detect <whisper> tags in SSML input.\n"
            "2. Map <whisper> tags to ElevenLabs whisper emotion parameter if supported.\n"
            "3. If not supported, apply a digital whisper filter to the audio segment.\n"
            "4. Ensure the whispered segment is contextually appropriate and intelligible.\n"
            "5. Log all whisper tag processing for analysis.\n"
            "6. Provide fallback to neutral voice if whisper rendering is not possible."
        ),
        key_factors=[
            "SSML parsing",
            "ElevenLabs whisper support",
            "Audio filtering"
        ],
        primary_authority=["SSML Specification", "ElevenLabs API Documentation"],
        burden_holder="Emotion Tag Processor",
        adversary_position="Whispering can be ignored or replaced with neutral speech.",
        counter_arguments=[
            "Ignoring whispers reduces expressiveness.",
            "Neutral speech cannot convey intended intimacy or secrecy."
        ],
        resolution_strategy="Prioritize expressive rendering; fallback only if technically infeasible.",
        entity_scope="Emotion Processing Layer",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET03 emotion tag handling for whispers."
    ),
    DoctrineBlock(
        topic="Emotion Tag Processing: Sighs",
        keywords=["emotion", "tag", "processing", "sigh", "SSML", "TTS"],
        conclusion_template="The ET04 engine must process <sigh> tags and render corresponding sigh audio.",
        reasoning_framework=(
            "1. Parse SSML input for <sigh> tags.\n"
            "2. Map <sigh> tags to ElevenLabs emotion parameter if available.\n"
            "3. If not available, insert a pre-recorded sigh audio segment.\n"
            "4. Ensure the sigh is contextually appropriate and does not disrupt speech flow.\n"
            "5. Log all sigh tag processing for analytics.\n"
            "6. Provide fallback to neutral voice if sigh rendering is not possible."
        ),
        key_factors=[
            "SSML parsing",
            "ElevenLabs emotion support",
            "Audio timing"
        ],
        primary_authority=["SSML Specification", "ElevenLabs API Documentation"],
        burden_holder="Emotion Tag Processor",
        adversary_position="Sighs can be omitted without loss of meaning.",
        counter_arguments=[
            "Omitting sighs reduces expressiveness.",
            "Sighs can convey important emotional context."
        ],
        resolution_strategy="Prioritize expressive rendering; fallback only if technically infeasible.",
        entity_scope="Emotion Processing Layer",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ET03 emotion tag handling for sighs."
    ),
    DoctrineBlock(
        topic="Emotion Tag Processing: Sarcastic",
        keywords=["emotion", "tag", "processing", "sarcastic", "SSML", "TTS"],
        conclusion_template="The ET04 engine must process <sarcastic> tags and render corresponding sarcastic tone.",
        reasoning_framework=(
            "1. Detect <sarcastic> tags in SSML input.\n"
            "2. Map <sarcastic> tags to ElevenLabs emotion parameter if supported.\n"
            "3. If not supported, adjust prosody and pitch to simulate sarcasm.\n"
            "4. Ensure the sarcastic tone is contextually appropriate and intelligible.\n"
            "5. Log all sarcastic tag processing for analysis.\n"
            "6. Provide fallback to neutral voice if sarcasm rendering is not possible."
        ),
        key_factors=[
            "SSML parsing",
            "ElevenLabs emotion support",
            "Prosody adjustment"
        ],
        primary_authority=["SSML Specification", "ElevenLabs API Documentation"],
        burden_holder="Emotion Tag Processor",
        adversary_position="Sarcasm can be omitted or replaced with neutral speech.",
        counter_arguments=[
            "Omitting sarcasm reduces expressiveness.",
            "Sarcasm conveys important nuance."
        ],
        resolution_strategy="Prioritize expressive rendering; fallback only if technically infeasible.",
        entity_scope="Emotion Processing Layer",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET03 emotion tag handling for sarcasm."
    ),
    DoctrineBlock(
        topic="Emotion Tag Processing: Excited",
        keywords=["emotion", "tag", "processing", "excited", "SSML", "TTS"],
        conclusion_template="The ET04 engine must process <excited> tags and render corresponding excited tone.",
        reasoning_framework=(
            "1. Detect <excited> tags in SSML input.\n"
            "2. Map <excited> tags to ElevenLabs emotion parameter if supported.\n"
            "3. If not supported, adjust pitch, rate, and volume to simulate excitement.\n"
            "4. Ensure the excited tone is contextually appropriate and intelligible.\n"
            "5. Log all excited tag processing for analysis.\n"
            "6. Provide fallback to neutral voice if excitement rendering is not possible."
        ),
        key_factors=[
            "SSML parsing",
            "ElevenLabs emotion support",
            "Prosody adjustment"
        ],
        primary_authority=["SSML Specification", "ElevenLabs API Documentation"],
        burden_holder="Emotion Tag Processor",
        adversary_position="Excitement can be omitted or replaced with neutral speech.",
        counter_arguments=[
            "Omitting excitement reduces expressiveness.",
            "Excitement conveys important emotional context."
        ],
        resolution_strategy="Prioritize expressive rendering; fallback only if technically infeasible.",
        entity_scope="Emotion Processing Layer",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ET03 emotion tag handling for excitement."
    ),
    DoctrineBlock(
        topic="Cartesia API for GS343 Voice Personality",
        keywords=["Cartesia", "API", "GS343", "voice", "personality", "integration"],
        conclusion_template="The ET04 engine must integrate with the Cartesia API to access the GS343 voice personality.",
        reasoning_framework=(
            "1. Review Cartesia API documentation for authentication and endpoint details.\n"
            "2. Implement secure API calls to retrieve GS343 voice personality data.\n"
            "3. Cache personality data locally for performance.\n"
            "4. Handle API errors and implement retry logic for transient failures.\n"
            "5. Monitor for API changes and update integration as needed.\n"
            "6. Log all API interactions for audit and debugging."
        ),
        key_factors=[
            "API reliability",
            "Authentication method",
            "Caching strategy"
        ],
        primary_authority=["Cartesia API Documentation"],
        burden_holder="Integration Layer",
        adversary_position="Cartesia API integration is unnecessary; use ElevenLabs fallback.",
        counter_arguments=[
            "Cartesia provides unique GS343 features.",
            "Fallback may lack required characteristics."
        ],
        resolution_strategy="Prioritize Cartesia integration with fallback to ElevenLabs only on failure.",
        entity_scope="Voice Selection Layer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET03 Cartesia API integration for GS343."
    ),
    DoctrineBlock(
        topic="Whisper STT Integration",
        keywords=["Whisper", "STT", "integration", "speech-to-text", "OpenAI"],
        conclusion_template="The ET04 engine must integrate with Whisper STT for all speech-to-text requirements.",
        reasoning_framework=(
            "1. Review Whisper STT API documentation for endpoint and model details.\n"
            "2. Implement secure API calls for speech-to-text conversion.\n"
            "3. Handle audio format compatibility between ET04 and Whisper.\n"
            "4. Implement error handling and retry logic for transient failures.\n"
            "5. Cache STT results where appropriate to optimize performance.\n"
            "6. Log all STT interactions for debugging and analytics."
        ),
        key_factors=[
            "API reliability",
            "Audio format compatibility",
            "Caching strategy"
        ],
        primary_authority=["Whisper STT Documentation"],
        burden_holder="Integration Layer",
        adversary_position="Whisper STT integration is unnecessary; use local STT.",
        counter_arguments=[
            "Local STT may lack accuracy.",
            "Whisper provides state-of-the-art performance."
        ],
        resolution_strategy="Prioritize Whisper integration; fallback to local STT only if Whisper is unavailable.",
        entity_scope="Speech Recognition Layer",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ET03 Whisper STT integration."
    ),
    DoctrineBlock(
        topic="Voice Streaming: Chunked Transfer",
        keywords=["voice", "streaming", "chunked", "transfer", "HTTP", "audio"],
        conclusion_template="The ET04 engine must support chunked transfer encoding for streaming voice output.",
        reasoning_framework=(
            "1. Implement HTTP chunked transfer encoding for all streaming endpoints.\n"
            "2. Ensure audio data is sent in manageable chunks to minimize latency.\n"
            "3. Handle client disconnects and partial transfers gracefully.\n"
            "4. Monitor chunk sizes and adjust for optimal performance.\n"
            "5. Log all streaming sessions for debugging and analytics."
        ),
        key_factors=[
            "Chunk size optimization",
            "Client compatibility",
            "Error handling"
        ],
        primary_authority=["HTTP/1.1 Specification", "ET04 Streaming Guide"],
        burden_holder="Streaming Subsystem",
        adversary_position="Chunked transfer is unnecessary; send full audio after generation.",
        counter_arguments=[
            "Chunked transfer reduces latency.",
            "Full audio transfer increases perceived delay."
        ],
        resolution_strategy="Demonstrate latency improvements with chunked transfer.",
        entity_scope="Streaming Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 chunked transfer implementation."
    ),
    DoctrineBlock(
        topic="Voice Streaming: Buffer Management",
        keywords=["voice", "streaming", "buffer", "management", "audio", "latency"],
        conclusion_template="The ET04 engine must implement efficient buffer management for streaming audio.",
        reasoning_framework=(
            "1. Allocate audio buffers dynamically based on stream size and client bandwidth.\n"
            "2. Monitor buffer fill levels to prevent underruns and overruns.\n"
            "3. Adjust buffer sizes in real-time to optimize latency and throughput.\n"
            "4. Log buffer statistics for performance analysis.\n"
            "5. Provide alerts for buffer-related errors."
        ),
        key_factors=[
            "Buffer size optimization",
            "Latency management",
            "Error detection"
        ],
        primary_authority=["ET04 Streaming Guide"],
        burden_holder="Streaming Subsystem",
        adversary_position="Simple static buffers are sufficient.",
        counter_arguments=[
            "Static buffers may cause latency spikes.",
            "Dynamic management improves user experience."
        ],
        resolution_strategy="Demonstrate improved performance with dynamic buffer management.",
        entity_scope="Streaming Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 buffer management implementation."
    ),
    DoctrineBlock(
        topic="Audio Format Handling: PCM",
        keywords=["audio", "format", "handling", "PCM", "conversion"],
        conclusion_template="The ET04 engine must support PCM audio format for input and output.",
        reasoning_framework=(
            "1. Implement PCM encoding and decoding for all audio streams.\n"
            "2. Ensure compatibility with ElevenLabs and Whisper APIs.\n"
            "3. Provide conversion utilities for other formats as needed.\n"
            "4. Log all format conversions for debugging."
        ),
        key_factors=[
            "Format compatibility",
            "Conversion accuracy"
        ],
        primary_authority=["Audio Format Specification"],
        burden_holder="Audio Processing Subsystem",
        adversary_position="PCM support is unnecessary; use compressed formats only.",
        counter_arguments=[
            "PCM is widely supported and lossless.",
            "Some APIs require PCM input."
        ],
        resolution_strategy="Support PCM as a baseline; offer compressed formats as options.",
        entity_scope="Audio Processing Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 PCM support."
    ),
    DoctrineBlock(
        topic="Audio Format Handling: MP3",
        keywords=["audio", "format", "handling", "MP3", "conversion"],
        conclusion_template="The ET04 engine must support MP3 audio format for input and output.",
        reasoning_framework=(
            "1. Implement MP3 encoding and decoding for all audio streams.\n"
            "2. Ensure compatibility with ElevenLabs and Whisper APIs.\n"
            "3. Provide conversion utilities for other formats as needed.\n"
            "4. Log all format conversions for debugging."
        ),
        key_factors=[
            "Format compatibility",
            "Conversion accuracy"
        ],
        primary_authority=["Audio Format Specification"],
        burden_holder="Audio Processing Subsystem",
        adversary_position="MP3 support is unnecessary; use lossless formats only.",
        counter_arguments=[
            "MP3 is widely supported and efficient.",
            "Some clients require MP3 output."
        ],
        resolution_strategy="Support MP3 as an option; default to lossless formats where possible.",
        entity_scope="Audio Processing Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 MP3 support."
    ),
    DoctrineBlock(
        topic="Audio Format Handling: OGG",
        keywords=["audio", "format", "handling", "OGG", "conversion"],
        conclusion_template="The ET04 engine must support OGG audio format for input and output.",
        reasoning_framework=(
            "1. Implement OGG encoding and decoding for all audio streams.\n"
            "2. Ensure compatibility with ElevenLabs and Whisper APIs.\n"
            "3. Provide conversion utilities for other formats as needed.\n"
            "4. Log all format conversions for debugging."
        ),
        key_factors=[
            "Format compatibility",
            "Conversion accuracy"
        ],
        primary_authority=["Audio Format Specification"],
        burden_holder="Audio Processing Subsystem",
        adversary_position="OGG support is unnecessary; use more common formats.",
        counter_arguments=[
            "OGG is open-source and efficient.",
            "Some clients require OGG output."
        ],
        resolution_strategy="Support OGG as an option; default to more common formats where possible.",
        entity_scope="Audio Processing Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 OGG support."
    ),
    DoctrineBlock(
        topic="Sample Rate Management",
        keywords=["audio", "sample", "rate", "management", "conversion"],
        conclusion_template="The ET04 engine must manage audio sample rates for compatibility with all integrated APIs.",
        reasoning_framework=(
            "1. Detect required sample rates for ElevenLabs, Whisper, and Cartesia APIs.\n"
            "2. Implement sample rate conversion utilities.\n"
            "3. Validate sample rates before sending audio to external APIs.\n"
            "4. Log all sample rate conversions for debugging."
        ),
        key_factors=[
            "API requirements",
            "Conversion accuracy"
        ],
        primary_authority=["Audio Format Specification"],
        burden_holder="Audio Processing Subsystem",
        adversary_position="Sample rate management is unnecessary; use default rates.",
        counter_arguments=[
            "APIs may reject incompatible sample rates.",
            "Conversion ensures maximum compatibility."
        ],
        resolution_strategy="Implement sample rate detection and conversion as standard practice.",
        entity_scope="Audio Processing Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 sample rate management."
    ),
    DoctrineBlock(
        topic="Voice Cloning Parameters",
        keywords=["voice", "cloning", "parameters", "customization", "TTS"],
        conclusion_template="The ET04 engine must support configurable voice cloning parameters.",
        reasoning_framework=(
            "1. Expose configuration options for voice cloning (e.g., timbre, accent, pitch).\n"
            "2. Validate parameters before submitting to ElevenLabs or Cartesia APIs.\n"
            "3. Provide sensible defaults and document all options.\n"
            "4. Log all cloning parameter usage for analytics."
        ),
        key_factors=[
            "Parameter validation",
            "API compatibility"
        ],
        primary_authority=["ElevenLabs API Documentation", "Cartesia API Documentation"],
        burden_holder="Voice Cloning Subsystem",
        adversary_position="Voice cloning should use fixed parameters.",
        counter_arguments=[
            "Configurable parameters allow for greater flexibility.",
            "Fixed parameters limit expressiveness."
        ],
        resolution_strategy="Support configurable parameters with validation.",
        entity_scope="Voice Cloning Layer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET03 voice cloning parameter support."
    ),
    DoctrineBlock(
        topic="Pronunciation Dictionary Integration",
        keywords=["pronunciation", "dictionary", "integration", "TTS", "lexicon"],
        conclusion_template="The ET04 engine must integrate a pronunciation dictionary for accurate TTS output.",
        reasoning_framework=(
            "1. Load pronunciation dictionaries at system startup.\n"
            "2. Reference the dictionary during TTS synthesis for word-level corrections.\n"
            "3. Allow for custom user dictionaries.\n"
            "4. Log all dictionary lookups and overrides."
        ),
        key_factors=[
            "Dictionary accuracy",
            "Customizability"
        ],
        primary_authority=["Lexicon Specification"],
        burden_holder="Pronunciation Subsystem",
        adversary_position="Pronunciation dictionary is unnecessary; rely on API defaults.",
        counter_arguments=[
            "APIs may mispronounce uncommon words.",
            "Custom dictionaries improve accuracy."
        ],
        resolution_strategy="Integrate dictionary as a standard feature.",
        entity_scope="TTS Processing Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 pronunciation dictionary integration."
    ),
    DoctrineBlock(
        topic="SSML to Emotion Tag Conversion",
        keywords=["SSML", "emotion", "tag", "conversion", "TTS"],
        conclusion_template="The ET04 engine must convert SSML emotion tags to ElevenLabs emotion parameters.",
        reasoning_framework=(
            "1. Parse SSML for emotion tags (e.g., <laugh>, <whisper>, <excited>).\n"
            "2. Map tags to ElevenLabs emotion parameters.\n"
            "3. Handle unsupported tags with fallback strategies.\n"
            "4. Log all conversions for debugging."
        ),
        key_factors=[
            "Tag mapping accuracy",
            "Fallback handling"
        ],
        primary_authority=["SSML Specification", "ElevenLabs API Documentation"],
        burden_holder="Emotion Tag Processor",
        adversary_position="Direct SSML rendering is sufficient.",
        counter_arguments=[
            "Direct rendering may not trigger correct emotion in TTS.",
            "Explicit mapping ensures intended expressiveness."
        ],
        resolution_strategy="Implement explicit tag-to-parameter mapping.",
        entity_scope="Emotion Processing Layer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET03 SSML to emotion mapping."
    ),
    DoctrineBlock(
        topic="TTS Latency Optimization",
        keywords=["TTS", "latency", "optimization", "performance"],
        conclusion_template="The ET04 engine must optimize TTS latency for real-time applications.",
        reasoning_framework=(
            "1. Profile TTS pipeline to identify latency bottlenecks.\n"
            "2. Implement asynchronous processing where possible.\n"
            "3. Cache frequent requests to reduce API round-trips.\n"
            "4. Optimize network stack for low-latency communication.\n"
            "5. Log latency metrics for continuous improvement."
        ),
        key_factors=[
            "Pipeline profiling",
            "Asynchronous processing",
            "Caching strategy"
        ],
        primary_authority=["ET04 Performance Guide"],
        burden_holder="Performance Subsystem",
        adversary_position="Latency is acceptable with current implementation.",
        counter_arguments=[
            "Lower latency improves user experience.",
            "Real-time applications require minimal delay."
        ],
        resolution_strategy="Demonstrate measurable latency reductions.",
        entity_scope="Performance Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 latency optimization."
    ),
    DoctrineBlock(
        topic="Audio Buffer Management",
        keywords=["audio", "buffer", "management", "streaming", "latency"],
        conclusion_template="The ET04 engine must implement robust audio buffer management.",
        reasoning_framework=(
            "1. Allocate and manage audio buffers based on stream requirements.\n"
            "2. Monitor buffer health and adjust dynamically.\n"
            "3. Prevent buffer underruns and overruns.\n"
            "4. Log buffer statistics for analysis."
        ),
        key_factors=[
            "Buffer allocation",
            "Dynamic adjustment"
        ],
        primary_authority=["ET04 Streaming Guide"],
        burden_holder="Streaming Subsystem",
        adversary_position="Static buffers are sufficient.",
        counter_arguments=[
            "Dynamic management improves reliability.",
            "Static buffers may cause issues under load."
        ],
        resolution_strategy="Implement dynamic buffer management.",
        entity_scope="Streaming Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 buffer management."
    ),
    DoctrineBlock(
        topic="Fallback Voice Selection",
        keywords=["fallback", "voice", "selection", "TTS", "error handling"],
        conclusion_template="The ET04 engine must implement fallback voice selection for unavailable voices.",
        reasoning_framework=(
            "1. Detect unavailable or failed voice selections.\n"
            "2. Select the most similar available voice as fallback.\n"
            "3. Notify users or log fallback events.\n"
            "4. Allow for configurable fallback preferences."
        ),
        key_factors=[
            "Fallback similarity",
            "User notification"
        ],
        primary_authority=["ET04 Voice Selection Guide"],
        burden_holder="Voice Selection Subsystem",
        adversary_position="Fallback is unnecessary; fail requests instead.",
        counter_arguments=[
            "Fallback improves reliability.",
            "Failing requests degrades user experience."
        ],
        resolution_strategy="Implement fallback as standard practice.",
        entity_scope="Voice Selection Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 fallback voice selection."
    ),
    DoctrineBlock(
        topic="Voice Personality Matching",
        keywords=["voice", "personality", "matching", "TTS", "user preference"],
        conclusion_template="The ET04 engine must match voice personalities to user or context preferences.",
        reasoning_framework=(
            "1. Collect user or context preferences for voice personality.\n"
            "2. Match preferences to available voices using metadata.\n"
            "3. Provide best-fit voice if exact match is unavailable.\n"
            "4. Log all personality matching decisions."
        ),
        key_factors=[
            "Preference collection",
            "Metadata accuracy"
        ],
        primary_authority=["ET04 Voice Selection Guide"],
        burden_holder="Voice Selection Subsystem",
        adversary_position="Personality matching is unnecessary; use default voice.",
        counter_arguments=[
            "Matching improves personalization.",
            "Default voice may not suit all contexts."
        ],
        resolution_strategy="Implement personality matching as standard.",
        entity_scope="Voice Selection Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 personality matching."
    ),
    DoctrineBlock(
        topic="Audio Quality Scoring",
        keywords=["audio", "quality", "scoring", "TTS", "analysis"],
        conclusion_template="The ET04 engine must implement audio quality scoring for all output.",
        reasoning_framework=(
            "1. Analyze audio output for quality metrics (e.g., SNR, clarity, artifacts).\n"
            "2. Score each output and log results.\n"
            "3. Use scores to trigger alerts or fallback if quality is below threshold.\n"
            "4. Continuously refine scoring algorithms."
        ),
        key_factors=[
            "Metric selection",
            "Threshold definition"
        ],
        primary_authority=["Audio Quality Specification"],
        burden_holder="Quality Assurance Subsystem",
        adversary_position="Quality scoring is unnecessary; rely on user feedback.",
        counter_arguments=[
            "Automated scoring enables proactive quality control.",
            "User feedback may be delayed or inconsistent."
        ],
        resolution_strategy="Implement automated scoring as standard.",
        entity_scope="Quality Assurance Layer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET03 audio quality scoring."
    ),
    DoctrineBlock(
        topic="Noise Gate Application",
        keywords=["noise", "gate", "application", "audio", "processing"],
        conclusion_template="The ET04 engine must apply a noise gate to all audio output.",
        reasoning_framework=(
            "1. Analyze audio output for background noise levels.\n"
            "2. Apply a noise gate filter to suppress unwanted noise.\n"
            "3. Tune noise gate parameters for optimal performance.\n"
            "4. Log all noise gate applications."
        ),
        key_factors=[
            "Noise detection",
            "Parameter tuning"
        ],
        primary_authority=["Audio Processing Specification"],
        burden_holder="Audio Processing Subsystem",
        adversary_position="Noise gate is unnecessary; output is clean.",
        counter_arguments=[
            "Some environments introduce noise.",
            "Noise gate improves perceived quality."
        ],
        resolution_strategy="Apply noise gate as standard practice.",
        entity_scope="Audio Processing Layer",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ET03 noise gate application."
    ),
    DoctrineBlock(
        topic="Volume Normalization",
        keywords=["volume", "normalization", "audio", "processing"],
        conclusion_template="The ET04 engine must normalize audio volume for all output.",
        reasoning_framework=(
            "1. Analyze audio output for volume levels.\n"
            "2. Normalize volume to a standard target level.\n"
            "3. Prevent clipping and distortion during normalization.\n"
            "4. Log all normalization events."
        ),
        key_factors=[
            "Target level selection",
            "Clipping prevention"
        ],
        primary_authority=["Audio Processing Specification"],
        burden_holder="Audio Processing Subsystem",
        adversary_position="Volume normalization is unnecessary; output is consistent.",
        counter_arguments=[
            "Input sources may vary in volume.",
            "Normalization ensures consistent user experience."
        ],
        resolution_strategy="Normalize volume as standard practice.",
        entity_scope="Audio Processing Layer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET03 volume normalization."
    ),
    DoctrineBlock(
        topic="Audio Caching",
        keywords=["audio", "caching", "performance", "latency"],
        conclusion_template="The ET04 engine must cache frequently requested audio to optimize performance.",
        reasoning_framework=(
            "1. Identify frequently requested audio segments.\n"
            "2. Cache audio output for quick retrieval.\n"
            "3. Implement cache eviction policies to manage storage.\n"
            "4. Log all cache hits and misses."
        ),
        key_factors=[
            "Cache hit rate",
            "Eviction policy"
        ],
        primary_authority=["ET04 Performance Guide"],
        burden_holder="Performance Subsystem",
        adversary_position="Caching is unnecessary; generate audio on demand.",
        counter_arguments=[
            "Caching reduces latency for common requests.",
            "On-demand generation increases load."
        ],
        resolution_strategy="Implement caching as standard.",
        entity_scope="Performance Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 audio caching."
    ),
    DoctrineBlock(
        topic="Concurrent TTS Handling",
        keywords=["concurrent", "TTS", "handling", "threading", "performance"],
        conclusion_template="The ET04 engine must handle concurrent TTS requests efficiently.",
        reasoning_framework=(
            "1. Support multi-threaded or asynchronous TTS processing.\n"
            "2. Manage shared resources to prevent contention.\n"
            "3. Monitor system load and adjust concurrency limits.\n"
            "4. Log all concurrent processing events."
        ),
        key_factors=[
            "Thread safety",
            "Resource management"
        ],
        primary_authority=["ET04 Performance Guide"],
        burden_holder="Performance Subsystem",
        adversary_position="Serial processing is sufficient.",
        counter_arguments=[
            "Concurrency improves throughput.",
            "Serial processing limits scalability."
        ],
        resolution_strategy="Implement concurrent handling as standard.",
        entity_scope="Performance Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 concurrent TTS handling."
    ),
    DoctrineBlock(
        topic="API Key Security",
        keywords=["API", "key", "security", "authentication", "encryption"],
        conclusion_template="The ET04 engine must securely manage all API keys for external integrations.",
        reasoning_framework=(
            "1. Store API keys in encrypted configuration files or environment variables.\n"
            "2. Never log or expose API keys in plaintext.\n"
            "3. Rotate API keys regularly and on suspected compromise.\n"
            "4. Restrict access to API keys to authorized processes only.\n"
            "5. Audit all API key usage."
        ),
        key_factors=[
            "Encryption",
            "Access control"
        ],
        primary_authority=["Security Best Practices"],
        burden_holder="Security Subsystem",
        adversary_position="Plaintext storage is sufficient in trusted environments.",
        counter_arguments=[
            "Plaintext storage increases risk of compromise.",
            "Encryption is standard practice."
        ],
        resolution_strategy="Enforce encrypted storage and access controls.",
        entity_scope="Security Layer",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ET03 API key security."
    ),
    DoctrineBlock(
        topic="Error Logging and Monitoring",
        keywords=["error", "logging", "monitoring", "debugging", "analytics"],
        conclusion_template="The ET04 engine must log and monitor all errors for debugging and analytics.",
        reasoning_framework=(
            "1. Log all errors with sufficient context for debugging.\n"
            "2. Monitor error rates and trigger alerts on anomalies.\n"
            "3. Store logs securely and retain for audit purposes.\n"
            "4. Provide dashboards for real-time monitoring."
        ),
        key_factors=[
            "Log detail",
            "Alerting"
        ],
        primary_authority=["ET04 Monitoring Guide"],
        burden_holder="Monitoring Subsystem",
        adversary_position="Minimal logging is sufficient.",
        counter_arguments=[
            "Detailed logging aids debugging.",
            "Monitoring enables proactive issue detection."
        ],
        resolution_strategy="Implement comprehensive logging and monitoring.",
        entity_scope="Monitoring Layer",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ET03 error logging and monitoring."
    ),
    DoctrineBlock(
        topic="Configuration Reloading",
        keywords=["configuration", "reloading", "hot reload", "runtime"],
        conclusion_template="The ET04 engine must support hot reloading of configuration without downtime.",
        reasoning_framework=(
            "1. Monitor configuration files for changes.\n"
            "2. Reload configuration into memory without restarting the engine.\n"
            "3. Validate new configuration before applying.\n"
            "4. Log all reload events."
        ),
        key_factors=[
            "Reload reliability",
            "Validation"
        ],
        primary_authority=["ET04 Configuration Guide"],
        burden_holder="Configuration Subsystem",
        adversary_position="Restarting engine for config changes is acceptable.",
        counter_arguments=[
            "Hot reloading reduces downtime.",
            "Frequent restarts disrupt service."
        ],
        resolution_strategy="Implement hot reloading as standard.",
        entity_scope="Configuration Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 hot reloading."
    ),
    DoctrineBlock(
        topic="Health Check Endpoint",
        keywords=["health", "check", "endpoint", "monitoring", "status"],
        conclusion_template="The ET04 engine must provide a health check endpoint for monitoring.",
        reasoning_framework=(
            "1. Implement a /health endpoint on port 8000.\n"
            "2. Return engine status, API connectivity, and resource usage.\n"
            "3. Ensure endpoint is lightweight and fast.\n"
            "4. Log all health check requests."
        ),
        key_factors=[
            "Endpoint reliability",
            "Status detail"
        ],
        primary_authority=["ET04 Monitoring Guide"],
        burden_holder="Monitoring Subsystem",
        adversary_position="Health checks are unnecessary; monitor externally.",
        counter_arguments=[
            "Built-in health checks provide real-time status.",
            "External monitoring may miss internal issues."
        ],
        resolution_strategy="Implement health check endpoint as standard.",
        entity_scope="Monitoring Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 health check endpoint."
    ),
    DoctrineBlock(
        topic="Rate Limiting",
        keywords=["rate", "limiting", "API", "throttling", "protection"],
        conclusion_template="The ET04 engine must implement rate limiting for all external API calls.",
        reasoning_framework=(
            "1. Monitor API call frequency for each integration.\n"
            "2. Enforce rate limits as defined by external APIs.\n"
            "3. Queue or reject requests that exceed limits.\n"
            "4. Log all rate limit events."
        ),
        key_factors=[
            "Limit enforcement",
            "Queue management"
        ],
        primary_authority=["API Documentation"],
        burden_holder="Integration Subsystem",
        adversary_position="Rate limiting is unnecessary; rely on API errors.",
        counter_arguments=[
            "Proactive limiting prevents service disruption.",
            "API errors may result in bans."
        ],
        resolution_strategy="Implement rate limiting as standard.",
        entity_scope="Integration Layer",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ET03 rate limiting."
    ),
    DoctrineBlock(
        topic="Request Timeout Management",
        keywords=["request", "timeout", "management", "API", "latency"],
        conclusion_template="The ET04 engine must manage request timeouts for all external API calls.",
        reasoning_framework=(
            "1. Set reasonable timeout values for each API integration.\n"
            "2. Abort requests that exceed timeout thresholds.\n"
            "3. Log all timeout events for analysis.\n"
            "4. Allow for configurable timeout settings."
        ),
        key_factors=[
            "Timeout value selection",
            "Abort handling"
        ],
        primary_authority=["API Documentation"],
        burden_holder="Integration Subsystem",
        adversary_position="Timeouts are unnecessary; wait for API response.",
        counter_arguments=[
            "Timeouts prevent resource exhaustion.",
            "Waiting indefinitely may hang the system."
        ],
        resolution_strategy="Implement timeout management as standard.",
        entity_scope="Integration Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 timeout management."
    ),
    DoctrineBlock(
        topic="User Customization Support",
        keywords=["user", "customization", "preferences", "TTS", "settings"],
        conclusion_template="The ET04 engine must support user customization of TTS settings.",
        reasoning_framework=(
            "1. Expose configuration options for voice, rate, pitch, and emotion.\n"
            "2. Store user preferences securely.\n"
            "3. Apply preferences to all TTS requests.\n"
            "4. Log customization usage for analytics."
        ),
        key_factors=[
            "Preference storage",
            "Option coverage"
        ],
        primary_authority=["ET04 User Guide"],
        burden_holder="Customization Subsystem",
        adversary_position="Customization is unnecessary; use defaults.",
        counter_arguments=[
            "Customization improves user satisfaction.",
            "Defaults may not suit all users."
        ],
        resolution_strategy="Support customization as standard.",
        entity_scope="User Layer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ET03 customization support."
    ),
    DoctrineBlock(
        topic="Internationalization and Locale Handling",
        keywords=["internationalization", "locale", "language", "TTS"],
        conclusion_template="The ET04 engine must handle internationalization and locale-specific TTS output.",
        reasoning_framework=(
            "1. Detect language and locale from user input or context.\n"
            "2. Select appropriate voice and pronunciation dictionary.\n"
            "3. Apply locale-specific formatting and conventions.\n"
            "4. Log all locale handling events."
        ),
        key_factors=[
            "Locale detection",
            "Voice selection"
        ],
        primary_authority=["ET04 Internationalization Guide"],
        burden_holder="Locale Subsystem",
        adversary_position="Locale handling is unnecessary; use default language.",
        counter_arguments=[
            "Locale handling improves accessibility.",
            "Defaults may not suit all users."
        ],
        resolution_strategy="Implement locale handling as standard.",
        entity_scope="Locale Layer",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ET03 locale handling."
    ),
    DoctrineBlock(
        topic="SSML Compliance",
        keywords=["SSML", "compliance", "parsing", "TTS"],
        conclusion_template="The ET04 engine must be compliant with the SSML specification.",
        reasoning_framework=(
            "1. Parse SSML input according to the official specification.\n"
            "2. Support all required tags and attributes.\n"
            "3. Provide fallbacks for unsupported features.\n"
            "4. Log all compliance issues."
        ),
        key_factors=[
            "Specification coverage",
            "Fallback handling"
        ],
        primary_authority=["SSML Specification"],
        burden_holder="SSML Processor",
        adversary_position="Partial compliance is sufficient.",
        counter_arguments=[
            "Full compliance ensures interoperability.",
            "Partial compliance may cause issues."
        ],
        resolution_strategy="Aim for full compliance.",
        entity_scope="SSML Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 SSML compliance."
    ),
    DoctrineBlock(
        topic="Output Port Configuration",
        keywords=["output", "port", "configuration", "network"],
        conclusion_template="The ET04 engine must listen on port 8000 for all API requests.",
        reasoning_framework=(
            "1. Configure the engine to bind to port 8000 on startup.\n"
            "2. Ensure no port conflicts with other services.\n"
            "3. Log all port binding events.\n"
            "4. Allow for configurable port via environment variable."
        ),
        key_factors=[
            "Port binding",
            "Conflict detection"
        ],
        primary_authority=["ET04 Configuration Guide"],
        burden_holder="Network Subsystem",
        adversary_position="Port selection can be arbitrary.",
        counter_arguments=[
            "Standard port simplifies integration.",
            "Arbitrary ports may cause confusion."
        ],
        resolution_strategy="Default to 8000; allow override if needed.",
        entity_scope="Network Layer",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ET03 port 8000 usage."
    ),
    DoctrineBlock(
        topic="Secure Transport Enforcement",
        keywords=["secure", "transport", "encryption", "TLS", "HTTPS"],
        conclusion_template="The ET04 engine must enforce secure transport (TLS/HTTPS) for all network communication.",
        reasoning_framework=(
            "1. Require HTTPS for all API endpoints.\n"
            "2. Reject unencrypted HTTP requests.\n"
            "3. Use strong TLS ciphers and certificates.\n"
            "4. Log all transport security events."
        ),
        key_factors=[
            "Encryption strength",
            "Certificate management"
        ],
        primary_authority=["Security Best Practices"],
        burden_holder="Network Subsystem",
        adversary_position="HTTP is sufficient in trusted environments.",
        counter_arguments=[
            "Unencrypted transport exposes sensitive data.",
            "TLS is standard for modern APIs."
        ],
        resolution_strategy="Enforce HTTPS as standard.",
        entity_scope="Network Layer",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ET03 secure transport enforcement."
    ),
    DoctrineBlock(
        topic="Request Tracing",
        keywords=["request", "tracing", "debugging", "performance"],
        conclusion_template="The ET04 engine must implement request tracing for debugging and performance analysis.",
        reasoning_framework=(
            "1. Assign unique trace IDs to all incoming requests.\n"
            "2. Propagate trace IDs through all subsystems and external API calls.\n"
            "3. Log trace information for each processing stage.\n"
            "4. Use trace data for debugging and performance tuning."
        ),
        key_factors=[
            "Trace ID propagation",
            "Log integration"
        ],
        primary_authority=["ET04 Debugging Guide"],
        burden_holder="Debugging Subsystem",
        adversary_position="Tracing is unnecessary; use logs only.",
        counter_arguments=[
            "Tracing provides end-to-end visibility.",
            "Logs alone may not correlate events."
        ],
        resolution_strategy="Implement tracing as standard.",
        entity_scope="Debugging Layer",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ET03 request tracing."
    ),
    DoctrineBlock(
        topic="Resource Usage Monitoring",
        keywords=["resource", "usage", "monitoring", "CPU", "memory"],
        conclusion_template="The ET04 engine must monitor resource usage and report anomalies.",
        reasoning_framework=(
            "1. Track CPU, memory, and disk usage in real-time.\n"
            "2. Trigger alerts on abnormal usage patterns.\n"
            "3. Log resource statistics for analysis.\n"
            "4. Provide dashboards for monitoring."
        ),
        key_factors=[
            "Metric selection",
            "Alerting"
        ],
        primary_authority=["ET04 Monitoring Guide"],
        burden_holder="Monitoring Subsystem",
        adversary_position="Resource monitoring is unnecessary.",
        counter_arguments=[
            "Monitoring prevents outages.",
            "Unmonitored usage may cause failures."
        ],
        resolution_strategy="Implement monitoring as standard.",
        entity_scope="Monitoring Layer",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ET03 resource monitoring."
    ),
    DoctrineBlock(
        topic="Graceful Shutdown Handling",
        keywords=["graceful", "shutdown", "handling", "signal", "cleanup"],
        conclusion_template="The ET04 engine must handle graceful shutdown on termination signals.",
        reasoning_framework=(
            "1. Listen for termination signals (SIGTERM, SIGINT).\n"
            "2. Complete in-flight requests before shutting down.\n"
            "3. Release all resources and close network connections.\n"
            "4. Log shutdown events."
        ),
        key_factors=[
            "Signal handling",
            "Resource cleanup"
        ],
        primary_authority=["ET04 Operations Guide"],
        burden_holder="Operations Subsystem",
        adversary_position="Immediate shutdown is sufficient.",
        counter_arguments=[
            "Graceful shutdown prevents data loss.",
            "Immediate shutdown may corrupt state."
        ],
        resolution_strategy="Implement graceful shutdown as standard.",
        entity_scope="Operations Layer",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ET03 graceful shutdown."
    ),
    DoctrineBlock(
        topic="Startup Self-Test",
        keywords=["startup", "self-test", "diagnostics", "boot"],
        conclusion_template="The ET04 engine must perform a self-test on startup.",
        reasoning_framework=(
            "1. Verify connectivity to all external APIs.\n"
            "2. Check configuration validity and required resources.\n"
            "3. Log self-test results and abort startup on critical failures.\n"
            "4. Provide self-test summary via health check endpoint."
        ),
        key_factors=[
            "Test coverage",
            "Failure handling"
        ],
        primary_authority=["ET04 Operations Guide"],
        burden_holder="Startup Subsystem",
        adversary_position="Self-test is unnecessary; rely on runtime errors.",
        counter_arguments=[
            "Self-test prevents runtime failures.",
            "Early detection improves reliability."
        ],
        resolution_strategy="Implement self-test as standard.",
        entity_scope="Startup Layer",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ET03 startup self-test."
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