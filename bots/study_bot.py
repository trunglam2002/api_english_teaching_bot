import re
from .config.api_config import configure_api, get_model
from prompts.prompt_templates import get_keyword

class StudyBot:
    def __init__(self):
        # Cấu hình API Gemini
        configure_api()
        self.model = get_model()

    def update_conversation(self, object, message, conversation_history):
        """Thêm thông tin vào lịch sử trò chuyện"""
        conversation_history.append(f"{object}: {message}\n")

    def ask_gemini(self, user_input, system_prompt, conversation_history):
        """Gửi prompt tới Gemini API và nhận phản hồi"""
        try:
            self.update_conversation('user', user_input, conversation_history)
            full_prompt =  f"{system_prompt}\n\nLịch sử trò chuyện:\n{conversation_history}\n"
            response = self.model.generate_content(full_prompt)
            self.update_conversation('Chatbot', response, conversation_history)
            return response.text.strip()
        except Exception as e:
            return f"Đã xảy ra lỗi: {e}"
    
    def analyze_correct_user_response(self, chatbot_response):
        if "chính xác" in chatbot_response.lower():
            return True
        elif "chưa chính xác" in chatbot_response.lower():
            return False
        return None
    
    def analyze_keyword_response(self, conversation_history):
        analysis_prompt = get_keyword(conversation_history)
        return self.model.generate_content(analysis_prompt).text.strip()

