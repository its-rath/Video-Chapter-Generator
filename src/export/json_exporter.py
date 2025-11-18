import json
from typing import List, Dict
from ..chapter_generation.generator import Chapter
from ..chapter_generation.timestamp_formatter import TimestampFormatter

class JSONExporter:
    """Export chapters as JSON metadata."""

    def export(
        self,
        chapters: List[Chapter],
        video_metadata: Dict,
        output_path: str
    ):
        """
        Export comprehensive JSON metadata.
        """
        data = {
            "video": video_metadata,
            "chapters": [
                {
                    "chapter_number": ch.number,
                    "title": ch.title,
                    "start_seconds": ch.start_time,
                    "end_seconds": ch.end_time,
                    "duration_seconds": ch.duration,
                    "start_timestamp": TimestampFormatter.seconds_to_youtube(ch.start_time),
                    "end_timestamp": TimestampFormatter.seconds_to_youtube(ch.end_time),
                    "description": ch.description
                }
                for ch in chapters
            ],
            "total_chapters": len(chapters),
            "total_duration": chapters[-1].end_time if chapters else 0
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
