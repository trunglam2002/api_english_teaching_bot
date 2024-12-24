from flask import Flask, jsonify
import speech_recognition as sr
import os
import json

app = Flask(__name__)

# Đường dẫn tệp lưu giá trị energy_threshold
THRESHOLD_FILE = "energy_threshold.json"

def load_energy_threshold():
    """Tải giá trị energy_threshold từ tệp, nếu có."""
    if os.path.exists(THRESHOLD_FILE):
        with open(THRESHOLD_FILE, "r") as file:
            return json.load(file).get("energy_threshold", 300)  # Giá trị mặc định là 300
    return 300

def save_energy_threshold(threshold):
    """Lưu giá trị energy_threshold vào tệp."""
    with open(THRESHOLD_FILE, "w") as file:
        json.dump({"energy_threshold": threshold}, file)

def adjust_energy_threshold(recognizer, duration=2):
    """Điều chỉnh ngưỡng năng lượng dựa trên tiếng ồn môi trường."""
    with sr.Microphone() as source:
        print("Điều chỉnh ngưỡng năng lượng dựa trên tiếng ồn môi trường...")
        recognizer.adjust_for_ambient_noise(source, duration=duration)
        print(f"Ngưỡng năng lượng mới: {recognizer.energy_threshold}")
        save_energy_threshold(recognizer.energy_threshold)  # Lưu giá trị sau khi điều chỉnh

def set_default_energy_threshold(recognizer, default_value=300):
    """Đặt ngưỡng năng lượng về một giá trị mặc định."""
    recognizer.energy_threshold = default_value
    save_energy_threshold(default_value)
    print(f"Ngưỡng năng lượng đã đặt về giá trị mặc định: {default_value}")

@app.route('/speech-to-text', methods=['GET'])
def speech_to_text():
    recognizer = sr.Recognizer()

    # Tải giá trị energy_threshold đã lưu
    recognizer.energy_threshold = load_energy_threshold()
    print(f"Energy threshold hiện tại: {recognizer.energy_threshold}")

    # Sử dụng micro để thu âm
    with sr.Microphone() as source:
        try:
            print("Bắt đầu nói...")
            # Ghi âm từ micro
            audio = recognizer.listen(source, timeout=5)
            print("Đang nhận diện giọng nói...")

            # Chuyển đổi âm thanh thành text
            text = recognizer.recognize_google(audio, language='vi-VN')
            print("Đã nhận diện giọng nói thành công :", text)
            return jsonify({"status": "success", "text": text})
        
        except sr.UnknownValueError:
            return jsonify({"status": "error", "message": "Không nhận diện được giọng nói."})
        except sr.RequestError as e:
            return jsonify({"status": "error", "message": f"Lỗi dịch vụ: {e}"})
        except sr.WaitTimeoutError:
            return jsonify({"status": "error", "message": "Không nhận được âm thanh trong thời gian quy định."})

@app.route('/adjust-threshold', methods=['POST'])
def adjust_threshold():
    recognizer = sr.Recognizer()
    adjust_energy_threshold(recognizer)
    return jsonify({"status": "success", "message": "Đã điều chỉnh ngưỡng năng lượng."})

@app.route('/set-default-threshold', methods=['POST'])
def set_default_threshold():
    recognizer = sr.Recognizer()
    default_value = 300  # Bạn có thể thay đổi giá trị mặc định tại đây
    set_default_energy_threshold(recognizer, default_value)
    return jsonify({"status": "success", "message": f"Ngưỡng năng lượng đặt về {default_value}."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
