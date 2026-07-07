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
            # We only take the first ~200 characters to avoid breaking Whisper's token limit
            # Too long prompts can cause "tensor of 0 elements" reshape errors
            options["initial_prompt"] = script_text[:800]
            
        try:
            result = self.model.transcribe(audio_path, **options)
        except Exception as e:
            # Fallback without initial_prompt if it crashes
            print(f"Whisper crashed with prompt: {e}. Retrying without prompt.")
            result = self.model.transcribe(audio_path, word_timestamps=True)
        
        word_timings = []
        for segment in result.get("segments", []):
            seg_start = segment.get("start", 0.0)
            seg_end = segment.get("end", 0.0)
            for word_info in segment.get("words", []):
                start = word_info.get("start")
                end = word_info.get("end")
                word_timings.append({
                    "word": word_info["word"].strip(),
                    "start": start if start is not None else seg_start,
                    "end": end if end is not None else seg_end
                })
                
        return word_timings

voice_service = VoiceService()
