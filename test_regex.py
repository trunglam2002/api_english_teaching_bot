import re

# Chuỗi để kiểm tra
text = '''câu trả lời của bạn là hoàn toàn chính xác "Bioderversity" là cánh bướm. Tiếp theo chúng ta sẽ đến với từ "Undermestiate"'''

# Regex để tìm chuỗi trong dấu ngoặc kép
pattern = r'"([^"]*)"'
match = re.search(pattern, text)
if match:
    question = match.group(1).strip() 
# In các chuỗi tìm được
print(question)
