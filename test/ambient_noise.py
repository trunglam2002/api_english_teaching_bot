import speech_recognition as sr

def recognize_speech_from_microphone():
    """
    Nhận diện giọng nói từ micro bằng Google Web Speech API.
    Hỗ trợ tiếng Việt.
    """
    recognizer = sr.Recognizer()

    # Sử dụng micro để thu âm
    with sr.Microphone() as source:
        print("Đang điều chỉnh tiếng ồn xung quanh... Vui lòng chờ!")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Điều chỉnh ngưỡng năng lượng
        print("Hãy bắt đầu nói...")

        try:
            # Ghi âm và nhận dạng giọng nói
            audio = recognizer.listen(source, timeout=5)  # Chờ trong 5 giây
            print("Đang nhận diện giọng nói...")

            # Sử dụng Google Web Speech API
            text = recognizer.recognize_google(audio, language="vi-VN")  # Chỉ định tiếng Việt
            print("Bạn đã nói:", text)
            return text

        except sr.UnknownValueError:
            print("Không thể nhận diện giọng nói.")
            return None

        except sr.RequestError as e:
            print(f"Lỗi kết nối đến Google Web Speech API: {e}")
            return None

if __name__ == "__main__":
    recognize_speech_from_microphone()
