from typing import List
from ..chapter_generation.generator import Chapter
from ..chapter_generation.timestamp_formatter import TimestampFormatter

class EDLExporter:
    """Export chapters as EDL markers for video editors."""

    def export(
        self,
        chapters: List[Chapter],
        output_path: str,
        fps: int = 30
    ):
        """
        Generate CMX-3600 EDL format.
        """
        lines = [
            "TITLE: Video Chapters",
            "FCM: NON-DROP FRAME",
            ""
        ]

        for i, chapter in enumerate(chapters, start=1):
            start_tc = TimestampFormatter.seconds_to_timecode(chapter.start_time, fps)
            end_tc = TimestampFormatter.seconds_to_timecode(chapter.end_time, fps)
            lines.append(f"{i:03d}  BL       V     C        {start_tc} {end_tc} {start_tc} {end_tc}")
            lines.append(f"* FROM CLIP NAME: {chapter.title}")
            lines.append("")

        with open(output_path, 'w') as f:
            f.write("\n".join(lines))
