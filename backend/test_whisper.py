import whisper

model = whisper.load_model("base")
# Use a short fake audio or just see what transcribe outputs
try:
    res = model.transcribe("test.mp3", word_timestamps=True)
    print(res)
except Exception as e:
    print(e)
