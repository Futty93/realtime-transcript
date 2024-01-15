import whisper
import os
import keyboard
import threading
from queue import Queue
import pyaudio

lang = "en"
# model = whisper.load_model("medium.en")
model = whisper.load_model("medium.en")

def get_live_audio_chunk(chunk_size):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=chunk_size)
    
    try:
        chunk = stream.read(chunk_size)
        return chunk
    except:
        stream.stop_stream()
        stream.close()
        p.terminate()
        return None

q = Queue()

def record_audio():
    chunk_size = 8192 # audio chunk size to use
    directory = "TestSound"
    
    while True:
        chunk = get_live_audio_chunk(chunk_size) #function to get live audio 
        if chunk:  
            q.put(chunk) #put audio chunk in queue to process later
        else: 
            break # no more audio chunks 
            


keep_recording = False

def transcribe_thread():
    global keep_recording
    
    while True:
        if not q.empty() and keep_recording:
            chunk = q.get()
            audio = whisper.bytes_to_audio(chunk) 
            result = model.transcribe(audio, language=lang)
            print(result["text"])
      
x = threading.Thread(target=transcribe_thread)
x.start()

thread = None
        
while True:
    if keyboard.is_pressed(' '):
        keep_recording = True 
        if thread is None:    
          thread = threading.Thread(target=record_audio)
          thread.start()  
    elif not keyboard.is_pressed(' '):
        keep_recording = False
        if thread is not None:
          thread.join()
          thread = None
        print("Transcription finished.")