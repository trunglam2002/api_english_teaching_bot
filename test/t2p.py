from gtts import gTTS
from langdetect import detect
from pydub import AudioSegment
import os

def detect_language_by_word(sentence):
    """
    Phát hiện ngôn ngữ từng từ trong một câu.
    Trả về danh sách (ngôn ngữ, từ).
    """
    words = sentence.split()  # Tách câu thành các từ
    results = []
    for word in words:
        try:
            lang = detect(word)  # Phát hiện ngôn ngữ của từ
            results.append((lang, word))
        except:
            # Nếu không xác định được ngôn ngữ, mặc định là tiếng Việt
            results.append(("vi", word))
    return results

def text_to_speech(text, lang, output_file):
    """
    Chuyển đổi văn bản thành giọng nói với ngôn ngữ chỉ định.
    """
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_file)
    print(f"Đã tạo file âm thanh: {output_file}")

def change_audio_speed(input_file, output_file, speed=1.5):
    """
    Thay đổi tốc độ phát âm thanh.
    """
    audio = AudioSegment.from_file(input_file)
    audio = audio.speedup(playback_speed=speed)
    audio.export(output_file, format="mp3")
    print(f"Đã thay đổi tốc độ âm thanh: {output_file}")

def merge_audio(files, output_file):
    """
    Ghép nhiều file âm thanh thành một file duy nhất.
    """
    combined = AudioSegment.empty()
    for file in files:
        audio = AudioSegment.from_file(file)
        combined += audio
    combined.export(output_file, format="wav")
    print(f"File âm thanh ghép nối đã được lưu: {output_file}")

if __name__ == "__main__":
    # Câu chứa cả tiếng Anh và tiếng Việt
    text = "Hello bạn, how are you hôm nay, tôi khỏe thank you bạn. Tôi thích cup cake?"

    # Phát hiện ngôn ngữ từng từ
    word_segments = detect_language_by_word(text)
    
    # Xử lý TTS cho từng từ
    files = []
    for i, (lang, word) in enumerate(word_segments):
        tts_lang = "en" if lang == "en" else "vi"  # Ánh xạ mã ngôn ngữ sang mã TTS
        temp_file = f"word_{i+1}.mp3"
        output_file = f"word_{i+1}_fast.mp3"
        text_to_speech(word, tts_lang, temp_file)
        
        # Thay đổi tốc độ
        change_audio_speed(temp_file, output_file, speed=1.5)
        files.append(output_file)

        # Xóa file tạm ban đầu
        os.remove(temp_file)

    # Ghép nối các file âm thanh lại
    merge_audio(files, "final_output.wav")

    # Xóa các file tạm
    for file in files:
        os.remove(file)

