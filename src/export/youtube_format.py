from typing import List
from ..chapter_generation.generator import Chapter
from ..chapter_generation.timestamp_formatter import TimestampFormatter

class YouTubeExporter:
    """Export chapters in YouTube description format."""

    def export(self, chapters: List[Chapter]) -> str:
        """
        Generate YouTube chapters text.

        Format:
        00:00 Introduction
        02:15 Key Concept
        """
        lines = []
        for chapter in chapters:
            timestamp = TimestampFormatter.seconds_to_youtube(chapter.start_time)
            lines.append(f"{timestamp} {chapter.title}")
        return "\n".join(lines)

    def export_with_descriptions(self, chapters: List[Chapter]) -> str:
        """Export with chapter descriptions."""
        lines = []
        for chapter in chapters:
            timestamp = TimestampFormatter.seconds_to_youtube(chapter.start_time)
            lines.append(f"{timestamp} {chapter.title}")
            if chapter.description:
                lines.append(f"  {chapter.description}")
            lines.append("")  # Empty line
        return "\n".join(lines)
