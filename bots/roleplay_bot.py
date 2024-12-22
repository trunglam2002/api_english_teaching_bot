import re
import google.generativeai as genai 
from .config.api_config import get_model, configure_api
from prompts.prompt_templates import get_detect_error_prompt, get_roleplay_contexts
from edit_table import update_two_params, insert_sample_error

class RolePlayBot:
    def __init__(self):
        configure_api()
        self.model = get_model()

    def update_conversation(self, object, message, conversation_history):
        """Thêm thông tin vào lịch sử trò chuyện"""
        conversation_history.append(f"{object}: {message}\n")


    def generate_response(self, user_input, conversation_history, context):
        """Generate response based on user input"""
        self.update_conversation('user', user_input, conversation_history)
        # Create chat prompt
        full_prompt = f"{get_roleplay_contexts(context)}\n\nLịch sử trò chuyện:\n{conversation_history}\n"
        try:
            response = self.model.generate_content(full_prompt)
            assistant_response = response.text.strip()
            self.update_conversation('assistant', assistant_response, conversation_history)
            return assistant_response
        except Exception as e:
            return f"Error generating response: {e}"

    def analyze_errors(self, user_response):
        analysis_prompt = get_detect_error_prompt(user_response)
        try:
            response = self.model.generate_content(analysis_prompt)
            analysis = response.text.strip()
            # Extract errors using regex
            error_pattern = r"-\s*(.*?):\s*(.*?)\s-\s.*:\s(.*)"
            errors = re.findall(error_pattern, analysis)
            # Update error statistics
            for error_type, error_subtype, error_fix in errors:
                update_two_params(False, 'error', 
                                  error_type.lower(), 
                                  error_subtype.lower())
                if "không có lỗi" not in error_fix.lower():
                    insert_sample_error('sample_error', user_response, error_fix)
            
            return analysis
        except Exception as e:
            return f"Error analyzing response: {e}"
