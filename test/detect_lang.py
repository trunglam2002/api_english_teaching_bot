from polyglot.detect import Detector

def detect_language_polyglot(text):
    # Sử dụng Polyglot để phát hiện ngôn ngữ của văn bản đa ngôn ngữ
    try:
        detector = Detector(text)
        languages = [lang.code for lang in detector.languages]
        return languages
    except Exception as e:
        return f"Error detecting language: {str(e)}"

# Test với câu chứa hai ngôn ngữ
if __name__ == "__main__":
    sample_text = "I am learning Python và tôi cũng đang học AI."  # English + Vietnamese

    # Phát hiện ngôn ngữ của câu đa ngôn ngữ
    detected_languages = detect_language_polyglot(sample_text)
    print(f"Detected languages: {detected_languages}")
