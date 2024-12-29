import torch
import sounddevice as sd
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from flask import Flask, jsonify
import numpy as np
from langdetect import detect, DetectorFactory

# Đảm bảo ngẫu nhiên của langdetect luôn nhất quán
DetectorFactory.seed = 0

# Kiểm tra xem có GPU không
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# Load Whisper model và processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")

# Đưa mô hình lên GPU (nếu khả dụng)
model.to(device)

# Tạo Flask ứng dụng
app = Flask(__name__)

# Các tham số cấu hình mặc định
DEFAULT_DURATION = 5       # Thời gian ghi âm mặc định (5 giây)
DEFAULT_SAMPLERATE = 16000 # Tần số lấy mẫu mặc định (16000)
DEFAULT_LANGUAGE = 'en'    # Ngôn ngữ mặc định 

# Hàm ghi âm
def record_audio(duration=DEFAULT_DURATION, samplerate=DEFAULT_SAMPLERATE):
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, 
                   channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.")
    return audio.flatten()

# Hàm chuyển âm thanh thành văn bản
def transcribe_audio(audio_array, language=DEFAULT_LANGUAGE, samplerate=DEFAULT_SAMPLERATE):
    # Cấu hình ngôn ngữ cho mô hình
    model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(
        language=language, 
        task="transcribe"
    )
    
    # Xử lý âm thanh và chuyển input sang GPU
    input_features = processor(
        audio_array, 
        sampling_rate=samplerate, 
        return_tensors="pt"
    ).input_features.to(device)

    with torch.no_grad():
        # Generate dựa trên input_features
        predicted_ids = model.generate(input_features)

    # Giải mã kết quả
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    return transcription[0]

# Hàm kiểm tra ngôn ngữ của từng từ
def detect_words_language(text):
    words = text.split()  # Tách câu thành các từ
    for word in words:
        try:
            lang = detect(word)  # Dự đoán ngôn ngữ của từng từ
            if lang not in ['en', 'vi']:  # Kiểm tra xem ngôn ngữ có phải là 'en' hoặc 'vi'
                return False
        except Exception:
            continue  # Bỏ qua lỗi nếu có
    return True

# API endpoint để ghi âm và chuyển văn bản
@app.route('/speech-to-text', methods=['GET'])
def transcribe_audio_endpoint():
    # Sử dụng các tham số mặc định
    duration = DEFAULT_DURATION
    samplerate = DEFAULT_SAMPLERATE
    
    # Ghi âm
    audio_data = record_audio(duration=duration, samplerate=samplerate)
    
    # Chuyển âm thanh thành văn bản
    transcription = transcribe_audio(audio_data, language=DEFAULT_LANGUAGE, samplerate=samplerate)
    
    # Kiểm tra ngôn ngữ của từng từ trong văn bản đã chuyển
    # if not detect_words_language(transcription):
    #     return jsonify({
    #         "status": "error",
    #         "message": "Chỉ hỗ trợ ngôn ngữ tiếng Anh hoặc tiếng Việt."
    #     })
    
    # Trả về kết quả dưới dạng JSON
    return jsonify({
        "status": "success",
        "text": transcription
    })

if __name__ == "__main__":
    # Chạy Flask ứng dụng
    app.run(host="0.0.0.0", port=4000)
