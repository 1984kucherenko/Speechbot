import pyttsx3
import subprocess

engine = pyttsx3.init()
voices = engine.getProperty('voices')

def text_to_file(text):
    # tmp_file_name = "test_mp3"
    mp3_file = f'data/test.mp3'
    out_file = f'data/test_out.ogg'
    engine.save_to_file(text, mp3_file)
    engine.runAndWait()
    subprocess.run(["ffmpeg", '-i', mp3_file, '-acodec', 'libopus', out_file, '-y'])
    return out_file
# print("script start", flush=True)
# print(text_to_file("Hello my name is Andrii"))
# print("script end", flush=True)
