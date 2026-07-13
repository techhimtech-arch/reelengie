import difflib

word_timings = [
    {"word": "Hello", "start": 0.0, "end": 0.5},
    {"word": "world", "start": 0.5, "end": 1.0}
]

script_text = "Hello world! This is a test."

script_words = script_text.split()
whisper_words = [wt['word'] for wt in word_timings]

def clean(w):
    return ''.join(e for e in w.lower() if e.isalnum())

clean_script = [clean(w) for w in script_words]
clean_whisper = [clean(w) for w in whisper_words]

matcher = difflib.SequenceMatcher(None, clean_whisper, clean_script)
aligned_timings = []
last_end = 0.0

for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag == 'equal':
        for i, j in zip(range(i1, i2), range(j1, j2)):
            aligned_timings.append({
                "word": script_words[j],
                "start": word_timings[i]["start"],
                "end": word_timings[i]["end"]
            })
            last_end = word_timings[i]["end"]
    elif tag == 'replace':
        w_start = word_timings[i1]["start"] if i1 < len(word_timings) else last_end
        w_end = word_timings[i2-1]["end"] if i2-1 < len(word_timings) else last_end + 0.5
        s_words = script_words[j1:j2]
        if s_words:
            step = (w_end - w_start) / len(s_words)
            for idx, w in enumerate(s_words):
                aligned_timings.append({
                    "word": w,
                    "start": w_start + idx * step,
                    "end": w_start + (idx + 1) * step
                })
            last_end = w_end
    elif tag == 'insert':
        s_words = script_words[j1:j2]
        for w in s_words:
            aligned_timings.append({
                "word": w,
                "start": last_end,
                "end": last_end + 0.3
            })
            last_end += 0.3
    elif tag == 'delete':
        if i2-1 < len(word_timings):
            last_end = word_timings[i2-1]["end"]

print(aligned_timings)
