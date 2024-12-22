import re
import google.generativeai as genai
from .config.api_config import configure_api, get_model
import random
from edit_table import get_errors
from prompts.prompt_templates import get_review_prompt

class ReviewBot:
    def __init__(self):
        # Cấu hình API của Gemini
        configure_api()
        self.model = get_model()
        self.sentences_with_errors = get_errors()
        self.prompt_template = get_review_prompt(self.sentences_with_errors)

    def update_conversation(self, object, message, conversation_history):
        """Thêm thông tin vào lịch sử trò chuyện"""
        conversation_history.append(f"{object}: {message}\n")

    def get_random_sentence(self):
        remaining_sentences = [s for s in self.sentences_with_errors]
        return random.choice(remaining_sentences) if remaining_sentences else None

    def generate_response(self, user_input, conversation_history):
        self.update_conversation('user', user_input, conversation_history)
        full_prompt = f"{self.prompt_template}\n\nLịch sử trò chuyện:\n{conversation_history}\n"
        try:
            response = self.model.generate_content(full_prompt).text.strip()
            self.update_conversation('Chatbot', response, conversation_history)
            return response
        except Exception as e:
            return f"Lỗi khi gọi API Gemini: {e}"

    def analyze_correct_user_response(self,  chatbot_response):
        if "chính xác" in chatbot_response:
            return True
        elif "chưa chính xác" in chatbot_response:
            return False
        return None

    def extract_question(self, chatbot_respond):
        """Phân tích lấy câu hỏi từ phản hồi của Gemini"""
        pattern = r'"([^"]*)"'
        match = re.search(pattern, chatbot_respond)
        if match:
            question = match.group(1).strip()
            return question
        return None
