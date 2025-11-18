import pysrt
from typing import List
from ..transcription.whisper_asr import TranscriptSegment
from ..chapter_generation.timestamp_formatter import TimestampFormatter

class SubtitleGenerator:
    """Generate SRT and VTT subtitle files."""

    def generate_srt(
        self,
        segments: List[TranscriptSegment],
        output_path: str
    ):
        """Generate SRT subtitle file."""
        subs = pysrt.SubRipFile()
        for seg in segments:
            item = pysrt.SubRipItem(
                index=seg.id + 1,
                start=pysrt.SubRipTime(seconds=seg.start),
                end=pysrt.SubRipTime(seconds=seg.end),
                text=seg.text
            )
            subs.append(item)
        subs.save(output_path, encoding='utf-8')

    def generate_vtt(
        self,
        segments: List[TranscriptSegment],
        output_path: str
    ):
        """Generate WebVTT subtitle file."""
        lines = ["WEBVTT\n"]
        for seg in segments:
            start = TimestampFormatter.seconds_to_vtt(seg.start)
            end = TimestampFormatter.seconds_to_vtt(seg.end)
            lines.append(f"{start} --> {end}")
            lines.append(seg.text)
            lines.append("")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
