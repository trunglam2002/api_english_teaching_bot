from flask import Flask, request, jsonify
from bots.review_bot import ReviewBot
from bots.roleplay_bot import RolePlayBot
from bots.study_bot import StudyBot
from edit_table import get_vocab_by_topic, update_one_param, update_vocab
from prompts.prompt_templates import get_grammar_prompt, get_vocab_prompt

# Initialize Flask app
app = Flask(__name__)

# Initialize chatbots
study_bot = StudyBot()
role_play_bot = RolePlayBot()
review_bot = ReviewBot()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Retrieve data from the request
        data = request.json
        print(data)
        choice = data.get('choice')  # 1, 2, or 3
        param1 = data.get('param1')  # Topic, context, or None
        param2 = data.get('param2')  # Subtopic or None
        user_input = data.get('user_input')  # User's input
        conversation_history = data.get('conversation_history', [])

        if not choice or not user_input:
            return jsonify({"error": "Missing 'choice' or 'user_input' parameter."}), 400

        # Choice 1: StudyBot
        if choice == 1:
            if not param1 or not param2:
                return jsonify({"error": "Missing 'param1' or 'param2' for StudyBot."}), 400

            system_prompt = None

            if param1.lower() == 'ngữ pháp':
                prompt_function = get_grammar_prompt
                update_function = update_one_param
                entity_type = "grammar"
            elif param1.lower() == 'từ vựng':
                prompt_function = get_vocab_prompt
                update_function = update_vocab
                entity_type = "vocab"
            else:
                return jsonify({"error": "Invalid 'param1' value for StudyBot."}), 400

            if entity_type == "vocab":
                list_vocab = get_vocab_by_topic(param2)
                system_prompt = prompt_function(list_vocab)
            elif entity_type == "grammar":
                system_prompt = prompt_function(param2)

            keyword = study_bot.analyze_keyword_response(conversation_history)
            chatbot_response = study_bot.ask_gemini(user_input, system_prompt, conversation_history)
            correctness = study_bot.analyze_correct_user_response(chatbot_response)
            print("KeyWord: ", keyword)
            # correctness, keyword = study_bot.extract_analysis_result(analyze_response)
            is_correct = True if correctness == "True" else False
            if entity_type == "vocab" and keyword:
                update_function(is_correct, entity_type, param2, keyword)
            elif entity_type == "grammar":
                update_function(is_correct, entity_type, 'grammar', param2)     

            return jsonify({"response": chatbot_response})

        # Choice 2: RolePlayBot
        elif choice == 2:  # RolePlayBot
            if not param1:
                return jsonify({"error": "Missing 'param1' for RolePlayBot."}), 400
            analysis = role_play_bot.analyze_errors(user_input)
            chatbot_response = role_play_bot.generate_response(user_input, conversation_history, param1)
            return jsonify({"response": chatbot_response, "grammar_errors": analysis})

        # Choice 3: ReviewBot 
        elif choice == 3:  # ReviewBot
            chatbot_response = review_bot.generate_response(user_input, conversation_history)
            question = review_bot.extract_question(chatbot_response)
            correctness = review_bot.analyze_correct_user_response(chatbot_response)
            # correctness, _ = review_bot.extract_analysis_result(analyze_response)
            # is_correct = True if correctness == "True" else False
            print(question)
            update_one_param(correctness, "sample_error", "example", question)
            return jsonify({"response": chatbot_response})
        
        else:
            return jsonify({"error": "Invalid choice."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
