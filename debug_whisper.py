import logging
logging.basicConfig(level=logging.DEBUG)
print("Importing faster_whisper...")
try:
    from faster_whisper import WhisperModel
    print("Imported WhisperModel")
except Exception as e:
    print(f"Error: {e}")
