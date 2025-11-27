from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import logging
from pathlib import Path
import uuid
# from src.audio_extraction.extractor import AudioExtractor
# from src.transcription.whisper_asr import WhisperTranscriber
# from src.segmentation.nlp_segmenter import NLPSegmenter
# from src.scene_detection.visual_detector import VisualSceneDetector
# from src.chapter_generation.generator import ChapterGenerator
# from src.export.youtube_format import YouTubeExporter
# from src.export.subtitle_generator import SubtitleGenerator
# from src.export.json_exporter import JSONExporter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Video Chapter Generator API",
    description="Automatic video chapter generation with ASR and NLP",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
# Initialize components
# Initialize components
# logger.info("Initializing AudioExtractor...")
# audio_extractor = AudioExtractor()

# MOCKING COMPONENTS FOR FRONTEND PREVIEW
logger.info("Mocking heavy components for preview...")

class MockAudioExtractor:
    def extract_audio_moviepy(self, path): 
        # Create a dummy audio file
        audio_path = Path("data/temp/mock_audio.wav")
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        audio_path.touch()
        return str(audio_path), 120.0

class MockTranscriber:
    def transcribe(self, path, language="en"):
        # Return dummy segments
        from dataclasses import dataclass
        @dataclass
        class Segment:
            start: float
            end: float
            text: str
        
        return [
            Segment(0.0, 10.0, "Welcome to this video."),
            Segment(10.0, 60.0, "This is the first chapter content."),
            Segment(60.0, 120.0, "And this is the conclusion.")
        ], {}

class MockSegmenter:
    def generate_embeddings(self, segments): return []
    def cluster_segments(self, embeddings): return []
    def identify_chapter_boundaries(self, segments, labels): return [0, 2] # Start at 0 and 2
    def extract_topics_nmf(self, segments, n_topics=1): return ["Introduction", "Conclusion"]

class MockSceneDetector:
    pass

class MockChapterGenerator:
    def generate_chapters(self, segments, boundaries, topics):
        from dataclasses import dataclass
        @dataclass
        class Chapter:
            number: int
            title: str
            start_time: float
            end_time: float
            duration: float = 0.0
            description: str = ""
            
        return [
            Chapter(1, "Introduction", 0.0, 60.0, 60.0, "Intro description"),
            Chapter(2, "Conclusion", 60.0, 120.0, 60.0, "Conclusion description")
        ]
    
    def optimize_chapter_durations(self, chapters, min_duration=60):
        return chapters

class MockYouTubeExporter:
    def export(self, chapters): return "00:00 Introduction\n01:00 Conclusion"

class MockJSONExporter:
    def export(self, chapters, metadata, path):
        import json
        with open(path, 'w') as f:
            json.dump({"chapters": []}, f)

class MockSubtitleGenerator:
    def generate_srt(self, segments, path):
        with open(path, 'w') as f:
            f.write("1\n00:00:00,000 --> 00:00:10,000\nWelcome to this video.")

audio_extractor = MockAudioExtractor()
transcriber = MockTranscriber()
segmenter = MockSegmenter()
scene_detector = MockSceneDetector()
chapter_gen = MockChapterGenerator()

# Helper classes for export
class YouTubeExporter(MockYouTubeExporter): pass
class JSONExporter(MockJSONExporter): pass
class SubtitleGenerator(MockSubtitleGenerator): pass

logger.info("All components initialized (MOCKED).")

class ChapterRequest(BaseModel):
    video_path: str
    language: str = "en"
    enable_scene_detection: bool = False
    min_chapter_duration: int = 60
    export_formats: list[str] = ["youtube", "json", "srt"]

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/generate-chapters")
async def generate_chapters(
    video: UploadFile = File(...),
    language: str = Form("en"),
    enable_scene_detection: bool = Form(False),
    min_chapter_duration: int = Form(60),
    export_formats: list[str] = Form(["youtube", "json", "srt"])
):
    """
    Generate chapters from uploaded video.

    Process:
    1. Extract audio
    2. Transcribe with Whisper
    3. Segment with NLP
    4. Generate chapters
    5. Export multiple formats
    """
    try:
        # Save uploaded video
        job_id = str(uuid.uuid4())
        video_path = Path("data/input") / f"{job_id}_{video.filename}"

        with open(video_path, "wb") as f:
            content = await video.read()
            f.write(content)

        logger.info(f"Processing video: {video_path}")

        # Step 1: Extract audio
        audio_path, duration = audio_extractor.extract_audio_moviepy(str(video_path))

        # Step 2: Transcribe
        segments, metadata = transcriber.transcribe(audio_path, language=language)

        # Step 3: Generate embeddings and cluster
        embeddings = segmenter.generate_embeddings(segments)
        labels = segmenter.cluster_segments(embeddings)
        boundaries = segmenter.identify_chapter_boundaries(segments, labels)

        # Step 4: Extract topics
        topics = segmenter.extract_topics_nmf(segments, n_topics=len(boundaries))

        # Step 5: Generate chapters
        chapters = chapter_gen.generate_chapters(segments, boundaries, topics)
        chapters = chapter_gen.optimize_chapter_durations(chapters, min_duration=min_chapter_duration)

        # Step 6: Export formats
        output_dir = Path("data/output") / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        # YouTube format
        youtube_path = output_dir / "chapters_youtube.txt"
        if "youtube" in export_formats:
            youtube_content = YouTubeExporter().export(chapters)
            with open(youtube_path, 'w') as f:
                f.write(youtube_content)

        # JSON format
        json_path = output_dir / "chapters.json"
        if "json" in export_formats:
            JSONExporter().export(
                chapters,
                {"filename": video.filename, "duration": duration},
                str(json_path)
            )

        # SRT format
        srt_path = output_dir / "subtitles.srt"
        if "srt" in export_formats:
            SubtitleGenerator().generate_srt(segments, str(srt_path))

        outputs = {}
        if "youtube" in export_formats:
            outputs["youtube"] = str(youtube_path)
        if "json" in export_formats:
            outputs["json"] = str(json_path)
        if "srt" in export_formats:
            outputs["srt"] = str(srt_path)

        return {
            "job_id": job_id,
            "status": "success",
            "chapters_count": len(chapters),
            "duration": duration,
            "outputs": outputs,
            "chapters": [
                {
                    "number": ch.number,
                    "title": ch.title,
                    "start": ch.start_time,
                    "end": ch.end_time
                }
                for ch in chapters
            ]
        }
    except Exception as e:
        logger.error(f"Chapter generation failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/download/{job_id}/{format}")
async def download_output(job_id: str, format: str):
    """Download generated chapter files."""
    output_dir = Path("data/output") / job_id
    format_map = {
        "youtube": "chapters_youtube.txt",
        "json": "chapters.json",
        "srt": "subtitles.srt",
        "vtt": "subtitles.vtt"
    }

    if format not in format_map:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid format: {format}"}
        )

    file_path = output_dir / format_map[format]
    if not file_path.exists():
        return JSONResponse(
            status_code=404,
            content={"error": "File not found"}
        )

    return FileResponse(file_path, filename=file_path.name)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
