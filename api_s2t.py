from flask import Flask, request, jsonify
import torch
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration
import sounddevice as sd

app = Flask(__name__)

# Tạo processor và model
processor = WhisperProcessor.from_pretrained("openai/whisper-large")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")

# Tạo pipeline
device = 0 if torch.cuda.is_available() else -1
stt_pipeline = pipeline(
    "automatic-speech-recognition",
    model=model,
    processor=processor,
    device=device
)

def set_language(language_code):
    """
    Cài đặt ngôn ngữ cho mô hình Whisper.
    """
    forced_decoder_ids = processor.get_decoder_prompt_ids(language=language_code, task="transcribe")
    model.config.forced_decoder_ids = forced_decoder_ids

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        # Lấy ngôn ngữ từ request
        language = request.json.get("language", "en")  # Mặc định là tiếng Anh
        if language not in ["en", "vi"]:
            return jsonify({"status": "error", "message": "Ngôn ngữ không được hỗ trợ."})

        # Cài đặt ngôn ngữ
        set_language(language)

        # Ghi âm (hoặc nhận file audio từ request)
        audio_data = record_audio(duration=5, samplerate=16000)

        # Chuyển đổi âm thanh thành text
        result = stt_pipeline(audio_data)
        text = result.get("text", "")
        return jsonify({"status": "success", "text": text, "language": language})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)

def record_audio(duration=5, samplerate=16000):
    """
    Ghi âm từ micro với độ dài (giây) và tần số lấy mẫu chỉ định.
    Trả về numpy array chứa dữ liệu audio.
    """
    print("Đang ghi âm...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate,
                   channels=1, dtype='float32')
    sd.wait()  # Chờ ghi âm xong    
    print("Ghi âm hoàn tất.")
    return audio.flatten()