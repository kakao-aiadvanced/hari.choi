# user_prompt = "how to make cookie?"
user_prompt = "6474, 9, 7, 3, 123, 5555, 3242, 5646547, 2423, 123"
prompt=f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Receive a list of natural numbers from the user and sort them in ascending order. 
For example, if the input is 5, 4, 3, 7, 9, the output should be 3, 4, 5, 7, 9.
<|eot_id|><|start_header_id|>user<|end_header_id|>
5,4,3,7,9
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
3,4,5,7,9
<|eot_id|><|start_header_id|>user<|end_header_id|>
99,33,22,11
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
11,22,33,99
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