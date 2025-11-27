import sys
import logging

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger("debug_startup")
import sys
sys.stdout.reconfigure(line_buffering=True)


logger.info("Starting imports...")

try:
    logger.info("Importing fastapi...")
    import fastapi
    logger.info("Importing torch...")
    import torch
    logger.info("Importing whisper...")
    import faster_whisper
    logger.info("Importing spacy...")
    import spacy
    logger.info("Importing src.api.main...")
    from src.api import main
    logger.info("Import successful!")
except Exception as e:
    logger.error(f"Import failed: {e}")
except KeyboardInterrupt:
    logger.error("Interrupted")
