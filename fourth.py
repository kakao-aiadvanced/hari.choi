# user_prompt = "how to make cookie?"
user_prompt = "how did world war I end?"
prompt=f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a classification bot with the following options:

Math Teacher
History Teacher

If neither option applies, return "None."
To make the instructions clearer and more engaging, let's add some context and examples:

Role Classification Bot

Your task is to classify the given input based on the options provided. You have two main categories:

Math Teacher: If the input is related to teaching mathematics, classify it under this category.
History Teacher: If the input is related to teaching history, classify it under this category.
Instructions:

If the input relates to mathematics (e.g., "teaches algebra," "explains calculus"), return "Math Teacher."
If the input relates to history (e.g., "teaches ancient civilizations," "explains World War II"), return "History Teacher."
If the input does not fit either category, return "None."
Examples:

Input: "Teaches algebra and geometry."
Output: "Math Teacher"

Input: "Explains the events of World War II."
Output: "History Teacher"

Input: "Teaches physical education."
Output: "None"
<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""


import requests

url = "http://localhost:11434/api/generate"
model = "llama3"

data = {
  "model": model,
  "prompt": prompt,
  "stream": False
}

response = requests.post(url, json=data)

# 응답 확인
if response.status_code == 200:
  print("Response:", response.json()["response"])
else:
  print("Failed to get response. Status code:", response.status_code)
  print("Response:", response.text)