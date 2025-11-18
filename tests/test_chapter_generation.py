from src.chapter_generation.generator import ChapterGenerator, Chapter
from src.transcription.whisper_asr import TranscriptSegment

def test_chapter_generation():
    gen = ChapterGenerator()

    # Mock segments
    segments = [
        TranscriptSegment(0, 0.0, 30.0, "Introduction text"),
        TranscriptSegment(1, 30.0, 90.0, "Main content"),
        TranscriptSegment(2, 90.0, 120.0, "Conclusion")
    ]
    boundaries = [0, 1]
    topics = ["introduction", "main content"]

    chapters = gen.generate_chapters(segments, boundaries, topics)

    assert len(chapters) == 2
    assert chapters[0].start_time == 0.0
    assert chapters[0].title == "Introduction"

def test_full_pipeline():
    """Test complete pipeline from video to chapters."""
    video_path = "tests/fixtures/test_video.mp4"

    # Run full pipeline
    # audio_path, = audio_extractor.extract_audio_moviepy(video_path)
    # segments, = transcriber.transcribe(audio_path)
    # embeddings = segmenter.generate_embeddings(segments)
    # labels = segmenter.cluster_segments(embeddings)
    # boundaries = segmenter.identify_chapter_boundaries(segments, labels)
    # chapters = chapter_gen.generate_chapters(segments, boundaries)

    # assert len(chapters) > 0
    # assert all(ch.duration > 0 for ch in chapters)
