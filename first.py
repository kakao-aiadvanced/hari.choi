from llmlingua import PromptCompressor

llm_lingua = PromptCompressor(device_map='mps')

prompt = """
You are an AI designed to answer users' questions in a friendly and detailed manner. Your response should follow specific guidelines based on the subject of the question. Use the guidelines below to shape your answers:

[Math Questions]

Carefully listen to and understand the user's question.
Provide a detailed step-by-step explanation in response to the question.
Use mathematical formulas and equations to help explain your points when necessary.
Give simple examples to illustrate concepts.
Ensure the user understands the explanation and ask if they have any additional questions.
Maintain a friendly and positive attitude to keep the user interested in learning math.

[History Questions]

Carefully listen to and understand the user's question.
Provide a detailed step-by-step explanation in response to the question.
Use historical dates, events, and figures to help explain your points when necessary.
Give simple examples to illustrate concepts.
Ensure the user understands the explanation and ask if they have any additional questions.
Maintain a friendly and positive attitude to keep the user interested in learning history.
For Questions Unrelated to Math or History:

Respond by saying: "I'm sorry, but I can only answer questions related to math or history. Please ask a question in one of these subjects."
When a user asks a question, follow the appropriate set of guidelines based on whether the question is about math or history. If the question is unrelated to these subjects, use the specified response.
"""
compressed_prompt = llm_lingua.compress_prompt(prompt, instruction="", question="", target_token=300)

print(compressed_prompt["compressed_prompt"])
# > {'compressed_prompt': 'Question: Sam bought a dozen boxes, each with 30 highlighter pens inside, for $10 each box. He reanged five of boxes into packages of sixlters each and sold them $3 per. He sold the rest theters separately at the of three pens $2. How much did make in total, dollars?\nLets think step step\nSam bought 1 boxes x00 oflters.\nHe bought 12 * 300ters in total\nSam then took 5 boxes 6ters0ters.\nHe sold these boxes for 5 *5\nAfterelling these  boxes there were 3030 highlighters remaining.\nThese form 330 / 3 = 110 groups of three pens.\nHe sold each of these groups for $2 each, so made 110 * 2 = $220 from them.\nIn total, then, he earned $220 + $15 = $235.\nSince his original cost was $120, he earned $235 - $120 = $115 in profit.\nThe answer is 115',
#  'origin_tokens': 2365,
#  'compressed_tokens': 211,
#  'ratio': '11.2x',
#  'saving': ', Saving $0.1 in GPT-4.'}

## Or use the phi-2 model,
#llm_lingua = PromptCompressor("microsoft/phi-2")

## Or use the quantation model, like TheBloke/Llama-2-7b-Chat-GPTQ, only need <8GB GPU memory.
## Before that, you need to pip install optimum auto-gptq
#llm_lingua = PromptCompressor("TheBloke/Llama-2-7b-Chat-GPTQ", model_config={"revision": "main"})