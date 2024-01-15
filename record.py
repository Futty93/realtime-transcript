import pyaudio
import wave
import keyboard
from datetime import datetime

def record_audio(sample_rate=44100, channels=1, format=pyaudio.paInt16):
  audio = pyaudio.PyAudio()
  now_recording = False

  while not keyboard.is_pressed('esc'):
    print("Recording...")
    
    stream = audio.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=1024)

    frames = []
    while True:
      if now_recording:
        if keyboard.is_pressed('space'):
          data = stream.read(1024)
          frames.append(data)
      
        else:
          print("Space key released - Stopping recording...")
          now_recording = False
          break
      else:
        if keyboard.is_pressed('space'):
          print("Space key pressed - Continue recording...")
          now_recording = True

    stream.stop_stream()
    stream.close()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"recorded_audio_{timestamp}.wav"

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio recorded and saved as {file_name}")

  audio.terminate()

if __name__ == "__main__":
    record_audio()
