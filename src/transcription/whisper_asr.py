from faster_whisper import WhisperModel
from typing import List, Dict, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class TranscriptSegment:
    """Represents a transcript segment with timestamps."""
    id: int
    start: float
    end: float
    text: str
    confidence: float = None

class WhisperTranscriber:
    """
    Wrapper for Faster-Whisper ASR with optimized settings.
    """
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8"
    ):
        logger.info(f"Loading Whisper {model_size} model...")
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe(
        self,
        audio_path: str,
        language: str = "en",
        beam_size: int = 5,
        word_timestamps: bool = True
    ) -> Tuple[List[TranscriptSegment], Dict]:
        """
        Transcribe audio with word-level timestamps.

        Returns:
            Tuple of (segments, metadata)
        """
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=beam_size,
            word_timestamps=word_timestamps,
            vad_filter=True,  # Voice Activity Detection
            vad_parameters={
                "threshold": 0.5,
                "min_speech_duration_ms": 250,
            }
        )

        transcript_segments = []
        for i, segment in enumerate(segments):
            transcript_segments.append(TranscriptSegment(
                id=i,
                start=segment.start,
                end=segment.end,
                text=segment.text.strip(),
                confidence=getattr(segment, 'avg_logprob', None)
            ))

        metadata = {
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "total_segments": len(transcript_segments)
        }
        logger.info(f"Transcribed: {len(transcript_segments)} segments")
        return transcript_segments, metadata