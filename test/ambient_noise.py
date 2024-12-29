import whisper
import sounddevice as sd
import numpy as np
import random
import wave
from Levenshtein import distance as levenshtein_distance
import time

# Bộ từ điển mẫu
DICTIONARY = [
    "I would like to order a coffee",
    "Please bring me some water",
    "How much does this cost",
    "Can I get the menu",
    "Where is the nearest restroom"
]

# Hàm ghi âm từ micro
def record_audio(filename, duration=5, samplerate=16000):
    print("Recording... Please speak clearly.")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Chờ ghi âm xong
    print("Recording complete.")
    
    # Lưu tệp âm thanh
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    print(f"Audio saved to {filename}")

# Hàm chọn cụm từ ngẫu nhiên
def get_random_phrase():
    return random.choice(DICTIONARY)

# Hàm đánh giá phát âm
def evaluate_pronunciation(reference_text, user_text):
    # Tính khoảng cách chỉnh sửa (Levenshtein Distance)
    distance = levenshtein_distance(reference_text.lower(), user_text.lower())
    accuracy = (1 - distance / len(reference_text)) * 100
    return accuracy

# Main Function
def main():
    # Chọn cụm từ ngẫu nhiên từ bộ từ điển
    random_phrase = get_random_phrase()
    print(f"Your phrase: {random_phrase}")
    print("Please read the phrase aloud after the countdown.")
    
    # Đếm ngược để người dùng chuẩn bị
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Start reading now!")

    # Ghi âm
    audio_file = "user_recording.wav"
    record_audio(audio_file, duration=5)
    
    # Tải mô hình Whisper
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    # Chuyển đổi âm thanh thành văn bản
    print("Transcribing audio...")
    result = model.transcribe(audio_file)
    user_text = result["text"]
    print(f"Transcribed Text: {user_text}")
    
    # Đánh giá phát âm
    accuracy = evaluate_pronunciation(random_phrase, user_text)
    print(f"Pronunciation Accuracy: {accuracy:.2f}%")
    
    # Phản hồi cho người dùng
    if accuracy > 90:
        print("Excellent pronunciation!")
    elif accuracy > 70:
        print("Good pronunciation, but you can improve!")
    else:
        print("Needs improvement. Try again!")

if __name__ == "__main__":
    main()