from typing import List
from datetime import timedelta

class TimestampFormatter:
    """Format timestamps for various export formats."""

    @staticmethod
    def seconds_to_youtube(seconds: float) -> str:
        """
        Convert seconds to YouTube format.
        Format: MM:SS or HH:MM:SS
        Examples: 2:15, 1:05:30
        """
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

    @staticmethod
    def seconds_to_srt(seconds: float) -> str:
        """
        Convert seconds to SRT format.
        Format: HH:MM:SS,mmm
        Example: 00:02:15,500
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def seconds_to_vtt(seconds: float) -> str:
        """
        Convert seconds to WebVTT format.
        Format: HH:MM:SS.mmm
        Example: 00:02:15.500
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    @staticmethod
    def seconds_to_timecode(seconds: float, fps: int = 30) -> str:
        """
        Convert to SMPTE timecode for EDL.
        Format: HH:MM:SS:FF
        Example: 01:05:30:15
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        frames = int((seconds - int(seconds)) * fps)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"
