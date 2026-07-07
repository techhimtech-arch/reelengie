import math

class CaptionService:
    def __init__(self):
        # Default ASS styling for vertical reels (1080x1920)
        self.ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,60,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def _format_time(self, seconds: float) -> str:
        """
        Format seconds into ASS time format: H:MM:SS.cs
        """
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int((seconds - int(seconds)) * 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    def generate_ass_file(self, word_timings: list[dict], output_path: str):
        """
        Generates an .ass subtitle file with word-level highlighting.
        Groups words into short phrases (approx 3-5 words per subtitle).
        """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.ass_header)
            
            # Group words into chunks
            chunk_size = 4
            for i in range(0, len(word_timings), chunk_size):
                chunk = word_timings[i:i + chunk_size]
                if not chunk:
                    continue
                    
                chunk_start = chunk[0]['start']
                chunk_end = chunk[-1]['end']
                
                start_str = self._format_time(chunk_start)
                end_str = self._format_time(chunk_end)
                
                # For each word in the chunk, we create a dialogue line that highlights that specific word
                for j, target_word in enumerate(chunk):
                    # Dialogue active during the word's duration
                    word_start_str = self._format_time(target_word['start'])
                    word_end_str = self._format_time(target_word['end'])
                    
                    # Build the text with color tags
                    # Primary color is white. We highlight the target word in Yellow (&H0000FFFF)
                    text_parts = []
                    for k, word in enumerate(chunk):
                        if k == j:
                            text_parts.append(f"{{\\c&H0000FFFF&}}{word['word']}{{\\c&H00FFFFFF&}}")
                        else:
                            text_parts.append(word['word'])
                            
                    full_text = " ".join(text_parts)
                    
                    dialogue = f"Dialogue: 0,{word_start_str},{word_end_str},Default,,0,0,0,,{full_text}\n"
                    f.write(dialogue)

caption_service = CaptionService()
