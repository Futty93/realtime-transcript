# import sounddevice as sd
# import wave
# import keyboard

# def record_and_save(filename, duration=5, samplerate=44100, channels=1):
#     # 録音
#     recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16')
#     sd.wait()

#     # WAVファイルとして保存
#     with wave.open(filename, 'wb') as wf:
#         wf.setnchannels(channels)
#         wf.setsampwidth(2)
#         wf.setframerate(samplerate)
#         wf.writeframes(recording.tobytes())

# def on_key_event(e):
#     if e.event_type == keyboard.KEY_DOWN and e.name == 'shift':
#         print("Shift key pressed. Recording started.")
#         record_and_save("recorded_audio.wav")
#         print("Recording stopped and saved.")

# keyboard.hook(on_key_event)

# try:
#     # プログラムが終了するまで待機
#     keyboard.wait()
# except KeyboardInterrupt:
#     # Ctrl+C が押されたらプログラムを終了
#     pass
# finally:
#     # フックを解除
#     keyboard.unhook_all()

import sounddevice as sd
import wave
import keyboard
import threading
import time
from datetime import datetime

# 録音中かどうかを示すフラグ
recording_flag = False

def record_and_save(samplerate=44100, channels=1):
    global recording_flag
    
    # 録音
    duration = 5  # 適切な録音時間を設定してください
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16')
    
    # ファイル名にタイムスタンプを組み込む
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recorded_audio_{timestamp}.wav"

    print(f"Recording started. Press Shift again to stop recording. Saving to {filename}")
    
    # 録音中フラグをTrueに設定
    recording_flag = True

    # Shiftキーが離されるまで録音を続ける
    while recording_flag:
        time.sleep(0.1)

    sd.stop()
    sd.wait()

    # WAVファイルとして保存
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

    print("Recording stopped and saved.")

def on_key_event(e):
    global recording_flag

    if e.event_type == keyboard.KEY_DOWN and e.name == 'shift':
        # Shiftキーが押されたら録音スレッドを開始
        if not recording_flag:
            recording_thread = threading.Thread(target=record_and_save)
            recording_thread.start()
    elif e.event_type == keyboard.KEY_UP and e.name == 'shift':
        # Shiftキーが離されたら録音中フラグをFalseに設定
        recording_flag = False

keyboard.hook(on_key_event)

try:
    # プログラムが終了するまで待機
    keyboard.wait()
except KeyboardInterrupt:
    # Ctrl+C が押されたらプログラムを終了
    pass
finally:
    # フックを解除
    keyboard.unhook_all()
