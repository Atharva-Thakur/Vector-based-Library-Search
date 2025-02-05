from transformers import AutoTokenizer, AutoModelForCausalLM
import time

program_start_time = time.time()

start_time = time.time()
# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v0.6")
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v0.6")
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time loading model: {execution_time:.4f} seconds")

# Your input query
query = '''Context:
Marie Curie was a pioneering physicist and chemist, best known for her work on radioactivity. Born in 1867 in Warsaw, Poland, Curie moved to Paris to pursue her studies at the Sorbonne, where she met her husband, Pierre Curie. Together, they discovered the elements polonium and radium. Marie Curie became the first woman to win a Nobel Prize, and she is the only person to have won Nobel Prizes in two different scientific fields—Physics in 1903 (shared with her husband and Henri Becquerel) and Chemistry in 1911 for her work on radium and polonium.
Consider the context and answer the following context

Question:
For which scientific discovery did Marie Curie receive the Nobel Prize in Chemistry in 1911?

Answer:
'''

# Tokenize the input query

start_time = time.time()
inputs = tokenizer(query, return_tensors="pt")
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time tokenizing input: {execution_time:.4f} seconds")

start_time = time.time()
# Generate a response from the model
outputs = model.generate(inputs['input_ids'], max_length=2000, num_return_sequences=1)

# Decode the response into a readable string
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
end_time = time.time()

execution_time = end_time - start_time
# Print the model's response
print(response)
print(f"Execution time generating reponse : {execution_time:.4f} seconds")

program_end_time = time.time()
program_execution_time = program_end_time-program_start_time
print(f"Execution time the entire program : {program_execution_time:.4f} seconds")

#Takes around 10 seconds to generate answer running on CPU.
#Generated content is mostly accurate as long as context contains the answers
#Need to check performance with a GPU