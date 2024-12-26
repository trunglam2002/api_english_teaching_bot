import torch
import sounddevice as sd
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Kiểm tra xem có GPU không
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# Load Whisper model và processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")

# Ví dụ cấu hình cho ngôn ngữ và task
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(
    language="vi", 
    task="transcribe"
)
model.config.suppress_tokens = None  # Bỏ giới hạn token để hỗ trợ song ngữ

# Đưa mô hình lên GPU (nếu khả dụng)
model.to(device)

def record_audio(duration=5, samplerate=16000):
    print("Recording...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, 
                   channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.")
    return audio.flatten()

def transcribe_audio(audio_array, samplerate=16000):
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

if __name__ == "__main__":
    audio_data = record_audio(duration=10, samplerate=16000)
    transcription = transcribe_audio(audio_data, samplerate=16000)
    print("Transcription:")
    print(transcription)
