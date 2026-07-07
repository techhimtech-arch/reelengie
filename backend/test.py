import traceback
from app.services.voice_service import voice_service

audio_path = r'h:\Zinglabs\reelengie\projects\22\voice\WhatsApp Ptt 2026-07-07 at 11.33.25 AM.mp3'
try:
    voice_service.transcribe_voice(audio_path)
    print('SUCCESS')
except Exception as e:
    traceback.print_exc()
