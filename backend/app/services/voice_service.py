import whisper
import os

class VoiceService:
    def __init__(self):
        # Load the base model; it's small enough for most systems and fast.
        # This will download the model on first run if not present.
        self.model = None

    def _load_model(self):
        if self.model is None:
            # "base" or "small" model is usually good for simple narration
            self.model = whisper.load_model("base")

    def transcribe_voice(self, audio_path: str, script_text: str = None) -> list[dict]:
        """
        Transcribes the audio file and returns word-level timestamps.
        Returns a list of dicts: [{'word': 'Hello', 'start': 0.0, 'end': 0.5}, ...]
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        self._load_model()
        
        # Transcribe with word timestamps
        options = {"word_timestamps": True}
        if script_text:
            options["initial_prompt"] = script_text
            
        result = self.model.transcribe(audio_path, **options)
        
        word_timings = []
        for segment in result.get("segments", []):
            for word_info in segment.get("words", []):
                word_timings.append({
                    "word": word_info["word"].strip(),
                    "start": word_info["start"],
                    "end": word_info["end"]
                })
                
        return word_timings

voice_service = VoiceService()
