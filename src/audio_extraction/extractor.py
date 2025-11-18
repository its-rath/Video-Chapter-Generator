import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import logging
from moviepy.editor import VideoFileClip
import librosa
import soundfile as sf

logger = logging.getLogger(__name__)

class AudioExtractor:
    """Extract audio from video files using FFmpeg and MoviePy."""

    def __init__(self, temp_dir: str = "data/temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def extract_audio_ffmpeg(
        self,
        video_path: str,
        output_format: str = "wav",
        sample_rate: int = 16000
    ) -> str:
        """
        Extract audio using FFmpeg (fastest method).

        Args:
            video_path: Path to input video file
            output_format: Audio format (wav, mp3, flac)
            sample_rate: Target sample rate in Hz

        Returns:
            Path to extracted audio file
        """
        video_path = Path(video_path)
        audio_path = self.temp_dir / f"{video_path.stem}.{output_format}"

        try:
            cmd = [
                "ffmpeg", "-i", str(video_path),
                "-vn",  # Disable video
                "-acodec", "pcm_s16le",
                "-ar", str(sample_rate),
                "-ac", "1",  # Mono
                "-y",  # Overwrite
                str(audio_path)
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            logger.info(f"Audio extracted: {audio_path}")
            return str(audio_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed: {e.stderr}")
            raise

    def extract_audio_moviepy(
        self,
        video_path: str
    ) -> Tuple[str, float]:
        """Extract audio using MoviePy with duration."""
        video = VideoFileClip(str(video_path))
        duration = video.duration
        audio_path = self.temp_dir / f"{Path(video_path).stem}.wav"

        video.audio.write_audiofile(str(audio_path), verbose=False, logger=None)
        video.close()

        return str(audio_path), duration
