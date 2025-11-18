from typing import List, Dict
from dataclasses import dataclass
import logging
from src.transcription.whisper_asr import TranscriptSegment

logger = logging.getLogger(__name__)

@dataclass
class Chapter:
    """Represents a video chapter."""
    number: int
    title: str
    start_time: float
    end_time: float
    duration: float
    description: str = ""

class ChapterGenerator:
    """
    Generate chapters from segments and boundaries.
    """

    def __init__(self):
        pass

    def generate_chapters(
        self,
        segments: List[TranscriptSegment],
        boundaries: List[int],
        topics: List[str] = None
    ) -> List[Chapter]:
        """
        Create chapter objects from boundaries.

        Args:
            segments: Transcript segments
            boundaries: Boundary indices
            topics: Optional topic keywords for titles

        Returns:
            List of Chapter objects
        """
        chapters = []

        for i, boundary_idx in enumerate(boundaries):
            # Determine end boundary
            if i < len(boundaries) - 1:
                end_idx = boundaries[i + 1] - 1
            else:
                end_idx = len(segments) - 1

            start_seg = segments[boundary_idx]
            end_seg = segments[end_idx]

            # Extract chapter text
            chapter_text = ". ".join([
                seg.text for seg in segments[boundary_idx:end_idx + 1]
            ])

            # Generate title
            if topics and i < len(topics):
                title = self._create_title_from_topic(topics[i])
            else:
                title = self._create_title_from_text(chapter_text)

            # Create chapter
            chapter = Chapter(
                number=i + 1,
                title=title,
                start_time=start_seg.start,
                end_time=end_seg.end,
                duration=end_seg.end - start_seg.start,
                description=self._create_description(chapter_text)
            )
            chapters.append(chapter)

        logger.info(f"Generated {len(chapters)} chapters")
        return chapters

    def _create_title_from_topic(self, topic: str) -> str:
        """Create human-friendly title from topic keywords."""
        words = topic.split()
        # Capitalize and format
        title = " ".join([w.capitalize() for w in words[:4]])
        return title

    def _create_title_from_text(self, text: str, max_length: int = 50) -> str:
        """Extract title from chapter text."""
        # Simple heuristic: use first meaningful sentence
        sentences = text.split('.')
        if sentences:
            title = sentences[0].strip()[:max_length]
            return title.capitalize()
        return "Chapter"

    def _create_description(self, text: str, max_length: int = 150) -> str:
        """Create short description from chapter text."""
        return text[:max_length].strip() + "..." if len(text) > max_length else text

    def optimize_chapter_durations(
        self,
        chapters: List[Chapter],
        min_duration: int = 60,
        max_duration: int = 600
    ) -> List[Chapter]:
        """
        Merge very short chapters and split very long ones.
        """
        optimized = []
        i = 0
        while i < len(chapters):
            chapter = chapters[i]

            # Merge short chapters
            if chapter.duration < min_duration and i < len(chapters) - 1:
                next_chapter = chapters[i + 1]
                merged = Chapter(
                    number=chapter.number,
                    title=f"{chapter.title} & {next_chapter.title}",
                    start_time=chapter.start_time,
                    end_time=next_chapter.end_time,
                    duration=next_chapter.end_time - chapter.start_time,
                    description=chapter.description
                )
                optimized.append(merged)
                i += 2
            else:
                optimized.append(chapter)
                i += 1

        # Renumber
        for i, chapter in enumerate(optimized):
            chapter.number = i + 1

        logger.info(f"Optimized to {len(optimized)} chapters")
        return optimized
