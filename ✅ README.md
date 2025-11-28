***

# 🎬 Video Chapter Generator

Automatically generate **accurate, meaningful chapter markers, titles, and descriptions** for long-form videos using Whisper ASR, advanced NLP topic segmentation, and scene/transition detection.

***

## 🚀 Features

- **Automatic Speech Recognition:** Uses OpenAI Whisper/Faster-Whisper for high-accuracy audio transcription; supports multiple languages.
- **NLP Topic Segmentation:** Segments video content into logical chapters using embeddings, semantic similarity, clustering, and topic modeling.
- **Scene/Transition Detection:** Optionally uses PySceneDetect/OpenCV for visual boundary refinement.
- **Export-Ready Chapters:** Outputs:
    - YouTube timestamp chapters
    - SRT and VTT subtitles
    - JSON metadata (with timestamps, titles, descriptions)
    - EDL, XML, and other NLE/editor marker files
- **High Performance \& Scalability:** Fast processing using GPU (if available), async API, Docker, and horizontal scaling.
- **REST API:** FastAPI-powered endpoints for automation and easy integration.

***

## 📂 Directory Structure

```
video-chapter-generator/
├── src/
│   ├── audio_extraction/
│   ├── transcription/
│   ├── segmentation/
│   ├── scene_detection/
│   ├── chapter_generation/
│   ├── export/
│   └── api/
├── config/
├── tests/
├── scripts/
├── data/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── setup.py
├── .env.example
└── README.md
```


***

## 🛠️ Requirements

- **Python:** 3.8+
- **FFmpeg:** System dependency for audio/video processing
- **Docker/Docker Compose** (for deployment, optional)
- **NVIDIA GPU** (optional, for speedup)

***

## 🔧 Installation

```bash
git clone https://github.com/yourusername/video-chapter-generator.git
cd video-chapter-generator
python -m venv venv
source venv/bin/activate            # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download a Whisper model (first-run only)
python -c "import whisper; whisper.load_model('base')"
```


***

## 🏃‍♂️ Usage

### CLI Example

```python
python scripts/process_video.py --input myvideo.mp4 --output-dir data/output/
```


### API (local development)

```bash
uvicorn src.api.main:app --reload
# Visit http://localhost:8000/docs for the OpenAPI UI
```


### Docker

```bash
docker-compose up -d
# FastAPI service at http://localhost:8000
```


***

## 📤 Export Formats

- YouTube format (for direct copy-paste in description)
- `.srt` / `.vtt` subtitle files
- `.json` chapter metadata
- `.edl`, `.xml` marker files for NLEs
- SEO-optimized text and optional thumbnails/descriptions

***

## 📲 REST API Endpoints

- `POST /generate-chapters`: Upload a video and generate chapter files.
- `GET /download/{job_id}/{format}`: Download output in chosen format.
- `GET /health`: Service status.

See `/docs` endpoint for the full interactive API!

***

## 📝 Example Output (YouTube Chapter Format)

```
00:00 - Introduction
02:15 - Key Concept 1
05:40 - Case Study
09:55 - Conclusion
```


***

## 🧪 Testing

Run all tests with:

```bash
pytest
```

Test coverage includes unit tests for all core modules and integration tests for the full pipeline and API.

***

## 🌍 Deployment

- **Local:** Use the provided `Dockerfile` and `docker-compose.yml` for ease of deployment.
- **Cloud/Kubernetes:** Ready for container orchestration (EKS, GKE, AKS). Add scaling and monitoring as needed.

***

## 📖 Documentation and Examples

- See the included PDF: **[Video Chapter Generation – Complete Implementation Guide](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/c304b67278b2816506843c08c5000009/5a3b3eef-fe27-406e-8dbd-c9c30fc215ba/pdf_21b335de.pdf)** for full code, diagrams, and instructions.
- Sample output files and API usage examples included in the `examples/` folder.

***

## 🏅 Credits

- **ASR:** [OpenAI Whisper](https://github.com/openai/whisper)
- **Embeddings:** [Sentence-BERT](https://www.sbert.net/)
- **Scene Detection:** [PySceneDetect](https://github.com/Breakthrough/PySceneDetect)
- **API:** [FastAPI](https://fastapi.tiangolo.com/)

***

## 📄 License

MIT (see LICENSE for details)

***

**Enhance your video content—automate logical, discoverable, and user-friendly chapters for every video, at production scale!**

***