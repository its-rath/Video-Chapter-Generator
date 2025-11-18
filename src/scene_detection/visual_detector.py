from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector, ThresholdDetector
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class VisualSceneDetector:
    """
    Detect scene transitions using visual content analysis.
    """

    def __init__(
        self,
        threshold: float = 30.0,
        min_scene_len: int = 15
    ):
        self.threshold = threshold
        self.min_scene_len = min_scene_len

    def detect_scenes(
        self,
        video_path: str,
        detection_mode: str = "content"
    ) -> List[Tuple[float, float]]:
        """
        Detect scene boundaries in video.

        Args:
            video_path: Path to video file
            detection_mode: 'content' or 'threshold'

        Returns:
            List of (start_time, end_time) tuples
        """
        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()

        # Add detector based on mode
        if detection_mode == "content":
            scene_manager.add_detector(
                ContentDetector(threshold=self.threshold, min_scene_len=self.min_scene_len)
            )
        else:
            scene_manager.add_detector(
                ThresholdDetector(threshold=self.threshold, min_scene_len=self.min_scene_len)
            )

        # Perform detection
        video_manager.set_downscale_factor()
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list()
        video_manager.release()

        # Convert to timestamps
        scenes = [
            (scene[0].get_seconds(), scene[1].get_seconds())
            for scene in scene_list
        ]
        logger.info(f"Detected {len(scenes)} visual scenes")
        return scenes

    def merge_with_nlp_boundaries(
        self,
        nlp_boundaries: List[float],
        visual_scenes: List[Tuple[float, float]],
        tolerance: float = 5.0
    ) -> List[float]:
        """
        Merge NLP and visual boundaries with tolerance.

        Returns:
            Combined boundary timestamps
        """
        merged = set(nlp_boundaries)

        for start, end in visual_scenes:
            # Check if visual boundary aligns with NLP boundary
            close_to_nlp = any(
                abs(start - nlp_ts) < tolerance
                for nlp_ts in nlp_boundaries
            )
            if not close_to_nlp:
                merged.add(start)

        return sorted(list(merged))
